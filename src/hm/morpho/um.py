"""
This file is part of HornMorpho, which is a project of PLoGS.

    Copyleft 2020-2025. Michael Gasser. gasser@iu.edu

    HornMorpho is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    HornMorpho is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with HornMorpho.  If not, see <http://www.gnu.org/licenses/>.

------------------------------------------------------
Author: Michael Gasser <gasser@iu.edu>

Conversion of HornMorpho features to UniMorph features and vice versa.

-- 2020-08-14
   Created.
"""

from .semiring import *
import os, re
from .utils import match_wild

def expand_udfeats(feats, exclude=None):
    '''
    Convert a string with feature=value pairs separated by |
    to a dict with features as keys, values as values.
    '''
    exclude = exclude or ['PronType', 'ClauseType']
    fv = [fv.split('=') for fv in feats.split('|')]
#    print("** fv {}".format(fv))
    return dict([(f, v) for f, v in fv if f not in exclude])
#    return dict([fv.split('=') for fv in feats.split('|')])

class UniMorph:
    """
    Functions for converting between HornMorpho and UniMorph features.
    """

    pos_re = re.compile(r'\s*POS\s*(.*)\s+(.*)$')
    feat_re = re.compile(r'\s*(.*)::\s*([ *():;,._+/{}\-\w\d]+)$')
    superfeat_re = re.compile(r'\s*(.*)::$')
    subfeat_re = re.compile(r'\s*(.*):\s*(.*)$')
    toUD_re = re.compile(r'\s*->UD\s+(.+)\s+(.+)$')
    abbrev_re = re.compile(r'\s*abbrev\s*(.+)\s+(.+)$')
    sep_convert_re = re.compile(r'\s*sepconvert\s+(.+)$')

    def __init__(self, language, read=True, morph_version=0):
        # A Language instance
        self.language = language
        self.hm2um = {}
        self.um2hm = {}
        self.um2ud = {}
        self.abbrevs = {}
        self.convertdict = {}
        if read:
            self.read(morph_version=morph_version)
            self.reverse()

    def __repr__(self):
        return "UM:{}".format(self.language.abbrev)

    ## Static methods for processing UM and UD features

    @staticmethod
    def create_UDfeats(udfdict, udfalts):
        '''
        udfdict is a feature:value dict.
        udfalts is a list of feature alternatives for ambiguous cases, each a feature:value dict.
        [ [{"Gender[psor]": "Masc", "Number[psor]": "Sing", "Person[psor]": 3}, {"Definite": "Def"}] ]
        '''
#        print("&& udfdict {}".format(udfdict))
        udfeats = UniMorph.udfdict2feats(udfdict, join=True, ls=False)
        if udfalts:
            udf_ambig = [[UniMorph.udfdict2feats(u, join=True, ls=False) for u in udfa] for udfa in udfalts]
            udf_ambig = ["{" + '/'.join(udf) + "}" for udf in udf_ambig]
            udfeats = ','.join([udfeats] + udf_ambig)
        return udfeats

    @staticmethod
    def udfdict2feats(udfdict, join=True, ls=False, feat_convert=None):
        if not udfdict:
            return ''
        if not ls:
            feats = list(udfdict.items())
        else:
            feats = udfdict
        feats.sort()
        if feat_convert:
            for index, (f, v) in enumerate(feats):
                if fconv := feat_convert.get(f):
                    feats[index] = (fconv, v)
#            print("  && converted {}".format(feats))
        feats = ["{}={}".format(feat, val) for feat, val in feats]
        if join:
            return "|".join(feats)
        return feats

    @staticmethod
    def um_intersect(um, features):
        '''
        um is a UM string, features of set of feature strings.
        returns the subset of UM consisting of features in features.
        '''
        um = um.split(';')
        inters = features.intersection(um)
        return ';'.join(inters)

    def expand_feat(self, abbrev):
        return self.abbrevs.get(abbrev, abbrev)

    def convert_um(self, pos, um, verbosity=0):
        """
        Convert a UM feature string to an HM FeatStruct.
        """
        umfeats = set(um.split(';'))
        posmap = self.um2hm.get(pos)
        fs = []
        # UM features already matched; needed to prevent subsets
        # of matched features from matching
        matched_um = []
        if not posmap:
