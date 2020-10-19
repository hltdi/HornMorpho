"""
This file is part of HornMorpho, which is part of the PLoGS project.

    <http://homes.soic.indiana.edu/gasser/plogs.html>

    Copyleft 2011, 2012, 2013, 2014, 2016, 2018, 2019, 2020.
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

Author: Michael Gasser <gasser@indiana.edu>

Language objects, with support mainly for morphology (separate
Morphology objects defined in morphology.py).

-- 2011-07-18
   Languages now created from data in language file:
   Language.make(abbrev)
-- 2013-02
   Multiling, TraState, TraArc created: for phrase translation FSTs.
-- 2014-06
   - Suffix stripping before transduction in analysis.
   - Accent and deaccent dictionaries for use in affix stripping to
     fix stems left after stripping.
   - new_anals dictionary to store new analyses for caching.
   - cache dictionary loaded when language is loaded.
   - cached forms used in anal_word()
   - (root, FSSet) separated into lists of (root, FS) with sep_anals
     option (required during anal_word()).
-- 2018-03
   - Separated from L3Morpho.
   - Separate cache files for analysis and segmentation (later also
     for phonological cases?).
"""

import os, sys, re, copy, itertools

LANGUAGE_DIR = os.path.join(os.path.dirname(__file__), os.path.pardir, 'languages')

from .morphology import *
from .anal import *
from .utils import some, segment
from .rule import *
from .um import *
from .ees import *

## Regex for extracting root from segmentation string
SEG_ROOT_RE = re.compile(r".*{(.+)}.*")

## Regexes for parsing language data
# Language name
LG_NAME_RE = re.compile(r'\s*n.*?:\s*(.*)')
# Backup language abbreviation
# l...:
BACKUP_RE = re.compile(r'\s*l.*?:\s*(.*)')
## preprocessing function
#PREPROC_RE = re.compile(r'\s*pre*?:\s*(.*)')
# Segments (characters)
# seg...:
SEG_RE = re.compile(r'\s*seg.*?:\s*(.*)')
# Accent dictionary
# accent:
ACC_RE = re.compile(r'\s*accent:\s*(.*)')
# Deaccent dictionary
# deaccent:
DEACC_RE = re.compile(r'\s*deaccent:\s*(.*)')
# Punctuation
# pun...:
PUNC_RE = re.compile(r'\s*pun.*?:\s*(.*)')
# Part of speech categories
# pos:
# pos: v verbo
POS_RE = re.compile(r'\s*pos:\s*(.*)\s+(.*)')
#POS_RE = re.compile(r'\s*pos:\s*(.*)')
# Feature abbreviations
# ab...:
ABBREV_RE = re.compile(r'\s*ab.*?:\s*(.*)')
# cod...:
CODE_RE = re.compile(r'\s*cod.*?:\s*(.*)')
# Term translations
# tr...:
TRANS_RE = re.compile(r'\s*tr.*?:\s*(.*)')
# Beginning of feature-value list
FEATS_RE = re.compile(r'\s*feat.*?:\s*(.*)')
# Feature-value pair
FV_RE = re.compile(r'\s*(.*?)\s*=\s*(.*)')
# FV combinations, could be preceded by ! (= priority)
FVS_RE = re.compile(r'([!]*)\s*([^!]*)')
# Feature group: {f1, f2,...} (v1, v2, ...): groupname = groupvalue
FEAT_GROUP_RE = re.compile(r"\{(.+)\}\s*\((.+)\):\s*(.*)\s+([+=])\s+(.+)")
# Abbrev, with prefixes, and full name
ABBREV_NAME_RE = re.compile(r'([*%]*?)([^*%()]*?)\s*\((.*)\)\s*(\[.*\])?')
NAME_RE = re.compile(r'([*%]*)([^*%\[\]]*)\s*(\[.*\])?')
# Feature to be recorded in anal output; new 2015.03.10
# xf: g gender
# xf~: VOS voseo
EXPL_FEAT_RE = re.compile(r'\s*xf(.*):\s*(.*)\s*=\s*(.*)')
# Preprocessing: replace characters in first list with last char
# clean: â, ä = ã
CLEAN_RE = re.compile(r'\s*cle.*?:\s*(.*)\s*=\s*(.*)')
# Pre- and post-processing (only works for Geez script now)
PREPROC_RE = re.compile(r'\s*preproc.*?:\s*(.*)')
POSTPROC_RE = re.compile(r'\s*postproc.*?:\s*(.*)')
PROCROOT_RE = re.compile(r'\s*procroot.*?:\s*(.*)')
POSTPOSTPROC_RE = re.compile(r'\s*postpostproc.*?:\s*(.*)')
GEMINATION_RE = re.compile(r'\s*gem.*?:\s*.*')

## Regex for checking for non-ascii characters
ASCII_RE = re.compile(r'[a-zA-Z]')

class Language:
    '''A single Language, currently only handling morphology.'''

    T = TDict()

    morphsep = '-'

    def __init__(self, label='', abbrev='', backup='',
                 # Preprocessing for analysis
                 preproc=None, procroot=None,
                 # Post-processing for generation
                 postproc=None, postpostproc=None,
                 seg_units=None, read_cache=False,
                 # Function that converts segmented word back to a word string
                 seg2string=None,
                 # list of grammatical features to be combined with roots for statistics,
                 # e.g., voice and aspect for Amharic verb roots (assume there's only
                 # list)
                 stat_root_feats=None,
                 # list of lists of grammatical features for statistics, e.g.,
                 # [poss, expl] for Amharic (whether is explicitly possessive)
                 stat_feats=None,
                 # Whether gemination is indicated in EES language
                 output_gemination=False,
                 rules=None,
                 citation_separate=True):
#                 msgs=None, trans=None):
        """
        Set some basic language-specific attributes.

        @param preproc            Pre-process input to analysis, for example,
                                  to convert non-roman to roman characters
        @param procroot           Pre-process roots
        @param postproc           Post-process output of generation, for
                                  example, to convert roman to non-roman characters
        @param seg_units          Segmentation units (graphemes)
        @param citation_separate  Whether citation form of words is separate from roots
#       @param msgs               Messages in the languages (or some other)
#       @param trans              Translations of terms from english to this language
        """
        self.label = label
        self.abbrev = abbrev or label[:3]
        # additional abbreviations for language
        self.codes = []
        # Backup language for term translation, etc.
        self.backup = backup
        self.morphology = None
        self.preproc = preproc
        self.procroot = procroot
        self.postproc = postproc
        self.postpostproc = postpostproc
        self.output_gemination = output_gemination
        self.seg2string = seg2string
        self.seg_units = seg_units or []
        self.stat_root_feats = stat_root_feats or []
        self.stat_feats = stat_feats or []
        # If any, dictionaries associating characters with their "accented" or
        # "unaccented" forms
        self.accent = None
        self.deaccent = None
        self.citation_separate = citation_separate
#        self.msgs = msgs or {}
#        self.trans = trans or {}
        self.directory = self.get_dir()
        self.tlanguages = [abbrev]
        if self.backup:
            self.tlanguages.append(self.backup)
        self.rules = rules or {}
        # Whether the language data and FSTs have been loaded
        self.load_attempted = False
        # Whether the morphology has been loaded
        self.morpho_loaded = False
        self.cached = {}
        # Cached entries read in when language is loaded
        if read_cache:
            self.read_cache()
        # New analyses since language loaded
        # each entry a wordform and list of (root, FS) analyses
        self.new_anals = {}
        # If available, create a converter between HM and UM features
        self.um = UniMorph(self)
        # Mapping from internal phone repr to standard repr
        self.phone_map = {}
        self.read_phon_file()

    def __str__(self):
        return self.label or self.abbrev

    def __repr__(self):
        return self.label or self.abbrev

    def get_dir(self):
        """Where data for this language is kept."""
        return os.path.join(LANGUAGE_DIR, self.abbrev)

    def get_data_file(self):
        """Data file for language."""
        return os.path.join(self.get_dir(), self.abbrev + '.lg')

    # Directory for translation data

    def get_trans_dir(self):
        """File with cached analyses."""
        return os.path.join(self.get_dir(), 'trans')

    def get_lex_dir(self):
        return os.path.join(self.get_dir(), 'lex')

    def get_valency_file(self, pos='v'):
        return os.path.join(self.get_lex_dir(), pos + '.val')

    def get_phon_file(self):
        return os.path.join(self.get_dir(), self.abbrev + '.ph')

