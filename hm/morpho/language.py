"""
This file is part of HornMorpho, which is part of the PLoGS project.

    <http://homes.soic.indiana.edu/gasser/plogs.html>

    Copyleft 2011, 2012, 2013, 2014, 2016, 2018.
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

LANGUAGE_DIR = os.path.join(os.path.dirname(__file__),
                            os.path.pardir,
                            'languages')

from .morphology import *
from .anal import *

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
# Term translations
# tr...:
TRANS_RE = re.compile(r'\s*tr.*?:\s*(.*)')
# Beginning of feature-value list
FEATS_RE = re.compile(r'\s*feat.*?:\s*(.*)')
# Feature-value pair
FV_RE = re.compile(r'\s*(.*?)\s*=\s*(.*)')
# FV combinations, could be preceded by ! (= priority)
FVS_RE = re.compile(r'([!]*)\s*([^!]*)')
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

## Regex for checking for non-ascii characters
ASCII_RE = re.compile(r'[a-zA-Z]')

class Language:
    '''A single Language, currently only handling morphology.'''

    T = TDict()

    def __init__(self, label='', abbrev='', backup='',
                 preproc=None, postproc=None, read_cache=False,
                 # There may be a further function for post-processing
                 postpostproc=None,
                 seg_units=None,
                 # list of grammatical features to be combined with roots for statistics,
                 # e.g., voice and aspect for Amharic verb roots (assume there's only
                 # list)
                 stat_root_feats=None,
                 # list of lists of grammatical features for statistics, e.g.,
                 # [poss, expl] for Amharic (whether is explicitly possessive)
                 stat_feats=None,
                 citation_separate=True):
#                 msgs=None, trans=None):
        """
        Set some basic language-specific attributes.

        @param preproc            Whether to pre-process input to analysis, for example,
                                  to convert non-roman to roman characters
        @param postproc           Whether to post-process output of generation, for
                                  example, to convert roman to non-roman characters
        @param seg_units          Segmentation units (graphemes)
        @param citation_separate  Whether citation form of words is separate from roots
