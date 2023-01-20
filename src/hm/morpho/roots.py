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
    return geezify(c+v, 'ees')

class Roots:

    PARSER = FSSet.parse

    # Signifies no input or output characters associated with an FSS
    NO_INPUT = '--'

    LINE_RE = re.compile(r'\s*<(.+?)>\s+(\S+?)$')
    RULE_RE = re.compile(r'\s*%(.+)$')

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
        def mrs(fst, charsets, weight, states, iterative=False, main_charsets=None):
#            if iterative:
#                print("*** charsets {}, main csets {}".format(charsets, main_charsets))
            source = 'start'
            for index, dest in enumerate(states[:-1]):
                position = index + 1
                chars = charsets.get(position)
                iter_chars = isinstance(chars, tuple)
                if iterative and not iter_chars:
                    # Check to see whether states and arcs already exist for these chars
                    if fst.has_state(source) and fst.has_state(dest):
                        found = True
                        for char in chars:
                            if not fst.state_has_inout(source, dest, char, char):
                                found = False
                                break
                        if found:
#                            print(" ** Already a state for {}".format(char))
                            source = dest
                            continue
                if iterative:
                    dest = dest + 'i'
                if iter_chars:
                    # iterated position, create two states
                    dest0 = dest + '_a'
                    dest = dest + '_b'
                    if not fst.has_state(dest0):
                        fst.add_state(dest0)
                    for char in chars[0]:
                        fst.add_arc(source, dest0, char, char, weight=weight if index==0 else None)
                    if not fst.has_state(dest):
                        fst.add_state(dest)
                    for char in chars[1]:
                        fst.add_arc(dest0, dest, char, char, weight=None)
                else:
                    if not fst.has_state(dest):
                        fst.add_state(dest)
                    for char in chars:
                        fst.add_arc(source, dest, char, char, weight=weight if index==0 else None)
                source = dest
            state = states[-1]
            chars = charsets[len(charsets)]
            for char in chars:
                fst.add_arc(source, 'end', char, char)
        cons = cons.split()
        state_name = ''.join(cons)
#        print("*** Make root states for {}, {}".format(cons, state_name))
        states = []
        for index, cs in enumerate(cons):
            i = index+1
            state_name0 = "{}{}".format(state_name, i)
            char = geezify_CV(cs, 'I')
            feats = "{},{}={}".format(feats, i, char)
            states.append(state_name0)
        feats = '[' + feats + ']'
        weight = UNIFICATION_SR.parse_weight(feats)
        cls = weight.get('c')
#        print("*** states {}, weight {}".format(states, weight.__repr__()))
        # make the simplex states and arcs
        charsets, strong = Roots.make_charsets(cons, cls, rules.get(cls))
        # Based on rules, assign ±strong to the root
        weight = weight.set_all('strong', strong)
        mrs(fst, charsets, weight, states, iterative=False)
        if (cls_it_rules := rules.get(cls + 'i')):
#            print("*** there are iterative rules: {}".format(cls_it_rules))
            it_charsets, strongi = Roots.make_charsets(cons, cls + 'i', cls_it_rules)
#            print("*** charsets {}, it_charsets {}".format(charsets, it_charsets))
            mrs(fst, it_charsets, weight, states, iterative=True, main_charsets=charsets)

    @staticmethod
    def get_rule(consonants, cls, rules):
        cls_rules = rules.get(cls)
        if not cls_rules:
            print("Warning: no rules for class {}!".format(cls))
            return

    @staticmethod
    def make_charsets(consonants, cls, rules):
        '''
        Given the root consonants and a set of rules for the class,
        return a dict of list of Geez characters for each position
        and whether the root is strong.
        '''
#        print("*** Rules: {}".format(rules))
        if not rules:
            print("Warning: no rules for class {}".format(cls))
            return
        charsets = {}
        defaults = rules.get('')
        strong = True
        if not defaults:
            print("Warning: no default rules class {}".format(cls))
            return
        for position, vowels in defaults.items():
#            print("** position {}, vowels {}".format(position, vowels))
#            if isinstance(vowels, tuple):
            charsets[position] = vowels
        for index in range(len(defaults)):
            cons = consonants[index]
            position = index + 1
            posrules = rules.get(position)
            if posrules and cons in posrules:
#                print("*** weak root: {}".format(consonants))
                strong = False
                posrules = posrules[cons]
                for pos, vowels in posrules.items():
#                    print("** pos {}, vowels {}".format(pos, vowels))
                    charsets[pos] = vowels
        for cons, (position, chars) in zip(consonants, charsets.items()):
            if isinstance(chars, tuple):
                # iterative position: make two charsets
                charsets[position] = tuple([Roots.make_charset(cons, position, v) for v in chars])
            else:
                charsets[position] = Roots.make_charset(cons, position, chars)
        return charsets, strong
        
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

            m = Roots.RULE_RE.match(line)
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
                    if len(subcat) > 1:
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
#                    elif subcat:
#                        r[subcat] = specs
                    else:
                        r[''] = specs
                else:
                    rules[maincat] = {}
                    if position:
                        rules[maincat][position] = {char: specs}
#                    elif subcat:
#                        rules[maincat][subcat] = specs
                    else:
                        rules[maincat][''] = specs
                continue

            m = Roots.LINE_RE.match(line)
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



