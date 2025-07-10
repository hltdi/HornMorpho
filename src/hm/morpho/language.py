"""
This file is part of HornMorpho, which is part of the PLoGS project.

    <http://homes.soic.indiana.edu/gasser/plogs.html>

    Copyleft 2011-2025.
    PLoGS and Michael Gasser <gasser@iu.edu>.

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

Author: Michael Gasser <gasser@iu.edu>

Language objects, with support mainly for morphology (separate
Morphology objects defined in morphology.py).

-- 2011-07-18
   Languages now created from data in language file:
   Language.make(abbrev)
-- 2013-02
   Multiling, etc. created: for phrase translation FSTs.
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

import os, sys, re, copy, itertools, copy, time

LANGUAGE_DIR = os.path.join(os.path.dirname(__file__), os.pardir, 'languages')

#LANGUAGE_DIR = os.path.join(os.path.join(os.path.dirname(__file__), os.pardir), os.pardir, 'languages')
#LANGUAGE_DIR = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'languages')

from .morphology import *
from .anal import *
from .utils import some, segment
from .rule import *
from .um import *
from .ees import *
from .sentence import *
from .cg import *

## Regex for extracting root from segmentation string
SEG_ROOT_RE = re.compile(r".*{(.+)}.*")

## Regexes for parsing language data
# Language name
LG_NAME_RE = re.compile(r'\s*name.*?:\s*(.*)')
# Target language name and abbrev (for translation)
TL_NAME_RE = re.compile(r'\s*tln.*?:\s*(.*)\s+(.*)')
# Backup language abbreviation
# l...:
BACKUP_RE = re.compile(r'\s*l.*?:\s*(.*)')
# Archive version number
VERSION_RE = re.compile(r'version:\s*(.*)')
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
# pos: v verb
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
# Pre-processing for generation
GEN_PREPROC_RE = re.compile(r'\s*genpreproc.*?:\s*(.*)')
GEMINATION_RE = re.compile(r'\s*gem.*?:\s*.*')
# Added 2021.11.24
FEATNORM_RE = re.compile(r'\s*feat.*?norm.*?:\s*(.*)')
# Added 2022.10.09
ABBREVCHARS_RE = re.compile(r'\s*abb.*?ch.*?:\s*(.+)')
#FEATCONV1_RE = re.compile(r'\s*(.*)\s*->\s*(.*)')
# Added 2022.09.27
# Get the root from a segmentation string
SEG_ROOT_RE = re.compile(r'\{(.*)\}')
# Added 2023.02.24
# string_set_label={chars1, chars1, chars2, ...}
SS_RE = re.compile(r'(\S+)\s*=\s*\{(.*)\}')
# Added 2023.07.24
MTAX_RE = re.compile(r"\s*morphotax::\s*(.*)")
#MSEG_RE = re.compile("")
# Added 2023.07.24
LEMMAFEATS_RE = re.compile(r"\s*lemmafeats\s*[:=]\s*(.+)")
# Added 2024.04.26
UMCATS_RE = re.compile(r"\s*umcats\s*[:=]\s*(.+)")
# Added 2023.09.04
MWE_RE = re.compile(r"\s*mwe::\s*(.*)")
# Added 2023.09.29
NO_MWE_RE = re.compile(r"\s*nomwe")
# Added 2023.09.06; character normalization
NORM_RE = re.compile(r"\s*normal\w*::\s*(.*)")
# Added 2023.09.17; character combination (within stems)
CHARCOMB_RE = re.compile(r"\s*charcomb\w*::\s*(.*)")
# Added 2023.11.03; POS, UD features, lemmas to merge
MERGE_RE = re.compile(r"\s*merge::\s*(.*)")
# Added 2024.11.12; disambiguation and dependency assignment
CG_RE = re.compile(r"\s*CG:\s*(.+)")

# Find the parts in a segmentation string: POS, FEATS, LEMMA, DEPREL, HEAD INCR
SEG_STRING_RE = re.compile(r"\((?:@(.+?))?(?:\$(.+?))?(?:\*(.+?))?(?:\~(.+?))?(?:,\+(.+?))?\)")
# Separate the parts of a MWE segmentation string
MWE_SEG_STRING_RE = re.compile(r"(.*?)\{(.+?)\}(.*)")

## Regex for checking for non-ascii characters
ASCII_RE = re.compile(r'[a-zA-Z]')

class Language:
    '''A single Language.'''

    T = TDict()

    infixsep = '--'
    posmark = '@'
    featsmark = '$'
    lemmamark = '&'
    joinposfeats = ';'
    joinfeats = '|'
    joinpos = ','
    roottempsep = '+'

    namefreq = 100

    def __init__(self, label='', abbrev='', backup='',
                 # Target language, for translation
                 tlang='',
                 tlabbrev = '',
                 # Directory
                 ldir='',
                 # Preprocessing for analysis
                 preproc=None, procroot=None,
                 # Preprocessing for generation
                 gen_preproc=None,
                 # Post-processing for generation
                 postproc=None, postpostproc=None,
                 # Default root postprocessing for analysis
                 dflt_postproc_root=None,
                 seg_units=None, read_cache=False,
                 # string translation table for character normalization
                 charnorm=None,
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
                 roman=True,
                 # CG instances responsible for disambiguation (POS, features) and dependencies
                 disambigCG = None,
                 depCG = None,
                 citation_separate=True,
                 # 2025.6.11: version to accommodate different ways of handling features in CoNNL-U
                 morph_version=0):
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
        self.tlang = tlang
        self.tlabbrev = tlabbrev
        self.abbrev = abbrev or label[:3]
        # additional abbreviations for language
        self.codes = []
        # Backup language for term translation, etc.
        self.backup = backup
        self.morphology = None
        self.preproc = preproc
        self.gen_preproc = gen_preproc
        self.procroot = procroot
        self.postproc = postproc
        self.postpostproc = postpostproc
        self.dflt_postproc_root = dflt_postproc_root
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
        self.directory = ldir
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
        self.um = UniMorph(self, morph_version=morph_version)
        # Mapping from internal phone repr to standard repr
        self.phone_map = {}
        # Stringsets for parsing FSTs
        self.stringsets = {}
        # Character normalization
        self.charnorm = None
        # Character combination across morpheme boundaries
        self.charcombs = None
        # Dict of type ('pos', 'udfeats', 'lemma') and merge possibilities
        self.merges = None
        # Whether the orthography is roman
        self.roman = roman
        # Archive version number; added 2024.09.16
        self.version = 1.0
        # Disambiguation and syntactic CGs
        self.disambigCG = None
        self.depCG = None
#        # A tree of multi-word expressions
#        self.mwe = {}
#        # Feature normalization
#        self.featnorm = {}
        self.read_phon_file()

    def __str__(self):
        return self.label or self.abbrev

    def __repr__(self):
        return self.label or self.abbrev

    ### Paths to directories and files

    @staticmethod
    def get_lang_dir(abbrev):
        path = os.path.join(LANGUAGE_DIR, abbrev)
        if not os.path.exists(path):
            return False
#        print("Directory for {}: {}".format(abbrev, path))
        return path

    def get_dir(self):
        """Where data for this language is kept."""
        return os.path.join(LANGUAGE_DIR, self.abbrev)

    def get_data_file(self, morph_version=0):
        """Data file for language."""
        if morph_version:
            return os.path.join(self.directory, "{}_{}.lg".format(self.abbrev, morph_version))
        return os.path.join(self.directory, self.abbrev + '.lg')

    def get_log_file(self):
        '''
        Log file for language, for recording updates.
        '''
        return os.path.join(self.directory, self.abbrev + '.log')

    def get_phon_file(self):
        return os.path.join(self.directory, self.abbrev + '.ph')

    def get_stat_dir(self):
        """Statistics directory: root and feature frequencies
        for disambiguation."""
        return os.path.join(self.directory, 'stat')

    def get_root_freq_file(self):
        statdir = self.get_stat_dir()
        if statdir:
            return os.path.join(statdir, 'root.frq')

    def get_cg_dir(self):
        return os.path.join(self.directory, 'cg')

    def get_disambig_file(self):
        cgdir = self.get_cg_dir()
        if cgdir:
            return os.path.join(cgdir, 'disamb.cg')

    def get_dep_file(self):
        cgdir = self.get_cg_dir()
        if cgdir:
            return os.path.join(cgdir, 'dep.cg')

    ## CACHING

    def get_cache_dir(self):
        """File with cached analyses."""
        return os.path.join(self.directory, 'cache')

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

    def log(self, pos, note):
        mode = 'a'
        if not os.path.exists(self.get_log_file()):
            mode = 'w'
        with open(self.get_log_file(), mode, encoding='utf8') as file:
            now = time.strftime("%Y %b %d", time.localtime())
            string = "{}: POS {}\n\t{}".format(now, pos, note)
            print(string, file=file)

    ###
    ### CREATING LANGUAGE
    ###

    @staticmethod
    def make(name, abbrev, load_morph=False,
             segment=False, phon=False, simplified=False, experimental=False, mwe=False,
             guess=True, poss=None, pickle=True, translate=False, gen=False,
             morph_version=0, cg=False, annotate=False,
             ldir='', v5=True, ees=False, recreate=True,
             verbose=False):
        """Create a language using data in the language data file."""
        if ees:
            lang = EESLanguage(abbrev=abbrev, ldir=ldir, morph_version=morph_version)
        else:
            lang = Language(abbrev=abbrev, ldir=ldir, morph_version=morph_version)
        # Load data from language file
        loaded = lang.load_data(load_morph=load_morph, pickle=pickle, gen=gen,
                                segment=segment, phon=phon, recreate=recreate,
                                experimental=experimental, mwe=mwe,
                                translate=translate, simplified=simplified,
                                morph_version=morph_version, cg=cg, annotate=annotate,
                                v5=v5,
                                guess=guess, poss=poss, verbose=verbose)
        if not loaded:
            # Loading data failed somewhere; abort
            return
        return lang

    def load_data(self, load_morph=False, pickle=True, recreate=False,
                  segment=False, phon=False, guess=True, gen=False,
                  simplified=False, translate=False, experimental=False, mwe=False,
                  morph_version=0, cg=False, annotate=False,
                  v5=True, poss=None, verbose=True):
        if self.load_attempted:
            return
        self.load_attempted = True
        filename = self.get_data_file(morph_version=morph_version)
        print("Loading data from {}".format(filename))
        if not os.path.exists(filename):
            if verbose:
                print(Language.T.tformat('(No language data file for {} at {})', [self, filename], self.tlanguages))
        else:
            if verbose:
                print(Language.T.tformat('Loading language data from {}', [filename], self.tlanguages))
            with open(filename, encoding='utf-8') as stream:
                data = stream.read()
                self.parse(data, poss=poss, cg=cg, annotate=annotate, verbose=verbose)
#        print("** Parsed data for {}; morphology {}".format(self, self.morphology))
        if load_morph:
            if v5:
                if not self.load_morpho(ortho=True, phon=phon,
                                         guess=guess, translate=translate, mwe=mwe,
                                         pickle=pickle, recreate=recreate,
                                         verbose=verbose):
                    return False
            elif not self.load_morpho4(segment=segment, ortho=True, phon=phon,
                                      guess=guess, simplified=simplified, translate=translate,
                                      experimental=experimental, mwe=mwe,
                                      pickle=pickle, recreate=recreate,
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
#            print("** posmorph {}, dFS {}".format(posmorph, posmorph.defaultFS.__repr__()))
        return True

    def parse(self, data, poss=None, cg=False, annotate=False, verbose=False):
        """
        Read in language data from a file.
        """
        if verbose:
            print('Parsing data for', self)

        lines = data.splitlines()[::-1]

        postproc = ''
        preproc = ''

        abbrevchars = ''

        seg = []
        punc = []
        featnorm = []

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
        lemmafeats = {}
        umcats = {}
        segments = {}
        mwefeats = {}

        merges = {}

        # Whether this is a MWE FST for different POS
        mwe = {}

        feature_groups = {}

        chars = ''

        current = None

        current_msegs = []

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

            if line.endswith('::'):
                # This is the beginning of a multiline feature
#                line = line[:-1]
                # Join succeeding lines
                done = False
                while not done:
                    next_line = lines.pop().split('#')[0].strip()
#                    print("line {}, next line {}".format(line, next_line))
                    if not line:
                        continue
                    if next_line[-1] == '\\':
                        next_line = next_line[:-1]
                    elif next_line[-1] != ';':
                        done = True
                    line += next_line
#                print("** joined: {}".format(line))

#            print("** LINE: {}".format(line))

            m = SS_RE.match(line)
            if m:
                label, ss = m.groups()
                ss = {s.strip() for s in ss.split(',')}
                self.stringsets[label] = ss
#                print("** String set {}, ...".format(label))
                continue

            m = FEATNORM_RE.match(line)
            if m:
                current = 'featnorm'
                fcpos = m.group(1).strip()
                featnorm.append([fcpos])
                continue

            m = ABBREVCHARS_RE.match(line)
            if m:
                abbrevchars = m.group(1)
                continue

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

            m = TL_NAME_RE.match(line)
            if m:
                self.tlang, self.tlabbrev = m.groups()
                continue

            m = BACKUP_RE.match(line)
            if m:
                lang = m.group(1).strip()
                self.backup = lang
                self.tlanguages.append(lang)
                continue

            m = VERSION_RE.match(line)
            if m:
                version = m.group(1).strip()
                self.version = version
                continue

            m = PUNC_RE.match(line)
            if m:
                current = 'punc'
                punc = m.group(1).split()
                continue

            m = NORM_RE.match(line)
            if m:
                norm = m.groups()[0].strip()
                normin, normout = norm.split(';')
                normin = normin.replace(' ', '').replace('\t', '')
                normout = normout.replace(' ', '').replace('\t', '')
                self.charnorm = str.maketrans(normin, normout)
#                print("** charnorm {}".format(self.charnorm))
                continue

            m = CHARCOMB_RE.match(line)
            if m:
                charcombs = m.group(1)
                charcombs = [cc.strip().split(':') for cc in charcombs.split(";")]
                self.charcombs = []
                for suff, pre in charcombs:
                    dct = {}
                    pre = pre.split(',')
                    for p in pre:
                        p1in, p1out = p.split()
                        dct[p1in] = p1out
                    self.charcombs.append([suff, dct])
#                print("** charcombs {}".format(self.charcombs))
                continue

            m = MERGE_RE.match(line)
            if m:
                merge = m.group(1)
                for mm in merge.split(';;'):
                    typ, specs = mm.split(':')
                    typ = typ.strip()
                    s1, s2, s3 = specs.split(';')
                    spec_key = frozenset([s1.strip(), s2.strip()])
                    if typ in merges:
                        merges[typ][spec_key] = s3.strip()
                    else:
                        merges[typ] = {spec_key: s3.strip()}
                continue

            m = CG_RE.match(line)
            if m:
                if not cg:
                    print("Skipping Constraint Grammar")
                    continue
                types = m.group(1)
                types = types.split()
                for typ in types:
                    if typ.startswith("dep") and annotate:
                        self.depCG = CG(self, disambig=False)
                        print("Loading disambiguation CG rules...")
                    elif typ.startswith("dis"):
                        self.disambigCG = CG(self, disambig=True)
                        print("Loading dependency CG rules...")
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
                self.preproc = eval(preproc)
                continue

            m = GEN_PREPROC_RE.match(line)
            if m:
                gen_preproc = m.group(1)
                self.gen_preproc = eval(gen_preproc)
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
                self.postproc = eval(postproc)
#                print("^^ postproc: {}".format(postproc))
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
#                    print("** {}".format(line))
                    pos, fullp = m.groups()
                    pos = pos.strip()
                    fullp = fullp.strip().replace('_', ' ')
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
                    # default values for these 3; overridden if there are specific features in data file
                    lemmafeats[pos] = []
                    umcats[pos] = {}
                    segments[pos] = []
                    mwefeats[pos] = []
                    continue

                m = MTAX_RE.match(line)
                if m:
                    segs = m.groups()[0].strip()
                    # prefixes, stem, suffixes
                    segs = segs.split(';;')
                    pre_segs, stem_segs, suf_segs = [segs[0].split(';'), segs[1], segs[2].split(';')]
#                    print("**  pre_segs {}".format(pre_segs))
                    # there may be no prefixes
                    if any(pre_segs):
                        pre_segs = [eval(s) for s in pre_segs]
                    else:
                        pre_segs = []
                    stem_segs = eval(stem_segs)
                    # there may be no suffixes
#                    for s in suf_segs:
#                        print("suf seg {}".format(s))
                    suf_segs = [eval(s) for s in suf_segs]
                    segs = [pre_segs, stem_segs, suf_segs]
                    segments[pos] = segs
                    continue

                m = MWE_RE.match(line)
                if m:
                    mwefeats1 = m.groups()[0].strip()
                    mwefeats1 = eval(mwefeats1)
#                    print("** mwe_specs {}".format(mwefeats1))
                    mwefeats[pos] = mwefeats1
                    continue

                m = NO_MWE_RE.match(line)
                if m:
                    mwe[pos] = False
                    continue

                m = LEMMAFEATS_RE.match(line)
                if m:
                    lemfeats = m.groups()[0].strip()
                    # if there is a semicolon, the feature before the semicolon determines whether
                    # gen is called (e.g., d;a,v for Amh nouns)
                    lemfeats = lemfeats.split(';')
                    if len(lemfeats) == 2:
                        lemfeats1, lemfeats2 = lemfeats
                    else:
                        lemfeats1 = ''
                        lemfeats2 = lemfeats[0]
                    lemfeats2 = [lf.strip() for lf in lemfeats2.split(',')]
#                    print("** lemmafeats {}".format(lemfeats))
                    lemmafeats[pos] = [lemfeats1, lemfeats2]
                    continue

                m = UMCATS_RE.match(line)
                if m:
                    umc = m.groups()[0].strip()
                    umc = eval(umc)
                    if not isinstance(umc, set):
                        umc = set(umc)
#                    print("umc {}".format(umc))
                    umcats[pos] = umc
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

            elif current == 'featnorm':
                oldf, newf = line.strip().split('->')
                oldf = oldf.strip()
                newf = newf.strip()
#                if oldf[0] != '[':
#                    oldf = '[' + oldf + ']'
#                if newf[0] != '[':
#                    newf = '[' + newf + ']'
                oldf = FeatStruct(oldf)
                newf = FeatStruct(newf)
                featnorm[-1].append((oldf, newf))

            else:
                raise ValueError("bad line: {}".format(line))

        if punc:
            punc = r'[' + ''.join(punc) + ']'
#        if punc and isinstance(punc, list):
#            # Make punc list into a string
#            punc = ''.join(punc)

        if seg:
            # Make a bracketed string of character ranges and other characters
            # to use for re
            chars = ''.join(set(''.join(seg)))
            chars = self.make_char_string(chars)
            # Make the seg_units list, [chars, char_dict], expected for transduction,
            # composition, etc.
            self.seg_units = self.make_seg_units(seg)

        self.merges = merges

        if feats and not self.morphology:
            pos_args = []
            for pos in feats:
                if not poss or pos in poss:
                    # Make feature_groups into a list, sorted by length of feature matches
                    fgroups = list(feature_groups[pos].items())
                    fgroups.sort(key=lambda x: -len(x[0]))
                    pos_args.append((pos, feats[pos], lex_feats[pos], excl[pos], abbrev[pos],
                                     fv_abbrev[pos], fv_dependencies[pos], fv_priorities[pos],
                                     fgroups, fullpos[pos], explicit[pos], true_explicit[pos],
                                     lemmafeats[pos], umcats[pos], segments[pos], mwefeats[pos], mwe.get(pos, True)))
            morph = Morphology(pos_morphs=pos_args,
                               punctuation=punc, characters=chars, abbrev_chars=abbrevchars)
            self.set_morphology(morph)
        elif self.morphology and abbrevchars:
            self.morphology.abbrev_chars = abbrevchars

        if featnorm:
            # Convert featnorm list to dict
            # This needs to happen after morphology and POSMorphology
            # objects are created.
            if not self.morphology:
                print("No morphology!")
            for fn in featnorm:
                # first element is POS, rest is old-new feature pairs
                fnpos = fn[0]
                fnfeats = fn[1:]
                posmorph = self.morphology.get(fnpos)
                if not posmorph:
                    print("No {} posmorph".format(fnpos))
                posmorph.featnorm = fnfeats

    ###
    ### Character conversion of various sorts.
    ###

    def transliterate(self, token):
        return self.romanize(token, ipa=True)

    def normalize(self, string):
        '''
        Normalize the string using the language's charnorm translation table if there is one.
        '''
        charnorm = self.charnorm
        if not charnorm:
            return string
        return string.translate(charnorm)

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
            if phone == ' ':
                cons = []
            elif phone not in vowels:
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

    def convert_phones(self, phones, gemination=True,
                       epenthesis=True, ipa=False):
        """
        Convert a sequence of phones (an unsegmented string)
        to an alternate phone representation.
        """
#        print("Convert phones {}, epenthesis {}".format(phones, epenthesis))
        phones = segment(phones, self.seg_units, correct=False)
#        if epenthesis:
#            self.epenthesis(phones)
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
        return self.convert_phones(root, gemination=False,
                                   epenthesis=False, ipa=ipa)

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
                     pickle=True, mwe=False, translate=False, suffix='',
                     recreate=False, guess=True, verbose=False):
        """
        Load words and FSTs for morphological analysis and generation.
        New method for version 5.
        """
#        print("&& load_morpho {}".format(guess))
        fsts = fsts or (self.morphology and self.morphology.pos)
#        opt_string = 'MWE_' if mwe else ''
        opt_string = ''
        if phon:
            opt_string += 'phonetic'
        else:
            opt_string += 'analysis/generation'
        print("Loading FSTs for {} (version {})".format(self, self.version))
        # In any case, assume the root frequencies will be needed?
        self.morphology.set_root_freqs()
#        self.morphology.set_feat_freqs()
        if ortho:
            # Load unanalyzed words
            self.morphology.set_words(ortho=True)
            self.morphology.set_suffixes(verbose=verbose)
            self.morphology.set_abbrevs()
        if phon:
            # Load unanalyzed words
            self.morphology.set_words(ortho=False)
            self.morphology.set_suffixes(verbose=verbose)
        if not fsts:
            return False
        for pos in fsts:
#            # Load pre-analyzed words if any
            self.morphology[pos].set_analyzed(ortho=ortho, simplify=False)
            if ortho:
                self.morphology[pos].make_generated()
            # Load phonetic->orthographic dictionary if file exists
            if ortho:
                self.morphology[pos].set_ortho2phon()
            # Load lexical anal and gen FSTs (no gen if segmenting)
            if ortho:
                self.morphology[pos].load_fst(gen=False, create_casc=False, pickle=pickle,
                                              experimental=False, mwe=False,
                                              phon=False, segment=False, translate=translate,
                                              gemination=self.output_gemination, v5=True, suffix=suffix,
                                              pos=pos, recreate=recreate, verbose=verbose)
                if mwe and self.morphology[pos].mwe:
                    self.morphology[pos].load_fst(gen=False, create_casc=False, pickle=pickle,
                                                  experimental=False, mwe=True,
                                                  phon=False, segment=False, translate=translate,
                                                  gemination=self.output_gemination, v5=True, suffix=suffix,
                                                  pos=pos, recreate=recreate, verbose=verbose)
            # Load generator for both analysis and segmentation
#            if phon or (ortho and not segment):
            self.morphology[pos].load_fst(gen=True, create_casc=False, pickle=pickle,
                                          experimental=False, mwe=False,
                                          phon=phon, segment=False, translate=translate,
                                          gemination=self.output_gemination, v5=True, suffix=suffix,
                                          pos=pos, recreate=recreate, verbose=verbose)
            if mwe and self.morphology[pos].mwe:
                self.morphology[pos].load_fst(gen=True, create_casc=False, pickle=pickle,
                                              experimental=False, mwe=True,
                                              phon=phon, segment=False, translate=translate,
                                              gemination=self.output_gemination, v5=True, suffix=suffix,
                                              pos=pos, recreate=recreate, verbose=verbose)
            # Load guesser anal and gen FSTs
            if guess:
                if ortho:
                    self.morphology[pos].load_fst(gen=False, guess=True, phon=False,
                                                  segment=False, translate=translate,
                                                  pickle=pickle, create_casc=False,
                                                  experimental=False, mwe=False,
                                                  gemination=self.output_gemination, v5=True, suffix=suffix,
                                                  pos=pos, recreate=recreate, verbose=verbose)
                # Always load phonetic generation guesser
                if phon:
                    self.morphology[pos].load_fst(gen=True, guess=True, phon=True, segment=segment,
                                                  create_casc=False, pickle=pickle, experimental=False, mwe=False,
                                                  translate=translate, v5=True,
                                                  gemination=self.output_gemination, suffix=suffix,
                                                  pos=pos, recreate=recreate, verbose=verbose)
            # Load statistics for generation
            self.morphology[pos].set_root_freqs()
            self.morphology[pos].set_feat_freqs()

        self.morpho_loaded = True
        return True

    def get_fsts(self, generate=False, phon=False, experimental=False, mwe=False,
                 v5=True,
                 simplified=False, segment=False, translate=False):
        '''Return all analysis FSTs (for different POSs) satisfying phon and segment contraints.'''
        fsts = []
        for pos in self.morphology.pos:
            if phon:
                fst = self.morphology[pos].get_fst(generate=True, phon=True, experimental=experimental, mwe=mwe, v5=v5)
            else:
                fst = self.morphology[pos].get_fst(generate=generate, segment=segment, experimental=experimental, mwe=mwe, v5=v5)
            if fst:
                fsts.append(fst)
        return fsts

    def has_cas(self, generate=False, guess=False, experimental=False, mwe=False,
                simplified=False, phon=False, segment=False):
        """Is there at least one cascade file for the given FST features?"""
        if not self.morphology:
            return False
        for pos in self.morphology.pos:
            if self.morphology[pos].has_cas(generate=generate, simplified=simplified,
                                            experimental=experimental, mwe=mwe,
                                            guess=guess, phon=phon, segment=segment):
                return True
        return False

#    def get_trans(self, word):
#        return self.trans.get(word, word)

    ###
    ### ANALYZING WORDS AND SENTENCES
    ###

    def analyze(self, raw_token, **kwargs):
        '''
        Analyze a token according to HM 5.0, returning a Word object.
        kwargs: mwe=False, conllu=False, degem=True, sep_feats=True, combine_segs=False, verbosity=0
        '''
#        print("** analyze5 kwargs {}".format(kwargs))
        all_analyses = []
        # Analyze multiple tokens
        mwe = kwargs.get('mwe', False)
        # There may be a cache dict where the analyses can be found or stored.
        cache = kwargs.get('cache')
        # Try different POSs, but restrict these if 'pos' is in kwargs
        analpos = kwargs.get('pos')
        guess = kwargs.get('guess', False)
        feats = kwargs.get('feats')
        timeit = kwargs.get('timeit')
        skip_pos = analpos and kwargs.get('skip_pos', True)
#        roots = kwargs.get('roots', None)
        if timeit:
            starttime = time.time()
        # Character normalization
        normalized = False
        def special_word():
            wordobj = Word.create_empty(None if mwe else raw_token)
            if isinstance(cache, dict) and not mwe:
                cache[raw_token] = wordobj
            return wordobj
        token = self.normalize(raw_token)
        if token != raw_token:
            normalized = True
        if not isinstance(cache, dict):
            cache = {}
        cached = cache.get(token)
        if cached is not None:
            # This assumes the cache stores "processed" analyses (Word instances)
            copy = cached.copy(name=raw_token)
#            print("Copying cached word {}".format(copy))
            return copy
        # punctuation, numerals; skip if feats are specified
        if not feats:
            special_anal = self.analyze_special(token)
            if special_anal:
                special_anal = self.check_analpos(special_anal, analpos)
                # If this is a numeral, punctuation, or abbreviation, don't bother going further.
                wordobj = Word(special_anal, name=raw_token, merges=self.merges) if special_anal else Word.create_empty(raw_token)
                if isinstance(cache, dict):
                    cache[token] = wordobj.copy(name=raw_token)
                return wordobj
            # Try unanalyzed words or MWEs
            unanalyzed = self.analyze_unanalyzed5(token, mwe=mwe, analpos=analpos)
            if unanalyzed:
                if analpos:
                    return special_word()
                else:
                    all_analyses.extend(unanalyzed)
        # if there is an analpos, first try other POS and fail (because of ambiguity) if any succeeds
        if analpos and not skip_pos:
            for pos, pmorph in self.morphology.items():
                if pos in analpos:
                    continue
                analyses = pmorph.anal(token, mwe=mwe, guess=guess, feats=feats)
                if analyses:
                    return special_word()
        for pos, pmorph in self.morphology.items():
            if analpos and pos not in analpos:
#                print("Skipping analysis of {} for {}".format(token, pos))
                continue
            analyses = pmorph.anal(token, mwe=mwe, guess=guess, feats=feats)
#            if analyses:
#                print("** analyses 1: {}".format(len(analyses)))
            if analyses:
                analyses = pmorph.process_all5(token, analyses, raw_token if normalized else '', **kwargs)
#                print("** analyses 2: {}".format(len(analyses)))
                all_analyses.extend(analyses)
        if not all_analyses:
            return special_word()
        wordobj = Word(all_analyses, name=raw_token, merges=self.merges)
        cache[token] = wordobj
        wordobj.arrange()
        if timeit:
            print("Time taken: {}".format(time.time() - starttime))
#        if not feats or not wordobj.is_empty():
        return wordobj

    def check_analpos(self, analysis, analpos):
#        print("** Checking analpos {} for {}".format(analpos, analysis))
        if not analpos:
            return [analysis]
        else:
            thispos = analysis['pos']
            if thispos not in analpos and thispos.lower() not in analpos:
                return []
            return [analysis]

    def analyze_unanalyzed5(self, word, mwe=False, analpos=[]):
        '''
        Look for the unanalyzed form of the word, returning the default in dict anal format.
        '''
        words = self.morphology.wordsM if mwe else self.morphology.words1
        anal = {'token': word, 'nsegs': 1, 'pos': ''}
        if not self.roman:
            trans = self.transliterate(word)
            anal['misc'] = ["Translit={}".format(trans)]
        if word in words:
#            print("** Looking for word {}".format(word))
            pos = ''
            feats = ''
            freq = self.morphology.get_freq(word)
            lex = words.get(word)
#            lex = self.morphology.words1[word]
            if len(lex) == 1:
                pos = lex[0]
                anal['freq'] = freq
                return [anal]
#                return [{'token': word, 'pos': pos, 'nsegs': 1, 'freq': freq}]
#            form, cats = self.morphology.words1[word]
            form, cats = words.get(word)
            if cats[0] == '[':
                # These are HM features
                feats = FeatStruct(cats)
                pos = feats.get('pos', '')
            elif cats.startswith('um='):
                # These are UM features
                feats = cats.split("|")
                # There may be more than one
                if len(feats) > 1:
                    f = [feats[0].split('=')[1]]
                    f.extend(feats[1:])
                    anals = []
                    for ff in f:
                        pos = ff.split(';')[0]
                        anals.append({'token': form, 'pos': pos, 'nsegs': 1, 'freq': freq, 'um': ff})
                    return anals
                else:
                    f = feats[0].split('=')[1]
                    pos = f.split(';')[0]
                    anal['pos'] = pos
                    anal['um'] = f
                    return [anal]
#                    return [{'token': form, 'pos': pos, 'nsegs': 1, 'freq': freq, 'um': f}]
            else:
                pos = cats
            freq = self.morphology.get_freq(word)
            tokens = form.split()
            nsegs = len(tokens)
            anal['freq'] = freq
            anal['nsegs'] = nsegs
            anal['pos'] = pos
#            anal = {'token': form, 'pos': pos, 'nsegs': nsegs, 'freq': freq}
            if nsegs > 1:
                dep = 'fixed'
                # MWE
                # Later have the FSS already storied in words1
                token_list = []
                mwe_feats = feats.get('mwe') if feats else Noe
                token_pos = mwe_feats.get('tokpos') if mwe_feats else None
                # There may be explicit POSs for tokens in the form of a FS tuple
                for ti, tok in enumerate(tokens):
                    tdict = {'token': tok}
                    if token_pos:
                        tdict['pos'] = token_pos[ti]
                    token_list.append(tdict)
                anal['tokens'] = token_list
                if mwe_feats:
                    if dep := mwe_feats.get('dep'):
                        anal['dep'] = dep
                if dep in ('fixed', 'flat'):
                    # head is first token, other tokens are "suffixes"
                    tok = tokens[0]
                    anal['stem'] = {'seg': tok, 'head': 0, 'pos': pos}
                    #token_list[0].get('pos', 'N')}
                    anal['suf'] = []
                    for ti, tok in enumerate(tokens[1:]):
                        anal['suf'].append({'seg': tok, 'head': 0, 'dep': dep, 'pos': None})
                        #token_list[ti+1].get('pos', 'N'))
                else:
                    # head is last token, other tokens are "prefixes"
                    tok = tokens[-1]
                    anal['stem'] = {'seg': tok, 'head': nsegs-1, 'pos': pos}
                    #token_list[-1].get('pos', 'N')}
                    anal['pre'] = []
                    for ti, tok in enumerate(tokens[-1]):
                        anal['pre'].append({'seg': tok, 'head': nsegs-1, 'dep': dep, 'pos': None})
                        #token_list[ti].get('pos', 'N'), 'dep': dep})
#            token_list = [{'token': t} for t in tokens]
            if feats:
                anal['feats'] = feats
            if anal:
                return [anal]
#                return self.check_analpos(anal, analpos)

    def analyze_special(self, token):
        '''
        Handle special cases, currently abbreviations, numerals, and punctuation.
        '''
        if self.morphology.is_punctuation(token):
            return {'pos': 'PUNCT', 'token': token, 'lemma': token, 'nsegs': 1}
        if abb := self.morphology.get_abbrev(token):
            expansion, pos = abb
            tokens = expansion.split()
            return {'pos': pos, 'xpos': 'ABBR', 'token': token, 'lemma': token, 'tokens': tokens, 'nsegs': 1}
        # Check numeral before abbreviation
        numeral = self.morphology.match_numeral(token)
        if numeral:
            prenum, num, postnum = numeral
            if postnum:
                return {'token': token, 'pos': 'N', 'lemma': postnum, 'nsegs': 1}
            elif prenum:
                return {'token': token, 'pos': 'N', 'lemma': num, 'nsegs': 1}
            else:
                return {'token': token, 'pos': 'NUM', 'lemma': token, 'nsegs': 1}
        if self.morphology.is_abbrev(token):
            return {'pos': 'N', 'xpos': 'ABBR', 'token': token, 'lemma': token, 'nsegs': 1}
        return None

    def combine_segments(self, stem_string):
        '''
        Return the string with stem segments combined.
        '''
#        print("** combining segments in {}".format(stem_string))
        if self.charcombs:
            for suf, prefixes in self.charcombs:
                if suf in stem_string:
                    previous = stem_string.split(suf)[0][-1]
                    if previous in prefixes:
                        replacement = prefixes[previous]
                        stem_string = stem_string.replace(previous + suf, replacement)
        return stem_string.replace(Morphology.morph_sep, '')

    def anal_sentence(self, sentence, **kwargs):
        '''
        Version 5:
        Analyze the tokens in a sentence (a string), returning a Sentence object.
        Try MWEs before single tokens.
        kwargs: degem, sep_feats, combine_segs, verbosity, pos, props
        '''
#        print("^^ sentence {}, kwargs {}".format(sentence, kwargs))
        skip_mwe = kwargs.get('skip_mwe', False) or kwargs.get('feats', False)
        if 'cache' not in kwargs:
            kwargs['cache'] = dict()
        timeit = kwargs.get('timeit', False)
        if timeit:
            starttime = time.time()
            # do this to prevent timing of individual token analysis
            kwargs['timeit'] = False
        tokens = sentence.split()
        ntokens = len(tokens)
        sentobj = Sentence(sentence, self, **kwargs)
#            sentence, language=self, batch_name=kwargs.get('batch_name', ''), sentid=kwargs.get('sentid', 1), label=kwargs.get('label'))
        token_index = 0
        while token_index < ntokens:
            if skip_mwe:
                mwe_anal, new_index = None, token_index
            else:
                mwe_anal, new_index = self.anal_mwe1(tokens, token_index, sentobj, **kwargs)
            if mwe_anal:
                token_index = new_index
            else:
                kwargs['mwe'] = False
                token = tokens[token_index]
                token_index += 1
                if skip := kwargs.get('skip'):
                    if token in skip:
                        continue
                anal1 = self.analyze(token, **kwargs)
                if not isinstance(anal1, Word):
                    print("*** Analysis of {} is not a Word!".format(token))
                sentobj.add_word5(anal1, unsegment=kwargs.get('unsegment', False))
#        if 'props' in kwargs:
#            sentobj.set_props(kwargs['props'])
        if timeit:
            print("Time taken: {}".format(time.time() - starttime))
        return sentobj

    def anal_mwe1(self, tokens, token_index, sent_obj, **kwargs):
        '''
        Attempt to analyze a MWE within tokens starting from token_id.
        '''
        max_mwe = kwargs.get('max_mwe', 3)
        words = tokens[token_index]
        end_index = token_index + 1
        timeit = kwargs.get('timeit', False)
        if timeit:
            starttime = time.time()
        while end_index < len(tokens):
            next_word = tokens[end_index]
            if self.morphology.is_punctuation(next_word) or self.morphology.is_punctuation(next_word):
                return False, token_index
            words = words + ' ' + next_word
#            print("^^ attempting to analyze {}".format(words))
            kwargs['mwe'] = True
            analyses = self.analyze(words, **kwargs)
            if analyses.is_known():
#                print("** analyses {}".format(analyses))
                if not isinstance(analyses, Word):
                    print("*** Analysis of {} is not a Word!".format(tokens))
                sent_obj.add_word5(analyses, unsegment=kwargs.get('unsegment', False))
#                print("  ** Success: {}".format(analyses[0]))
                return True, end_index + 1
            end_index += 1
        if timeit:
            print("Time taken: {}".format(time.time() - starttime))
        return False, token_index

    def anal_sentence5_1(self, sentence, **kwargs):
        '''
        Version 5:
        Analyze the tokens in a sentence (a string), returning a Sentence object.
        kwargs: degem, sep_feats, combine_segs, verbosity
        '''
        if 'cache' not in kwargs:
            kwargs['cache'] = dict()
        tokens = sentence.split()
        sentobj = Sentence(sentence, self)
        # For now just try single-word tokens.
        for token in tokens:
            wordobj = self.analyze(token, **kwargs)
            if not isinstance(wordobj, Word):
                print("*** Analysis of {} is not a Word!".format(token))
            sentobj.add_word5(wordobj, unsegment=kwargs.get('unsegment', False))
        if 'props' in kwargs:
            sentobj.set_props(kwargs['props'])
        return sentobj

    def anal_sent_mwe(self, sentence, sent_obj, **kwargs):
        '''
        Analyze the tokens using the MWE FSTs.
        '''
        tokens = sentence.split()
        sent_obj = sent_obj or Sentence(sentence, self)
        seglevel = kwargs.get('seglevel', 2)
        ntokens = len(tokens)
        w_index = 0
        morphid = 0
        while w_index < ntokens:
            word = tokens[w_index]
            simps = None
            words = None
            if w_index < len(tokens)-1:
                next_word = tokens[w_index+1]
                if not self.morphology.is_punctuation(word) and not self.morphology.is_punctuation(next_word):
                    words = word + " " + next_word
            if words:
                print("** Attempting to analyze {}".format(words))
                kwargs['mwe'] = True
                analyses = self.analyze(words, **kwargs)
                if analyses:
                    if not isinstance(analyses, Word):
                        print("*** Analysis of {} is not a Word!".format(words))
                    sent_obj.add_word5(analyses, unsegment=kwargs.get('unsegment', False))
                    print("  ** Success: {}".format(analyses[0]))
                    w_index += 2
                    if seglevel == 0:
                        morphid += 1
                    else:
                        # Just use the first analysis
                        morphid += analyses[0]['nsegs']
                else:
                    w_index += 1
                    morphid += 1
            else:
                print("** No MWE possibilities: {}".format(tokens[w_index:]))
                w_index += 1
                morphid += 1
        return sent_obj

    def disambiguate(self, sentence, verbosity=0):
        '''
        Disambiguate the sentence using the language's disamb rules if any.
        '''
#        if not self.disambigCG:
#            print("No CG!")
#        elif not self.disambigCG.initialized:
#            print("CG not initialized!")
        if self.disambigCG and self.disambigCG.initialized:
            return self.disambigCG.run(sentence, verbosity=verbosity)

    def annotate(self, sentence, verbosity=0):
        '''
        Annotate the sentence using the language's dependency rules if any.
        '''
        if self.depCG and self.depCG.initialized:
            return self.depCG.run(sentence, verbosity=verbosity)

    def _anal_sentence5(self, sentence,
                       conllu=True, xml=None, multseg=False, dicts=None, xsent=None,
                       sep_punc=False, word_sep='\n', sep_ident=False, minim=False,
                       feats=None, simpfeats=None, um=0, normalize=False,
                       nbest=100, report_freq=False, report_n=50000,
                       remove_dups=True, seglevel=2,
                       batch_name='', local_cache=None, sentid=0, morphid=1,
                       verbosity=0):
        sentlist = []
        local_cache = local_cache if isinstance(local_cache, dict) else {}
        tokens = sentence.split()
        ntokens = len(tokens)
        w_index = 0
        while w_index < ntokens:
            word = tokens[w_index]
            simps = None
            words = None
            if w_index < len(tokens)-1:
                next_word = tokens[w_index+1]
                if not self.morphology.is_punctuation(word) and not self.morphology.is_punctuation(next_word):
                    words = word + " " + next_word
            if words:
                if self.get_from_cache5(words, local_cache, um=um, seglevel=seglevel, conllu=conllu, sentlist=sentlist, morphid=morphid,
                                       verbosity=verbosity
                                                 ):
                    # MWE analysis stored in cache
                    w_index += len(words.split())
                    continue
                # Attempt to analyze MWE
                analyses = self.analyze(words, mwe=True, conllu=conllu, gemination=gemination, sepfeats=sepfeats)
                if analyses:
                    if seglevel == 0:
                        morphid += 1
                    else:
                        morphid += len(analyses[0])
            # Analyze single word
            if verbosity:
                print("**  Analyzing word {}".format(word))
            # Lowercase on the first word, assuming a line is a sentence
            if self.get_from_cache5(word, local_cache, um=um, seglevel=seglevel, morphid=morphid, sentlist=sentlist, conllu=conllu,
                                    verbose=verbose
                                        ):
                w_index += 1
                continue
            if not analyses:
                ## Analyze
                analyses = \
                  self.analyze(word, mwe=False, conllu=conllu, gemination=gemination, sepfeats=sepfeats)
                if analyses:
                  if seglevel == 0:
                      morphid += 1
                  else:
                      morphid += len(analyses[0])
            # Go to next word
            w_index += 1
        # End of sentence
        return sentlist

    def get_from_cache5(self, word, cache, sentlist=None, sentobj=None,
                        filter_cache=None, filtered=None, gramfilter=None,
                        verbosity=0):
        if word in cache:
            print("** Getting {} from local cache".format(word))
            analysis = cache[word]
            sentlist.append((word, analysis))
            return True
        return False

    def postprocess5(self, form):
        '''
        Postprocess a form if there's a postproc function.
        '''
        if self.postproc:
            return self.postproc(form)
        return form

    def gen_preprocess(self, form):
        '''
        Preprocess a form before generating if there's a gen_preproc function.
        '''
        if self.gen_preproc:
            return self.gen_preproc(form)
        return form

    ### Old functions (HM 4)

#    def preprocess(self, form):
#        '''Preprocess a form.'''
#        if self.preproc:
#            res = self.preproc(form)
#            if type(res) == tuple:
#                # preproc() may also return number of simplifications
#                return res[0]
#            return res
#        return form

#    def postprocess(self, form, phon=False, ipa=False, ortho_only=False,
#                    phonetic=True):
#        '''Postprocess a form.'''
#        if self.postproc:
#            return self.postproc(form, phon=phon, ipa=ipa,
#                                 ortho_only=ortho_only, phonetic=phonetic)
#        return form

#    def postpostprocess(self, form):
#        '''Postprocess a form that has already been postprocessed.'''
#        if self.postpostproc:
#            return self.postpostproc(form)
#        return form

    ## Methods related to segmentation

    def seg2morphs(self, seg, pos=None, joininfixes=True):
        '''
        Returns the morphemes in a segmentation string, and index of the root.
        '''
        if joininfixes:
            # Remove the string separating an infix from a following suffix
            seg = seg.replace(Language.infixsep, '')
        # separate morphemes
        morphs = seg.split(Morphology.morph_sep)
        rootindex = -1
        for index, morph in enumerate(morphs):
            if '(' in morph:
                morph = morph.split('(')
                morph = [morph[0], '(' + morph[1]]
            else:
                morph = [morph, '']
            form = morph[0]
            if '{' in form:
                form = form[1:-1]
                morph[0] = form
                rootindex = index
            morphs[index] = morph
        return morphs, rootindex

    def seg2root(self, seg):
        """Returns the root morpheme (form, features) for a segmentation string."""
        morphs = self.seg2morphs(seg)
        return morphs[0][morphs[1]]

    def segmentation2string(self, word, segmentation, sep='-', transortho=True, features=False,
                            um=0, udformat=False, simplifications=None, conllu=True):
        '''
        Convert a segmentation (POS, segstring, count) to a form string,
        using a language-specific function if there is one, otherwise using a default function.
        '''
        if self.seg2string:
            return self.seg2string(word, segmentation, sep=sep, transortho=transortho,
                                   udformat=udformat, simplifications=simplifications, um=um, conllu=conllu)
        else:
            morphs = [m[0] for m in self.seg2morphs(segmentation[1])]
            # This ignores whatever alternation rules might operate at boundaries
            return sep.join(morphs)

    @staticmethod
    def root_from_segstring(string, template=False):
        '''
        Get the root, minus the template if template is False,
        from the segmentation string.
        '''
        m = SEG_ROOT_RE.search(string)
        if m:
            root = m.group(1)
            if not template:
                root = root.split(Language.roottempsep)[0]
            return root
        return ''

    @staticmethod
    def udformat_posfeats(string, dropfeats=['ውልድ'], conllu=True):
        '''
        string is ([@pos,...,][$feat],[*lemma],[~deprel]).
        format string as in UD.
        '''
        feats = None
        match = SEG_STRING_RE.match(string)
        if not match:
            print("** segstring {} doesn't match RE!".format(string))
            return {}
        else:
            pos, feats, lemma, deprel, headi = match.groups()
            if headi and headi.isdigit():
                headi = int(headi)
            if lemma:
                lemma = lemma.replace(',', '')
        if feats:
            feats = Language.udformat_feats(feats, dropfeats=dropfeats)
        else:
            feats = None
        if pos:
            pos = Language.udformat_pos(pos)
        else:
            pos = None
        if conllu:
#            print("** result {}".format({'lemma': lemma, 'pos': pos, 'feats': feats, 'deprel': deprel, 'head': headi}))
            return {'lemma': lemma, 'pos': pos, 'feats': feats, 'deprel': deprel, 'head': headi}
        else:
            return "(" + Language.joinposfeats.join(pos + feats) + ")"

    @staticmethod
    def udformat_pos(pos):
        '''
        Delete POS char (@) and uppercase pos name(s).
        '''
        poss = pos.split(',')
        poss = [Language.udformat_pos_fromHM(p.strip()) for p in poss if p]
        # Replace HM POS tags with UD tags
        return poss

    @staticmethod
    def udformat_pos_fromHM(pos):
        p = pos.replace('@', '')
        p = p.upper()
        if p == 'V':
            return 'VERB'
        elif p == 'N':
            return 'NOUN'
        elif p.startswith('NM'):
            return 'PROPN'
        elif p.startswith('N_'):
            return 'NOUN'
        else:
            return p

    @staticmethod
    def udformat_feats(feats, dropfeats=None):
        '''Delete feat char ($) and capitalize features and value.'''
        ffeats = [f.strip().split('=') for f in feats.split(',') if f]
        ffeats = ['='.join([Language.udformat_feat(f[0]), Language.udformat_value(f[1])]) for f in ffeats if f[0] not in dropfeats]
        if not ffeats:
            return None
        # Alphabetize by feature names
        ffeats.sort()
        return Language.joinfeats.join(ffeats)

    @staticmethod
    def udformat_feat(feat):
        '''Capitalize feature name, also capitalizing "Type" or "Class" if those are in the name.'''
        if 'type' in feat:
            return feat.split('type')[0].capitalize() + 'Type'
        elif 'class' in feat:
            return feat.split('class')[0].capitalize() + 'Class'
        elif feat == 'caurcp':
            return "CauRcp"
        elif feat == 'transrcp':
            return "TransRcp"
        else:
            return feat.capitalize()

    @staticmethod
    def udformat_value(value):
        '''
        Normally capitalize values.
        Make an except for values containing '_', like 'te_'.
        Replace / with , for ambiguous values.
        '''
        if '_' in value:
            return value
        value = value.replace('/', ',')
        return value.capitalize()

    def preprocess_file(self, filein, fileout):
        '''Preprocess forms in filein, writing them to fileout.'''
#        fin = codecs.open(filein, 'r', 'utf-8')
#        fout = codecs.open(fileout, 'w', 'utf-8')
        fin = open(filein, 'r', encoding='utf-8')
        fout = open(fileout, 'w', encoding='utf-8')
        for line in fin:
            fout.write(str(self.preprocess(line), 'utf-8'))
        fin.close()
        fout.close()

    ### MWEs

#    def get_mwes(self, lexfile, pos):
#        mwes = []
#        with open(lexfile, encoding='utf8') as file:
#            for line in file:
#                line = line.split('#')[0].strip() # strip comments
#                if line:
#                    token = line.split()[0]
#                    if Language.mwesep in token:
#                        mwes.append(token)
#        return mwes

    ### Analyze words or sentences

#    def analyze4(self, item, pos='v', mwe=False, guess=False, nbest=10):
#        posM = self.morphology.get(pos)
#        if not posM:
#            print(">>> No POS {} for this language <<<".format(posM))
#            return
#        analyses = posM.anal(item)
#        return analyses

    def anal_word(self, word, fsts=None, guess=True, only_guess=False,
                  phon=False, segment=False, init_weight=None, experimental=False, mwe=False,
                  um=1, gloss=True, phonetic=True, normalize=False, simplify=True,
                  ortho_only=False, lemma_only=False, sep_anals=True,
                  get_all=True, to_dict=False, preproc=False, postproc=False,
                  cache=False, no_anal=None, string=False, print_out=False,
                  display_feats=None, report_freq=True, nbest=100,
                  conllu=False, skip_other_pos=False,
                  only_anal=False, preseg=False, verbosity=0):
        '''
        Analyze a single word, trying all existing POSs, both lexical and guesser FSTs.
        If segment is True, this does morphological segmentation, with various
        things happening differently.
        If experimental is True, this uses the "experimental" (*X) FST, which
        could be a segmenter, in which case segment is also True, or an analyzer,
        in which case segment is False.
        '''
        # Before anything else, check to see if the word is in the list of
        # words that have failed to be analyzed
        if no_anal != None and word in no_anal:
            return None
        # Whether the analyses are found in the cache
        found = False
        preproc = preproc and self.preproc
        postproc = postproc and self.postproc
        normalize = normalize and not um
        analyses = []
        to_cache = [] if cache else None
        fsts = fsts or self.morphology.pos
        # number of normalization simplifications
        simps = None
        if preproc:
            # Convert to roman, for example
            form, simps = self.preproc(word)
        else:
            form = word
         # See if the word is unanalyzable ...
        unal_word = self.morphology.is_unanalyzed(form)

        # unal_word is a form, POS pair
        if unal_word and not skip_other_pos:
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
                                              phonetic=phonetic, 
                                              normalize=normalize, segment=segment, guess=False,
                                              postproc=postproc, freq=report_freq,
                                              verbosity=verbosity)

        # Is word already analyzed, without any root/stem (for example, there is a POS and/or a translation)?
        if not analyses and form in self.morphology.analyzed and not skip_other_pos:
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
            if suff_anal and not skip_other_pos:
                if cache:
                    to_cache.extend(suff_anal)
                for stem, fs in suff_anal:
                    cat = fs.get('pos', '')
                    analyses.append((cat, stem, stem, fs, None, 100))
#        print("** 1 {}, get_all {}".format(analyses, get_all))
        if not analyses or (not found and get_all):
            if not only_guess:
                for pos in fsts:
                    #... or already analyzed within a particular POS
                    # % fix segmentation for these cases! v_analyzed.lex and n_analyzed.lex
                    preanal = not segment and self.morphology[pos].get_analyzed(form, sep_anals=True)
                    if preanal:
                        if cache:
                            to_cache.extend(preanal)
                        analyses.extend(self.proc_anal(form, preanal, pos,
                                                       phonetic=phonetic,
                                                       normalize=normalize, segment=segment,
                                                       guess=False, postproc=postproc,
                                                       freq=report_freq, verbosity=verbosity))
                    else:
                        # We have to really analyze it; first try lexical FSTs for each POS
                        if verbosity:
                            print("** analyzing {} with {} FST".format(form, pos))
                        self.anal_word_(form, analyses, pos, to_cache, postproc=postproc,
                                        guess=False, phon=phon, segment=segment, init_weight=init_weight,
                                        experimental=experimental, mwe=mwe, normalize=False, to_dict=to_dict,
                                        sep_anals=sep_anals, verbosity=verbosity)
        # If nothing has been found, try guesser FSTs for each POS
#        print("** 2 analyses {}".format(analyses))
        if not analyses and guess:
            # Accumulate results from all guessers
            for pos in fsts:
                self.anal_word_(form, analyses, pos, to_cache, postproc=postproc,
                                guess=True, phon=phon, segment=segment, init_weight=init_weight,
                                experimental=experimental, mwe=False, normalize=False, to_dict=to_dict,
                                sep_anals=sep_anals, verbosity=verbosity)
        if cache and not found:
            self.add_new_anal(word, to_cache)
        if not analyses:
            # Impossible to analyze the word/form.
            if no_anal != None:
                no_anal.append(word)
            if segment and experimental:
                analyses = [('UNK', None, None)]
            return analyses
        if len(analyses) > 1:
            self.sort_analyses(analyses)
        # Select the n best analyses
        analyses = analyses[:nbest]
#        print("** Sorted analyses {}".format(analyses))
        self.filter_analyses(analyses)
        if print_out:
            # Print out stringified version
            print(self.analyses2string(word, analyses, seg=segment, lemma_only=lemma_only,
                                       ortho_only=ortho_only, form_only=not gram))
        elif segment and um:
            # Getting UM and UD features for segmented analyis
            for aindex, analysis in enumerate(analyses):
                pos, segmentation, lemma, features, freq = analysis
                POS = Language.convertPOS(pos)
                if POS in self.um.hm2um:
                    umfeats = self.um.convert(features, pos=POS)
                    udfeats = self.um.convert2ud(umfeats, POS, extended=um==2)
                    analyses[aindex] = analysis + (udfeats,)
                else:
                    analyses[aindex] = analysis + ('',)
        elif not segment and not string:
            # Do final processing of analyses, given options
            for i, analysis in enumerate(analyses):
                if len(analysis) <= 2:
                    analyses[i] = (analysis[1],)
                else:
                    a = self.finalize_anal(analysis, um=um,
                                           gloss=gloss, report_freq=report_freq,
                                           phonetic=phonetic, simplify=simplify,
                                           simplifications=not phonetic and simps)
                    analyses[i] = a
#            analyses =  [(anal[1], anal[-2], anal[-1]) if len(anal) > 2 else (anal[1],) for anal in analyses]

        return [a for a in analyses if a]

    def anal_word_(self, form, analyses, pos, to_cache,
                   guess=False, phon=False, segment=False, init_weight=None, experimental=False, mwe=False,
                   phonetic=True, normalize=False, sep_anals=True,
                   to_dict=False, postproc=False, cache=False, report_freq=True,
                   verbosity=0):
        analysis = self.morphology[pos].anal(form, guess=guess, init_weight=init_weight,
                                             phon=phon, segment=segment, experimental=experimental, mwe=mwe,
                                             normalize=normalize, to_dict=to_dict, sep_anals=sep_anals,
                                             verbosity=verbosity)
        if analysis:
            if cache:
                to_cache.extend(analysis)
                # Keep trying if an analysis is found
            analyses.extend(self.proc_anal(form, analysis, pos, 
                                           segment=segment, normalize=normalize,
                                           phonetic=phonetic, guess=guess, postproc=postproc,
                                           freq=report_freq, verbosity=verbosity))

##    def anal_file(self, pathin, pathout=None, preproc=True, postproc=True, pos=None,
##                  segment=False,
##                  lemma_only=False, ortho_only=False, realize=False,
##                  knowndict=None, guessdict=None, cache=False, no_anal=None,
##                  phon=False, only_guess=False, guess=True, raw=False, experimental=False, mwe=False,
##                  sep_punc=True, word_sep='\n', sep_ident=False, minim=False, feats=None, simpfeats=None, um=0, normalize=False,
##                  # Kind of output
##                  conllu=True, seglevel=2,
##                  # Filter for morphological properites
##                  gramfilter=None,
##                  # Ambiguity
##                  report_freq=False, nbest=100, report_n=50000,
##                  lower=True, lower_all=False, nlines=0, start=0, batch_name='',
##                  local_cache=None, xml=None, multseg=False, csentences=None, sentid=0,
##                  verbosity=0):
##        """
##        Analyze words in file, either writing results to pathout, storing in
##        knowndict or guessdict, or printing out.
##        saved is a dict of saved analyses, to save analysis time for words occurring
##        more than once.
##        """
##        preproc = preproc and self.preproc
##        postproc = postproc and self.postproc
##        storedict = True if knowndict != None else False
##        normalize = normalize and not um
##        realizer = realize and self.segmentation2string
##        batch_name = batch_name or "Batch"
##        csent = None
##        xsent = None
###        if csentences != False:
##        if not isinstance(csentences, list):
##            # Create the list of CoNLL-U sentences
##            csentences = []
##        elif xml:
##            # This is either a CACO XML tree or True or False (or None)
##            if not isinstance(xml, ET.ElementTree):
##                # Create the CACO tree
##                xml = make_caco()
##            xmlroot = xml.getroot()
##        try:
##            filein = open(pathin, 'r', encoding='utf-8')
##            # If there's no output file and no outdict, write analyses to terminal
##            out = sys.stdout
##            if segment:
##                print('Segmenting words in', pathin)
##            else:
##                print('Analyzing words in', pathin)
##            if pathout:
##                # Where the analyses are to be written
##                fileout = open(pathout, 'w', encoding='utf-8')
##                print('Writing to', pathout)
##                out = fileout
##            fsts = pos or self.morphology.pos
##            n = 0
##            # Save words already analyzed to avoid repetition
##            if no_anal:
##                no_anal = []
##            else:
##                no_anal = None
##            # Store final representations here; these depend not only on analyses but also
##            # on various options to this method, like minim and segment
##            local_cache = local_cache if isinstance(local_cache, dict) else {}
##            # If nlines is not 0, keep track of lines read
##            lines = filein.readlines()
##            if start or nlines:
##                lines = lines[start:start+nlines]
##            for line in lines:
##                line = line.strip()
##                sentid += 1
##                n += 1
##                if n % report_n == 0:
##                    print("ANALYZED {} LINES".format(n))
##                # Separate punctuation from words
##                if sep_punc:
##                    line = self.morphology.sep_punc(line)
##                identifier = ''
##                string = ''
##                if sep_ident:
##                    # Separate identifier from line
##                    identifier, line = line.split('\t')
##                    string = "{}\t".format(identifier)
##                if verbosity:
##                    print("** Analyzing line {}".format(line))
###                if csentences != False:
##                csent = Sentence(line, self, batch_name=batch_name, sentid=sentid)
##                csentences.append(csent)
##                if xml:
##                    xsent = add_caco_sentence(xmlroot)
##                # Segment into words
##                morphid = 1
##                csent = \
##                self.anal_sentence4(line, csent=csent, csentences=csentences, file=out,
##                                   preproc=preproc, postproc=postproc, pos=pos, fsts=fsts, segment=segment, 
##                                   realize=realize, realizer=realizer, dicts=[knowndict, guessdict] if storedict else None,
##                                   conllu=conllu, xsent=xsent, seglevel=seglevel, gramfilter=gramfilter,
##                                   phon=phon, only_guess=only_guess, guess=guess, raw=raw, experimental=experimental, mwe=mwe,
##                                   sep_punc=sep_punc, word_sep=word_sep, sep_ident=sep_ident, minim=minim, feats=feats, simpfeats=simpfeats,
##                                   um=um, normalize=normalize, report_freq=report_freq, nbest=nbest, report_n=report_n,
##                                   lower=lower, lower_all=lower_all, batch_name=batch_name,
##                                   local_cache=local_cache, xml=xml, multseg=multseg, sentid=sentid, morphid=morphid,
##                                   verbosity=0)
##            filein.close()
##            if pathout:
##                fileout.close()
##        except IOError:
##            print('No sufile or path; try another one.')
##        if xml:
##            return xml
##        elif experimental:
##            return csentences

