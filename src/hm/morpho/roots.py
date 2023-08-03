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
from .utils import segment, pad2eqlen
from .semiring import FSSet # , UNIFICATION_SR
from .fs import FeatStruct, simple_unify
from .geez import *
from .ees import EES

make_weight = EES.make_weight

def geezify_CV(c, v):
    '''
    Convert roman cons and vowel to a Geez character.
    v may be '0' in which case the vowelless (ሳድስ) character is returned.
    v may be '0x', where x is a Geez character. In this case this character
    is returned, and c is ignored.
    '''
#    print("** geezifying {} + {}".format(c, v))
    if v in '0-_' or not v:
        return ''
    elif len(v) > 1 and v[0] == '0':
        return v[1]
    elif is_geez(c):
        c = romanize(c, 'ees')
#        print(" ** romanized {}".format(c))
    if len(c) > 1:
        if c[-1] == 'u':
            c = c[0] + 'W'
#        print("** Geezifying {} + {}".format(c, v))
    g = geezify(c+v, 'ees')
#    if len(c) > 1:
#        print("** Geezified: {}".format(g))
    if not is_geez(Roots.remove_gem(g)):
#            g.replace(EES.pre_gem_char, '')):
        return ''
#    print("** geezified {}".format(g))
    return g

class Roots:

#    PARSER = FSSet.parse

    # Signifies no input or output characters associated with an FSS
    NO_INPUT = '--'

    CHAR_MAP_RE = re.compile(r'\s*\$\s*(.+?)\s*(\[.+\])?(\s+.+)?$')
    CHAR_SET_RE = re.compile(r'\s*\$\$\s*(.+?)\s+(.+?)$')
    ROOT_RE =     re.compile(r'\s*<(.+?)>\s+(\S+?)$')
    IRR_ROOT_RE = re.compile(r'\s*\*<(.+?)>\s+(\S+?)$')
    RULE_RE = re.compile(r'\s*%(.+)$')
    PATTERN_RE = re.compile(r'\s*(.+)$')
    FEATURES_RE = re.compile(r'\s*(\[.+\])$')
    CHAR_FEAT_RE = re.compile(r"(.+?)(\[.+\])")
    CHAR_MAP_LABEL_RE = re.compile(r'([^(^)]+)(?:\((.+)\))?')

    # Root in particular combination of v and a
    SUBROOT_RE = re.compile(r'\s+(\S+?)$')

    # Abbreviation (lemma) for root type
    ROOT_TYPE_RE = re.compile(r'\s*\{(.+?)\}\s*:\s*(.+?)$')

    # File with specific roots and their constraints
    ROOT_FILE_RE = re.compile(r'\s*\+(.+)\+$')

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
    def remove_gem(char):
        return char.replace(EES.pre_gem_char, '').replace(':', '')

    @staticmethod
    def make_root_states(fst, cons, feats, subroots, rules, duprules, char_maps, charmap_weights, cascade, posmorph, labbrev,
                         gen=False, seglevel=2, gemination=True):
#        print("*** Creating root states for {}, seglevel={}, feats={}, gemination={}".format(cons, seglevel, feats.__repr__(), gemination))

        def dup_weight(drules, weight):
            if drules:
                for (pos1, pos2), vowels in drules:
                    feat = "dup{}{}".format(pos1, pos2)
                    if cons[pos1-1] == cons[pos2-1]:
#                        print("   *** {} matched drule".format(cons))
                        return weight.set_all(feat, True)
                    return weight.set_all(feat, False)
            return weight

        def gem_char_arc(source, dest, inchar, outchar, weight, gem_weight, verbosity=0):
#            print("** gem_char_arc {}->{}".format(inchar, outchar))
            outchar = outchar if (gen or seglevel==0) else inchar
            gem = EES.pre_gem_char
            dest_gem = dest + '_gem'
            if not fst.has_state(dest_gem):
                fst.add_state(dest_gem)
                outgem = gem if gemination and seglevel else ''
                if verbosity:
                    print("  ** outchar {}, inchar {}, {}, {}".format(outgem, '/', source, dest_gem))
                charfeat_arc(gem, outgem, gem_weight, source, dest_gem, fst)
            if verbosity:
                print("  ** outchar {}, inchar {}, {}, {}".format(outchar, inchar, dest_gem, dest))
            charfeat_arc(inchar, outchar, weight, dest_gem, dest, fst)

        def charfeat_arc(inchar, outchar, wt, source, dest, fst, verbosity=0):
            # Create the arc from source dest
            # char is either a character or a (character, weight) tuple
            if verbosity:
                print("  ** out {} in {} src {} dest {}".format(outchar, inchar, source, dest))
            if isinstance(inchar, tuple):
                # this char depends on a weight
                inchar, charfeats = inchar
                # happens for seg but not gen
                if not gen and seglevel:
                    outchar = inchar
                if wt:
                    wt0 = wt.unify(charfeats)
                else:
                    wt0 = charfeats
                fst.add_arc(source, dest, inchar, outchar, weight=wt0)
            else:
                fst.add_arc(source, dest, inchar, outchar, weight=wt)
                
        def mrs(fst, charsets, weight, states, root_chars, manner=False, iterative=False, aisa=False, main_charsets=None):
