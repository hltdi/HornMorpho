"""
This file is part of the HornMorpho package.

    HornMorpho is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    HornMorpho is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with L3Morpho.  If not, see <http://www.gnu.org/licenses/>.

Author: Michael Gasser <gasser@indiana.edu>
-------------------------------------------------------

ALTERNATION RULES

 A change rule contains
 - a left context
 - a right context
 - a change
 A filter rule contains a single context.

 Each segment consists of a sequence of
 - charstrings, representing characters or character classes
   or sequences thereof
   .  .*   .-x*  .-@X*  .-x,y  x  @X  x,y  @X-x,y  0
   (the . can be dropped from all but the first)

-- 2011-07-08
   Some fixes in Context.make_rules(), applicable especially to
   rules with no right context
-- 2011-07...
   Various other fixes in Context.make_rules(), Change.make_rules(),
   Change.make_fail_states()
-- 2012-08-01
   Added change fail state to rules with right contexts but no change
   character, that is, rules that delete in analysis, insert in
   generation.
-- 2012-08-02
   Fixed make_fail_states so that the final successful fail state
   has a .:. loop.
-- 2012-08-04
   More fixes to make_fail_states:
   Initial fail_state is not automatically final.
   Additional state is created for the case.
      | * X *
-- 2012-08-05
   More fixes to make_fail_states:
   Loop in final successful fail state (see 2012-08-02)
   should not be .:. but instead exclude the initial change characters;
   there is an arc for the change characters back to the change fail
   state.
   Initial fail state *is* final (see 2012-08-02).
"""

import re, copy
from .utils import segment

CHANGE_RE = re.compile(r'\s*(\S+)\s*(->|<-|<->)\s*(\S*)')
# character class
SS_RE = re.compile(r'(\S+)\s*=\s*\{(.*)\}')
# left and right contexts; both can be empty
CONTEXT_RE = re.compile(r'(.*)\|(.*)')
# single filter context
FILTER_RE = re.compile(r'!!\s+(.+)')
# keywords: mult, comment, etc.
KEYWORD_RE = re.compile(r'%(\S+)\s*(.+)')
# comment: %% short form for comments
COMMENT_RE = re.compile(r'%%\s*(.+)')

CHARSTRING_MODS = '*+?)'

class AltRule:

    def __init__(self, fst, seg_units, verbose=False):
        self.verbose = verbose
        self.fst = fst
        self.cascade = fst.cascade
        self.seg_units = seg_units
        # contexts
        self.lc = None
        self.rc = None
        self.change = None
        self.keywords = {}
        self.mult = None
        self.multRC = None
        self.multLC = None
        self.filter = None
#        print('Created', self)

    def __repr__(self):
        return '<AltRule {}>'.format(self.fst.label)

    def make_state(self, index, infix, final=False):
        if index >= 0:
            index_string = str(index)
        else:
            index_string = ''
        label = self.fst.label + infix + index_string
        self.fst.add_state(label)
        if final:
            self.fst.set_final(label)
#        print('Making state', label)
        if index >= 0:
            index = index + 1
        return label, index

    def set_properties(self):
        # Multiple changes?
        # possibilities
        # - multiple repetitions of the change between the LC and RC
        #   requires a separate start and end state for the change
        #   'multC'
        # - multiple repetitions of the LC and change, within a single RC
        #   requires a separate end state for the change (or start state for RC)
        #   LC cannot be left-bounded
        #   Gn prenasal->nasal rule
        #   'multLC+C'
        # - multiple repetitions of the change and RC, within a single LC
        #   requires a separate start state for the change (or end state for the LC)
        #   RC cannot be right-bounded
        #   'multC+RC'
        # - multiple repetitions of LC-change-RC
        #   LC cannot be left-bounded; RC cannot be right-bounded
        #   'mult'
        multprops = self.keywords.get('mult')
        if multprops:
            self.mult = True
            multprops = multprops.split()
            if 'RC' in multprops:
                self.multRC = True
            if 'LC' in multprops:
                self.multLC = True
        if 'comment' in self.keywords:
            self.fst._comment = self.keywords['comment']
        if self.change:
            self.fst._change_list = self.change.change_list
            if self.lc:
                self.fst.lc_strings = self.lc.strings
            if self.rc:
                self.fst.rc_strings = self.rc.strings
        elif self.filter:
            self.fst.filter_strings = self.filter.strings

    def compile(self):
        init_state, index = self.make_state(-1, '_i', final=not self.lc or not self.lc.left_bounded)
        self.fst._set_initial_state(init_state)
        current = init_state

        if self.filter:
#            print('COMPILING filter rule', self)

#            print('Making states')
            current, index = self.filter.make_fail_states(current, init_state, [])

            self.fst.set_final(current)

        else:
#            print('COMPILING change rule', self)

#            print('LC: left bounded {}, right bounded {}, empty {}'.format(self.lc.left_bounded,
#                                                                           self.lc.right_bounded,
#                                                                           self.lc.empty))
#            print('RC: left bounded {}, right bounded {}, empty {}'.format(self.rc.left_bounded,
#                                                                           self.rc.right_bounded,
#                                                                           self.rc.empty))

            lc_copy, init_copy, lc_copy_end = None, None, None

            nochange = self.change.get_nochange(0)
            ## Do the left context
            if self.lc:
                current, index = self.lc.make_states(current, nochange=nochange)

            pre_change = current
            
            change_mult = 0
            if self.mult:
                if self.multLC:
                    if self.multRC:
                        change_mult = 3
                    else:
                        change_mult = 2
                else:
                    change_mult = 1

            if change_mult == 2:
#                print('Multiple LC and C possible, so make a copy of the LC without final states')
                lc_copy = self.lc.make_copy()
                # State to start of lc_copy in place of init_state
                init_copy, ic_index = self.make_state(-1, '_i+')
#                print('Making states for context copy', lc_copy, 'starting at', init_copy)
                lc_copy_end, lc_copy_index = lc_copy.make_states(init_copy, nochange=nochange)
                
            ## Do the change
            current, change_fail, change_chars, index = self.change.make_states(pre_change, not self.rc.empty,
                                                                                mult=change_mult,
                                                                                lc_right_bounded=self.lc.right_bounded,
                                                                                lc_copy_init=init_copy)
            
            # if change_mult == 2, make a copy of the change
            if change_mult == 2:
#                print('Making copy of change state')
                change_copy = self.change.make_copy()
                # Join change_copy to lc_copy
                change_copy_end, ignore, change_chars, change_copy_index = change_copy.make_states(lc_copy_end, not self.rc.empty,
                                                                                                   mult=change_mult,
                                                                                                   lc_copy_init=init_copy)
            
#            print('Processing right context', self.rc)

            ## Do the right context
            if self.rc:
                if init_copy:
                    # If it's mult LC + C, start the right context from the initial state of the LC copy
                    current = init_copy
                current, index = self.rc.make_states(current, change_fail,
                                                     change_chars=change_chars,
                                                     sep_start=self.mult and not self.multRC,
                                                     last_change=self.change[-1],
                                                     init_state=init_state)

            self.fst.set_final(current)
            if change_mult == 3:
                # Multiple LC -- RC changes; make an arc back to the beginning
                self.fst.add_arc(current, init_state, '', '')

    @staticmethod
    def make_char_comp(c1, c2):
        if '-' in c2:
            if '-' in c1:
                print("No way yet to combine subtraction with subtraction")
            else:
                c2a, c2b = c2.split('-')
                if c1 == c2a:
                    return c2b
                else:
                    return c2b + ',' + c1 + '-' + c2a
        elif c1 == c2:
            return ''
        else:
            return c1 + '-' + c2

    @staticmethod
    def charclass_excl(charclass):
        if '-' in charclass:
            return charclass.split('-')[-1]
        return ''

    def parse(self, s):
        """
        Parse an alternation rule FST from a string consisting of multiple lines from a file.
        """

        # Character classes
        charclasses = []

        # Join lines ending in '\'
        pending_line = ''
        # Current indentation
        current_indent = 0

        change_dir = ''

        contexts = []

        changes = []

        filter_context = None

        lines = s.split('\n')[::-1]
        while lines:
            line = lines.pop().split('#')[0].rstrip() # strip comments

            # Ignore blank lines
            if not line: continue

            if line[-1] == '\\':
                # Continue on to next line
                pending_line += line[:-1]
                continue

            if pending_line:
                # Add this line onto pending line before parsing
                line = pending_line + line
                pending_line = ''

            # Comment: %%
            m = COMMENT_RE.match(line)
            if m:
                comment = m.group(1)
                if comment:
                    self.fst._comment = comment
                continue

            # Keyword: % keyword body
            m = KEYWORD_RE.match(line)
            if m:
                keyword, value = m.groups()
                if not value:
                    value = True
#                print('Found keyword', keyword, value)
                self.keywords[keyword] = value
                continue

            # Change
            m = CHANGE_RE.match(line)
            if m:
                lex, direction, surf = m.groups()
                # lexical to surface is the default
                lex = segment(lex, self.seg_units, correct=False)
                surf = segment(surf, self.seg_units, correct=False)