#            print("Warning: no UM2HM map for {}".format(pos))
            return
        if verbosity:
            print("Converting {} to HM feats for {}".format(umfeats, pos))
        for u, map in posmap:
            if verbosity:
                print(" Checking {}:{}".format(u, map))
            if matched_um:
                tupu = (u,) if isinstance(u, str) else u
                if any([(mu.issuperset(tupu)) for mu in matched_um]):
                    if verbosity:
                        print(" Skipping {}".format(u))
                    continue
            matched = False
            if isinstance(u, tuple):
                if umfeats.issuperset(u):
                    if verbosity:
                        print("  {} within {}".format(u, umfeats))
                    matched = True
            elif map[0].endswith("0") and umfeats.issuperset(u):
                # Fail for this POS
                if verbosity:
                    print("  Fail for POS {}".format(pos))
                return
            elif u[0] == '-':
                # Negative UM feature
                u = u[1:]
                if u not in umfeats:
                    if verbosity:
                        print("  {} not in {}".format(u, umfeats))
                    matched = True
            elif u in umfeats:
                if verbosity:
                    print("  {} in {}".format(u, umfeats))
                matched = True
            if matched:
                # No guidelines how to choose so pick first one
                if not any(map):
                    # map could be empty if not default features are
                    # to change
                    continue
                if verbosity:
                    print(" Found maps {}".format(map))
                mu = set(list(u)) if isinstance(u, str) else set(u)
                matched_um.append(mu)
                if fs:
                    newfs = []
                    for map1 in map:
                        map2 = map1.split(',')
                        if verbosity:
                            print("  Checking {}".format(map2))
                        if any([mm in ffss for mm in map2 for ffss in fs]):
                            if verbosity:
                                print("  {} already in {}; abandoning".format(map1, ffss))
                            # In this case don't add any of the features
                            break
                        else:
                            for ffss in fs:
                                if verbosity:
                                    print("  Adding features {} to map {}".format(ffss, map1))
                                newfs.append(ffss + ',' + map1)
                    if newfs:
                        fs = newfs
                else:
                    fs = map
        fs = ["[{}]".format(f) for f in fs]
        if verbosity:
            print("FS: {}".format(fs))
        return fs

    @staticmethod
    def convert1(fs, feature, valuemap, matched_feats=None, verbosity=1):
        """
        Given a feature and an association of values
        with UM features, apply it to a FeatStruc.
        matched_feats is a list of features already matched
        in case there is an unless constraint.
        """
        if verbosity:
            print(" convert1; checking {} : {}".format(feature, valuemap))
        if '!' in valuemap:
            unless = valuemap['!']
            if matched_feats and unless in matched_feats:
                if verbosity:
                    print(" Rejecting because of previous match: {}".format(unless))
                return False
        fsvalue = fs.get(feature, 'None')
