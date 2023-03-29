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

    # Pair of roots
    ROOT_RE = re.compile(r'\s*<(.+?)>(?:\s+(\S+?))?$')
    # Default feature mapping
    DEFAULT_RE = re.compile(r'\s*\$\s*(.+)$')

    @staticmethod
    def make_gram_features(feateq_defaults, scls='A', tcls='A', feat_constraints=None):
        if not feat_constraints:
            classes = "c={},sc={}".format(scls, tcls)
            valence = ["sv=0,v=0", "v=p,v=p", "sv=a,v=a", "sv=as,v=at"]
            return ';'.join(["[{},{}]".format(classes, v) for v in valence])

    @staticmethod
    def make_lextrans_states(fst, entry_pairs, feateq_defaults, scls='A', tcls='A', feat_constraints=None):
        gram_feats = LexTrans.make_gram_features(feateq_defaults, scls=scls, tcls=tcls, feat_constraints=feat_constraints)
        print("*** gram feats {}".format(gram_feats))
#        weight = make_weight(feats, not gen)
        for pair in entry_pairs:
            src = pair[0]
            targ = pair[-1]
            print("** src {}, targ {}".format(src, targ))
            src_root, src_feats = src
            targ_root, targ_feats = targ
            src_root = src_root.split()
            targ_root = targ_root.split()
            state_name = "{}>{}".format(''.join(src_root), ''.join(targ_root))
            root_feats = []
            states = []
            for index, (schar, tchar) in enumerate(zip(src_root, targ_root)):
                position = index + 1
                states.append("{}{}".format(state_name, position))
                root_feats.append("s{}={},{}={}".format(position, schar, position, tchar))
            root_feats = ','.join(root_feats)
            print("*** states {}".format(states))
            print("*** root_feats {}".format(root_feats))
                
#            for cindex, chars in enumerate(pattern):
#                if cindex == 0:
#                    wt = weight
#                else:
#                    wt = None
#                if cindex == len(pattern) - 1:
#                    dest = 'end'
#                else:
#                    dest = "{}_{}".format(pat_state_name, cindex)
#                    fst.add_state(dest)
#                print("  ** creating arc from {} to {} with {}".format(source, dest, chars))
#                strings = fst.sub_IOabbrevs(chars, abbrevs)
#                strings = [s for s in strings.split(';')]
#                for arc_spec in strings:
#                    arc = fst._parse_arc(arc_spec)
#                    if isinstance(arc, list):
#                        # out_string is a stringset label
#                        for instring, outstring in arc:
#                            fst.add_arc(source, dest, instring, outstring, weight=wt)
#                    else:
#                        fst.add_arc(source, dest, arc[0], arc[1], weight=wt)
#                source = dest

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

        entry_pairs = []

        feateq_defaults = {}

        default_feats = []

#        rules = []

        # Create start and end states
        if not fst.has_state(label): fst.add_state('start')
        fst._set_initial_state('start')
        fst.set_final('start')
        if not fst.has_state('end'): fst.add_state('end')
        fst.set_final('end')

        entries = [ss.strip() for ss in s.split(LexTrans.lexsep)[::-1]]

        while entries:

            entry = entries.pop()

            entry_pair = []

            for line in entry.split("\n"):
                line = line.split('#')[0].strip()

                if not line: continue

#                print("** line {}".format(line))

                m = LexTrans.ROOT_RE.match(line)
                if m:
                    root, feat = m.groups()
                    if feat:
                        feat = feat.strip()
#                    print("** Found root {} feat {}".format(root, feat))
                    entry_pair.append((root, feat))
                    continue

                m = LexTrans.DEFAULT_RE.match(line)
                if m:
                    default = m.groups()[0]
                    if '::' in default:
                        # This is a list of feature maps
                        default = default.split(';')
                        for d in default:
                            feature, maps = d.split('::')
                            maps = maps.split(',')
                            maps = [m.split(':') for m in maps]
                            feateq_defaults[feature] = maps
#                    print("** Found default {}".format(default))
                    continue
                
                print("*** Something wrong with {}".format(line))

            if entry_pair:
                entry_pairs.append(entry_pair)

        print("** entry lists: {}".format(entry_pairs))
        print("** feateq defaults: {}".format(feateq_defaults))

        LexTrans.make_lextrans_states(fst, entry_pairs, feateq_defaults)

#        print(fst)

        return fst
