"""
This file is part of HornMorpho, which is part of the PLoGS project.

    <http://homes.soic.indiana.edu/gasser/plogs.html>

    Copyleft 2007-2023.
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
--------------------------------------------------------------------

Rudimentary implementation of semirings for use in weighted FSTs.
Includes feature structures sets, as in Amtrup (2003).
Feature structures based on those in NLTK <http://www.nltk.org/>.

Author: Michael Gasser <gasser@indiana.edu>

2009-06-11: unification modified to accommodate 'fail' result
2011-06-04:
  Parsing of disjunctions in string FS representations:
  +-feat
  feat=val1|val2
2013-02-23:
  Sets of FeatStructs get cast properly to FSSets.
2017.05.10
  Add method for getting a feature value within a FSSet.
  Override union for FSSet so it returns an FSSet.
"""

from .fs import *
from .utils import *
# import re

######################################################################
# FeatStruct Sets
######################################################################

## Regular expressions needed for splitting strings into feature-value
## pairs

# either
# {+,-,+-} value
# or
# feat = value
SIMP_FVAL_RE = re.compile(r'([+-]{1,2}\w+?|\w+?\s*=\s*[^\]]+?)(?:,|\]|$)')

# feat = [...]
COMP_FVAL_RE = re.compile(r'(\w+?\s*=\s*\[.+?\])')

class FSSet(set, FS):
    """Sets of feature structures."""

    def __init__(self, *items):
        '''
        Create a feature structure set from items, normally a list of
        feature structures or strings.
        By default it's frozen.
        '''
        # This may still be needed for unpickling, when items is a tuple of a list of FeatStructs
        if len(items) > 0 and isinstance(items[0], (list, set)):
            items = items[0]
        if not isinstance(items, set):
            items = [(FeatStructParser().parse(i) if isinstance(i, str) else i) for i in items]
            # Freeze each feature structure
            for index, itm in enumerate(items):
                if isinstance(itm, FeatStruct):
                    itm.freeze()
                else:
                    # Umm...how is it possible for itm not to be a feature structure?
                    items[index] = tuple(itm)
        set.__init__(self, items)

    def __repr__(self):
        string = ''
        for i, fs in enumerate(self):
            string += fs.__repr__()
            if i < len(self) - 1:
                string += ';'
        return string

    def union(self, fsset):
        """Override set union method by casting result to FSSet."""
        res = set.union(self, fsset)
        return FSSet(res)

    def copy(self):
        """Return a copy of the FSSet."""
        fss = set()
        for fs in self:
#            if not fs.frozen():
#                fs = fs.freeze()
            fss.add(fs.copy())
        return FSSet(fss)

    def remove(self, FS):
        """
        Remove the FS from all FSs in the set, returning the new FSSet
        (as a list!).
        """
        fsset = self.unfreeze()
        to_remove = []
        for fs in fsset:
            for key in list(FS.keys()):
                # Assume there's only one level
                fs.pop(key)
            if not fs:
                # Nothing left in it; remove it
                to_remove.append(fs)
        for fs in to_remove:
            fsset.remove(fs)
        return fsset

    def delete(self, features, freeze=False):
        fslist = self.unfreeze()
        for index, fs in enumerate(fslist):
            fslist[index] = fs.delete(features)
        return FSSet(fslist)

    def u(self, f, strict=False, verbose=False):
        """Unify this FSSet with either another FSSet or a FeatStruct."""
        if isinstance(f, FSSet):
            return self.unify(f, verbose=verbose)
        else:
            return self.unify_FS(f, strict=strict, verbose=verbose)

    def unify(self, fs2, verbose=False):
        fs2_list = list(fs2)
        fs1_list = list(self)
        if verbose:
            print('FSS1: {}, FSS2: {}'.format(fs1_list, fs2_list))
        result1 = [simple_unify(f1, f2) for f1 in fs1_list for f2 in fs2_list]
        if verbose:
            print('Result1', result1)
        if every(lambda x: x == TOP, result1):
            # If everything unifies to TOP, return one of them
            return TOPFSS
        else:
            # Get rid of all instances of TOP and unification failures
            return FSSet(*filter(lambda x: x != 'fail', result1))

    def unify_FS(self, fs, strict=False, verbose=False):
        """Attempt to unify this FSSet with a simple FeatStruct instance, basically filter
        the FeatStructs in the set by their unification with fs. Pretty much like FSSet.unify()."""
        # This is a list of the unifications of the elements of self with fs
        result1 = [simple_unify(f1, fs, strict=strict, verbose=verbose) for f1 in list(self)]
        if every(lambda x: x == TOP, result1):
            return TOPFSS
        else:
            # All FeatStructs in self that unify with fs
            result2 = list(filter(lambda x: x != 'fail', result1))
            if verbose:
                print("unify_FS: unifying {} with {}, result {}".format(self, fs.__repr__(), result2))
            if not result2:
                # None of the FeatStructs in self unifies with fs
                return 'fail'
            return FSSet(*result2)

    def get(self, feature, default=None):
        """Get the value of the feature in the first FeatStruct that has one."""
        for fs in self:
            value = fs.get(feature)
            if value != None:
                return value
        return default

    def get_all(self, feature, default=None):
        """
        Get the value of the feature in all FeatStructs that have one.
        """
        values = []
        for fs in self:
            value = fs.get(feature)
            if value != None:
                values.append(value)
        return values or default

    # def get_all_mult(self, features, default=None):
    #     values = []
    #     for fs in self:
    #         values1 = []
    #         for feature in features:
    #             value = fs.get(feature)
    #             if value != None:
    #                 values1.append(value)
    #         if values1:
    #             values.append(values1)
    #     return values or default

    def set_all(self, feat, value, force=True, verbose=False):
        """
        Return a new FSSet with feat set to value in all component FeatStructs.
        If force is True, do this even it conflicts with the features in self.
        """
        if force:
            fss = self.unfreeze()
            for f in fss:
                if verbose:
                    print("  ** set_all forceably setting {} {} to {}".format(f.__repr__(), feat, value))
                f[feat] = value
            return FSSet(fss)
        u = self.unify_FS(FeatStruct("[{}={}]".format(feat, value)))
        if u != 'fail':
            u = u.unfreeze()
            for f in u:
                if verbose:
                    print("  ** set_all setting {} {} to {}".format(f.__repr__(), feat, value))
                f[feat] = value
            if verbose:
                print(" ** set_all {}".format(u.__repr__()))
            return u
        return None

    def inherit(self):
        """Inherit feature values for all members of set, returning new set."""
        items = [item.inherit() for item in self]
        return FSSet(*items)

    @staticmethod
    def parse(string):
        """string could be a single FS or several separated by ';'."""
#        print("Parsing {}".format(string))
        if string == '[]':
            return TOPFSS
        strings = [s.strip() for s in string.split(';')]
        strings = reduce_lists([FSSet.proc_fv(s) for s in strings])
        return FSSet(*strings)

    @staticmethod
    def proc_fv(fv):
        '''Process a string representing feature-value pairs, returning
        a list of strings, one for each combination of alternatives
        specified by | or +-.
        '''
        fv_split = FSSet.split_rep(fv)
        if not fv_split:
            return fv
        res = FSSet.split_fval(fv_split[0])
        if len(fv_split) > 1:
            for fv in fv_split[1:]:
#                print('res', res, 'fv', fv)
                res = FSSet.incorp_fval(res, fv)
        return ['[' + r + ']' for r in res]

    @staticmethod
    def split_rep(rep):
        '''Split a featstruc string representation into top-level feat-value
        pairs, assuming at most one level of nesting.'''
        rep0 = rep[1:-1]
        pos = 0
        res = []
        while pos < len(rep0):
            char = rep0[pos]
            if char in ', ':
                pos += 1
            else:
                comp = COMP_FVAL_RE.match(rep0[pos:])
                if comp:
                    fv = comp.group(1)
                    res.append(fv)
                    pos = pos + comp.end()
                else:
                    simp = SIMP_FVAL_RE.match(rep0[pos:])
                    if simp:
                        fv = simp.group(1)
                        res.append(fv)
                        pos = pos + simp.end()
                    else:
                        print('Something wrong at position', pos, char, 'in', rep)
                        break
        return res

    @staticmethod
    def split_fval(fval):
        '''Process a feature-value string returning alternatives if
        it contains | or +-.
        '''
        if '|' not in fval and '+-' not in fval:
            return [fval]
        elif '[' in fval or '=' in fval:
            fv0 = fval.partition('=')
            feat = fv0[0]
            values = fv0[2]
            if '[' in values:
                return [feat + '=' + x for x in FSSet.proc_fv(values)]
            else:
                # |
                return [feat + '=' + v for v in values.split('|')]
        else:
            # +-
            fv0 = fval.partition('+-')
            feat = fv0[-1]
            return ['+' + feat, '-' + feat]

    @staticmethod
    def incorp_fval(strings, fval):
        splitv = FSSet.split_fval(fval)
        return [s + ',' + x for s in strings for x in splitv]

    @staticmethod
    def cast(obj):
        """Cast object to a FSSet."""
        if isinstance(obj, FSSet):
            return obj
        elif isinstance(obj, FeatStruct):
            return FSSet(obj)
        elif isinstance(obj, (str, str)):
            return FSSet.parse(obj)
        else:
            return TOPFSS

    def upd(self, features=None):
        """
        Return an updated FSSet agreeing with features in features.
        """
        return FSSet.update(self, features)

    @staticmethod
    def update(fsset, feats):
        """Return a new fsset with feats updated to match each fs in fsset."""
        fslist = []
        for fs in fsset:
            if isinstance(feats, FSSet):
                fslist1 = []
                for fs1 in feats:
                    fs1_copy = fs1.copy()
                    fs1_copy.update(fs)
                    fslist1.append(fs1_copy)
                fslist.extend(fslist1)
            else:
                fs_copy = feats.copy()
                fs_copy.update(fs)
                fslist.append(fs_copy)
        return FSSet(*fslist)

#    def updateFS(self, FS, verbose=0):
#        """Update FSS with features in FS."""
#        l = list(self)
#        u = [simple_unify(f, FS) for f in l]
#        return FSSet(*filter(lambda x: x!='fail', u))

    def featconv(self, subFSs, verbose=False):
        '''
        Convert a list of old subFS - new subFS pairs in self.
        If replace is True, get rid of the features in the old subFSs
        that are not also in the new subFSs.
        '''
        fslist = self.unfreeze()
        result = []
        for fs in fslist:
            fs = fs.featconv(subFSs, replace=True, unfreeze=False,
                             refreeze=True, skipcheck=True,
                             verbose=verbose)
            result.append(fs)
        return FSSet(result)

    @staticmethod
    def setfeats(fsset, condition, feature, value):
        """
        A new FSSet with feature set to value if condition is satisfied.
        """
        fslist = []
        for fs in fsset:
            if not condition or unify(fs, condition):
                # Copy because it's frozen
                fs_copy = fs.copy()
                fs_copy.setdefault(feature, value)
                fslist.append(fs_copy)
            else:
                fslist.append(fs)
        return FSSet(*fslist)

    def unfreeze(self):
        """A copy of the FSSet (as a list!) that is a set of unfrozen FSs."""
        return [fs.copy() for fs in self]

    @staticmethod
    def compareFSS(fss_list):
        """Compare feature values in a list of FSSs, first reducing each to a single FS with all shared values."""
        fs_list = [FSSet.FSS2FS(fss) for fss in fss_list]
        shared, diff = FSSet.compare(fs_list)
        return diff

    def FSS2FS(fss):
        """Convert the FSSet to a FeatStruct that includes the features shared across the set of FeatStructs
        in the FSSet."""
        fs = FeatStruct()
        fsslist = list(fss)
        fs0 = fsslist[0]
        fss_rest = fsslist[1:]
        for f1 in fs0.keys():
            fs01 = fs0.get(f1)
            shared = True
            for fs2 in fss_rest:
                if f1 not in fs2:
                    shared = False
                    break
                fs21 = fs2.get(f1)
                if fs01 != fs21:
                    shared = False
                    break
            if shared:
                # Each FS has a value and they're all equal, so add this to
                # the shared values
                fs[f1] = fs01
        return fs

    @staticmethod
    def compare(fss):
        """Compare feature values in the FS set, returning a pair of dicts: shared values, different values."""
        if len(fss) == 1:
            return list(fss)[0], {}
        feats = set()
        shared = {}
        diffs = {}
        for fs in fss:
            feats.update(list(fs.keys()))
        for f in feats:
            # values of features f in all FSs
            values = [fs.get(f, None) for fs in fss]
            v0 = values[0]
            same = True
            index = 1
            while same and index < len(values):
                v = values[index]
                if v != v0:
                    same = False
                index += 1
            if same:
                shared[f] = v0
            else:
                diffs[f] = values
        return shared, diffs

    def agree(self, target, agrs, force=False):
        """
        Similar to FeatStruct.agree(). Change values of agrs features in
        target to agree with some member(s) of FSSet.
        Ignore features that don't agree (rather than failing) unless
        force is True.
        """
        agr_pairs = agrs.items() if isinstance(agrs, dict) else agrs
        for fs in list(self):
            vals = []
            for src_feat, targ_feat in agr_pairs:
                if src_feat in fs:
                    src_value = fs[src_feat]
                    if targ_feat not in target:
                        vals.append((targ_feat, src_value))
                    else:
                        targ_value = target[targ_feat]
                        u = simple_unify(src_value, targ_value)
                        if u == 'fail':
                            if force:
                                vals.append((targ_feat, src_value))
                            else:
                                # Ignore this feature
                                continue
                        else:
                            vals.append((targ_feat, u))
