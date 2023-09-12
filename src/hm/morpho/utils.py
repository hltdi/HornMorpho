"""
This file is part of HornMorpho.
    Copyleft (Ɔ) 2007-2023.
    by HLTDI and PLoGS <gasser@indiana.edu>

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

Miscellaneous utility functions.
"""

import collections, functools
# tarfile, zipfile, codecs, re, copy, pickle, types, shelve

from .tdict import *
from .menu import *

def allcombs(seqs):
    """Returns a list of all sequences consisting of one element from each of seqs.
    This could also be done with itertools.product."""
    if not seqs:
        return []
    res = [[x] for x in seqs[0]]
    for item in seqs[1:]:
        for i in range(len(res)-1, -1, -1):
            rr = res[i]
#            print(" {} | {} | {}".format(i, rr, [(rr + [itemitem]) for itemitem in item]))
            res[i:i+1] = [(rr + [itemitem]) for itemitem in item]
    return res

### Segmentation of words into graphemes/phonemes.

def segment(word, units, correct=True):
    res = []
    pos = 0
    while pos < len(word):
        ch = word[pos]
        if ch in units[0]:
            res.append(ch)
            pos += 1
        else:
            sublists = units[1]
            if ch in sublists:
                sublist = sublists[ch]
                if pos < len(word) - 1 and ch + word[pos + 1] in sublist:
                    if pos < len(word) - 2 and ch + word[pos + 1:pos + 3] in sublist:
                        res.append(ch + word[pos + 1:pos + 3])
                        pos += 3
                    else:
                        res.append(ch + word[pos + 1])
                        pos += 2
                else:
                    res.append(ch)
                    pos += 1
            elif ch == ' ':
                res.append(' ')
                pos += 1
            elif correct:
                print(ch, 'in', word, 'is not an acceptable character')
                return
            else:
                res.append(ch)
                pos += 1
    return res

### String functions
def string_dif(str1, str2):
    """
    Assumes strings are same length. Returns the positions and characters that are
    different.
    """
    res = []
    for index, (c1, c2), in enumerate(zip(str1, str2)):
        if c1 != c2:
            res.append((index, c1, c2))
    return res
    
def isnumstring(string):
    """
    Is string a string representation of a numeral?
    """
    string = string.replace(".", '', 1)
    string = string.replace("-", '', 1)
    return string.isdigit()

### Sequence functions

def pad2eqlen(l1, l2, paditem=''):
    '''
    Make l1 and l2 the same length, using paditem to pad the shorter one at the end.
    '''
    len1 = len(l1)
    len2 = len(l2)
    if len1 > len2:
        l2.extend([paditem] * (len1 - len2))
    elif len2 > len1:
        l1.extend([paditem] * (len2 - len1))

def isseq(item):
    return isinstance(item, collections.Sequence)

def flatten(seq):
    """Flattens the sequence, consisting of elements or sequences."""
    if not seq:
        return []
    result = []
    for thing in seq:
        if isinstance(thing, (list, tuple, set)):
            result.extend(flatten(thing))
        else:
            result.append(thing)
    return result

def reduce_lists(lists):
    '''Flatten a list of lists (doesn't mutate lists).'''
#    print("Reducing {}".format(lists))
    return functools.reduce(lambda x, y: x + y, lists) if lists else []

def reduce_sets(sets):
    '''Flatten a list of sets (doesn't mutate sets).'''
    return functools.reduce(lambda x, y: x | y, sets) if sets else []

def every(predicate, seq):
    """True if every element of seq satisfies predicate.
    >>> every(callable, [min, max])
    1
    >>> every(callable, [min, 3])
    0
    """
    for x in seq:
        if not predicate(x): return False
    return True

def some(predicate, seq):
    """If some element x of seq satisfies predicate(x), return predicate(x).
    >>> some(callable, [min, 3])
    1
    >>> some(callable, [2, 3])
    0
    """
    for x in seq:
        px = predicate(x)
        if  px: return px

def del_suffix(string, sufstart, last = True):
    '''String without everything after the last (or first) occurrence of sufstart.'''
    sufpos = string.rfind(sufstart) if last else string.find(sufstart)
    if sufpos >= 0:
        return string[:sufpos]
    else:
        return string

