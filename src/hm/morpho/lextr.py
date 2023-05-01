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
#sourcify_feats = EES.sourcify_feats
targetify_feats = EES.targetify_feats
combine_src_targ_feats = EES.combine_src_targ_feats

class LexTrans:

    # Signifies no change in a stem character.
    lexsep = '%'

    # Pair of roots
    ROOT_RE = re.compile(r'\s*<(.+?)>(?:\s+(\S+?))?$')
    # Default feature mapping
    DEFAULT_RE = re.compile(r'\s*\$\s*(.+)$')

    @staticmethod
    def make_gram_FSSet(feateq_defaults):
        if not feateq_defaults:
            gram = "[v=0,tv=0];[v=p,tv=p];[v=a,tv=a];[v=as,tv=at]"
        else:
            gram = []
            for feat, values in feateq_defaults.items():
#                print("*** feat {}, values {}".format(feat, values))
                gram1 = []
                for svalue, tvalue in values:
                    gram1.append("[{}={},t{}={}]".format(feat, svalue, feat, tvalue))
                gram1 = ';'.join(gram1)
#                print("*** gram1 {}".format(gram1))
                gram.append(gram1)
        print("*** default gram {}".format(gram))
        return [make_weight(g) for g in gram]

    @staticmethod
    def make_lextrans_states(fst, entry_pairs, gram_feats):
#        cls_feats = LexTrans.make_class_FSSet()
#        print("*** gram feats {}".format(gram_feats.__repr__()))
#        print("*** class feats {}".format(cls_feats.__repr__()))
        for pair in entry_pairs:
            src = pair[0]
            targ = pair[-1]
#            print("** src {}, targ {}".format(src, targ))
            src_root, src_feats = src
            targ_root, targ_feats = targ
            src_root = src_root.split()
            targ_root = targ_root.split()
#            src_feats = sourcify_feats(src_feats)
            targ_feats = targetify_feats(targ_feats)
            root_gram_feats = combine_src_targ_feats(src_feats, targ_feats)
#            print("** root_gram_feats {}".format(root_gram_feats))
            root_gram_feats = make_weight(root_gram_feats)
            state_name = "{}>{}".format(''.join(src_root), ''.join(targ_root))
            root_char_feats = []
            states_chars = []
            for index, (schar, tchar) in enumerate(zip(src_root, targ_root)):
                position = index + 1
                states_chars.append(("{}{}".format(state_name, position), schar, tchar))
                root_char_feats.append("{}={},t{}={}".format(position, schar, position, tchar))
            root_char_feats = '[' + ','.join(root_char_feats) + ']'
#            print("** root_char_feats {}".format(root_char_feats))
            root_char_feats = make_weight(root_char_feats)
            weights = [root_char_feats.u(gram_feats[0])]
            weights = [weights[0].u(root_gram_feats)]
            for w in gram_feats[1:]:
                weights.insert(0, w)
#            weights = [root_char_feats.u(gf) for gf in gram_feats]
#            weights = [weight.u(root_gram_feats) for weight in weights]
#            print("*** states {}".format(states_chars))
#            print("*** weights {}".format([weight.__repr__() for weight in weights]))
            src = 'start'
            nstates = len(states_chars)
            # initial states (before stem) and arcs
#            fst.add_state('prefixes')
#            dest = 'prefixes'
            dest = 'start'
            # later simplify the character set to only affix characters
            fst.add_arc(src, dest, '-', '-', weight=None)
            fst.add_arc(src, dest, '**', '**', weight=None)
#            print("  *** Creating arc {}->{}; {}:{}".format(src, dest, '-;**', '-;**'))
            if not fst.has_state('stembound1'):
                fst.add_state('stembound1')
            dest = 'stembound1'
            fst.add_arc(src, dest, '+', '+', weight=None)
#            print("  *** Creating arc {}->{}; {}:{}".format(src, dest, '+', '+'))
            src = 'stembound1'
            if not fst.has_state('stembound2'):
                fst.add_state('stembound2')
            for sindex, (state, schar, tchar) in enumerate(states_chars):
#                print("  *** state {}, schar {}, tchar {}".format(state, schar, tchar))
                wt = None
                if weights:
                    wt = weights.pop()
#                if sindex == 0:
#                    wt = weights.pop()
#                    wt = weights[0]
#                elif sindex == 1:
#                    wt = weights[1]
                if sindex == nstates - 1:
                    dest = 'stembound2'
                else:
                    dest = state
                    fst.add_state(state)
#                print("  *** Creating arc {}->{}; {}:{}".format(src, dest, schar, tchar))
                fst.add_arc(src, dest, schar, tchar, weight=wt)
                src = dest
            if weights:
                print("*** Warning: some weights not included!")
            # post-stem states and arcs
            dest = 'end'
            fst.add_arc(src, dest, '+', '+', weight=None)
#            print("  *** Creating arc {}->{}; {}:{}".format(src, dest, '+', '+'))
            src = 'end'
            fst.add_arc(src, dest, '-', '-', weight=None)
            fst.add_arc(src, dest, '**', '**', weight=None)
#            print("  *** Creating arc {}->{}; {}:{}".format(src, dest, '-;**', '-;**'))
                
    @staticmethod
    def parse(label, s, cascade=None, fst=None, gen=False, seglevel=2,
              directory='', seg_units=[], abbrevs=None,
              weight_constraint=None, verbose=False):
        """
        Parse an FST from a string consisting of multiple lines from a file.
        Create a new FST if fst is None.
        """
#        print("** Parsing lextrans file {}, fst {}".format(s, fst))

        language = cascade.language

        entry_pairs = []

        feateq_defaults = {}

        default_feats = []

#        rules = []

        # Create start and end states
        if not fst.has_state('start'): fst.add_state('start')
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


#        print("** entry lists: {}".format(entry_pairs))
#        print("** feateq defaults: {}".format(feateq_defaults))

        gram_feats = LexTrans.make_gram_FSSet(feateq_defaults)

        LexTrans.make_lextrans_states(fst, entry_pairs, gram_feats)

        print(fst)

        return fst