#        @param msgs               Messages in the languages (or some other)
#        @param trans              Translations of terms from english to this language
        """
        self.label = label
        self.abbrev = abbrev or label[:3]
        # Backup language for term translation, etc.
        self.backup = backup
        self.morphology = None
        self.preproc = preproc
        self.postproc = postproc
        self.postpostproc = postpostproc
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
        # Whether the language data and FSTs have been loaded
        self.load_attempted = False
        self.cached = {}
        # Cached entries read in when language is loaded
        if read_cache:
            self.read_cache()
        # New analyses since language loaded
        # each entry a wordform and list of (root, FS) analyses
        self.new_anals = {}

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
                print("Reading cached words")
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
             segment=False, phon=False,
             guess=True, poss=None, verbose=False):
        """Create a language using data in the language data file."""
        lang = Language(abbrev=abbrev)
        # Load data from language file
        loaded = lang.load_data(load_morph=load_morph, segment=segment, phon=phon,
                                guess=guess, poss=poss, verbose=verbose)
        if not loaded:
            # Loading data failed somewhere; abort
            return
        return lang

    def load_data(self, load_morph=False, segment=False, phon=False, guess=True,
                  poss=None, verbose=False):
        if self.load_attempted:
            return
        self.load_attempted = True
        filename = self.get_data_file()
        if not os.path.exists(filename):
#            print(Language.T.tformat('No language data file for {}', [self], self.tlanguages))
            pass
        else:
            if verbose:
                print(Language.T.tformat('Loading language data from {}', [filename], self.tlanguages))
            with open(filename, encoding='utf-8') as stream:
                data = stream.read()
                self.parse(data, poss=poss, verbose=verbose)
        if load_morph:
            if not self.load_morpho(segment=segment, ortho=True, phon=phon, guess=guess, verbose=verbose):
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

            m = CLEAN_RE.match(line)
            if m:
                # Ignore in HornMorpho
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
#            print("feats {}".format(feats))
            for pos in feats:
                if not poss or pos in poss:
                    pos_args.append((pos, feats[pos], lex_feats[pos], excl[pos],
                                     abbrev[pos], fv_abbrev[pos], fv_dependencies[pos],
                                     fv_priorities[pos]))
            morph = Morphology(pos_morphs=pos_args,
                               punctuation=punc, characters=chars)
            self.set_morphology(morph)

    def proc_feat_string(self, feat, abbrev_dict, excl_values, lex_feats, fv_dependencies):
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

    def load_morpho(self, fsts=None, ortho=True, phon=False,
                    segment=False, recreate=False, guess=True, verbose=False):
        """Load words and FSTs for morphological analysis and generation."""
        fsts = fsts or self.morphology.pos
        opt_string = ''
        if segment:
            opt_string = 'segmentation'
        elif phon:
            opt_string = 'phonetic'
        else:
            opt_string = 'analysis'
        if not self.has_cas(generate=phon, guess=False, phon=phon, segment=segment):
            print('No {} FST available for {}!'.format(opt_string, self))
            return False
        msg_string = Language.T.tformat('Loading morphological data for {0}{1} ...',
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
            # Load lexical anal and gen FSTs (no gen if segmenting)
            if ortho:
                self.morphology[pos].load_fst(gen=not segment,
                                              create_casc=False,
                                              phon=False, segment=segment,
                                              recreate=recreate, verbose=verbose)
            if phon:
                self.morphology[pos].load_fst(gen=True,
                                              create_casc=False,
                                              phon=True, segment=segment,
                                              recreate=recreate, verbose=verbose)
            # Load guesser anal and gen FSTs
            if not segment and guess:
                if ortho:
                    self.morphology[pos].load_fst(gen=True, guess=True, phon=False, segment=segment,
                                                  create_casc=False,
                                                  recreate=recreate, verbose=verbose)
                if phon:
                    self.morphology[pos].load_fst(gen=True, guess=True, phon=True, segment=segment,
                                                  create_casc=False,
                                                  recreate=recreate, verbose=verbose)
            # Load statistics for generation
            self.morphology[pos].set_root_freqs()
            self.morphology[pos].set_feat_freqs()

        return True

    def get_fsts(self, generate=False, phon=False, segment=False):
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
                phon=False, segment=False):
        """Is there at least one cascade file for the given FST features?"""
        for pos in self.morphology.pos:
            if self.morphology[pos].has_cas(generate=generate,
                                            guess=guess, phon=phon, segment=segment):
                return True
        return False

    ### Analyze words or sentences

    def anal_file(self, pathin, pathout=None, preproc=True, postproc=True, pos=None,
                  root=True, citation=True, segment=False, gram=True,
                  knowndict=None, guessdict=None, cache=True, no_anal=True,
                  phon=False, only_guess=False, guess=True, raw=False,
                  sep_punc=True, word_sep='\n', sep_ident=False, minim=False,
                  feats=None, simpfeats=None,
                  # Ambiguity
                  rank=True, report_freq=True, nbest=100,
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
                if n % report_n == 0:
                    print("Analyzed {} lines".format(n))
                n += 1
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
                            elif raw:
                                analysis = (word, [])
                            elif segment:
                                analysis = "{}: {}\n".format(word, analysis)
                            else:
                                analysis = 'word: ' + analysis + '\n'
                        else:
                            # Attempt to analyze the word
                            form = word
                            if preproc:
                                form = self.preproc(form)
                            analyses = self.anal_word(form, fsts=fsts, guess=guess,
                                                      phon=phon, only_guess=only_guess, segment=segment,
                                                      root=root, stem=True, citation=citation and not raw, gram=gram, 
                                                      preproc=False, postproc=postproc and not raw,
                                                      cache=cache, no_anal=no_anal,
                                                      rank=rank, report_freq=report_freq, nbest=nbest,
                                                      string=not raw, print_out=False,
                                                      only_anal=storedict)
                            if minim:
                                analysis = self.minim_string(form, analyses, feats=feats, simpfeats=simpfeats)
                            elif raw and analyses: 
                                analyses = (form, [(anal[0], anal[1], anal[2]) if len(anal) > 2 else (anal[0],) for anal in analyses])
                            # If we're storing the analyses in a dict, don't convert them to a string
                            if storedict or raw:
                                analysis = analyses
                            # Otherwise (for file or terminal), convert to a string
                            elif not minim:
                                if analyses:
                                    # Convert the analyses to a string
                                    analysis = self.analyses2string(word, analyses,
                                                                    seg=segment, form_only=not gram, word_sep=word_sep)
                                elif segment:
                                    analysis = "{}: {}\n".format(word, form)
                                else:
                                    analysis = '?word: ' + word + '\n'
                        # Either store the analyses in the dict or write them to the terminal or the file
                        if storedict:
                            if analysis:
                                add_anals_to_dict(self, analysis, knowndict, guessdict)
                        elif minim:
                            if w_index != 0:
                                string += " "
                            string += analysis
                        elif raw:
                            analysis = self.pretty_analyses(analysis)
                            print(analysis, file=out)
                        elif not minim:
                            print(analysis, file=out)
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
            return ''
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
                        webdicts=None):
        '''Convert a list of analyses to a string, and if webdicts, add analyses to dict.'''
        if seg:
            if analyses:
                analyses = [':'.join((a[0], a[1])) for a in analyses]
                return "{} -- {}{}".format(word, ';;'.join(analyses), word_sep)
            else:
                return word + word_sep
        elif form_only:
            if analyses:
#                print('analyses', analyses)
                return word + ': ' + ', '.join(analyses) + word_sep
            else:
                return word + word_sep
        s = ''
        if not analyses:
            s += '?'
        s += Language.T.tformat('{}: {}\n', ['word', word], self.tlanguages)
        for analysis in analyses:
            pos = analysis[0]
            if pos:
                webdict = None
                pos = pos.replace('?', '')
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

    def anal_word(self, word, fsts=None, guess=True, only_guess=False,
                  phon=False, segment=False,
                  root=True, stem=True, citation=True, gram=True,
                  get_all=True, to_dict=False, preproc=False, postproc=False,
                  cache=True, no_anal=None, string=False, print_out=False,
                  rank=True, report_freq=True, nbest=100,
                  only_anal=False):
        '''Analyze a single word, trying all existing POSs, both lexical and guesser FSTs.

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

        # See if the word is cached
        cached = self.get_cached_anal(word)
        if cached:
            found = True
            analyses = self.proc_anal(word, cached, None,
                                      show_root=root, citation=citation, stem=stem,
                                      segment=segment, guess=False,
                                      postproc=postproc, gram=gram, freq=rank or report_freq)
        # Is word already analyzed, without any root/stem (for example, there is a POS and/or
        # a translation
        elif form in self.morphology.analyzed:
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
                        analysis = self.morphology[pos].anal(form,
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
                analysis = self.morphology[pos].anal(form, guess=True,
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
        if print_out:
            # Print out stringified version
            print(self.analyses2string(word, analyses, seg=segment, form_only=not gram))
        elif not string and not segment:
            analyses =  [(anal[1], anal[-2], anal[-1]) if len(anal) > 2 else (anal[1],) for anal in analyses]

        return analyses

    def simp_anal(self, analysis, postproc=False, segment=False):
        '''Process analysis for unanalyzed cases.'''
#        print("simp_anal({})".format(analysis))
        if segment:
            return analysis[0], analysis[1], 100000
        elif postproc:
            # Convert the word to Geez.
            analysis[1] = self.postproc(analysis[1])
#        if segment:
#            return analysis
        pos, form = analysis
        # 100000 makes it likely these will appear first in ranked analyses
        return pos, form, None, 100000

    def proc_anal_noroot(self, form, analyses, segment=False):
        '''Process analyses with no roots/stems.'''
#        print("Form {}, analyses {}".format(form, analyses))
        return [(analysis.get('pos'), None, None, analysis, None, 0) for analysis in analyses]

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
        '''Process analyses according to various options, returning a list of analysis tuples.
        If freq, include measure of root and morpheme frequency.'''
        results = set()
#        print("Analyses")
#        for analysis in analyses:
#            print(" {}".format(analysis))
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
#                print("Root {}, real root {}".format(root, real_root))
                root_freq = 0
                if freq:
#                    print("Figuring freq for root {} and feats {}".format(real_root, feats.__repr__()))
                    root_freq = self.morphology.get_root_freq(real_root, feats)
                    feat_freq = self.morphology.get_feat_freq(feats)
                    root_freq *= feat_freq
                res.append((pos, root, root_freq))
            return res
#            return [(analysis[1] if isinstance(analysis[1], str) else analysis[1].get('pos'), self.postpostprocess(analysis[0])) for analysis in analyses]
        for analysis in analyses:
            root = self.postpostprocess(analysis[0])
            grammar = analysis[1]
            if not grammar:
                # No analysis; skip this one
#                results.add((root, None, 0))
                continue
#                p = pos or ''
            elif not pos:
                p = grammar.get('pos', '')
            else:
                p = pos
            cat = '?' + p if guess else p
            # grammar is a single FS
            if not show_root and not segment:
                analysis[0] = None
            if postproc and self.morphology[p].postproc:
                self.morphology[p].postproc(analysis)
#            proc_root = analysis[0]
            root_freq = 0
#            for g in grammar:
            if freq:
                # The freq score is the count for the root-feature combination
                # times the product of the relative frequencies of the grammatical features
                root_freq = self.morphology.get_root_freq(root, grammar)
                feat_freq = self.morphology.get_feat_freq(grammar)
                root_freq *= feat_freq
            # Find the citation form of the root if required
            if citation and self.morphology[p].citation:
                cite = self.morphology[p].citation(root, grammar, guess, stem)
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
            # Just add each form with no analysis to the dict
            if postpostproc:
                analyzed = [self.postpostprocess(a) for a in analyzed]
            results = dict([(a, '') for a in analyzed])
        else:
            # Try to analyze it with FSTs
            for posmorph in self.morphology.values():
                output = posmorph.ortho2phon(preproc, rank=rank)
                if output:
                    # Analyses found for posmorph; add each to the dict
                    for form, anal in output.items():
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
                return result_list
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

class Multiling(dict):

    def __init__(self, abbrev, *lang_pos, load_lexicons=False):
        """Constructor takes one or more pairs: (language, [pos strings])."""
        dict.__init__(self, [(lang.abbrev, [lang.morphology[pos] for pos in poss]) for lang, poss in lang_pos])
        self.abbrev = abbrev
        self.directory = self.get_dir()
        name = []
        for l, ps in self.items():
            name.append(l + ':' + '[' + ','.join([p.pos for p in ps]) + ']')
        self.name = '<<' + ' | '.join(name) + '>>'
        self.lexicons = {}
        # Abbrevs for first two languages
        self.langs2 = list(self.keys())[:2]
        if load_lexicons:
            # first two languages
            self.get_lexicon(self.langs2[0], self.langs2[1])
            self.get_lexicon(self.langs2[1], self.langs2[0])
        # lists of FSTs organized by direction
        self.fsts = {}

    def __repr__(self):
        return self.name

    def get_dir(self):
        """Where data for this multiling is kept."""
        return os.path.join(LANGUAGE_DIR, self.abbrev)

    def get_lex_file(self, source, target):
        s = source if isinstance(source, str) else source.abbrev
        t = target if isinstance(target, str) else target.abbrev
        return os.path.join(self.directory, s + '2' + t + '.lex')

    def get_lexicon(self, source, target):
        abbrev = source + target
        if abbrev in self.lexicons:
            return self.lexicons[abbrev]
        else:
            import yaml
            file = self.get_lex_file(source, target)
            lexicon = yaml.load(open(file, encoding='utf8'))
            self.lexicons[abbrev] = lexicon
            return lexicon

    def tra(self, morph=False, lexicon=False):
        """Make an interactive text menu for translating words or phrases."""
        first = True
        tdir = ''
        while True:
            t = '1'
            if not first:
                t = input("\n¿Traducir de nuevo?  [1]   |   ¿Terminar?   [2] >> ")
            if t == '2':
                return
            first = False
            tdir = self.tra1(morph=morph, lexicon=lexicon, tdir=tdir)

    def tra1(self, morph=False, lexicon=False, tdir=''):
        """Make an interactive text menu for translating words or phrases."""
        lex = True
        if morph:
            lex = False
        elif lexicon:
            lex = True
        else:
            transi = input("-Morfología          [1]   |   +Morfología  [2] >> ")
            if transi and transi == '2':
                lex = False
        if not tdir:
            dir1 = "{}->{}".format(self.langs2[0], self.langs2[1])
            dir2 = "{}->{}".format(self.langs2[1], self.langs2[0])
            direction = input("Dirección: {}    [1]   |   {}       [2] >> ".format(dir1, dir2))
            if direction and direction == '2':
                tdir = self.langs2[1] + self.langs2[0]
            else:
                tdir = self.langs2[0] + self.langs2[1]
        item = input("Palabra   o   frase   para   traducir           :: ")
        if lex:
            trans = self.tralex(item, direction=tdir)
            if not trans:
                print("   Traducción no encontrada")
        else:
            trans = self.tramorf(item, direction=tdir)
            if not trans:
                print("   Traducción no encontrada")
        return tdir

    def tramorf(self, phrase, fsts=None, direction='', verbose=False):
        """Use lexicons and morphological FSTs to attempt to translate phrase."""
        # phrase must be a list of words
        if isinstance(phrase, str):
            phrase = phrase.split()
        if not fsts:
            fsts = self.fsts.get(direction)
        if not fsts:
            if verbose:
                print("No FSTs found")
                return []
        for f in fsts:
            if verbose:
                print("Attempting to translate with FST {}".format(f))
            trans = f.transduce(phrase, verbose=verbose)
            if trans:
                return trans
        return []

    def tralex(self, item, direction='', root=None, only_one=False):
        """Use lexicons to attempt to translate item."""
        dct = self.lexicons.get(direction)
        if not dct:
            print('No lexicon loaded')
            return []
        key = root if root else item
        entries = dct.get(key)
        if not entries:
            return []
        res = []
        for sphrase, troot, tphrase, tpos in entries:
            if sphrase == item:
                if only_one:
                    print('   {}'.format(tphrase))
                    return [tphrase]
                else:
                    print('   {}'.format(tphrase))
                    res.append(tphrase)
        return res

    @staticmethod
    def get_translations(source, lexicon, tlang, one_word=True, one=False, match_all=True):
        """
        Get translations for source root in lexicon dict.
        """
        targets = lexicon.get(source, [])
        res = []
        for sphrase, target, tphrase, tpos in targets:
            if match_all and source != sphrase:
                continue
            if ' ' in tphrase and one_word:
                continue
            res.append((target, tpos))
            if one and len(res) == 1:
                return res
        return res

    @staticmethod
    def gen_target(root, feats, pos, prefixes=None, final=False, verbose=False):
        if verbose:
            print('Generating {}: {}'.format(root, feats.__repr__()))
#        result = pos.gen(root, interact=False, update_feats=feats)
        result = pos.generate(root, feats, interact=False, print_word=final)
        return [r[0] for r in result]

    @staticmethod
    def match_cond(root, feats, condFS):
        if condFS:
            if not Multiling.match_feats(feats, condFS):
                return False
        return True

    @staticmethod
    def match_feats(fs1, fs2):
        """Match two FSSetss, converting strings to FSSets if necessary."""
        if not isinstance(fs1, FSSet):
            fs1 = FSSet(fs1)
        if not isinstance(fs2, FSSet):
            fs2 = FSSet(fs2)
        return fs1.unify(fs2)

class TraFST:
    """FST for phrase translation.
    """

    stateID = 0

    def __init__(self, multiling, slang, tlang, states=None):
        self.multiling = multiling
        # Language abbreviations
        self.slang = slang
        self.tlang = tlang
        self.states = states if states else {}
        self.lexicon = multiling.get_lexicon(slang, tlang)
        # Initial state ID
        self.init = -1
        # Add the FST to the appropriate list in the multiling
        abbrev = slang + tlang
        if abbrev in multiling.fsts:
            multiling.fsts[abbrev].append(self)
        else:
            multiling.fsts[abbrev] = [self]

    def add_state(self, ins=None, outs=None):
        ins = ins if ins else []
        outs = outs if outs else []
        id = TraFST.stateID
        if not self.states:
            self.init = id
        self.states[id] = [ins, outs]
        TraFST.stateID += 1
        return id

    def add_arc(self, source, dest, arc):
        if source != None:
            # outs for source
            self.states[source][1].append(arc)
        if dest != None:
            # ins for dest
            self.states[dest][0].append(arc)
        arc.sstate = source
        arc.dstate = dest

    def make_arc(self, scond, tcond, fscond, name=''):
        return TraArc(scond, tcond, fscond, name=name)

    def is_final(self, state):
        return not self.states[state][1]

    def is_initial(self, state):
        return not self.states[state][0]

    def out_arcs(self, state):
        return self.states[state][1]

    def transduce(self, words, initial=None, one=False, verbose=False):
        init_tra_state = initial if initial else self.init_tra_state(words)
        init_fst_state = init_tra_state.fst_state
        init_arcs = self.out_arcs(init_fst_state)
        if not init_arcs:
            print('No out arcs from initial state!')
            return
        results = []
        stack = [(init_tra_state, init_arcs[0])]
        for arc in init_arcs[1:]:
            tra_state = init_tra_state.clone()
            stack.append((tra_state, arc))
        while stack:
            if verbose:
                print('Current stack: {}'.format(stack))
            tra_state, arc = stack.pop()
            if verbose:
                print('Current state {}, current arc {}'.format(tra_state, arc))
                print(' Current FS {}'.format(tra_state.fs.__repr__()))
            traverse = tra_state.traverse(arc, verbose=verbose)
            if traverse:
                if verbose:
                    print('Succeeded on arc {}'.format(arc))
                # Find the arcs out of the dest state
                new_fst_state = tra_state.fst_state
                if self.is_final(new_fst_state):
                    if verbose:
                        print('{} is a final state'.format(new_fst_state))
                    if tra_state.is_empty():
                        output = [' '.join(o) for o in tra_state.output]
                        for o in output:
                            print("--> {}".format(o))
#                        print('Output: {}'.format(output))
                        results.extend(output)
                    elif verbose:
                        print('But {} is not empty'.format(new_fst_state))
                else:
                    new_arcs = self.out_arcs(new_fst_state)
                    stack.append((tra_state, new_arcs[0]))
                    for arc in new_arcs[1:]:
                        new_tra_state = tra_state.clone()
                        stack.append((new_tra_state, arc))
            elif verbose:
                print('Failed on arc {}'.format(arc))
        return results                  

    def init_tra_state(self, words):
        sPOSs = self.multiling.get(self.slang)
        tPOSs = self.multiling.get(self.tlang)
        lexicon = self.lexicon
        return TraState(words, [], FeatStruct(), sPOSs, tPOSs,
                        lexicon, self.slang, self.tlang, self,
                        fst_state=self.init)

class TraState:
    """
    State of translation FST transduction:
    0 current word: [word, {POS: analysis, ...}]
    1 source words left
    2 current output
    3 current FeatStruct
    """

    id = 0

    def __init__(self, swords, output, fs,
                 sPOSs, tPOSs, s2tlex,
                 slang, tlang, fst,
                 sword=None, fst_state=-1, name=None):
        if not sword:
            self.sword = [swords[0], {}]
            self.swords = swords[1:]
        else:
            self.sword = sword
            self.swords = swords
        self.output = output
        self.fs = fs
        self.sPOSs = sPOSs
        self.tPOSs = tPOSs
        self.s2tlex = s2tlex
        self.slang = slang
        self.tlang = tlang
        self.fst = fst
        self.fst_state = fst_state
        self.name = name or ' '.join(swords)
        self.id = TraState.id
        self.position = 0
        TraState.id += 1

    def __repr__(self):
        return '{{{{{}:#{}|{}}}}}'.format(self.name, self.id, self.sword[0])

    def clone(self):
        sword = copy.deepcopy(self.sword)
        swords = self.swords.copy()
        output = self.output.copy()
        fs = self.fs.copy(deep=True)
        return TraState(swords, output, fs,
                        self.sPOSs, self.tPOSs, self.s2tlex,
                        self.slang, self.slang, self.fst,
                        sword=sword, fst_state=self.fst_state, name=self.name)

    def is_empty(self):
        """Have all words been consumed?"""
        return not self.sword

    def traverse(self, arc, final=False, verbose=False):
        """
        Traverse a TraArc, updating the TraState, possibly generating
        new TraStates or returning False if traversal fails.
        """
        if verbose:
            print('**{} traversing {}'.format(self, arc))
        # Test source condition, parsing source word if necessary.
        if not self.match_source(arc.scond, verbose=verbose):
            return False
        ## Update FS
        if not self.update_fs(arc.fscond, verbose=verbose):
            return False
        ## Update target
        if not self.update_target(arc.tcond, final=final, verbose=verbose):
            return False
        ## Update source words
        if 'pop' in arc.scond:
            self.update_words(verbose=verbose)
        self.fst_state = arc.dstate
        return True

    def get_target_pos(self, abbrev):
        for p in self.tPOSs:
            if p.pos == abbrev:
                return p

    def get_word_fvs(self, feat, POSs):
        """List values for feat string in analyses of current word for pos."""
#        print('Getting word FVs {}, {}'.format(feat, pos))
        anals = []
        for pos in POSs:
            if pos in self.sword[1]:
                anals.extend(self.sword[1].get(pos))
#        print('Found anals {}'.format(anals))
        if anals:
            # only the first anal
            return [a.get(feat) for a in anals[0][1]]
        return []
    
    def copy_fs(self, feat, POSs, verbose=False):
        """Copy value(s) of feat in analyses of current word for pos to current FS."""
        fvs = self.get_word_fvs(feat, POSs)
        if verbose:
            print('Copying {} to FS'.format(fvs))
        if fvs:
            # For now just copy the first feature value
            self.fs.update({feat: fvs[0]})
#            print('FS now {}'.format(self.fs.__repr__()))

    def match_source(self, cond, verbose=False):
        """Match the source condition on an arc."""
        if verbose:
            print('*Matching source')
        if not cond:
            # Don't update swords and sword.
            return True
        if self.is_empty():
            # Everything else requires a current word.
            return False
        word = self.sword[0]
        condanal = cond.get('anal')
        condFS = condroot = condposs = None
        if condanal:
            condroot, condposs, condFS = condanal
        if condFS or condroot:
            # word analysis dict
            analyses = self.sword[1]
            if not isinstance(condFS, FSSet):
                condFS = FSSet(condFS)
            anals = []
            # We have to analyze the input word
            if verbose:
                print("Looking for anals in {}".format(self.sPOSs))
            for pos in self.sPOSs:
                pos_abbrev = pos.pos
                if pos_abbrev in condposs:
                    if pos_abbrev in analyses:
                        if verbose:
                            print("There are already analyses {}".format(analyses[pos_abbrev]))
                        # There are already analyses of the word
                        anals.extend(analyses[pos_abbrev])
                    else:
                        if verbose:
                            print("Analyzing {} with FS {} in {}".format(word, condFS.__repr__(), pos))
                        anal = pos.analyze(word, init_weight=condFS)  #, trace=1)
                        if anal:
                            if not condroot or all([(condroot == a[0]) for a in anal]):
                                analyses[pos_abbrev] = anal
                                anals.extend(anal)
#            if verbose:
#                print('Found anals', anals)
            # There may be multiple analyses
            if not anals:
                if verbose:
                    print("No analyses found")
                return False
            else:
                if len(anals) > 1:
                    print('Análisis multiples encontrados')
                # Check only the first analysis
                root, feats = anals[0]
                if not Multiling.match_cond(root, feats, condFS):
#                    if verbose:
#                        print('Updating words')
#                    self.update_words()
#                    return True
#                else:
                    if verbose:
                        print('Analysis fails to match source condition')
                    return False
        else:
            # No analysis required for matching; just match the raw word
            condword = cond.get('word')
            if condword and word != condword:
                if verbose:
                    print('Word fails to match source condition')
                return False
            else:
                return True
        return True

    def update_fs(self, cond, verbose=False):
        if verbose:
            print('*Updating FS')
        if cond:
            add = cond.get('add')
            if add:
                if not isinstance(add, FeatStruct):
                    add = FeatStruct(add)
                new_fs = simple_unify(self.fs, add)
                if new_fs == 'fail':
                    if verbose:
                        print('Update FS fails to unify')
                    return False
                self.fs = new_fs
            copy = cond.get('copy')
            if copy:
                feats, POSs = copy
                if not isinstance(POSs, list):
                    POSs = [POSs]
                for f in feats:
                    self.copy_fs(f, POSs, verbose=verbose)
        return True

#    def update_fs(self, update):
#        """Update the current FS, unifying it with FS update."""
#        if not isinstance(update, FeatStruct):
#            update = FeatStruct(update)
#        new_fs = simple_unify(self.fs, update)
#        if new_fs == 'fail':
#            return False
#        self.fs = new_fs
#        return True

    def update_words(self, verbose=False):
        if verbose:
            print('*Popping words')
        self.position += 1
        if self.swords:
            self.sword = [self.swords[0], {}]
            self.swords.pop(0)
        else:
            self.sword = []

    def update_target(self, cond, final=False, verbose=False):
        if verbose:
            print("*Updating target")
        if not cond:
            return True
        if 'gen' in cond:
            troot, tfs, sPOSs = cond['gen']
            if troot == '?t':
                if not isinstance(sPOSs, list):
                    sPOSs = [sPOSs]
                # Use the translation of sroot
                # find sroot and sanal
                anals = []
                for spos in sPOSs:
                    if spos in self.sword[1]:
                        anals.extend(self.sword[1][spos])
                if not anals:
                    if verbose:
                        print("No analyses found for {}".format(sPOSs))
                # Just get one analysis
                sroot, sanal = anals[0] # self.sword[1][spos][0]
                trans = Multiling.get_translations(sroot, self.s2tlex, self.tlang,
                                                   one_word=True, one=False, match_all=True)
                if not trans:
                    if verbose:
                        print('No translations for sroot {}'.format(sroot))
                    return False
                fs = self.fs
                if tfs:
                    # Should be a list of FeatStructs (or maybe a FSSet)
                    # Incorporate features in each
                    u_fs = []
                    for f in tfs:
                        if not isinstance(f, FeatStruct):
                            f = FeatStruct(f)
#                            print('Unifying state FS {} with arc gen FS {}'.format(fs.__repr__(), f.__repr__()))
                            u = simple_unify(fs, f)
                            if u == 'fail':
                                if verbose:
                                    print('Current FS failed to unify target condition')
                                return False
                            u_fs.append(u)
                    # Make a dict of POS FSTs: updated FSs for generation
                    pos_dct = {}
                    for t in trans:
                        pos_abbrev = t[1]
                        if pos_abbrev in pos_dct:
                            # Already recorded
                            continue
                        pos = self.get_target_pos(pos_abbrev)
                        # Combine the features in tfs with the default
                        pos_u_fs = [pos.update_FS(pos.defaultFS, t) for t in u_fs]
                        pos_dct[pos_abbrev] = pos_u_fs

                    new_out = []

                    for t in trans:
                        root = t[0]
                        pos_abbrev = t[1]
                        pos = self.get_target_pos(pos_abbrev)
                        features = pos_dct[pos_abbrev]
                        for f in features:
                            if not f:
                                continue
                            gen = Multiling.gen_target(root, f, pos, final=final, verbose=verbose)
                            for g in gen:
                                if self.output:
                                    for o in self.output:
                                        out = o + [g]
                                        new_out.append(out)
#                                        if final:
#                                            print(new_out)
                                else:
                                    new_out.append([g])
#                                    if final:
#                                        print(g)
                    if not new_out:
                        if verbose:
                            print('Generation failed')
                        return False
                    self.output = new_out
            elif sPOSs:
                # If there's a POSs, then generate the word with the given root
                # but treat this as a *target* POS
                pos = self.get_target_pos(sPOSs)
                fs = self.fs
                if tfs:
                    # Should be a list of FeatStructs (or maybe a FSSet)
                    # Incorporate features in each
                    u_fs = []
                    for f in tfs:
                        if not isinstance(f, FeatStruct):
                            f = FeatStruct(f)
#                            print('Unifying state FS {} with arc gen FS {}'.format(fs.__repr__(), f.__repr__()))
                            u = simple_unify(fs, f)
                            if u == 'fail':
                                if verbose:
                                    print('Current FS failed to unify target condition')
                                return False
                            u_fs.append(u)
                    # Combine the features in tfs with the default
                    pos_u_fs = [pos.update_FS(pos.defaultFS, t) for t in u_fs]
                    new_out = []
                    for f in pos_u_fs:
                        if not f:
                            continue
                        gen = Multiling.gen_target(troot, f, pos, final=final, verbose=verbose)
                        for g in gen:
                            if self.output:
                                for o in self.output:
                                    out = o + [g]
                                    new_out.append(out)
                            else:
                                new_out.append([g])
                    if not new_out:
                        if verbose:
                            print('Generation failed')
                        return False
                    self.output = new_out
            else:
                if self.output:
                    for i, o in enumerate(self.output):
                        self.output[i] = o + [troot]
                else:
                    self.output = [[troot]]
        return True

class TraArc:
    """
    Arc in a translation FST:
    1 input (source) condition
      a dict: {'word': string, 'root': string, 'feats': [POSs, FS]}
    2 output (target) condition
      a dict: {'words': string, 'gen': [POSs, ??]}
    3 FS update condition
      a dict: {'add': FS, 'copy': [FS feats]}
    """

    arcID = 0

    def __init__(self, scond, tcond, fscond, name='', sstate=-1, dstate=-1):
        self.scond = scond
        self.tcond = tcond
        self.fscond = fscond
        self.sstate = sstate
        self.dstate = dstate
        self.set_name(name)

    def __repr__(self):
        return '>>{}<<'.format(self.name)
# [[{} {} {}]]'.format(self.scond, self.tcond, self.fscond)

    def set_name(self, name):
        if name:
            self.name = name
        else:
            self.name = str(TraArc.arcID)
            TraArc.arcID += 1

##    def graphics(self):
##        start_graphics(self.values())

#    def load_fst(self):
#        for pos in self.values():
#            pos.load_fst()

##    def set_transfer_fs(self, fss):
##        '''Set the transfer FSs.'''
##        self.transfer_fss = fss
##
##    def transfer1(self, source, source_fs, target):
##        source_trans = FeatStruct()
##        source_trans[source] = source_fs
##        target_morphpos = self[target]
##        for fs in self.transfer_fss:
##            unify_fs = unify(source_trans, fs)
##            if unify_fs:
##                target_morphpos.assign_defaults(unify_fs[target])
##                return unify_fs
##
##    def transfer(self, source_lang, source_fss, target_lang):
##        """Root, FS pairs for generating target word(s)."""
##        target = []
##        for fs_set in source_fss:
##            for fs in fs_set:
##                target_fs = self.transfer1(source_lang, fs, target_lang)
##                if target_fs:
##                    # The source FS unifies with some transfer FS
##                    if target_lang in target_fs:
##                        target_glosses = target_fs[target_lang]['g'], split[',']
##                        for gloss in target_gloses:
##                            target.append((gloss, target_fs))
##        return target
                    