#        if fsvalue == True:
#            fsvalue = ''
        um = valuemap.get(fsvalue, False)
        if not um and fsvalue == True:
            # Try '' in place of True (does this ever happen?)
            um = valuemap.get('', False)
        if um and um[0] == '-':
            if verbosity:
                print(" {} is negative; not adding".format(um))
            return False
        if verbosity:
            print("  {}".format(um))
        return um

    @staticmethod
    def convert_bool(fs, featmap, verbosity=1):
        """
        Given a mapping of boolean features to UM features
        (a list), apply it to FeatStruc.
        featmap is a list of feature, UM feature pairs, where
        feature could be a tuple of features.
        """
        if verbosity:
            print(" convert_bool; checking {}".format(featmap))
        for feats, um in featmap:
            found = True
            if isinstance(feats, tuple):
                for feat in feats:
                    if not fs.get(feat):
                        found = False
                        break
            elif feats != None and not fs.get(feats):
                # None is default
                found = False
            if found:
                return um
        return False

    @staticmethod
    def convert_mult(fs, features, valuemap, matched_feats=None,
                     verbosity=1):
        """
        Given a tuple of features and an association
        of value tuples with UM features, apply it
        to a FeatStruc.
        """
        if verbosity:
            print(" convert_mult; checking {} : {}".format(features, valuemap))
        if '!' in valuemap:
            unless = valuemap['!']
            if matched_feats and unless in matched_feats:
                if verbosity:
                    print(" Rejecting because of previous match: {}".format(unless))
                return False
        fsvalues = []
        for f in features:
            if ':' in f:
                # superfeat: subfeat
                super, sub = f.split(':')
                ff = fs.get((super, sub), None)
            elif f[0] == '+':
                # '+' prefixed to feature means to treat True as default
                f = f[1:]
                ff = fs.get(f, True)
            elif f[0] == '-':
                # '-' prefixed to feature means to treat False as default
                f = f[1:]
                ff = fs.get(f, False)
            else:
                # None is 'default' default value when the feature is not present in fs
                ff = fs.get(f, None)
            fsvalues.append(ff)
#        fsvalues = tuple([fs.get(f, None) for f in features])
        fsvalues = tuple(fsvalues)
        if verbosity:
            print(" FS values: {}".format(fsvalues))
        ufeat = valuemap.get(fsvalues, False)
        if not ufeat:
            if verbosity:
                print(" Checking feat combs with wildcard")
            for val, uf in valuemap.items():
                if '*' in val:
                    if verbosity:
                        print("  Checking {}".format(val))
                    if match_wild(fsvalues, val):
                        if verbosity:
                            print("   Matched!")
                        ufeat = uf
#            # * in valuemap is a wildcard; any value for this feature matches
#            ufeat = valuemap.get((fsvalues[0], '*'), False)
        if verbosity:
            print(" ufeat: {}".format(ufeat))
        if ufeat and ufeat[0] == '-':
            # negative feature; don't add it
            if verbosity:
                print(" {} is negative; not adding".format(ufeat))
            return False
        if verbosity:
            if not ufeat:
                print(" No UM feat found")
            else:
                print(" Found UM feat {}".format(ufeat))
        return ufeat

    def convert(self, fs, pos='n', verbosity=0):
        """
        Convert a FeatStruct to a UM string.
        """
        um = []
        feats = []
        posh2u = self.hm2um.get(pos)
        if verbosity:
            print("&& converting {}".format(fs.__repr__()))
        if not fs and pos:
            # No feature structure, but there is a POS;
            # find the UM feat in posh2u
            for f, v in posh2u:
                if f == '':
                    return v
            # No UM feat specified for case of no FS
            return None
        if posh2u:
            for f, v in posh2u:
                if verbosity:
                    print("CHECKING {} : {}".format(f, v))
                    print(" FS: {}".format(fs.__repr__()))
#                    print(" MATCHED FEATS: {}".format(feats))
                if isinstance(f, tuple):
                    # we're checking multiple features
                    multmatch = UniMorph.convert_mult(fs, f, v, feats, verbosity=verbosity)
                    if multmatch:
                        feats.extend(f)
                        if multmatch not in um:
                            for umm in multmatch.split(';'):
                                if umm not in um:
                                    um.append(umm)
                    continue
                if isinstance(v, list):
                    # Subfeats are specified
                    if f not in fs:
                        continue
                    ffss = fs[f]
                    uv = UniMorph.convert_bool(ffss, v, verbosity=verbosity)
                    if uv:
                        if uv not in um:
                            um.append(uv)
                        feats.append(f)
                    continue
                if isinstance(v, dict):
                    # Dict gives specific values for f
                    uv = UniMorph.convert1(fs, f, v, feats, verbosity=verbosity)
                    if uv:
                        if verbosity:
                            print(" Adding {} to UM".format(uv))
                        feats.append(f)
                        if uv not in um:
                            um.append(uv)
                    continue
                if fs.get(f):
                    # Simple boolean featmap with one feature
                    feats.append(f)
                    if v not in um:
                        um.append(v)
        if verbosity:
            print("UM: {}".format(um))
        if um:
            um.sort()
            return ';'.join(um)

    @staticmethod
    def add_um_feat(dct, feat, value):
        """
        Add feat (possibly multiple), to dct, checking first
        whether it's already there.
        """
        if ';' in feat:
            feat = tuple(feat.split(';'))
        if feat in dct:
#            print("Warning: {} already in um2hm dict".format(feat))
            dct[feat].append(value)
        else:
            dct[feat] = [value]

    def reverse(self, verbosity=0):
        """
        Reverse the hm2um list to create a um2hm dict.
        """
        if verbosity:
            print("Reversing hm2um list")
        u2h = {}
        for pos, maps in self.hm2um.items():
            posdict = {}
            for feat, item in maps:
                if not feat:
                    # feat could be empty string
                    continue
                if verbosity:
                    print("feat {}, item {}".format(feat, item))
                if isinstance(item, str):
                    # item is a UM feature which applies
                    # if feat is True
                    feat = "+" + feat
                    UniMorph.add_um_feat(posdict, item, feat)
                    continue
                if isinstance(item, list):
                    # item is a list of pairs:
                    #   boolean_feats, UM feat
                    for feats1, umfeat in item:
                        if feats1 == None:
                            fstring = ''
                        elif isinstance(feats1, str):
                            fstring = "{}=[+{}]".format(feat, feats1)
                        else:
                            s = ','.join(["+" + f1 for f1 in feats1])
                            fstring = "{}=[{}]".format(feat, s)
                        UniMorph.add_um_feat(posdict, umfeat, fstring)
                    continue
                if isinstance(item, dict):
                    # item is a dict of feat value(s), UM feats
                    for values, umfeat in item.items():
                        if verbosity:
                            print("values {}, umfeat {}".format(values, umfeat))
                        if values == '!':
                            # Ignore unless constraint?
                            continue
                        if ';' in umfeat:
                            umfeat = tuple(umfeat.split(';'))
                        if isinstance(feat, tuple):
                            fvs = list(zip(feat, values))
                            fvlist = []
                            supfvlist = {}
                            for f, v in fvs:
                                super = None
                                if ':' in f:
                                    super, f = f.split(':')
                                if isinstance(v, bool):
                                    if v == True:
                                        ff = "+{}".format(f)
                                    else:
                                        ff = "-{}".format(f)
                                elif v == None:
                                    ff = "{}=None".format(f)
                                else:
                                    ff = "{}={}".format(f, v)
                                if super:
                                    if super in supfvlist:
                                        supfvlist[super].append(ff)
                                    else:
                                        supfvlist[super] = [ff]
                                else:
                                    fvlist.append(ff)
                            # if there are superfeats, add them to fvslist
                            for sup, sublist in supfvlist.items():
                                fvlist.append("{}=[{}]".format(sup, ','.join(sublist)))
                            fvstring = ','.join(fvlist)
                            if verbosity:
                                print("  fvstring {}".format(fvstring))
                        elif values == '':
                            fvstring = "+" + feat
                        else:
                            fvstring = "{}={}".format(feat, values)
                        UniMorph.add_um_feat(posdict, umfeat, fvstring)
                    continue
                print("Something wrong with {}".format(item))
            posdict = list(posdict.items())
            posdict.sort(key=lambda x: isinstance(x[0], str))
            u2h[pos] = posdict
        self.um2hm = u2h

    def get_path(self, morph_version=0):
        """
        Path for where the UM conversion data is stored for
        the language.
        """
        d = self.language.get_dir()
        if morph_version:
            return os.path.join(d, "{}_{}.um".format(self.language.abbrev, morph_version))
        return os.path.join(d, self.language.abbrev + ".um")

    def convert2ud(self, um, pos, POS=None, extended=False, nonud=None, return_dict=False):
        """
        Convert a string consisting of UM features to a string consisting of UD features.
        """