#            if not iterative and not aisa:
#            print("  *** Making root states for {} with weight {}".format(root_chars, weight.__repr__()))
            source = 'start'
            for index, (rchar, dest) in enumerate(zip(root_chars[:-1], states[:-1])):
                position = index + 1
                chars = charsets.get(position)
#                if root_chars == ['ብ', 'ር', 'ር']:
#                    print("** Root state {} rchar {} chars {}".format(position, rchar, chars))
                wt = weight if index == 0 else None
                iter_chars = isinstance(chars, tuple)
                if (iterative or manner) and not iter_chars:
                    # Check to see whether states and arcs already exist for these chars
                    if fst.has_state(source) and fst.has_state(dest):
                        found = True
                        for char in chars:
                            if not fst.state_has_inout(source, dest, char, char):
                                found = False
                                break
                        if found:
#                            print("   ** Already a state for {}".format(char))
                            source = dest
                            continue
                if iterative:
                    dest = dest + 'i'
                elif aisa:
                    dest = dest + 'a'
                elif manner:
                    dest = dest + 'm'
                if iter_chars:
                    # iterated position, create two states
                    dest0 = dest + '_a'
                    dest = dest + '_b'
                    if not fst.has_state(dest0):
                        fst.add_state(dest0)
                    for char in chars[0]:
                        outchar = rchar if (gen or seglevel==0) else char
#                        print("** Creating iter state 1, source {} dest {} char {} outchar {} {}".format(source, dest0, char, outchar, wt))
                        charfeat_arc(char, outchar, wt, source, dest0, fst)
                    if not fst.has_state(dest):
                        fst.add_state(dest)
                    for char in chars[1]:
                        if len(char) == 2:
                            # second character is geminated
                            inchar = Roots.remove_gem(char)
                            gem_char_arc(dest0, dest, inchar, '', wt, wt)
                        else:
                            outchar = '' if (gen or seglevel==0) else char
#                            print("** Creating iter state 2, source {} dest {} char {} outchar {} {}".format(dest0, dest, char, outchar, wt))
                            charfeat_arc(char, outchar, wt, dest0, dest, fst)
                else:
                    if not fst.has_state(dest):
                        fst.add_state(dest)
                    for char in chars:
                        if len(char) == 2:
                            inchar = Roots.remove_gem(char)
                            gem_char_arc(source, dest, inchar, rchar, wt, wt, verbosity=0) #root_chars == ['ብ', 'ር', 'ር'])
                        else:
                            outchar = rchar if (gen or seglevel==0) else char
#                            print("** Creating regular states source {} dest {} char {} outchar {} {}".format(source, dest, char, outchar, wt))
                            charfeat_arc(char, outchar, wt, source, dest, fst, verbosity=0) # root_chars == ['ብ', 'ር', 'ር'])
                source = dest
            state = states[-1]
            # chars for last position
            chars = charsets[len(charsets)]
            rchar = root_chars[-1]
            for char in chars:
                if len(char) == 2:
                    inchar = Roots.remove_gem(char)
                    gem_char_arc(source, 'end', inchar, rchar, wt, wt, verbosity=0)
                else:
                    outchar = rchar if (gen or seglevel==0) else char
                    inchar = char