#    def get_stat_dir(self):
#        """Statistics directory: root and feature frequencies
#        for disambiguation."""
#        return os.path.join(self.directory, 'stat')

    ## CACHING

    def get_cache_dir(self):
        """File with cached analyses."""
        return os.path.join(self.get_dir(), 'cache')

    def get_cache_file(self, segment=False):
        d = self.get_cache_dir()
        if segment:
            name = 'seg'
        else:
            name = 'anal'
        return os.path.join(d, name + '.cch')

    def add_new_anal(self, word, anals):
        self.new_anals[word] = anals

    def write_cache(self, segment=False):
        """Write a dictionary of cached entries to a cache file."""
        if self.new_anals:
            # Only attempt to cache analyses if there are new ones.
            file = self.get_cache_file(segment=segment)
            with open(file, 'a', encoding='utf8') as out:
                for word, analyses in self.new_anals.items():
                    # analyses is a list of root, fs pairs
                    if len(analyses) == 1 and analyses[0][0] == word and not analyses[0][1]:
                        # The word is unanalyzed
                        print("{}".format(word), file=out)
                    else:
                        anals = ["{}:{}".format(r, f.__repr__() if f else '') for r, f in analyses]
                        anals = ';'.join(anals)
                        print("{} || {}".format(word, anals), file=out)
        # Empty new_anals in case we want to add things later
        self.new_anals.clear()

    def read_cache(self, segment=False):
        """Read cached entries into self.cached from a file."""
        file = self.get_cache_file(segment=segment)
        try:
            with open(file, encoding='utf8') as f:
#                print("Reading cached words")
                for line in f:
                    if '||' not in line:
                        self.cached[line.strip()] = []
                        continue
                    split_line = line.strip().split(" || ")
                    word, analyses = split_line
                    analyses = analyses.split(';')
                    analyses = [a.split(':') for a in analyses]
                    analyses = [(r, FeatStruct(a, freeze=True) if a else None) for r, a in analyses]
                    self.cached[word] = analyses
        except IOError:
            pass
#            print('No such cache file as {}'.format(file))

    def get_cached_anal(self, word):
        """Returns cached analyses for word if any."""
        if word in self.cached:
            entry = self.cached[word]
            if not entry:
                return [(word, None)]
            else:
                return entry
        if word in self.new_anals:
            entry = self.new_anals[word]
            if not entry:
                return [(word, None)]
            else:
                return entry
        return False

    @staticmethod
    def make(name, abbrev, load_morph=False,
             segment=False, phon=False, simplified=False,
             guess=True, poss=None,
             ees=False,
             verbose=False):
        """Create a language using data in the language data file."""
        if ees:
            lang = EESLanguage(abbrev=abbrev)
        else:
            lang = Language(abbrev=abbrev)
        # Load data from language file
        loaded = lang.load_data(load_morph=load_morph,
                                segment=segment, phon=phon, simplified=simplified,
                                guess=guess, poss=poss, verbose=verbose)
        if not loaded:
            # Loading data failed somewhere; abort
            return
        return lang

    def load_data(self, load_morph=False,
                  segment=False, phon=False, guess=True, simplified=False,
                  poss=None, verbose=False):
        if self.load_attempted:
            return
        self.load_attempted = True
        filename = self.get_data_file()
        if not os.path.exists(filename):
            if verbose:
                print(Language.T.tformat('(No language data file for {} at {})', [self, filename], self.tlanguages))
        else:
            if verbose:
                print(Language.T.tformat('Loading language data from {}', [filename], self.tlanguages))
            with open(filename, encoding='utf-8') as stream:
                data = stream.read()
                self.parse(data, poss=poss, verbose=verbose)
        if load_morph:
            if not self.load_morpho(segment=segment, ortho=True, phon=phon,
                                    guess=guess, simplified=simplified,
                                    verbose=verbose):
                # There is no FST of the desired type
                return False
        # Create a default FS for each POS
        for posmorph in self.morphology.values():
            if posmorph.defaultFS:
                if isinstance(posmorph.defaultFS, str):
                    posmorph.defaultFS = FeatStruct(posmorph.defaultFS)
            else:
                posmorph.defaultFS = posmorph.make_default_fs()
        return True

    def parse(self, data, poss=None, verbose=False):

        """Read in language data from a file."""
        if verbose:
            print('Parsing data for', self)

        lines = data.split('\n')[::-1]

        postproc = ''
        preproc = ''

        seg = []
        punc = []
        abbrev = {}
        fv_abbrev = {}
        trans = {}
        fv_dependencies = {}
        fv_priorities = {}
        fullpos = {}

        excl = {}
        feats = {}
        lex_feats = {}
        true_explicit = {}
        explicit = {}

        feature_groups = {}

        chars = ''

        current = None

#        current_pos = ''
        current_feats = []
        current_lex_feats = []
        current_excl = []
        current_abbrev = {}
        current_fv_abbrev = []
        current_fv_priority = []

        complex_feat = False
        current_feat = None
        current_value_string = ''
        complex_fvs = []

        current_explicit = []
        current_true_explicit = []

        current_feature_groups = {}

        while lines:

            line = lines.pop().split('#')[0].strip() # strip comments

            # Ignore empty lines
            if not line: continue

            # Beginning of segmentation units
            m = SEG_RE.match(line)
            if m:
                current = 'seg'
                seg = m.group(1).split()
                continue

            m = ACC_RE.match(line)
            if m:
                acc = m.group(1).split(',')
                self.accent = {}
                for chars in acc:
                    u, a = chars.split(':')
                    self.accent[u.strip()] = a.strip()
                continue

            m = DEACC_RE.match(line)
            if m:
                deacc = m.group(1).split(',')
                self.deaccent = {}
                for chars in deacc:
                    a, u = chars.split(':')
                    self.deaccent[a.strip()] = u.strip()
                continue

            m = LG_NAME_RE.match(line)
            if m:
                label = m.group(1).strip()
                self.label = label
                continue

            m = BACKUP_RE.match(line)
            if m:
                lang = m.group(1).strip()
                self.backup = lang
                self.tlanguages.append(lang)
                continue

            m = PUNC_RE.match(line)
            if m:
                current = 'punc'
                punc = m.group(1).split()
                continue

            m = TRANS_RE.match(line)
            if m:
                current = 'trans'
                w_g = m.group(1).split()
                if '=' in w_g:
                    w, g = w_g.split('=')
                    # Add to the global TDict
                    Language.T.add(w.strip(), g.strip(), self.abbrev)
#                    self.trans[w.strip()] = g.strip()
                continue

            m = PREPROC_RE.match(line)
            if m:
                preproc = m.group(1)
#                if preproc.startswith('geez'):
#                    from .geez import geez2sera
#                    self.preproc = lambda form: geez2sera(None, form, lang=self.abbrev,
#                                                          gemination='gem' in preproc)
                self.preproc = eval(preproc)
                continue

            m = PROCROOT_RE.match(line)
            if m:
                procroot = m.group(1)
                if procroot.startswith('def'):
                    self.procroot = Language.dflt_procroot
                else:
                    self.procroot = eval(procroot)
                continue

            m = POSTPROC_RE.match(line)
            if m:
                postproc = m.group(1)
#                if postproc.startswith('geez'):
#                    from .geez import sera2geez
#                    self.postproc = lambda form: sera2geez(None, form, lang=self.abbrev,
#                                                           gemination='gem' in postproc)
                self.postproc = eval(postproc)
                continue

            m = POSTPOSTPROC_RE.match(line)
            if m:
                postpostproc = m.group(1)
                self.postpostproc = eval(postpostproc)
                continue

            m = GEMINATION_RE.match(line)
            if m:
                self.output_gemination = True
                continue

            m = CLEAN_RE.match(line)
            if m:
                # Ignore in HornMorpho
                continue

            m = CODE_RE.match(line)
            if m:
                code = m.group(1)
                self.codes.append(code.strip())
                continue

            m = FEATS_RE.match(line)
            if m:
                current = 'feats'
                continue

            if current == 'feats':
                m = POS_RE.match(line)
                if m:
                    pos, fullp = m.groups()
                    pos = pos.strip()
                    fullp = fullp.strip()
#                    self.pos.append(pos)
                    # Differs in ParaMorfo below
                    # Start a set of features for a new part-of-speech category
#                    pos = m.group(1).strip()
                    current_feats = []
                    current_lex_feats = []
                    current_excl = []
                    current_abbrev = {}
                    current_fv_abbrev = []
                    current_fv_dependencies = {}
                    current_fv_priority = []
                    current_explicit = []
                    current_true_explicit = []
                    current_feature_groups = {}
                    lex_feats[pos] = current_lex_feats
                    feats[pos] = current_feats
                    excl[pos] = current_excl
                    abbrev[pos] = current_abbrev
                    fv_abbrev[pos] = current_fv_abbrev
                    fv_dependencies[pos] = current_fv_dependencies
                    fv_priorities[pos] = current_fv_priority
                    explicit[pos] = current_explicit
                    true_explicit[pos] = current_true_explicit
                    fullpos[pos] = fullp
                    feature_groups[pos] = current_feature_groups
                    continue

                m = ABBREV_RE.match(line)
                if m:
#                    current = 'abbrev'
                    abb_sig = m.group(1).strip()
                    if '=' in abb_sig:
                        abb, sig = abb_sig.split('=')
                        current_abbrev[abb.strip()] = sig.strip()
                    continue

                m = EXPL_FEAT_RE.match(line)
                # Feature to include in pretty output; ignore in HornMorpho
                if m:
                    opt, fshort, flong = m.groups()
                    fshort = fshort.strip()
                    opt = opt.strip()
                    current_abbrev[fshort] = flong.strip()
                    current_explicit.append(fshort)
                    if opt and opt == '~':
                        current_true_explicit.append(fshort)
                    continue

                m = FEAT_GROUP_RE.match(line)
                if m:
                    groupfeats, groupvalues, groupname, oper, groupvalue = m.groups()
                    groupfeats = tuple([f.strip() for f in groupfeats.split(',')])
                    groupvalues = [v.strip() for v in groupvalues.split(',')]
                    for i, v in enumerate(groupvalues):
                        if v.isdigit():
                            groupvalues[i] = int(v)
                        elif v == "False":
                            groupvalues[i] = False
                        elif v == "True":
                            groupvalues[i] = True
                        elif v == "None":
                            groupvalues[i] = None
                    groupvalues = tuple(groupvalues)
                    groupname = groupname.strip()
#                    print("groupfeats {}, groupname {}, gvalues {}, add {}".format(groupfeats, groupname, groupvalues, oper))
                    if groupfeats in current_feature_groups:
                        current_feature_groups[groupfeats].append((groupvalues, groupname, groupvalue, oper=='='))
                    else:
                        current_feature_groups[groupfeats] = [(groupvalues, groupname, groupvalue, oper=='=')]
                    if groupname not in current_explicit:
                        current_explicit.append(groupname)
#                    print("feature groups {}".format(current_feature_groups))
                    continue

                m = FV_RE.match(line)
                if m:
                    # A feature and value specification
                    feat, val = m.groups()
                    if '+' in feat or '-' in feat:
                        # Expansion for a set of boolean feature values
                        # See if there's a ! (=priority) prefix
                        m2 = FVS_RE.match(feat)
                        priority, fvs = m2.groups()
                        # An abbreviation for one or more boolean features with values
                        fvs = fvs.split(',')
                        fvs = [s.strip() for s in fvs]
                        fvs = [s.split('=') if '=' in s else [s[1:], (True if s[0] == '+' else False)] for s in fvs]
                        current_fv_abbrev.append((fvs, val))
                        if priority:
                            current_fv_priority.append(fvs)
                    elif '=' in val:
                        # Complex feature (with nesting)
                        complex_feat = self.proc_feat_string(feat, current_abbrev, current_excl, current_lex_feats,
                                                             current_fv_dependencies)
                        vals = val.split(';')
                        for fv2 in vals:
                            fv2 = fv2.strip()
                            if fv2:
                                m2 = FV_RE.match(fv2)
                                if m2:
                                    feat2, val2 = m2.groups()
                                    f = self.proc_feat_string(feat2, current_abbrev, current_excl, current_lex_feats,
                                                              current_fv_dependencies)
                                    v = self.proc_value_string(val2, f, current_abbrev, current_excl,
                                                               current_fv_dependencies)
                                    complex_fvs.append((f, v))
                        if len(vals) == 1:
                            current_feats.append((complex_feat, complex_fvs))
                            complex_feat = None
                            complex_fvs = []
                    else:
                        fvs = line.split(';')
                        if len(fvs) > 1:
                            # More than one feature-value pair (or continuation)
                            if not complex_feat:
                                complex_feat = current_feat
                            for fv2 in fvs:
                                fv2 = fv2.strip()
                                if fv2:
                                    m2 = FV_RE.match(fv2)
                                    if m2:
                                        # A single feature-value pair
                                        feat2, val2 = m2.groups()
                                        f = self.proc_feat_string(feat2, current_abbrev, current_excl, current_lex_feats,
                                                                  current_fv_dependencies)
                                        v = self.proc_value_string(val2, f, current_abbrev, current_excl,
                                                                   current_fv_dependencies)
                                        complex_fvs.append((f, v))
                        elif complex_feat:
                            # A single feature-value pair
                            f = self.proc_feat_string(feat, current_abbrev, current_excl, current_lex_feats,
                                                      current_fv_dependencies)
                            v = self.proc_value_string(val, f, current_abbrev, current_excl,
                                                       current_fv_dependencies)
                            complex_fvs.append((f, v))
                            current_feats.append((complex_feat, complex_fvs))
                            complex_feat = None
                            complex_fvs = []
                        else:
                            # Not a complex feature
                            current_feat = self.proc_feat_string(feat, current_abbrev, current_excl, current_lex_feats,
                                                                 current_fv_dependencies)
                            current_value_string = ''
                            val = val.strip()
                            if val:
                                # The value is on this line
                                # Split the value by |
                                vals = val.split('|')
                                vals_end = vals[-1].strip()
                                if not vals_end:
                                    # The line ends with | so the value continues
                                    current_value_string = val
                                else:
                                    v = self.proc_value_string(val, current_feat, current_abbrev, current_excl,
                                                               current_fv_dependencies)
                                    current_feats.append((current_feat, v))

                else:
                    # Just a value
                    val = line.strip()
                    current_value_string += val
                    # Split the value by | to see if it continues
                    vals = val.split('|')
                    if vals[-1].strip():
                        v = self.proc_value_string(current_value_string, current_feat, current_abbrev, current_excl,
                                                   current_fv_dependencies)
                        current_feats.append((current_feat, v))
                        current_value_string = ''

            elif current == 'seg':
                seg.extend(line.strip().split())

            elif current == 'punc':
                punc.extend(line.strip().split())

            elif current == 'pos':
                pos.extend(line.strip().split())

            elif current == 'trans':
                wd, gls = line.strip().split('=')
                # Add to the global TDict
                Language.T.add(wd.strip(), gls.strip(), self.abbrev)
#                self.trans[wd] = gls.strip()

            else:
                raise ValueError("bad line: {}".format(line))

        if punc:
            # Make punc list into a string
            punc = ''.join(punc)

        if seg:
            # Make a bracketed string of character ranges and other characters
            # to use for re
            chars = ''.join(set(''.join(seg)))
            chars = self.make_char_string(chars)
            # Make the seg_units list, [chars, char_dict], expected for transduction,
            # composition, etc.
            self.seg_units = self.make_seg_units(seg)

        if feats and not self.morphology:
            pos_args = []
            for pos in feats:
                if not poss or pos in poss:
                    # Make feature_groups into a list, sorted by length of feature matches
                    fgroups = list(feature_groups[pos].items())
                    fgroups.sort(key=lambda x: -len(x[0]))
                    pos_args.append((pos, feats[pos], lex_feats[pos], excl[pos], abbrev[pos],
                                     fv_abbrev[pos], fv_dependencies[pos], fv_priorities[pos],
                                     fgroups, fullpos[pos],
                                     explicit[pos], true_explicit[pos]))
#                    pos_args.append((pos, feats[pos], lex_feats[pos], excl[pos],
#                                     abbrev[pos], fv_abbrev[pos], fv_dependencies[pos],
#                                     fv_priorities[pos]))
            morph = Morphology(pos_morphs=pos_args,
                               punctuation=punc, characters=chars)
            self.set_morphology(morph)

    ### Phone representation conversion
    def read_phon_file(self, verbosity=0):
        """
        Read the phone representation mapping file.
        """
        path = self.get_phon_file()
        try:
            with open(path, encoding='utf8') as file:
                if verbosity:
                    print("Reading phoneme mapping")
                for line in file:
                    # Get rid of comments
                    line = line.strip().split('#')[0]
                    if not line:
                        continue
                    phones = line.split()
                    # First item is HM internal representation
                    hm = phones[0]
                    # Other are alternative standard representations
                    self.phone_map[hm] = phones[1:]
        except IOError:
            pass

    def get_vowels(self):
        """
        Find the vowels in the phone mapping.
        """
        if 'VV' not in self.phone_map:
            print("Vowel list missing from phone map!")
            return
        return self.phone_map['VV']

    def get_epen(self):
        """
        Get the epenthetic character.
        """
        if 'EE' not in self.phone_map:
            print("Epenthetic character missing from phone map!")
            return
        return self.phone_map['EE'][0]

    def epenthesis(self, phones):
        """
        Insert epenthesis character to separate consonant sequences.
        """
        if not isinstance(phones, list):
            phones = segment(phones, self.seg_units)
        nphones = len(phones)
        vowels = self.get_vowels()
        epen = self.get_epen()
        cons_seqs = []
        cons = []
        for index, phone in enumerate(phones):
            if phone not in vowels:
                if not cons:
                    cons.append(index)
                cons.append(phone)
            else:
                if len(cons) >= 4 or (len(cons) == 3 and index == 2):
                    cons_seqs.append(cons)
                cons = []
        if cons and (len(cons) >= 4 or len(cons)-1 == len(phones)):
            cons_seqs.append(cons)