### Complex set objects
### An object is a set of explicit attributes (lists, dicts, and dict values).
### Implicit attributes are "inherited" from
### the object's "parents" -- objects of the same class that represent subsets.

##class Set(object):
##
##    def add_parent(self, parent):
##        if hasattr(self, 'parents'):
##            self.parents.append(parent)
##        else:
##            self.parents = [parent]
##
##    def get_parents(self):
##        return getattr(self, 'parents', [])
##
##    def isa(self, anc):
##        '''Does this thing have anc as a subset?  Should it inherit from anc?'''
##        parents = self.get_parents()
##        return anc in parents or some(lambda p: p.isa(anc), parents)
##
##    def get_attr(self, attr):
##        a = getattr(self, attr, None)
##        return a if a != None else some(lambda p: p.get_attr(attr), self.get_parents())
##
##    def get_list(self, attr):
##        return getattr(self, attr, []) or some(lambda p: p.get_list(attr), self.get_parents()) or []
##
##    def get_dict(self, attr):
##        d = getattr(self, attr, {})
##        return d if d != None else some(lambda p: p.get_dict(attr), self.get_parents()) or {}
##
##    def get_dictvalue(self, dictattr, key):
##        '''Get the value for the key in the dict which is the value of dictattr.'''
##        return getattr(self, dictattr, {}).get(key, None) or \
##               some(lambda p: p.get_dictvalue(dictattr, key), self.get_parents())
##
##class DictSet(Set, dict):
##
##    def get_value1(self, key, partial = False):
##        v = self.get(key, None)
##        if v != None:
##            return v
##        elif partial:
##            v = dict_partkey(self, key)
##            if v != None:
##                return v
##
##    def get_value(self, key, partial = False, default = None):
##        '''Get value for key in this Set or its parents, matching partial key if partial.'''
##        v = self.get_value1(key, partial = partial)
##        if v != None:
##            return v
##        else:
##            v = some(lambda p: p.get_value(key, partial = partial),
##                     self.get_parents())
##            if v != None:
##                return v
##            elif default:
##                v = default.get_value1(key, partial = partial)
##                if v != None:
##                    return v
##
##    def get_value_partial(self, part_key, default = None):
##        '''Get value for part_key in the Set or its parents.'''
##        v = dict_partkey(self, part_key)
##        if v != None:
##            return v
##        else:
##            v = some(lambda p: dict_partkey(p, part_key), self.get_parents())
##            if v != None:
##                return v
##            elif default:
##                v = dict_partkey(default, part_key)
##                if v != None:
##                    return v

##def list_pairs(seq):
##    '''Return a list of successive pairs in seq.'''
##    return [(seq[i], seq[i + 1]) for i in range(0, len(seq), 2)]

##def zip_strings(string1, string2, seq_units=[], left_just=True):
##    """Make lists of corresponding elements in the two strings, padding on the right or left,
##    and segmenting with seq_units."""
##    # Segment
##    if seq_units:
##        string1 = segment(string1, seq_units, unic=True)
##        string2 = segment(string2, seq_units, unic=True)
##    else:
##        string1 = list(string1)
##        string2 = list(string2)
##    # Pad with empty strings
##    len_diff = len(string1) - len(string2)
##    if len_diff > 0:
##        string2.extend([''] * len_diff)
##    elif len_diff < 0:
##        string1.extend([''] * -len_diff)
##    return zip(string1, string2)

##def conc_strings(*strings):
##    """Concatenate strings together efficiently."""
##    file_str = StringIO()
##    for s in strings:
##        file_str.write(s)
##    return file_str.getvalue()

