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
Creating an FST from a set of roots.
2023.01.05

"""

import re, os
from .utils import segment
from .semiring import FSSet, UNIFICATION_SR, TOPFSS
from .fs import FeatStructParser
from .geez import *

# Default name for final state
DFLT_FINAL = 'fin'
# Signifies no input or output characters associated with an FSS
NO_INPUT = '--'

LINE_RE = re.compile(r'\s*<(.+?)>\s+(\S+?)$')
RULE_RE = re.compile(r'\s*%(.+)$')

def geezify_CV(c, v):
    if v in '0-_' or not v:
        return ''
    return geezify(c+v, 'ees')

class Roots:

    PARSER = FSSet.parse

#    def __init__(self, fst, directory=''):
#        self.fst = fst
#        self.cascade = fst.cascade
#        self.seg_units = self.cascade.seg_units
#        self.directory = directory
#        self.weighting = UNIFICATION_SR
#        self.states = []

#    def __repr__(self):
#        return "Roots {}".format(self.fst.label)

    @staticmethod
    def make_root_states(fst, cons, feats, rules, cascade):
        cons = cons.split()
#        c = [c.replace('*', '') for c in cons]
        state_name = ''.join(cons)
#        print("*** Make root states for {}, {}".format(cons, state_name))
        states = []
        for index, cs in enumerate(cons):
            i = index+1
            state_name0 = "{}{}".format(state_name, i)
#            weak = False
#            if cs[0] == '*':
#                weak = True
#                cs = cs[1:]
#            weight[i] = cs
            char = geezify_CV(cs, 'I')
            feats = "{},{}={}".format(feats, i, char)
#            stringset = cascade.stringset(cs)
#            print("**** State {}, feats {}, stringset {}".format(state_name0, feats, stringset))
            states.append(state_name0)
        feats = '[' + feats + ']'
        weight = UNIFICATION_SR.parse_weight(feats)
        cls = weight.get('c')
#        print("*** states {}, weight {}".format(states, weight.__repr__()))
        charsets = Roots.make_charsets(cons, cls, rules)
#        print("*** charsets {}".format(charsets))
        source = 'start'
        for index, dest in enumerate(states[:-1]):
            position = index + 1
            chars = charsets.get(position)
#            print("*** {} -> {} -> {}".format(source, chars, dest))
            if not fst.has_state(dest):
                fst.add_state(dest)
            for char in chars:
                fst.add_arc(source, dest, char, char, weight=weight if index==0 else None)
            source = dest
        state = states[-1]
        chars = charsets[len(charsets)]
#        print("*** {} -> {} -> end".format(source, chars))
        for char in chars:
            fst.add_arc(source, 'end', char, char)

    @staticmethod
    def get_rule(consonants, cls, rules):
        cls_rules = rules.get(cls)
        if not cls_rules:
            print("Warning: no rules for class {}!".format(cls))
            return

    @staticmethod
    def make_charsets(consonants, cls, rules):
        rules = rules.get(cls)
        if not rules:
            print("Warning: no rules for class {}".format(cls))
            return
        charsets = {}
        defaults = rules.get('')
        if not defaults:
            print("Warning: no default rules class {}".format(cls))
            return
        for position, vowels in defaults.items():
            charsets[position] = vowels
        for index in range(len(defaults)):
            cons = consonants[index]
            position = index + 1
            posrules = rules.get(position)
            if posrules and cons in posrules:
                posrules = posrules[cons]
                for pos, vowels in posrules.items():
                    charsets[pos] = vowels
        for cons, (position, chars) in zip(consonants, charsets.items()):
            charsets[position] = Roots.make_charset(cons, position, chars)
        return charsets
        
    @staticmethod
    def make_charset(cons, position, vowels, default='eI'):
        return [geezify_CV(cons, vowel) for vowel in vowels]

    @staticmethod
    def parse(label, s, cascade=None, fst=None, gen=False, 
              directory='', seg_units=[], abbrevs=None,
              weight_constraint=None, verbose=False):
        """
        Parse an FST from a string consisting of multiple lines from a file.
        Create a new FST if fst is None.
        """
#        print("** Parsing roots file {}, fst {}".format(s, fst))

#        weighting = fst.weighting()

        rules = {}
        roots = []

        # Create start and end states
        if not fst.has_state(label): fst.add_state('start')
        fst._set_initial_state('start')
        if not fst.has_state('end'): fst.add_state('end')
        fst.set_final('end')

        lines = s.split('\n')[::-1]

        while lines:
            line = lines.pop().split('#')[0].strip() # strip comments

            if not line: continue

            m = RULE_RE.match(line)
            if m:
                rule = m.groups()[0]
#                print("*** rule {}".format(rule))
                cat, specs = rule.split('::')
                cat = cat.strip().split(',')
                position = 0
                if len(cat) == 1:
                    subcat = ''
                else:
                    subcat = cat[-1]
                    char, position = tuple(subcat)
                    position = int(position)
                maincat = cat[0].strip()
                specs = eval(specs)
#                specs = [s.strip().split(':') for s in specs]
#                print("maincat {}, subcat {}, specs {}".format(maincat, subcat, specs))
                if maincat in rules:
                    r = rules[maincat]
                    if position:
                        if position in r:
                            r[position][char] = specs
                        else:
                            r[position] = {char: specs}
                    else:
                        r[''] = specs
                else:
                    rules[maincat] = {}
                    if position:
                        rules[maincat][position] = {char: specs}
                    else:
                        rules[maincat][''] = specs
                continue

            m = LINE_RE.match(line)
            if m:
                cons, feats = m.groups()
#                print("*** cons {}, feats {}".format(cons, feats))
                roots.append((cons, feats))
                continue

            print("*** Something wrong with {}".format(line))

        for cons, feats in roots:
            Roots.make_root_states(fst, cons, feats, rules, cascade)

#        print("** rules: {}".format(rules))

#        print(fst)

        return fst