#        print("Cons sequences {}".format(cons_seqs))
        if cons_seqs:
            nepens = []
            for cseq in cons_seqs:
                nepen = 0
#                print("cseq {}, type {}".format(cseq, type(cseq)))
                clen = len(cseq) - 1
                if clen == 2:
                    # Only at the beginning
                    cseq[2:2] = epen
                    nepen += 1
                elif clen == 3:
                    if cseq[2] == '_' or cseq[0] == (nphones - clen):
                        # end of word
                        cseq[3:3] = epen
                    else:
                        cseq[2:2] = epen
                    nepen += 1
                elif clen == 4 or clen == 5:
                    if cseq[2] == '_' or (cseq[1] in 'lmnrwy' and cseq[0] != 0):
                        cseq[3:3] = epen
                        nepen += 1
                        if clen == 5:
                            cseq[5:5] = epen
                            nepen += 1
                    else:
                        cseq[2:2] = epen
                        cseq[5:5] = epen
                        nepen += 2
                elif cseq[2] == '_':
                    cseq[3:3] = epen
                    cseq[5:5] = epen
                    nepen += 2
                else:
                    cseq[2:2] = epen
                    cseq[4:4] = epen
                    cseq[7:7] = epen
                    nepen += 3
                nepens.append(nepen)
#            print("nepens {}".format(nepens))
#            print("Cons sequences adjusted {}".format(cons_seqs))
            naccum = 0
            for cseq, nep in zip(cons_seqs, nepens):
                index = cseq[0]
                cseq = cseq[1:]
                clen = len(cseq) - nep
                start = index + naccum
                phones[start:start+clen] = cseq
                naccum += nep
#        print("Updated phones {}".format(phones))
        return phones

    def convert_phones(self, phones, gemination=True, epenthesis=True,
                       ipa=False):
        """
        Convert a sequence of phones (an unsegmented string)
        to an alternate phone representation.
        """
        phones = segment(phones, self.seg_units)
        if epenthesis:
            self.epenthesis(phones)
        result = []
        for phone in phones:
            if phone in self.phone_map:
                alts = self.phone_map[phone]
                if ipa:
                    alt = alts[-1]
                else:
                    alt = alts[0]
                result.append(alt)
            else:
                result.append(phone)
        if gemination and '_' in result:
            for index, seg in enumerate(result):
                if seg == '_':
                    if index == 0:
                        print("Gemination character can't be first!")
                        continue
                    result[index] = result[index-1]
        return ''.join(result)

    def convert_root(self, root, ipa=False):
        """
        Convert an HM root representation to an alternate
        conventional representation.
        """
        return self.convert_phones(root, gemination=False, epenthesis=False,
                                   ipa=ipa)

    @staticmethod
    def dflt_procroot(root, fs=None, pos=None):
        """
        Default function for pre-processing root.
        <sbr:A> =>  sbr, [cls=A]
        """
        cls = ''
        if '<' in root:
            root = root.replace('<', '').replace('>', '')
        if ':' in root:
            root, cls = root.split(':')
        if cls:
            if fs:
                # a string: [...]
                fs = "[cls={},{}]".format(cls, fs[1:-1])
            else:
                fs = "[cls={}]".format(cls)
        return root, fs

    def proc_feat_string(self, feat, abbrev_dict, excl_values,
                         lex_feats, fv_dependencies):
        prefix = ''
        depend = None
        m = ABBREV_NAME_RE.match(feat)

        if m:
            prefix, feat, name, depend = m.groups()
            abbrev_dict[feat] = name
        else:
            m = NAME_RE.match(feat)
            prefix, feat, depend = m.groups()

#        print('Prefix {}, feat {}, depend {}'.format(prefix, feat, depend))

        # * means that the feature's values are not reported in analysis output
        if '*' in prefix:
            excl_values.append(feat)
        # % means that the feature is lexical
        if '%' in prefix:
            lex_feats.append(feat)

        if depend:
            # Feature and value that this feature value depends on
            # Get rid of the []
            depend = depend[1:-1]
            # Can be a comma-separated list of features
            depends = depend.split(',')
            for index, dep in enumerate(depends):
                dep_fvs = [fvs.strip() for fvs in dep.split()]
                if dep_fvs[-1] == 'False':
                    dep_fvs[-1] = False
                elif dep_fvs[-1] == 'True':
                    dep_fvs[-1] = True
                elif dep_fvs[-1] == 'None':
                    dep_fvs[-1] = None
                depends[index] = dep_fvs
            fv_dependencies[feat] = depends

        return feat

    def proc_value_string(self, value_string, feat, abbrev_dict, excl_values, fv_dependencies):
        '''value_string is a string containing values separated by |.'''
        values = [v.strip() for v in value_string.split('|')]
        res = []
        prefix = ''
        for value in values:
            if not value:
                continue
            if value == '+-':
                res.extend([True, False])
            else:
                m = ABBREV_NAME_RE.match(value)
                if m:
                    prefix, value, name, depend = m.groups()
                    abbrev_dict[value] = name
                else:
                    m = NAME_RE.match(value)
                    prefix, value, depend = m.groups()

                value = value.strip()

                if value == 'False':
                    value = False
                elif value == 'True':
                    value = True
                elif value == 'None':
                    value = None
                elif value == '...':
#                    print('prefix {}, value {}, depend {}'.format(prefix, value, depend))
                    value = FeatStruct('[]')
                elif value.isdigit():
                    value = int(value)

                if '*' in prefix:
                    excl_values.append((feat, value))

                if depend:
                    # Feature and value that this feature value depends on
                    depend = depend[1:-1]
                    dep_fvs = [fvs.strip() for fvs in depend.split()]
                    if dep_fvs[-1] == 'False':
                        dep_fvs[-1] = False
                    elif dep_fvs[-1] == 'True':
                        dep_fvs[-1] = True
                    elif dep_fvs[-1] == 'None':
                        dep_fvs[-1] = None
                    elif dep_fvs[-1] == '...':
#                        print('prefix {}, value {}, depend {}'.format(prefix, value, depend))
                        dep_fvs[-1] = FeatStruct('[]')
                    fv_dependencies[(feat, value)] = dep_fvs

                res.append(value)
        return tuple(res)

    def make_char_string(self, chars):
        non_ascii = []
        for char in chars:
            if not ASCII_RE.match(char):
                non_ascii.append(char)
        non_ascii.sort()
        non_ascii_s = ''.join(non_ascii)
        return r'[a-zA-Z' + non_ascii_s + r']'

    def make_seg_units(self, segs):
        """Convert a list of segments to a seg_units list + dict."""
        singletons = []
        dct = {}
        for seg in segs:
            c0 = seg[0]
            if c0 in dct:
                dct[c0].append(seg)
            else:
                dct[c0] = [seg]
        for c0, segs in dct.items():
            if len(segs) == 1 and len(segs[0]) == 1:
                singletons.append(c0)
        for seg in singletons:
            del dct[seg]
        singletons.sort()
        return [singletons, dct]

#    def get_trans(self, word):
#        return self.trans.get(word, word)

    def preprocess(self, form):
        '''Preprocess a form.'''
        if self.preproc:
            return self.preproc(form)
        return form

    def postprocess(self, form):
        '''Postprocess a form.'''
        if self.postproc:
            return self.postproc(form)
        return form

    def postpostprocess(self, form):
        '''Postprocess a form that has already been postprocessed.'''
        if self.postpostproc:
            return self.postpostproc(form)
        return form

    ## Methods related to segmentation

    def seg2morphs(self, seg):
        '''Returns the morphemes in a segmentation string, and index of the root.
        USE REGEX.'''
        # separate morphemes
        morphs = seg.split(Language.morphsep)
        rootindex = -1
        for index, morph in enumerate(morphs):
            if '(' in morph:
                morph = morph.split('(')
                morph = [morph[0], '(' + morph[1]]
            else:
                morph = [morph, '']
            form = morph[0]
            if '{' in form:
                morph[0] = form[1:-1]
                rootindex = index
            morphs[index] = morph
        return morphs, rootindex

    def seg2root(self, seg):
        """Returns the root morpheme (form, features) for a segmentation string."""
        morphs = self.seg2morphs(seg)
        return morphs[0][morphs[1]]

    def segmentation2string(self, segmentation, sep='-', transortho=True, features=False):
        '''Convert a segmentation (POS, segstring, count) to a form string,
        using a language-specific function if there is one, otherwise using a default function.'''
        if self.seg2string:
            return self.seg2string(segmentation, sep=sep, transortho=transortho, features=features)
        else:
            morphs = [m[0] for m in self.seg2morphs(segmentation[1])]
            # This ignores whatever alternation rules might operate at boundaries
            return sep.join(morphs)

    def preprocess_file(self, filein, fileout):
        '''Preprocess forms in filein, writing them to fileout.'''