#                print('Found change {} {} {}'.format(surf, lex, direction))
                changes.append((surf, lex))
                continue

            # Character class
            m = SS_RE.match(line)
            if m:
                label, chars = m.groups()
                chars = [c.strip() for c in chars.split(',')]
#                print('Found class {} = {}'.format(label, chars))
                charclasses.append((label, chars))
                continue

            # Filter context
            m = FILTER_RE.match(line)
            if m:
                filter_context = m.group(1)
                filter_context = filter_context.strip().split(' ')                
#                print('Found filter context {}'.format(filter_context))
                continue

            # Left and right contexts
            m = CONTEXT_RE.match(line)
            if m:
                left, right = m.groups()
                left, right = left.strip(), right.strip()
                if left: left = left.split(' ')
                if right: right = right.split(' ')
#                print('Found contexts {} | {}'.format(left, right))
                contexts = [left, right]
                continue

        self.set_properties()

        classes = self.cascade._stringsets

        if filter_context:                
#            print('Filter rule')
            self.filter = Context(filter_context, None, True, fst=self.fst, classes=classes)
        else:
#            print('Change rule')
            self.change = Change(changes, change_dir, fst=self.fst)
            self.lc = Context(contexts[0], self.change, True, fst=self.fst, classes=classes)
            self.rc = Context(contexts[1], self.change, False, fst=self.fst, classes=classes)
            self.lc.exclude_change_chars(self.change)

        self.compile()

class Change(list):

    def __init__(self, change_list, dir_arrow, fst=None):
        self.fst = fst
        self.change_list = change_list
        # Assume direction is the same for all changes
        self.dir = 'l2s'
        self.copy = False
        if '<' in dir_arrow:
            if '>' in dir_arrow:
                self.dir = 'bidir'
            else:
                self.dir = 's2l'
        # Make a list of sets of
        # input (surface) char, output (lexical) char, change char, no change string
        surf_lex = [list(zip(s, l)) for s, l in change_list]
        for position in range(len(surf_lex[0])):
            sl = [self.proc_chars(sl_pairs[position]) for sl_pairs in surf_lex]
            for index, (s, l) in enumerate(sl):
                change_char = self.get_dir_string(s, l)
#                no_change_string = AltRule.make_char_comp('.', change_char)
                sl[index] = s, l, change_char #, no_change_string
            self.append(set(sl))

    def __repr__(self):
        return '<Change{} {}>'.format('+' if self.copy else '',
                                      ' '.join([';'.join([y[0] + ':' + y[1] for y in x]) for x in self]))

    def make_copy(self):
        change_copy = copy.copy(self)
        change_copy.copy = True
        return change_copy

    def get_change(self, position):
        charset = self[position]
        return [c[2] for c in charset]
#        return ','.join(change_chars)

    def get_nochange(self, position):
        charset = self[position]
        change_chars = [c[2] for c in charset]
        change_chars = ','.join(change_chars)
        if change_chars:
            return AltRule.make_char_comp('.', change_chars)
        else:
            return '.'

    def proc_chars(self, charpair):
        if charpair[0] == '0':
            return '', charpair[1]
        if charpair[1] == '0':
            return charpair[0], ''
        return charpair

    def get_dir_string(self, inchar, outchar):
        if self.dir == 'l2s':
            return outchar
        elif self.dir == 's2l':
            return inchar
        else:
            return inchar + ',' + outchar

    def make_arc_string(self, position):
        charset = self[position]
        return [(x[0], x[1]) for x in charset]

    def make_states(self, pre_change, any_rc, mult=0, lc_copy_init=None,
                    lc_right_bounded=False):
        # Left context copy init state is needed if multiple LC+C is happening
        index = 0
        no_change_state = None
        current = pre_change
        change_fail = None
        new_change_fail = None
        init_state = pre_change
        change_chars = []
#        if any_rc:
#            print('{} MAKING CHANGE states{}, starting from {}'.format(self,
#                                                                       ' (copy)' if self.copy else '',
#                                                                       pre_change))
        for change_index, io_set in enumerate(self):
#            print('  Charstrings', io_set)

            if any_rc and not self.copy and any([x[2] for x in io_set]):
                # Make a state for the case where the change fails if the change_char is not empty
                # and there is some right context
                new_change_fail, index = self.make_state(index, 'f', final=True)
