"""
This file is part of HornMorpho.

    <http://homes.soic.indiana.edu/gasser/plogs.html>

    Copyleft 2018, 2019, 2020, 2021, 2022, 2023
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
    along with morfo.  If not, see <http://www.gnu.org/licenses/>.
-------------------------------------------------------

WEIGHTED FINITE STATE TRANSDUCERS

Finite state transducers with weights and cascades of FSTs that can
share some properties, including string class abbreviations, and
that can be conveniently composed.

The FST class does not provide support for:

  - Multiple initial states.

  - Initializing strings (an output string associated with the initial
    state, which is always generated when the FST begins).

  - Determinization and minimization of weighted FSTs.

Author: Michael Gasser <gasser@indiana.edu>
based on the NLTK fst module (URL: <http://www.nltk.org/>)
written by some unidentified author.

Version 2.0
"""

import re, os, copy, time, functools, glob, pickle
from collections import deque
# Required for weights.
from .semiring import *
# Required for parsing files of stems or roots into FSTs
from .letter_tree import *
# Parsing alternation rules
from .altrule import *
# Parsing morphotactic rules
from .mtax import *
# Parsing lists of consonant roots
from .roots import *

from .language import LANGUAGE_DIR

######################################################################
# CONTENTS
######################################################################
# 0. Constants
# 1. Finite State Transducer Cascade (added by MG)
# 2. Finite State Transducer
#    - State information
#    - Transition Arc Information
#    - FST Information
#    - State Modification
#    - Transition Arc Modification
#    - Transformations
#    - Misc
#    - Transduction
#    - Operations
######################################################################

######################################################################
# Constants
######################################################################

UNKNOWN = '?'

## Transducing times out after this many time steps
TIMEOUT = 2000

## Regexs for parsing FSTs and cascades
# string_set_label={chars1, chars1, chars2, ...}
SS_RE = re.compile('(\S+)\s*=\s*\{(.*)\}')
# weighting = UNIFICATION
WEIGHTING_RE = re.compile('weighting\s*=\s*(.*)')
# whether to reverse strings returned by the cascade FST
R2L_RE = re.compile('r2l')
# >fst<
CASC_FST_RE = re.compile(r'>(.*?)<')
# >xxx.rl<
CASC_ROOT_RE = re.compile(r'>(.+?\.rt)<')
# >xxx.ar<
CASC_AR_RE = re.compile(r'>(.+?\.ar)<')
# >xxx.mtx<
CASC_MTAX_RE = re.compile(r'>(.+?\.mtx)<')
# IO abbreviations
CASC_IO_ABBREV_RE = re.compile(r'{(.+)}\s*=\s*(.+)')
# -> state
INIT_RE = re.compile(r'->\s*(\S+)$')
# state ->
FINAL_RE = re.compile(r'(\S+)\s*->\s*(?:\[([^\]]*)\])?$')
# Transducer reverses input before transducing
R2L_RE = re.compile(r'\s*r2l\s*$')
# src -> dest [arc] [weight]
ARC_RE = re.compile(r'(\S+)?\s*->\s*(\S+)\s*\[(.*?)\]\s*(.*?)$')
# src -> dest <arc> [weight]
MULT_ARC_RE = re.compile(r'(\S+)?\s*->\s*(\S+)\s*<([^:]*?)(:?)([^:]*?)>\s*(.*?)$')
# IO pair abbreviation; replace with value in _IOabbrevs dict.
IO_ABBREV_RE= re.compile(r'{(.+?)}')
# src -> dest >>casc<<
CASC_RE = re.compile(r'(\S+)?\s*->\s*(\S+)\s*>>(.*?)<<\s*(.*?)$')
# src -> dest >FST<
FST_RE = re.compile(r'(\S+)?\s*->\s*(\S+)\s*>(.*?)<\s*(.*?)$')
# src -> dest +lex+
LEX_DEST_RE = re.compile(r'(\S+)?\s*->\s*(\S+)\s*\+(.*?)\+\s*(.*?)$')
# src +lex+
LEX_RE = re.compile(r'(\S+)?\s*\+(.*?)\+\s*(.*?)$')
# cascade name = {0, 1, 3, ...}
SUBCASC_RE = re.compile('cascade\s*(\S+)\s*=\s*\{(.*)\}')
# +lex+
CASC_LEX_RE = re.compile(r'\+(.*?)\+')
# features = {}
FEATS_RE = re.compile('features\s*=\s*(.+)')
# defaultFS = []
DEFAULT_FS_RE = re.compile('d\S*?\s*=\s*(.+)')

## Filtering FSTs for composition

CFILT = \
{'cfilt':
"""-> 0
0 -> 0 [?]
0 -> 0 [ep2:ep1]
0 -> 1 [ep1]
1 -> 1 [ep1]
1 -> 0 [?]
0 -> 2 [ep2]
2 -> 2 [ep2]
2 -> 0 [?]
0 ->
1 ->
2 ->
""",
'cfilt0':
"""-> 0
0 -> 0 [?]
0 -> 1 [ep1]
1 -> 1 [ep1]
1 -> 0 [?]
0 ->
1 ->
"""
}

######################################################################
# Finite State Transducer Cascade
######################################################################

class FSTCascade(list):
    """
    A list of FSTs to be composed.
    """

    def __init__(self, label, *fsts):
        list.__init__(self, fsts)

        self.label = label

        # String sets, abbreviated in cascade file
        self._stringsets = {}

        # IO pair abbreviations
        self._IOabbrevs = {}

        # Semiring weighting for all FSTs; defaults to FSS with unification
        self._weighting = UNIFICATION_SR

        # Composition of FSTs
        self._composition = None

        # All FSTs, including those not in the composition
        self._fsts = {}

        # Language this cascade belongs to
        self.language = None

        # Initial weight to use during transduction
        self.init_weight = None

        # Dictionary of lists of FST indices, for particular purposes
        self._cascades = {}

        # Segmentation units
        self.seg_units = []

        # Whether to reverse strings returned and input
        self.r2l = False

    def __str__(self):
        """Print name for cascade."""
        return 'Cascade ' + self.label

    def get_cas_dir(self):
        return os.path.join(self.language.directory, 'cas')

    def get_fst_dir(self, dirname='test'):
        if not self.language:
            d = os.path.join(os.path.dirname(__file__), os.path.pardir, 'languages', dirname)
        else:
            d = self.language.directory
        return os.path.join(d, 'fst')

    def get_lex_dir(self, dirname=''):
        if not self.language:
            d = os.path.join(os.path.dirname(__file__), os.path.pardir, 'languages', dirname)
        else:
            d = self.language.directory
        return os.path.join(d, 'lex')

    def add(self, fst):
        """Add an FST to the dictionary with its label as key."""
        self._fsts[fst.label] = fst

    def inverted(self):
        """Return a list of inverted FSTs in the cascade."""
        fsts = [(fst.inverted() if isinstance(fst, FST) else fst) for fst in self]
        inv = FSTCascade(self.label + '_inv', *fsts)
        inv.init_weight = self.init_weight
        inv._weighting = self._weighting
        inv._stringsets = self._stringsets
        if self.r2l:
            inv.r2l = True
        return inv

    def compose(self, begin=0, end=None, first=None, last=None, subcasc=None, backwards=False,
                relabel=True, trace=0):
        """Compose the FSTs that make up the cascade list or a sublist, including possible first and last FSTs."""
        if len(self) == 1:
            if self.r2l:
                self[0]._reverse = True
            return self[0]
        elif backwards:
            return self.compose_backwards(trace=trace)
        else:
            fsts = []
            if subcasc:
                if subcasc not in self._cascades:
                    raise ValueError("%r is not a valid subscascade label" % subcasc)
                fsts = [self[i] for i in self._cascades[subcasc]]
            else:
                fsts = self[begin:(end if end != None else len(self))]  # end could be 0
                if first:
                    fsts = [first] + fsts
                if last:
                    fsts.append(last)
            return FST.compose(fsts, self.label + '@', relabel=relabel, reverse=self.r2l, trace=trace)

    def mult_compose(self, ends):
        begin = 0
        fsts = []
        for end in ends:
            fsts.append(self.compose(begin, end))
            begin = end
        fsts.append(self.compose(begin, len(self)))
        return fsts

    def rev_compose(self, split_index, begin=0, trace=0):
        """Compose the FSTs in the cascade in two steps."""
        # Compose from split_index to end
        c1 = self.compose(begin=split_index, trace=trace)
        # Compose from beginning to split_index
        return self.compose(begin=begin, end=split_index, last=c1, trace=trace)

    def compose_backwards(self, indices=[], subcasc=None, trace=0):
#        print("Cascade backwards composition")
        if not indices:
            if subcasc:
                # Use a copy of the cascade indices because we're going to reverse them
                indices = list(self._cascades[subcasc])
            else:
                indices = list(range(len(self)))
        indices.reverse()
        c = FST.compose([self[indices[1]], self[indices[0]]], trace=trace, reverse=self.r2l)
        for n in indices[2:]:
            c = FST.compose([self[n], c], trace=trace, reverse=self.r2l)
        return c

    def composition(self, begin=0, end=None):
        """The composed FSTs."""
        if not self._composition:
            self._composition = self.compose(begin=begin, end=end or len(self))
        return self._composition

    def seq_transduce(self, string, weight=None):
        result = [[string, weight]]
        for fst in self[::-1]:
            print(fst.label)
            result = reduce_lists([fst.transduce(x[0], x[1]) for x in result])
            if not result:
                return False
        return result

    def transduce(self, inp_string, inp_weight, fsts, seg_units=[]):
        result = [[inp_string, inp_weight]]
        for fst in fsts:
            print(fst.label)
            result = reduce_lists([fst.transduce(x[0], x[1], seg_units=seg_units) for x in result])
            if not result:
                return False
        return result

    def transduce1(self, inp_string, fst_label='', fst_index=0, invert=False, trace=0):
        fst = self.get_fst(fst_label=fst_label, fst_index=fst_index)
        if not fst:
            print('No FST found for {}'.format(fst_label))
            return
        if invert:
            fst = fst.inverted()
        return fst.transduce(inp_string, seg_units=self.seg_units, trace=trace)

    def get_fst(self, fst_label='', fst_index=0):
        '''Return the FST with the given label or index.'''
        if fst_label:
            for fst in self:
                if fst.label == fst_label:
                    return fst
        else:
            return self[fst_index]

    def stringset(self, label):
        """A labeled set of strings."""
        return self._stringsets.get(label, None)

    def stringset_label(self, stringset):
        """The label for a stringset if it's in the dict."""
        for label, sset in self._stringsets.items():
            if stringset == sset:
                return label

    def stringset_intersection(self, ss_label1=None, ss_label2=None, ss1=None, ss2=None):
        """Label for the intersection of two stringsets or element if only one.

        Either the labels or the stringsets or both are provided."""
        ss1 = ss1 or self.stringset(ss_label1)
        ss2 = ss2 or self.stringset(ss_label2)
        ss_label1 = ss_label1 or self.stringset_label(ss1)
        ss_label2 = ss_label2 or self.stringset_label(ss2)
        if ss1 and ss2:
            intersect = ss1 & ss2
            if intersect:                                    # could be empty
                if len(intersect) == 1:
                    # If there's only one element, don't create a new stringset
                    return list(intersect)[0]
                # Otherwise create a new stringset
                i_label = self.stringset_label(intersect)
                if i_label:
                    # The stringset intersection is already in the dict
                    return i_label
                # The stringset intersection is not in the dict
                # Add it and return its label
                new_label = FSTCascade.simplify_intersection_label(ss_label1, ss_label2)
                return new_label

    @staticmethod
    def simplify_intersection_label(label1, label2):
        """Simplify an intersection label by eliminating common elements."""
        if not '&' in label1 and not '&' in label2:
            # the two expressions between with the same stringset
            return FSTCascade.simplify_difference_intersection_labels(label1, label2)
        else:
            return '&'.join(set(label1.split('&')) | set(label2.split('&')))

    @staticmethod
    def simplify_difference_intersection_labels(label1, label2):
        """Simplify an intersection of differences if first elements are the same."""
        labels1 = label1.split('-')
        labels2 = label2.split('-')
        if labels1[0] == labels2[0]:
            set1 = set(labels1[1].split(',')) if len(labels1) > 1 else set()
            set2 = set(labels2[1].split(',')) if len(labels2) > 1 else set()
            subtracted = set1 | set2
            return labels1[0] + '-' + ','.join(subtracted)
        else:
            return label1 + '&' + label2

    def generate_stringset(self, label):
        """Make a stringset from a label.

        L: stored stringset
        L1-L2: difference of two stored stringsets
        L1-abc: difference of stringset L1 and the set of characters {abc}
        L1&L2: intersection of two stringsets (stored or generated)
        """
        ss = self.stringset(label)
#        print("Making stringset {}: {}".format(label, ss))
        if ss:
            return ss
        if '-' in label or '&' in label:
            return self.intersect_stringsets(label.split('&'))

    def subtract_stringsets(self, label1, label2):
        """Difference between stringsets with labels or sets of characters."""
        ss1 = self.stringset(label1)
        if not ss1:
            ss1 = set([label1])
        ss2 = self.stringset(label2)
        if not ss2:
            ss2 = set([label2])    # set consisting of single phoneme/grapheme
        return ss1 - ss2

    def intersect_stringsets(self, labels):
        """Intersection of stringsets with given labels."""
        return functools.reduce(lambda x, y: x.intersection(y), [self.diff_stringset(label) for label in labels])

    def diff_stringset(self, label):
        """label is either a stored stringset or a stringset difference expression."""
        ss = self.stringset(label)
        if ss:
            return ss
        labels = label.split("-")
        # Assume there's only one -
        return self.subtract_strings(labels[0], labels[1])

    def subtract_strings(self, label1, label2):
        """Difference between stringsets with labels or sets of characters."""
        ss1 = self.stringset(label1)
        if not ss1:
            ss1 = set(label1.split(','))
        ss2 = self.stringset(label2)
        if not ss2:
            ss2 = set(label2.split(','))
        return ss1 - ss2

    def add_stringset(self, label, seq):
        """Add a labeled set of strings, updating sigma accordingly."""