#        fin = codecs.open(filein, 'r', 'utf-8')
#        fout = codecs.open(fileout, 'w', 'utf-8')
        fin = open(filein, 'r', encoding='utf-8')
        fout = open(fileout, 'w', encoding='utf-8')
        for line in fin:
            fout.write(str(self.preproc(line), 'utf-8'))
        fin.close()
        fout.close()

    def set_morphology(self, morphology, verbosity=0):
        '''Assign the Morphology object for this Language.'''
        self.morphology = morphology
        morphology.language = self
        for pos in morphology.values():
            pos.language = self
        morphology.directory = self.directory
        morphology.seg_units = self.seg_units
        morphology.phon_fst = morphology.restore_fst('phon', create_networks=False)

    def load_morpho(self, fsts=None, ortho=True, phon=False, simplified=False,
                    segment=False, recreate=False, guess=True, verbose=False):
        """Load words and FSTs for morphological analysis and generation."""
        fsts = fsts or self.morphology.pos
        opt_string = ''
        if segment:
            opt_string = 'segmentation'
        elif phon:
            opt_string = 'phonetic'
        else:
            opt_string = 'analysis/generation'
        if not self.has_cas(generate=phon, guess=False, phon=phon,
                            segment=segment, simplified=simplified):
            print('No {} FST available for {}!'.format(opt_string, self))
            return False
        msg_string = Language.T.tformat('Loading FSTs for {0}{1} ...',
                                        [self, ' (' + opt_string + ')' if opt_string else ''],
                                        self.tlanguages)
        print(msg_string)
        # In any case, assume the root frequencies will be needed?
        self.morphology.set_root_freqs()
        self.morphology.set_feat_freqs()
        if ortho:
            # Load unanalyzed words
            self.morphology.set_words(ortho=True)
            self.morphology.set_suffixes(verbose=verbose)
        if phon:
            # Load unanalyzed words
            self.morphology.set_words(ortho=False)
            self.morphology.set_suffixes(verbose=verbose)
        for pos in fsts:
            # Load pre-analyzed words if any
            if ortho:
                self.morphology[pos].make_generated()
            # Load phonetic->orthographic dictionary if file exists
            if ortho:
                self.morphology[pos].set_ortho2phon()
            # Load lexical anal and gen FSTs (no gen if segmenting)
            if ortho:
                self.morphology[pos].load_fst(gen=not segment,
                                              create_casc=False,
                                              simplified=simplified,
                                              phon=False, segment=segment,
                                              recreate=recreate, verbose=verbose)
            if phon or (ortho and not segment):
                self.morphology[pos].load_fst(gen=True,
                                              create_casc=False,
                                              simplified=simplified,
                                              phon=True, segment=segment,
                                              recreate=recreate, verbose=verbose)
            # Load guesser anal and gen FSTs
            if not segment and guess:
                if ortho:
                    self.morphology[pos].load_fst(gen=True, guess=True, phon=False,
                                                  segment=segment,
                                                  create_casc=False,
                                                  simplified=simplified,
                                                  recreate=recreate, verbose=verbose)
                if phon:
                    self.morphology[pos].load_fst(gen=True, guess=True, phon=True, segment=segment,
                                                  create_casc=False,
                                                  simplified=simplified,
                                                  recreate=recreate, verbose=verbose)
            # Load statistics for generation
            self.morphology[pos].set_root_freqs()
            self.morphology[pos].set_feat_freqs()

        self.morpho_loaded = True
        return True

    def get_fsts(self, generate=False, phon=False,
                 simplified=False, segment=False):
        '''Return all analysis FSTs (for different POSs) satisfying phon and segment contraints.'''
        fsts = []
        for pos in self.morphology.pos:
            if phon:
                fst = self.morphology[pos].get_fst(generate=True, phon=True)
            else:
                fst = self.morphology[pos].get_fst(generate=generate, segment=segment)
            if fst:
                fsts.append(fst)
        return fsts

    def has_cas(self, generate=False, guess=False,
                simplified=False, phon=False, segment=False):
        """Is there at least one cascade file for the given FST features?"""
        for pos in self.morphology.pos:
            if self.morphology[pos].has_cas(generate=generate, simplified=simplified,
                                            guess=guess, phon=phon, segment=segment):
                return True
        return False

    ### Analyze words or sentences

    def anal_word(self, word, fsts=None, guess=True, only_guess=False,
                  phon=False, segment=False, init_weight=None,
                  root=True, stem=True, citation=True, gram=True,
                  um=True, gloss=True,
                  get_all=True, to_dict=False, preproc=False, postproc=False,
                  cache=False, no_anal=None, string=False, print_out=False,
                  display_feats=None, rank=True, report_freq=True, nbest=100,
                  only_anal=False):
        '''
        Analyze a single word, trying all existing POSs, both
        lexical and guesser FSTs.

        [ [POS, {root|citation}, FSSet] ... ]
        '''
        # Before anything else, check to see if the word is in the list of words that
        # have failed to be analyzed
        if no_anal != None and word in no_anal:
            return None
        # Whether the analyses are found in the cache
        found = False
        preproc = preproc and self.preproc
        postproc = postproc and self.postproc
        citation = citation and self.citation_separate
        analyses = []
        to_cache = [] if cache else None
        fsts = fsts or self.morphology.pos
        if preproc:
            # Convert to roman, for example
            form = self.preproc(word)
        else:
            form = word
        # See if the word is unanalyzable ...
        unal_word = self.morphology.is_word(form)
        # unal_word is a form, POS pair
        if unal_word:
            # Don't cache these
            cache = False
            if only_anal:
                return []
            a = self.simp_anal(unal_word, postproc=postproc, segment=segment)
            analyses.append(a)

        # See if the word is cached (but only if there is no init_weight)
        if cache:
            cached = self.get_cached_anal(word)
            if cached:
                if not init_weight:
                    found = True
                    analyses = self.proc_anal(word, cached, None,
                                              show_root=root, citation=citation, stem=stem,
                                              segment=segment, guess=False, postproc=postproc, gram=gram, freq=rank or report_freq)
        # Is word already analyzed, without any root/stem (for example, there is a POS and/or a translation)
        if not analyses and form in self.morphology.analyzed:
            if only_anal:
                return []
            # Assume these are the *only* analyses
            get_all = False
            a = self.proc_anal_noroot(form, self.morphology.get_analyzed(form), segment=segment)
            if cache:
                to_cache.extend(a)
            analyses.extend(a)
        else:
            # Try stripping off suffixes
            suff_anal = self.morphology.strip_suffixes(form)
            if suff_anal:
                if cache:
                    to_cache.extend(suff_anal)
                for stem, fs in suff_anal:
                    cat = fs.get('pos', '')
                    analyses.append((cat, stem, stem, fs, 100))
        if not analyses or (not found and get_all):
            if not only_guess:
                for pos in fsts:
                    #... or already analyzed within a particular POS
                    preanal = self.morphology[pos].get_analyzed(form, sep_anals=True)
                    if preanal:
                        if cache:
                            to_cache.extend(preanal)
                        analyses.extend(self.proc_anal(form, preanal, pos,
                                                       show_root=root, citation=citation, stem=stem,
                                                       segment=segment, guess=False,
                                                       postproc=postproc, gram=gram,
                                                       freq=rank or report_freq))
                    else:
                        # We have to really analyze it; first try lexical FSTs for each POS
                        analysis = self.morphology[pos].anal(form, init_weight=init_weight,
                                                             phon=phon, segment=segment,
                                                             to_dict=to_dict, sep_anals=True)
                        if analysis:
                            if cache:
                                to_cache.extend(analysis)
                            # Keep trying if an analysis is found
                            analyses.extend(self.proc_anal(form, analysis, pos,
                                                           show_root=root, citation=citation and not segment,
                                                           segment=segment,
                                                           stem=stem,
                                                           guess=False, postproc=postproc, gram=gram,
                                                           freq=rank or report_freq))
        # If nothing has been found, try guesser FSTs for each POS
        if not analyses and guess:
            # Accumulate results from all guessers
            for pos in fsts:
                analysis = self.morphology[pos].anal(form, guess=True, init_weight=init_weight,
                                                     phon=phon, segment=segment,
                                                     to_dict=to_dict, sep_anals=True)
                if analysis:
                    if cache:
                        to_cache.extend(analysis)
                    analyses.extend(self.proc_anal(form, analysis, pos,
                                                   show_root=root,
                                                   citation=citation and not segment,
                                                   segment=segment,
                                                   guess=True, gram=gram,
                                                   postproc=postproc,
                                                   freq=rank or report_freq))
        if cache and not found:
#            print("Adding new anal {}, {}".format(word, to_cache))
            # Or use form instead of word
            self.add_new_anal(word, to_cache)
        if not analyses:
            # Impossible to analyze the word/form.
            if no_anal != None:
                no_anal.append(word)
            return analyses
        if rank and len(analyses) > 1:
#            print("Ranking analyses")
            analyses.sort(key=lambda x: -x[-1])
        # Select the n best analyses
        analyses = analyses[:nbest]
#        print("print_out {}, string {}, segment {}".format(print_out, string, segment))
        if print_out:
            # Print out stringified version
            print(self.analyses2string(word, analyses, seg=segment, form_only=not gram))
        elif not segment and not string:
            # Do final processing of analyses, given options
            for i, analysis in enumerate(analyses):
                if len(analysis) <= 2:
                    analyses[i] = (analysis[1],)
                else:
                    a = self.finalize_anal(analysis, citation=citation, um=um,
                                           gloss=gloss, report_freq=report_freq)
                    analyses[i] = a
#            analyses =  [(anal[1], anal[-2], anal[-1]) if len(anal) > 2 else (anal[1],) for anal in analyses]

        return [a for a in analyses if a]

    def anal_file(self, pathin, pathout=None, preproc=True, postproc=True, pos=None,
                  root=True, citation=True, segment=False, gram=True,
                  knowndict=None, guessdict=None, cache=True, no_anal=True,
                  phon=False, only_guess=False, guess=True, raw=False,
                  sep_punc=True, word_sep='\n', sep_ident=False, minim=False,
                  feats=None, simpfeats=None, um=False,
                  # Ambiguity
                  rank=True, report_freq=False, nbest=100,
                  report_n=50000,
                  lower=True, lower_all=False, nlines=0, start=0):
        """Analyze words in file, either writing results to pathout, storing in
        knowndict or guessdict, or printing out.
        saved is a dict of saved analyses, to save analysis time for words occurring
        more than once.
        """
        preproc = preproc and self.preproc
        postproc = postproc and self.postproc
        citation = citation and self.citation_separate
        storedict = True if knowndict != None else False
        try:
            filein = open(pathin, 'r', encoding='utf-8')
            # If there's no output file and no outdict, write analyses to terminal
            out = sys.stdout
            if segment:
                print('Segmenting words in', pathin)
            else:
                print('Analyzing words in', pathin)
            if pathout:
                # Where the analyses are to be written
                fileout = open(pathout, 'w', encoding='utf-8')
                print('Writing to', pathout)
                out = fileout
            fsts = pos or self.morphology.pos
            n = 0
            # Save words already analyzed to avoid repetition
            if no_anal:
                no_anal = []
            else:
                no_anal = None
            # Store final representations here; these depend not only on analyses but also
            # on various options to this method, like minim
            local_cache = {}
            # If nlines is not 0, keep track of lines read
            lines = filein.readlines()
            if start or nlines:
                lines = lines[start:start+nlines]
            for line in lines:
                n += 1
                if n % report_n == 0:
                    print("Analyzed {} lines".format(n))
                # Separate punctuation from words
                if sep_punc:
                    line = self.morphology.sep_punc(line)
                identifier = ''
                string = ''
                if sep_ident:
                    # Separate identifier from line
                    identifier, line = line.split('\t')
                    string = "{}\t".format(identifier)
                # Segment into words
                for w_index, word in enumerate(line.split()):
                    # Ignore punctuation
#                    if word in self.morphology.punctuation:
#                        continue
                    # Lowercase on the first word, assuming a line is a sentence
                    if lower_all or (lower and w_index == 0):
                        word = word.lower()
                    if word in local_cache:
#                        print("{} already in cache: {}".format(word, local_cache[word]))
                        analysis = local_cache[word]
                        if storedict:
                            if analysis:
                                add_anals_to_dict(self, analysis, knowndict, guessdict)
                        elif minim:
                            if w_index != 0:
                                string += " "
                            string += analysis
                        elif raw or not minim:
                            print(analysis, file=out)
                    else:
                        # If there's no point in analyzing the word (because it contains
                        # the wrong kind of characters or whatever), don't bother.
                        # (But only do this if preprocessing.)
                        analysis = preproc and self.morphology.trivial_anal(word)
                        if analysis:
                            if minim:
                                analysis = word
                            elif raw or um:
                                analysis = "{}  {}".format(word, analysis)
                            elif segment:
                                analysis = "{}: {}\n".format(word, analysis)
                            else:
                                analysis = word + ': ' + analysis
                        else:
                            # Attempt to analyze the word
                            form = word
                            if preproc:
                                form = self.preproc(form)
                            analyses = \
                            self.anal_word(form, fsts=fsts, guess=guess,
                                           phon=phon, only_guess=only_guess,
                                           segment=segment,
                                           root=root, stem=True,
                                           citation=citation and not raw,
                                           gram=gram,
                                           preproc=False, postproc=postproc and not raw,
                                           cache=cache, no_anal=no_anal, um=um,
                                           rank=rank, report_freq=report_freq,
                                           nbest=nbest,
                                           string=not raw and not um,
                                           print_out=False, only_anal=storedict)
                            if minim:
                                analysis = self.minim_string(form, analyses, feats=feats, simpfeats=simpfeats)
#                            elif raw and analyses:
#                                print("Raw analyses {}".format(analyses))
#                                analyses = (form, [(anal[0], anal[1], anal[2]) if len(anal) > 2 else (anal[0],) for anal in analyses])
                            # If we're storing the analyses in a dict, don't convert them to a string
                            if storedict or raw:
                                analysis = analyses
                            # Otherwise (for file or terminal), convert to a string
                            elif not minim:
                                if analyses:
                                    if raw or um:
                                        analysis = "{}  {}".format(form, analyses.__repr__())
                                    else:
                                        # Convert the analyses to a string
                                        analysis = self.analyses2string(word, analyses, seg=segment, form_only=not gram,
                                                                        short=False, word_sep=word_sep)
                                elif segment:
                                    analysis = "{}: {}".format(word, form)
                                else:
                                    analysis = word
                        # Either store the analyses in the dict or write them to the terminal or the file
                        if storedict:
                            if analysis:
                                add_anals_to_dict(self, analysis, knowndict, guessdict)
                        elif minim:
                            if w_index != 0:
                                string += " "
                            string += analysis
                        elif um or raw:
#                            analysis = self.pretty_analyses(analysis)
                            print(analysis, file=out)
                        else:
                            print(analysis, file=out, end='')
                        local_cache[word] = analysis
                if minim:
                    # End of line
                    print(string, file=out)
            filein.close()
            if pathout:
                fileout.close()
        except IOError:
            print('No such file or path; try another one.')

    def minim_string(self, form, analyses=None, feats=None, simpfeats=None):
        """Create a minimal string representing the analysis of a word.
        feats are features to include from the FeatStruct(s) in the
        analyses."""
#        print('form {}, analyses {}'.format(form, analyses))
        analysis = "{}".format(form)
        if analyses:
            root_pos = set()
            if len(analyses) == 1:
                if analyses[0][0]:
                    a = analyses[0]
                    # There is a real analysis
                    pos = a[0]
                    root = a[1]
                    suffixes = ''
                    if '+' in root:
                        # This would not work for prefixes
                        root, x, suffixes = root.partition('+')
                    rpg_string = "{}:{}".format('*' if root==form else root, pos)
                    part_fs = ''
                    if feats:
                        fs = a[3]
                        if fs:
                            part_fs = fs.part_copy(feats, simpfeats).__repr__()
                            rpg_string = "{}:{}".format(rpg_string, part_fs)
                    if suffixes:
                        analysis = "{};{} ({})".format(analysis, rpg_string, suffixes)
                    else:
                        analysis = "{};{}".format(analysis, rpg_string)
            else:
                for anal in analyses:
                    pos = anal[0]
                    root = anal[1]
                    rpg_string = '*' if root==form else root
                    if pos:
                        rpg_string = "{}:{}".format('*' if root==form else root, pos)
                        if feats:
                            fs = anal[3]
                            if fs:
                                part_fs = fs.part_copy(feats, simpfeats).__repr__()
                                rpg_string = "{}:{}".format(rpg_string, part_fs)
                    root_pos.add(rpg_string)
