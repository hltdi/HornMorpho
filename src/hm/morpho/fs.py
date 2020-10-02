"""
This file is part of HornMorpho, which is part of the PLoGS project.

    <http://homes.soic.indiana.edu/gasser/plogs.html>

    Copyleft 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2016, 2018, 2020.
    PLoGS and Michael Gasser <gasser@indiana.edu>.

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

---------------------------------------------------
fs.py is a modification of featstruct.py in NLTK.
There is no support for variables in feature structures,
and there are modest feature structure hierachies.

Copyright (C) 2001-2007 University of Pennsylvania
Author: Edward Loper <edloper@gradient.cis.upenn.edu>,
        Rob Speer,
        Steven Bird <sb@csse.unimelb.edu.au>
URL: <http://www.nltk.org/>

Modified by Michael Gasser <gasser@cs.indiana.edu>

2008:
  Added FSHier.

2009-06-11:
  simplify_unify modified to accommodate None as feature value,
    now returns 'fail' rather than None when it fails.
2014-07:
  A few minor changes, so need to recompile for Cython.
2016-05-19:
  Changed FS.__repr__() so it includdes quotes with string values that contain commas.
  Important because __repr__ is used in writing FSTs to files.
"""

import re, copy
from .logic import Variable, Expression, SubstituteBindingsI, LogicParser
from . import internals

def _flatten(lst, cls):
    """
    Helper function -- return a copy of list, with all elements of
    type C{cls} spliced in rather than appended in.
    """
    result = []
    for elt in lst:
        if isinstance(elt, cls): result.extend(elt)
        else: result.append(elt)
    return result

######################################################################
# Interface class for FeatStruct and FSSet
######################################################################

class FS:

    def delete(self, features):
        print("delete() not defined")

#    def unify_FS(self, fs, strict=False, verbose=False):
#        print("Not defined")

#    def agree(self, target, agrs, force=False):
#        print("Not defined")

#    def upd(self, fs):
#        """
#        Return an FS/FSSet with features updated to agree with
#        fs.
#        """
#        print("Not defined")

######################################################################
# Feature Structure
######################################################################

class FeatStruct(FS):

    def __init__(self, features=None, types=None, fsh=None,
                 label='', freeze=False, **morefeatures):
        """
        Create a new feature structure, with the specified features.

        @param types: A list of feature structure types.
        @param features: The initial value for this feature structure.
        If C{features} is a C{FeatStruct}, then its features are copied
        (shallow copy).  If C{features} is a C{dict}, then a feature is
        created for each item, mapping its key to its value.  If
        C{features} is a string, then it is parsed using L{parse()}.  If
        C{features} is a list of tuples C{name,val}, then a feature is
        created for each tuple.
        """
        self._frozen = False
        self._features = {}
        #{ Added by MG
        self._types = types or set()
        self._label = label
        # FS Hierarchy
        self._fsh = fsh
        #}
        if isinstance(features, str):
            FeatStructParser(fsh=fsh).parse(features, self)
            self.update(morefeatures)
        else:
            self.update(features, **morefeatures)
        if freeze:
            self.freeze()

    # Note: The Feature class is added to this list, when it is defined
    # below.
    _feature_name_types = (str,)
    """A list of the types that feature names may have."""

    #////////////////////////////////////////////////////////////
    #{ Types and inheritance
    #////////////////////////////////////////////////////////////

