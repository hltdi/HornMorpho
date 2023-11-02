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

    def __init__(self, init, name='', unk=False):
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
        self.conllu = []
        self.id = Word.id
        Word.id += 1

    def __repr__(self):
        return "W{}:{}{}".format(self.id, '*' if self.unk else '', self.name)

    @staticmethod
    def create_unk(name):
        '''
        Create a Word instances for an unanalyzed token.
        '''
        dct = {'string': name, 'pos': 'UNK', 'nsegs': 1}
        return Word([dct], name=name, unk=True)

    def show(self):
        if len(self) == 0:
            print()
        for item in self:
            print(item)

    def remove(self, indices, index_map):
        '''
        Remove the analyses at indices. Update index_map (a list of pairs)
        to reflect the deletions.
        '''
        # Reverse-sort indices to avoid changing items to delete.
        indices.sort(reverse=True)
        to_del = []
        for index in indices:
            del self[index]
            del self.conllu[index]
            for i, iold_new in enumerate(index_map):
                if iold_new[0] == index:
                    to_del.append(i)
                elif iold_new[0] > index:
                    iold_new[1] -= 1
        to_del.sort(reverse=True)
        for index in to_del:
            del index_map[index]

    def merge(self):
        '''
        Possibly merge segmentations for word, if there are alternatives
        '''
        print("\n***Merge word {}".format(self))
        merges = []
        to_del = []
        nsegs = len(self)
        POSs = [('NOUN', 'PROPN'), ('PROPN', 'NOUN')]
        for index1, segs1 in enumerate(self[:-1]):
            for index2, segs2 in enumerate(self[index1+1:]):
                i2 = index1+index2+1
                if i2 in to_del:
                    continue
#                print(" *** Comparing segmentations {} and {}".format(index1, i2))
                c = self.compare_segs(segs1, segs2)
                if c is False:
                    # seg1 and seg2 are identical
#                    merges.append(([index1, i2], {}))
                    to_del.append(i2)
                    continue
                elif c is True:
                    # seg1 and seg2 are different lengths or otherwise incompatible
                    continue
                else:
                    merges.append(([index1, i2], c))
#                else:
#                    print("  *** Diffs {}".format(c))
#                else:
#                    for mindex, merged in c.items():
#                        if merged.get('upos') in POSs:
#                            merges.append((index1, i2, mindex, [('upos', 'NPROPN'), ('xpos', 'NPROPN')]))
        index_map = [[i, i] for i in range(nsegs)]
        if to_del:
            self.remove(to_del, index_map)
        index_map = dict(index_map)
        m = []
        for (i1, i2), diffs in merges:
            if i1 in index_map and i2 in index_map:
                m.append([[index_map[i1], index_map[i2]], diffs])
        print("  ** final merges {}".format(m))
        # Implement merges where possible
        for (i1, i2), diffs in m:
            if len(diffs) == 1:
                # only one difference
                if 'pos' in diffs:
                    d = diffs['pos']
                    self.merge_pos(self[i1], self[i2], d[0], d[1])
        return m

    def merge_pos(self, seg1, seg2, pos1, pos2):
        '''
        Attempt to merge the two segmentations on the basis of their POSs.
        '''
        print("  ** attempting to merge POS for {} and {}".format(seg1, seg2))

    def compare_segs(self, segs1, segs2):
        '''
        Compare the two segmentations (dicts) to see if they can be merged.
        '''
#        print(" ** Comparing {} and {}".format(segs1, segs2))
        if segs1 == segs2:
#            print(" ** segs are equal!")
            return False
        poseq = False
        umeq = False
        udfeq = False
        segseq = True
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
#        print("  ** UM inters {}, diff1 {}, diff2 {}".format(i, d1, d2))
        if not d1 and not d2:
            umeq = True
        udf1 = segs1.get('udfeats')
        udf2 = segs2.get('udfeats')
        i, d1, d2 = Word.compare_udf(udf1, udf2)
        if not d1 and not d2:
            udfeq = True
#        print("  ** UDF inters {}, diff1 {}, diff2 {}".format(i, d1, d2))
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
            if not udfeq:
                diffs['udfeats'] = [d1, d2]
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
