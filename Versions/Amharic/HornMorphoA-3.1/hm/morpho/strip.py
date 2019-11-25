"""
This file is part of HornMorpho.

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
--------------------------------------------------------------------
Author: Michael Gasser <gasser@indiana.edu>

Strip off affixes, returning stem and affixes.

"""

import re

def sub_curry(lg='', n=1, acc=0, deacc=0, ins=''):
    """Function returning a function that takes a match object, to
    be used as the second argument of re.subn."""
    def subber(match):
        result = ''
        for gindex in range(n):
            i = gindex + 1
            string = match.group(i)
            if i == acc:
                string = lg.accent[string]
            elif i == deacc:
                string = lg.deaccent[string]
            result += string
        if ins:
            result += ins
        return result
    return subber

def sufstrip(word, suffixes, verbose=False):
    """
    word: string
    suffixes: dict with strings as keys and dicts of features values.
    Returns a list of segmentations and analyses.
    """
    # Start at the left-end to prefer longer suffixes
    result = []
    for n in range(1, len(word)):
        suf = word[n:]
#        print('suf {}'.format(suf))
        if suf in suffixes:
            attribs = suffixes[suf]
            aff = attribs[0]
            entries = attribs[1:]
            for entry in entries:
                stem = word[:n]
                pat = entry.get('pat', '')
                change = entry.get('change')
                # Use a different suffix for this entry
                aff = entry.get('aff', aff)
                # Whether to analyze the resulting stem (default is True)
                anal = entry.get('anal', entry.get('pos'))
                if pat and not change:
                    # Just check to see whether the entry matches the pattern
                    # and return it unchanged
#                    print("Trying to match pattern {} against stem {}".format(pat, stem))
                    if re.search(pat, stem):
                        result.append((stem + aff, entry.get('gram'), anal))
                    else:
                        continue
                if pat and change:
                    form, nmatch = re.subn(pat, change, stem)
                    if nmatch:
                        # form has changed
                        result.append((form + aff, entry.get('gram'), anal))
                    else:
                        continue
    return result

def accent(word, index):
    """Accent the first vowel in index position on right side."""
    count = 0
    segs = []
    done = False
    for pos in range(1, len(word)+1):
        c = word[-pos]
        if c in ACCENT and not done:
            if count == index:
                segs.insert(0, ACCENT[c])
                done = True
            else:
                count += 1
                segs.insert(0, c)
        else:
            segs.insert(0, c)
    return ''.join(segs)

def deaccent(word, index):
    """Deaccent the first vowel in index position on right side.
    If index is negative, deaccent all vowels."""
    count = 0
    segs = []
    done = False
    for pos in range(1, len(word)+1):
        c = word[-pos]
#        print('pos {}, count {}, c {}'.format(pos, count, c))
        if done or c not in DEACCENT:
            segs.insert(0, c)
            if c in ACCENT:
                count += 1
        elif c in DEACCENT:
            if index < 0 or count == index:
                segs.insert(0, DEACCENT[c])
                done = True
            else:
                count += 1
                segs.insert(0, c)
    return ''.join(segs)

#### Worry about prefixes later.
##
##def prestrip(word, prefixes):
##    """word: string
##    prefixes: dict with strings as keys and lists of prefixes as values.
##    """
##    # Start at right-end of word to prefer longer prefixes
##    for n in range(1, len(word)):
##        pre = word[:-n]
###        print('pre {}'.format(pre))
##        if pre in prefixes:
##            stem = word[-n:]
##            return stem + prefixes[pre].get('aff', '')
##    return False

##def left_accent(word, index):
##    """Accent the first vowel in index position on left side."""
##    count = 0
##    segs = []
##    done = False
##    for pos in range(0, len(word)):
##        c = word[pos]
##        if c in ACCENT and not done:
##            if count == index:
##                segs.append(ACCENT[c])
##                done = True
##            else:
##                count += 1
##                segs.append(c)
##        else:
##            segs.append(c)
##    return ''.join(segs)
##
##def left_deaccent(word, index):
##    """Deaccent the first vowel in index position on left side."""
##    count = 0
##    segs = []
##    done = False
##    for pos in range(0, len(word)):
##        c = word[pos]
##        if c in ACCENT and not done:
##            if count == index:
##                segs.append(ACCENT[c])
##                done = True
##            else:
##                count += 1
##                segs.append(c)
##        else:
##            segs.append(c)
##    return ''.join(segs)