#        print("Adding stringset {}: {}".format(label, seq))
        self._stringsets[label] = frozenset(seq)

    def get_IOpairs(self, abbrev):
        """
        The string containing IO character pairs for the given abbreviation.
        """
        return self._IOabbrevs.get(abbrev)

    def weighting(self):
        """The weighting semiring for the cascade."""
        return self._weighting

    def set_weighting(self, label):
        """Set the weighting for the cascade."""
        label = label.lower()
        if 'uni' in label:
            self._weighting = UNIFICATION_SR
        elif 'prob' in label:
            self._weighting = PROBABILITY_SR
        elif 'trop' in label:
            self._weighting = TROPICAL_SR

    def get(self, label):
        """The FST with the given label."""
        return self._fsts.get(label)

    def set_init_weight(self, fs):
        self.init_weight = FSSet(fs)

    @staticmethod
    def load(filename, seg_units=[], create_networks=True, subcasc=None,
             language=None,
             dirname='', weight_constraint=None, gen=False, verbose=True):
        """
        Load an FST cascade from a file.

        If not create_networks, only create the weighting and string sets.
        """
        if verbose:
            print('Loading FST cascade from {} for {}'.format(filename, language))
        directory, fil = os.path.split(filename)
        label = del_suffix(fil, '.')

        return FSTCascade.parse(label, open(filename, encoding='utf-8').read(), directory=directory,
                                subcasc=subcasc, create_networks=create_networks, seg_units=seg_units,
                                dirname=dirname,
                                language=language, weight_constraint=weight_constraint,
                                gen=gen, verbose=verbose)

    @staticmethod
    def parse(label, s, directory='', create_networks=True, seg_units=[],
              subcasc=None, language=None, dirname='',
              weight_constraint=None, gen=False, verbose=False):
        """
        Parse an FST cascade from the contents of a file as a string.

        If not create_networks, only create the weighting and string sets.
        """
        cascade = FSTCascade(label)
        cascade.language = language
        cascade.seg_units = seg_units

        lines = s.split('\n')[::-1]
        subcasc_indices = []

        while lines:
            line = lines.pop().split('#')[0].strip() # strip comments

            if not line: continue

            # Weighting for all FSTs
            m = WEIGHTING_RE.match(line)
            if m:
                cascade.set_weighting(m.group(1))
                continue

            # Whether to reverse the string returned
            m = R2L_RE.match(line)
            if m:
                cascade.r2l = True
                print("{} is right-to-left".format(cascade))
                continue

            # Subcascade, specifying indices
            #   label = {i, j, ...}
            m = SUBCASC_RE.match(line)
            if m:
                label, indices = m.groups()
                indices = [int(i.strip()) for i in indices.split(',')]
                cascade._cascades[label] = indices
                # If we're only loading a certain subcascade and this is it, save its indices
                if label == subcasc:
                    subcasc_indices = indices
                continue

            # String set (a list, converted to a frozenset)
            m = SS_RE.match(line)
            if m:
                label, strings = m.groups()
                # Characters may contain unicode
#                strings = strings.decode('utf8')
                cascade.add_stringset(label, [s.strip() for s in strings.split(',')])
                continue

            m = CASC_IO_ABBREV_RE.match(line)
            if m:
                abbrev, pairs = m.groups()
                cascade._IOabbrevs[abbrev] = pairs
#                print("Found IO abbrev: {} = {}".format(abbrev, pairs))
                continue

            # Alternation rule
            m = CASC_AR_RE.match(line)
            if m:
                if create_networks:
                    filename = m.group(1)
                    if not subcasc_indices or len(cascade) in subcasc_indices:
                        fst = FST.load(os.path.join(cascade.get_fst_dir(dirname=dirname), filename),
                                       cascade=cascade, weighting=cascade.weighting(),
                                       seg_units=seg_units, weight_constraint=weight_constraint,
                                       gen=gen, verbose=verbose)
                    else:
                        fst = 'FST' + str(len(cascade))
                        if verbose:
                            print('Skipping FST {}'.format(label))
                    cascade.append(fst)
                continue

            # Morphotactics
            m = CASC_MTAX_RE.match(line)
            if m:
                if create_networks:
                    filename = m.group(1)
                    if not subcasc_indices or len(cascade) in subcasc_indices:
                        fst = FST.load(os.path.join(cascade.get_fst_dir(dirname=dirname), filename),
                                       cascade=cascade, weighting=cascade.weighting(),
                                       seg_units=seg_units, weight_constraint=weight_constraint,
                                       gen=gen, verbose=verbose)
                    else:
                        fst = 'FST' + str(len(cascade))
                        if verbose:
                            print('Skipping FST {}'.format(label))
                    cascade.append(fst)
                continue

            # Roots
            m = CASC_ROOT_RE.match(line)
            if m:
                if create_networks:
                    filename = m.group(1)
                    print("** Looking for roots file {}".format(filename))
                    if not subcasc_indices or len(cascade) in subcasc_indices:
                        abbrevs = cascade._IOabbrevs
                        fst = FST.load(os.path.join(cascade.get_fst_dir(dirname=dirname), filename),
                                       cascade=cascade, weighting=cascade.weighting(),
                                       abbrevs=abbrevs,
                                       seg_units=seg_units, weight_constraint=weight_constraint,
                                       gen=gen, verbose=verbose)
                    else:
                        fst = 'FST' + str(len(cascade))
                        if verbose:
                            print('Skipping FST {}'.format(label))
                    cascade.append(fst)
                continue

            # FST
            m = CASC_FST_RE.match(line)
            if m:
                if create_networks:
                    label = m.group(1)
                    filename = label + '.fst'
                    if not subcasc_indices or len(cascade) in subcasc_indices:
                        abbrevs = cascade._IOabbrevs
                        fst = FST.load(os.path.join(cascade.get_fst_dir(dirname=dirname), filename),
                                       cascade=cascade, weighting=cascade.weighting(),
                                       abbrevs=abbrevs,
                                       seg_units=seg_units, weight_constraint=weight_constraint,
                                       gen=gen, verbose=verbose)
                    else:
                        fst = 'FST' + str(len(cascade))
                        if verbose:
                            print('Skipping FST {}'.format(label))
                    cascade.append(fst)
                continue

            # FST in a lex file
            m = CASC_LEX_RE.match(line)
            if m:
                if create_networks:
                    label = m.group(1)
                    # handle specs
                    filename = label + '.lex'
                    if not subcasc_indices or len(cascade) in subcasc_indices:
                        if verbose:
                            print('Adding lex FST {} to cascade, reversed? {}'.format(label, cascade.r2l))
                        fst = FST.load(os.path.join(cascade.get_lex_dir(dirname=dirname), filename),
                                       cascade=cascade, weighting=cascade.weighting(),
                                       seg_units=seg_units, weight_constraint=weight_constraint,
                                       gen=gen, reverse=cascade.r2l,
                                       verbose=verbose, lex_features=True)
                    else:
                        fst = 'FST' + str(len(cascade))
                        if verbose:
                            print('Skipping lex FST {}'.format(label))
                    cascade.append(fst)
                continue
            raise ValueError("bad line: %r" % line)

        return cascade

######################################################################
#{ Finite State Transducer
######################################################################

class FST:
    """
    A finite state transducer.  Each state is uniquely identified by a
    label, which is typically a string name or an integer id.  A
    state's label is used to access and modify the state.  Similarly,
    each arc is uniquely identified by a label, which is used to
    access and modify the arc.

    The set of arcs pointing away from a state are that state's
    I{outgoing} arcs.  The set of arcs pointing to a state are that
    state's I{incoming} arcs.  The state at which an arc originates is
    that arc's I{source} state (or C{src}), and the state at which it
    terminates is its I{destination} state (or C{dst}).

    It is possible to define an C{FST} object with no initial state.
    This is represented by assigning a value of C{None} to the
    C{initial_state} variable.  C{FST}s with no initial state are
    considered to encode an empty mapping.  I.e., transducing any
    string with such an C{FST} will result in failure.

    An FST is weighted if weighting is some Semiring. (MG)
    """

    def __init__(self, label, cascade=None, weighting=None):
        """
        Create a new finite state transducer, containing no states.
        """

        self.label = label
        """A label identifying this FST, for display and debugging purposes only."""

        self._comment = ''
        """An informal description of the FST."""

        # Strings that are raw representations of the changes and contexts or
        # filter context for the rule (if this is an alternation rule).
        self._filter_strings = []
        self._change_list = []
        self._lc_strings = []
        self._rc_strings = []

        #{ String set, possibly abbreviated in FST file (MG)
        self._stringsets = {}
        #}

        #{ (MG)
        """Copy seg_units and stringsets from cascade."""
        self.cascade = cascade
        """Cascade of FSTs that this FST is part of."""
        if cascade != None and cascade.language:
            self.seg_units = cascade.language.seg_units
        else:
            self.seg_units = []
        if cascade != None:
            self._stringsets = self.cascade._stringsets
        #}

        #{ (MG)
        if weighting != None:
            self._weighting = weighting
        elif cascade != None:
            self._weighting = cascade.weighting()
        else:
            self._weighting = None
        if self._weighting:
            self._default_weight = self._weighting.one
        else:
            self._default_weight = None
        """A Semiring that constrains the weights on arcs and their
        combination."""
        # This only applies to FSSet weighting
        self._defaultFS = None
        #}

        #{ Alphabets (Added by MG).
        self._sigma = set()
        """Symbols 'known' to the network (initially those appearing
        on arcs."""
        #}

        #{ Inserted FSTs, value is the number; needed for names
        # of inserted FST states (MG)
        self._inserted = {}
        #}

        #{ Dict of features and their possible values
        self.features = {}
        #}

        #{ Destination states (in the containing FST) for final states
        self._final_dst = {}
        #}

        #{ State Information
        ## Note that only one initial state is possible (MG).
        self._initial_state = None
        """The label of the initial state, or C{None} if this FST
        does not have an initial state."""

        self._incoming = {}
        """A dictionary mapping state labels to lists of incoming
        transition arc labels."""

        self._outgoing = {}
        """A dictionary mapping state labels to lists of outgoing
        transition arc labels."""

        self._is_final = {}
        """A dictionary mapping state labels to boolean values,
        indicating whether the state is final."""

        self._finalizing_string = {}
        """A dictionary mapping state labels of final states to output
        strings.  This string should be added to the output
        if the FST terminates at this state."""

        self._final_weight = {}
        """A dictionary mapping state labels of final states to output
        weights.  (Add by MG.)"""

        self._state_descr = {}
        """A dictionary mapping state labels to (optional) state
        descriptions."""
        #}

        #{ Transition Arc Information
        self._src = {}
        """A dictionary mapping each transition arc label to the label of
        its source state."""

        self._dst = {}
        """A dictionary mapping each transition arc label to the label of
        its destination state."""

        self._in_string = {}
        """A dictionary mapping each transition arc label to its input string."""

        self._out_string = {}
        """A dictionary mapping each transition arc label to its output string."""

        self._arc_descr = {}
        """A dictionary mapping transition arc labels to (optional)
        arc descriptions."""

        self._weight = {}
        """A dictionary mapping transition arc labels to weights.
        (MG)"""

        self._n_arcs = -1
        """Keep track of number of arcs to label arcs uniquely."""
        #}

        #{ Add to dict in parent cascade (MG)
        if self.cascade:
            self.cascade.add(self)
        #}

        self._reverse = False

    #////////////////////////////////////////////////////////////
    #{ State Information
    #////////////////////////////////////////////////////////////

    def states(self):
        """Return an iterator that will generate the state label of
        each state in this FST."""
        return iter(self._incoming)

    def has_state(self, label):
        """Return true if this FST contains a state with the given label."""
        return label in self._incoming

    def _get_initial_state(self):
        return self._initial_state

    def _set_initial_state(self, label):
        if label is not None and label not in self._incoming:
            raise ValueError('Unknown state label %r' % label)
        self._initial_state = label
    initial_state = property(_get_initial_state, _set_initial_state,
                             doc="The label of the initial state (R/W).")

    def incoming(self, state):
        """Return an iterator that will generate the incoming
        transition arcs for the given state.  The effects of modifying
        the FST's state while iterating are undefined, so if you plan
        to modify the state, you should copy the incoming transition
        arcs into a list first."""
        return iter(self._incoming[state])

    def outgoing(self, state):
        """Return an iterator that will generate the outgoing
        transition arcs for the given state.  The effects of modifying
        the FST's state while iterating are undefined, so if you plan
        to modify the state, you should copy the outgoing transition
        arcs into a list first."""
        return iter(self._outgoing[state])

    def is_final(self, state):
        """Return true if the state with the given state label is final."""
        return self._is_final[state]

    def _get_final_states(self):
        """Return a list of final states."""
        return [state for state in self.states() if self.is_final(state)]

    def finalizing_string(self, state):
        """Return the output string associated with the given final
        state.  If the FST terminates at this state, then this string
        will be emitted."""
        return self._finalizing_string.get(state, ())

    def final_weight(self, state):
        """Return the output weight associated with the given final
        state."""
        return self._final_weight.get(state, self._weighting.one)

    def state_descr(self, state):
        """Return the description for the given state, if it has one;
        or None, otherwise."""
        return self._state_descr.get(state)

    def n_states(self):
        """Number of states."""
        return len([s for s in self.states()])

    def state_arcs(self, src, dst):
        """Arcs from src state to dst state."""
        incoming = list(self.incoming(dst))
        return [out for out in self.outgoing(src) if out in incoming]

    def state_inout(self, src, dst):
        """Arc in and out strings for arcs from src state to dst state."""
        return [(self.in_string(a), self.out_string(a)) for a in self.state_arcs(src, dst)]

    def state_has_inout(self, src, dst, instr, outstr):
        """Is the in-out string pair on some arc from src state to dst state?"""
        return (instr, outstr) in self.state_inout(src, dst)

    #////////////////////////////////////////////////////////////
    #{ Transition Arc Information
    #////////////////////////////////////////////////////////////

    def arcs(self):
        """Return an iterator that will generate the arc label of
        each transition arc in this FST."""
        return iter(self._src)

    def src(self, arc):
        """Return the state label of this transition arc's source
        state."""
        return self._src[arc]

    def dst(self, arc):
        """Return the state label of this transition arc's destination
        state."""
        return self._dst[arc]

    def in_string(self, arc):
        """Return the given transition arc's input string."""
        return self._in_string[arc]

    def out_string(self, arc):
        """Return the given transition arc's output string."""
        return self._out_string[arc]

    def arc_descr(self, arc):
        """Return the description for the given transition arc, if it
        has one; or None, otherwise."""
        return self._arc_descr.get(arc)

    def arc_info(self, arc):
        """Return a tuple (src, dst, in_string, out_string) for the
        given arc, where:
          - C{src} is the label of the arc's source state.
          - C{dst} is the label of the arc's destination state.
          - C{weight} is the arc's weight.
          - C{in_string} is the arc's input string.
          - C{out_string} is the arc's output string.
        (Changed by MG.)
        """
        return (self._src[arc], self._dst[arc], self._in_string[arc], self._out_string[arc]) + \
               ((self.arc_weight(arc),) if self.is_weighted() else ())

    def arc_weight(self, arc):
        """Return the weight for the given arc.  Use the default if none is stored.

        (MG)"""
        return self._weight.get(arc, self._weighting.one)

    def arc_weight_jit(self, arc):
        """Return the weight for the given arc, creating it from a string if necessary (MG)."""
        weight = self._weight.get(arc, self._weighting.one)