##    def types(self):
##        return self._types
##
##    def add_type(self, tp):
##        tp.freeze()
##        self._types.add(tp)
##
##    def get_all_types(self):
##        """A list of all type ancestors of self."""
##        if not self._types:
##            return set()
##        else:
##            return self._types | reduce_sets([t.get_all_types() for t in self._types])
##
##    def inherit(self, trace=False):
##        """Inherit features from all ancestors."""
##        return inherit_all(self, trace=trace)
##
##    def inherit_feat(self, name_or_path, default=None):
##        """Attempt to find a value for name_or_path in self or its ancestors."""
##        val = self.get(name_or_path)
##        if val != None:
##            return val
##        else:
##            for anc in self.get_all_types():
##                val = anc.get(name_or_path)
##                if val != None:
##                    return val
##        return default
##
##    def label(self):
##        return self._label

    #////////////////////////////////////////////////////////////
    #{ Read-only mapping methods
    #////////////////////////////////////////////////////////////

    def __getitem__(self, name_or_path):
        """If the feature with the given name or path exists, return
        its value; otherwise, raise C{KeyError}."""
        if isinstance(name_or_path, self._feature_name_types):
            return self._features[name_or_path]
        if name_or_path == ():
            return self
        else:
            try:
                parent, name = self._path_parent(name_or_path, '')
                return parent._features[name]
            except KeyError: raise KeyError(name_or_path)

    def get(self, name_or_path, default=None):
        """If the feature with the given name or path exists, return its
        value; otherwise, return C{default}."""
        try:
            return self[name_or_path]
        except KeyError:
            return default
    def __contains__(self, name_or_path):
        """Return true if a feature with the given name or path exists."""
        try:
            self[name_or_path]; return True
        except KeyError:
            return False
    def has_key(self, name_or_path):
        """Return true if a feature with the given name or path exists."""
        return name_or_path in self
    def keys(self):
        """Return an iterator of the feature names in this FeatStruct."""
        return self._features.keys()
    def values(self):
        """Return an iterator of the feature values in this FeatStruct."""
        return self._features.values()
    def items(self):
        """Return an iterator of (name, value) pairs for all features in
        this FeatStruct."""
        return self._features.items()
    def __iter__(self): # same as keys
        """Return an iterator over the feature names in this FeatStruct."""
        return iter(self._features)
    def __len__(self):
        """Return the number of features defined by this FeatStruct."""
        return len(self._features)

    #////////////////////////////////////////////////////////////
    #{ Mutating mapping methods
    #////////////////////////////////////////////////////////////

    def __delitem__(self, name_or_path):
        """If the feature with the given name or path exists, delete
        its value; otherwise, raise C{KeyError}."""
        if self._frozen: raise ValueError(self._FROZEN_ERROR)
        if isinstance(name_or_path, self._feature_name_types):
            del self._features[name_or_path]
        else:
            try:
                parent, name = self._path_parent(name_or_path, 'deleted')
                del parent._features[name]
            except KeyError: raise KeyError(name_or_path)

    def __setitem__(self, name_or_path, value):
        """Set the value for the feature with the given name or path
        to C{value}.  If C{name_or_path} is an invalid path, raise
        C{KeyError}."""
        if self._frozen:
            print(self.__repr__(), 'is frozen')
            raise ValueError(self._FROZEN_ERROR)
        if isinstance(name_or_path, self._feature_name_types):
            self._features[name_or_path] = value
        else:
            try:
                parent, name = self._path_parent(name_or_path, 'set')
                parent[name] = value
            except KeyError: raise KeyError(name_or_path)

    def clear(self):
        """Remove all features from this C{FeatStruct}."""
        if self._frozen: raise ValueError(self._FROZEN_ERROR)
        self._features.clear()

    def update(self, features=None, **morefeatures):
        """
        If C{features} is a mapping, then:
            >>> for name in features:
            ...     self[name] = features[name]

        Otherwise, if C{features} is a list of tuples, then:
            >>> for (name, value) in features:
            ...     self[name] = value

        Then:
            >>> for name in morefeatures:
            ...     self[name] = morefeatures[name]
        """
        if self._frozen: raise ValueError(self._FROZEN_ERROR)
        if features is None:
            items = ()
        elif hasattr(features, 'keys'):
            items = features.items()
        elif hasattr(features, '__iter__'):
            items = features
        else:
            raise ValueError('Expected mapping or list of tuples')

        for key, val in items:
            if not isinstance(key, self._feature_name_types):
                raise TypeError('Feature names must be strings')
            # The case where the value is a mapping; first convert
            # it to a FeatStruct
            if hasattr(val, 'keys'):
                val = FeatStruct(val)
            self[key] = val
        for key, val in morefeatures.items():
            if not isinstance(key, self._feature_name_types):
                raise TypeError('Feature names must be strings')
            self[key] = val

    def delete(self, features, freeze=False):
        """
        Return a copy of this FeatStruct with each feature in features
        removed. features is a list of feature names or feature paths
        (tuples of feature names).
        """
        fs = self.copy()
        for feat_or_path in features:
            try:
                del fs[feat_or_path]
            except KeyError:
                print("Warning: {} not in {}".format(feat_or_path, fs.__repr__()))
        if freeze:
            fs.freeze()
        return fs

    def _path_parent(self, path, operation):
        """
        Helper function -- given a feature path, return a tuple
        (parent, name) containing the parent and name of the specified
        feature.  If path is (), then raise a TypeError.
        """
        if not isinstance(path, tuple):
            raise TypeError('Expected str or tuple of str.  Got %r.' % path)
        if len(path) == 0:
            raise TypeError('The path () can not be %s' % operation)
        val = self
        for name in path[:-1]:
            if not isinstance(name, str):
                raise TypeError('Expected str or tuple of str.  Got %r.'%path)
            if not isinstance(val.get(name), FeatStruct):
                raise KeyError(path)
            val = val[name]
        if not isinstance(path[-1], str):
            raise TypeError('Expected str or tuple of str.  Got %r.' % path)
        return val, path[-1]

    ##////////////////////////////////////////////////////////////
    #{ Equality & Hashing
    ##////////////////////////////////////////////////////////////

    def equal_values(self, other):
        """
        @return: True if C{self} and C{other} assign the same value to
        to every feature.  In particular, return true if
        C{self[M{p}]==other[M{p}]} for every feature path M{p} such
        that C{self[M{p}]} or C{other[M{p}]} is a base value (i.e.,
        not a nested feature structure).

        @param check_reentrance: If true, then also return false if
            there is any difference between the reentrances of C{self}
            and C{other}.

        @note: the L{== operator <__eq__>} is equivalent to
            C{equal_values()} with C{check_reentrance=True}.
        """
        return self._equal(other, set(), set(), set())

    def __eq__(self, other):
        """
        Return true if C{self} and C{other} are both feature
        structures, assign the same values to all features, and
        contain the same reentrances.  I.e., return
        C{self.equal_values(other, check_reentrance=True)}.

        @see: L{equal_values()}
        """
        return self._equal(other, set(), set(), set())

    def __ne__(self, other):
        """
        Return true unless C{self} and C{other} are both feature
        structures, assign the same values to all features, and
        contain the same reentrances.  I.e., return
        C{not self.equal_values(other, check_reentrance=True)}.
        """
        return not self.__eq__(other)

    def _equal(self, other, visited_self, visited_other, visited_pairs):
        """
        Helper function for L{equal_values} -- return true iff self
        and other have equal values.

        @param visited_self: A set containing the ids of all C{self}
            values we've already visited.
        @param visited_other: A set containing the ids of all C{other}
            values we've already visited.
        @param visited_pairs: A set containing C{(selfid, otherid)}
            pairs for all pairs of values we've already visited.
        """
        # If we're the same object, then we're equal.
        if self is other: return True

        # If other's not a feature struct, we're definitely not equal.
        if not isinstance(other, FeatStruct): return False

        # If we have different types, we're not the same.
        if self._types != other._types:
            return False

        # If we define different features, we're definitely not equal.
        # (Perform len test first because it's faster -- we should
        # do profiling to see if this actually helps)
        if len(self) != len(other): return False
        if set(self) != set(other): return False

        # If we're not checking reentrance, then we still need to deal
        # with cycles.  If we encounter the same (self, other) pair a
        # second time, then we won't learn anything more by examining
        # their children a second time, so just return true.
        else:
            if (id(self), id(other)) in visited_pairs:
                return True

        # Keep track of which nodes we've visited.
        visited_self.add(id(self))
        visited_other.add(id(other))
        visited_pairs.add( (id(self), id(other)) )

        # Now we have to check all values.  If any of them don't match,
        # then return false.
        for (fname, self_fval) in self.items():
            other_fval = other[fname]
            if isinstance(self_fval, FeatStruct):
                if not self_fval._equal(other_fval,
                                        visited_self, visited_other,
                                        visited_pairs):
                    return False
            else:
                if self_fval != other_fval: return False

        # Everything matched up; return true.
        return True

    def __hash__(self):
        """
        If this feature structure is frozen, return its hash value;
        otherwise, raise C{TypeError}.
        """
        if not self._frozen:
            raise TypeError('FeatStructs must be frozen before they '
                            'can be hashed.')
        try: return self.__hash
        except AttributeError:
            self.__hash = self._hash(set())
            return self.__hash

    def _hash(self, visited):
        if id(self) in visited: return 1
        visited.add(id(self))

        hashval = 0
        for (fname, fval) in sorted(self.items()):
            hashval += hash(fname)
            if isinstance(fval, FeatStruct):
                hashval += fval._hash(visited)
            else:
                hashval += hash(fval)

        # Convert to a 32 bit int.
        return int(hashval & 0x7fffffff)

    ##////////////////////////////////////////////////////////////
    #{ Freezing
    ##////////////////////////////////////////////////////////////

    #: Error message used by mutating methods when called on a frozen
    #: feature structure.
    _FROZEN_ERROR = "Frozen FeatStructs may not be modified"

    def freeze(self):
        """
        Make this feature structure, and any feature structures it
        contains, immutable.  Note: this method does not attempt to
        'freeze' any feature values that are not C{FeatStruct}s; it
        is recommended that you use only immutable feature values.
        """
        if self._frozen: return
        self._freeze(set())

    def frozen(self):
        """
        @return: True if this feature structure is immutable.  Feature
        structures can be made immutable with the L{freeze()} method.
        Immutable feature structures may not be made mutable again,
        but new mutable copies can be produced with the L{copy()} method.
        """
        return self._frozen

    def _freeze(self, visited):
        if id(self) in visited: return
        visited.add(id(self))
        self._frozen = True
        for (fname, fval) in sorted(self.items()):
            if isinstance(fval, FeatStruct):
                fval._freeze(visited)

    def unfreeze(self):
        """Return an unfrozen copy of the FS if frozen; otherwise self."""
        if self.frozen():
            return self.copy()
        else:
            return self

    ##////////////////////////////////////////////////////////////
    #{ Copying
    ##////////////////////////////////////////////////////////////

    def copy(self, deep=True):
        """
        Return a new copy of C{self}.  The new copy will not be
        frozen.

        @param deep: If true, create a deep copy; if false, create
            a shallow copy.
        """
        if deep:
            return copy.deepcopy(self)
        else:
            return FeatStruct(self)

    def __deepcopy__(self, memo):
        memo[id(self)] = selfcopy = self.__class__()
        selfcopy._types = self._types
        for (key, val) in self.items():
            selfcopy[copy.deepcopy(key,memo)] = copy.deepcopy(val,memo)
        return selfcopy

    def part_copy(self, feats, simplify=None):
        """
        Return a new FeatStruct with values only for the top-level features in feats.
        simplify is None or a dict of value:string pairs, to be used in simplifying
        the resulting FS.
        """
        fs = FeatStruct()
        for f, v in self.items():
            if f in feats:
                if simplify and v in simplify:
                    fs[f] = simplify[v]
                else:
                    fs[f] = v
        return fs

    @staticmethod
    def make_simp_dict(dct):
        """
        Convert a dict of FS string->string representations to a
        dict of (frozen) FS->string representations.
        """
        d = {}
        for fsstr, string in dct.items():
            fs = FeatStruct(fsstr, freeze=True)
            d[fs] = string
        return d

    ##////////////////////////////////////////////////////////////
    #{ String Representations
    ##////////////////////////////////////////////////////////////

    def __repr__(self, shrt=False):
        """
        Display a single-line representation of this feature structure,
        suitable for embedding in other representations.  If shrt,
        don't display False or nil values.
        """
        return self._repr(shrt=shrt)

    def short_print(self):
        """Print out only True or non-nil values."""
        print(self.__repr__(True))

    def __str__(self):
        """
        Display a multi-line representation of this feature structure
        as an FVM (feature value matrix).
        """
        return '\n'.join(self._str())

    def _repr(self, shrt=False):
        """
        @return: A string representation of this feature structure.
        """
        segments = []
        #{ Added by MG
        types = [t._label for t in self._types]
        #}
        prefix = ''
        suffix = ''
        # True if any value is neither False nor nil
        anything = False

        items = self.items()
        # sorting note: keys are unique strings, so we'll never fall
        # through to comparing values.
        for (fname, fval) in sorted(items):
            anything0 = True
            display = getattr(fname, 'display', None)
            if (display == 'prefix' and not prefix and
                  isinstance(fval, (Variable, str))):
                    prefix = '%s' % fval
            elif display == 'slash' and not suffix:
                if isinstance(fval, Variable):
                    suffix = '?%s' % fval.name
                else:
                    suffix = '/%r' % fval
            elif isinstance(fval, Variable):
                segments.append('%s=%s' % (fname, fval.name))
            elif fval is True:
                segments.append('+%s' % fname)
            elif fval is False:
                anything0 = False
                if not shrt:
                    segments.append('-%s' % fname)
            elif isinstance(fval, Expression):
                segments.append('%s=<%s>' % (fname, fval))
            elif not isinstance(fval, FeatStruct):
                if fval == 'nil':
                    anything0 = False
                    if not shrt:
                        segments.append('%s=nil' % (fname,))
                elif isinstance(fval, str) and \
                any([char in fval for char in (',', ' ', "'", "-", "+")]):
                # quotes required around strings with special chars
                    segments.append('{}="{}"'.format(fname, fval))
                else:
                    segments.append("{}={}".format(fname, fval))
            else:
                fval_repr = fval._repr(shrt=shrt)
                if fval_repr:
                    segments.append('%s=%s' % (fname, fval_repr))
            if anything0:
                anything = True
        if anything or not shrt or prefix:
            #{ Added by MG
            if anything or not shrt:
                type_string = ' '.join(types)
                if len(types) > 1:
                    type_string = '{' + type_string + '}'
                if len(items) > 0 and types:
                    type_string += ' '
            #}
            return '%s[%s%s]%s' % (prefix, type_string, ','.join(segments), suffix)
        else:
            return ''

    def _str(self):
        """
        @return: A list of lines composing a string representation of
            this feature structure.
        """
        #{ Added by MG
        types = [t._label for t in self._types]
        if types:
            type_string = ' '.join(types)
            if len(types) > 1:
                type_string = '{' + type_string + '}'
        else:
            type_string = ''

        #}

        # Special case:
        if len(self) == 0:
            brack = '[]'
            if types:
                brack = '[' + type_string + ']'
            return [brack]

        # What's the longest feature name?  Use this to align names.
        maxfnamelen = max(len(str(k)) for k in self.keys())

        lines = []
        items = self.items()

        # sorting note: keys are unique strings, so we'll never fall
        # through to comparing values.
        for (fname, fval) in sorted(items):
            fname = str(fname)
            if isinstance(fval, Variable):
                lines.append('%s = %s' % (fname.ljust(maxfnamelen),
                                          fval.name))

            elif isinstance(fval, Expression):
                lines.append('%s = <%s>' % (fname.ljust(maxfnamelen), fval))

            elif not isinstance(fval, FeatStruct):
                # It's not a nested feature structure -- just print it.
                lines.append('%s = %r' % (fname.ljust(maxfnamelen), fval))

            else:
                # It's a new feature structure.  Separate it from
                # other values by a blank line.
                if lines and lines[-1] != '': lines.append('')

                # Recursively print the feature's value (fval).
                fval_lines = fval._str()

                # Indent each line to make room for fname.
                fval_lines = [(' '*(maxfnamelen+3))+l for l in fval_lines]

                # Pick which line we'll display fname on.
                nameline = (len(fval_lines)-1)//2

                fval_lines[nameline] = (
                        fname.ljust(maxfnamelen)+' ='+
                        fval_lines[nameline][maxfnamelen+2:])

                # Add the feature structure to the output.
                lines += fval_lines

                # Separate FeatStructs by a blank line.
                lines.append('')

        # Get rid of any excess blank lines.
        if lines[-1] == '': lines = lines[:-1]

        # Add brackets around everything.
        maxlen = max(len(line) for line in lines)
        lines = ['[ %s%s ]' % (line, ' '*(maxlen-len(line))) for line in lines]

        # If there are types, make them the first line
        #{ Added by MG
        if types:
            lines = [type_string] + lines
        #}

        return lines

    def string_list(self, lng=True):
        """Return a list of abbreviated strings for the feature structure."""
        strings = []
        if lng:
            for feat, value in self.items():
                s = ''
                if isinstance(value, FeatStruct):
                    value = value.string_list(False)
                    s = feat + ':' + '|'.join(value)
                elif isinstance(value, bool):
                    if value:
                        s = feat
                strings.append(s)
        else:
            s = self.__repr__()
            s = s.replace("'", "").replace(" ", '').replace("[", "").replace("]", "")
            s_list = s.split(',')
            s_pos = []
            for f in s_list:
                if f[0] == '-':
                    # False, omit
                    pass
                elif f[0] == '+':
                    # True, drop the '+'
                    s_pos.append(f[1:])
            if s_pos:
                s = ','.join(s_pos)
            else:
                s = '_'
            strings.append(s)
        return strings