#                    print("** Creating final state source {} end char {} outchar {} wt None".format(source, inchar, outchar))
                    charfeat_arc(inchar, outchar, None, source, 'end', fst, verbosity=0) #root_chars == ['ብ', 'ር', 'ር'])

        # one of cons could be a char, feature tuple
        cons_chars = [(c[0] if isinstance(c, tuple) else c) for c in cons]
        state_name = ''.join(cons_chars)
        states = []
        # Add this root to the POSMorphology instance's rootfeats dict
        if posmorph:
            if state_name in posmorph.rootfeats:
                posmorph.rootfeats[state_name].append(feats)
            else:
                posmorph.rootfeats[state_name] = [feats]
        for index, cs in enumerate(cons):
            i = index+1
            if isinstance(cs, tuple):
                # cs may have a feature constraint
                cs = cs[0]
            state_name0 = "{}{}".format(state_name, i)
            char = geezify_CV(cs, 'I')
            sourceroot = 't' if gen else ''
            feats = "{},{}{}={}".format(feats, sourceroot, i, char)
            states.append(state_name0)
        # Add source and target language features for generation and 0 seglevel.
        if gen:
            feats = "{},tl={}".format(feats, labbrev)
        elif seglevel == 0:
            # Add source language feature
            feats = "{},sl={}".format(feats, labbrev)

        # Add root feature to feats
        feats = "root={},{}".format(''.join(cons_chars), feats)

        if subroots:
            # Make an FSSet from feats and subroots
            expanded_feats = []
            for subroot in subroots:
                expanded_feats.append("{},{}".format(feats, subroot))
            feats = ';'.join(['[' + x + ']' for x in expanded_feats])
#            print("** expanded feats {}".format(feats))
        else:
            feats = '[' + feats + ']'
        weight = make_weight(feats, target=gen)
        cls = weight.get('tc') if gen else weight.get('c')

        # Root may be explicitly 'strong', in which case weak rules are ignored (this prevents ጸለየ (ጽልይ) from being treated like ለየ (ልይይ).
        expl_strength = weight.get('strong', False)

        # make the simplex states and arcs
        drules = duprules.get(cls)
        charsets, strong = Roots.make_charsets(cons, cls, rules.get(cls), drules, char_maps, charmap_weights, expl_strength=expl_strength)
        # Based on rules, assign ±strong to the root
        strength_feat = 'tstrong' if gen else 'strong'
        weight = weight.set_all(strength_feat, strong)
        weight1 = dup_weight(drules, weight)
        mrs(fst, charsets, weight1, states, cons_chars, iterative=False, aisa=False)
        if (cls_it_rules := rules.get(cls + 'i')):
            drules = duprules.get(cls + 'i')
            it_charsets, strongi = Roots.make_charsets(cons, cls + 'i', cls_it_rules, drules, char_maps, charmap_weights, expl_strength=expl_strength)
            # Add a=i if it's compatible with other features
            weighti = weight.set_all('a', 'i', force=False)
            if weighti:
                weighti = dup_weight(drules, weighti)
                mrs(fst, it_charsets, weighti, states, cons_chars, iterative=True, aisa=False, main_charsets=charsets)
        if (cls_m_rules := rules.get(cls + 'm')):
            drules = duprules.get(cls + 'm')
            m_charsets, strongi = Roots.make_charsets(cons, cls + 'm', cls_m_rules, drules, char_maps, charmap_weights, expl_strength=expl_strength)
            # Add a=i if it's compatible with other features
            weightm = weight.set_all('d', 'm', force=False)
            if weightm:
                weightm = dup_weight(drules, weightm)
                mrs(fst, m_charsets, weightm, states, cons_chars, manner=True, iterative=False, aisa=False, main_charsets=charsets)
        if (cls_a_rules := rules.get(cls + 'a')):
            drules = duprules.get(cls + 'a')
            a_charsets, strongi = Roots.make_charsets(cons, cls + 'a', cls_a_rules, drules,  char_maps, charmap_weights, expl_strength=expl_strength)
            # Add a=a if it's compatible with other features
            weighta = weight.set_all('a', 'a', force=False)
            if weighta:
                weighta = dup_weight(drules, weighta)
                mrs(fst, a_charsets, weighta, states, cons_chars, iterative=False, aisa=True, main_charsets=charsets)

    @staticmethod
    def get_rule(consonants, cls, rules):
#        print("*** Getting rules for {}, {}".format(consonants, cls))
        cls_rules = rules.get(cls)
        if not cls_rules:
            print("Warning: no rules for consonants {} in class {}!".format(consonants, cls))
            return

    @staticmethod
    def make_charsets(consonants, cls, rules, duprules, char_maps, charmap_weights, expl_strength=False):
        '''
        Given the root consonants and a set of rules for the class,
        return a dict of list of Geez characters for each position
        and whether the root is strong.
        '''