#                print(self, 'making change fail state', new_change_fail)

            # if this is the last change and there is no right context, don't make a new state
            if change_index < len(self) - 1 or any_rc:
                change_state, index = self.make_state(index, '')
            else:
                change_state = current
            for (inchar, outchar, change_char) in io_set:
                # Connect the last change state to the current one with strings representing the change
                self.fst.add_arc(current, change_state, inchar, outchar)
                # Connect the last change fail state to the current one with strings representing no change
                if new_change_fail and change_char:
                    # Don't do this if the change char is 0 (that is, if something is being inserted (deleted)).
                    last_state = change_fail or current
                    self.fst.add_arc(last_state, new_change_fail, change_char, change_char)
#                    print('  Joining', last_state, 'to new change fail state', new_change_fail, 'with', change_char)
                    if change_index == 0:
#                        print('Making loop on change fail state', new_change_fail, 'with', change_char)
                        self.fst.add_arc(new_change_fail, new_change_fail, change_char, change_char)
#                        print('And making arc to change state', change_state, 'with', inchar, outchar)
                        self.fst.add_arc(new_change_fail, change_state, inchar, outchar)
                        change_chars.append(change_char)
#            if new_change_fail and change_index == 0 and not lc_right_bounded:
#                # This is the first change fail state so make a return arc from it to the last state
#                # if the left context is not right-bounded
#                print(' Making return arc from', new_change_fail, 'to', last_state)
#                self.fst.add_arc(new_change_fail, last_state, '', '')
            # Update the change fail state
            if new_change_fail:
                change_fail = new_change_fail
            if no_change_state:
                no_change_string = '.'
                excl_chars = ','.join(s[2] for s in io_set)
                if excl_chars:
                    no_change_string += '-' + excl_chars
#                print('Creating an arc from', no_change_state, 'to', pre_change, 'with chars', no_change_string)
                # Add an arc from the no-change state to pre-change that excludes the changed char
                self.fst.add_arc(no_change_state, pre_change, no_change_string, no_change_string)
            # If this are any more changes, make a state for the case where the change does not happen (successfully)
            if change_index < len(self) - 1 and not self.copy:
                no_change_state = None
                if inchar != outchar and change_char:
                    # If there are any more changes, make a state for the case where the
                    # change does not happen (successfully): the output or input character
                    # remains the same
                    # This state is identical to the change fail state, except that its input
                    # arc comes from the current *change state* rather than the current
                    # *change fail* state
                    no_change_state, index = self.make_state(index, 'e', final=True)
                    self.fst.add_arc(current, no_change_state, change_char, change_char)
#                    print(self, 'making escape state', no_change_state, 'with change char', change_char)
                
            # Continue from the change state
            current = change_state
        
        if mult == 1:
#            print('Do change multiple times, loop back from', current, 'to', init_state)
            self.fst.add_arc(current, init_state, '', '')
        elif mult == 2:
#            print('Do change multiple times, including LC; loop from', current, 'to', lc_copy_init)
            self.fst.add_arc(current, lc_copy_init, '', '')

        if any_rc and not self.copy and not change_fail:
            # For the case where the change is only analysis deletions / generation insertions,
            # make a change_fail state with no change
            change_fail, index = self.make_state(index, 'f', final=True)
            self.fst.add_arc(pre_change, change_fail, '', '')
#            print('Making change fail state', change_fail, 'with no changes')
#        if change_fail:
#            print('  Change chars for change fail {}'.format(change_chars))

        return current, change_fail, change_chars, index

    def make_state(self, index, infix, final=False):
        if self.copy:
            infix = '_+c' + infix
        else:
            infix = '_c' + infix
        label = self.fst.label + infix + str(index)
        self.fst.add_state(label)
        if final:
            self.fst.set_final(label)
#        print('Making state', label)
        return label, index + 1

class Context(list):

    def __init__(self, strings=[], change=[], left=True, fst=None,
                 classes=None):
        self.strings = strings
        self.left = left
        self.change = change
        self.classes = classes
        self.fst = fst
        self.copy = False
        self.decode(strings)
#        if self.empty:
#            print('{} is empty'.format(self))

    def __repr__(self):
        return '<Context {}>'.format('left' if self.left else 'right')

    def make_copy(self):
        context_copy = copy.copy(self)
        context_copy.copy = True
#        context_copy.fst = self.fst
        return context_copy

    def make_excl_loop(self, state, exclchars):
        '''Make a looping arc to state excluding chars in exclchars, modifying
        an existing arc if there is already one excluding other chars.'''
        for arc in self.fst.outgoing(state):
            if self.fst.dst(arc) == state:
                # arc is a loop
                ins = self.fst.in_string(arc)
                outs = self.fst.out_string(arc)
                if ins == outs:
                    incl, excl = ins.split('-')
                    if incl == '.':
                        if not exclchars:
                            # Don't add any new arc
                            return
                        if excl:
#                            print('Adding', exclchars, 'to existing arc', arc, 'with excl', excl)
                            string = '.-' + excl + ',' + exclchars
                            self.fst._in_string[arc] = string
                            self.fst._out_string[arc] = string
                        else:
#                            print('Excluding', exclchars, 'from existing . arc', arc)
                            string = '.-' + exclchars
                            self.fst._in_string[arc] = string
                            self.fst._out_string[arc] = string
                        return
        string = '.'
        if exclchars:
            string += '-' + exclchars
#        string = '.-' + exclchars
        self.fst.add_arc(state, state, string, string)

    def combine_arc(self, src, dst, charstring):
        """If there is already an arc from src to dst that can be combined with charstring,
        combine them; otherwise create a new arc."""
        if '-' in charstring:
            cs_incl, cs_excl = charstring.split('-')
            cs_excl_chars = set()
            if ',' not in cs_excl:
                cs_excl_class = self.expand_charclass(cs_excl)
                if cs_excl_class:
                    cs_excl_chars = cs_excl_class
                else:
                    cs_excl_chars = set(cs_excl)
            else:
                cs_excl_chars = set(cs_excl.split(','))
            for arc in self.fst.state_arcs(src, dst):
                ins = self.fst.in_string(arc)
                outs = self.fst.out_string(arc)
                if ins == outs:
                    incl, excl = ins.split('-')
                    if cs_incl == incl:
                        if cs_excl == excl:
                            # No need to make the arc; it's already covered
                            return
                        excl_chars = set()
                        if ',' not in excl:
                            excl_class = self.expand_charclass(excl)
                            if excl_class:
                                excl_chars = excl_class
                            else:
                                excl_chars = set(excl)
                        else:
                            excl_chars = set(excl.split(','))
                        if cs_excl_chars == excl_chars:
                            # No need to make the arc here either; it's already covered
                            return
                        # Change the existing arc
                        string = incl + '-' + ','.join(cs_excl_chars) + ',' + ','.join(excl_chars)
#                        print(' Changing existing arc from', ins, 'to', string)
                        self.fst._in_string[arc] = string
                        self.fst._out_string[arc] = string
                        return
        self.fst.add_arc(src, dst, charstring, charstring)

    def make_arc_string(self, element):
        string = element['charclass']
        if element['excl']:
            string += '-' + element['excl']
        return string

    def decode1(self, charstring, index):
        '''Decode context charstring and add it to the context.'''
        elemdict = {}
        lastchar = charstring[-1]
        # Look for a modifier symbol at the end
        if lastchar in CHARSTRING_MODS:
            charstring = charstring[:-1]
            if lastchar in '*?)':
                elemdict['min'] = 0
            else:
                elemdict['min'] = 1
            if lastchar in '?)':
                elemdict['max'] = 1
            else:
                elemdict['max'] = 100
        else:
            elemdict['min'] = 1
            elemdict['max'] = 1
        if charstring and charstring[0] == '(':
            charstring = charstring[1:]
        charclass_excluded = charstring.split('-')
        if len(charclass_excluded) == 2:
            charclass, excluded = charclass_excluded
        else:
            charclass = charstring
            excluded = ''
        if not charclass:
            # . may be omitted when there are other characters
            # in the charstring
            elemdict['charclass'] = '.'
        else:
            elemdict['charclass'] = charclass
        elemdict['excl'] = excluded
        elemdict['index'] = index
        self.append(elemdict)

    def decode(self, charstrings):
        for index, charstring in enumerate(charstrings):
            self.decode1(charstring, index)
        # Go through the elements again, excluding following single element
        # from unlimited charset
        for index, element in enumerate(self):
            if index < len(self) - 1 and element['min'] == 0 and element['max'] > 5 and not element['excl']:
                next_element = self[index+1]
                if next_element['min'] == 1 and next_element['max'] == 1:
                    element['excl'] = next_element['charclass']
                    
        if len(self) == 0 or self[0]['min'] > 0:
            self.left_bounded = True
        else:
            self.left_bounded = False
        if len(self) == 0 or self[-1]['min'] > 0:
            self.right_bounded = True
        else:
            self.right_bounded = False
        self.empty = True
        for element in self:
            if not self.elem_unconstrained(element):
                self.empty = False
                break

    def exclude_change_chars(self, change):
        '''If the last element is unlimited, exclude from it the first set of change chars.'''
        last_element = self[-1]
        if last_element['min'] == 0 and last_element['max'] > 5 and not last_element['excl']:
            change_chars = change.get_change(0)
            if all(change_chars):
                change_chars = ','.join(change_chars)