######################################################################
# Specialized Features
######################################################################

class Feature:
    """
    A feature identifier that's specialized to put additional
    constraints, default values, etc.
    """
    def __init__(self, name, default=None, display=None):
        assert display in (None, 'prefix', 'slash')

        self._name = name # [xx] rename to .identifier?
        """The name of this feature."""

        self._default = default # [xx] not implemented yet.
        """Default value for this feature.  Use None for unbound."""

        self._display = display
        """Custom display location: can be prefix, or slash."""

        if self._display == 'prefix':
            self._sortkey = (-1, self._name)
        elif self._display == 'slash':
            self._sortkey = (1, self._name)
        else:
            self._sortkey = (0, self._name)

    name = property(lambda self: self._name)
    default = property(lambda self: self._default)
    display = property(lambda self: self._display)

    def __repr__(self):
        return '*%s*' % self.name

    def __hash__(self):
        return hash(self._name)

    #////////////////////////////////////////////////////////////
    # These can be overridden by subclasses:
    #////////////////////////////////////////////////////////////

    def parse_value(self, s, position, reentrances, parser):
        return parser.parse_value(s, position, reentrances)

    def unify_base_values(self, fval1, fval2, bindings):
        """
        If possible, return a single value..  If not, return
        the value L{UnificationFailure}.
        """
        if fval1 == fval2: return fval1
        else: return None
        #UnificationFailure

