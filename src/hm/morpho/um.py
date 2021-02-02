"""
This file is part of HornMorpho, which is a project of PLoGS.

    Copyleft 2020. Michael Gasser.

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
Author: Michael Gasser <gasser@indiana.edu>

Conversion of HornMorpho features to UniMorph features and vice versa.

-- 2020-08-14
   Created.
"""

from .semiring import *
import os, re

class UniMorph:
    """
    Functions for converting between HornMorpho and UniMorph features.
    """

    pos_re = re.compile(r'\s*POS\s*(.*)\s+(.*)$')
    feat_re = re.compile(r'\s*(.*)::\s*([ *:;,._+\w\d]+)$')
    superfeat_re = re.compile(r'\s*(.*)::$')
    subfeat_re = re.compile(r'\s*(.*):\s*(.*)$')

    def __init__(self, language, read=True):
        # A Language instance
        self.language = language
        self.hm2um = {}
        self.um2hm = {}
        if read:
            self.read()
            self.reverse()

    def __repr__(self):
        return "UM:{}".format(self.language.abbrev)

    def convert_um(self, pos, um, verbosity=0):
        """
        Convert a UM feature string to an HM FeatStruct.
        """
        umfeats = set(um.split(';'))
        posmap = self.um2hm.get(pos)
        if verbosity:
            print("Converting {} to HM feats for {}".format(umfeats, pos))
        fs = []
        # UM features already matched; needed to prevent subsets
        # of matched features from matching
        matched_um = []
        if not posmap:
#            print("Warning: no UM2HM map for {}".format(pos))
            return
        for u, map in posmap:
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
                        for ffss in fs:
                            newfs.append(ffss + ',' + map1)
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
            else:
                ff = fs.get(f, None)
            fsvalues.append(ff)
#        fsvalues = tuple([fs.get(f, None) for f in features])
        fsvalues = tuple(fsvalues)
        if verbosity:
            print(" FS values: {}".format(fsvalues))
        ufeat = valuemap.get(fsvalues, False)
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
                    print("CHECKING {} : {} (v type {})".format(f, v, type(v)))
                    print(" FS: {}".format(fs.__repr__()))
#                    print(" MATCHED FEATS: {}".format(feats))
                if isinstance(f, tuple):
                    # we're checking multiple features
                    multmatch = UniMorph.convert_mult(fs, f, v,
                    feats, verbosity=verbosity)
                    if multmatch:
                        feats.extend(f)
                        um.append(multmatch)
                    continue
                if isinstance(v, list):
                    # Subfeats are specified
                    if f not in fs:
                        continue
                    ffss = fs[f]
                    uv = UniMorph.convert_bool(ffss, v, verbosity=verbosity)
                    if uv:
                        um.append(uv)
                        feats.append(f)
                    continue
                if isinstance(v, dict):
                    # Dict gives specific values for f
                    uv = UniMorph.convert1(fs, f, v, feats,
                    verbosity=verbosity)
                    if uv:
                        if verbosity:
                            print(" Adding {} to UM".format(uv))
                        feats.append(f)
                        um.append(uv)
                    continue
                if fs.get(f):
                    # Simple boolean featmap with one feature
                    feats.append(f)
                    um.append(v)
        if verbosity:
            print("UM: {}".format(um))
        if um:
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

    def get_path(self):
        """
        Path for where the UM conversion data is stored for
        the language.
        """
        d = self.language.get_dir()
        return os.path.join(d, self.language.abbrev + ".um")

    def read(self, verbosity=0):
        """
        Read in the UM converstion data.
        """
        path = self.get_path()
        current_pos = ''
        current_supfeat = ''
        current_feats = []
        current_pos_list = []
        try:
            with open(path, encoding='utf8') as file:
                lines = file.read().split('\n')[::-1]
                while lines:
                    line = lines.pop().split('#')[0].strip() # strip comments

                    # ignore empty lines
                    if not line: continue

                    if verbosity:
                        print("Matching line {}".format(line))

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
#                        print("Matched feat {}".format(feat))
                        unless = ''
                        if ':' in value:
                            value = value.split(';;')
                            value = [fv.strip().split(':') for fv in value]
#                            print("value3 {}".format(value))
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
