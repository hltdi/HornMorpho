"""
This file is part of HornMorpho, which is a project of PLoGS

    Copyleft 2008-2025. Michael Gasser.

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
Author: Michael Gasser <gasser@iu.edu>

morpho:

This package includes modules that deal with finite-state transducers (FSTs) weighted
with feature structure sets (as in Amtrup, 2003).

Transduction handles ambiguity, returning output strings and accumulated weights for
all paths through an FST.

Composition of weighted FSTs is also supported.

-- 2011-07
   New modules for compiling alternation rule (altrule) and morphotactic (mtax) FSTs.
   New modules for translation dictionaries (tdict) and menus (menu).
-- 2024
   Many new modules added in the interim
"""

__all__ = ['altrule', 'fs', 'fst', 'internals', 'language',\
           'languages', 'letter_tree', 'logic', 'morphology', 'mtax',\
           'rule', 'semiring', 'strip', 'um', 'utils', 'anal', 'corpus', 'sentence',\
           'roots', 'tmp', 'mut', 'lextr', 'gui', 'word', 'cg', 'usr', 'disamb']

#            'menu', 'tdict', 'dev', 'trans'

from .corpus import *

# 2020.08.14: eliminating trans classes for now
# from .trans import *