# Add ourselves to the list of permissible types for feature names.
FeatStruct._feature_name_types += (Feature,)


class SlashFeature(Feature):
    def parse_value(self, s, position, reentrances, parser):
        return parser.partial_parse(s, position, reentrances)

##class RangeFeature(Feature):
##    RANGE_RE = re.compile('(-?\d+):(-?\d+)')
##    def parse_value(self, s, position, reentrances, parser):
##        m = self.RANGE_RE.match(s, position)
##        if not m: raise ValueError('range', position)
##        return (int(m.group(1)), int(m.group(2))), m.end()
##
##    def unify_base_values(self, fval1, fval2, bindings):
##        if fval1 is None: return fval2
##        if fval2 is None: return fval1
##        rng = max(fval1[0], fval2[0]), min(fval1[1], fval2[1])
##        if rng[1] < rng[0]: return UnificationFailure
##        return rng

SLASH = SlashFeature('slash', default=False, display='slash')
TYPE = Feature('type', display='prefix')

######################################################################
# Feature Structure Parser
######################################################################

class FeatStructParser:
    def __init__(self, features=(SLASH, TYPE), cls=FeatStruct, fsh=None):
        self._features = dict((f.name,f) for f in features)
        self._class = cls
        self._prefix_feature = None
        self._slash_feature = None
        self._fsh = fsh
        for feature in features:
            if feature.display == 'slash':
                if self._slash_feature:
                    raise ValueError('Multiple features w/ display=slash')
                self._slash_feature = feature
            if feature.display == 'prefix':
                if self._prefix_feature:
                    raise ValueError('Multiple features w/ display=prefix')
                self._prefix_feature = feature
        self._features_with_defaults = [feature for feature in features
                                        if feature.default is not None]

    def parse(self, s, fstruct=None):
        """
        Convert a string representation of a feature structure (as
        displayed by repr) into a C{FeatStruct}.  This parse
        imposes the following restrictions on the string
        representation:
          - Feature names cannot contain any of the following:
            whitespace, parentheses, quote marks, equals signs,
            dashes, commas, and square brackets.  Feature names may
            not begin with plus signs or minus signs.
          - Only the following basic feature value are supported:
            strings, integers, variables, C{None}, and unquoted
            alphanumeric strings.
          - For reentrant values, the first mention must specify
            a reentrance identifier and a value; and any subsequent
            mentions must use arrows (C{'->'}) to reference the
            reentrance identifier.
        """
        s = s.strip()
        value, position = self.partial_parse(s, 0, {}, fstruct)
        if position != len(s):
            self._error(s, 'end of string', position)
        return value

    _START_FSTRUCT_RE = re.compile(r'\s*(?:\((\d+)\)\s*)?(\??[\w-]+)?(\[)')
    _END_FSTRUCT_RE = re.compile(r'\s*]\s*')
    _SLASH_RE = re.compile(r'/')
    _FEATURE_NAME_RE = re.compile(r'\s*([+-]?)([^\s\(\)"\'\-=\[\],]+)\s*')
    _REENTRANCE_RE = re.compile(r'\s*->\s*')
    _TARGET_RE = re.compile(r'\s*\((\d+)\)\s*')
    _ASSIGN_RE = re.compile(r'\s*=\s*')
    _COMMA_RE = re.compile(r'\s*,\s*')
    _BARE_PREFIX_RE = re.compile(r'\s*(?:\((\d+)\)\s*)?(\??[\w-]+\s*)()')
    #{ Added by MG
    # One type: %type
    _TYPE_RE = re.compile(r'\s*(%\w+)\s*')
    # Multiple types: {type1 type2...}
    _TYPES_RE = re.compile(r'\s*\{([%\w\s]+)\}\s*')
    #}

    def partial_parse(self, s, position=0, reentrances=None, fstruct=None):
        """
        Helper function that parses a feature structure.
        @param s: The string to parse.
        @param position: The position in the string to start parsing.
        @param reentrances: A dictionary from reentrance ids to values.
            Defaults to an empty dictionary.
        @return: A tuple (val, pos) of the feature structure created
            by parsing and the position where the parsed feature
            structure ends.
        """
        if reentrances is None: reentrances = {}
        try:
            return self._partial_parse(s, position, reentrances, fstruct)
        except ValueError as e:
            if len(e.args) != 2: raise
            self._error(s, *e.args)

    def _partial_parse(self, s, position, reentrances, fstruct=None):
        # Create the new feature structure
        if fstruct is None:
            fstruct = self._class()
        else:
            fstruct.clear()

        # Read up to the open bracket.
        match = self._START_FSTRUCT_RE.match(s, position)
        if not match:
            match = self._BARE_PREFIX_RE.match(s, position)
            if not match:
                raise ValueError('open bracket or identifier', position)
        position = match.end()

        # If there as an identifier, record it.
        if match.group(1):
            identifier = match.group(1)
            if identifier in reentrances:
                raise ValueError('new identifier', match.start(1))
            reentrances[identifier] = fstruct

        # If there was a prefix feature, record it.
        if match.group(2):
            if self._prefix_feature is None:
                raise ValueError('open bracket or identifier', match.start(2))
            prefixval = match.group(2).strip()
            if prefixval.startswith('?'):
                prefixval = Variable(prefixval)
            fstruct[self._prefix_feature] = prefixval

        # If group 3 is emtpy, then we just have a bare prefix, so
        # we're done.
        if not match.group(3):
            return self._finalize(s, match.end(), reentrances, fstruct)

        # There is a [; check first for types
        # Multiple types
        match = self._TYPES_RE.match(s, position)
        if match:
            # Get the type from the hierarchy and add it to self._types
            tps = [self._fsh.get(tp.strip()) for tp in match.group(1).split()]
            for tp in tps:
                fstruct.add_type(tp)
            position = match.end()
        else:
            # Single type
            match = self._TYPE_RE.match(s, position)
            if match:
                tp = self._fsh.get(match.group(1))
                # Get the type from the hierarchy and add it to self._types
                fstruct.add_type(self._fsh.get(match.group(1)))
                position = match.end()

        # Build a list of the features defined by the structure.
        # Each feature has one of the three following forms:
        #     name = value
        #     name -> (target)
        #     +name
        #     -name
        while position < len(s):
            # Use these variables to hold info about each feature:
            name = target = value = None

            # Check for the close bracket.
            match = self._END_FSTRUCT_RE.match(s, position)
            if match is not None:
                return self._finalize(s, match.end(), reentrances, fstruct)

            # Get the feature name's name
            match = self._FEATURE_NAME_RE.match(s, position)
            if match is None: raise ValueError('feature name', position)
            name = match.group(2)
            position = match.end()

            # Check if it's a special feature.
            if name[0] == '*' and name[-1] == '*':
                name = self._features.get(name[1:-1])
                if name is None:
                    raise ValueError('known special feature', match.start(2))

            # Check if this feature has a value already.
            if name in fstruct:
                raise ValueError('new name', match.start(2))

            # Boolean value ("+name" or "-name")
            if match.group(1) == '+': value = True
            if match.group(1) == '-': value = False

            # Reentrance link ("-> (target)")
            if value is None:
                match = self._REENTRANCE_RE.match(s, position)
                if match is not None:
                    position = match.end()
                    match = self._TARGET_RE.match(s, position)
                    if not match:
                        raise ValueError('identifier', position)
                    target = match.group(1)
                    if target not in reentrances:
                        raise ValueError('bound identifier', position)
                    position = match.end()
                    value = reentrances[target]

            # Assignment ("= value").
            if value is None:
                match = self._ASSIGN_RE.match(s, position)
                if match:
                    position = match.end()
                    value, position = (self._parse_value(name, s, position, reentrances))
                # None of the above: error.
                else:
                    raise ValueError('equals sign', s, position)

            # Store the value.
            fstruct[name] = value

            # If there's a close bracket, handle it at the top of the loop.
            if self._END_FSTRUCT_RE.match(s, position):
                continue

            # Otherwise, there should be a comma
            match = self._COMMA_RE.match(s, position)
            if match is None: raise ValueError('comma', position)
            position = match.end()

        # We never saw a close bracket.
        raise ValueError('close bracket', position)

    def _finalize(self, s, pos, reentrances, fstruct):
        """
        Called when we see the close brace -- checks for a slash feature,
        and adds in default values.
        """
        # Add the slash feature (if any)
        match = self._SLASH_RE.match(s, pos)
        if match:
            name = self._slash_feature
            v, pos = self._parse_value(name, s, match.end(), reentrances)
            fstruct[name] = v
        ## Add any default features.  -- handle in unfication instead?
        #for feature in self._features_with_defaults:
        #    fstruct.setdefault(feature, feature.default)
        # Return the value.
        return fstruct, pos

    def _parse_value(self, name, s, position, reentrances):
        if isinstance(name, Feature):
            return name.parse_value(s, position, reentrances, self)
        else:
            return self.parse_value(s, position, reentrances)

    def parse_value(self, s, position, reentrances):
        for (handler, regexp) in self.VALUE_HANDLERS:
            match = regexp.match(s, position)
            if match:
                handler_func = getattr(self, handler)
                return handler_func(s, position, reentrances, match)
        raise ValueError('value', position)

    def _error(self, s, expected, position):
        estr = ('Error parsing feature structure\n    ' +
                s + '\n    ' + ' '*position + '^ ' +
                'Expected %s' % expected)
        raise ValueError(estr)

    #////////////////////////////////////////////////////////////
    #{ Value Parsers
    #////////////////////////////////////////////////////////////

    #: A table indicating how feature values should be parsed.  Each
    #: entry in the table is a pair (handler, regexp).  The first entry
    #: with a matching regexp will have its handler called.  Handlers
    #: should have the following signature:
    #:
    #:    def handler(s, position, reentrances, match): ...
    #:
    #: and should return a tuple (value, position), where position is
    #: the string position where the value ended.  (n.b.: order is
    #: important here!)
    VALUE_HANDLERS = [
        ('parse_fstruct_value', _START_FSTRUCT_RE),
        ('parse_var_value', re.compile(r'\?[a-zA-Z_][a-zA-Z0-9_]*')),
        ('parse_str_value', re.compile("[uU]?[rR]?(['\"])")),
        ('parse_int_value', re.compile(r'-?\d+')),
        ('parse_sym_value', re.compile(r'\w\w*', re.U)),  # (r'[a-zA-Z_][a-zA-Z0-9_]*', re.U)),
        ('parse_app_value', re.compile(r'<(app)\((\?[a-z][a-z]*)\s*,'
                                       r'\s*(\?[a-z][a-z]*)\)>')),
        ('parse_logic_value', re.compile(r'<([^>]*)>')),
        ('parse_set_value', re.compile(r'{')),
        ('parse_tuple_value', re.compile(r'\(')),
        ]

    def parse_fstruct_value(self, s, position, reentrances, match):
        return self.partial_parse(s, position, reentrances)

    def parse_str_value(self, s, position, reentrances, match):
        return internals.parse_str(s, position)

    def parse_int_value(self, s, position, reentrances, match):
        return int(match.group()), match.end()

    # Note: the '?' is included in the variable name.
    def parse_var_value(self, s, position, reentrances, match):
        return Variable(match.group()), match.end()

    _SYM_CONSTS = {'None':None, 'True':True, 'False':False}
    def parse_sym_value(self, s, position, reentrances, match):
        val, end = match.group(), match.end()
        return self._SYM_CONSTS.get(val, val), end

    def parse_app_value(self, s, position, reentrances, match):
        """Mainly included for backwards compat."""
        return LogicParser().parse('(%s %s)' % match.group(2,3)), match.end()

    def parse_logic_value(self, s, position, reentrances, match):
        parser = LogicParser()
        try:
            expr = parser.parse(match.group(1))
            if parser.buffer: raise ValueError()
            return expr, match.end()
        except ValueError:
            raise ValueError('logic expression', match.start(1))

    def parse_tuple_value(self, s, position, reentrances, match):
        return self._parse_seq_value(s, position, reentrances, match, ')',
                                     FeatureValueTuple, FeatureValueConcat)

    def parse_set_value(self, s, position, reentrances, match):
        return self._parse_seq_value(s, position, reentrances, match, '}',
                                     FeatureValueSet, FeatureValueUnion)

    def _parse_seq_value(self, s, position, reentrances, match,
                         close_paren, seq_class, plus_class):
        """
        Helper function used by parse_tuple_value and parse_set_value.
        """
        cp = re.escape(close_paren)
        position = match.end()
        # Special syntax for empty tuples:
        m = re.compile(r'\s*/?\s*%s' % cp).match(s, position)
        if m: return seq_class(), m.end()
        # Read values:
        values = []
        seen_plus = False
        while True:
            # Close paren: return value.
            m = re.compile(r'\s*%s' % cp).match(s, position)
            if m:
                if seen_plus: return plus_class(values), m.end()
                else: return seq_class(values), m.end()

            # Read the next value.
            val, position = self.parse_value(s, position, reentrances)
            values.append(val)

            # Comma or looking at close paren
            m = re.compile(r'\s*(,|\+|(?=%s))' % cp).match(s, position)
            if m.group(1) == '+': seen_plus = True
            if not m: raise ValueError("',' or '+' or '%s'" % cp, position)
            position = m.end()