#        print('Weight to parse', weight)
        # Convert the string to a real weight and replace the string with the weight in _weight
        if isinstance(weight, str):
            weight = self._weighting.parse_weight(weight)
            self._weight[arc] = weight
        return weight

    def arc_unknown(self, arc, in_side = True):
        """Is the label on in(out)_side UNKNOWN? (MG)"""
        string = self.in_string(arc) if in_side else self.out_string(arc)
        return self._label_unknown(string)

    def _label_unknown(self, label):
        """Unknown arc label (MG)."""
        return label == UNKNOWN

    def show_arcs(self):
        """Display useful information about all arcs."""
        for a in self.arcs():
            print("{}, {}, {}, {}, {}".format(a, self._src[a], self._dst[a], self._in_string[a], self._weight[a]))

    #////////////////////////////////////////////////////////////
    #{ FST Information
    #////////////////////////////////////////////////////////////

    def r2l(self):
        return self._reverse

    def sigma(self):
        """The sigma alphabet. (MG)"""
        return self._sigma

    ## Stringsets (lots of duplication with methods in FSTCascade
    ## make a Stringset class?)
    ## Added by MG.

    def stringset(self, label):
        """A labeled set of strings.  (MG)"""
        ss = self._stringsets.get(label, None)
        if not ss:
            ss = self.generate_stringset(label)
        return ss

    def add_stringset(self, label, lst):
        """Add a labeled set of strings, updating sigma accordingly. (MG)"""
        self._stringsets[label] = lst
        self._sigma = self._sigma.union(lst)

    def stringset_label(self, stringset):
        """The label for a stringset if it's in the dict."""
        for label, sset in self._stringsets.items():
            if stringset == sset:
                return label

    def stringset_intersection(self, ss_label1=None, ss_label2=None, ss1=None, ss2=None):
        """Label for the intersection of two stringsets or element if only one.

        Either the labels or the stringsets or both are provided."""
        ss1 = ss1 or self._stringsets.get(ss_label1, None)
        ss2 = ss2 or self._stringsets.get(ss_label2, None)
        ss_label1 = ss_label1 or self.stringset_label(ss1)
        ss_label2 = ss_label2 or self.stringset_label(ss2)
        if ss1 and ss2:
            intersect = ss1 & ss2
            if intersect:                                    # could be empty
                if len(intersect) == 1:
                    # If there's only one element, don't create a new stringset
                    return list(intersect)[0]
                # Otherwise create a new stringset
                i_label = self.stringset_label(intersect)
                if i_label:
                    # The stringset intersection is already in the dict
                    return i_label
                # The stringset intersection is not in the dict
                # Add it and return its label
                new_label = FSTCascade.simplify_intersection_label(ss_label1, ss_label2)
                return new_label

    def generate_stringset(self, label):
        """Make a stringset from a label.

        L: stored stringset
        L1-L2: difference of two stored stringsets
        L1-abc: difference of stringset L1 and the set of characters {abc}
        L1&L2: intersection of two stringsets (stored or generated)
        """
        if '-' in label or '&' in label:
            return self.intersect_stringsets(label.split('&'))

    def intersect_stringsets(self, labels):
        """Intersection of stringsets with given labels."""
#        print('INTERSECTING stringsets for {}'.format(labels))
        return functools.reduce(lambda x, y: x.intersection(y), [self.diff_stringset(label) for label in labels])

    def diff_stringset(self, label):
        """label is either a stored stringset or a stringset difference expression."""
        ss = self._stringsets.get(label, None)
        if ss:
            return ss
        labels = label.split("-")
        # Assume there's only one -
        return self.subtract_strings(labels[0], labels[1])

    def subtract_strings(self, label1, label2):
        """Difference between stringsets with labels or sets of characters."""
        ss1 = self._stringsets.get(label1, None)
        if not ss1:
            ss1 = set(label1.split(','))
        ss2 = self._stringsets.get(label2, None)
        if not ss2:
            # A comma-separated list of symbols of stringsets
            split_label2 = label2.split(',')
            ss2 = set([])
            for label in split_label2:
                ss = self._stringsets.get(label, None)
                if ss:
                    ss2.update(ss)
                else:
                    ss2.add(label)
        return ss1 - ss2

    def is_weighted(self):
        """
        Return true if this is FST is weighted.
        (MG)
        """
        return self._weighting

    def weighting(self):
        """
        Return true if this is FST is weighted.
        (MG)
        """
        if self.cascade:
            return self.cascade.weighting()
        else:
            return self._weighting

    def no_weight(self, weight):
        """Does FST have no weight? (MG)"""
        if not weight:
            return True
        weighting = self.weighting()
        if weighting and weight == weighting.one:
            return True
        return False

    #////////////////////////////////////////////////////////////
    #{ State Modification
    #////////////////////////////////////////////////////////////

    def add_state(self, label=None, is_final=False,
                  finalizing_string=(),
                  # (MG)
                  final_weight=None, descr=None):
        """
        Create a new state, and return its label.  The new state will
        have no incoming or outgoing arcs.  If C{label} is specified,
        then it will be used as the state's label; otherwise, a new
        unique label value will be chosen.  The new state will be
        final iff C{is_final} is true.  C{descr} is an optional
        description string for the new state.

        Arguments should be specified using keywords!
        """
        label = self._pick_label(label, 'state', self._incoming)

        # Add the state.
        self._incoming[label] = []
        self._outgoing[label] = []
        self._is_final[label] = is_final
        self._state_descr[label] = descr
        self._finalizing_string[label] = tuple(finalizing_string)
        self.set_final_weight(label, final_weight)

        # Return the new state's label.
        return label

    def del_state(self, label, trace=0):
        """
        Delete the state with the given label.  This will
        automatically delete any incoming or outgoing arcs attached to
        the state.
        (Debugged by MG.)
        """
        if label not in self._incoming:
            raise ValueError('Unknown state label %r' % label)

        if trace:
            print('Deleting state {}'.format(label))

        # Delete the incoming/outgoing arcs.
        for arc in self._incoming[label]:
            if arc in self._src:    # It may have been deleted already (MG)
                self._outgoing[self._src[arc]].remove(arc)   # First remove from other end (MG)
                del (self._src[arc], self._dst[arc], self._in_string[arc],
                     self._out_string[arc], self._arc_descr[arc])
        for arc in self._outgoing[label]:
            if arc in self._src:    # It may have been deleted already (MG)
                self._incoming[self._dst[arc]].remove(arc)   # First remove from other end (MG)
                del (self._src[arc], self._dst[arc], self._in_string[arc],
                     self._out_string[arc], self._arc_descr[arc])

        # Delete the state itself.
        del (self._incoming[label], self._outgoing[label],
             self._is_final[label], self._state_descr[label],
             self._finalizing_string[label])
        if label in self._final_weight:
             del self._final_weight[label]

        # Check if we just deleted the initial state.
        if label == self._initial_state:
            self._initial_state = None

    def set_final(self, state, is_final=True):
        """
        If C{is_final} is true, then make the state with the given
        label final; if C{is_final} is false, then make the state with
        the given label non-final.
        """
        if state not in self._incoming:
            raise ValueError('Unknown state label %r' % state)
        self._is_final[state] = is_final

    def set_finalizing_string(self, state, finalizing_string):
        """
        Set the given state's finalizing string.
        """
        if not self._is_final[state]:
            raise ValueError('%s is not a final state' % state)
        if state not in self._incoming:
            raise ValueError('Unknown state label %r' % state)
        self._finalizing_string[state] = tuple(finalizing_string)

    def set_final_weight(self, state, weight):
        """
        Set the given state's final weight (MG).
        """
        if weight:
            if not self._is_final[state]:
                raise ValueError('%s is not a final state' % state)
            if state not in self._incoming:
                raise ValueError('Unknown state label %r' % state)
            self._final_weight[state] = weight

    def set_final_dst(self, state, dst):
        if not self._is_final[state]:
            raise ValueError('%s is not a final state' % state)
        if state not in self._incoming:
            raise ValueError('Unknown state label %r' % state)
        self._final_dst[state] = dst

    def set_descr(self, state, descr):
        """
        Set the given state's description string.
        """
        if state not in self._incoming:
            raise ValueError('Unknown state label %r' % state)
        self._state_descr[state] = descr

    def dup_state(self, orig_state, label=None):
        """
        Duplicate an existing state.  I.e., create a new state M{s}
        such that:
          - M{s} is final iff C{orig_state} is final.
          - If C{orig_state} is final, then M{s.finalizing_string}
            is copied from C{orig_state}
          - For each outgoing arc from C{orig_state}, M{s} has an
            outgoing arc with the same input string, output
            string, and destination state.

        Note that if C{orig_state} contained self-loop arcs, then the
        corresponding arcs in M{s} will point to C{orig_state} (i.e.,
        they will I{not} be self-loop arcs).

        The state description is I{not} copied.

        @param label: The label for the new state.  If not specified,
            a unique integer will be used.
        """
        if orig_state not in self._incoming:
            raise ValueError('Unknown state label %r' % src)

        # Create a new state.
        new_state = self.add_state(label=label)

        # Copy finalization info.
        if self.is_final(orig_state):
            self.set_final(new_state)
            self.set_finalizing_string(new_state,
                                       self.finalizing_string(orig_state))
            # (MG)
            self.set_final_weight(new_state, self._final_weight.get(orig_state))

        # Copy the outgoing arcs.
        for arc in self._outgoing[orig_state]:
            self.add_arc(src=new_state, dst=self._dst[arc],
                         in_string=self._in_string[arc],
                         out_string=self._out_string[arc],
                         weight = self._weight[arc] if self.is_weighted() else None)

        return new_state

    #////////////////////////////////////////////////////////////
    #{ Transition Arc Modification
    #////////////////////////////////////////////////////////////

    def add_arc(self, src, dst, in_string, out_string, label=None, descr=None, weight=None):
        """
        Create a new transition arc, and return its label.

        Arguments should be specified using keywords!

        @param src: The label of the source state.
        @param dst: The label of the destination state.
        @param in_string: The input string
        @param out_string: The output string
        """
        label = self._pick_arc_label()

        # Check that src/dst are valid labels.
        if src not in self._incoming:
            raise ValueError('Unknown state label %r' % src)
        if dst not in self._incoming:
            raise ValueError('Unknown state label %r' % dst)

        # Add the arc.
        self._src[label] = src
        self._dst[label] = dst
        self._in_string[label] = in_string
        self._out_string[label] = out_string
        self._arc_descr[label] = descr
        #{ (MG)
        if self.is_weighted() and weight and weight != self.default_weight():
            # Only add the weight if there is one and it's not ONE
            self._weight[label] = weight  # if weight else self.default_weight()
        self._sigma = self._sigma.union((in_string, out_string))
        #}

        # Link the arc to its src/dst states.
        self._incoming[dst].append(label)
        self._outgoing[src].append(label)

        # Return the new arc's label.
        return label

    def _pick_arc_label(self):
        """A unique name for an arc."""
        self._n_arcs += 1
        return 'arc' + str(self._n_arcs)

    def del_arc(self, label):
        """
        Delete the transition arc with the given label.
        """
        if label not in self._src:
            raise ValueError('Unknown arc label %r' % src)

        # Disconnect the arc from its src/dst states.
        self._incoming[self._dst[label]].remove(label)
        self._outgoing[self._src[label]].remove(label)

        # Delete the arc itself.
        del (self._src[label], self._dst[label], self._in_string[label],
             self._out_string[label], self._arc_descr[label])
        #{ (MG)
        if self.is_weighted():
            del self._weight[label]
        ## Should we also delete the labels from the sigma??
        #}

    #////////////////////////////////////////////////////////////
    #{ Transformations
    #////////////////////////////////////////////////////////////

    def inverted(self):
        """Swap all in_string/out_string pairs."""
        fst = self.copy(del_suffix(self.label, '.') + '_inv')
        fst._in_string, fst._out_string = fst._out_string, fst._in_string
        if self._reverse:
            fst._reverse = True
        return fst

    def reversed(self):
        """Reverse the direction of all transition arcs."""
        fst = self.copy()
        fst._incoming, fst._outgoing = fst._outgoing, fst._incoming
        fst._src, fst._dst = fst._dst, fst._src
        return fst

    def trim(self, label='', trace=0):
        '''Trim by eliminating deadends.'''
        if trace:
            deleted = 0
            t0 = time.process_time()
            t = t0
            n_states = 0

        if self.initial_state is None:
            raise ValueError("No initial state!")

        to_delete = set(self.states())

        # Determine whether there is a path from each node to a final
        # node.
        queue = [s for s in self.states() if self.is_final(s)]
        if trace:
            t1 = time.process_time()
            if t1 - t > 30:
                print('  Took {} minute(s) to form initial trimming queue'.format(round((t1 - t0) / 60.0, 2)))
                t = t1
        path_to_final = set(queue)
        to_delete -= path_to_final
        while queue:
            state = queue.pop()
            if trace:
                n_states += 1
                t1 = time.process_time()
                if t1 - t > 30:
                    print('  Retaining {} valid states after {} minute(s)'.format(n_states,
                                                                                  round((t1 - t0) / 60.0, 2)))
                    t = t1
            srcs = [self.src(arc) for arc in self.incoming(state)]
            queue += [s for s in srcs if s not in path_to_final]
            path_to_final.update(srcs)
            to_delete -= set(srcs)

        for state in to_delete:
            if trace:
                deleted += 1
                t1 = time.process_time()
                if t1 - t > 60:
                    print('  Deleted {} states after {} minute(s)'.format(deleted,
                                                                          round((t1 - t0) / 60.0, 2)))
                    t = t1
            self.del_state(state)

        if trace and deleted > 0:
            print('Deleted {} total states'.format(deleted))

    def relabeled(self, label=None, relabel_states=True, relabel_arcs=True, trace=0):
        """
        Return a new FST that is identical to this FST, except that
        all state and arc labels have been replaced with new labels.
        These new labels are consecutive integers, starting with zero.

        @param relabel_states: If false, then don't relabel the states.
        @param relabel_arcs: If false, then don't relabel the arcs.
        """
        if trace:
            print('Relabeling')
            t0 = time.process_time()
            t = t0
            n_states = 0

        if label is None: label = '%s (relabeled)' % self.label
        fst = FST(label, cascade=self.cascade, weighting=self._weighting)
        # In case there is no cascade (how can this happen?), at least copy the
        # stringsets from self
        fst._stringsets = self._stringsets

        # This will ensure that the state relabelling is canonical, *if*
        # the FST is subsequential.
        state_ids = self._relabel_state_ids(self._initial_state, {})
        if len(state_ids) < len(self._outgoing):
            for state in self.states():
                if state not in state_ids:
                    state_ids[state] = len(state_ids)

        # This will ensure that the arc relabelling is canonical, *if*
        # the state labelling is canonical.
        arcs = sorted(self.arcs(), key=self.arc_info)
        arc_ids = dict([(a,i) for (i,a) in enumerate(arcs)])

        for state in self.states():
            if trace:
                n_states += 1
                t1 = time.process_time()
                if t1 - t > 30:
                    print('  Relabeled {} states after {} minute(s)'.format(n_states,
                                                                            round((t1 - t0) / 60.0, 2)))
                    t = t1
            if relabel_states: label = state_ids[state]
            else: label = state
            fst.add_state(label, is_final=self.is_final(state),
                          finalizing_string=self.finalizing_string(state),
                          final_weight=self._final_weight.get(state, None),
                          descr=self.state_descr(state))

        weight = None
        if trace:
            t0 = time.process_time()
            t = t0
            n_arcs = 0
        for arc in self.arcs():
            if trace:
                n_arcs += 1
                t1 = time.process_time()
                if t1 - t > 30:
                    print('  Relabeled {} arcs after {} minute(s)'.format(n_arcs,
                                                                          round((t1 - t0) / 60.0, 2)))
                    t = t1
            if relabel_arcs: label = arc_ids[arc]
            else: label = arc
            if self.is_weighted():
                src, dst, in_string, out_string, weight = self.arc_info(arc)
            else:
                src, dst, in_string, out_string = self.arc_info(arc)
            if relabel_states:
                src = state_ids[src]
                dst = state_ids[dst]
            fst.add_arc(src=src, dst=dst, in_string=in_string,
                        out_string=out_string,
                        weight=weight,
                        label=label, descr=self.arc_descr(arc))

        if relabel_states:
            fst._initial_state = state_ids[self._initial_state]
        else:
            fst._initial_state = self._initial_state

        return fst

    def _relabel_state_ids(self, state, ids):
        """
        A helper function for L{relabel()}, which decides which new
        label should be assigned to each state.
        """
        if state in ids: return
        ids[state] = len(ids)
        for arc in sorted(self.outgoing(state), key = lambda a:self.in_string(a)):
            self._relabel_state_ids(self.dst(arc), ids)
        return ids

    #////////////////////////////////////////////////////////////
    #{ Misc
    #////////////////////////////////////////////////////////////

    def copy(self, label=None):
        # Choose a label & create the FST.
        if label is None: label = '%s-copy' % self.label
        fst = FST(label)

        # Copy all state:
        fst._initial_state = self._initial_state
        #{ Values are lists, so we need deepcopies (MG)
        fst._incoming = copy.deepcopy(self._incoming)
        fst._outgoing = copy.deepcopy(self._outgoing)
        #}
        fst._is_final = self._is_final.copy()
        fst._finalizing_string = self._finalizing_string.copy()
        fst._final_weight = self._final_weight.copy()
        fst._state_descr = self._state_descr.copy()
        fst._src = self._src.copy()
        fst._dst = self._dst.copy()
        fst._in_string = self._in_string.copy()
        fst._out_string = self._out_string.copy()
        fst._arc_descr = self._arc_descr.copy()
        #{ Added by MG
        fst._weight = self._weight.copy()
        fst._weighting = self._weighting
        fst._sigma = self._sigma
        fst._stringsets = self._stringsets
        fst._inserted = self._inserted
        fst.cascade = self.cascade
        fst._n_arcs = self._n_arcs
        if self._comment:
            fst._comment = self._comment + ' (inverted)'
        fst._filter_strings = self._filter_strings
        fst._change_list = self._change_list
        fst._lc_strings = self._lc_strings
        fst._rc_strings = self._rc_strings
        #}
        return fst

    def __repr__(self):
        return '<FST {}>'.format(self.label)

    def __str__(self):
        # State labels cast with 'str' to make tuples also possible labels (MG)
        lines = ['FST %s' % self.label]
        if self._comment:
            lines.append('Comment: {}'.format(self._comment))
        for state in sorted(self.states()):
            # State information.
            if state == self._initial_state:
                line = '-> %s' % state
                lines.append('  %-60s # Initial state' % line)
            if self.is_final(state):
                line = '%s ->' % state
                if self.finalizing_string(state):
                    line += ' [%s]' % ' '.join(self.finalizing_string(state))
                lines.append('  %-60s # Final state' % line)
            # List states that would otherwise not be listed.
            if (state != self._initial_state and not self.is_final(state)
                and not self.outgoing(state) and not self.incoming(state)):
                lines.append('  %-60s # State' % state)
        # Outgoing edge information.
        for arc in sorted(self.arcs()):
            # (MG)
            if self.is_weighted():
                src, dst, in_string, out_string, weight = self.arc_info(arc)
            else:
                src, dst, in_string, out_string = self.arc_info(arc)
            #
            line = ('%s -> %s [%s:%s]' % (src, dst, in_string, out_string))
            lines.append('  %s' % line)
        return '\n'.join(lines)

    def default_weight(self):
        """
        Default weight for arcs: the 'one' element of the weighting semiring.
        (MG)
        """
        if self.is_weighted():
            return self._weighting.one

    def init_weight(self):
        """
        Default initial weight for transduction (MG).
        """
        if self.is_weighted():
            if self.cascade and self.cascade.init_weight:
                return self.cascade.init_weight
            else:
                return self._weighting.one

    def set_features(self, feats):
        """
        Set features and possible values on weights in this FST.
        """
        self.features = feats

    def get_features(self, feats=None, exclude=[]):
        """
        All features and possible values on weights in this FST.
        """
        if not self.features:
            features = feats or {}
            for arc in self.arcs():
                fss = self.arc_weight_jit(arc)
                for fs in fss:
                    self.accum_fs_features(fs, features, exclude)
            self.features = features
        return self.features

    def accum_fs_features(self, fs, feats, exclude):
        """Accumulate features from fs in feats.
        @param  fs     FeatStruct to get features and values from
        @param  feats  dict of current features and their possible values
        """
        for feat, value in fs.items():
            if value != None:
                # Ignore None values
                if feat in exclude:
                    continue
                elif isinstance(value, FeatStruct):
                    if feat in feats:
                        feats_val = feats[feat]
                    else:
                        feats_val = {}
                    if isinstance(feats_val, dict):
                        self.accum_fs_features(value, feats_val, exclude)
                        feats[feat] = feats_val
                elif feat not in feats:
                    if isinstance(value, bool):
                        feats[feat] = [True, False]
                    else:
                        feats[feat] = [value]
                elif not isinstance(value, bool):
                    # Don't record separate boolean value
                    feats_val = feats[feat]
                    # A list of values; add value if it's not there
                    if isinstance(feats_val, list) and value not in feats_val:
                        feats[feat].append(value)

    @staticmethod
    def get_dir(language):
        """
        The directory where FSTs, compiled and uncompiled, are stored.
        """
        return os.path.join(language.directory, 'fst')

    @staticmethod
    def get_pickle_dir(language):
        """
        The directory where FSTs, compiled and uncompiled, are stored.
        """
        return os.path.join(language.directory, 'pkl')

    @staticmethod
    def pickle(fst, language=None, directory='', replace=False,
               label='', verbose=False):
        """
        Dump the FST to a pickle.
        """
        directory = directory or FST.get_pickle_dir(language)
        label = label or fst.label
        path = os.path.join(directory, label + ".pkl")
        if not replace and os.path.exists(path):
            print("Pickle {} exists, not replacing".format(path))
            return
        file = open(path, 'wb')
        pickle.dump(fst, file)

    @staticmethod
    def unpickle(label, language=None, directory='', verbose=False):
        """
        Load the FST from a .pkl file.
        """
        directory = directory or FST.get_pickle_dir(language)
        path = os.path.join(directory, label + ".pkl")
        if not os.path.exists(path):