#                print('Excluding', change_chars, 'from', self)
                last_element['excl'] = change_chars

    def elem_unconstrained(self, element):
        return element['min'] == 0 and element['max'] > 5 and element['charclass'] == '.' and not element['excl']

    def make_fail_states(self, change_fail, init_state, change_chars, last_change=None):
        """
        change_fail: the state reached by failing to make the change
        change_chars: the characters that should have changed in the first change state
        """
        index = 0
        current = change_fail
        pending_arc = None
        fail_state = None
#        print('  Making context fail states starting from', change_fail)
        for elem_index, element in enumerate(self):
#            print('   Element {}, index {}'.format(element, elem_index))
            next_element = self[elem_index+1] if elem_index < len(self) - 1 else None
            last_element = self[elem_index-1] if elem_index > 0 else None
            charstring = element['charclass']
            excl = element['excl']
            succ_string = self.make_arc_string(element)
            if element['min'] == 0:
                if not next_element:
                    if fail_state:
#                        print(' Making empty arc back to beginning from fail context', fail_state)
                        self.fst.add_arc(fail_state, init_state, '', '')
#                    if fail_state:
#                        # This is the last context element and there's a fail state;
#                        # make a loop with the element's succ_string on the fail state
#                        self.fst.add_arc(fail_state, fail_state, succ_string, succ_string)
                else:
#                    print('Unlimited class:', element, 'no way to fail here')
                    # No way to fail here; for now just duplicate the path
                    # First check whether the last element was a loop
                    if (elem_index == 0) or (last_element and last_element['min'] == 0):
                        # So we need a new state here
#                        print('Last element was a loop, so make a new state')
                        new_state, index = self.make_state(index, 'f')
                        self.fst.add_arc(current, new_state, succ_string, succ_string)
#                        print('    Current fail state', current, 'to RC state', new_state, 'with', succ_string)
                        self.fst.add_arc(new_state, new_state, succ_string, succ_string)
                        if next_element:
                            # Also need an escape arc to a state not yet created
                            next_arc_string = self.make_arc_string(next_element)
                            pending_arc = current, next_arc_string
                        current = new_state
                    else:
#                        print("Preceding state is not a loop, so make a loop if it's not already there")
                        if not self.fst.has_arc(current, current, succ_string, succ_string):
#                            print('Making loop in', current, 'with', succ_string)
                            self.fst.add_arc(current, current, succ_string, succ_string)
            else:
                new_state = None
#                print('A single character or class', charstring, 'excl', excl)
                # Fail by being in the complement of
                # charclass - excl
                fail_chars = AltRule.make_char_comp('.', charstring)
#                print('    Fail chars', fail_chars, 'current', current)
                # First check whether this string is already on a loop in the previous state
                if self.fst.has_arc(current, current, fail_chars, fail_chars):
#                    print('    Failure already possible with current state', current, 'so make it final')
                    self.fst.set_final(current)
                else:
                    # Exclude charclass, but also the last charclass if it was the first in the sequence,
                    # in an arc back to the first state
                    if last_element and last_element['min'] > 0:
                        # Check two elements back to make sure the immediate sequence stops there
                        if (elem_index > 1 and self[elem_index-2]['min'] == 0) or elem_index == 1:
                            # Assume nothing is excluded in the last element
                            last_charstring = last_element['charclass']
                            fail_chars = AltRule.make_char_comp('.', charstring + ',' + last_charstring)
                    if self.left_bounded:
                        fail_state, index = self.make_state(index, 'f', final=True)
#                        print('    Left bounded so make final fail state', fail_state, 'with in arc', fail_chars, 'from', current)
                        fail_arc = fail_chars
                        last_change_chars = [chars[2] for chars in last_change]
#                        print('Last change chars', last_change_chars)
                        if any(last_change_chars):
                            fail_arc = self.combine_fail_chars(fail_chars, last_change_chars)
                        self.fst.add_arc(current, fail_state, fail_arc, fail_arc)
#                        print('Making new RC fail state', fail_state, 'for fail chars', fail_chars, 'from', current)
                        # Final fail state needs loop for characters following  fail arc
#                        print('    Making loop for fail state', fail_state)
                        if change_chars:
                            change_char_string = ','.join(change_chars)
                            self.make_excl_loop(fail_state, change_char_string)
