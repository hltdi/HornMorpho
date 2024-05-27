"""
This file is part of HornMorpho, which is part of the PLoGS project.

    <http://homes.soic.indiana.edu/gasser/plogs.html>

    Copyleft 2023, 2024.
    PLoGS and Michael Gasser <gasser@indiana.edu>.

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
--------------------------------------------------------------------
Author: Michael Gasser <gasser@indiana.edu>

Representation of 'items': words, MWEs, punctuation, numerals.
2023-09-18
"""
from .ees import EES

class Word(list):

    id = 0
    POS = {frozenset(['N', 'PROPN']): "NPROPN"}
    empty = {}

    EMPTY = None

    def __init__(self, init, name='', unk=False, merges={}):
        '''
        init is a list of analyses returned by Language.analyze5().
        '''
        list.__init__(self, init)
#        self.posmorph = posmorph
        if not init or unk:
            self.unk = True
        else:
            self.unk = False
        self.name = name
        self.merges = merges
        self.conllu = []
        self.id = Word.id
#        self.is_empty = len(self) == 0
#        self.is_known = not self.unk
        Word.id += 1

    def __repr__(self):
        return "W{}:{}{}{}".format(self.id, '*' if self.unk else '', self.name, "[{}]".format(len(self)) if self.is_known else '')

    def copy(self):
        return Word(self, name=self.name, unk=self.unk, merges=self.merges)

    def show(self):
        if len(self) == 0:
            print()
        for item in self:
            print(item)

#    def string(self):
#        return list.__repr__(self)

    @staticmethod
    def create_unk(name):
        '''
        Create a Word instance for an unanalyzed token.
        '''
        dct = {'seg': name, 'pos': 'UNK', 'nsegs': 1}
        return Word([dct], name=name, unk=True)

    def create_empty(name):
        '''
        Create an empty Word instance.
        '''
#        print("** Creating empty word {}".format(name))
        if not name:
            if not Word.EMPTY:
                Word.EMPTY = Word([], name='EMPTY', unk=True)
            return Word.EMPTY
        dct = {'seg': name, 'pos': 'UNK', 'nsegs': 1}
        return Word([dct], name=name, unk=True)

    def is_empty(self):
        return self.unk

    def is_known(self):
        return not self.unk

    def arrange(self):
        '''
        Be default, sort by freq. (nsegs). Called "arrange" to avoid confusion
        with list.sort().
        '''
        if len(self) > 1:
            self.sort(key=lambda x: x.get('freq'), reverse=True)
#        if len(self) <= 1:
#            return
#        self.sort(key=lambda x: x.get('nsegs', 1))

    def remove(self, indices, index_map):
        '''
        Remove the analyses at indices. Update index_map (a list of pairs)
        to reflect the deletions.
        '''
#        print(" *** removing {}".format(indices))
        # Reverse-sort indices to avoid changing items to delete.
        indices.sort(reverse=True)
        to_del = []
        for index in indices:
            if index >= len(self):
#                print("&& {} trying to delete {}".format(self, index))
                continue
            del self[index]
            del self.conllu[index]
            if index_map:
                for i, iold_new in enumerate(index_map):
                    if iold_new[0] == index:
                        to_del.append(i)
                    elif iold_new[0] > index:
                        iold_new[1] -= 1
        to_del.sort(reverse=True)
        for index in to_del:
            del index_map[index]

    def to_dicts(self, props):
        '''
        Return a list of dicts, each containing values for props only.
        '''
        dicts = []
        if not self.is_empty():
            for analysis in self:
                dct = dict([(k, analysis[k]) for k in props if k in analysis])
                dicts.append(dct)
        return dicts

    def merge1(self, merges, to_del, gemination=False, sep_senses=False, verbosity=0):
        for index1, (segs1, csegs1) in enumerate(zip(self[:-1], self.conllu[:-1])):
            for index2, (segs2, csegs2) in enumerate(zip(self[index1+1:], self.conllu[index1+1:])):
                i2 = index1+index2+1
                if i2 in to_del:
                    continue
                if verbosity:
                    print(" *** Comparing segmentations {} and {}".format(index1, i2))
                c = self.compare_segs(segs1, segs2, csegs1, csegs2, gemination=gemination,
                                      sep_senses=sep_senses)
                if c is False:
                    # seg1 and seg2 are identical
                    if verbosity:
                        print("  *** identical, deleting {}".format(i2))
