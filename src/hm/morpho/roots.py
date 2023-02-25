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
from .fs import FeatStruct, simple_unify
#from .fs import FeatStructParser
from .geez import *

#IRR_FS = FSSet("[-reg]")

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

class Roots:

    PARSER = FSSet.parse

    # Signifies no input or output characters associated with an FSS
    NO_INPUT = '--'

    CHAR_MAP_RE = re.compile(r'\s*\$\s*(.+?)\s*(\[.+\])?(\s+.+)?$')
    ROOT_RE = re.compile(r'\s*<(.+?)>\s+(\S+?)$')
    IRR_ROOT_RE = re.compile(r'\s*\*<(.+?)>\s+(\S+?)$')
    RULE_RE = re.compile(r'\s*%(.+)$')
    PATTERN_RE = re.compile(r'\s*(.+)$')
    FEATURES_RE = re.compile(r'\s*(\[.+\])$')
    CHAR_FEAT_RE = re.compile(r"(.+?)(\[.+\])")
    CHAR_MAP_LABEL_RE = re.compile(r'([^(^)]+)(?:\((.+)\))?')

    possep = ';'
    charmapsep = ';'
    vspecsep = ','

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
    def make_charmap(name, charsets, spec=None):
        '''
        Make a character map from charsets, possibly with a
        specification, including palatalize, depalatalize, voice, devoice.
        '''
#        print("** Making charmap for {}".format(name))
        map = {}
        charset = charsets.get(name)
        if not charset:
            print("NO charset called {}!".format(name))
            return
        for char in charset:
            char6 = to_sads(char, spec=spec)
            if char6 not in map:
                map[char6] = [char]
            else:
                map[char6].append(char)
        return map

    @staticmethod
    def make_root_states(fst, cons, feats, rules, char_maps, charmap_weights, cascade):

        def charfeat_arc(char, wt, source, dest, fst):
            # Create the arc from source dest
            # char is either a character or a (character, weight) tuple
#            print(" *** charfeat_arc {}, {}, {}, {}".format(char, wt.__repr__(), source, dest))
            if isinstance(char, tuple):
                # this char depends on a weight
                char, charfeats = char
#                print("  **** char {}, charfeats {}".format(char, charfeats.__repr__()))
                if wt:
                    wt0 = wt.unify(charfeats)
                else:
                    wt0 = charfeats
                fst.add_arc(source, dest, char, char, weight=wt0)
            else:
                fst.add_arc(source, dest, char, char, weight=wt)
                
        def mrs(fst, charsets, weight, states, iterative=False, aisa=False, main_charsets=None):
#            if iterative:
#                print("**** mrs {} weight {} states {}".format(charsets, weight.__repr__(), states))
            source = 'start'
            for index, dest in enumerate(states[:-1]):
                position = index + 1
                chars = charsets.get(position)
                wt = weight if index == 0 else None
#                if iterative:
#                    print("  **** position {}, chars {}, weight {}".format(position, chars, wt.__repr__()))
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
                        charfeat_arc(char, wt, source, dest0, fst)
                    if not fst.has_state(dest):
                        fst.add_state(dest)
                    for char in chars[1]:
                        charfeat_arc(char, wt, dest0, dest, fst)
                else:
                    if not fst.has_state(dest):
                        fst.add_state(dest)
                    for char in chars:
                        charfeat_arc(char, wt, source, dest, fst)
                source = dest
            state = states[-1]
            chars = charsets[len(charsets)]
            for char in chars:
                fst.add_arc(source, 'end', char, char)
#        cons = cons.split()

        # one of cons could be a char, feature tuple
        cons_chars = [(c[0] if isinstance(c, tuple) else c) for c in cons]
        state_name = ''.join(cons_chars)
#        print("*** Make root states for {}, {}".format(cons, state_name))
        states = []
        for index, cs in enumerate(cons):
            i = index+1
            if isinstance(cs, tuple):
                # cs may have a feature constraint
                cs = cs[0]
            state_name0 = "{}{}".format(state_name, i)
            char = geezify_CV(cs, 'I')
            feats = "{},{}={}".format(feats, i, char)
            states.append(state_name0)
        feats = '[' + feats + ']'
        weight = UNIFICATION_SR.parse_weight(feats)
        cls = weight.get('c')
#        print("*** states {}, weight {}".format(states, weight.__repr__()))
        # make the simplex states and arcs
        charsets, strong = Roots.make_charsets(cons, cls, rules.get(cls), char_maps, charmap_weights)
        # Based on rules, assign ±strong to the root
        weight = weight.set_all('strong', strong)
        mrs(fst, charsets, weight, states, iterative=False, aisa=False)
        if (cls_it_rules := rules.get(cls + 'i')):
#            print("*** there are iterative rules: {}".format(cls_it_rules))
            it_charsets, strongi = Roots.make_charsets(cons, cls + 'i', cls_it_rules, char_maps, charmap_weights)