######################################################################
# FeatureValueSet & FeatureValueTuple
######################################################################

class SubstituteBindingsSequence(SubstituteBindingsI):
    """
    A mixin class for sequence classes that distributes variables() and
    substitute_bindings() over the object's elements.
    """
    def variables(self):
        return ([elt for elt in self if isinstance(elt, Variable)] +
                sum([elt.variables() for elt in self
                     if isinstance(elt, SubstituteBindingsI)], []))

    def substitute_bindings(self, bindings):
        return self.__class__([self.subst(v, bindings) for v in self])

    def subst(self, v, bindings):
        if isinstance(v, SubstituteBindingsI):
            return v.substitute_bindings(bindings)
        else:
            return bindings.get(v, v)

class FeatureValueTuple(SubstituteBindingsSequence, tuple):
    """
    A base feature value that is a tuple of other base feature values.
    FeatureValueTuple implements L{SubstituteBindingsI}, so any
    variable substitutions will be propagated to the elements
    contained by the set.  C{FeatureValueTuple}s are immutable.
    """
    def __repr__(self): # [xx] really use %s here?
        if len(self) == 0: return '()'
        return '(%s)' % ', '.join('%s' % (b,) for b in self)

class FeatureValueSet(SubstituteBindingsSequence, frozenset):
    """
    A base feature value that is a set of other base feature values.
    FeatureValueSet implements L{SubstituteBindingsI}, so it any
    variable substitutions will be propagated to the elements
    contained by the set.  C{FeatureValueSet}s are immutable.
    """
    def __repr__(self): # [xx] really use %s here?
        if len(self) == 0: return '{/}' # distinguish from dict.
        # n.b., we sort the string reprs of our elements, to ensure
        # that our own repr is deterministic.
        return '{%s}' % ', '.join(sorted('%s' % (b,) for b in self))
    __str__ = __repr__