#                    if pos:
#                        root_pos.add((root, ":" + pos))
#                    else:
#                        root_pos.add((root, ''))
                if root_pos:
                    rp_string = '|'.join(root_pos)
# ["{}{}".format(r, p) for r, p in root_pos])
                    analysis = "{};{}".format(analysis, rp_string)
        return analysis

    def pretty_analyses(self, analyses):
        """Print raw analyses."""
        if not analyses:
            return "- {}\n".format(word)
        form = analyses[0]
        anals = analyses[1]
        s = '- ' + form + '\n'
        if anals:
            for anal in anals:
                if len(anal) == 1:
                    s += '  {}\n'.format(anal[0])
                else:
                    # root, features, frequency
                    s += '  {} {} {}\n'.format(anal[0], anal[1].__repr__(), anal[2])
        return s

    def analyses2string(self, word, analyses, seg=False, form_only=False, word_sep='\n',
                        short=False, webdicts=None):
        '''Convert a list of analyses to a string, and if webdicts, add analyses to dict.'''
        if seg:
            if analyses:
                analyses = [':'.join((a[0], a[1])) for a in analyses]
                return "{} -- {}{}".format(word, ';;'.join(analyses), word_sep)
            else:
                return word + word_sep
        elif form_only:
            if analyses:
                return word + ': ' + ', '.join({a[0] for a in analyses}) + word_sep
            else:
                return word + word_sep
        s = ''
#        if not analyses:
#            s += '?'
        s += Language.T.tformat('{}: {}\n', ['word', word], self.tlanguages)
        for analysis in analyses:
            if short:
                # What happens with file analysis
                root = analysis[0]
                features = analysis[1]
                if features:
                    pos = features.get('pos')
                    if pos == 'nadj' or pos == 'n_dv':
                        pos = 'n'
                    if pos:
                        if pos in self.morphology:
                            s += self.morphology[pos].pretty_anal(analysis, root=root, fs=features)
                        elif self.morphology.anal2string:
                            s += self.morphology.anal2string(analysis, webdict=webdict)
            else:
                fs = analysis[3]
#                print("fs {}".format(fs.__repr__()))
                pos = fs.get('pos') if fs else None
                if pos == 'nadj' or pos == 'n_dv':
                    pos = 'n'
                if pos:
                    webdict = None
#                    pos = pos.replace('?', '')
                    if webdicts != None:
                        webdict = {}
                        webdicts.append(webdict)
                    if pos in self.morphology:
                        if self.morphology[pos].anal2string:
                            s += self.morphology[pos].anal2string(analysis, webdict=webdict)
                        else:
                            s += self.morphology[pos].pretty_anal(analysis, webdict=webdict)
                    elif self.morphology.anal2string:
                        s += self.morphology.anal2string(analysis, webdict=webdict)
        return s

    def analysis2dict(self, analysis, record_none=False, ignore=[]):
        """Convert an analysis (a FeatStruct) to a dict."""
        dct = {}
        for k, v in analysis.items():
            if isinstance(v, FeatStruct):
                v_dict = self.analysis2dict(v, record_none=record_none, ignore=ignore)
                if v_dict:
                    # Could be {}
                    dct[k] = v_dict
            elif not v:
                # v is None, False, '', or 0
                if record_none:
                    dct[k] = None
            elif k not in ignore:
                dct[k] = v
        return dct

    def cache(self, form, root, fs, dct):
        """Add an analysis to the cache dictionary."""
        if form in dct:
            dct[form].append((root, fs))
        else:
            dct[form] = [(root, fs)]

    def finalize_anal(self, anal, citation=True, um=True, gloss=True,
                      report_freq=False):
        """
        Create dict with analysis.
        """
        a = {}
        pos, root, cit, gram1, gram2, count = anal
        # Postprocess root if appropriate
        root = self.postproc_root(self.morphology.get(pos),
                                  root, gram2)
        if not gram2 and not cit:
            # Unanalyzed word
            a['lemma'] = root
            if pos:
                a['POS'] = pos
        elif citation and cit:
            a['lemma'] = cit
#            self.finalize_citation(cit)
        if not citation or (cit and root != cit):
            a['root'] = root
        if gloss:
            g = self.get_gloss(gram2)
            if g:
                a['gloss'] = g
            elif um:
                # If there's no gloss and UM is True,
                # ignore this analysis
                return None
        if um and pos in self.um.hm2um:
            ufeats = self.um.convert(gram2, pos=pos)
            if ufeats:
                gram2 = ufeats
                a['gram'] = gram2
        if not um:
            if gram2:
                a['gram'] = gram2
        if report_freq:
            a['freq'] = count
        return a

    def finalize_citation(self, citation, ipa=False):
        """
        Do final processing of citation: convert romanization
        to standard phonetic representation.
        """
#        print("Finalizing {}".format(citation))
        if '|' in citation:
            ortho, phon = citation.split('|')
            phon = self.convert_phones(phon, ipa=ipa)
            return ortho + '|' + phon
        return self.convert_phones(citation, ipa=ipa)

    def simp_anal(self, analysis, postproc=False, segment=False):
        '''Process analysis for unanalyzed cases.'''
        if segment:
            return analysis[0], analysis[1], 100000
        elif postproc:
            # Convert the word to Geez.
            analysis = (analysis[0], self.postproc(analysis[1]))
#        if segment:
#            return analysis
        pos, form = analysis
        # 100000 makes it likely these will appear first in ranked analyses
        return pos, form, None, None, None, 100000

    def proc_anal_noroot(self, form, analyses, segment=False):
        '''Process analyses with no roots/stems.'''
        return [(analysis.get('pos'), None, None, analysis, None, 0) for analysis in analyses]

    def postproc_root(self, posmorph, root, fs):
        """
        If posmorph has a root_proc function, use it to produce
        a root.
        """
        if posmorph and posmorph.root_proc:
            func = posmorph.root_proc
            return func(root, fs)
        return root

    def get_gloss(self, fs, lg='eng'):
        """
        Get the gloss (root/stem translation) in the FeatStruct
        if there is one.
        """
        if fs and 't' in fs:
            t = fs['t']
            if lg in t:
                return t[lg]
        return ''

    @staticmethod
    def root_from_seg(segmentation):
        """Extract the root from a segmentation expression."""
        r = SEG_ROOT_RE.match(segmentation)
        if r:
            return r.group(1).split("+")[0]
        return ''

    def proc_anal(self, form, analyses, pos, show_root=True, citation=True,
                  segment=False, stem=True, guess=False,
                  postproc=False, gram=True, string=False,
                  freq=True):
        '''
        Process analyses according to various options, returning a list of analysis tuples.
        If freq, include measure of root and morpheme frequency.
        '''
        results = set()
#        print("proc_anal {}".format(analysis[0]))
        if segment:
            res = []
            for analysis in analyses:
                feats = analysis[1]
                if not feats:
                    # No analysis
                    continue
                if isinstance(feats, str):
                    pos = feats
                else:
                    pos = feats.get('pos')
                root = self.postpostprocess(analysis[0])
                # Remove { } from root
                real_root = Language.root_from_seg(root)
                root_freq = 0
                if freq:
                    root_freq = self.morphology.get_root_freq(real_root, feats)
                    feat_freq = self.morphology.get_feat_freq(feats)
                    root_freq *= feat_freq
                res.append((pos, root, root_freq))
            return res
        for analysis in analyses:
            root = self.postpostprocess(analysis[0])
            grammar = analysis[1]
            if not grammar:
                # No analysis; skip this one
                continue
            elif not pos:
                p = grammar.get('pos', '')
            else:
                p = pos
            cat = '?' + p if guess else p
            # grammar is a single FS
            if not show_root and not segment:
                analysis[0] = None
            if postproc and p in self.morphology and self.morphology[p].postproc:
                self.morphology[p].postproc(analysis)
            root_freq = 0
            if freq:
                # The freq score is the count for the root-feature combination
                # times the product of the relative frequencies of the grammatical features
                root_freq = self.morphology.get_root_freq(root, grammar)
                feat_freq = self.morphology.get_feat_freq(grammar)
                root_freq *= feat_freq
            # Find the citation form of the root if required
            if citation and p and p in self.morphology and self.morphology[p].citation:
                cite = self.morphology[p].citation(root, grammar, guess, stem)
                if not cite:
                    cite = root
                if postproc:
                    cite = self.postprocess(cite)
            else:
                cite = None
                # Prevent analyses with same citation form and FS (results is a set)
                # Include the grammatical information at the end in case it's needed
            results.add((cat, root, cite, grammar if gram else None, grammar, round(root_freq)))
        return list(results)

    def ortho2phon(self, word, gram=False, raw=False, return_string=False,
                   gram_pre='-- ', postpostproc=False,
                   rank=True, nbest=100, report_freq=False):
        '''Convert a form in non-roman to roman, making explicit features that are missing in orthography.
        @param word:     word to be analyzed
        @type  word:     string or unicode
        @param gram:     whether a grammatical analysis is to be included
        @type  gram:     boolean
        @param return_string: whether to return string analyses (needed for phon_file)
        @type  return_string: boolean
        @param gram_pre: prefix to put before form when grammatical analyses are included
        @type  gram_pre: string
        @param postpostproc: whether to call postpostprocess on output form
        @type  postpostproc: boolean
        @param rank: whether to rank the analyses by the frequency of their roots
        @type  rank: boolean
        @param nbest: return or report only this many analyses
        @type  nbest: int
        @param report_freq: whether to report the frequency of the root
        @type  report_freq: boolean
        @return:         a list of analyses
        @rtype:          list of (root, feature structure) pairs
        '''
        preproc = self.preprocess(word)
        # An output form to count, analysis dictionary
        results = {}
        # Is the word in the word or analyzed lists?
        analyzed = self.morphology.ortho2phon(preproc)
        if analyzed:
            analyzed = [self.convert_phones(a) for a in analyzed]
            # Just add each form with no analysis to the dict
            if postpostproc:
                analyzed = [self.postpostprocess(a) for a in analyzed]
            results = dict([(a, '') for a in analyzed])
        else:
            # Try to analyze it with FSTs
            for posmorph in self.morphology.values():
                output = posmorph.o2p(preproc, rank=rank)
                if output:
                    # Analyses found for posmorph; add each to the dict
                    for form, anal in output.items():