#            print("*** charsets {}, it_charsets {}".format(charsets, it_charsets))
            mrs(fst, it_charsets, weight, states, iterative=True, aisa=False, main_charsets=charsets)
        if (cls_a_rules := rules.get(cls + 'a')):
#            print("*** there are _a_ rules: {}".format(cls_a_rules))
            a_charsets, strongi = Roots.make_charsets(cons, cls + 'a', cls_a_rules, char_maps, charmap_weights)
            mrs(fst, a_charsets, weight, states, iterative=False, aisa=True, main_charsets=charsets)

    @staticmethod
    def get_rule(consonants, cls, rules):
        cls_rules = rules.get(cls)
        if not cls_rules:
            print("Warning: no rules for class {}!".format(cls))
            return

    @staticmethod
    def make_charsets(consonants, cls, rules, char_maps, charmap_weights):
        '''
        Given the root consonants and a set of rules for the class,
        return a dict of list of Geez characters for each position
        and whether the root is strong.
        '''
#        print("**** Making character sets for {}, {}".format(consonants, cls))
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
            if isinstance(cons, tuple):
                # cons has an associated feature
                cons, cons_feat = cons
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
            cons_feat = None
            if isinstance(cons, tuple):
                # cons has an associated feature constraint
                cons, cons_feat = cons
#            print("  **** cons {} chars {}".format(cons, chars))
            if isinstance(chars, tuple):
                # iterative position: make two charsets
                charsets[position] = \
                  tuple([Roots.make_charset(cons, position, v, char_maps=char_maps, charmap_weights=charmap_weights, cons_feat=cons_feat) for v in chars])
            else:
                charsets[position] = Roots.make_charset(cons, position, chars, char_maps=char_maps, charmap_weights=charmap_weights, cons_feat=cons_feat)
#        print("  *** charsets {}".format(charsets))
        return charsets, strong
        
    @staticmethod
    def make_charset(cons, position, vowels, default='eI', char_maps=None, charmap_weights=None, cons_feat=None):
#        print(" *** Making charset for {} in {} with {}, cons feat {}".format(cons, position, vowels, cons_feat.__repr__()))
        result = []
        for vowel_spec in vowels:
            vowel_feat = None
            if isinstance(vowel_spec, tuple):
                # This character or character map has an associated feature
                v, vowel_feat = vowel_spec
            else:
                v = vowel_spec
#            print("  *** vowel {}, vowel_feat {}, cm_weight {}".format(v, vowel_feat.__repr__(), charmap_weights.get(v).__repr__()))
            # If there's a cons feat and a vowel feature, check to see whether they agree
            if cons_feat and vowel_feat:
                if vowel_feat.unify_FS(cons_feat) == 'fail':
#                    print("** cons {} with feat {} fails to match vowel {} with feat {}".format(cons, cons_feat, v, vowel_feat))
                    continue
            if char_maps and (vmap := char_maps.get(v)):
                if (cm_weight := charmap_weights.get(v)):
                    if cons_feat and cm_weight.unify_FS(cons_feat) == 'fail':
#                        print("  ** cons {} with feat {} fails to match charmap {} with feat {}".format(cons, cons_feat.__repr__(), v, cm_weight.__repr__()))
                        continue
                if (vchar := vmap.get(cons)):
                    # if the consonant is not in the map, ignore it
                    if cm_weight:
                        vchar = [(char, cm_weight) for char in vchar]
#                    if vowel_feat:
#                        vchar = [(char, vowel_feat) for char in vchar]
                    for vc in vchar:
                        if vc not in result:
                            result.append(vc)
#                    result.extend(vchar)
            else:
                cv = geezify_CV(cons, v)
                if vowel_feat:
                    if (cv, vowel_feat) not in result:
                        result.append((cv, vowel_feat))
                else:
                    if cv not in result:
                        result.append(cv)
#        print("  *** result {}".format(result))
        return result

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
#        print("** Parsing roots file {}, fst {}".format(s, fst))

#        weighting = fst.weighting()

        language = cascade.language

        stringsets = language.stringsets or cascade._stringsets

#        print("*** stringset ~ye {}".format(stringsets.get('~ye')))

        rules = {}

        roots = []

        irr_roots = {}

        char_maps = {}

        charmap_weights = {}

        current_root = ''
        current_feats = ''

        # Create start and end states
        if not fst.has_state(label): fst.add_state('start')
        fst._set_initial_state('start')
        if not fst.has_state('end'): fst.add_state('end')
        fst.set_final('end')

        lines = s.split('\n')[::-1]

        def proc_vspec(vspec):
            # vspec is something like a,_a[+mut]
            # if there is a feature for an item, convert the char and feature to a tuple
            vspec = vspec.split(Roots.vspecsep)
            for vindex, v in enumerate(vspec):
                v = v.strip()
                if (match := Roots.CHAR_FEAT_RE.match(v)):
                    vs, feature = match.groups()
                    # Create an FSS for this vowel spec
                    feature = UNIFICATION_SR.parse_weight(feature)
                    vspec[vindex] = (vs, feature)