##def move_right(elem, seq, wrap = True):
##    '''Move elem one position to the right, pushing the elem that was there to the left.'''
##    if elem in seq:
##        pos = seq.index(elem)
##        if pos >= 0 and wrap or pos < len(seq) - 1:
##            next_pos = pos + 1
##            if next_pos >= len(seq):
##                next_pos = 0
##            next = seq[next_pos]
##            seq[pos] = next
##            seq[next_pos] = elem
##
##def move_left(elem, seq, wrap = True):
##    '''Move elem one position to the left, pushing the elem that was there to the right.'''
##    if elem in seq:
##        pos = seq.index(elem)
##        if pos >= 0 and wrap or pos > 0:
##            next_pos = pos - 1
##            if next_pos < 0:
##                next_pos = len(seq) - 1
##            next = seq[next_pos]
##            seq[pos] = next
##            seq[next_pos] = elem
##
##def swap(seq, pos1, pos2):
##    '''Swap the positions of the elements in pos1 and pos2 in seq.'''
##    if abs(pos1) < len(seq) and abs(pos2) < len(seq):
##        elem1 = seq[pos1]
##        seq[pos1] = seq[pos2]
##        seq[pos2] = elem1
##
##def make_list(elem, length):
##    '''A list with the given length with all elements elem.'''
##    return [elem for x in range(length)]

##def starts(subseq, seq):
##    '''Does the subseq begin the seq?'''
##    if len(subseq) > len(seq):
##        return False
##    else:
##        for i in range(len(subseq)):
##            if subseq[i] != seq[i]:
##                return False
##        return True
##
##def seq_index(subseq, seq, pos = 0):
##    '''Index of the subseq within the seq, -1 if it's not there at all.'''
##    if subseq[0] in seq:
##        start = seq.index(subseq[0])
##        if starts(subseq, seq[start:]):
##            return start + pos
##        else:
##            return seq_index(subseq, seq[start+1:], start)
##    else:
##        return -1
##
##def split_at(string, *positions):
##    '''Split string into list at positions.'''
##    result = []
##    index = 0
##    for p in positions:
##        result.append(string[index:p])
##        index = p
##    result.append(string[index:])
##    return result

##def split_repl(string, match_substr, repl, filt = True, re = None):
##    '''For first substring in string that matches match_substr or re, replace it with repl; return list.
##
##    Does not mutate anything.  If filter is True, empty strings are filtered out.'''
##    if not re and match_substr in string or re.search(string):
##        split_repl = subs_pos_list(string, match_substr, repl, 0)
##        if filt:
##            return filter(None, split_repl)
##        else:
##            return split_repl
##
##def split_repls(string, match_substr, repl, filt = True, re = None):
##    '''For each substring in string that matches match_substr or re, replace it with repl; return list.
##
##    Does not mutate anything.  If filter is True, empty strings are filtered out.'''
##    if not re and match_substr in string or re.search(string):
##        n_matches = string.count(match_substr) if not re and match_substr else len(re.findall(string))
##        res = []
##        for n in range(n_matches):
##            split_repl = subs_pos_list(string, match_substr, repl, n)
##            if filt:
##                res.append(filter(None, split_repl))
##            else:
##                res.append(split_repl)
##        return res
##
##def subs_pos_list(string, old, new, n):
##    '''Replace the nth occurrence of old with new in string, listing the three parts.'''
##    split = string.split(old)
##    if len(split) > n + 1:
##        current_string = ''
##        res = []
##        for i, x in enumerate(split):
##            if i != n:
##                current_string += x
##                if i < len(split) - 1:
##                    current_string += old
##            else:
##                current_string += x
##                res.append(current_string)
##                res.append(new)
##                current_string = ''
##        res.append(current_string)
##        return res

##def subs_pos(string, old, new, n):
##    '''Replace the nth occurrence of old with new in string.'''
##    positions = indices(old, string)
##    if len(positions) > n:
##        start = positions[n]
##        end = start + len(old)
##        return string[0:start] + new + string[end:]
##    else:
##        return string
##
##def substitute(seq, old, new):
##    '''Replace the first occurrence of old in seq with new.
##
##    Mutates seq.'''
##    if old in seq:
##        pos = seq.index(old)
##        seq[pos] = new
##        return seq
##
##def subs(seq, old, new):
##    '''Replaces all occurrences of old in seq with new, mutating seq.'''
##    for i, x in enumerate(seq):
##        if x == old:
##            seq[i] = new

##def indices(x, string):
##    '''List of indices in string where x is found.'''
##    positions = []
##    pos = 0
##    while pos < len(string):
##        next = string.find(x, pos)
##        if next >= 0:
##            positions.append(next)
##            pos = next + len(x)
##        else:
##            return positions
##    return positions