#        print("  **** Making character sets for {}, {}; {}".format(consonants, cls, expl_strength))
        if not rules:
            print("Warning: no rules for consonants {} in class {}".format(consonants, cls))
            return
        charsets = {}
        defaults = rules.get('')
        strong = True
        if not defaults:
            print("Warning: no default rules class {}".format(cls))
            return
        for position, vowels in defaults.items():
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
            # Skip the weak rules for this position if one has already been found
            # or if the root is expicitly strong
            if position in positions_reset or expl_strength:
                continue
            posrules = rules.get(position)
            if posrules and cons in posrules:
                # Give priority to weak classes found earlier, e.g., 1=' over 2=w
                strong = False
                posrules = posrules[cons]
                for pos, vowels in posrules.items():
                    charsets[pos] = vowels
                    positions_reset.append(pos)
        if duprules:
            for duprule in duprules:
                positions, cvs = duprule
                c1, c2 = consonants[positions[0]-1], consonants[positions[1]-1]
                if c1 == c2:
                    for position, vowels in cvs.items():
                        charsets[position] = vowels
        for cons, (position, chars) in zip(consonants, charsets.items()):
            cons_feat = None
            if isinstance(cons, tuple):
                # cons has an associated feature constraint
                cons, cons_feat = cons
            if isinstance(chars, tuple):
                # iterative position: make two charsets
                charsets[position] = \
                  tuple([Roots.make_charset(cons, position, v, char_maps=char_maps, charmap_weights=charmap_weights, cons_feat=cons_feat) for v in chars])
            else:
                charsets[position] = Roots.make_charset(cons, position, chars, char_maps=char_maps, charmap_weights=charmap_weights, cons_feat=cons_feat)
#        print(" *** charsets {}".format(charsets))
        return charsets, strong
        
    @staticmethod
    def make_charset(cons, position, vowels, default='eI', char_maps=None, charmap_weights=None, cons_feat=None):
#        print(" *** Making charset for {} in {} with {}, cons feat {}".format(cons, position, vowels, cons_feat.__repr__()))
        result = []
        for vowel_spec in vowels:
            geminated = False
            vowel_feat = None
            if isinstance(vowel_spec, tuple):
                # This character or character map has an associated feature
                v, vowel_feat = vowel_spec
            else:
                v = vowel_spec
            if EES.pre_gem_char in v:
                geminated = True
                v = Roots.remove_gem(v)
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
                if not cv and cv != '':
                    continue
                if geminated:
                    cv = '/' + cv
                if vowel_feat:
                    if (cv, vowel_feat) not in result:
                        result.append((cv, vowel_feat))
                else:
                    if cv not in result:
                        result.append(cv)
#        print("*** result {}".format(result))
        return result

    @staticmethod
    def make_irr_root(fst, cons, feats, patterns, posmorph, labbrev, gen=False, seglevel=2, gemination=True):
        cons = cons.split()
        state_name = ''.join(cons)
        # Add this root to the POSMorphology instance's rootfeats dict
        if posmorph:
            if state_name in posmorph.rootfeats:
                posmorph.rootfeats[state_name].append(feats)
            else:
                posmorph.rootfeats[state_name] = [feats]
        states = []
        for index, cs in enumerate(cons):
            i = index+1
            char = geezify_CV(cs, 'I')
            sourceroot = 't' if gen else ''
            feats = "{},{}{}={}".format(feats, sourceroot, i, char)
        if seglevel == 0:
            # Add source language feature
            feats = "{},sl={}".format(feats, labbrev)
        elif gen:
            feats = "{},tl={}".format(feats, labbrev)
        # Add root feature to feats
        feats = "root={},{}".format(''.join(cons), feats)
        feats = '[' + feats + ']'
        weight = make_weight(feats, target=gen)
        cls_feat = 'tc' if gen else 'c'
        cls = weight.get(cls_feat)
        tmp_length = len(cons)
        # Position of possibly geminated consonant (all EES!)
        gem_pos = {tmp_length - 1}

        for pindex, (pattern, pfeatures) in enumerate(patterns):