#            print("Pickle {} not found!".format(path))
            return
        file = open(path, "rb")
        if verbose:
            print('Unpickling {}'.format(path))
#            print("File {}".format(file))
        return pickle.load(file)

    @staticmethod
    def stringify_weights(fst):
        '''Convert each weight to a string (MG).'''
        print('Stringifying weights')
        for arc, weight in fst._weight.items():
            fst._weight[arc] = weight.__str__()

    @staticmethod
    def write(fst, filename=None, directory='',
              defaultFS='', stringsets=False,
              features=False, exclude_features=[]):
        """Write an FST to a file."""
        if not filename:
            extension = '.fst'
            filename = os.path.join(directory, fst + extension)

        print('Writing FST {} to {}'.format(fst.label, filename))
        out = open(filename, 'w', encoding='utf-8')
        # Write the features and values, defaultFS, and stringsets; whether FST is reversed (right-to-left)
        if fst.r2l():
            out.write("r2l\n")
        if features:
            out.write('features=' + str(fst.get_features(exclude=exclude_features)) + '\n')
        if defaultFS:
            out.write('defaultFS=' + defaultFS + '\n')
        if stringsets:
            out.write(fst._stringsets.__repr__() + '\n')
            #            print(fst._stringsets.__repr__(), file=out)
        # Write the initial and final states
        out.write('->' + str(fst._initial_state) + '\n')
        for state in fst.states():
            if fst.is_final(state):
                out.write(str(state) + '->\n')
                # Still need finalizing string and weight
        for arc in fst.arcs():
            ## Arc source and dest
            src_label = str(fst._src[arc])
            dest_label = str(fst._dst[arc])
            out.write(src_label + '->' + dest_label)
            in_string = fst._in_string[arc]
            out_string = fst._out_string[arc]
            out.write(' [')
            if in_string == out_string:
                if in_string:
                    out.write(in_string)
                else:
                    out.write(':')
            else:
                if in_string:
                    out.write(in_string)
                out.write(':')
                if out_string:
                    out.write(out_string)
            out.write('] ')
            ## Arc weights
            if fst.weighting():
                weight = fst.arc_weight(arc)
                weight_repr = weight.__repr__()
#                Here because there was a problem with strings including commas in FSs
#                if weight_repr != '[]':
#                    print("Writing weight for arc {}, {}, {}".format(arc, weight, weight_repr))
                if isinstance(weight, str):
                    # String weight
                    if weight != '':
                        out.write(weight)
                elif weight != fst._weighting.one:
                    # FSSet weight
#                    if '"' in weight_repr:
#                        print(weight_repr)
                    out.write(weight_repr)
            out.write('\n')
        out.close()

    @staticmethod
    def get_fst_files(fst_name, fst_directory, parts=True):
        """
        Get FST files for fst_name in fst_directory, searching either for parts
        or for complete file.
        """
        if parts:
            files = glob.glob(os.path.join(fst_directory, '*__' + fst_name + '.fst'))
            if files:
                return files
        full = glob.glob(os.path.join(fst_directory, fst_name + '.fst'))
        if full:
            return full
        return []

    @staticmethod
    def restore(fst_name,
                cas_directory='', fst_directory='', pkl_directory='',
                cascade=None, weighting=UNIFICATION_SR, seg_units=[],
                # if True, look for .pkl file to load
                pickle=True,
                # Features determining which FST
                empty=True, phon=False, segment=False, generate=False, simplified=False,
                experimental=False, mwe=False, create_weights=True, verbose=False):
        '''Restore an FST from a file, in some cases creating the cascade first.

        If empty is true, look for the empty (guesser) FST only.
        Otherwise, look first for the lexical one, then the empty one.
        2021.5: returns pair with second element a boolean indicating
        whether the FST was found in a pickle.
        '''
        empty_name = fst_name + '0'
        # experimental has priority over others
        name = fst_name
        if mwe:
            name = name + 'M'
        if experimental:
            name = name + 'X'
        elif empty:
            name = empty_name
            if phon:
                name = name + 'P'
        elif simplified:
            name = fst_name + '_S'
        elif phon:
            name = fst_name + 'P'
        elif segment:
            name = fst_name + '+'
        else:
            name = fst_name
        if generate:
            name += 'G'
            empty_name += 'G'
        elif not segment:
            name += 'A'
            empty_name += 'A'
        if pickle:
#            print("Unpickling {} in {}".format(name, pkl_directory))
            fst = FST.unpickle(name, directory=pkl_directory)
            if fst:
                return fst, True
        # Look for the full, explicit FST
        explicit = FST.get_fst_files(name, pkl_directory)
#        filename = name + '.fst'
#        if os.path.exists(os.path.join(fst_directory, filename)):
        if explicit:
            if verbose:
                print('  Restoring FST {} from FST files {}'.format(name, explicit))
            return FST.restore_parse_from_files(explicit, name,
                                                cascade=cascade, weighting=weighting,
                                                seg_units=seg_units,
                                                create_weights=create_weights,
                                                verbose=verbose), \
                   False
        # Look for the empty FST (except for segmentation) if there is no lexical one
        if not empty and not segment:
            empty_paths = FST.get_fst_files(empty_name, pkl_directory)
#            filename = empty_name + '.fst'
#            if os.path.exists(os.path.join(fst_directory, filename)):
            if empty_paths:
                if verbose:
                    print('  Restoring empty FST {} from FST file {}'.format(empty_name, empty_paths))
                return FST.restore_parse_from_files(empty_paths, empty_name,
                                                    cascade=cascade, weighting=weighting,
                                                    seg_units=seg_units,
                                                    create_weights=create_weights,
                                                    verbose=verbose), \
                       False

    @staticmethod
    def split(directory, fst_file, limit=50000):
        """Split an FST, writing it to multiple files."""
        print('Splitting FST in {}'.format(fst_file))
        lines = open(os.path.join(directory, fst_file), encoding='utf-8')
        line_n = 0
        file_n = 0
        out = open(os.path.join(directory, '{}__{}'.format(file_n, fst_file)),
                   'w', encoding='utf-8')
        for line in lines:
            if line_n >= limit:
                out.close()
                file_n += 1
                out = open(os.path.join(directory, '{}__{}'.format(file_n, fst_file)),
                           'w', encoding='utf-8')
                line_n = 0
            out.write(line)
            line_n += 1
        out.close()

    @staticmethod
    def restore_parse_from_files(paths, label, cascade=None, weighting=None,
                                 seg_units=[],
                                 create_weights=True, verbose=False):
        """Restore an FST from one or more files."""
#        print('Restoring {}, cascade {}'.format(label, cascade))
        fst = FST.restore_parse(None, None, path=paths[0], label=label,
                                cascade=cascade,
                                weighting=weighting,
                                seg_units=seg_units, fst=None,
                                create_weights=create_weights, verbose=verbose)
        for path in paths[1:]:
            FST.restore_parse(None, None, path, label=label,
                              cascade=cascade,
                              weighting=weighting,
                              seg_units=seg_units, fst=fst,
                              create_weights=create_weights, verbose=verbose)
        return fst

    @staticmethod
    def restore_parse(directory, fst_file=None, path=None, weighting=None,
                      label='', cascade=None, fst=None,
                      seg_units=[], create_weights=True, verbose=False):
        """Restore an FST from a .fst file."""
#        print("** Restoring {} from file {}".format(label, fst_file))
#        label, suffix = fst_file.split('.')

        path = path or os.path.join(directory, fst_file)

        s = open(path, encoding='utf-8').read()

        fst = fst or FST(label, cascade=cascade, weighting=weighting)

        weighting = fst.weighting()

        prev_src = None
        lines = s.split('\n')[::-1]
        nstates = 0

        while lines:
            line = lines.pop().split('#')[0].strip() # strip comments

            if not line: continue

            # Stringsets
            if line[0] == '{' and line[-1] == '}':
                # line is a dictionary, which must be the stringsets for the FST
                fst._stringsets = eval(line)
