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
FST for root translation.
2023.03.07

"""

import re, os
from .utils import segment
from .semiring import FSSet
from .geez import *
from .ees import EES

make_weight = EES.make_weight

class LexTrans:

    # Signifies no change in a stem character.
    lexsep = '%'

    ROOT_RE = re.compile(r'\s*<(.+?)>\s+(\S+?)$')

    @staticmethod
    def make_lextrans_states(fst, features, patterns, abbrevs, index):
        weight = UNIFICATION_SR.parse_weight(features)
        feat_state_name = "mut{}".format(index)
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
        print("** Parsing lextrans file {}, fst {}".format(s, fst))

        language = cascade.language

        entry_lists = []

#        rules = []

        # Create start and end states
        if not fst.has_state(label): fst.add_state('start')
        fst._set_initial_state('start')
        fst.set_final('start')
        if not fst.has_state('end'): fst.add_state('end')
        fst.set_final('end')

        entries = s.split(LexTrans.lexsep)[::-1]

        while entries:

            entry = entries.pop()

            entry_list = []

            for line in entry.split("\n"):
                line = line.split('#')[0].strip()

                if not line: continue

                m = LexTrans.ROOT_RE.match(line)

                if m:
                    root, feat = m.groups()
                    print("** Found root {} feat {}".format(entry, feat))
                    entry_list.append((entry, feat))
                    continue

            entry_lists.append(entry_list)

                print("*** Something wrong with {}".format(line))

#        print("** rules: {}".format(rules))
#        print("** mutations: {}".format(mutations))

#        print(fst)

        return fst