##    def anal_sentence4(self, sentence, csent=None, csentences=None, file=None, pathout="",
##                      preproc=True, postproc=True, pos=None, fsts=None,
##                      segment=True, realize=True, realizer=None,
##                      conllu=True, xml=None, multseg=False, dicts=None, xsent=None,
##                      phon=False, only_guess=False, guess=True, raw=False, experimental=True, mwe=True,
##                      sep_punc=False, word_sep='\n', sep_ident=False, minim=False,
##                      feats=None, simpfeats=None, um=0, normalize=False,
##                      nbest=100, report_freq=False, report_n=50000,
##                      remove_dups=True, seglevel=2,
##                      gramfilter=None, filter_cache=None,
##                      lower=True, lower_all=False, batch_name='', local_cache=None, sentid=0, morphid=1,
##                      verbosity=0):
##        # Keep track of words that are filtered out because they match filter conditions
##        countgrams = None
##        if gramfilter and isinstance(gramfilter, str):
##            gramfilter = EES.get_filter(gramfilter)
##            # Check whether this filter counts instances of "in" words; assume this is the only condition
##            for key, value in gramfilter.items():
##                if isinstance(key, tuple):
##                    # the key is (min, max); are these the only possibilities?
##                    countgrams = key
##                    print("** Counting gramfilter matches")
##        # lists of words that filter fails on and words it succeeds on
##        filtered = [[], []]
##        if preproc and not callable(preproc):
##            preproc = self.preproc
##        if postproc and not callable(postproc):
##            postproc = self.postproc
##        csent = csent or Sentence(sentence, self, batch_name=batch_name, sentid=sentid)
##        local_cache = local_cache if isinstance(local_cache, dict) else {}
##        if not file and pathout:
##            file = open(pathout, 'w', encoding='utf-8')
##        if not fsts:
##            fsts = pos or self.morphology.pos
##            skip_other_pos = False
##        else:
##            skip_other_pos = True
##        if realize and not realizer:
##            realizer = self.segmentation2string
##        # Create a list of CoNNL-U sentences.
##        if not isinstance(csentences, list):
##            csentences = []
##        tokens = sentence.split()
##        ntokens = len(tokens)
##        w_index = 0
##        while w_index < ntokens:
##            if filtered[0]:
##                # There is a failed word
###                print("*** filtered {}, rejecting sentence".format(filtered))
##                return
##            word = tokens[w_index]
##            simps = None
##            words = None
##            if w_index < len(tokens)-1:
##                next_word = tokens[w_index+1]
##                if not self.morphology.is_punctuation(word) and not self.morphology.is_punctuation(next_word):
##                    words = word + " " + next_word
##            if words:
##                if self.get_from_local_cache(words, local_cache, um=um, seglevel=seglevel, gramfilter=gramfilter, filtered=filtered,
##                                             experimental=experimental, segment=segment,
##                                             printout=file and not experimental,
##                                             dicts=dicts, conllu=conllu, xml=xml, xsent=xsent, csent=csent, filter_cache=filter_cache,
##                                             multseg=multseg, morphid=morphid, file=file):
##                    # MWE analysis stored in cache
##                    w_index += len(words.split())
##                    continue
##                simps = None
##                if preproc:
##                    form, simps = self.preproc(words)
##                # Attempt to analyze MWE
##                analyses = \
##                    self.anal_word(form, fsts=fsts, guess=guess, phon=phon, only_guess=only_guess,
##                                   segment=segment, experimental=experimental, mwe=True,
##                                   normalize=normalize, ortho_only=False,
##                                   preproc=False, postproc=postproc and not raw,
##                                   skip_other_pos=skip_other_pos,
##                                   cache=False, no_anal=None, um=um, report_freq=report_freq, nbest=nbest,
##                                   string=not raw and not um, print_out=False, only_anal=False, verbosity=verbosity)
##                newmorphid = \
##                   self.handle_word_analyses(words, analyses, mwe=True, simps=simps, csent=csent, morphid=morphid,
##                                             experimental=experimental,
##                                             gramfilter=gramfilter, filtered=filtered, filter_cache=filter_cache,
##                                             local_cache=local_cache, segment=segment, realize=realize, realizer=realizer,
##                                             conllu=conllu, xml=xml, dicts=dicts, multseg=multseg, raw=raw, um=um,
##                                             remove_dups=remove_dups, seglevel=seglevel, verbosity=verbosity,
##                                             printout=file and not experimental,
##                                             word_sep=word_sep, file=file)
##                if newmorphid:
##                    # MWE analysis succeeded
##                    w_index += len(words.split())
##                    morphid = newmorphid
##                    continue
##            # Analyze single word
##            if verbosity:
##                print("**  Analyzing word {}".format(word))
##            # Lowercase on the first word, assuming a line is a sentence
##            if lower_all or (lower and w_index == 0):
##                word = word.lower()
##            if self.get_from_local_cache(word, local_cache, um=um, seglevel=seglevel, gramfilter=gramfilter, filtered=filtered,
##                                         experimental=experimental, segment=segment,
##                                         printout=file and not experimental,
##                                         dicts=dicts, conllu=conllu, xml=xml, xsent=xsent, csent=csent, filter_cache=filter_cache,
##                                         multseg=multseg, morphid=morphid, file=file):
##                w_index += 1
##                continue
##            simps = None
##            if not skip_other_pos:
##                analyses = self.preproc_special(word, segment=segment, print_out=False)
##            else:
##                analyses = None
##            if not analyses:
##                ## Analyze
##                if preproc:
##                    form, simps = self.preproc(word)
##                analyses = \
##                  self.anal_word(form, fsts=fsts, guess=guess, phon=phon, only_guess=only_guess,
##                       segment=segment, experimental=experimental, mwe=False, 
##                       normalize=normalize, ortho_only=False, preproc=False, postproc=postproc and not raw,
##                       skip_other_pos=skip_other_pos,
##                       cache=False, no_anal=None, um=um, report_freq=report_freq, nbest=nbest,
##                       string=not raw and not um, print_out=False, only_anal=False, verbosity=verbosity)
##            morphid = \
##                self.handle_word_analyses(word, analyses, mwe=False, simps=simps, csent=csent, morphid=morphid,
##                                          experimental=experimental,
##                                          gramfilter=gramfilter, filtered=filtered, filter_cache=filter_cache,
##                                          local_cache=local_cache, segment=segment, realize=realize, realizer=realizer,
##                                          conllu=conllu, xml=xml, dicts=dicts, multseg=multseg, raw=raw, um=um,
##                                          remove_dups=remove_dups, seglevel=seglevel, verbosity=verbosity,
##                                          printout=file and not experimental,
##                                          word_sep=word_sep, file=file)
##            # Go to next word
##            w_index += 1
##        if filtered[0]:
##                # There is a failed word
##            return
##        if gramfilter:
##            if not filtered[1]:
##                return
##            elif countgrams:
##                print("*** accepted by filter: {}".format(filtered[1]))
##                nfiltered = len(filtered[1])
##                if countgrams[0] > nfiltered or countgrams[1] < nfiltered:
##                    print("*** failed count constraints")
##                    return
##        # End of sentence
##        csent.finalize()
##        return csent

    def get_from_local_cache(self, word, local_cache, um=0, seglevel=2, gramfilter=None, filtered=None, filter_cache=None,
                             dicts=None, conllu=True, xml=False, csent=None, xsent=None, multseg=False,
                             experimental=True, segment=True, word_sep="\n",
                             morphid=1, file='', printout=False, verbosity=0):
        if word in local_cache:
#            print("** Getting {} from local cache".format(word))
            analysis = local_cache[word]
#            analysis = copy.deepcopy(analysis)
#            print("** Found in local cache {}".format(analysis))
            if gramfilter and filter_cache:
                if word in filter_cache[0]:
                    if verbosity:
                        print("** {} in failed filter cache".format(word))
                    filtered[0].append(word)
                if word in filter_cache[1]:
                    if verbosity:
                        print("** {} in succeeded filter cache".format(word))
                    filtered[1].append(word)
#            if gramfilter and analysis:
#                Language.filter_word(analysis, gramfilter, filtered, filter_cache)
            if dicts:
                add_anals_to_dict(self, analysis, dicts[0], dicts[1])
            elif xml:
                add_caco_word(xsent, word, analysis, multseg=multseg)
            elif experimental:
                csent.add_word(word, analysis, morphid, conllu=True, um=um, seglevel=seglevel)
            elif printout:
                anal_string = self.analyses2string(word, analysis, seg=segment, form_only=False, lemma_only=False,
                                                   ortho_only=False, word_sep=word_sep)
#                print("** string {}".format(anal_string))
                print(anal_string, file=file, end='')
#            else:
            return True

    def handle_word_analyses(self, word, analyses, mwe=False, experimental=True,
                             gramfilter=None, filtered=None, filter_cache=None,
                             local_cache=None, segment=True, realize=True, realizer=None,
                             conllu=True, xml=False, dicts=None, multseg=True, simps=None, csent=None,
                             remove_dups=True, seglevel=2, printout=False, extract_features=None,
                             morphid=1, raw=False, um=0, word_sep=" ", file='', verbosity=0):
        """
        Do the post-processing of word (or MWE) analyses within sentences.
        if mwe is True, check whether the analysis is empty ('UNK').
        """
        if not analyses:
#            print("** No analyses for {}".format(word))
            return 0
        if mwe and analyses[0][0] == 'UNK':
#            print("** Analysis for {} is empty".format(word))
            return 0

#        print("*** analyses: {}".format(analyses))
        if gramfilter and analyses:
            # Check gramfilter to see if word passes
            Language.filter_word(word, analyses, gramfilter, filtered, filter_cache)

        string_analyses = ''

        if segment and realize and experimental:
            analyses = [realizer(word, analysis, features=True, udformat=True, um=um, simplifications=simps) for analysis in analyses]

        if verbosity:
            print("*** handling analyses for {}: {}".format(word, analyses))
        
        # Remove duplicate analyses
        if remove_dups:
            anals = []
            for a in analyses:
                if a not in anals:
                    anals.append(a)
            if len(anals) != len(analyses):
                analyses = anals
        # Otherwise (for file or terminal), convert to a string
        if analyses:
            if raw or (um and not segment):
                analyses = "{}  {}".format(word, analyses.__repr__())
            elif not experimental or not realize:
                # Convert the analyses to a string
                string_analyses = \
                  self.analyses2string(word, analyses, seg=segment, form_only=False, lemma_only=False,
                                       ortho_only=False, word_sep=word_sep)
            elif not conllu and not xml:
                string_analyses = "{}: {}".format(word, analyses)
        elif segment and not conllu and not xml:
            analyses = "{}: []".format(word)
        else:
            analyses = word
        # Cache before adjusting head indices because these are going to be done after retrieving
        # cachec analyses anyway.