#            print("** Making irr root {}, {}, {}, {}".format(cons, feats, pattern, pfeatures.__repr__()))
            pposition = pindex + 1
            pfeatures = make_weight(pfeatures, target=gen)
            pfeatures = FSSet.update(pfeatures, weight)
            source = 'start'
            if gen or seglevel == 0:
                pad2eqlen(cons, pattern)
            gem_feat = None
            for cindex, (char, c) in enumerate(zip(pattern[:-1], cons[:-1])):
                gem = False
                cposition = cindex + 1
                if cposition in gem_pos:
                    gem_feat = "gem{}".format(cposition)
                    gem = ":" in char or EES.pre_gem_char in char
                    if gem:
                        gem_feat = make_weight("[+{}]".format(gem_feat), target=gen)
                        char = Roots.remove_gem(char)
                    else:
                        gem_feat = make_weight("[-{}]".format(gem_feat), target=gen)
                dest = "{}_{}_{}".format(state_name, pposition, cposition)
                if not fst.has_state(dest):
                    fst.add_state(dest)
                if gem:
                    # Make a separate arc for the pre-gem character
                    dest_gem = source + '_gem'
                    if not fst.has_state(dest_gem):
                        fst.add_state(dest_gem)
                    gemc = EES.pre_gem_char
                    fst.add_arc(source, dest_gem, gemc, gemc, weight=gem_feat)
                    inchar = char
                    if gen or seglevel == 0:
                        outchar = c
                    else:
                        outchar = char
                    fst.add_arc(dest_gem, dest, inchar, outchar, weight=pfeatures)
#                    print(" ** adding gem arc {}->{}".format(inchar, outchar))
                else:
                    inchar = char
                    if gen or seglevel == 0:
                        outchar = c
                    else:
                        outchar = char
                    fst.add_arc(source, dest, inchar, outchar, weight=pfeatures if cindex==0 else gem_feat)
#                    print(" ** adding arc {}->{}".format(inchar, outchar))
                source = dest
            dest = 'end'
            rchar = cons[-1]
            pchar = pattern[-1]
            final_in = pchar
            if gen or seglevel == 0:
                final_out = rchar
            else:
                final_out = pchar
#            if len(pattern) == 1:
#                print("** only one stem cons {}, using weight {}".format(final_in, pfeatures.__repr__()))
            fst.add_arc(source, dest, final_in, final_out, weight=pfeatures if len(pattern) == 1 else None)
#            print(" ** adding final arc {}->{}".format(final_in, final_out))

    @staticmethod
    def parse_root_file(filename, lexdir, roots, root_types):
        file = os.path.join(lexdir, filename + ".lex")
        s = open(file, encoding='utf8').read()
#        print("** Opening root file {}".format(file))

        lines = s.split('\n')[::-1]

        while lines:
            line = lines.pop().split('#')[0].rstrip() # strip comments

            if not line.lstrip(): continue

#            print("*** line: {}".format(line))

            m = Roots.ROOT_RE.match(line)
            if m:
                cons, feats = m.groups()
                cons = cons.split()
                # A consonant may have an associated feature constraint
                current_root = cons
                for cindex, c in enumerate(cons):
                    if (match := Roots.CHAR_FEAT_RE.match(c)):
                        c, feature = match.groups()
                        feature = FeatStruct(feature)
                        cons[cindex] = (c, feature)

                roots.append([cons, feats, []])
                continue

            m = Roots.SUBROOT_RE.match(line)
            if m:
                subrootfeats = m.groups()[0]
                # Add subrootfeatures to most recent root
                roots[-1][2].append(subrootfeats)
                continue

            m = Roots.ROOT_TYPE_RE.match(line)
            if m:
                rtype, rtypefeats = m.groups()
                root_types.append((rtype, rtypefeats))
                continue

            print("*** Something wrong with {}".format(line))

    @staticmethod
    def parse(label, s, cascade=None, fst=None, gen=False, posmorph=None,
              directory='', seg_units=[], abbrevs=None, seglevel=2,
              lexdir='', gemination=True, weight_constraint=None, verbose=False):
        """
        Parse an FST from a string consisting of multiple lines from a file.
        Create a new FST if fst is None.
        """
#        print("** Parsing roots file, fst {}, posmorph {}, gen {}, seglevel {}, gemination {}".format(fst, posmorph, gen, seglevel, gemination))

#        weighting = fst.weighting()

        language = cascade.language

        labbrev = language.abbrev

        stringsets = language.stringsets or cascade._stringsets


        rules = {}

        duprules = {}

        roots = []

        irr_roots = {}

        root_types = []

        char_maps = {}

        char_sets = {}

        charmap_weights = {}

        current_root = ''
        current_irr_root = ''
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
                    feature = make_weight(feature, target=gen)
                    vspec[vindex] = (vs, feature)
            return vspec

        while lines:
            line = lines.pop().split('#')[0].rstrip() # strip comments

            if not line.lstrip(): continue

