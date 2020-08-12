#!/usr/bin/env python

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
    along with HornMorpho.  If not, see <http://www.gnu.org/licenses/>.

Author: Michael Gasser <gasser@indiana.edu>

Convert a form in phonetic SERA to Tadesse's SERA.
"""

import re

# Convert in this order to prevent confusion with multiple uses of
# 'x' and 'i'
TA_CONSONANTS = [
                ('P', 'px'), ('T', 'tx'), ('C', 'cx'), ('S', 'xx'),
                ('N', 'nx'), ('Z', 'zx')]
TA_VOWELS = [('i', 'ii'), ('E', 'ie'), ('I', 'ix')]
TA_GEM_RE = re.compile(r'(\w)_')
TA_GS_RE = re.compile(r"'([aeiouEI])")

def ta_convert(form):
    '''
    Return form converted from SERA to Tadesse's SERA.
    '''
    # This has to come first because each consonant is still one character
    form = ta_convert_gem(form)
    # This has to come next because x is part of other characters
    form = form.replace('x', 'sx')
    # This has to come before the vowels because they may end up with two characters.
    form = ta_convert_gs(form)
    # Some consonants now become two characters
    for char_in, char_out in TA_CONSONANTS:
        form = form.replace(char_in, char_out)
    # Some vowels now become two characters
    for char_in, char_out in TA_VOWELS:
        form = form.replace(char_in, char_out)
    return form

def ta_convert_gem(form):
    '''
    Replace X_ with 'X in form, returning the result.
    '''
    return TA_GEM_RE.sub(r"'\1", form)

def ta_convert_gs(form):
    """Replace 'V with axV."""
    return TA_GS_RE.sub(r"ax\1", form)