#        print("%% converting {} to UD; POS {}; nonud {}".format(um, pos, nonud))
        udfeats = set()
        udalts = []
        um2ud = self.um2ud.get(pos)
        if not um2ud:
            if return_dict:
                return '', ''
            return ''
        for umfeat in um.split(';'):
#            print("  %% umfeat {}".format(umfeat))
            if udfeat := um2ud.get(umfeat):
#                print("    %% udfeat {}".format(udfeat))
                if isinstance(udfeat, tuple):
                    # multiple features
                    ummult, udfeat = udfeat
#                    print("%% ummult {}, udfeat {}".format(ummult, udfeat))
                    if all([(umm in um) for umm in ummult]):
                        if udfeat[0] == '*':
                            if extended:
                                udfeat = udfeat[1:]
                                for udd in udfeat.split(','):
                                    udfeats.add(udd)
                        else:
                            for udd in udfeat.split(','):
                                udfeats.add(udd)
                elif udfeat[0] == '*':
                    if extended:
                        udfeat = udfeat[1:]
                        for udd in udfeat.split(','):
                            udfeats.add(udd)
                else:
                    for udd in udfeat.split(','):
                        featname = udd.split('=')[0]
                        toadd = True
                        if nonud:
                            for nu in nonud:
                                if featname in ['PronType', 'ClauseType']:
                                    toadd = False
                                elif type(nu) is tuple:
                                    if nu[-1] == featname and POS in nu[:-1]:
                                        toadd = False
                                elif nu == featname:
                                    toadd = False
                        if toadd:
                            udfeats.add(udd)
        udfeats = list(udfeats)
        udfeats.sort()
        if return_dict:
            return dict([u.split('=') for u in udfeats]), udalts
        return '|'.join(udfeats)

    def read(self, morph_version=0, verbosity=0):
        """
        Read in the UM conversion data.
        """
        path = self.get_path(morph_version=morph_version)
        print("Loading UM and CoNNL-U conventions from {}".format(path))
        current_pos = ''
        current_supfeat = ''
        current_feats = []
        current_pos_list = []
        try:
#            print("Reading UM file")
            with open(path, encoding='utf8') as file:
                lines = file.read().split('\n')[::-1]
                while lines:
                    line = lines.pop().split('#')[0].strip() # strip comments

                    # ignore empty lines
                    if not line: continue

                    if verbosity:
                        print("Matching line {}".format(line))

                    m = UniMorph.abbrev_re.match(line)
                    if m:
                        abbrev, value = m.groups()
                        self.abbrevs[abbrev] = value
                        continue

                    m = UniMorph.sep_convert_re.match(line)
                    if m:
                        convertdict = m.group(1)
                        convertdict = convertdict.split(',')
                        convertdict = [c.split(':') for c in convertdict]
                        convertdict = dict(convertdict)
                        self.convertdict = convertdict
#                        print("*** convertdict: {}".format(convertdict))
                        continue

                    m = UniMorph.pos_re.match(line)
                    if m:
                        pos, POS = m.groups()
                        if verbosity:
                            print(" Matched POS {}".format(pos))

                        if current_pos:
                            if current_supfeat:
                                current_pos_list.append((current_supfeat, current_feats))
                                current_supfeat = ''
                                current_feats = []
                            if verbosity:
                                print("Setting hm2um for {}".format(current_pos))
                            self.hm2um[current_pos] = current_pos_list
                        current_pos_list = []
                        if POS:
                            current_pos_list.append(("", POS))
                        current_pos = pos
                        self.um2ud[current_pos] = {}
                        continue

                    m = UniMorph.toUD_re.match(line)
                    if m:
                        umfeat, udfeat = m.groups()
                        umfeat = umfeat.strip(); udfeat = udfeat.strip()
                        ## %% Combination UM features, like CAUS;RECP don't work yet!