#                    merges.append(([index1, i2], {}))
                    to_del.append(i2)
                    continue
                elif c is True:
                    # seg1 and seg2 are different lengths or otherwise incompatible
                    continue
                else:
                    merges.append(([index1, i2], c))

    def merge(self, gemination=False, sep_senses=False, verbosity=0):
        '''
        Possibly merge segmentations for word, if there are alternatives
        '''
        if verbosity:
            print("***Merge word {}".format(self))
        merges = []
        to_del = []
        nsegs = len(self)

        self.merge1(merges, to_del, gemination=gemination, sep_senses=sep_senses, verbosity=verbosity)

        index_map = [[i, i] for i in range(nsegs)]
        if to_del:
            self.remove(to_del, index_map)
        index_map = dict(index_map)
        m = []
        for (i1, i2), diffs in merges:
            if i1 in index_map and i2 in index_map:
                m.append([[index_map[i1], index_map[i2]], diffs])
#        print(" *** final merges {}".format(m))
        to_del = []
        # Implement merges where possible
        udf_merges = []
        for (i1, i2), diffs in m:
#            print("** i1 {}, i2 {}, diffs {}".format(i1, i2, diffs))
            if len(diffs) == 1:
                # only one difference
                if 'pos' in diffs:
                    d = diffs['pos']
                    self.mergePOS(i1, d[0], i2, d[1], d[2], to_del, verbosity=verbosity)
                elif 'udfeats' in diffs:
                    d = diffs['udfeats']
                    umindex, ud1, ud2 = d
                    lang_merges = self.merges.get('udfeats', {})
                    if lang_merges:
                        udfmerge = Word.get_merge_udfeats(umindex, ud1, ud2, lang_merges)
                        if udfmerge:
                            if verbosity:
                                print("  ** merging udfeats in CoNLL-U {}: {}; del {}".format(self.conllu[i1], udfmerge, i2))
                            udf_merges.append((self.conllu[i1], umindex, udfmerge, ud1, ud2, i2))
#                elif 'gloss' in diffs:
#                    g = diffs['gloss']
#                    g1, g2, gi = g
#                    self.conllu[i1][gi]['misc'] = g1
#                    self.conllu[i2][gi]['misc'] = g2
            
            # When there's more than one difference, glosses for identical lemmas are also relevant
            if 'gloss' in diffs:
                g = diffs['gloss']
                g1, g2, gi = g
                self.conllu[i1][gi]['misc'] = g1
                self.conllu[i2][gi]['misc'] = g2
#                print("  ** i1 {}, i2 {}, gloss {}".format(i1, i2, diffs['gloss']))

        for c, ui, mf, u1, u2, deli in udf_merges:
            Word.udfeats_merge(c, ui, mf, u1, u2)
            if verbosity:
                print("  ** deleting {}".format(deli))
            if deli not in to_del:
                to_del.append(deli)
        if to_del:
            self.remove(to_del, None)

        if len(self.conllu) > 1 and to_del:
            # Some merging happened but it may be possible to merge POS within these
            merges = []
            to_del = []
            self.merge1(merges, to_del, verbosity=verbosity)
            if merges:
                for (i1, i2), diffs in merges:
                    # only check for POS differences this time?
                    if 'pos' in diffs:
                        d = diffs['pos']
                        self.mergePOS(i1, d[0], i2, d[1], d[2], to_del, verbosity=verbosity)
                if to_del:
                    self.remove(to_del, None)
        if verbosity:
            print(" *** merges: {}".format(m))
        return m

    @staticmethod
    def udfeats_merge(conllu, umindex, mergefeats, ud1, ud2):
        if len(conllu) > 1:
            # multi-morpheme token
            morph = conllu[umindex]
            morphfeats = morph.get('feats')
            if morphfeats:
                # this has to be true
                udcomb = ud1 + ',' + ud2