#                print('Read in stringsets for', fst)
                continue

            # Initial state
            m = INIT_RE.match(line)
            if m:
                label = m.group(1)
                if not fst.has_state(label):
                    fst.add_state(label)
                    nstates += 1
                fst._set_initial_state(label)
                continue

            # Features and values
            m = FEATS_RE.match(line)
            if m:
                fst.set_features(eval(m.group(1)))
                continue

            # DefaultFS
            m = DEFAULT_FS_RE.match(line)
            if m:
                df = m.group(1)
                fst._defaultFS = FeatStruct(df)
                continue

            # Final state
            m = FINAL_RE.match(line)
            if m:
                label, finalizing_string = m.groups()
                if not fst.has_state(label):
                    fst.add_state(label)
                    nstates += 1
                fst.set_final(label)
                if finalizing_string is not None:
                    finalizing_string = finalizing_string.split()
                    fst.set_finalizing_string(label, finalizing_string)
                continue

            # right-to-left transduction
            m = R2L_RE.match(line)
            if m:
                fst._reverse = True
                continue

            # Transition arc(s)
            m = ARC_RE.match(line)
            if m:
                src, dst, strings, weight = m.groups()
                if src is None: src = prev_src
                if src is None: raise ValueError("bad line: %r" % line)
                prev_src = src
                if weighting and create_weights:
                    weight = weighting.parse_weight(weight)
                if not fst.has_state(src):
                    fst.add_state(src)
                    nstates += 1
                if not fst.has_state(dst):
                    fst.add_state(dst)
                    nstates += 1
                # arc could be a list of string pairs separated by ;
                # don't strip these because char could be space
                strings = [s for s in strings.split(';')]
                for arc_spec in strings:
                    arc = fst._parse_arc(arc_spec)
                    if isinstance(arc, list):
                        # out_string is a stringset label
                        for instring, outstring in arc:
                            fst.add_arc(src, dst, instring, outstring, weight=weight)
                    else:
                        fst.add_arc(src, dst, arc[0], arc[1], weight=weight)
                continue

            if nstates % 1000 == 0:
                print('States created {}'.format(nstates))

            raise ValueError("bad line: %r" % line)

        return fst

    @staticmethod
    def load(filename, cascade=None, weighting=None, reverse=False,
             seg_units=[], verbose=False, abbrevs=None,
             lex_features=False, dest_lex=False, weight_constraint=None,
             gen=False):
        """
        Load an FST from a file.

        dest_lex=True means that the destination FST is specified for each entry in a .lex file.
        """
        directory, fil = os.path.split(filename)
        label, suffix = fil.split('.')

        print("** Loading FST from {}".format(filename))

        if suffix == 'fst':
            if verbose:
                print('Loading FST from {}'.format(filename))
            # It's a file in the standard FST format; parse() it
            return FST.parse(label, open(filename, encoding='utf-8').read(),
                             weighting=weighting,
                             cascade=cascade, directory=directory,
                             seg_units=seg_units, abbrevs=abbrevs,
                             weight_constraint=weight_constraint,
                             gen=gen, verbose=verbose)

        elif suffix == 'rt':
            if verbose:
                print("Loading roots from {}".format(filename))
            return Roots.parse(label, open(filename, encoding='utf-8').read(),
                               fst=FST(label, cascade=cascade, weighting=UNIFICATION_SR),
                               cascade=cascade, directory=directory,
                               seg_units=seg_units, abbrevs=abbrevs,
                               weight_constraint=weight_constraint,
                               gen=gen, verbose=verbose)

        elif suffix == 'mtx':
            if verbose:
                print('Loading morphotactics from {}'.format(filename))
            # It's a file in MTAX format; parse_mtax() it
            fst = FST(label, cascade=cascade)
            mtax = MTax(fst, directory=directory)
            mtax.parse(label, open(filename, encoding='utf-8').read(),
                       verbose=verbose)
            FST.compile_mtax(mtax, gen=gen, cascade=cascade, verbose=verbose)
            return fst

        elif suffix == 'ar':
            # It's a file in alternation rule format; parse_altrule() it
            fst = FST(label, cascade=cascade)
            altrule = AltRule(fst, seg_units)
            altrule.parse(open(filename, encoding='utf-8').read())
            if verbose:
                print('Loading {} from {}'.format('filter altrule' if altrule.filter else 'change altrule', filename))
            return fst

        elif suffix == 'lex':
            # It's a file in lexicon format; treeify the file, then convert the tree to an FST
            if verbose:
                print('Loading sublexicon from {}, reverse={}'.format(filename, reverse))
            treeified = treeify_file(filename, seg_units=seg_units, reverse=reverse,
                                     dest=dest_lex, verbose=False)
#            print('Treeified {}'.format(treeified))
            return FST.tree_to_fst(treeified,
                                   label, cascade=cascade, weighting=weighting,
                                   lex_features=lex_features, weight_constraint=weight_constraint,
                                   dest=dest_lex, verbose=False)

    @staticmethod
    def compile_mtax(mtax, gen=False, cascade=None, verbose=False):
        print("Compiling {} with {}".format(mtax, cascade))
        # Create a final state
        final_label = DFLT_FINAL
        mtax.states.append([final_label, {'paths': [], 'shortcuts': []}])
        mtax.fst.add_state(final_label)
        mtax.fst.set_final(final_label)

        # Now make the paths between the successive states
        for index, state in enumerate(mtax.states[:-1]):
            src = state[0]
            paths = state[1].get('paths')
            dest = mtax.states[index+1][0]
            # Do the normal paths
            for in_string, weight in paths:
                if '.lex' in in_string:
                    # in_string is a lex filename
                    label = in_string.split('.')[0]
                    fst1 = mtax.cascade.get(label) if mtax.cascade else None
                    if not fst1:
                        if verbose:
                            print('Creating FST from lex file', in_string)
                        fst1 = mtax.fst.load(os.path.join(mtax.cascade.get_lex_dir(), in_string),
                                             weighting=mtax.weighting, cascade=cascade,
                                             seg_units=mtax.seg_units, reverse=cascade.r2l,
                                             lex_features=True, dest_lex=False)
                    if verbose:
                        print('Inserting', fst1.label, 'between', src, 'and', dest)
                    mtax.fst.insert(fst1, src, dest, weight=weight, mult_dsts=False)
                elif '.cas' in in_string:
                    # in_string is a cascade filename
                    label = in_string.split('.')[0]
                    fst1 = mtax.cascade.get(label) if mtax.cascade else None
                    if not fst1:
                        casc = FSTCascade.load(os.path.join(mtax.cascade.get_cas_dir(), in_string), seg_units=mtax.seg_units,
                                               language=mtax.cascade.language)
                        if verbose:
                            print('Composing {}'.format(casc))
                        fst1 = casc.compose(trace=verbose)
                        # Record the new composed FST in the higher cascade
                        if mtax.cascade:
                            mtax.cascade.add(fst1)
                        if verbose:
                            print('Inserting cascade {} between {} and {}, r2l? {}'.format(label, src, dest, casc.r2l))
                        if casc.r2l:
#                            print("{} (inserted) is right-to-left".format(casc))
                            fst1._reverse = True
                    mtax.fst.insert(fst1, src, dest, weight=weight, mult_dsts=False)
                elif '.fst' in in_string:
                    # in_string is a FST filename
                    label = in_string.split('.')[0]
                    fst1 = mtax.cascade.get(label) if mtax.cascade else None
                    if not fst1:
                        if verbose:
                            print('Compiling FST from file', in_string)
                        fst1 = mtax.fst.load(os.path.join(mtax.cascade.get_fst_dir(), in_string),
                                             weighting=mtax.weighting, cascade=mtax.cascade,
                                             seg_units=mtax.seg_units)
                    if verbose:
                        print('Inserting', fst1.label, 'between', src, 'and', dest)
                    mtax.fst.insert(fst1, src, dest, weight=weight, mult_dsts=False)
                elif in_string == NO_INPUT:
                    mtax.fst.add_arc(src, dest, '', '', weight=weight)
                else:
#                    print("Making multiple arcs for {} from {} to {}, weight: {}".format(in_string, src, dest, weight))
                    mtax.fst._make_mult_arcs(in_string, '', src, dest, weight, mtax.seg_units, gen=gen)
            # Do the shortcuts
            shortcuts = state[1].get('shortcuts')
            for dest, file, fss in shortcuts:
                print("Shortcut: {}, {}, {}".format(dest, file, fss))
                if file:
                    if fss:
                        wt = fss
                    else:
                        wt = TOPFSS
#                    if verbose:
#                        print('lex shortcut', file)
                    label = file.split('.')[0]
                    fst1 = mtax.cascade.get(label) if mtax.cascade else None
                    if not fst1:
                        fst1 = mtax.fst.load(os.path.join(mtax.cascade.get_lex_dir(), file),
# os.path.join(mtax.directory, file),
                                             weighting=mtax.weighting, cascade=mtax.cascade,
                                             seg_units=mtax.seg_units,
                                             lex_features=True, dest_lex=False)
                    if verbose:
                        print('Inserting', fst1.label, 'between', src, 'and', dest)
                    mtax.fst.insert(fst1, src, dest, weight=wt, mult_dsts=False)
                else:
#                    print("FS shortcut from {} to {} with weight {}".format(src, dest, fss))
                    mtax.fst.add_arc(src, dest, '', '', weight=fss)

    @staticmethod
    def load_fst_from_files(names, directory,
                            cascade=None, weighting=None, seg_units=[],
                            verbose=False, lex_features=False,
                            dest_lex=False, weight_constraint=None):
        """
        Load an FST from a list of filenames.
        """
        name0 = names[0]
        filename0 =  name0 + '.fst'
        fst = FST.parse(name0, open(filename0, encoding='utf-8').read(),
                        weighting=weighting,
                        cascade=cascade, directory=directory,
                        seg_units=seg_units, weight_constraint=weight_constraint,
                        verbose=verbose)
        for name in names[1:]:
            filename = name + '.fst'
            FST.parse(name, open(filename, encoding='utf-8').read(),
                      fst=fst, weighting=weighting,
                      cascade=cascade, directory=directory,
                      seg_units=seg_units, weight_constraint=weight_constraint,
                      verbose=verbose)
        return fst

    @staticmethod
    def parse(label, s, weighting=None, cascade=None, fst=None,
              directory='', seg_units=[], gen=False, abbrevs=None, verbose=False,
              weight_constraint=None):
        """
        Parse an FST from a string consisting of multiple lines from a file.
        Create a new FST if fst is None.
        """
#        print("** Parsing {}".format(s))
        fst = fst or FST(label, cascade=cascade, weighting=weighting)

        weighting = fst.weighting()

        lines = s.split('\n')[::-1]
        while lines:
            line = lines.pop().split('#')[0].strip() # strip comments

            if not line: continue

            line = FST.sub_IOabbrevs(line, abbrevs)

            #{ String set (a list; added by MG)
            m = SS_RE.match(line)
            if m:
                label, strings = m.groups()
                fst.add_stringset(label, [s.strip() for s in strings.split(',')])
                continue
            #}

            #{ FST is reversed (right-to-left).
            m = R2L_RE.match(line)
            if m:
#                print("FST is right-to-left")
                fst._reverse = True
                continue
            #}

            #{ Features and values (a dict; added by MG)
            m = FEATS_RE.match(line)
            if m:
                features = m.group(1)
                print('Features {}'.format(eval(features)))
                continue
            #}

            # Initial state
            m = INIT_RE.match(line)
            if m:
                label = m.group(1)
                if not fst.has_state(label): fst.add_state(label)
                fst._set_initial_state(label)
                continue

            # Final state
            # Still need a way to read in the final weight (MG)
            m = FINAL_RE.match(line)
            if m:
                label, finalizing_string = m.groups()
                if not fst.has_state(label): fst.add_state(label)
                fst.set_final(label)
                if finalizing_string is not None:
                    finalizing_string = finalizing_string.split()
                    fst.set_finalizing_string(label, finalizing_string)
                continue

            # State
            m = re.match('(\S+)$', line)
            if m:
                label = m.group(1)
                if not fst.has_state(label): fst.add_state(label)
                continue

            # State description
            m = re.match(r'descr\s+(\S+?):\s*(.*)$', line)
            if m:
                label, descr = m.groups()
                # Allow for multi-line descriptions:
                while lines and re.match(r'\s+\S', lines[-1]):
                    descr = descr.rstrip()+' '+lines.pop().lstrip()
                if not fst.has_state(label): fst.add_state(label)
                fst.set_descr(label, descr)
                continue

            # Transition arc(s)
            # MG: Changes here to allow for weight at end, optional ':' separator, and
            # multiple arcs joining the same two states (separated by ';')
            m = ARC_RE.match(line)
            if m:
                src, dst, strings, weight = m.groups()
                if src is None: raise ValueError("bad line: %r" % line)
                if weighting:
                    weight = weighting.parse_weight(weight)
                    if weight_constraint:
                        constrained_weight = weighting.multiply(weight, weight_constraint)
                        if not constrained_weight:
                            continue
                        else:
                            weight = constrained_weight
                if not fst.has_state(src): fst.add_state(src)
                if not fst.has_state(dst): fst.add_state(dst)
                # arc could be a list of string pairs separated by ;
                # don't strip these because char could be space
                strings = [s for s in strings.split(';')]
                for arc_spec in strings:
                    arc = fst._parse_arc(arc_spec)
                    if isinstance(arc, list):
                        # out_string is a stringset label
                        for instring, outstring in arc:
                            fst.add_arc(src, dst, instring, outstring, weight=weight)
                    else:
                        fst.add_arc(src, dst, arc[0], arc[1], weight=weight)
                continue

            #{ Multiple transitions connecting src to dst: insert a simple, non-branching FST
            # <chars:feats>
            m = MULT_ARC_RE.match(line)
            if m:
                groups = m.groups()
                src, dst = groups[:2]
                if src is None: src = prev_src
                if src is None: raise ValueError("bad line: %r" % line)
                prev_src = src
                # Out string is what follows : or None
                if groups[3]:  # the : separating in_string and out_string
                    in_string, out_string = groups[2], groups[4]
                else:
                    in_string = groups[4]
                    out_string = None
                weight = groups[5]
                if weighting:
                    weight = weighting.parse_weight(weight)
                    if weight_constraint:
                        constrained_weight = weighting.multiply(weight, weight_constraint)
                        if not constrained_weight:
                            continue
                        else:
                            weight = constrained_weight
                if not fst.has_state(src): fst.add_state(src)
                if not fst.has_state(dst): fst.add_state(dst)
                fst._make_mult_arcs(in_string, out_string, src, dst, weight, seg_units)
                continue
            #}

            #{ FST cascade to be loaded from file, composed, and concatenated in (MG)
            #  unless it's already been composed
            #  >>file<<
            m = CASC_RE.match(line)
            if m:
                src, dst, label, weight = m.groups()
                if src is None: src = prev_src
                if src is None: raise ValueError("bad line: %r" % line)
                prev_src = src
                if weighting:
                    weight = weighting.parse_weight(weight)
                fstfile = label + '.fst'
                fstpath = os.path.join(cascade.get_fst_dir(), fstfile)
