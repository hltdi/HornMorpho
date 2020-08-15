"""
This file is part of HornMorpho, which is a project of PLoGS

    Copyleft 2020. Michael Gasser.

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

------------------------------------------------------
Author: Michael Gasser <gasser@indiana.edu>

Conversion of HornMorpho features to UniMorph features.

-- 2020-08-14
   Created.
"""

from .semiring import *
import os, re

class UniMorph:
    """
    Functions for converting between HornMorpho and UniMorph features.
    """

    pos_re = re.compile(r'\s*POS\s*(.*)$')
    feat_re = re.compile(r'\s*(.*)::\s*(.*)$')
    superfeat_re = re.compile(r'\s*(.*)::$')
    subfeat_re = re.compile(r'\s*(.*):\s*(.*)$')

    def __init__(self, language):
        # A Language instance
        self.language = language
        self.hm2um = {}
        self.um2hm = {}

    def __repr__(self):
        return "UM:{}".format(self.language.abbrev)

    def convert(self, fs):
        """
        Convert a FeatStruct to a UM string.
        """
        um = ''
        for f, v in self.hm2um.items():
            if f in fs:
                # FeatStruct has a value for this feature
                if isinstance(v, dict):
                    # Subfeats are specified
                    for ff, vv in v.items():
                        if isinstance(ff, tuple):
                            # Subfeat is a set of feats
                            pass

    def get_path(self):
        """
        Path for where the UM conversion data is stored for
        the language.
        """
        d = self.language.get_dir()
        return os.path.join(d, self.language.abbrev + ".um")

    def read(self):
        """
        Read in the UM converstion data.
        """
        path = self.get_path()
        current_pos = ''
        current_supfeat = ''
        current_feats = {}
        current_pos_dict = {}
        try:
            with open(path, encoding='utf8') as file:
                lines = file.read().split('\n')[::-1]
                while lines:
                    line = lines.pop().split('#')[0].strip() # strip comments

                    # ignore empty lines
                    if not line: continue

                    m = UniMorph.pos_re.match(line)
                    if m:
                        pos = m.group(1)
                        print("Matched POS {}".format(pos))
                        if current_pos:
                            if current_supfeat:
                                current_pos_dict[current_supfeat] = current_feats
                                current_supfeat = ''
                                current_feats = {}
                            self.hm2um[current_pos] = current_pos_dict
                        current_pos = pos
                        continue
                    m = UniMorph.superfeat_re.match(line)
                    if m:
                        supfeat = m.group(1)
                        print("Matched superfeat {}".format(supfeat))
                        if current_supfeat:
                            current_pos_dict[current_supfeat] = current_feats
                            current_supfeat = ''
                            current_feats = {}
                        current_supfeat = supfeat
                        continue
                    m = UniMorph.feat_re.match(line)
                    if m:
                        feat, value = m.groups()
                        print("Matched feat {}: {}".format(feat, value))
                        current_pos_dict[feat] = value
                        continue
                    m = UniMorph.subfeat_re.match(line)
                    if m:
                        feat, value = m.groups()
                        print("Matched subfeat {}: {}".format(feat, value))
                        if ',' in feat:
                            feat = tuple(feat.split(','))
                        current_feats[feat] = value
                        continue
                    print("Failed to match line {}".format(line))
            if current_pos:
                if current_supfeat:
                    current_pos_dict[current_supfeat] = current_feats
                self.hm2um[current_pos] = current_pos_dict

        except IOError as e:
            print("No UM file for {}".format(self.language.abbrev))
