"""
This file is part of the HornMorpho package.

Copyright (C) 2011, 2012, 2013, 2014, 2017, 2018, 2022, 2023
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

2015.03.04
-- Extended options. Now possible:
   -> +lexfile+ [FSS]
"""

import re, os
from .utils import segment
from .semiring import FSSet, UNIFICATION_SR, TOPFSS
from .fs import FeatStructParser
from .ees import EES, TARGET_WT_CONV
#from .fst import FSTCascade

# Convert weight string to one suitable for translation target
conv_string = lambda string: EES.conv_string(string, TARGET_WT_CONV)

# Default name for final state
DFLT_FINAL = 'fin'
# Signifies no input or output characters associated with an FSS
NO_INPUT = '--'

# new state; capture the state only
STATE_RE = re.compile(r'\s*\$\s+(\S+)$')
# Feature structure for subsequent paths; capture the FS string
# and indentation
FS_RE = re.compile(r'(\s*)(\[.+?\])$')
# Path: input string to match ... Feature Structure Set; capture
# indentation, input string, optional output string and FSSet
PATH_RE = re.compile(r'(\s*?)(\S+)\s*(?:<(.*?)>)?\s*(\[.*?\])?$')
# Path with no FSS
PATH_NO_FS_RE = re.compile(r'(\s*?)(\S+)$')
# A lex file and a Feature Structure Set; capture indentation,
# file name, and FSSet
LEX_RE = re.compile(r'(\s*?)\+(.*?)\+\s+(\[.*?\])$')
# A cascade spec in a separate file; capture indentation and file name
#    >>CASC<<
CASC_RE = re.compile(r'(\s*?)>>(.*?)<<$')
# An FST in a separate file and a FSS; capture indentation,
# file name, and FSSet
#    >FST<  [FSS]
FST_RE = re.compile(r'(\s*?)>(.*?)<\s+(\[.*?\])$')
# Specify a state other than the next one and a FSS; capture both.
SHORTCUT_FS_RE = re.compile(r'\s*->\s*(\S+)\s*(\[.+?\])$')
# Specify a state other than the next one and a lex file; capture both.
SHORTCUT_LEX_RE = re.compile(r'\s*->\s*(\S+)\s*\+(.*?)\+$')
# Specify a state other than the next one and a lex file and a FSS; capture all three.
SHORTCUT_LEX_FS_RE = re.compile(r'\s*->\s*(\S+)\s*\+(.*?)\+\s*(\[.+?\])$')

class MTax:

    PARSER = FSSet.parse

    def __init__(self, fst, directory=''):
        self.fst = fst
        self.cascade = fst.cascade
        self.seg_units = self.cascade.seg_units
        self.directory = directory
        self.weighting = UNIFICATION_SR
        self.states = []

    def __repr__(self):
        return "MTax {}".format(self.fst.label)

    def parse(self, label, s, gen=False, gemination=True, output_segs=True, verbose=False):
        """
        Parse a morphotactic FST from a string consisting of multiple lines from a file.
        """
#        print("** MTAX parse, output segs = {}".format(output_segs))
        # Feature structures
        FSs = []

        # Current state
        current_state = None

        # Current FS
        current_fs = None

        # Join lines ending in ';'
        pending_line = ''

        # Current indentation within a state
        current_indent = 0

        lines = s.split('\n')[::-1]

        while lines:
            line = lines.pop().split('#')[0].rstrip() # strip comments

            if not line: continue
#            print("** MTAX line {}".format(line))

            if line[-1] == ';':
                # Continue on to next line
                pending_line += line
                continue

            if pending_line:
                # Add this line onto pending line before parsing
                line = pending_line + line
                pending_line = ''

            # New state
            m = STATE_RE.match(line)
            if m:
                label = m.group(1)
                # Create the state
                self.fst.add_state(label)
                if not current_state:
                    # This must be the first state, so make it initial
                    self.fst._set_initial_state(label)
                # Use this for all paths and lex files until the next state
                current_state = [label, {'paths': [], 'shortcuts': []}]
                current_fs = None
                current_indent = 0
                self.states.append(current_state)
                continue

            # Lex file to be converted to a letter tree, then to an FST and concatenated in
            # Destination FST not in file, to be used for all entries.
            # +file+
            m = LEX_RE.match(line)
            if m:
                indentation, label, fss = m.groups()
                if gen and fss:
                    fss = conv_string(fss)
                weight = self.weighting.parse_weight(fss)
                filename = label + '.lex'
                if len(indentation) > current_indent and current_fs:
                    # Update FSS with current FS
                    weight = weight.update(weight, current_fs)
                current_state[1]['paths'].append((filename, None, weight))
                continue

            # Cascade file to be compiled and inserted.
            # >>file<<
            m = CASC_RE.match(line)
            if m:
                indentation, label = m.groups()
                filename = label + '.cas'
                current_state[1]['paths'].append((filename, None, TOPFSS))
                continue

            # FST file to be compiled and concatenated in.
            # >file<
            m = FST_RE.match(line)
            if m:
                indentation, label, fss = m.groups()