#                fstpath = os.path.join(directory, fstfile)
                if os.path.exists(fstpath):
                    fst1 = FST.load(fstpath, weighting=weighting, cascade=cascade,
                                    seg_units=seg_units, weight_constraint=weight_constraint, verbose=verbose)
                else:
                    if verbose:
                        print('Cascade not yet composed')
                    casfile = label + '.cas'
                    if verbose:
                        print('Inserting cascade {} between {} and {}'.format(label, src, dst))
                    casc = FSTCascade.load(os.path.join(cascade.get_cas_dir(), casfile), seg_units=seg_units,
                                           language=cascade.language,
                                           weight_constraint=weight_constraint, verbose=verbose)
                    if verbose:
                        print('Composing {}'.format(casc))
                    fst1 = casc.compose()
                    # Record the new composed FST in the higher cascade
                    if cascade:
                        cascade.add(fst1)
                fst.insert(fst1, src, dst, weight=weight)
                continue
            #}

            #{ FST already loaded or to load from file, to be concatenated in (MG)
            # >file<
            m = FST_RE.match(line)
            if m:
                src, dst, label, weight = m.groups()
                if src is None: src = prev_src
                if src is None: raise ValueError("bad line: %r" % line)
                prev_src = src
                if weighting:
                    weight = weighting.parse_weight(weight)
                filename = label + '.fst'
                fst1 = cascade.get(label) if cascade else None
                if not fst1:
                    fst1 = FST.load(os.path.join(directory, filename), weighting=weighting, cascade=cascade,
                                    seg_units=seg_units, weight_constraint=weight_constraint, verbose=verbose)
#                if fst1._reverse:
#                    print("{} is right-to-left".format(fst1))
                fst.insert(fst1, src, dst, weight=weight)
                continue
            #}

            #{ Lex file to be converted to a letter tree, then to an FST and concatenated in (MG)
            # Destination FST specified here, not in file, to be used for all entries.
            # +file+
            m = LEX_DEST_RE.match(line)
            if m:
                src, dst, label, weight = m.groups()
                if src is None: src = prev_src
                if src is None: raise ValueError("bad line: %r" % line)
                prev_src = src
                if weighting:
                    weight = weighting.parse_weight(weight)
                # handle specs
                filename = label + '.lex'
                fst1 = cascade.get(label) if cascade else None
                if not fst1:
                    fst1 = FST.load(os.path.join(cascade.get_lex_dir(), filename), weighting=weighting, cascade=cascade,
                                    seg_units=seg_units, verbose=verbose, lex_features=True, dest_lex=False)
                fst.insert(fst1, src, dst, weight=weight, mult_dsts=False)
                continue
            #}

            #{ Lex file to be converted to a letter tree, then to an FST and concatenated in (MG).
            # Each lex entry specifies an output and a destination FST, as well as a possible weight.
            # +file+
            m = LEX_RE.match(line)
            if m:
                src, label, weight = m.groups()
                if src is None: src = prev_src
                if src is None: raise ValueError("bad line: %r" % line)
                prev_src = src
                if weighting:
                    weight = weighting.parse_weight(weight)
                # handle specs
                filename = label + '.lex'
                fst1 = cascade.get(label) if cascade else None
                if not fst1:
                    fst1 = FST.load(os.path.join(cascade.get_lex_dir(), filename), weighting=weighting, cascade=cascade,
                                    seg_units=seg_units, verbose=verbose, lex_features=True, dest_lex=True)
                fst.insert(fst1, src, None, weight=weight, mult_dsts=True)
                continue
            #}

            raise ValueError("bad line: %r" % line)

#        if fst._reverse:
#            print("Reversing\n{}".format(fst))
#            fst = fst.reversed()
#            print("Reversed\n{}".format(fst))

        return fst

    @staticmethod
    def sub_IOabbrevs(string, abbrevs):
        """
        Replace IOabbrevs in string with IO pairs, using IOabbrevs dict
        for cascade.
        For examples, see mvz/cas/v_stemA.cas
        """
        if not abbrevs:
            return string
        def subfunc(matchobj):
            key = matchobj.group(1)
            string = abbrevs.get(key)
            if not string:
                print("WARNING: {} NOT IN DICT".format(key))
                return ''
            else:
                return string
        return IO_ABBREV_RE.sub(subfunc, string)

    def _parse_arc(self, string):
        """Parse input and output strings for one arc (MG).

        in_string:out_string
        inout_string
        """
        m = re.match(r'([^:]*)(:?)([^:]*)', string)
        if m:
            groups = m.groups()
            if groups[1]:  # the : separating in_string and out_string
                # There is a value for either in_string or out_string or both
                in_string = groups[0] if groups[0] else ''
                out_string = groups[2] if groups[2] else ''
                outss = self.stringset(out_string)
                if outss:
                    return [(in_string, o) for o in outss]
            else:
                # the : is missing; use the same value for both strings
                # (which can't be '')
                in_string = out_string = groups[0]
            return in_string, out_string
        else:
            raise ValueError("bad arc representation: %r" % string)

    def _make_mult_arcs(self, in_string, out_string, src, dst, weight, seg_units,
                        gen=False):
        """
        Create states and arcs to join src with dst, given multiple chars in in_string.
        """
#        print("** make_mult_arcs {} {} {} {} {}".format(in_string, out_string, src, dst, weight.__repr__()))
        ## Intermediate state labels
        # In case there are spaces in in_string, remove these for state names
        in_string_label = in_string.replace(' ', '')
        label_pre = src + '_' + in_string_label
        label_suf = '_' + dst

        ## If there are parentheses in in_string, separate the three portions
        in_string1 = in_paren = out_string1 = out_paren = ''
        in_strings1 = in_paren_s = in_strings2 = []
        in_string2 = in_string
        out_string2 = out_string
        if '(' in in_string:
            in_string1, in_paren, in_string2 = FST.split_paren(in_string)
            if len(in_string1) > len(in_string2):
                # Pre-paren portion is longer; use this to correspond to output string
                out_string1 = out_string
                out_string2 = None if out_string == None else ''
                out_paren = None if out_string == None else ''
            elif in_string2:
                # Post-paren portion is longer; use this to correspond to output string
                in_string = in_string2
                out_string2 = out_string
                out_string2 = None if out_string == None else ''
                out_paren = None if out_string == None else ''
            else:
                # Only parenthetical stuff
                out_paren = out_string

        dst1 = src

        # Pre-paren portion
        if in_string1:
            in_strings1, out_strings1 = FST.make_in_out_strings(in_string1, out_string1, seg_units)
            dst1 = self._make_mult_arcs1(in_strings1, out_strings1, src, label_pre, label_suf, 0,
                                         weight=weight if gen else None)

        # Parenthetical portion
        if in_paren:
            # Save the beginning of the skip arc
            src1 = dst1
            in_paren_s, out_paren_s = FST.make_in_out_strings(in_paren, out_paren, seg_units)
            if not in_string2:
                # This is the end of the in_string, so only go as far as the second-to-last char
                last_in, last_out = in_paren_s[-1], out_paren_s[-1]
                in_paren_s, out_parens = in_paren_s[:-1], out_paren_s[:-1]
            dst1 = self._make_mult_arcs1(in_paren_s, out_paren_s, dst1, label_pre, '()' + label_suf, len(in_strings1),
                                         weight=weight if (gen and not in_string1) else None)
            # Make the skip arc
            if not in_string2:
                # This is the last arc on the path, so add the weight
                self.add_arc(src1, dst, '', '', weight=weight)
            else:
                # Skip as far as dst1 without the weight
                self.add_arc(src1, dst1, '', '')

        # Post-paren portion
        if in_string2:
            in_strings2, out_strings2 = FST.make_in_out_strings(in_string2, out_string2, seg_units)
            last_in, last_out = in_strings2[-1], out_strings2[-1]
            dst1 = self._make_mult_arcs1(in_strings2[:-1], out_strings2[:-1], dst1, label_pre, label_suf,
                                         len(in_strings1) + len(in_paren_s),
                                         weight=weight if (gen and not in_paren) else None)

        # What do to if there's no input string but there's an output string
        if not in_string and out_string:
            in_strings, out_strings = FST.make_in_out_strings(in_string, out_string, seg_units)
            last_in, last_out = in_strings[-1], out_strings[-1]
            dst1 = self._make_mult_arcs1(in_strings[:-1], out_strings[:-1], dst1, label_pre, label_suf, 0)

        # Last characters in in_strings and out_strings; put weight here unless we put it at the beginning
        # of a string of input characters for generation.
        w = None
        if not gen or (gen and len(in_strings2) == 1):
            w = weight
        self.add_arc(dst1, dst, last_in, last_out, weight=w)

    def _make_mult_arcs1(self, in_strings, out_strings, src, label_pre, label_suf, start_index,
                         weight=None):
        '''Starting with src, create states for corresponding chars in in_strings and out_strings,
        returning the last intermediate state.'''
        src1 = src
        dst1 = src
#        if weight:
#            print('make_mult_arcs with weight {}'.format(weight.__repr__()))
        for index, (s_in, s_out) in enumerate(zip(in_strings, out_strings)):
            dst1 = label_pre + str(index + start_index) + label_suf
            # But it still might not be novel
            while self.has_state(dst1):
                # Try again by adding an asterisk
                dst1 += '*'
            # Add the new intermediate state
            self.add_state(dst1)
            # Connect the last two intermediate states
            self.add_arc(src1, dst1, s_in, s_out, weight=weight if (weight and index==0) else None)
            src1 = dst1
        return dst1

    @staticmethod
    def split_paren(string):
        '''Split string into 3 substrings: portion before "(", portion between "()", portion after ")".'''
        s1 = string.partition('(')
        s2 = s1[-1].partition(')')
        return [s1[0], s2[0], s2[-1]]

    @staticmethod
    def make_in_out_strings(in_string, out_string, seg_units):
        in_strings = segment(in_string, seg_units, correct=False) if seg_units else list(in_string)
        # If out_string is None, use in_strings
        if out_string == None:
            out_strings = in_strings
        elif out_string == '':
            # No output characters
            out_strings = [''] * len(in_strings)
        else:
            out_strings = segment(out_string, seg_units, correct=False) if seg_units else list(out_string)

        # Make in_strings and out_strings match
        n_in, n_out = len(in_strings), len(out_strings)
        if n_in > n_out:
            # Pad out_strings on the right with ''s
            out_strings.extend([''] * (n_in - n_out))
        elif n_out > n_in:
            # Pad in_strings on the right with ''s
            in_strings.extend([''] * (n_out - n_in))
        return in_strings, out_strings

    @staticmethod
    def tree_to_fst(tree, label, cascade=None, weighting=None, lex_features=False,
                    dest=False, weight_constraint=None,
                    verbose=False):
        """
        Turn a letter tree into an FST (MG).

        dest=True means that destination FSTs appear before weights in a pair.
        """
        fst = FST(label, cascade=cascade, weighting=weighting)

        weighting = fst.weighting()

        fst.add_state('start')
        fst._set_initial_state('start')
        fst._subtree_to_states('start', tree, '', weighting=weighting, lex_features=lex_features, dest=dest,
                               weight_constraint=weight_constraint, verbose=verbose)
#        print("** fst {}".format(fst))
        return fst

    def _subtree_to_states(self, state, subtree, label, weighting=None, lex_features=False, dest=False,
                           weight_constraint=None, verbose=False):
        """
        subtree a dict with characters as keys, values either subtrees,
        (chars, feats), or [feats] (MG).
        """
        for char, rest in subtree.items():
            if verbose:
                print('char {} rest {}'.format(char, rest))
            if not char or char == '':
                # End of the word and no more chars
                if rest and isinstance(rest, list):
                    # Multiple destinations and features
                    for n, rest0 in enumerate(rest):
                        state_n = state + str(n)
                        self.add_state(state_n)
                        self.add_arc(state, state_n, '', '')
                        self.set_final(state_n)
                        if dest:
                            self.set_final_dst(state_n, rest0[0])
                        if lex_features:
                            if dest:
                                weight_spec = rest0[1]
                            else:
                                weight_spec = rest0
                            weight = weighting.parse_weight(weight_spec)
                            if weight and weight_constraint:
                                constrained_weight = weighting.multiply(weight, weight_constraint)
                                if not constrained_weight:
                                    print('Warning: weight {} is incompatible with constraint {}'.format(weight, weight_constraint))
                                else:
                                    weight = constrained_weight
                            self.set_final_weight(state_n, weight)
                else:
                    # Just one destination and feature set
                    self.set_final(state)
                    if dest:
                        self.set_final_dst(state, rest[0])
                    # Add any features to the arcs INTO this state
                    if lex_features and rest:
                        if dest:
                            weight_spec = rest[1]
                        else:
                            weight_spec = rest
                        weight = weighting.parse_weight(';'.join(weight_spec))
                        if weight and weight_constraint:
                            constrained_weight = weighting.multiply(weight, weight_constraint)
                            if not constrained_weight:
                                print('Warning: weight {} is incompatible with constraint {}'.format(weight, weight_constraint))
                            else:
                                weight = constrained_weight
                        self.set_final_weight(state, weight)
            else:
                if isinstance(char, tuple):
                    # Either inchar or outchar could be empty
                    inchar = char[0]
                    outchar = char[1]
                    if inchar == outchar:
                        new_state = label + inchar + '_'
                    else:
                        new_state = label + inchar + ':' + outchar + '_'
                else:
                    inchar = char
                    outchar = char
                    new_state = label + inchar
                self.add_state(new_state)
                # No weight specified
                inarc = inchar if inchar else ''
                outarc = outchar if outchar else ''
                self.add_arc(state, new_state, inarc, outarc)
                if isinstance(rest, dict):
                    # Another subtree
                    self._subtree_to_states(new_state, rest, new_state, weighting=weighting, lex_features=lex_features,
                                            dest=dest, weight_constraint=weight_constraint,
                                            verbose=False)
                else:
                    self._extend_subtree(new_state, rest[0], rest[1], weighting=weighting, lex_features=lex_features,
                                         dest=dest, weight_constraint=weight_constraint,
                                         verbose=False)

    def _extend_subtree(self, state, chars, features, weighting=None, lex_features=False, dest=False,
                        weight_constraint=None, verbose=False):
        """Extend a subtree (remaining chars and features) (MG)."""
        curr_state = state
        if verbose:
            print('chars {}'.format(chars))
        for char in chars:
            if isinstance(char, tuple):
                inchar = char[0]
                outchar = char[1]
                if inchar == outchar:
                    next_state = curr_state + inchar + '_'
                else:
                    next_state = curr_state + inchar + ':' + outchar + '_'
            else:
                inchar = char
                outchar = char
                next_state = curr_state + char
            self.add_state(next_state)
            inarc = inchar if inchar else ''         # (inchar,) if inchar else ()
            outarc = outchar if outchar else ''      # (outchar,) if outchar else ()
            self.add_arc(curr_state, next_state, inarc, outarc)
            curr_state = next_state
        self.set_final(curr_state)
        if dest:
            self.set_final_dst(curr_state, features[0])
        if lex_features and features:
            # Add features to the arcs INTO the final state
            weight_spec = features[1] if dest else features
            weight = weighting.parse_weight(weight_spec)
            if weight and weight_constraint:
                constrained_weight = weighting.multiply(weight, weight_constraint)
                if not constrained_weight:
                    print('Warning: weight {} is incompatible wit constraint {}'.format(weight, weight_constraint))
                else:
                    weight = constrained_weight
            self.set_final_weight(curr_state, weight)

    #////////////////////////////////////////////////////////////
    #{ Transduction
    #////////////////////////////////////////////////////////////

    def transduce1(self, input, trace=False):
        """Return the output for one path through the FST for the input."""
        out = self.step_transduce(input, step=trace, all_paths=False).__next__()
        if out:
            return ''.join(out[1]), out[2]

    def transduce(self, input, init_weight=None, split_string='',
                  # related to generation
                  gen=False, print_word=False, print_prefixes=None,
                  seg_units=[], reject_same=False,
                  trace=0, tracefeat='', dup_output=False,
                  result_limit=5, timeit=False, timeout=TIMEOUT,
                  verbosity=0):
        """
        Return the output for all paths through the FST for the input and
        initial weight. (MG)
        """