class FeatureValueUnion(SubstituteBindingsSequence, frozenset):
    """
    A base feature value that represents the union of two or more
    L{FeatureValueSet}s or L{Variable}s.
    """
    def __new__(cls, values):
        # If values contains FeatureValueUnions, then collapse them.
        values = _flatten(values, FeatureValueUnion)

        # If the resulting list contains no variables, then
        # use a simple FeatureValueSet instead.
        if sum(isinstance(v, Variable) for v in values) == 0:
            values = _flatten(values, FeatureValueSet)
            return FeatureValueSet(values)

        # If we contain a single variable, return that variable.
        if len(values) == 1:
            return list(values)[0]

        # Otherwise, build the FeatureValueUnion.
        return frozenset.__new__(cls, values)

    def __repr__(self):
        # n.b., we sort the string reprs of our elements, to ensure
        # that our own repr is deterministic.  also, note that len(self)
        # is guaranteed to be 2 or more.
        return '{%s}' % '+'.join(sorted('%s' % (b,) for b in self))

class FeatureValueConcat(SubstituteBindingsSequence, tuple):
    """
    A base feature value that represents the concatenation of two or
    more L{FeatureValueTuple}s or L{Variable}s.
    """
    def __new__(cls, values):
        # If values contains FeatureValueConcats, then collapse them.
        values = _flatten(values, FeatureValueConcat)

        # If the resulting list contains no variables, then
        # use a simple FeatureValueTuple instead.
        if sum(isinstance(v, Variable) for v in values) == 0:
            values = _flatten(values, FeatureValueTuple)
            return FeatureValueTuple(values)

        # If we contain a single variable, return that variable.
        if len(values) == 1:
            return list(values)[0]

        # Otherwise, build the FeatureValueConcat.
        return tuple.__new__(cls, values)

    def __repr__(self):
        # n.b.: len(self) is guaranteed to be 2 or more.
        return '(%s)' % '+'.join('%s' % (b,) for b in self)