#        print("** Caching {}".format(analyses))
        local_cache[word] = analyses

        # Use a copy of analyses for further processing
        analyses = copy.deepcopy(analyses)

        # Either store the analyses in the dict or write them to the terminal or the file
#        print("** analyses {}".format(analyses))
        if dicts:
            add_anals_to_dict(self, analyses, dicts[0], dicts[1])
        elif conllu and experimental:
#            print("** Adding CoNLL-U word {}".format(word))
            csent.add_word(word, analyses, morphid, conllu=True, seglevel=seglevel, um=um)
            # Update the morpheme id, assuming the first analysis
            if seglevel == 0:
                morphid += 1
            # Need to handle seglevel=1
            else:
                morphid += len(analyses[0])
        elif xml:
            add_caco_word(xsent, word, analyses, multseg=multseg)
        elif experimental:
            csent.add_word(word, analyses, morphid, conllu=False, seglevel=seglevel, um=um)
        elif printout:
            print(string_analyses, file=file, end='')

        return morphid

#    def format_analysis(self, criterion='conllu', form=None, features=None, lemma=None, freq=None):
#        '''
#        Format the analysis according to different criteria:
#        'conllu', 'dict', 'seg', 'list', 'xml'.
#        '''

    def get_root_freq4(self, pos, feats, root=''):
        # The freq score is the count for the root-feature combination
        # times the product of the relative frequencies of the grammatical features
        if pos.startswith('nm'):
            # Treat names specially
            root_freq = Language.namefreq
        else:
            root_freq = self.morphology.get_root_freq(root, feats)
            feat_freq = self.morphology.get_feat_freq(feats)
            root_freq *= feat_freq
            root_freq = round(root_freq)
        return root_freq

    def get_lemma(self, pos, feats=None, root='', guess=False, postprocess=True, phonetic=False):
        lemma = None
        l = feats.get('lemma') if feats else ''
        if l:
            lemma = l
        else:
            # Convert nadj, n_dv to n
            POS = Language.convertPOS(pos)
            posmorph = POS and POS in self.morphology and self.morphology[POS]
            if posmorph and posmorph.citation and isinstance(feats, FeatStruct):
                lemma = posmorph.citation(root, feats, guess, True, phonetic=phonetic)
                if not lemma:
                    lemma = root
                if postprocess:
#                    print("** Postprocessing {}".format(lemma))
                    lemma = self.postprocess(lemma, ortho_only=True, phonetic=phonetic)
        return lemma

    @staticmethod
    def filter_word(word, analyses, gramfilter, filtered, filter_cache, nanals=2, verbosity=0):
        '''
        Does the word satisfy the filter conditions?
        gramfilter is a dict with keys 'in' and/or 'out' and values tuples of gramfilter
        Each filter condition is a tuple of of pairs with possible first elements
        'pos', 'feats, 'featfail', 'lemma', 'lemmafail', (minmatches, maxmatches)
        '''
        succeeded = []
        failed = []
        if verbosity:
            print("**Filter word {} with {}".format(word, gramfilter))
        for aindex, analysis in enumerate(analyses[:nanals]):
            if len(analysis) < 5:
#                print("*** short anal {}".format(analysis))
                return True
            if verbosity:
                print(" *** Checking analysis {}".format(aindex))
            pos = analysis[0]; features = analysis[3]; lemma = analysis[2]
            if not isinstance(pos, str):
                print("***! POS {} in analysis {} is not string".format(pos, analysis.__repr__()))
                return True
            for filtertype, filterconds in gramfilter.items():
                if verbosity:
                    print(" *** filtertype {}")
                if isinstance(filtertype, tuple):
                    # this is a "count in" condition with min and max
                    filtertype = 'in'
                for filtercond in filterconds:
                    if verbosity:
                        print("  *** filtercond {}".format(filtercond))
                    matched = True
                    for key, value in filtercond:
                        if verbosity:
                            print("   *** key {} value {} lemma {} features {}".format(key, value, lemma, features.__repr__()))
                        if key == 'pos':
                            # value could be a single POS or a tuple of POSs
                            if isinstance(value, str) and pos == value:
                                if verbosity:
                                    print("    *** passed pos condition {}!".format(value))
                                continue
                            elif pos in value:
                                if verbosity:
                                    print("    *** passed pos condition {}!".format(value))
                                continue
                        elif key == 'featfail':
                            if features and simple_unify(features, value) == 'fail':
                                if verbosity:
                                    print("    *** passed featfail condition {}!".format(value))
                                continue
                        elif key.startswith('feat'):
                            if features and simple_unify(features, value) != 'fail':
                                if verbosity:
                                    print("    *** passed feat condition {}!".format(value))
                                continue
                        elif key == 'lemmafail':
                            if isinstance(value, str) and lemma != value:
                                if verbosity:
                                    print("    *** passed lemmafail condition {}!".format(value))
                                continue
                            elif lemma not in value:
                                if verbosity:
                                    print("    *** passed lemmafail condition {}!".format(value))
                                continue
                        elif key == 'lemma':
                            if isinstance(value, str) and lemma == value:
                                if verbosity:
                                    print("    *** passed lemma condition {}!".format(value))
                                continue
                            elif lemma in value:
                                if verbosity:
                                    print("    *** passed lemma condition {}!".format(value))
                                continue
                        if verbosity:
                            print("   *** Failed to match")
                        matched = False
                        break
                    # Pos and feature conditions match; word is *in* or *out* depending on filtertype
                    if matched:
                        if filtertype == 'out':
                            # Matched the properties, so exclude this one
                            if verbosity:
                                print("    *** match for out; FAIL")
                            failed.append((word, aindex))
                            break
                    elif filtertype == 'in':
                        # one mismatch is enough to exclude the word
                        if verbosity:
                            print("    *** mismatch for in; FAIL")
                            failed.append((word, aindex))
                            break
                # We made it through all of the conditions, matching for 'in', failing to match for 'out'
                # Don't check more conditions
                if failed:
                    break
            # Tried all conditions; succeed if nothing failed
            if not failed:
                succeeded.append((word, aindex))
                if verbosity:
                    print("***   word succeeded for analysis {}".format(aindex))