#        print("Transducing {} -- {}".format(input, init_weight.__repr__()))
#        print(" Result limit {}".format(result_limit))
        if timeit:
            time1 = time.time()
        words = []
        result = []
        word_count = 1
        original_word = input
        # Split the input string into 'characters'
        if seg_units:
            # Use seg_units to segment, accepting any character not in the list
            input = list(segment(input, seg_units, correct=False))
        elif split_string:
            input = list(input.split(split_string))
        else:
            input = list(input)
        n_outputs = 0
        if self.r2l():
            # FST operates right-to-left, so reverse the input list of segments
            input.reverse()
        for output in self.step_transduce(input, step=False, init_weight=init_weight,
                                          trace=trace, tracefeat=tracefeat):
            # output[0] is 'succeed' or 'fail'
            # output[1] is output string (if success)
            # output[2] is accumulated weight (if success)
            # There can be failures and duplicate successes
            if len(result) >= result_limit:
                if verbosity:
                    print("Exceeded result limit {}: {}".format(result_limit, input))
#                print("Exceeded {}".format(result_limit))
#                print("Result {}".format(result))
                break
            if output[1] and (output not in result):
                if self.r2l():
                    # FST operates right-to-left, so reverse the output list of segments before joining
#                    output[1].reverse()
                    word = ''.join(reversed(output[1]))
#                    print("Reversed output {}".format(output[1]))
                else:
                    word = ''.join(output[1])
                if reject_same and word == original_word:
#                    print('{} is the same the original word')
                    continue
#                print('Found word {}: {}'.format(word_count, word))
                word_count += 1
                output[1] = word
                if dup_output or word not in words:
                    if print_word:
                        self.print_output(word, prefixes=print_prefixes)
                    words.append(word)
                    result.append(output)
                elif not gen:
                    result.append(output)
                if timeout:
                    # Only count outputs if they succeed
                    if n_outputs >= timeout:
                        if verbosity:
                            print('Timed out at {}: {}'.format(timeout, input))
                        break
                    n_outputs += 1
#        print('transduce result: {}'.format(result))
        res = []
        for r in result:
            if r[2]:
                # (joined) output string, accumulated weight
                res.append([r[1], r[2]])
            else:
                # no weight, just (joined) output string
                res.append(r[1])
        # Group results by output string before returning
        res = self.consolidate(res)
        if timeit:
            print('Transduction took {} seconds'.format(time.time()-t1))
#        if self.cascade and self.cascade.reverse:
#            print("Reversing output string")
#            res = res[::-1]
        return res

    def print_output(self, word, prefixes=None):
        """For generation, we may want to print output words, possibly with other words
        or morphemes prefixed to them, immediately."""
        if prefixes:
            for p in print_prefixes:
                print(p + word)
        else:
            print(word)

    def consolidate(self, out_weights):
        """For transduction output list, consolidate weights for the same output (MG)."""
        if len(out_weights) > 1 and every(lambda x: isinstance(x, list), out_weights):
            dct = {}
            for out, weight in out_weights:
                if out in dct:
                    dct[out] = self.weighting().add(dct[out], weight)
                else:
                    dct[out] = weight
            # Result has to be a list of lists so they can be mutated later on
            return [[k, v] for (k, v) in dct.items()]
        else:
            return out_weights

    def transduce_all(self, inputs_weights):
        """Transduce all input weight pairs. (MG)"""
        return reduce_lists([self.transduce(i, w) for i, w in inputs_weights])

    def _transduce_match_input(self, input, in_pos, in_string,
                               weight=None, accum_weight=None,
                               trace=0):
        """Does the string in input beginning with in_pos match in_string from FST?
        """
        ## Different ways to fail
        if in_string != '':
            if in_pos >= len(input):
                if trace > 2:
                    print('  Match fails because of position {}'.format(in_pos))
                return False
            if self._label_unknown(in_string):
                if not self.match_unknown(input[in_pos:in_pos+1]):
                    if trace > 2:
                        print("  Match fails because unknown doesn't match")
                    return False
            stringset = self.stringset(in_string)
            input_string = input[in_pos]
            # Fail if the in_string is a stringset and input_string is not in it
            if stringset:
                if input_string not in stringset:
                    if trace > 2:
                        print("  Match fails because {} not in {}".format(input_string, stringset))
                    return False
            # Fail if the appropriate portion of the input doesn't match in_string
            elif input_string != in_string:
                if trace > 2:
                    print("  Match fails because {} != {}".format(input_string, in_string))
                return False

        ## Succeed
        # For a weighted FST, return the new accumulated weight
        if self.is_weighted():
            wt_prod = self.weighting().multiply(accum_weight, weight)
            if not wt_prod and trace > 2:
                print("  Match fails because {} doesn't match {}".format(accum_weight, weight))
            return wt_prod

        # For an unweighted FST, return True
        return True

    def _transduce_match_final(self, state, input, in_pos, accum_weight, trace=0, path=[]):
        """Match final states in transduction, returning accumulated weight (MG)."""
        if self.is_final(state) and in_pos >= len(input):
            if self.is_weighted():
                final_weight = self._final_weight.get(state, None)
                if final_weight:
                    if trace > 1:
                        print('Multiplying again')
                    accum_weight = self.weighting().multiply(accum_weight, final_weight)
                if accum_weight:
                    if trace:
                        print('FINAL STATE, INPUT CONSUMED')
                    if trace > 1: print('weight: {}'.format(accum_weight))
                    return accum_weight
            else:
                return True

    def match_unknown(self, target):
        """Does the target string match the unknown character?"""
        return target not in self.sigma()

    def step_transduce(self, input, step=True, all_paths=True, init_weight=None,
                       trace=0, tracefeat=''):
        """
        This is implemented as a generator, to make it easier to support stepping.

        all_paths added to permit returning more than one path.
        """
        output = []
        in_pos = 0
        # Only relevant for weighted FSTs.
        # Weight on one arc
        weight = None
        # Accumulated weight for path through FST
        accum_weight = init_weight if init_weight else self.init_weight()

        # 'frontier' is a stack used to keep track of which parts of
        # the search space we have yet to examine.  Each element has
        # the form (arc, in_pos, out_pos), and indicates that we
        # should try rolling the input position back to in_pos, the
        # output position back to out_pos, and applying arc.  Note
        # that the order that we check elements in is important, since
        # rolling the output position back involves discarding
        # generated output.
        frontier = []

        # Start in the initial state, and search for a valid
        # transduction path to a final state.
        state = self._initial_state

        go_on = True
        found = False

        # Outer loop; necessary for returning outputs for multiple paths (MG)
        while go_on:

            # Inner loop: find a single path through the FST
            # as long as we haven't run out of input or we haven't reached
            # a final state or the frontier hasn't been emptied
            while not found and go_on:

                if trace:
                    if trace > 1: print()
                    print('STATE: {}'.format(state))
                    s = '  Output: {}'.format(output)
#                    s = '  Output: ' + output
                    if in_pos >= len(input):
                        print(s + ' end of input')
                        print('  weight: {}'.format(accum_weight))
                    else:
                        print(s + ' input pos: {}, char: {}'.format(in_pos, input[in_pos]))
                        print('  weight: {}'.format(accum_weight))

                # Get a list of arcs we can possibly take.
                arcs = self.outgoing(state)

                # Add the arcs to our backtracking stack.
                if trace:
                    any_matches = False
                    any_arcs = False
                    matching_arcs = []
                    nonmatching_arcs = []
                for arc in arcs:
                    any_arcs = True
                    in_string = self.in_string(arc)
                    # (MG)
                    if self.is_weighted():
                        weight = self.arc_weight_jit(arc)
                    # For a weighted FST, this is the new weight
                    input_match = self._transduce_match_input(input, in_pos, in_string, weight, accum_weight,
                                                              trace=trace)
                    # Trace weight feature
                    if weight and tracefeat:
                        weightfvals = {fs.get(tracefeat) for fs in weight}
                        if any(weightfvals):
                            accumfvals = {fs.get(tracefeat) for fs in accum_weight}
                            if not input_match:
                                print('OUTPUT: {}; {} FAILED TO MATCH {}'.format(''.join(output), accumfvals, weightfvals))
                    if input_match and (in_pos < len(input) or in_string == ''):
                        # Don't bother if we've already reached the end of the word
                        if trace:
                            matching_arcs.append((arc[3:], in_string, self.out_string(arc), weight))
                            any_matches = True
                        frontier_elem = (arc, in_pos, len(output)) + ((input_match,) if weight else ())
                        frontier.append(frontier_elem)
                    elif trace:
                        if trace > 2 and not input_match:
                            print("  Input match failed")
                        if trace > 2 and (in_pos >= len(input)):
                            print("  Input match fails because input position {} >= input length {}".format(in_pos, len(input)))
                        nonmatching_arcs.append((arc[3:], in_string, self.out_string(arc), weight))
                if trace:
                    if any_arcs:
                        if matching_arcs:
                            s = '  Matching:'
                            #                            print('  Matching:', end='')
                            if trace > 1 or len(matching_arcs) < 9:
                                for a, ins, outs, wt in matching_arcs:
                                    s += ' {}[{}:{}]'.format(a, ins, outs)
                                    if trace > 3:
                                        print(s + ' {}'.format(wt))
                            else:
                                s += ' ...'
                            print(s)
                        if nonmatching_arcs:
                            s = '  Not matching:'
                            if trace > 1 or len(nonmatching_arcs) < 9:
                                for a, ins, outs, wt in nonmatching_arcs:
                                    s += ' {}[{}:{}]'.format(a, ins, outs)
                                    if trace > 3:
                                        print(s + ' {}'.format(wt))
                            else:
                                s += ' ...'
                            print(s)
                        if not any_matches:
                            print('  NO MATCHES')
                            if trace > 2:
                                if frontier:
                                    print('  Remaining frontier:')
                                    for f in frontier:
                                        print('  {}'.format(f))

                final_match = self._transduce_match_final(state, input, in_pos, accum_weight, trace=trace)

                if final_match:
                    if self.is_weighted():
                        accum_weight = final_match
                    found = True
                elif frontier:
                    # Make a new triple from the top element of the frontiering stack
                    if weight:
                        arc, in_pos, out_pos, accum_weight = frontier.pop()
                    else:
                        arc, in_pos, out_pos = frontier.pop()
                    if trace:
                        print('  Selected: {}<{},{}>'.format(arc[3:], in_pos, out_pos))
                    if step:
                        yield ['step', (arc, in_pos, output[:out_pos]) + ((accum_weight,) if weight else ())]

                    # update our state, input position, & output.
                    state = self.dst(arc)
#                    if out_pos > len(output):
#                        print('out pos {}, output {}, in_string {}, out_string {}'.format(out_pos, output,
#                                                                                          self.in_string(arc),
#                                                                                          self.out_string(arc)))
                    assert out_pos <= len(output)
                    in_string = self.in_string(arc)
                    out_string = self.out_string(arc)
                    if out_string != '' and (out_string == UNKNOWN or self.stringset(out_string)):
                        # UNKNOWN as the output character only makes sense if UNKNOWN is the input character;
                        # the same holds for stringsets
                        # add whatever UNKNOWN or the stringset matched on the input to the output
                        if in_pos > len(input) - 1:
                            print("Something wrong with {} and/or input {} at position {}".format(out_string, input, in_pos))
                        out_string = input[in_pos]
                    # always add 1 CHAR, unless '', right?
                    if in_string != '':
                        in_pos = in_pos + 1                  # len(in_string)
                    output = output[:out_pos]
                    if out_string != '':
                        output.append(out_string)
                    if trace > 2:
                        print(" Updating {}, {}, {}, {}, {}".format(arc, state, in_string, out_string, output))
                else:
                    # The stack is empty; quit
                    go_on = False
                    yield ['fail', None, accum_weight]

            # Unless nothing was found, return the output
            if go_on:
                # If a subsequential transducer, add the final output for the terminal state.
                output += self.finalizing_string(state)
                if self.is_weighted():
                    # For a weighted FST, multiply in the final state's weights (MG)
                    fw = self._final_weight.get(state, None)
                    if fw:
                        accum_weight = self.weighting().multiply(accum_weight, fw)
                # Return the output side and weight (MG) for one path
                found = True
                yield ['succeed', output, accum_weight]

                # If all_paths is True, backtrack and return output for other paths (MG)
                if all_paths and frontier:
                    found = False
                    # Use the last triple/quadruple in the frontier and pop it off
                    if weight:
                        arc, in_pos, out_pos, accum_weight = frontier.pop()
                    else:
                        arc, in_pos, out_pos = frontier.pop()
                    if trace:
                        print('Backtracking, selected: {}<{},{}>; {},{}'.format(arc[3:], in_pos, out_pos, output, output[:out_pos]))
                    if step:
                        yield ['backtrack', (arc, in_pos, output[:out_pos]) + ((accum_weight,) if weight else ())]
                    # Using the new triple...,
                    # set the state to be the arc's destination,
                    state = self.dst(arc)
                    assert out_pos <= len(output)
                    # set the input position to be the start position
                    # + the length of the new input string,
                    in_string = self.in_string(arc)
                    out_string = self.out_string(arc)
                    if out_string == UNKNOWN or self.stringset(out_string):
                        # UNKNOWN as the output character only makes sense if UNKNOWN is the input character;
                        # add whatever UNKNOWN matched on the input to the output
                        out_string = input[in_pos]
                    if in_string != '':
                        in_pos = in_pos + 1
                    # set the output list to be everything up to the saved position
                    # + the new output string
                    output = output[:out_pos]
                    output.append(out_string)
                # Stop looking if all_paths is False or there's nothing on the frontier (MG)
                else:
                    go_on = False

    #////////////////////////////////////////////////////////////
    #{ Operations (added by MG)
    #////////////////////////////////////////////////////////////

    @staticmethod
    def compose(fsts, label='', relabel=True, reverse=False, trace=0):
        """Compose a list of FSTs."""
        weighting = fsts[0].weighting()
        for f in fsts[1:]:
            if f.weighting() != weighting:
                raise ValueError("%s has different weighting from %s" % (f.label, fsts[0].label))
        if len(fsts) > 2:
            comp1 = functools.reduce(lambda f1, f2: FST.compose2(f1, f2, trace=trace, relabel=False), fsts[:-1])
            return FST.compose2(comp1, fsts[-1], label=label, relabel=relabel, reverse=reverse, trace=trace)
        else:
            return FST.compose2(fsts[0], fsts[1], label=label, relabel=relabel, reverse=reverse, trace=trace)

    @staticmethod
    def compose2(fst1, fst2, label='', relabel=False, reverse=False, trace=0):
        """Compose fst1 and fst2, inserting an epsilon if necessary."""