######################################################################
#{ Simple unification (no variables)
######################################################################

def simple_unify(x, y):
    """Unify the expressions x and y, returning the result or 'fail'."""
    # If either expression doesn't exist, return the other, unless this is the top-level
    # If they're the same, return one.
#    print("simple unify {} ({}), {} ({})".format(x.__repr__(), type(x), y.__repr__(), type(y)))
    if x == y:
        return x
    # If both are dicts, call unify_dict
    elif isinstance(x, FeatStruct) and isinstance(y, FeatStruct):
        return unify_dicts(x, y)
    # Otherwise fail
    else:
        return 'fail'

def unify_dicts(x, y):
    '''Try to unify two dicts in the context of bindings, returning the merged result.'''
    # Make an empty dict of the type of x
#    print('Unifying dicts {} {}'.format(x.__repr__(), y.__repr__()))
    result = FeatStruct()
    for k in set(x.keys()) | set(y.keys()):
        # Check all of the keys of x and y
        x_val, y_val = x.get(k, 'nil'), y.get(k, 'nil')
        if x_val != 'nil':
            if y_val != 'nil':
                # If x and y both have a value for k, try to unify the values
                u = simple_unify(x_val, y_val)
                if u == 'fail':
#                    print('Failed')
                    return 'fail'
                else:
                    result[k] = u
            else:
                # If x has a value for k but y doesn't, use x's value
                result[k] = x_val
        elif y_val != 'nil':
            # If y has a value for k but x doesn't, use y's value
            result[k] = y_val

    return result