#            if filtertype == 'out' and not failed:
#                succeeded.append(word)
        if verbosity:
            print("*** failed {}, succeeded {}".format(failed, succeeded))
        if len(failed) > len(succeeded):
            filtered[0].append(word)
            if filter_cache:
                if verbosity:
                    print("    *** adding word to fail cache {}!".format(word))
                filter_cache[0].append(word)
        elif len(succeeded) > len(failed):
            filtered[1].append(word)
            if filter_cache:
                if verbosity:
                    print("    *** adding word to succeed cache {}!".format(word))
                filter_cache[1].append(word)
#        filtered[0].extend(failed)
#        filtered[1].extend(succeeded)
        if verbosity:
            print("*** post filter: {}".format(filtered))
#        return failed, succeeded

    def preproc_special(self, word, segment=False, print_out=False):
        '''
        Handle special cases, currently abbreviations, numerals, and punctuation.
        '''
        if self.morphology.is_punctuation(word):
            return [self.process_punc(word, segment=segment, print_out=print_out)]
        if self.morphology.is_abbrev(word):
#            print("{} is an abbreviation".format(word))
            return [self.process_abbrev(word, segment=segment, print_out=print_out)]
        numeral = self.morphology.match_numeral(word)
        if numeral:
            prenum, num, postnum = numeral
            return [self.process_numeral(word, prenum, num, postnum, segment=True, print_out=print_out)]
        return None

    def process_abbrev(self, word, segment=False, print_out=False):
        '''
        Return analysis or segmentation of abbreviation.
        Later expand abbreviation to full form for lemma if one word.
        '''
        # Assumes all abbreviations are nouns
        pos = 'n'
        if print_out:
            string = "{} -- abbrev".format(word)
            print(string)
        elif segment:
            string = "{" + word + "}}({}abbr=yes)".format(Language.featsmark)
            return (pos, string, word)
        else:
            return (pos, word, word, None, 100)
#            return [{'POS': pos, 'lemma': word, 'freq': 100}]

    def process_punc(self, word, segment=False, print_out=False):
        '''
        Return analysis or segmentation of punctuation.
        '''
        pos = 'punct'
        if print_out:
            string = "{} -- punc".format(word)
            print(string)
        elif segment:
            string = None # word
            return (pos, string, '', None, 10000)
        else:
            return (pos, word, word, None, 10000)
#            return [{'POS': pos, 'freq': 10000}]

    def process_numeral(self, word, pre, num, post, segment=False, print_out=False):
        '''
        Return analysis or segmentation of word containing numeral.
        %% TODO: finish analysis
        '''
        pos = 'n' if post else 'num'
        if post:
            lemma = post
        elif pre:
            lemma = num
        else:
            lemma = ''
#        lemma = post if post else num
        if print_out:
            string = "{} -- num: {}".format(word, num)
            if post:
                string += ", head: {}".format(post)
            if pre:
                string += ", prep: {}".format(pre)
            print(string)
        elif segment:
            if post:
                if pre:
                    string = "{}(@adp,*{},~case)-{}(@num,*{},~nummod)-{{{}}}".format(pre, pre, num, num, post)
                else:
                    string = "{}(@num,*{},~nummod)-{{{}}}".format(num, num, post)
            elif pre:
                string = "{}(@adp,*{},~case)-{{{}}}".format(pre, pre, num)
            else:
                string = None #"{}".format(num)
            return (pos, string, lemma, None, 1000)
#            return (pos, string, lemma)
        else:
            result = [{'POS': pos, 'freq': 1000}]
            if lemma:
                result['lemma'] = lemma
            return (pos, word, lemma, None, 1000)