#                        print("form {}, anal {}".format(form, anal.__repr__()))
#                        root_count = count_anal[0]
#                        anal = count_anal[1:]
                        if gram:
                            if not raw:
                                anal = [(a[0], posmorph.anal2string(a[1:], None)) for a in anal]
                            else:
                                anal = [(a[0], a[2], a[4]) for a in anal]
                        else:
                            anal = [(a[0], a[1:]) for a in anal]
                        if postpostproc:
                            form = self.postpostprocess(form)
                        results[form] = results.get(form, []) + anal
            if not results:
                # No analysis
                # First phoneticize the form and mark as unknown ('?')
                form = '?' + self.morphology.phonetic(preproc)
                if postpostproc:
                    form = self.postpostprocess(form)
                # Then add it to the dict
                results = {form: ''}
        # Now do something with the results
        # Convert the result dict to a list (ranked if rank=True)
        result_list = []
        for f, anals in results.items():
            count = 0
            anal_list = []
            if anals:
                for a in anals:
                    count += a[0]
                    anal_list.append(a[1:])
            result_list.append((f, count, anal_list))
        if rank:
            result_list.sort(key=lambda x: -x[1])
        result_list = result_list[:nbest]
#        print("result list {}".format(result_list))
        if gram:
            # Include grammatical analyses
            if not raw:
                if return_string:
                    # Return the results as a string
                    return [(r[0], r[1:]) for r in result_list]
                # Print out the results
                for f, c, anals in result_list:
                    print(gram_pre + f)
                    for anal in anals:
                        print(anal[0], end='')
            else:
                # Return the raw results
                result = []
                for form, count, anals in result_list:
                    result1 = {}
                    result1['form'] = form
                    if report_freq:
                        result1['count'] = count
                    anals1 = []
                    for a in anals:
                        adct = {}
                        root = a[0]
                        anals2 = a[1]
                        pos = anals2.get('pos')
                        if pos == 'n_dv':
                            pos = 'n'
                        if pos:
                            m = self.morphology.get(pos)
                            if m:
                                root = m.root_proc(root, anals2)
                        if '<' in root:
                            adct['root'] = root
                        else:
                            adct['lemma'] = root
                        adct['gram'] = anals2
                        if 't' in anals2 and 'eng' in anals2['t']:
                            adct['gloss'] = anals2['t']['eng']
                        anals1.append(adct)
                    result1['anals'] = anals1
                    result.append(result1)
                return result
        elif raw or return_string:
            # Return only the forms and frequencies
            if rank and report_freq:
                return [(r[0], r[1]) for r in result_list]
            else:
                return [r[0] for r in result_list]
        else:
            # Print out only the forms
            for anal, count in [(r[0], r[1]) for r in result_list]:
                if rank and report_freq:
                    print('{} ({})'.format(anal, count), end=' ')
                else:
                    print('{}'.format(anal), end=' ')
            print()

    def ortho2phon_file(self, infile, outfile=None, gram=False,
                        word_sep='\n', anal_sep=' ', print_ortho=True,
                        postpostproc=False,
                        rank=True, report_freq=False, nbest=100,
                        start=0, nlines=0):
        '''Convert non-roman forms in file to roman, making explicit features that are missing in the orthography.
        @param infile:   path to a file to read the words from
        @type  infile:   string
        @param outfile:  path to a file where analyses are to be written
        @type  outfile:  string
        @param gram:     whether a grammatical analysis is to be included
        @type  gram:     boolean
        @param word_sep:  word separator (only when gram=False)
        @type  word_sep:  string
        @param anal_sep:  analysis separator (only when gram=False)
        @type  anal_sep:  string
        @param print_ortho: whether to print the orthographic form first
        @type  print_ortho: boolean
        @param postpostproc: whether to call postpostprocess on output form
        @type  postpostproc: boolean
        @param rank: whether to rank the analyses by the frequency of their roots
        @type  rank: boolean
        @param report_freq: whether to report the frequency of the root
        @type  report_freq: boolean
        @param start:    line to start analyzing from
        @type  start:    int
        @param nlines:   number of lines to analyze (if not 0)
        @type  nlines:   int
        '''
        try:
            filein = open(infile, 'r', encoding='utf-8')
            # Whether to write analyses to terminal
            out = sys.stdout
            # Dictionary to store analyzed words in
            saved_dct = {}
            print('Analyzing words in', infile)
            if outfile:
                # Where the analyses are to be written
#                out = codecs.open(outfile, 'w', 'utf-8')
                out = open(outfile, 'w', encoding='utf-8')
                print('Writing analysis to', outfile)
            lines = filein.readlines()
            if start or nlines:
                lines = lines[start:start+nlines]
            begun = False
            for line in lines:
                # Separate punctuation from words
                line = self.morphology.sep_punc(line)
                # Segment into words
                for word in line.split():
                    if word in saved_dct:
                        # Don't bother to analyze saved words
                        analysis = saved_dct[word]
                    else:
                        # Analyze the word
                        analysis = self.ortho2phon(word, gram=gram,
                                                   postpostproc=postpostproc,
                                                   raw=False, return_string=True,
                                                   rank=rank, report_freq=report_freq, nbest=nbest)
                        saved_dct[word] = analysis
#                    print("Analysis {}".format(analysis))
                    # Write the analysis to file or stdout
                    if gram:
                        print("{0}".format(word), file=out)
                        for form, anal in analysis:
                            print("-- {0}".format(form), file=out)
                            for a in anal[1:]:
                                for a1 in a:
                                    print("{0}".format(a1[0]), end='', file=out)
                        print(file=out)
                    else:
                        # Start with the word_sep string
                        if begun:
                            print(file=out, end=word_sep)
                        if print_ortho:
                            # Print the orthographic form
                            print("{0} ".format(word), end='', file=out)
                        for anal in analysis[:-1]:
                            # Print an analysis followed by the analysis separator
                            print("{0} ({1})".format(anal[0], anal[1]), end=anal_sep, file=out)
                        # Print the last analysis with no analysis separator
                        if analysis:
                            print("{0} ({1})".format(analysis[-1][0], analysis[-1][1]), end='', file=out)
                    begun=True
            if not gram:
                # Final newline
                print(file=out)
            filein.close()
            if outfile:
                out.close()
        except IOError:
            print('No such file or path; try another one.')

    ## Using RE rules for joining morphological segments

    def add_rules(self, POS, rules):
        self.rules[POS] = rules

    def join_segments(self, POS, segstring):
        rules = self.rules.get(POS)
        segstring = self.preprocess(segstring)
        if rules:
            output = rules.apply(segstring)
            return self.postprocess(output)
        else:
            print("No rules available for {}".format(POS))
            return segstring

class EESLanguage(EES, Language):
    '''
    Ethio-Eritrean Semitic languages, which share many properties,
    especially related to orthography.
    '''

    def __init__(self, abbrev):
        Language.__init__(self, abbrev)
        EES.__init__(self)