##def dict_partkey(dct, key):
##    '''Value for a key that's contained in the dct key.  None if there is none.'''
##    for k, v in dct.items():
##        if key in k:
##            return v

### Printing

##VERBOSITY = 0
##
##COMMENT = '#'

##def incr_verbosity():
##    globals()['VERBOSITY'] += 1
##
##def decr_verbosity():
##    globals()['VERBOSITY'] -= 1
##    globals()['VERBOSITY'] = max(globals()['VERBOSITY'], 0)
##
##def vprint(verbosity, *args):
##    '''Print args to stdout in one line, indent 2 * verbosity if VERBOSITY >= verbosity.'''
##    if globals()['VERBOSITY'] >= verbosity:
##        print(''.ljust(verbosity * 2), end=' ')
##        for a in args:
##            print(a, end=' ')
##        print()
##
##def list_str(ls):
##    '''A string with print names of the list elements.'''
##    if isinstance(ls, list) or isinstance(ls, tuple):
##        string = '['
##        for i, x in enumerate(ls):
##            string = string + list_str(x)
##            if i < len(ls) - 1:
##                string = string + ', '
##        return string + ']'
##    else:
##        return ls.__str__()

### File functions

##def comment(line):
##    '''Is this a comment line?'''
##    return line and line[0] == COMMENT
##
##def blank(line):
##    '''Is this a blank line?'''
##    return not line.split()
##
##def next_real_line(fileobj, splitit = False):
##    '''Return the next non-empty or uncommented line, False if EOF.'''
##    line = ''
##    while blank(line) or comment(line):
##        line = fileobj.readline()
##        if not line:
##            return False
##    if splitit:
##        return line.split()
##    else:
##        return line.strip()

##def peek_line(fileobj, passcomment = True, passblank = False):
##    '''Return the next line without going there.'''
##    pos = fileobj.tell()
##    line = fileobj.readline()
##    if (passcomment and comment(line)) or (passblank and blank(line)):
##        # Found a comment or blank link, peek further
##        return peek_line(fileobj, passcomment, passblank)
##    else:
##        # Return to beginning of previous line
##        fileobj.seek(pos, 0)
##        return line
##
##def next_line(fileobj, splitit = False):
##    '''Return the next uncommented line, False if blank or EOF.'''
##    line = '#'
##    while comment(line):
##        line = fileobj.readline()
##        if not line:
##            return False
##    if splitit:
##        return line.split()
##    else:
##        return line.strip()

##def remove_dup_lines(inpath, outpath, verbose = True):
##    '''Write file at input to file at output, eliminating duplicate lines.'''
##    try:
##        infile = file(inpath)
##        outfile = file(outpath, 'w')
##        seen = []
##        dups = 0
##        n = 0
##        for line in infile:
##            if line not in seen:
##                seen.append(line)
##                outfile.write(line)
##            else:
##                if verbose:
##                    print('repeated', line, end=' ')
##                dups += 1
##            n += 1
##            if n % 500 == 0:
##                print(n, 'lines')
##        infile.close()
##        outfile.close()
##        print(n, 'lines with', dups, 'duplicates')
##    except IOError:
##        print("Can't open file(s)")
##        return False

##def tarpy(direc = '.', filename = 'tar', others = ()):
##    tar = tarfile.open(filename + ".tgz", "w:gz")
##    for fl in [f for f in os.listdir(direc) if f[-3:] == '.py']:
##        tar.add(fl)
##    for o in others:
##        tar.add(o)
##    tar.close()
##
##def tarl(version):
##    tarpy(filename = 'lll' + str(version), others = (Data))

### PICKLING

##def _pickle_method(method):
##    func_name = method.im_func.__name__
##    obj = method.im_self
##    cls = method.im_class
##    return _unpickle_method, (func_name, obj, cls)
##
##def _unpickle_method(func_name, obj, cls):
##    for cls in cls.mro():
##        try:
##            func = cls.__dict__[func_name]
##        except KeyError:
##            pass
##        else:
##            break
##    return func.__get__(obj, cls)
##
##copy_reg.pickle(types.MethodType, _pickle_method, _unpickle_method)
