"""
This file is part of HornMorpho, which is part of the PLoGS project.

    <http://homes.soic.indiana.edu/gasser/plogs.html>

    Copyleft 2023.
    PLoGS and Michael Gasser <gasser@indiana.edu>.

    morfo is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    morfo is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with morfo.  If not, see <http://www.gnu.org/licenses/>.
--------------------------------------------------------------------
Author: Michael Gasser <gasser@indiana.edu>

Representation of 'items': words, MWEs, punctuation, numerals.
2023-09-18
"""

class Word(list):

    id = 0
    POS = {frozenset(['N', 'PROPN']): "NPROPN"}

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
        Word.id += 1

    def __repr__(self):
        return "W{}:{}{}".format(self.id, '*' if self.unk else '', self.name)

    def show(self):
        if len(self) == 0:
            print()
        for item in self:
            print(item)

    @staticmethod
    def create_unk(name):
        '''
        Create a Word instances for an unanalyzed token.
        '''
        dct = {'string': name, 'pos': 'UNK', 'nsegs': 1}
        return Word([dct], name=name, unk=True)

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

    def merge1(self, merges, to_del, verbosity=0):
        for index1, (segs1, csegs1) in enumerate(zip(self[:-1], self.conllu[:-1])):
            for index2, (segs2, csegs2) in enumerate(zip(self[index1+1:], self.conllu[index1+1:])):
                i2 = index1+index2+1
                if i2 in to_del:
                    continue
                if verbosity:
                    print(" *** Comparing segmentations {} and {}".format(index1, i2))
                c = self.compare_segs(segs1, segs2, csegs1, csegs2)
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

    def merge(self, verbosity=0):
        '''
        Possibly merge segmentations for word, if there are alternatives
        '''
        if verbosity:
            print("***Merge word {}".format(self))
        merges = []
        to_del = []
        nsegs = len(self)

        self.merge1(merges, to_del, verbosity=verbosity)

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
            if len(diffs) == 1:
                # only one difference
                if 'pos' in diffs:
                    d = diffs['pos']
                    self.mergePOS(i1, d[0], i2, d[1], to_del, verbosity=verbosity)
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
#                        print("  ** current udfeats: {}".format(self.conllu[i1][0]))
        for c, ui, mf, u1, u2, deli in udf_merges:
            Word.udfeats_merge(c, ui, mf, u1, u2)
            if verbosity:
                print("  ** deleting {}".format(deli))
            if deli not in to_del:
                to_del.append(deli)
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

    def mergePOS(self, i1, pos1, i2, pos2, to_del, verbosity=0):
        pos_merges = self.merges.get('pos', {})
        pset = frozenset([pos1, pos2])
        if pset in pos_merges:
            if POS := pos_merges[pset]:
                if verbosity:
                    print("   ** merging POS in CoNLL-U {}: {}".format(self.conllu[i1], POS))
                # for now just change the first HMToken
                self.conllu[i1][0]['upos'] = POS
                self.conllu[i1][0]['xpos'] = POS
                # and delete the second CoNLL-U and analysis
                to_del.append(i2)

    def compare_segs(self, segs1, segs2, csegs1, csegs2):
        '''
        Compare the two segmentations (dicts) and CoNLL-U segmentations to see if they can be merged.
        '''
#        print(" ** Comparing {}\n and {} ; {}\n and {}".format(segs1, segs2, csegs1, csegs2))
        if segs1 == segs2:
#            print(" ** segs are equal!")
            return False
        poseq = False
        umeq = False
        udfeq = False
        segseq = True
        # Morpheme index where feat differences happen
        mi = -1
        n1 = segs1['nsegs']
        n2 = segs2['nsegs']
        if n1 != n2:
#            print("  ** nsegs: {} ; {}".format(n1, n2))
            return True
        pos1 = segs1.get('pos')
        pos2 = segs2.get('pos')
        if pos1 == pos2:
            poseq = True
#        print("  ** pos: {} ; {}".format(pos1, pos2))
        l1 = segs1.get('lemma')
        l2 = segs2.get('lemma')
#        print("  ** lemmas: {} ; {}".format(l1, l2))
        leq = l1 == l2
        um1 = segs1.get('um')
        um2 = segs2.get('um')
        i, d1, d2 = Word.compare_um(um1, um2)
#        print("  ** UM diff1 {}, diff2 {}".format(d1, d2))
        if not d1 and not d2:
            umeq = True
        udf1 = segs1.get('udfeats')
        udf2 = segs2.get('udfeats')
        i, d1, d2 = Word.compare_udf(udf1, udf2)
        if not d1 and not d2:
            udfeq = True
#        else:
#            print("   ** UDF diff1 {}, diff2 {}".format(d1, d2))
        if d1 and d2:
            for mindex, (m1, m2) in enumerate(zip(csegs1, csegs2)):
#                print("    ** mindex {}".format(mindex))
                f1 = m1['feats']
                f2 = m2['feats']
                if f1 and f2 and all([d in f1 for d in d1]) and all([d in f2 for d in d2]):
#                    print("     ** diff udfeats at index {} in {} and {} ; {} and {}".format(mindex, m1, m2, f1, f2))
                    mi = mindex
        if not poseq and not udfeq:
#            print("  ** both POS and UDF mismatch")
            return True
        if n1 > 1:
            preeq = Word.parts_equal(segs1.get('pre'), segs2.get('pre'))
            sufeq = Word.parts_equal(segs1.get('suf'), segs2.get('suf'))
            stemeq = Word.parts_equal([segs1.get('stem')], [segs2.get('stem')])
            segseq = preeq and stemeq and sufeq
        if poseq and udfeq and leq and segseq:
#            print("  ** POS, UDF, lemmas, and segments match")
            return False
        else:
            diffs = {}
            if not leq:
                diffs['lemma'] = [l1, l2]
            if not udfeq and mi >= 0:
                diffs['udfeats'] = [mi, ','.join(d1), ','.join(d2)]
            if not poseq:
                diffs['pos'] = [pos1, pos2]
            if not segseq:
                diffs['segs'] = [preeq, stemeq, sufeq]
            return diffs
#        print(" ** poseq {}, udfeq {}".format(poseq, udfeq))

    @staticmethod
    def parts_equal(part1, part2):
        '''
        part1 and part2 are prefix, stem, or suffix lists of dicts.
        '''
#        print("  *** parts_equal {} ?= {}".format(part1, part2))
        if len(part1) != len(part2):
            return False
        for s1, s2 in zip(part1, part2):
            str1 = s1 if isinstance(s1, str) else s1.get('string')
            str2 = s2 if isinstance(s2, str) else s2.get('string')
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