#            print("*** line: {}".format(line))

            m = Roots.RULE_RE.match(line)
            if m:
                rule = m.groups()[0]

                cat, specs = rule.strip().split('::')
                cat = cat.strip().split(',')
                position = 0
                chars = ''
                char = ''
                dup_positions = ''
                if len(cat) == 1:
                    subcat = ''
                else:
                    subcat = cat[-1]
                    if '==' in subcat:
                        # subcat is like 2==3; duplicate root consonants
                        dup_positions = [int(p) for p in subcat.split('==')]
                    elif '=' in subcat:
                        # subcat is like 2=ው
                        position, char = subcat.split('=')
                        if char in char_sets:
                            chars = char_sets[char]
                        position = int(position)
                    elif len(subcat) > 1:
                        char, position = tuple(subcat)
                        position = int(position)
                maincat = cat[0].strip()
                if specs.strip() == '!':
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
                chars = chars or [char]
                if dup_positions:
                    if maincat not in duprules:
                        duprules[maincat] = []
                    r = duprules[maincat]
                    r.append((dup_positions, specs))
                else:
                    if maincat not in rules:
                        rules[maincat] = {}
                    r = rules[maincat]
                    if position:
                        for c in chars:
                            if position in r:
                                r[position][c] = specs
                            else:
                                r[position] = {c: specs}
                    else:
                        r[''] = specs
                continue

            m = Roots.CHAR_SET_RE.match(line)
            if m:
                charset, chars = m.groups()
                char_sets[charset] = chars
                continue

            m = Roots.CHAR_MAP_RE.match(line)
            if m:
                maplabel, feature, chars = m.groups()
                if feature:
                    feature = make_weight(feature, target=gen)
                if chars:
                    chars = chars.strip()
                if not chars:
                    mm = Roots.CHAR_MAP_LABEL_RE.match(maplabel)
                    spec = None
                    if mm:
                        maplabel, spec = mm.groups()
                    charmap = Roots.make_charmap(maplabel, stringsets, spec=spec)
                    char_maps[maplabel] = charmap
                    if feature:
                        charmap_weights[maplabel] = feature
                    continue
                chars = [c.strip() for c in chars.split(Roots.charmapsep)]
                chars = [[c[0], list(c[1:])] for c in chars]
                chars = dict(chars)
                char_maps[maplabel] = chars
                if feature:
                    charmap_weights[maplabel] = feature
                continue

            m = Roots.ROOT_FILE_RE.match(line)
            if m:
                filename = m.groups()[0]
                Roots.parse_root_file(filename, lexdir, roots, root_types)
                continue

            m = Roots.ROOT_RE.match(line)
            if m:
                cons, feats = m.groups()
                cons = cons.split()
                # A consonant may have an associated feature constraint
                current_root = cons
                for cindex, c in enumerate(cons):
                    if (match := Roots.CHAR_FEAT_RE.match(c)):
                        c, feature = match.groups()
                        feature = FeatStruct(feature)
                        cons[cindex] = (c, feature)

                roots.append([cons, feats, []])
                continue

            m = Roots.SUBROOT_RE.match(line)
            if m:
                subrootfeats = m.groups()[0]
                # Add subrootfeatures to most recent root
                roots[-1][2].append(subrootfeats)
                continue

            m = Roots.IRR_ROOT_RE.match(line)
            if m:
                current_irr_root = m.groups()
                irr_roots[current_irr_root] = []
                continue

            m = Roots.ROOT_TYPE_RE.match(line)
            if m:
                rtype, rtypefeats = m.groups()
                root_types.append((rtype, rtypefeats))
                continue

            m = Roots.FEATURES_RE.match(line)
            if m:
                features = m.groups()[0]
                current_feats = features
                continue

            m = Roots.PATTERN_RE.match(line)
            if m:
                pattern = m.groups()[0].split()
                irr_roots[current_irr_root].append((pattern, current_feats))
                continue

            print("*** Something wrong with {}".format(line))

#        print("** rules: {}".format(rules))

        for cons, feats, subroots in roots:
            Roots.make_root_states(fst, cons, feats, subroots, rules, duprules, char_maps, charmap_weights, cascade, posmorph,
                                   labbrev, gen=gen, seglevel=seglevel, gemination=gemination)

        if irr_roots:
            for (cons, feats), patterns in irr_roots.items():
                Roots.make_irr_root(fst, cons, feats, patterns, posmorph, labbrev, gen=gen, seglevel=seglevel, gemination=gemination)

#        print("** char maps {}".format(char_maps))
#        print("** char maps weights {}".format(charmap_weights))

#        print("** irr roots: {}".format(irr_roots))

        return fst