#        print("  Composing2 fsts, reverse={}".format(reverse))
        ep_modifications = fst1._composition_ep_preprocess(fst2)
        fst = None
        if ep_modifications:
            fst1m, filt, fst2m = ep_modifications
            fst = FST.really_compose(FST.really_compose(fst1m, filt, trace=trace),
                                     fst2m, label=fst1.label + '**' + fst2.label, trace=trace)
        else:
            fst = FST.really_compose(fst1, fst2, label=label, trace=trace)
        if relabel:
            fst = fst.relabeled(label=fst.label, trace=trace)
        if trace:
            print('{} states / {} arcs in {}'.format(fst.n_states(), fst._n_arcs, fst.label))
        if reverse:
            fst._reverse = True
        return fst

    @staticmethod
    def really_compose(fst1, fst2, label='', trace=0):
        """Compose fst1 and fst2.

        Algorithm from Mohri (2005)."""
        if trace:
            print('Composing {} and {}'.format(fst1.label, fst2.label))
        # These are for checking on how many are checked
        state_pairs = 0
        arc_pairs = 0
        # Initialize the composed FST
        composition = FST(label if label else (fst1.label + '*' + fst2.label),
                          weighting = fst1.weighting() if (fst1.is_weighted() and fst2.is_weighted()) else None,
                          cascade=fst1.cascade)
        start1, start2 = fst1._get_initial_state(), fst2._get_initial_state()
        states = deque()
        states.append((start1, start2))
        if start1 == None or start2 == None:
            print('One or the other initial state is null: {}, {}, {}'.format(start1, start2, fst2))
        start_name = fst1._composition_state_name(start1, start2)
        composition.add_state(start_name)
        composition._set_initial_state(start_name)

        t0 = time.process_time()
        t = t0
        while states:
            if trace > 1:
                print('States {}'.format(states))
            state_pairs += 1
            if trace:
                t1 = time.process_time()
                if t1 - t > 60:
                    print('  Checked {} state pairs in {} minute(s)'.format(state_pairs,
                                                                            round((t1 - t0) / 60.0, 2)))
                    t = t1
#            if trace and state_pairs % 10000 == 0:
#                print('  Checked', state_pairs, 'state pairs', arc_pairs, 'arc pairs')
            state_pair = states.pop()
            state1, state2 = state_pair[0], state_pair[1]
            state_name = fst1._composition_state_name(state1, state2)
            composed_weight = True
            if fst1.is_final(state1) and fst2.is_final(state2):
                # Final state
                if trace > 1:
                    print(' Both states are final')
                composition.set_final(state_name)
                if fst1.is_weighted() and fst2.is_weighted():
                    fw = None
                    fw1, fw2 = fst1._final_weight.get(state1), fst2._final_weight.get(state2)
                    if fw1:
                        if fw2:    fw = fst1.weighting().multiply(fw1, fw2)
                        else:      fw = fw1
                    elif fw2:      fw = fw2
                    composition.set_final_weight(state_name, fw)
                    # What about finalizing string??
            for arc1 in fst1.outgoing(state1):
                in1 = fst1.in_string(arc1)
                out1 = fst1.out_string(arc1)
                dst1 = fst1.dst(arc1)
                for arc2 in fst2.outgoing(state2):
                    arc_pairs += 1
                    in2 = fst2.in_string(arc2)
                    out2 = fst2.out_string(arc2)
                    if trace > 1:
                        print(' arc1 {}: in {}, out {}; arc2 {}: in {} out {}'.format(arc1, in1, out1,
                                                                                      arc2, in2, out2))
                    comp_in_out_strings = fst1._composition_arc_match(fst2, in1, out1, in2, out2, trace=trace)
                    if comp_in_out_strings:
                        if trace > 1:
                            print(' ARC MATCH {}'.format(comp_in_out_strings))
                        if fst1.is_weighted():
                            weight1, weight2 = fst1.arc_weight(arc1), fst2.arc_weight(arc2)
                            composed_weight = fst1.weighting().multiply(weight1, weight2)
                            if trace > 1 and (weight1 != TOPFSS or weight2 != TOPFSS):
                                print(' Weights {} {} composed arc wt {}'.format(weight1, weight2, composed_weight))
                        if composed_weight:
                            # The in_ and out_strings for the composition if there's a match
                            comp_in, comp_out = comp_in_out_strings
#                            if trace > 1:
#                                print('Match, in', comp_in, 'out', comp_out)
                            dst2 = fst2.dst(arc2)
                            # Possible new state
                            next_state_pair = (dst1, dst2)
                            next_state_name = fst1._composition_state_name(dst1, dst2)
                            if not composition.has_state(next_state_name):
                                if trace > 1:
                                    print(' Created new state {}'.format(next_state_name))
                                # It is new; add it to the composed FST and to the queue
                                composition.add_state(next_state_name)
                                states.append(next_state_pair)
                            # Add the new arc to arc list if it's not already there
                            if composition.state_has_inout(state_name, next_state_name, comp_in, comp_out):
                                if trace > 1:
                                    print('State pair {} / {} already has arc with strings {}:{}'.format(state_name,
                                                                                                         next_state_name,
                                                                                                         comp_in,
                                                                                                         comp_out))
                            else:
                                if trace > 1:
                                    print(' Joining {} to {} with arc {}:{}'.format(state_name, next_state_name,
                                                                                    comp_in, comp_out))
                                composition.add_arc(state_name, next_state_name, comp_in, comp_out,
                                                    weight=composed_weight if fst1.is_weighted() else None)

        # Get rid of blind alleys
        composition.trim(composition.label, trace=trace)
        return composition

    def _composition_state_name(self, state1, state2):
        """A name for a state in the composition of two FSTs."""
        if isinstance(state1, tuple):
            state1 = '|'.join(state1)
        if isinstance(state2, tuple):
            state1 = '|'.join(state2)
        if isinstance(state1, int):
            state1 = str(state1)
        if isinstance(state2, int):
            state2 = str(state2)
        return state1 + '|' + state2

    def _composition_ep_preprocess(self, fst2):
        """Make modifications in this and another FST and create the epsilon filter if appropriate.

        Returns mutated copies if it makes any changes."""
        # See whether there are any output epsilons in self or input epsilons in fst2
        out_ep1 = self._any_ep(False)
        in_ep2 = fst2._any_ep(True)
        filt = None
        if not out_ep1 and not in_ep2:
            return None
        else:
            # Make copies to mutate
            fst1 = self.copy(del_suffix(self.label, '.') + '%')
            fst2 = fst2.copy(del_suffix(fst2.label, '.') + '%')
            if in_ep2:
                # Copy fst2 and change the names of its epsilon in_strings to ep1
                fst2._replace_ep('ep1', True)
                # Add epsilon loops to fst1 states
                fst1._add_ep_loops('ep1', False)
                if out_ep1:
                    # Change the names of fst1's epsilon out_strings to ep2
                    fst1._replace_ep('ep2', False)
                    # Add epsilon loops to fst2 states
                    fst2._add_ep_loops('ep2', True)
                    filt = FST.composition_ep_filter(weighting=self.weighting(), cascade=self.cascade)
                else:
                    filt = FST.composition_ep_filter(weighting=self.weighting(), full=False, cascade=self.cascade)
            else:
                fst1._replace_ep('ep1', False)
                # Add epsilon loops to fst1 states
                fst2._add_ep_loops('ep1', True)
                filt = FST.composition_ep_filter(weighting=self.weighting(), full=False, cascade=self.cascade)

        return fst1, filt, fst2

    @staticmethod
    def composition_ep_filter(weighting=None, full=True, cascade=None):
        """Make an intermediate filter to handle epsilons during composition."""
        label = 'cfilt' if full else 'cfilt0'
        if cascade:
            filt = cascade.get(label)
            if filt:
                return filt
        # Get the FST string from CFILT dict
        fst_string = CFILT[label]
        return FST.parse(label, fst_string, weighting=weighting, cascade=cascade)

    def _composition_arc_match(self, fst2, in1, out1, in2, out2, trace=0):
        """If the arc labels match, return the right fst2 (in_string, out_string)."""
        if self._label_unknown(out1):
            if trace > 2:
                print('out1 is ?')
            if fst2._label_unknown(in2):
                if trace > 2:
                    print('in2 is ?')
                # Both inside labels are UNKNOWN
                return in1, out2
            elif self._composition_unknown_match(in2):
                print('? matches {}'.format(in2))
                if self._label_unknown(in1):
                    print('in1 is ?')
                    # If both in_ and out_strings in self are UNKNOWN, pass on in2, out2
                    return in2, out2
                else:
                    return in1, out2
        elif fst2._label_unknown(in2):  # And out1 is not UNKNOWN
            if trace > 2:
                print('in2 is ?')
            if fst2._composition_unknown_match(out1):
                if trace > 2:
                    print('{} matches ?'.format(out1))
                if fst2._label_unknown(out2):
                    if trace > 2:
                        print('out2 is ?')
                    # If both in_ and out_strings in fst2 are UNKNOWN, pass on in1, out1
                    return in1, out1
        else:
            # ...
            stringset1 = self.stringset(out1)
            stringset2 = fst2.stringset(in2)
            if trace > 2 and (stringset1 or stringset2):
                print(' SS: out1 {}'.format(stringset1 or out1))
                print(' SS: in2 {}'.format(stringset2 or in2))
            if stringset1 and stringset2:
                intersection = self.stringset_intersection(ss_label1=out1, ss_label2=in2,
                                                           ss1=stringset1, ss2=stringset2)
                if intersection:
                    return intersection, intersection
            elif stringset1:
                if in2 == '' or in2 in stringset1:
                    return in2, out2
            elif stringset2:
                if out1 == '' or out1 in stringset2:
                    return in1, out1
            elif out1 == in2:
                return in1, out2

    def _composition_unknown_match(self, other_string):
        """Does the UNKNOWN symbol match a string in another FST?

        Epsilon or a character not in self's sigma matches."""
        sset = self.stringset(other_string)
        if sset:
            # True if none of the elements in the string set is in sigma
            return sset.intersection(self.sigma()) == set()
        else:
            return other_string == '' or other_string not in self.sigma()

    def _replace_ep(self, new_label, input_side = True):
        """Replace the epsilons on input (output) sides of arcs with new_label."""
        for arc in self.arcs():
            if input_side:
                if self.in_string(arc) == '':
                    self._in_string[arc] = new_label
            elif self.out_string(arc) == '':
                self._out_string[arc] = new_label
        self._sigma.add(new_label)

    def _any_ep(self, input_side = True):
        """Are there any epsilons on the input(outside) side of the arcs?"""
        for arc in self.arcs():
            if input_side:
                if self.in_string(arc) == '':
                    return True
            elif self.out_string(arc) == '':
                return True
        return False

    def _add_ep_loops(self, ep_label, label_input = True):
        """Add a looping arc to each state, either [ep_label:] or [:ep_label]."""
        for state in self._incoming.keys():
            in_string = ep_label if label_input else ''
            out_string = '' if label_input else ep_label
            self.add_arc(state, state, in_string, out_string)

    ## CONCATENATION, INSERTION

    def insert(self, insertion, src, dst, weight=None, mult_dsts=False):
        """Insert the FST insertion between src and dst states.

        mult_dsts=True means that different destinations are specified for each
        final state in insertion."""
        no_weight = self.no_weight(weight)
        ins_start = insertion._get_initial_state()
        single_final = len(insertion._get_final_states()) == 1
        ins_label = insertion.label
        if ins_label in self._inserted:
            self._inserted[ins_label] += 1
        else:
            self._inserted[ins_label] = 1
#        print("** Insertion {} with weight {}, single final? {}".format(insertion, weight.__repr__(), single_final))
        # Copy the stringsets of insertion into those in self
        for key, value in insertion._stringsets.items():
            if key not in self._stringsets:
                self.add_stringset(key, value)
        # Make the src and dst states if they don't already exist
        if not self.has_state(src):
            self.add_state(src)
        if dst and not self.has_state(dst):
            self.add_state(dst)
        state_pairs = [(src, ins_start)]
        while state_pairs:
            state_pair = state_pairs.pop()
            state = state_pair[0]
            ins_state = state_pair[1]
            if insertion.is_final(ins_state):
                if mult_dsts:
                    dst = insertion._final_dst[ins_state]
                    if not self.has_state(dst):
                        self.add_state(dst)
                # There's more than one final state, so connect each to dst
                ins_final_weight = insertion.final_weight(ins_state)
                final_weight = self.weighting().multiply(weight, ins_final_weight if ins_final_weight else self.default_weight())
#                print('** Final arc from {0} to {1}'.format(state, dst))
                self.add_arc(state, dst, '', '', weight=final_weight)
            for arc in insertion.outgoing(ins_state):
                arc_dst = insertion.dst(arc)
                if insertion.is_final(arc_dst) and single_final:
                    if mult_dsts:
                        new_arc_dst = insertion._final_dst[arc_dst]
                        if not self.has_state(new_arc_dst):
                            self.add_state(new_arc_dst)
                    else:
                        new_arc_dst = dst
                    arc_weight = insertion.arc_weight(arc) if no_weight and insertion.is_weighted() else weight
                    if insertion.is_weighted() and not no_weight and not self.no_weight(insertion.arc_weight(arc)):
                        raise ValueError('Weights on both final insertion arc %s and superarc %s' %
                                         (ins_state+'->'+arc_dst, src+'->'+dst))
                else:
                    # arc_dst might be an int (if its fst has been relabeled), so it needs to be cast to a str
                    new_arc_dst = ins_label + str(self._inserted[ins_label]) + '_' + str(arc_dst)
                    arc_weight = insertion.arc_weight(arc) if insertion.is_weighted() else None
                    if not self.has_state(new_arc_dst):
                        self.add_state(new_arc_dst)
                        state_pairs.append((new_arc_dst, arc_dst))
#                print('** Arc from {0} to {1}; in: {2}, out: {3}'.format(state, new_arc_dst, insertion.in_string(arc),
#                                                                       insertion.out_string(arc)))
                self.add_arc(state, new_arc_dst, insertion.in_string(arc), insertion.out_string(arc),
                             weight=arc_weight)

    #////////////////////////////////////////////////////////////
    #{ Helper Functions
    #////////////////////////////////////////////////////////////

    def has_arc(self, source, dest, in_string, out_string):
        """
        Does source have an outgoing arc to dest with in_string and out_string?
        """
        for arc in self.outgoing(source):
            if self.in_string(arc) == in_string and self.out_string(arc) == out_string \
                    and arc in self.incoming(dest):
                return True
            return False

    def _pick_label(self, label, typ, used_labels):
        """
        Helper function for L{add_state} and C{add_arc} that chooses a
        label for a new state or arc.
        """
        if label is not None and label in used_labels:
            raise ValueError("%s with label %r already exists" %
                             (typ, label))
        # If no label was specified, pick one.
        if label is not None:
            return label
        else:
            label = 1
            while '%s%d' % (typ[0], label) in used_labels: label += 1
            return '%s%d' % (typ[0], label)