#            return result

    def minim_string(self, form, analyses=None, feats=None, simpfeats=None):
        """
        Create a minimal string representing the analysis of a word.
        feats are features to include from the FeatStruct(s) in the
        analyses.
        """
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
                if root_pos:
                    rp_string = '|'.join(root_pos)
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

    @staticmethod
    def convertPOS(pos):
        '''
        Replace POS string by one used to index FSTs, for example, 'nadj' -> 'n'.
        '''
        if pos in ('nadj', 'n_dv', 'nm_pl', 'nm_prs', 'pron', 'adj', 'nadv', 'npropn'):
            return 'n'
        elif pos in ('vintj',):
            return 'v'
        elif pos in ('aux',):
            return 'cop'
        return pos

    def analyses2string(self, word, analyses, seg=False,
                        lemma_only=False, ortho_only=False, form_only=False,
                        word_sep='\n', webdicts=None):
        '''
        Convert a list of analyses to a string, and if webdicts, add analyses to dict.
        '''
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
        if lemma_only:
            s = Language.T.tformat('{}: ', [word], self.tlanguages)
        else:
            s += Language.T.tformat('{}: {}\n', ['word', word], self.tlanguages)
        lemmas = []
        for analysis in analyses:
            fs = analysis[3]
            pos = fs.get('pos') if fs else None
            if pos == 'nadj' or pos == 'n_dv':
                pos = 'n'
            if pos:
                webdict = None
                if webdicts != None:
                    webdict = {}
                    webdicts.append(webdict)
                if pos in self.morphology:
                    if self.morphology[pos].anal2string:
                        analstring = \
                        self.morphology[pos].anal2string(analysis, webdict=webdict, lemma_only=lemma_only)
                        if lemma_only:
                            if analstring not in lemmas:
                                lemmas.append(analstring)
                        else:
                            s += analstring
                    else:
                        s += self.morphology[pos].pretty_anal(analysis, webdict=webdict)
                elif self.morphology.anal2string:
                    s += self.morphology.anal2string(analysis, webdict=webdict)
            elif analysis[1] and analysis[0]:
                # this is the POS for unanalyzable words
                pos = analysis[1]
                root = analysis[0]
                if self.postproc:
                    root = self.postproc(root, ortho_only=ortho_only)
                if lemma_only:
                    lemmas.append(root)
                else:
                    s += " POS = {}, lemma = {}\n".format(pos, root)
        if lemma_only:
            s += ' '.join(lemmas) + "\n"
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

    def finalize_anal(self, anal, um=1, gloss=True,
                      report_freq=False, phonetic=True,
                      simplify=True, simplifications=None):
        """
        Create dict with analysis.
        """
        a = {}
        pos, root, cit, gram, count = anal
        # POS could be '?v', etc.
#        pos = pos.replace('?', '')
        # Postprocess root if appropriate
        root1 = None
        simplifications = simplifications if simplify else None
        if root:
            root1 = self.postproc_root(self.morphology.get(pos.replace('?', '')),
                                       root, gram, phonetic=phonetic, simplifications=simplifications)
        if pos:
            a['POS'] = pos
        if not gram and not cit:
            # Unanalyzed word
            a['lemma'] = root1
        elif cit:
            a['lemma'] = cit
        if root and ((cit and root != cit) or (root1 != root)):
            a['root'] = root1
        if gloss:
            g = self.get_gloss(gram)
            if g:
                a['gloss'] = g
        if um and pos in self.um.hm2um:
            ufeats = self.um.convert(gram, pos=pos)
            if ufeats:
                gram = ufeats
                a['gram'] = gram
        if not um:
            if gram:
                a['gram'] = gram
        if report_freq:
            a['freq'] = count
        return a

    def simp_anal(self, analysis, postproc=False, segment=False):
        '''Process analysis for unanalyzed cases.'''
        cite = None
        if len(analysis) == 1:
            print("*** analysis only {}".format(analysis))
        form, pos = analysis
        if Morphology.mwe_sep in form:
            form = form.replace(Morphology.mwe_sep, ' ')
        if segment:
            cite = self.get_lemma(pos, root=form, postprocess=postproc, phonetic=False)
            return pos, form, cite, None, 10000
        cite = self.get_lemma(pos, root=form, postprocess=postproc, phonetic=False)
        # 100000 makes it likely these will appear first in ranked analyses
        # form is actually the root for a few cases
        return pos, form, cite, None, 10000

    def proc_anal_noroot(self, form, analyses, segment=False):
        '''Process analyses with no roots/stems.'''
        return [(analysis.get('pos'), None, None, analysis, 0) for analysis in analyses]

    def postproc_root(self, posmorph, root, fs, phonetic=True, simplifications=None):
        """
        If posmorph has a root_proc function, use it to produce a root.
        """
        if posmorph and posmorph.root_proc:
            func = posmorph.root_proc
            return func(root, fs, phonetic=phonetic, simplifications=simplifications)
        elif self.dflt_postproc_root:
            return self.dflt_postproc_root(root, fs, phonetic=phonetic, simplifications=simplifications)
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

    def proc_anal1(self, analysis, pos, segment=True, guess=False,
                   freq=True, postproc=True, phonetic=True, normalize=False):
        feats = analysis[1]
        if not (feats := analysis[1]):
            return
        analstring = self.postpostprocess(analysis[0])
        if not pos:
            pos = feats.get('pos', '')
        cat = '?' + pos if guess else pos
        headi = feats.get('headi')
        if headi and segment:
            # MWE expression with features specifying head index, POS for non-head words, deprel
            modpos = feats.get('modpos', '')
            dep = feats.get('dep', '')
            match = MWE_SEG_STRING_RE.match(analstring)
            if match:
                pre, rt, post = match.groups()
                rootwords = rt.split()
                morphs = []
                for i, x in enumerate(rootwords):
                    if i == headi:
                        morphs.append('{' + x + '}')
                    else:
                        lemma1 = self.postproc(x, ortho_only=True)
                        morphs.append("{}(@{},*{},~{})".format(x, modpos, lemma1, dep))
                analstring = "{}{}{}".format(pre, "-".join(morphs), post)
        if segment:
            real_seg = Language.root_from_seg(analstring)
            root = Language.root_from_segstring(analstring)
        else:
            root = analstring
        root_freq = 0
        if freq:
            root_freq = self.get_root_freq(pos, feats, root)
        posmorph = pos and pos in self.morphology and self.morphology[pos]
        if postproc and posmorph and posmorph.postproc:
            posmorph.postproc(analysis)
        # Find the citation form of the root if required
        # This only works if FSSets have been separated into FeatStructs
        cite = ''
        cite = self.get_lemma(pos, feats=feats, root=root, guess=guess, postprocess=postproc, phonetic=phonetic)
        # Normalize features
        if not segment:
            if normalize and posmorph:
                feats = posmorph.featconv(feats)
        newitem = (cat, analstring, cite, feats, root_freq)
#        if newitem not in results:
#            results.append(newitem)

        # Use the 'raw' POS, e.g., 'nadj' rather than 'n'
#        print("** proc_anal {} {} {}".format(pos, analstring, cite))
        return pos, analstring, cite, feats, root_freq
#        res.append((pos, analstring, cite, feats, root_freq))

    def proc_anal(self, form, analyses, pos,
                  freq=True, normalize=False, segment=False, guess=False, postproc=False,
                  string=False, phonetic=True, verbosity=0):
        '''
        Process analyses according to various options, returning a list of
        analysis tuples.
        If freq, include measure of root and morpheme frequency.
        '''
        results = []
        for analysis in analyses:
            if (newanal := \
                    self.proc_anal1(analysis, pos, segment=segment, guess=guess,
                                    freq=freq, 
                                    postproc=postproc,
                                    phonetic=phonetic, normalize=normalize)):
                if newanal not in results:
                    results.append(newanal)
        return results

    def ortho2phon(self, word, gram=False, raw=False, return_string=False,
                   gram_pre='-- ', postpostproc=False,
                   nbest=100, report_freq=False):
        '''Convert a form in non-roman to roman, making explicit features that are missing in orthography.
        @param word:     word to be analyzed
        @param gram:     whether a grammatical analysis is to be included
        @param return_string: whether to return string analyses (needed for phon_file)
        @param gram_pre: prefix to put before form when grammatical analyses are included
        @param postpostproc: whether to call postpostprocess on output form
        @param nbest: return or report only this many analyses
        @param report_freq: whether to report the frequency of the root
        @return:         a list of analyses
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
                output = posmorph.o2p(preproc)
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
        # Convert the result dict to a list (ranked by frequency)
        result_list = []
        for f, anals in results.items():
            count = 0
            anal_list = []
            if anals:
                for a in anals:
                    count += a[0]
                    anal_list.append(a[1:])
            result_list.append((f, count, anal_list))
        self.sort_analyses(result_list)
#            result_list.sort(key=lambda x: -x[1])
        result_list = result_list[:nbest]
        self.filter_analyses(result_list)
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
            if report_freq:
                return [(r[0], r[1]) for r in result_list]
            else:
                return [r[0] for r in result_list]
        else:
            # Print out only the forms
            for anal, count in [(r[0], r[1]) for r in result_list]:
                if report_freq:
                    print('{} ({})'.format(anal, count), end=' ')
                else:
                    print('{}'.format(anal), end=' ')
            print()

    # Version 5 sort analyses within word.

    def sort_analyses(self, analyses):
        '''
        V 4.
        Sort analyses (or segmentations) by estimated frequency and
        whether the word is treated as a whole or is segmented.
        '''
        # Sort by frequency (the last item in each analysis)
        analyses.sort(key=lambda x: -x[-1])

    def filter_analyses(self, analyses):
        '''
        analyses is a sorted list of analyses with estimated freq as the last item
        in each analysis.
        If there are multiple analyses, ones are eliminated if their freq is 0
        or less than 0.02 of the previous freq.
        '''
        if len(analyses) == 1:
            return
        drop_index = 1
        last_freq = analyses[0][-1]
        for analysis in analyses[1:]:
            freq = analysis[-1]
#            print("** filter: freq {}, last_freq {}, analysis {}".format(freq, last_freq, analysis))
            if last_freq:
                if not freq or last_freq / freq > 50:
                    break
            last_freq = freq
            drop_index += 1
        while len(analyses) > drop_index:
            analyses.pop()
        
    def ortho2phon_file(self, infile, outfile=None, gram=False,
                        word_sep='\n', anal_sep=' ', print_ortho=True,
                        postpostproc=False,
                        report_freq=False, nbest=100,
                        start=0, nlines=0):
        '''Convert non-roman forms in file to roman, making explicit features that are missing in the orthography.
        @param infile:   path to a file to read the words from
        @param outfile:  path to a file where analyses are to be written
        @param gram:     whether a grammatical analysis is to be included
        @param word_sep:  word separator (only when gram=False)
        @param anal_sep:  analysis separator (only when gram=False)
        @param print_ortho: whether to print the orthographic form first
        @param postpostproc: whether to call postpostprocess on output form
        @param report_freq: whether to report the frequency of the root
        @param start:    line to start analyzing from
        @param nlines:   number of lines to analyze (if not 0)
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
                                                   report_freq=report_freq, nbest=nbest)
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

    def gen_um_outputs(self, outputs, ptags, verbosity=0):
        """
        Given a list of outputs from POSMorphology.gen(),
        word, FeatStruct pairs, return a list of word, UM
        feature string pairs.
        ptags is a list of POS tags, one for each output.
        """
        result = []
        for output, pos in zip(outputs, ptags):
            word = output[0]
            fs = output[1]
#            pos = fs.get('pos')
            if not pos:
                print("NO POS FOR {}:{}".format(word, fs.__repr__()))
            if verbosity:
                print("{}: converting {}".format(pos, fs.__repr__()))
            if fs:
                um = self.um.convert(fs, pos, verbosity=verbosity)
            else:
                um = ''
            result.append((word, um))
        return result

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

    def __init__(self, abbrev, ldir='', morph_version=0):
#        print("Creating EES language...")
        Language.__init__(self, abbrev, ldir=ldir, roman=False, morph_version=morph_version)
        EES.__init__(self)
