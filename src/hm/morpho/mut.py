"""
This file is part of the HornMorpho package.

Copyright (C) 2023.
Michael Gasser <gasser@indiana.edu>

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
-------------------------------------------------------
Creating an FST from a set of stem mutations.
2023.02.14

"""

import re, os
from .utils import segment
from .semiring import FSSet, UNIFICATION_SR, TOPFSS
#from .fs import FeatStruct
#from .fs import FeatStructParser
from .geez import *

def geezify_CV(c, v):
    '''
    Convert roman cons and vowel to a Geez character.
    v may be '0' in which case the vowelless (ሳድስ) character is returned.
    v may be '0x', where x is a Geez character. In this case this character
    is returned, and c is ignored.
    '''
    if v in '0-_' or not v:
        return ''
    elif len(v) > 1 and v[0] == '0':
        return v[1]
    elif is_geez(c):
        c = romanize(c, 'ees')
    return geezify(c+v, 'ees')

class Mutation:

#    PARSER = FSSet.parse

    # Signifies no change in a stem character.
    NO_CHANGE = '-'

    RULE_RE = re.compile(r'\s*\$\s+(.+)$')
    FEATURES_RE = re.compile(r'\s*(\[.+\])$')
    PATTERN_RE = re.compile(r'\s*(.+)$')

    @staticmethod
    def make_unmutated_arc(fst, unmutated_weight):
        unmutated_weight = UNIFICATION_SR.parse_weight(unmutated_weight)
        fst.add_arc('start', 'start', '**', '**', weight=unmutated_weight)

    @staticmethod
    def make_mutation_states(fst, features, patterns, abbrevs, index):
        weight = UNIFICATION_SR.parse_weight(features)
        feat_state_name = "mut{}".format(index)
#        print("** mutations for {}: {}".format(weight.__repr__(), patterns))
        for pindex, pattern in enumerate(patterns):
            pat_state_name = "{}_{}".format(feat_state_name, pindex)
            source = 'start'
            for cindex, chars in enumerate(pattern):
                if cindex == 0:
                    wt = weight
                else:
                    wt = None
                if cindex == len(pattern) - 1:
                    dest = 'end'
                else:
                    dest = "{}_{}".format(pat_state_name, cindex)
                    fst.add_state(dest)
#                print("  ** creating arc from {} to {} with {}".format(source, dest, chars))
#                print("  *** abbrevs {}".format(list(abbrevs.keys())))
                strings = fst.sub_IOabbrevs(chars, abbrevs)
                strings = [s for s in strings.split(';')]
                for arc_spec in strings:
                    arc = fst._parse_arc(arc_spec)
                    if isinstance(arc, list):
                        # out_string is a stringset label
                        for instring, outstring in arc:
                            fst.add_arc(source, dest, instring, outstring, weight=wt)
                    else:
                        fst.add_arc(source, dest, arc[0], arc[1], weight=wt)
                source = dest

    @staticmethod
    def parse(label, s, cascade=None, fst=None, gen=False, seglevel=2,
              directory='', seg_units=[], abbrevs=None,
              weight_constraint=None, verbose=False):
        """
        Parse an FST from a string consisting of multiple lines from a file.
        Create a new FST if fst is None.
        """
#        print("** Parsing mutation file {}, fst {}, abbrevs {}".format(s, fst, list(abbrevs.keys())))

#        weighting = fst.weighting()

        language = cascade.language

        rules = []
        mutations = {}

        current_feats = ''
        unmutated_weight = None

        # Create start and end states
        if not fst.has_state(label): fst.add_state('start')
        fst._set_initial_state('start')
        fst.set_final('start')
        if not fst.has_state('end'): fst.add_state('end')
        fst.set_final('end')

        lines = s.split('\n')[::-1]

        while lines:
            line = lines.pop().split('#')[0].strip() # strip comments

            if not line: continue

            m = Mutation.RULE_RE.match(line)
            if m:
                rule = m.groups()[0]
#                print("*** rule {}".format(rule))
                if rule[0] == '[':
                    unmutated_weight = rule
                else:
                    rules.append(rule)
                continue

            m = Mutation.FEATURES_RE.match(line)
            if m:
                current_feats = m.groups()[0]
                mutations[current_feats] = []
#                print("*** features {}".format(current_feats))
                continue

            m = Mutation.PATTERN_RE.match(line)
            if m:
                pattern = m.groups()[0].split()
#                print("*** stem pattern {}".format(pattern))
                mutations[current_feats].append(pattern)
                continue

            print("*** Something wrong with {}".format(line))

#        print("** rules: {}".format(rules))
#        print("** mutations: {}".format(mutations))


        if unmutated_weight:
            Mutation.make_unmutated_arc(fst, unmutated_weight)

        for index, (features, patterns) in enumerate(mutations.items()):
            Mutation.make_mutation_states(fst, features, patterns, abbrevs, index)

#        print(fst)

        return fst