#                print("   *** udfeats_merge {} ; {} ; {} ; {}".format(morph, morphfeats, mergefeats, udcomb))
                new_feats = Word.replace_udf(morphfeats, udcomb, mergefeats)
#                print("   *** new_feats {}".format(new_feats))
                morph['feats'] = new_feats

    @staticmethod
    def get_merge_udfeats(index, f1, f2, merges):
        '''
        Attempt to merge the udfeats that differentiate two segmentations.
        '''
#        print("   ** merge udfeats {} ; {} {} ; {}".format(index, f1, f2, merges))
        fset = frozenset([f1, f2])
        if fset in merges:
            merged = merges[fset]
#            print("    ** merged udfeats: {}".format(merged))
            return merged

    def mergePOS(self, i1, pos1, i2, pos2, pindex, to_del, verbosity=0):
        pos_merges = self.merges.get('pos', {})
        pset = frozenset([pos1, pos2])
        if verbosity:
            print("  ** mergePOS: {}, {}; {} ; {}".format(i1, i2, pset, pindex))
        if pset in pos_merges:
            if POS := pos_merges[pset]:
                if verbosity:
                    print("   ** merging POS in CoNLL-U {}: {}".format(self.conllu[i1], POS))
                # for now just change the first HMToken
                self.conllu[i1][pindex]['upos'] = POS
                self.conllu[i1][pindex]['xpos'] = POS
                # and delete the second CoNLL-U and analysis
                to_del.append(i2)

    def compare_lemmas(self, segs1, segs2, gemination=False):
        '''
        Compare lemmas and glosses.
        '''
        l1 = segs1.get('lemma')
        l2 = segs2.get('lemma')
        if not gemination:
            if not l1 or not l2:
#                print("** l1 {}, l2 {}".format(l1, l2))
                return False, l1, l2
            l1 = EES.degeminate(l1)
            l2 = EES.degeminate(l2)
        leq = l1 == l2
        return leq, l1, l2

    def compare_glosses(self, segs1, segs2, csegs1, csegs2, leq):
        geq = True
        g1 = g2 = None
        gi = -1
        # see whether the roots/lexemes are different in spite of identical lemmas
        if leq and (g1 := segs1.get('gloss')) and (g2 := segs2.get('gloss')):
            if g1 != g2:
                geq = False
                if len(csegs1) == 1:
                    gi = 0
                else:
                    for mindex, (m1, m2) in enumerate(zip(csegs1[1:], csegs2[1:])):
                        if m1['head'] == mindex + 1:
                            gi = mindex
                            break
        return geq, g1, g2, gi

    def compare_pos(self, segs1, segs2, csegs1, csegs2):
        pi = -1
        pos1 = segs1.get('pos')
        pos2 = segs2.get('pos')
        poseq = pos1 == pos2
        if not poseq:
            # Get the index of the morpheme where the POS difference is
            for mindex, (m1, m2) in enumerate(zip(csegs1, csegs2)):
                p1 = m1['upos']
                p2 = m2['upos']
                if p1 and p2 and p1 != p2:
                    pi = mindex
        return poseq, pos1, pos2, pi

    def compare_segs(self, segs1, segs2, csegs1, csegs2, gemination=False, sep_senses=True):
        '''
        Compare the two segmentations (dicts) and CoNLL-U segmentations to see if they can be merged.
        '''
        if segs1 == segs2:
#            print(" ** segs are equal!")
            return False
        poseq = False
        umeq = False
        udfeq = False
        segseq = True
        # Morpheme index where feat differences happen
        mi = -1
        # Morpheme index where POS differences happend
        n1 = segs1['nsegs']
        n2 = segs2['nsegs']
        if n1 != n2:
#            print("  ** nsegs: {} ; {}".format(n1, n2))
            return True

        poseq, pos1, pos2, pi = self.compare_pos(segs1, segs2, csegs1, csegs2)

        leq, l1, l2 = self.compare_lemmas(segs1, segs2, gemination=gemination)

        geq, g1, g2, gi = self.compare_glosses(segs1, segs2, csegs1, csegs2, leq)

        um1 = segs1.get('um')
        um2 = segs2.get('um')
        i, d1, d2 = Word.compare_um(um1, um2)
        if not d1 and not d2:
            umeq = True

        udf1 = segs1.get('udfeats')
        udf2 = segs2.get('udfeats')
        i, d1, d2 = Word.compare_udf(udf1, udf2)
        if not d1 and not d2:
            udfeq = True
        if d1 and d2:
            # Get the index of the morpheme where the feat difference is
            for mindex, (m1, m2) in enumerate(zip(csegs1, csegs2)):
                f1 = m1['feats']
                f2 = m2['feats']
                if f1 and f2 and all([d in f1 for d in d1]) and all([d in f2 for d in d2]):
                    mi = mindex
        if not poseq and not udfeq:
            return True
        if n1 > 1:
            preeq = Word.parts_equal(segs1.get('pre'), segs2.get('pre'))
            sufeq = Word.parts_equal(segs1.get('suf'), segs2.get('suf'))
            stemeq = Word.parts_equal([segs1.get('stem')], [segs2.get('stem')])
            segseq = preeq and stemeq and sufeq
        if poseq and udfeq and leq and segseq and (geq or not sep_senses):
            return False
        else:
            diffs = {}
            if not leq:
                diffs['lemma'] = [l1, l2]
            elif not geq:
                diffs['gloss'] = [g1, g2, gi]
            if not udfeq and mi >= 0:
                diffs['udfeats'] = [mi, ','.join(d1), ','.join(d2)]
            if not poseq:
                diffs['pos'] = [pos1, pos2, pi]
            if not segseq:
                diffs['segs'] = [preeq, stemeq, sufeq]
            return diffs

    @staticmethod
    def parts_equal(part1, part2):
        '''
        part1 and part2 are prefix, stem, or suffix lists of dicts.
        '''
#        print("  *** parts_equal {} ?= {}".format(part1, part2))
        if len(part1) != len(part2):
            return False
        for s1, s2 in zip(part1, part2):
            str1 = s1 if isinstance(s1, str) else s1.get('seg')
            str2 = s2 if isinstance(s2, str) else s2.get('seg')
            if str1 != str2:
                return False
        return True
            
    @staticmethod
    def compare_um(um1, um2):
        if not um1 or not um2:
            return None, None, None
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
        if not udf1 or not udf2:
            return None, None, None
        udf1 = set(udf1.split('|'))
        udf2 = set(udf2.split('|'))
        inters = list(udf1.intersection(udf2))
        diff1 = list(udf1.difference(udf2))
        diff2 = list(udf2.difference(udf1))
        diff1.sort()
        diff2.sort()
#        diff1 = ','.join(diff1)
#        diff2 = ','.join(diff2)
        return tuple(inters), tuple(diff1), tuple(diff2)

    @staticmethod
    def replace_udf(udf, to_replace, replacement):
        '''
        udf is a standard UDFeats string, with | separating features.
        to_replace is a string consisting of comma-separated features or a list of features.
        replacement is a single feature-value pairs, starting with & or containing /.
        '''
        udf = udf.split('|')
        if isinstance(to_replace, str):
            to_replace = to_replace.split(',')
        result = [replacement]
        for u in udf:
            if u not in to_replace:
                result.append(u)
#        result.sort()
        return "|".join(result)

    def create_attrib_string(self, attribs, all_anals=True):
        '''
        Create a string with the specified attributes (tab-separated) for word analyses,
        only the first unless all_anals is True
        '''
        analyses = self if all_anals else [self[0]]
        lines = []
        for index, analysis in enumerate(analyses):
            attrib_list = [analysis.get(attrib, '') for attrib in attribs]
#            print("{}: attrib list {}".format(self, attrib_list))
            attrib_string = '\t'.join(attrib_list)
            line = "{}\t{}".format(self.name if index == 0 else '', attrib_string)
            lines.append(line)
        return '\n'.join(lines)
