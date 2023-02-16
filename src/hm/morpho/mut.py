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

    PARSER = FSSet.parse

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
        print("** mutations for {}: {}".format(weight.__repr__(), patterns))
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
    def make_root_states(fst, cons, feats, rules, char_maps, cascade):
        def mrs(fst, charsets, weight, states, iterative=False, aisa=False, main_charsets=None):
#            print("**** mrs {} weight {} states {} iterative {}".format(charsets, weight.__repr__(), states, iterative))
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
                elif aisa:
                    dest = dest + 'a'
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
        charsets, strong = Roots.make_charsets(cons, cls, rules.get(cls), char_maps)
        # Based on rules, assign ±strong to the root
        weight = weight.set_all('strong', strong)
        mrs(fst, charsets, weight, states, iterative=False, aisa=False)
        if (cls_it_rules := rules.get(cls + 'i')):
#            print("*** there are iterative rules: {}".format(cls_it_rules))
            it_charsets, strongi = Roots.make_charsets(cons, cls + 'i', cls_it_rules, char_maps)
#            print("*** charsets {}, it_charsets {}".format(charsets, it_charsets))
            mrs(fst, it_charsets, weight, states, iterative=True, aisa=False, main_charsets=charsets)
        if (cls_a_rules := rules.get(cls + 'a')):
#            print("*** there are _a_ rules: {}".format(cls_a_rules))
            a_charsets, strongi = Roots.make_charsets(cons, cls + 'a', cls_a_rules, char_maps)
            mrs(fst, a_charsets, weight, states, iterative=False, aisa=True, main_charsets=charsets)

    @staticmethod
    def get_rule(consonants, cls, rules):
        cls_rules = rules.get(cls)
        if not cls_rules:
            print("Warning: no rules for class {}!".format(cls))
            return

    @staticmethod
    def make_charsets(consonants, cls, rules, char_maps):
        '''
        Given the root consonants and a set of rules for the class,
        return a dict of list of Geez characters for each position
        and whether the root is strong.
        '''
#        print("**** Making character sets for {}, {}, {}, {}".format(consonants, cls, rules, char_maps))
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
        # Keep track of positions where vowels are changed based on weak subclass rules, so
        # earlier rules have priority (otherwise <' w q> is treated as a 2=ው root)
        positions_reset = []
        for index in range(len(defaults)):
            cons = consonants[index]
            # assume that root classes have romanized keys
            if is_geez(cons):
                cons = romanize(cons, 'ees')
            position = index + 1
            if position in positions_reset:
                continue
            posrules = rules.get(position)
#            print("*** making charset for elem {}, cons {}, posrules {}".format(index, cons, posrules))
            if posrules and cons in posrules:
                # Give priority to weak classes found earlier, e.g., 1=' over 2=w
#                print("*** weak root {} for position {}".format(consonants, position))
                strong = False
                posrules = posrules[cons]
#                print("*** {} -- found weak rules for {}:{} : {}".format(consonants, position, cons, posrules))
                for pos, vowels in posrules.items():
                    charsets[pos] = vowels
                    positions_reset.append(pos)
        for cons, (position, chars) in zip(consonants, charsets.items()):
            if isinstance(chars, tuple):
                # iterative position: make two charsets
                charsets[position] = tuple([Roots.make_charset(cons, position, v) for v in chars])
            else:
                charsets[position] = Roots.make_charset(cons, position, chars, char_maps=char_maps)
        return charsets, strong
        
    @staticmethod
    def make_charset(cons, position, vowels, default='eI', char_maps=None):
#        print("*** Making charset for {} in {} with {}".format(cons, position, vowels))
        result = []
        for vowel in vowels:
            if (vmap := char_maps.get(vowel)) and (vchar := vmap.get(cons)):
                result.append(vchar)
            else:
                result.append(geezify_CV(cons, vowel))
        return result
#        return [geezify_CV(cons, vowel) for vowel in vowels]

    @staticmethod
    def make_irr_root(fst, cons, feats, patterns):
#        print("** Making irr root {}, {}, {}".format(cons, feats, patterns))
        cons = cons.split()
        state_name = ''.join(cons)
        states = []
        for index, cs in enumerate(cons):
            i = index+1
#            state_name0 = "{}{}".format(state_name, i)
            char = geezify_CV(cs, 'I')
            feats = "{},{}={}".format(feats, i, char)
#            states.append(state_name0)
        feats = '[' + feats + ']'
        weight = UNIFICATION_SR.parse_weight(feats)
        cls = weight.get('c')
#        weight = FSSet.update(weight, IRR_FS)
#        print("*** cons {}, weight {}".format(cons, weight.__repr__()))
        for pindex, (pattern, pfeatures) in enumerate(patterns):
            pposition = pindex + 1
            pfeatures = UNIFICATION_SR.parse_weight(pfeatures)
            pfeatures = FSSet.update(pfeatures, weight)
#            print("**** Creating states for root {} and pattern {} and features {}".format(cons, pattern, pfeatures.__repr__()))
            source = 'start'
            for cindex, char in enumerate(pattern[:-1]):
                cposition = cindex + 1
                dest = "{}_{}_{}".format(state_name, pposition, cposition)
                if not fst.has_state(dest):
                    fst.add_state(dest)
#                print(" **** Adding arc {}->{}: {}".format(source, dest, char))
                fst.add_arc(source, dest, char, char, weight=pfeatures if cindex==0 else None)
                source = dest
            final_char = pattern[-1]
#            print(" **** Adding arc {}->end: {}".format(source, final_char))
            fst.add_arc(source, 'end', final_char, final_char)

    @staticmethod
    def parse(label, s, cascade=None, fst=None, gen=False, 
              directory='', seg_units=[], abbrevs=None,
              weight_constraint=None, verbose=False):
        """
        Parse an FST from a string consisting of multiple lines from a file.
        Create a new FST if fst is None.
        """
#        print("** Parsing mutation file {}, fst {}".format(s, fst))

#        weighting = fst.weighting()

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
                print("*** rule {}".format(rule))
                if rule[0] == '[':
                    unmutated_weight = rule
                else:
                    rules.append(rule)
                continue

            m = Mutation.FEATURES_RE.match(line)
            if m:
                current_feats = m.groups()[0]
                mutations[current_feats] = []
                print("*** features {}".format(current_feats))
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