#            print(" AGREE: vals {}".format(vals))
#            print(" AGREE: target {}, type {}".format(target.__repr__(), type(target)))
            for f, v in vals:
                if isinstance(target, FeatStruct):
                    target[f] = v
                else:
                    # target is an FSSet
                    new_target = set()
                    for i, fs in enumerate(target):
#                        print("  AGREE: target FS {}".format(fs.__repr__()))
#                        print("         f {} v {}".format(f, v))
                        if f in fs and not force:
                            new_target.add(fs)
                            continue
                        fs = fs.unfreeze()
                        fs[f] = v
                        fs.freeze()
                        new_target.add(fs)
#                    print(" added {}".format(v))
                    target = FSSet(new_target)
#                    print(" AGREE: new target {}".format(target.__repr__()))
        return target

## Feature structure that unifies with anything.
TOP = FeatStruct('[]')
TOP.freeze()
TOPFSS = FSSet(TOP)

class Semiring:

    def __init__(self, addition = None, multiplication = None,
                 in_set = None, zero = None, one = None):
        self.addition = addition
        self.multiplication = multiplication
        self.zero = zero
        self.one = one
        self.in_set = in_set

    def multiply(self, x, y):
        return self.multiplication(x, y)

    def add(self, x, y):
        return self.addition(x, y)

    def is_in_set(self, x):
        return self.in_set(x)

    def parse_weight(self, s):
        """Parse a string into a weight."""
        if not s:
            # Default weight for this SR
            return self.one
        elif self.in_set == uni_inset:
            # UNIFICATION_SR (which may have been instantiated multiple times
            # on different runs of the program)
            return FSSet.parse(s)
        else:
            # Number
            return float(s)

### Three semirings

PROBABILITY_SR = Semiring(addition = lambda x, y: x + y,
                          multiplication = lambda x, y: x * y,
                          in_set = lambda x: isinstance(x, float) and x >= 0.0,
                          zero = 0.0,
                          one = 1.0)

TROPICAL_SR = Semiring(addition = lambda x, y: min([x, y]),
                       multiplication = lambda x, y: x + y,
                       in_set = lambda x: isinstance(x, float),
                       zero = None,  # really +infinity
                       one = 0.0)

### Operations for Unification semiring
def uni_add(x, y):
    return x.union(y)

def uni_mult(x, y):
    return x.unify(y)

def uni_inset(x):
    return isinstance(x, FSSet)

UNIFICATION_SR = Semiring(addition = uni_add,
                          multiplication = uni_mult,
                          in_set = uni_inset,
                          zero = set(),
                          one = TOPFSS)