#                print('Lex', label)
                if gen and fss:
                    fss = conv_string(fss)
                weight = self.weighting.parse_weight(fss)
                filename = label + '.fst'
                if len(indentation) > current_indent and current_fs:
                    # Update FSS with current FS
                    weight = weight.update(weight, current_fs)
                current_state[1]['paths'].append((filename, None, weight))
                continue

            # Feature structure for subsequent paths
            m = FS_RE.match(line)
            if m:
                indentation, fs = m.groups()
                if gen and fs:
                    fs = conv_string(fs)
                # a FeatStruct, not a FSSet
                weight = MTax.PARSER(fs)
#                FeatStructParser().parse(fs)
                current_fs = weight
                current_indent = len(indentation)
#                print("FS for next paths: {}, indent {}".format(current_fs.__repr__(), current_indent))
                continue

            # Path: input string and FSSet
            m = PATH_RE.match(line)
            if m:
                indentation, in_string, out_string, fss = m.groups()
                if out_string:
                    if out_string[0] == '$':
                        # This means the output string is only for generation and seglevel=0
                        if not output_segs:
                            out_string = out_string[1:]
                        else:
                            out_string = None
                elif not output_segs:
                    # This prevents in_string from being copied to out_string for seglevel=0 or generation
                    # unless there is an explicit out_string
                    out_string = ''
#                print("  ** PATH in {} out {} fss {}".format(in_string, out_string, fss))
                if gen and fss:
                    fss = conv_string(fss)
                weight = MTax.PARSER(fss) if fss else None
                if len(indentation) > current_indent and current_fs:
                    # Update FSS with current FS
#                    print("  String {}, FS {}, current FS {}".format(in_string, weight, current_fs.__repr__()))
                    if weight:
                        weight = weight.unify(current_fs)
                    else:
                        weight = current_fs
#                    weight.update(weight, current_fs)
#                    print("  New weight {}".format(weight))
                current_state[1]['paths'].append((in_string, out_string, weight))
                continue

            # Shortcut to another state with the associated FSS
            m = SHORTCUT_FS_RE.match(line)
            if m:
                next_state, fss = m.groups()
                if gen and fss:
                    fss = conv_string(fss)
                fss = self.weighting.parse_weight(fss)
                current_state[1]['shortcuts'].append((next_state, None, fss))
#                print("Shortcut {}, {}".format(next_state, fss))
                continue

            # Shortcut to another state via a lex file
            m = SHORTCUT_LEX_RE.match(line)
            if m:
                next_state, label = m.groups()
                filename = label + '.lex'
                current_state[1]['shortcuts'].append((next_state, filename, None))
                continue

            # Shortcut to another state via a lex file and an associated FSS
            m = SHORTCUT_LEX_FS_RE.match(line)
            if m:
                next_state, label, fss = m.groups()
                if gen and fss:
                    fss = conv_string(fss)
                fss = self.weighting.parse_weight(fss)
                filename = label + '.lex'
                current_state[1]['shortcuts'].append((next_state, filename, fss))
                continue

            # Path: input string but no FSSet
            m = PATH_NO_FS_RE.match(line)
            if m:
                indentation, in_string = m.groups()
                if ':' in in_string:
                    in_string, out_string = in_string.split(':')
                    in_string = in_string.strip()
                    out_string = out_string.strip()
                else:
                    out_string = in_string
                weight = ''
                if len(indentation) > current_indent and current_fs:
                    weight = FSSet(current_fs)
                current_state[1]['paths'].append((in_string, out_string, weight))
                continue

            raise ValueError("bad line: %r" % line)