#                    print("   **** vs {} feature {}".format(vs, feature.__repr__()))
            return vspec

        while lines:
            line = lines.pop().split('#')[0].strip() # strip comments

            if not line: continue

            m = Roots.RULE_RE.match(line)
            if m:
                rule = m.groups()[0]
#                print("*** rule {}".format(rule))

                cat, specs = rule.strip().split('::')
                cat = cat.strip().split(',')
                position = 0
                if len(cat) == 1:
                    subcat = ''
                else:
                    subcat = cat[-1]
                    if '=' in subcat:
                        # subcat is like 2=ው
                        position, char = subcat.split('=')
                        position = int(position)
                    elif len(subcat) > 1:
                        char, position = tuple(subcat)
                        position = int(position)
                maincat = cat[0].strip()
                if specs.strip() == '!':
                    print("*** Constraint on maincat {}, subcat {}".format(maincat, subcat))
                    continue
                elif '{' in specs:
                    specs = eval(specs)
                else:
                    specs = specs.split(Roots.possep)
                    specs = [s.strip().split(':') for s in specs]
                    proc_specs = []
                    for sindex, (p, spec) in enumerate(specs):
                        p = int(p)
                        if '|' in spec:
                            spec1, spec2 = spec.split('|')
                            spec1 = proc_vspec(spec1)
                            spec2 = proc_vspec(spec2)
                            proc_specs.append([p, (spec1, spec2)])
                        else:
                            proc_specs.append([p, proc_vspec(spec)])
                    specs = dict(proc_specs)
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

            m = Roots.CHAR_MAP_RE.match(line)
            if m:
                maplabel, feature, chars = m.groups()
                if feature:
                    feature = UNIFICATION_SR.parse_weight(feature)
                if chars:
                    chars = chars.strip()
#                print("*** char map {}: {}, {}".format(maplabel, chars, feature.__repr__()))
                if not chars:
#                    print("** Creating char map for {}".format(maplabel))
                    mm = Roots.CHAR_MAP_LABEL_RE.match(maplabel)
                    spec = None
                    if mm:
                        maplabel, spec = mm.groups()
#                        print("** maplabel: {} -- {}".format(maplabel, spec))
                    charmap = Roots.make_charmap(maplabel, stringsets, spec=spec)
#                    print("** charmap {}".format(charmap))
                    char_maps[maplabel] = charmap
                    if feature:
                        charmap_weights[maplabel] = feature
                    continue
                chars = [c.strip() for c in chars.split(Roots.charmapsep)]
                chars = [[c[0], list(c[1:])] for c in chars]
#                print("** -> ", chars)
                chars = dict(chars)
#                print("** -> ", chars)
                char_maps[maplabel] = chars
                if feature:
                    charmap_weights[maplabel] = feature
                continue

            m = Roots.ROOT_RE.match(line)
            if m:
                cons, feats = m.groups()
                cons = cons.split()
                # A consonant may have an associated feature constraint
                for cindex, c in enumerate(cons):
#                    print("*** {} {}".format(cindex, c))
                    if (match := Roots.CHAR_FEAT_RE.match(c)):
                        c, feature = match.groups()
                        feature = FeatStruct(feature)
                        cons[cindex] = (c, feature)
#                print("*** cons {}, feats {}".format(cons, feats))

                roots.append((cons, feats))
                continue

            m = Roots.IRR_ROOT_RE.match(line)
            if m:
                current_root = m.groups()
                irr_roots[current_root] = []
                continue

            m = Roots.FEATURES_RE.match(line)
            if m:
                features = m.groups()[0]
                current_feats = features
#                print("*** features {}".format(features))
#                irr_roots[current_root].append(features)
                continue

            m = Roots.PATTERN_RE.match(line)
            if m:
                pattern = m.groups()[0].split()
#                print("*** pattern {}".format(pattern))
                irr_roots[current_root].append((pattern, current_feats))
#                print("*** irr_roots {}".format(irr_roots))
                continue

            print("*** Something wrong with {}".format(line))

#        print("** rules: {}".format(rules))

        for cons, feats in roots:
            Roots.make_root_states(fst, cons, feats, rules, char_maps, charmap_weights, cascade)

        if irr_roots:
            for (cons, feats), patterns in irr_roots.items():
                Roots.make_irr_root(fst, cons, feats, patterns)

#        print("** char maps {}".format(char_maps))
#        print("** char maps weights {}".format(charmap_weights))

#        print("** irr roots: {}".format(irr_roots))

#        if irr_roots:
#                print(fst)

        return fst