#                            print('    Make return arcs to change fail {} from {} using change chars {}'.format(change_fail, fail_state, change_chars))
                            for char in change_chars:
                                self.fst.add_arc(fail_state, change_fail, char, char)
                        else:
                            self.fst.add_arc(fail_state, fail_state, '.', '.')
                    else:
#                        print('Make an arc back to first state with fail chars', fail_chars)
                        self.fst.add_arc(current, change_fail, fail_chars, fail_chars)

                # If this is the last element, make a new non-final state for it
                if not next_element:
                    new_state, index = self.make_state(index, 'f')
                    self.fst.add_arc(current, new_state, succ_string, succ_string)
#                    print(' Element', element, 'should be final so making non-final state', new_state, 'for it')
                    # new_state must be followed by something
                    final_state, index = self.make_state(index, 'f', final=True)
                    self.fst.add_arc(new_state, final_state, '.', '.')
#                    print(' and making final state after that', final_state)
                    # and has a loop with anything after it
#                    print('Making loop for final state', final_state)
                    self.fst.add_arc(final_state, final_state, '.', '.')
                # If there are more ways to fail, make a way to succeed
                # for this element
#                print('Checking remaining elements')
                for remaining in self[elem_index+1:]:
                    if remaining['min'] > 0:
#                        print('Found limited class element', remaining)
#                        print("Making current {} final".format(current))
                        self.fst.set_final(current)
                        new_state, index = self.make_state(index, 'f', final=True)
#                        print('  And make a new final state to continue:', new_state)
                        self.fst.add_arc(current, new_state, succ_string, succ_string)
                        current = new_state
                        break
                if pending_arc and new_state:
#                    print('Creating pending arc from', pending_arc[0], 'to', new_state)
                    self.fst.add_arc(pending_arc[0], new_state, pending_arc[1], pending_arc[1])
                    pending_arc = None

        return current, index

    def combine_fail_chars(self, fail_chars, last_change_chars):
        last_change_string = ','.join(last_change_chars)
#        print(' Combining fail chars', fail_chars, 'with last change chars', last_change_string)
        if '-' in fail_chars:
            return fail_chars + ',' + last_change_string
        else:
            print('FAIL CHARS', fail_chars, 'SHOULD EXCLUDE CHARACTERS')

    def make_states(self, current, change_fail=None, change_chars=None, sep_start=False, nochange='',
                    last_change=None, init_state=None):
        '''change_fail is a state for failures of the change; change_chars are the characters for the
        first change state that chage. Both are only relevant for the  right context.'''
        imm_seq = []
        pending_arc = None
        index = 0
        state0 = current

#        if not self.left and change_fail:
#            print('{} MAKING CONTEXT states {}{}, starting from {} with change fail {} and change chars {}'.format(self, '(left)' if self.left else '(right)',
#                                                                                                                   ' (copy)' if self.copy else '',
#                                                                                                                   current,
#                                                                                                                   change_fail,
#                                                                                                                   change_chars))
        for element in self:
#            print('Processing context element', element)
            elem_index = element['index']
            next_element = self[elem_index+1] if elem_index < len(self) - 1 else None
            arc_string = self.make_arc_string(element)
#            print('Arc string', arc_string)
            # 0 or more instances of character or class
            if element['min'] == 0 and element['max'] > 1:
                # Make a new state if the last state also had a loop
                if elem_index > 0 and self[elem_index-1]['min'] == 0:
                    new_state, index = self.make_state(index, '', final=self.left and not self.copy)
                    self.fst.add_arc(current, new_state, arc_string, arc_string)
#                    print('Creating new state for second loop', new_state)
                    if next_element:
                        next_arc_string = self.make_arc_string(next_element)
                        pending_arc = current, next_arc_string
                    current = new_state
                if imm_seq:
                    # Check whether the last element in the sequence is in this class
                    if not self.char_in_element(imm_seq[-1][0], element):
                        # No, so end the sequence
                        imm_seq = []
                if not self.copy and not self.empty:
                    # Make a loop for the appropriate characters, but don't
                    # for (left) context copies so there's a way
                    # to escape to the right context; also don't bother when there's
                    # no context at all
                    excl = AltRule.charclass_excl(arc_string)
#                    print(self, 'making excl loop', current, excl)
                    self.make_excl_loop(current, excl)
                # If the loop doesn't include all characters except the next one
                # in the context, make an escape to a final state for all other
                # characters;
                # but don't do this for left context copies??
                if element['charclass'] != '.' and not self.copy:
                    if next_element:
                        if next_element['min'] > 0:
                            excl_chars = self.make_element_union(element, next_element)
                            other_chars = AltRule.make_char_comp('.', excl_chars)
                            escape, index = self.make_state(index, 'e', final=True)
                            self.fst.add_arc(current, escape, other_chars, other_chars)
                            self.fst.add_arc(escape, escape, '.', '.')
                # If this is the last element, make an escape for all cases except the change
                if not next_element and self.left:
#                    print('+++Last context element, need a loop with no change string', nochange, 'to', current)
                    self.combine_arc(current, current, nochange)
#                    self.fst.add_arc(current, current, nochange, nochange)
            # exactly 1 instance of character or class
            else:
                if imm_seq and element['min'] == 1:
#                    print('Must make return arc to previous state')
                    if len(imm_seq) == 1:
                        last_char = imm_seq[0][0]
                        last_state = imm_seq[0][1]
                        chars = '.-' + arc_string + ',' + last_char
#                        print('Sequence has only one element, so make link excluding', arc_string, last_char,
#                              'back to', last_state)
                        self.fst.add_arc(current, last_state, chars, chars) 
#                        print('And make loop with', last_char, 'in', current)
                        self.fst.add_arc(current, current, last_char, last_char)
                    else:
                        first_char = imm_seq[0][0]
                        second_state = imm_seq[1][1]
#                        print('Sequence has multiple elements, so make link with first character',
#                              first_char, 'back to second state', second_state)
                        self.fst.add_arc(current, second_state, first_char, first_char)
#                        print('Make an escape state from the last state', current, 'excluding this char',
#                              arc_string, 'and first char', first_char)
                        # Don't make the escape if this is a copy?
                        if not self.copy:
                            excl_chars = AltRule.make_char_comp('.', arc_string + ',' + first_char)
                            escape_state, index = self.make_state(index, 'e', final=True)
                            self.fst.add_arc(current, escape_state, excl_chars, excl_chars)
                            self.fst.add_arc(escape_state, escape_state, '.', '.')
                imm_seq.append((arc_string, current))
                # Make a new state for the context element
                # Left context states are final states unless they are copies of left contexts
                new_state, index = self.make_state(index, '', final=self.left and not self.copy)
                self.fst.add_arc(current, new_state, arc_string, arc_string)
                # Element is optional
                if element['min'] == 0:
                    self.fst.add_arc(current, new_state, '', '')
                if not next_element and self.left:
                    # Don't do this if the first acceptable change "character" is 0
                    if nochange != '.':
                        self.fst.add_arc(new_state, state0, nochange, nochange)
                if pending_arc:
#                    print('Creating pending arc from', pending_arc[0], 'to', new_state)
                    self.fst.add_arc(pending_arc[0], new_state, pending_arc[1], pending_arc[1])
                    pending_arc = None
                current = new_state
        if change_fail:
            self.make_fail_states(change_fail, init_state, change_chars, last_change)
        return current, index

    def make_state(self, index, infix, final=False):
        infix = '_' + infix
        if self.copy:
            infix += '+'
        if self.left:
            infix += 'l'
        else:
            infix += 'r'
        if index >= 0:
            index_string = str(index)
        else:
            index_string = ''
        label = self.fst.label + infix + index_string
        self.fst.add_state(label)
        if final:
            self.fst.set_final(label)
#        print('Making state', label)
        if index >= 0:
            index = index + 1
        return label, index

    def char_in_element(self, char, element):
        # char could be a character or a character class
        # element is an element dict
        charstring = element['charclass']
        if element['excl']:
            char_out = element['excl']
            char_out = char_out.split(',')
            if char in char_out:
                return False
        if charstring[0] == '@':
            # It's a class; find the elements in it from the cascade
            class_elements = self.expand_charclass(charstring)
            if char in class_elements:
                return True
        elif char == charstring:
            return True
        else:
            return False

    def expand_charclass(self, charclass):
        return self.classes.get(charclass, set())

    def make_element_union(self, e1, e2):
        if e1['excl']:
            if e2['excl']:
                print('No way yet to combine subtraction with subtraction')
            else:
                c1, x1 = e1['charclass'], e1['excl']
                x1 = x1.split(',')
                c2 = e2['charclass']
                c2 = c2.split(',')
                for c2a in c2[:]:
                    if c2a in x1:
                        x1.remove(c2a)
                        c2.remove(c2a)
                if len(x1) > 1:
                    x1 = ','.join(x1)
                elif not x1:
                    x1 = ''
                else:
                    x1 = x1[0]
                if c2:
                    c2 = ','.join(c2)
                    c1 = c1 + ',' + c2
                if x1:
                    c1 + '-' + x1
                return c1
        else:
            return e1['charclass'] + ',' + e2['charclass']