#                        print("** Matched 2UD rule {}->{}".format(umfeat, udfeat))
                        self.um2ud[current_pos][umfeat.strip()] = udfeat.strip()
                        continue

                    m = UniMorph.superfeat_re.match(line)
                    if m:
                        supfeat = m.group(1)
                        if verbosity:
                            print(" Matched superfeat {}".format(supfeat))
#                        print("Matched superfeat {}".format(supfeat))
                        if current_supfeat:
                            current_pos_list.append((current_supfeat, current_feats))
                            current_supfeat = ''
                            current_feats = []
                        current_supfeat = supfeat
                        continue

                    m = UniMorph.feat_re.match(line)
                    if m:
                        feat, value = m.groups()
                        if verbosity:
                            print(" Matched featmap {}:{}".format(feat, value))
#                        print("  ** Matched feat {}; value {}".format(feat, value))
                        unless = ''
                        if ':' in value:
                            value = value.split(';;')
                            value = [fv.strip().split(':') for fv in value]
#                            print("   ** value {}".format(value))
                            # values could be a list corresponding to feat list
                            for i, (mapv, uv) in enumerate(value):
                                if ',' in mapv:
                                    mapv = mapv.split(',')
                                    for ii, mm in enumerate(mapv):
                                        if mm == 'None':
                                            mapv[ii] = None
                                        elif mm == 'False':
                                            mapv[ii] = False
                                        elif mm == 'True':
                                            mapv[ii] = True
                                        elif mm.isdigit():
                                            mapv[ii] = int(mm)
                                    value[i] = (tuple(mapv), uv)
                                elif mapv == 'False':
                                    value[i] = (False, uv)
                                elif mapv == 'True':
                                    value[i] = (True, uv)
                                elif mapv.isdigit():
                                    value[i] = (int(mapv), uv)
                            value = dict(value)
                        if '!' in feat:
                            feat, unless = feat.split('!')
                            if isinstance(value, dict):
                                value['!'] = unless
                            else:
                                value = {'!': unless, '': value}
                        if ',' in feat:
                            feat = tuple(feat.split(','))
#                        print("Matched feat {}: {}".format(feat, value))
                        if current_supfeat:
                            current_pos_list.append((current_supfeat, current_feats))
                            current_supfeat = ''
                            current_feats = []
                        current_pos_list.append((feat, value))
                        continue
                    m = UniMorph.subfeat_re.match(line)
                    if m:
                        feat, value = m.groups()
                        if verbosity:
                            print(" Matched subfeat map {} : {}".format(feat, value))
#                        print("Matched subfeat {}: {}".format(feat, value))
                        if ',' in feat:
                            feat = tuple(feat.split(','))
                        elif feat == 'None':
                            feat = None
                        current_feats.append((feat, value))
                        continue
                    print("Failed to match line {}".format(line))
            if current_pos:
                if verbosity:
                    print("Setting hm2um for {}".format(current_pos))
                if current_supfeat:
                    current_pos_list.append((current_supfeat, current_feats))
                self.hm2um[current_pos] = current_pos_list

        except IOError as e:
            print("No UM file for {}".format(self.language.abbrev))

    @staticmethod
    def compare_um(um1, um2):
        um1 = set(um1.split(';'))
        um2 = set(um2.split(';'))
        inters = list(um1.intersection(um2))
        diff1 = list(um1.difference(um2))
        diff2 = list(um2.difference(um1))
        diff1.sort()
        diff2.sort()
        return inters, diff1, diff2

    @staticmethod
    def compare_udf(udf1, udf2):
        udf1 = set(udf1.split('|'))
        udf2 = set(udf2.split('|'))
        inters = list(udf1.intersection(udf2))
        diff1 = list(udf1.difference(udf2))
        diff2 = list(udf2.difference(udf1))
        diff1.sort()
        diff2.sort()
        return inters, diff1, diff2
