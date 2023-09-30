"""
This file is part of HornMorpho and morfo, which are part of the PLoGS project.

    <http://homes.soic.indiana.edu/gasser/plogs.html>

    Copyleft 2018, 2020, 2022, 2023
    PLoGS and Michael Gasser <gasser@indiana.edu>.

    morfo is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    morfo is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with morfo.  If not, see <http://www.gnu.org/licenses/>.
--------------------------------------------------------------------
Author: Michael Gasser <gasser@indiana.edu>

Morphological processing.
Morphology and POSMorphology objects.
Analysis, generation.
Loading, composing, saving FSTs.

"""

import sys, re
from .fst import *
from . import strip
from .ees import EES
from .word import *

## Default punctuation characters; exclude single quote since it's
## often (usually) more like an alphanumeric character
PUNCTUATION = r'[“‘”’«»–—…¿¡•:;/\,<>?.!%$()[\]{}|#@&*\-\_+=\"`\^~]'
# Paren/bracket token transforms
PUNC_TOKENS = ['-LRB-', '-RRB-', '-LCB-', '-RCB-', '-lrb-', '-rrb-', '-lcb-', '-rcb-']
## Default alphabetic characters
CHARACTERS = r'[a-zA-Z]'

class Morphology(dict):
    """A dict of POSMorphology dicts, one for each POS class that has bound morphology."""

    version = 3.0
    complex = 0
    simple = 1

    default_sense = 0

    mwe_sep = '//'
    # Not clear which name is better
    morph_sep = '-'
    seg_sep = '-'

    # Regular expressions for affix files
    pattern = re.compile('\s*pat.*:\s+(\w+)\s+(.+)')
    function = re.compile('\s*func.*:\s+(\w+)\s+(.+)')
    suffix = re.compile('\s*suf.*:\s+(\S+)(\s.+)?')   # a single space separates the suffix from the segmented form
    grammar = re.compile('\s*gram.*:\s+(\w+)\s+(.+)')
    POS = re.compile('\s*pos:\s+(\w+)')

    # Regex for numerals or words containing numerals
    # %% Does this work for all Horn languages?
    numeral = re.compile('(\w*?)(\d+(?:[\d,]*)(?:\.\d+)?)(\w*?)')

    def __init__(self, pos_morphs=[], punctuation='', characters='', abbrev_chars='.'):
                 #                 fsh=None,
#                 feat_abbrevs=None,
#                 fv_abbrevs=None):
# excl_feats=None):
# , lex_feats=None):
        dict.__init__(self)
        #        if fsh:
        #            self.set_fsh(*fsh)
        #        else:
        #            self.fsh = None
        self.pos = []
        for pos_morph in pos_morphs:
            if not isinstance(pos_morph, tuple):
                pos_morph = (pos_morph,)
            label = pos_morph[0]
            posmorph = POSMorphology(*pos_morph)
            self[label] = posmorph
            posmorph.morphology = self
            self.pos.append(label)
        # Function that simplifies orthography
        self.simplify = None
        # Function that converts phonological to orthographic representation
        self.orthographize = None
        # Function that returns trivially analyzable forms
#        self.triv_anal = None
        # Function that tests whether string is punctuation in this language.
        self.is_punc = None
        # Function that converts (POS, root, citation, FS) to a string
        self.anal2string = None
        # Pair of lists of unanalyzable words: (complex, simple)
        self.words = []
        self.words1 = []
        self.wordsM = []
        self.words_phon = {}
        self.words_phone1 = {}
        self.words_phoneM = {}
        self.seg_units = []
        # Characters signalling abbrevations
        self.abbrev_chars = abbrev_chars or '.'
        # Regex to identify abbreviations
        self.abbrevRE = None
        self.language = None
        # Dictionary of preanalyzed words (varying POS)
        self.analyzed = {}
        self.analyzed_phon = {}
        # Dictionary of suffixes and suffix sequences and what to do with them
        self.suffixes = {}
        # Dictionary of prefixes and prefix sequences and what to do with them
        self.prefixes = {}
        # Dict of root frequencies
        self.root_freqs = None
        # Dict of grammatical feature frequencies
        self.feat_freqs = None
        # FST for making forms phonetic
        self.phon_fst = None
        self.directory = ''
        self.punctuation = punctuation or PUNCTUATION
        self.characters = characters or CHARACTERS
        # Language-specific method for analyzing or segmenting words containing numerals
        self.proc_num = None
        # Make punctuation regular expression objects and substitution string
        self.init_punc(self.characters, self.punctuation)
#        self.init_num(self.characters)
#        # Dict of feature names expanded to more readable strings
#        self.feat_abbrevs = feat_abbrevs or {}
        # List of feat-val pair list and abbreviations
#        self.fv_abbrevs = fv_abbrevs or []

    def get_cas_dir(self):
        return os.path.join(self.directory, 'cas')

    def get_lex_dir(self):
        return os.path.join(self.directory, 'lex')

    def get_fst_dir(self):
        return os.path.join(self.directory, 'fst')

    def get_pickle_dir(self):
        return os.path.join(self.directory, 'pkl')

    def get_stat_dir(self):
        return os.path.join(self.directory, 'stat')

    def expand_abbrev(self, abbrev):
        return self.feat_abbrevs.get(abbrev, abbrev)

    def init_punc(self, chars, punc):
        '''
        Make punctuation regular expression objects and substitution string.
        '''
        self.punc_after_re = re.compile(r'(' + chars + r')(' + punc + r'{1,3})', re.U)
        self.punc_before_re = re.compile(r'(' + punc + r'{1,3})(' + chars + r')', re.U)
        self.punc_sub = r'\1 \2'

#    def init_num(self, chars):
#        '''
#        Make numeral regular expression objects and substitution string.
#        '''
#        self.num_before_re = re.compile(r'(\d+?)(' + chars + r')', re.U)
#        self.num_sub = r'\1 \2'

    def sep_punc(self, text):
        """Separate punctuation from words."""
        text = self.punc_after_re.sub(self.punc_sub, text)
        text = self.punc_before_re.sub(self.punc_sub, text)
        return text

#    def sep_num(self, text):
#        """
#        Separate punctuation from words.
#        """
#        text = self.num_before_re.sub(self.num_sub, text)
#        return text

    def match_numeral(self, string):
        '''
        Does the string contain a numeral? If it does,
        return the characters before, the numeral as a string, and the characters after.
        '''
        match = Morphology.numeral.fullmatch(string)
        if match:
            return match.groups()
        return False

    def process_numeral(self, pre, num, post):
        '''
        Analyze or segment a numeral word with pre chars (normally a preposition),
        the numeral itself, and post chars (normally a measure noun).
        '''
        if self.proc_num:
            return self.proc_num(pre, num, post)
        if post:
            return 'n', "{} {} {}".format(pre, num, post)
        elif pre:
            return 'num', "{} {}".format(pre, num)
        else:
            return 'num', num

    def is_unanalyzed(self, word, simple=False, ortho=True, mwe=True):
        """
        Is word an unanalyzable word? If so, return the word preceded by its POS
        if available.
        """
        if ortho and (word in self.punctuation or word in PUNC_TOKENS):
            return word
        multi = False
        word_rec = None
        if ' ' in word:
            multi = True
            # Replaces spaces by //
            word = word.replace(' ', Morphology.mwe_sep)
        if mwe:
            if ortho:
                if multi:
                    word_rec = self.wordsM
                else:
                    word_rec = self.words1
            elif multi:
                word_rec = self.words_phonM
            else:
                word_rec = self.words_phon1
        elif ortho:
            word_rec = self.words
        else:
            word_rec = self.words_phon
        return word_rec and word_rec.get(word, False)
#        if ortho and not self.words:
#            return None
#        if not ortho and not self.words_phon:
#            return None
#        if ortho:
#            word_rec = self.words
#            return word_rec.get(word, False)
#        else:
#            word_rec = self.words_phon
#            return word_rec.get(word, False)

    def is_punctuation(self, string):
        '''
        Is this punctuation in this language?
        '''
        if self.is_punc:
            return self.is_punc(string)
        return string in self.punctuation

    def is_abbrev(self, string):
        '''
        Is this an abbreviation?
        '''
        regex = self.get_abbrevRE()
        return regex.fullmatch(string)

    def get_abbrevRE(self):
        '''
        Return the regex for identifying abbreviations, creating it if it hasn't already
        been set.
        '''
        if not self.abbrevRE:
            abbrev_chars = self.abbrev_chars or '.'
            string = "\w+[{}](?:\w+[{}]?)*".format(abbrev_chars, abbrev_chars)
#            string = "\w+[.](?:\w+[.]?)*"
            self.abbrevRE = re.compile(string)
        return self.abbrevRE

    def feat_name(self, values):
        if any(values):
            return '+'.join(values)
        else:
            return ''

    def rv_name(self, root, value):
        if value:
            return root + '+' + value
        else:
            return root

    def root_fv(self, root, anal):
        root_feats = self.language.stat_root_feats
        value = self.feat_name([anal.get(f, '') for f in root_feats])
        return self.rv_name(root, value)

    def get_fv(self, feats, anal):
        a = anal
        for f in feats:
            if f in a:
                a = a.get(f)
            else:
                return 'nothing'
        return a

    def get_root_freq(self, root, anal):
        rv = self.root_fv(root, anal)
#        print("** Getting root freq: {} {} ; {}".format(root, anal.__repr__(), rv))
        if self.root_freqs:
            return self.root_freqs.get(rv, 0)
        return 50

    def get_feat_freq(self, anal):
        freq = 1.0
        if self.feat_freqs:
            for f in self.language.stat_feats:
                v = self.get_fv(f, anal)
                if v != 'nothing':
                    feat_name = '+'.join(f)
                    freq0 = self.feat_freqs.get(feat_name, {}).get(v, 1.0)
                    freq *= freq0
        return freq

    def set_root_freqs(self):
        filename = 'root_freqs.dct'
        path = os.path.join(self.get_stat_dir(), filename)
        try:
            with open(path, encoding='utf-8') as roots:
                self.root_freqs = eval(roots.read())
        except IOError:
            pass
#            print('No root frequency file {} found'.format(path))

    def set_feat_freqs(self):
        filename = 'feat_freqs.dct'
        path = os.path.join(self.get_stat_dir(), filename)
        try:
            with open(path, encoding='utf-8') as feats:
                self.feat_freqs = eval(feats.read())
        except IOError:
            pass
#            print('No file frequency file {} found'.format(path))

    def set_words(self, filename='words.lex', ortho=True, simplify=False, mwe=True):
        '''
        Set the list/dict of unanalyzed words, reading them in from a file,
        one per line.
        If mwe is True, load separate files for single words and fixed MWEs.
        '''
        if mwe:
#            print("** Loading unanalyzed words")
            file1 = 'words1.lex'
            fileM = 'wordsM.lex'
            path1 = os.path.join(self.get_lex_dir(), file1)
            pathM = os.path.join(self.get_lex_dir(), fileM)
            if os.path.exists(path1):
                with open(path1, encoding='utf8') as file:
                    if ortho:
                        # Read in the words as a list
                        pairs = [w.split() for w in file]
                        self.words1 = dict([(w[0].strip(), w[1:]) for w in pairs])
                    else:
                        # Read in ortho:phon pairs as a dict
                        self.words_phon1 = dict([w.strip().split() for w in file])
            else:
                self.words1 = []
                self.words_phon1 = {}
            if os.path.exists(pathM):
                with open(pathM, encoding='utf8') as file:
                    if ortho:
                        # Read in the words as a list
                        pairs = [w.split() for w in file]
                        self.wordsM = dict([(w[0].strip(), w[1:]) for w in pairs])
                    else:
                        # Read in ortho:phon pairs as a dict
                        self.words_phonM = dict([w.strip().split() for w in file])
            else:
                self.wordsM = []
                self.words_phonM = {}
            return
        if not ortho:
            filename = 'words_phon.lex'
        path = os.path.join(self.get_lex_dir(), filename)
#        path = os.path.join(self.directory, filename)
#        position = Morphology.simple if simplify else Morphology.complex
        # Need to split and take first element because there may be semantic categories in the words file.
        if os.path.exists(path):
            with open(path, encoding='utf8') as file:
                if ortho:
                    # Read in the words as a list
                    pairs = [w.split() for w in file]
                    self.words = dict([(w[0].strip(), w[1:]) for w in pairs])
#                    self.words = [w.strip().split()[0] for w in file]
                else:
                    # Read in ortho:phon pairs as a dict
                    self.words_phon = dict([w.strip().split() for w in file])
        else:
            self.words = []
            self.words_phon = {}

    def get_analyzed(self, word):
        '''Get the pre-analyzed FS for word.'''
        return self.analyzed.get(word)

    def set_analyzed(self, filename='analyzed.lex', ortho=True, verbose=False):
        '''
        Set the dict of analyzed words, reading them in from a file, one per
        line.
        '''
        if not ortho:
            filename = 'analyzed_phon.lex'
        path = os.path.join(self.get_lex_dir(), filename)
#        path = os.path.join(self.directory, filename)
        if os.path.exists(path):
            file = open(path, encoding='utf8')
            if verbose:
                print('Storing pre-analyzed forms')
            if ortho:
                for line in file:
                    # Word and FS separated by two spaces
                    word, anal = line.split('  ')
                    fs = FSSet.parse(anal.strip())
                    self.analyzed[word] = fs
            else:
                for line in file:
                    # Word and FS separated by two spaces
                    word, phon, anal = line.split('  ')
                    fs = FSSet.parse(anal.strip())
                    self.analyzed_phon[word] = (phon, fs)
            file.close()

    def strip_suffixes(self, word, guess=False, phon=False, segment=False, verbose=False):
        '''Check to see if the word can be directly segmented into a stem and one or more suffixes.'''
        if self.suffixes:
            result = []
            stripped = strip.sufstrip(word, self.suffixes)
            if stripped:
                for segs, gram, anal in stripped:
                    if anal:
                        # 'segs' needs to be analyzed further
                        # First separate the stem from segs and find the POS
                        stem, x, suffixes = segs.partition('+')
#                        print("Stem {} suffixes {}".format(stem, suffixes))
#                        pos = gram.get('pos')
                        # Now use the anal FST for that POS to transduce the stem starting
                        # from the grammatical FSSet as an initial weight
                        fst = self[anal].get_fst(False, guess=guess, phon=phon, segment=segment)
                        anals = fst.transduce(stem, seg_units=self.seg_units, reject_same=guess,
                                              init_weight=gram)
                        if not anals:
                            continue
                        # Return each root and FS combination, as expected by language.anal_word()
                        for root, anls in anals:
                            for a in anls:
                                result.append([root + '+' + suffixes, a])
                    else:
                        result.append([segs, gram])
            return result

    def set_suffixes(self, filename='suf.lex', verbose=False):
        '''Set the dict of suffixes that can be stripped off.'''
        path = os.path.join(self.get_lex_dir(), filename)
        if os.path.exists(path):
            print("Loading suffixes from {}".format(path))

            current_pos = None
            current_suffix = None
            current_attribs = None
            functions = {}
            patterns = {}
            grams = {}

            with open(path, encoding='utf8') as file:
                for line in file:
                    line = line.split('#')[0].strip() # strip comments

                    if not line:
                        continue

                    m = Morphology.pattern.match(line)
                    if m:
                        patname = m.group(1)
                        regex = m.group(2)
#                        print("Pattern {} with regex {}".format(patname, regex))
                        patterns[patname] = re.compile(regex)
                        continue
                    m = Morphology.POS.match(line)
                    if m:
                        current_pos = m.group(1)
                        continue
                    m = Morphology.grammar.match(line)
                    if m:
                        gname = m.group(1)
                        fs = m.group(2)
#                        print("Grammar pattern {} with FS {}".format(fname, fs))
                        grams[gname] = FSSet.parse(fs)
                        continue
                    m = Morphology.function.match(line)
                    if m:
                        name = m.group(1)
                        args = m.group(2)
                        lg_arg = "lg=self.language, "
                        curry = "strip.sub_curry("
                        call = curry + lg_arg + args + ")"
#                        print("Function {}, call {}".format(name, call))
                        function = eval(call)
#                        print("Function {}: {}".format(name, function))
                        functions[name] = function
                        continue
                    m = Morphology.suffix.match(line)
                    if m:
                        if current_suffix:
                            if current_suffix in self.suffixes:
                                self.suffixes[current_suffix].extend(current_attribs)
                            else:
                                self.suffixes[current_suffix] = current_attribs
                        current_suffix = m.group(1)
                        current_attribs = m.group(2)
                        if current_attribs:
                            current_attribs = [current_attribs.strip()]
                        else:
                            current_attribs = []
#                        print("Suffix {}, segmentation {}".format(current_suffix, current_attribs))
                        continue
                    if current_suffix:
                        # This line represents a dict of suffix attribs for a particular case
                        # ; separate different attribs
                        attrib_dict = {}
                        suff_attribs = line.split(';')
                        for attrib in suff_attribs:
                            # We need partition instead of split because there
                            # can be other = to the right in a feature-value expression
                            typ, x, value = attrib.strip().partition('=')
                            if typ == 'pat':
                                if value not in patterns:
                                    print("Pattern {} not in pattern dict".format(value))
                                else:
                                    value = patterns[value]
                            elif typ == 'change':
                                if value not in functions:
                                    print("Function {} not in function dict".format(value))
                                else:
                                    value = functions[value]
                            elif typ == 'gram':
                                if value in grams:
                                    value = grams[value]
                                else:
                                    value = FSSet.parse(value)
                            attrib_dict[typ] = value
                        if 'pos' not in attrib_dict:
                            attrib_dict['pos'] = current_pos
                        current_attribs.append(attrib_dict)
                if current_suffix:
                    # Current suffix attribs not yet added to suffixes
                    if current_suffix in self.suffixes:
                        self.suffixes[current_suffix].extend(current_attribs)
                    else:
                        self.suffixes[current_suffix] = current_attribs

#            print('patterns {}'.format(patterns))
#            print('functions {}'.format(functions))

    def set_fsh(self, *label_fs):
        """Set the Feature Structure Hierarchy for this language's morphology."""
        self.fsh = FSHier()
        self.fsh.parse(label_fs)

    def trivial_anal(self, form):
        """Attempt to trivially analyze form."""
        return self.triv_anal and self.triv_anal(form)

    def anal(self, form, pos, to_dict=True, preproc=False, guess=False, phon=False, segment=False,
             trace=False, tracefeat=''):
        return self[pos].anal(form, to_dict=to_dict, preproc=preproc, guess=guess, phon=phon, segment=segment,
                              trace=trace, tracefeat=tracefeat)

    def gen(self, form, features, pos, from_dict=True, postproc=False, guess=False, phon=False, segment=False,
            trace=False):
        return self[pos].gen(form, features, from_dict=from_dict, postproc=postproc,
                             guess=guess, phon=phon, segment=segment, trace=trace)

    def restore_fst(self, label, create_networks=False, pos=''):
        '''Return the FST with label.'''
        cas_path = os.path.join(self.get_cas_dir(), label + '.cas')
        cascade = None
        if os.path.exists(cas_path):
            cascade = FSTCascade.load(cas_path,
                                      language=self.language, pos=pos,
                                      seg_units=self.seg_units,
                                      create_networks=create_networks,
                                      verbose=False)
        if cascade != None:
#            print('Restoring FST', label)
            # Look for the full, explicit FST
            fst_file = label + '.fst'
            fst_path = os.path.join(self.get_pickle_dir(), fst_file)
            if os.path.exists(fst_path):
                return FST.restore_parse(self.get_pickle_dir(), fst_file, cascade=cascade,
                                         weighting=UNIFICATION_SR,
                                         seg_units=self.seg_units,
                                         create_weights=True)

    def load_phon_fst(self, save=True, pos='', verbose=True):
        """Load the phon FST if there is one."""
        cascade = FSTCascade.load(os.path.join(self.get_cas_dir(), 'phon.cas'),
                                  language=self.language, pos=pos,
                                  seg_units=self.seg_units, create_networks=True,
                                  verbose=verbose)
        if cascade:
            fst = cascade.compose(backwards=False, trace=verbose)
            if fst:
                fst = fst.inverted()
                if save:
                    FST.write(fst, filename=os.path.join(self.get_pickle_dir(), 'phon.fst'))
                    self.phon_fst = fst
                return fst

    def ortho2phon(self, word):
        '''
        Attempt to convert a word to its phonetic form. (Assumes word is
        already romanized.)
        '''
        if word.isdigit():
            # word consists only of numbers
            return [word]
        if self.words_phon:
            words = self.words_phon
            if not isinstance(words, dict):
                print('Words dict is not loaded!')
                return
            phon = words.get(word, '')
            if phon:
                return [phon]
        elif word in self.analyzed_phon:
            form, fss = self.analyzed_phon[word]
            return [form]

    def phonetic(self, form):
        '''
        Make a form phonetic, calling the phon FST on it.
        '''
        fst = self.phon_fst
        if fst:
            phoneticized = fst.transduce(form, seg_units=self.seg_units)
            if phoneticized:
                return phoneticized[0][0]
        return form

    ### Various feature-related static methods

    @staticmethod
    def get_sense(fs):
        '''
        fs should be a FeatStruct or a FSSet with only one member.
        '''
        if isinstance(fs, FSSet) and len(FSSet) == 1:
            print("Warning: trying to get sense from FSSet {}".format(fs.__repr__()))
            return Morphology.default_sense
        return fs.get('sns', Morphology.default_sense)

class POSMorphology:
    """
    Lists of MorphCats and GramCats, anal and gen FSTs for a particular POS class.
    """

    segsep = '-'
    stemstart = '<'
    stemend = '>'

    segment_re = re.compile("(.+)<(.+)>(.+)")

    # Indices for different FSTs in self.fsts
    # Top level
    anal_i = 0
    gen_i = 1
    trans_i = 2
    # Indices within sublists
    guess_i = 1
    # Used for Amharic noun translation
    simp_i = 2
    phon_i = 3
    guessphon_i = 4
    seg_i = 5
    # New, "experimental" FST types: "X"
    exp_i = 6

    def __init__(self, pos, feat_list=None, lex_feats=None, excl_feats=None,
                 feat_abbrevs=None, fv_abbrevs=None, fv_dependencies=None, fv_priority=None,
                 feature_groups=None, name=None, explicit=None, true_explicit=None,
                 lemma_feats=None, segments=None, mwe_feats=None, mwe=True):
        # A string representing part of speech
        self.pos = pos
        # A string representing the full name of the POS
        self.name = name or pos
        # Weight constraint on FST arcs
        self.wc = None if pos == 'all' else FSSet('[pos=' + pos + ']')
        # The string used as type in FSs
        self.type = '%' + pos
#        # List of changeable features (not used for AfSem)
#        self.changefeats = changefeats
        # FSTs: [[anal, anal0, None, anal_P, anal0_P, anal+, analX],
        #        [gen, gen0, None, gen_P, gen0_P, (gen+), genX]],
        #        [trans, trans0, None, trans_P, trans0_P, (trans+), transX]]
        self.fsts = [[None, None, None, None, None, None, None],
                     [None, None, None, None, None, None, None],
                     # Translation FSTs
                     {},
                     ]
        self.mwefsts = [[None, None, None, None, None, None, None],
                        [None, None, None, None, None, None, None],
                        # Translation FSTs
                        {}
                            ]
        # Added for V5.
        self.fst_dict = {}
        # FST cascade
        self.casc = None
        self.mwecasc = None
        self.casc_inv = None
        self.morphology = None
        self.language = None
        # Default FS for generation
        self.defaultFS = ''
        # Default FS for citation
        self.citationFS = ''
        # Dictionary of FS implications
        self.FS_implic = {}
        ## Functions
        self.anal_to_dict = lambda root, fs: {'root': root}
        self.dict_to_anal = lambda root, dct: ['', FSSet('[]')]
        # Generate citation form; a function taking 
        self.citation = None
        # Analysis to string
        self.anal2string = None
        # Postprocess (roots might be treated specially)
        self.postprocess = None
        # Pair of dicts of common and irregular analyzed words: (complex, simple)
        self.analyzed = ({}, {})
        self.analyzed_phon = ({}, {})
        # Reverse dict for analyzed words, used in generation (derived from analyzed[0])
        self.generated = {}
        # Dict of possible grammatical features and their values
        self.features = {}
        # List of morpheme labels
        self.morphs = []
        # List of most "interesting" features
        self.sig_features = []
        # Defective roots
        self.defective = []
        ## Features
        # List of features and possible values
        self.feat_list = feat_list or []
        # List of lexical features: excluded from default for generation
        self.lex_feats = lex_feats or []
        # List of features to exclude from printed analysis output
        self.excl_feats = excl_feats or []
        # Features to include in pretty analysis output and web app
        self.explicit_feats = explicit or []
        # Features to include in pretty analysis output only if they're not False or None
        self.true_explicit_feats = true_explicit or []
        # List of abbreviations for features
        self.feat_abbrevs = feat_abbrevs or {}
        # List of abbreviations for feat-value combinations
        self.fv_abbrevs = fv_abbrevs or []
        # List of feature-value dependencies
        self.fv_dependencies = fv_dependencies or {}
        # List of feature-value pairs that have priority over others in displaying
        self.fv_priority = fv_priority or []
        # List of feature labels and value count for web app
        self.web_features = []
        # List of feature groups [([features], group_name),...]
        self.feature_groups = feature_groups or None
        # Features for generating lemma
        self.lemma_feats = lemma_feats
        # Segments and their properties
        self.segments = segments
        # MWE feats for this POS
        self.mwe_feats = mwe_feats
        # Whether there is a MWE FST for this POS
        self.mwe = mwe
        # Frequency statistics for generation
        self.root_freqs = None
        self.feat_freqs = None
        # A function of root and FeatStruc for postprocessing of roots
        self.root_proc = None
        # A dictionary from orthographic roots to phonetic roots
        self.ortho2phon = None
        # Dict specifying feature normalization
        self.featnorm = []
        # Dict of roots and feature constraints
        # {'ጥብቅ': [c=A];[c=B], 'ቅምጥ': [c=B,v=p|as], ...}
        self.rootfeats = {}

    def __str__(self):
        '''Print name.'''
        return self.pos + '_morphology'

    def __repr__(self):
        '''Print name.'''
        return self.pos + '_morphology'

    def get_fst(self, generate=False, guess=False, simplified=False,
                phon=False, segment=False, translate=False, experimental=False,
                mwe=False, tl='', v5=False, suffix=''):
        """
        The FST satisfying the parameters.
        """
        if v5:
            name = self.fst_name(generate=generate, guess=guess, translate=translate, mwe=mwe, suffix=suffix)
            fst = self.fst_dict.get(name)
            if not fst:
                print("*** No FST stored for {}".format(name))
                return
            return fst
#        print("*** Getting FST {} {} {} {} {} {} {} {}".format(generate, guess, simplified, phon, segment, translate, experimental, mwe))
        if translate:
            return self.fsts[self.trans_i].get(tl)
        analgen = None
        fsts = self.mwefsts if mwe else self.fsts
        if generate:
            analgen = fsts[self.gen_i]
        else:
            analgen = fsts[self.anal_i]
        if experimental:
            fst = analgen[self.exp_i]
        elif guess:
            if phon:
                fst = analgen[self.guessphon_i]
            else:
                fst = analgen[self.guess_i]
        elif simplified:
            fst = analgen[self.simp_i]
        elif phon:
            fst = analgen[self.phon_i]
        elif segment:
            fst = analgen[self.seg_i]
        else:
            fst = analgen[0] or analgen[self.guess_i] or analgen[self.simp_i]
        return fst

    def set_fst(self, fst, generate=False, guess=False, simplified=False,
                phon=False, segment=False, translate=False, experimental=False,
                mwe=False, tl='', suffix='', v5=False):
        """
        Assign the FST satisfying the parameters.
        """
        if v5:
            name = self.fst_name(generate=generate, guess=guess, translate=translate, mwe=mwe, suffix=suffix)
            self.fst_dict[name] = fst
            return
        # Translation is special because there's a dict with language abbrevs as keys
        if translate:
            self.fsts[self.trans_i][tl] = fst
        else:
            index2 = 0
            # Experimental FSTs have priority
            if experimental:
                index2 = self.exp_i
            elif simplified:
                index2 = self.simp_i
            elif guess:
                if phon:
                    index2 = self.guessphon_i
                else:
                    index2 = self.guess_i
            elif phon:
                index2 = self.phon_i
            elif segment:
                index2 = self.seg_i
            index1 = self.anal_i
            if generate:
                index1 = self.gen_i
            fsts = self.mwefsts if mwe else self.fsts
            fsts[index1][index2] = fst
        # Also assign the defaultFS if the FST has one
        # NOTE: DIFFERENT FSTs FOR THE SAME POS SHOULD AGREE ON THIS
        if fst._defaultFS:
            self.defaultFS = fst._defaultFS.__repr__()
#            print(self, 'assigned default FS', self.defaultFS)

    def relabel(self, generate=False, guess=False, simplified=False,
                phon=False, segment=False, translate=False, mwe=False, suffix='',
                v5=False):
        """
        Relabel an FST by simplifying state names.
        """
        f = self.get_fst(generate=generate, guess=guess, simplified=simplified,
                         phon=phon, segment=segment, translate=translate, mwe=mwe,
                         suffix=suffix, v5=v5)
        fr = f.relabeled(f.label, trace=1)
        self.set_fst(fr, generate=generate, guess=guess, simplified=simplified,
                     phon=phon, segment=segment, translate=translate, mwe=mwe,
                     suffix=suffix, v5=v5)

    def fst_name(self, generate=False, guess=False, simplified=False,
                 phon=False, segment=False, translate=False, experimental=False,
                 mwe=False, suffix=''):
        """
        Make a name for the FST satisfying the parameters.
        M: MWE; 0: guess; G|T: generation|translation; suffix: an arbitrary abbreviation
        POS (M) (0) (G|T) (suffix)
        """
        pos = self.pos
        # MWEs
        if mwe:
            pos += 'M'
        # Experimental FSTs have priority; later include A, G, or + in suffix depending
        # on experimental FST type.
        if experimental:
            pos += 'X'
        elif guess:
            pos += '0'
            if phon:
                pos += 'P'
        elif simplified:
            pos += '_S'
        elif phon:
            pos += 'P'
        elif segment:
            pos += '+'
        if generate:
            pos += 'G'
        elif translate:
            pos += 'T'
        if suffix:
            pos += suffix
        return pos

    def get_analyzed(self, word, init_weight=None, simple=False, sep_anals=False, segment=False):
        """Stored analysis of word if there is one."""
        if self.analyzed:
            anals = self.analyzed[Morphology.simple if simple else Morphology.complex].get(word, None)
            if anals:
                root = anals[0]
                gram = anals[1]
                if init_weight:
                    if not isinstance(init_weight, FSSet):
                        init_weight = FSSet(init_weight)
                    gram = gram.unify(init_weight)
                    if not gram:
                        return []
                if sep_anals:
                    anals = [(root, anal) for anal in gram]
                else:
                    anals= [root, gram]
            return anals

    def set_ortho2phon(self, verbosity=0):
        """
        If <POS>_ortho.lex file exists, set ortho2phon dict.
        """
        path = os.path.join(self.morphology.get_lex_dir(),
                            self.pos + '_ortho.lex')
        if os.path.exists(path):
            dct = {}
            self.ortho2phon = dct
            with open(path, encoding='utf8') as file:
                for line in file:
                    phon, ortho = line.split()
                    dct[phon.strip()] = ortho.strip()
        elif verbosity:
            print("No ortho file for {}:{}".format(self.language, self.pos))

    def set_analyzed(self, filename='analyzed.lex', ortho=True, simplify=True, verbose=False):
        '''
        Set the dict of analyzed words, reading them in from a file, one per
        line.
        '''
        if not ortho:
            filename = 'analyzed_phon.lex'
        path = os.path.join(self.morphology.get_lex_dir(), self.pos + '_' + filename)
        if os.path.exists(path):
            file = open(path, encoding='utf8')
            if verbose:
                print('Storing irregular pre-analyzed forms:', self.pos)
            for line in file:
                # For ortho=True, each line is
                # word  root  FSS
                # For ortho=False, each line is
                # word phon root FSS
                split_line = line.partition(' ')
                word = split_line[0]
                if not ortho:
                    split_line = split_line[2].strip().partition(' ')
                    phon = split_line[0]
                split_anal = split_line[2].strip().partition(' ')
                root = split_anal[0]
                fs = split_anal[2]
                if word and fs:
                    if not root:
                        root = word
                    fs = FSSet.parse(fs)
                    if ortho:
                        self.analyzed[Morphology.complex][word] = [root, fs]
                    else:
                        self.analyzed_phon[Morphology.complex][word] = [phon, root, fs]
                    if simplify and self.morphology.simplify:
                        word = self.morphology.simplify(word)
                        root = self.morphology.simplify(root)
                        if ortho:
                            self.analyzed[Morphology.simple][word] = [root, fs]
                        else:
                            self.analyzed_phon[Morphology.simple][word] = [phon, root, fs]
            file.close()

    def set_root_freqs(self):
        """If there's a root statistics file for generation for this POS, load it."""
        filename = self.pos + '_root_freqs.dct'
        path = os.path.join(self.morphology.get_stat_dir(), filename)
        try:
            with open(path, encoding='utf-8') as roots:
                self.root_freqs = eval(roots.read())
        except IOError:
            pass
#            print('No generation root frequency file {} found for {}'.format(path, self.pos))

    def set_feat_freqs(self):
        """If there's a feat statistics file for generation for this POS, load it."""
        filename = self.pos + '_feat_freqs.dct'
        path = os.path.join(self.morphology.get_stat_dir(), filename)
        try:
            with open(path, encoding='utf-8') as feats:
                self.feat_freqs = eval(feats.read())
        except IOError:
            pass
#            print('No generation feature frequency file {} found for {}'.format(path, self.pos))

    def make_generated(self):
        """Create a dictionary of analyzed words for generation."""
        analyzed = self.analyzed[Morphology.complex]
        # Only create the dict if there's a corresponding analyzed dict
        if analyzed:
            for word, (root, fs) in analyzed.items():
                # add an entry for this word form under the root
                if root in self.generated:
                    self.generated[root].append((fs, word))
                else:
                    self.generated[root] = [(fs, word)]

    def get_features(self):
        '''Get the dict of grammatical features and values, generating it if {}.'''
        if not self.features:
            fst = self.get_fst()
            if fst:
                self.features = fst.get_features()
        return self.features

    def has_cas(self, generate=False, simplified=False, guess=False,
                experimental=False, mwe=False, suffix='',
                phon=False, segment=False, translate=False):
        """Is there a cascade file for the given FST features?"""
#        print("** has_cas: experimental {}, segment {}".format(experimental, segment))
        name = self.fst_name(generate=generate, simplified=simplified,
                             guess=guess, phon=phon, segment=segment,
                             experimental=experimental, mwe=mwe, suffix=suffix,
                             translate=translate)
        path = os.path.join(self.morphology.get_cas_dir(), name + '.cas')
        return os.path.exists(path)

    ## Web app stuff

    def set_web_feats(self):
        """Set the list of feature labels and number of possible values."""
        if not self.web_features and self.explicit_feats:
            # Only do this if explicit features have been set and
            # web features have not been set (as happens in am_lang, etc.)
            feat_dict = dict(self.feat_list)
            for f in self.explicit_feats:
                flabel = self.feat_abbrevs.get(f, f)
                if flabel in [f[0] for f in self.web_features]:
                    # Feature already recorded
                    continue
                nvalues = 1
                if f in feat_dict:
                    # Feature groups won't be in feat_dict
                    v = feat_dict[f]
                    if isinstance(v, list):
                        nvalues = len(v)
                self.web_features.append((flabel, nvalues))

    # This is a mess. Fix it at some point.

    def load_fst(self, compose=False, subcasc=None, gen=False,
                 recreate=False, create_fst=True, create_casc=False,
                 create_weights=False, guess=False, seglevel=2,
                 pickle=True, create_pickle=True, fidel=False,
                 simplified=False, phon=False, segment=False, translate=False,
                 experimental=False, mwe=False, pos='', suffix='',
                 gemination=True,
                 invert=False, compose_backwards=True, split_index=0,
                 v5=False,
                 setit=True, relabel=True, verbose=False):
        '''
        Load FST; if compose is False, search for saved FST in file and use that if it exists.

        If guess is true, create the lexiconless guesser FST.
        2023.2.28: Added seglevel.
        '''
#        if mwe:

        # seglevel should be 0 if segment is 0
#        if not segment:
#            seglevel = 0
        
        fst = None
        name = self.fst_name(gen, guess, simplified, phon=phon, mwe=mwe, suffix=suffix,
                             segment=segment, translate=translate, experimental=experimental)
#        print("  *** load_fst {}, name {}, seglevel {}".format(pos, name, seglevel))
        path = os.path.join(self.morphology.get_cas_dir(), name + '.cas')
        if verbose:
            s1 = 'Attempting to load {0} FST for {1} {2}{3}{4}{5} (recreate {6})'
            print(s1.format(('TRANSLATION' if translate else ('GENERATION' if gen else 'ANALYSIS')),
                            self.language.label, self.pos,
                            (' (GUESSER)' if guess else ''),
                            (' (SEGMENTED)' if segment else (' (EXPERIMENTAL)' if experimental else '')),
                            (' (MWE)' if mwe else ''),
                            recreate))
        if not compose and not recreate:
            # Load a composed FST encompassing everything in the cascade
            fst = FST.restore(name, pos,
                              cas_directory=self.morphology.get_cas_dir(),
                              fst_directory=self.morphology.get_fst_dir(),
                              pkl_directory=self.morphology.get_pickle_dir(),
                              seg_units=self.morphology.seg_units, pickle=pickle,
                              create_weights=create_weights, generate=gen,
                              guess=guess, phon=phon, segment=segment, simplified=simplified,
                              experimental=experimental, mwe=mwe, suffix=suffix,
                              v5=v5,
                              verbose=verbose)
            if fst:
#                if mwe:
                fst, found_pickle = fst
#                print("   *** Found FST; path {}, label {}".format(path, fst.label))
                if found_pickle and verbose:
                    print("Finished unpickling {}".format(fst.label))
                if pickle and not found_pickle and create_pickle:
                    print("No pickle found for {}, creating one".format(name))
                    FST.pickle(fst, directory=self.morphology.get_pickle_dir(), label=name)
                if setit:
                    self.set_fst(fst, gen, guess, simplified, phon=phon, mwe=mwe, suffix=suffix,
                                 v5=v5,
                                 segment=segment, translate=translate, experimental=experimental)
                if create_casc and not self.casc:
                    casc = FSTCascade.load(path, seg_units=self.morphology.seg_units, posmorph=self,
                                           create_networks=True, subcasc=subcasc, seglevel=seglevel,
                                           language=self.language, gen=gen, pos=pos, gemination=gemination,
                                           verbose=verbose)
                    if casc:
                        self.casc = casc
                        self.casc_inv = self.casc.inverted()
        if not self.get_fst(gen, guess, simplified, phon=phon, translate=translate, segment=segment, suffix=suffix, v5=v5) or recreate:
            # Either there was no composed FST or we're supposed to recreate it anyway, so get
            # the cascade and compose it (well, unless create_fst is False)
#            if verbose:
#                print('Looking for cascade at', path, 'subcasc', subcasc)
            if os.path.exists(path):
                if recreate:
                    # Load each of the FSTs in the cascade and compose them
                    if verbose:
                        print('Recreating...')
                    self.casc = FSTCascade.load(path, seg_units=self.morphology.seg_units, posmorph=self,
                                                create_networks=True, subcasc=subcasc, pos=pos, seglevel=seglevel,
                                                gemination=gemination,
                                                language=self.language, gen=gen, verbose=verbose)
                    self.casc_inv = self.casc.inverted()
                    # create_fst is False in case we just want to load the individuals fsts.
                    if create_fst:
                        if verbose:
                            print("Composing analysis FST, reverse={}, split_index={}".format(self.casc.r2l, split_index))
                        if split_index:
                            fst = self.casc.rev_compose(split_index, trace=verbose)
                        else:
#                            print("*** Composing {}, relabel {}".format(self.casc, relabel))
                            fst = self.casc.compose(backwards=compose_backwards, trace=verbose, subcasc=subcasc,
                                                    relabel=relabel)
                        if self.casc.insertions:
                            # Insert insertion FSTs into composed FST
#                            print("*** {} has FST insertions {}".format(self.casc, self.casc.insertions))
                            start = fst._get_initial_state()
                            end = fst._get_final_states()[0]
                            for insertion in self.casc.insertions:
                                fst.insert(insertion, start, end)
                        if invert:
                            fst = fst.inverted()
                        if setit:
                            self.set_fst(fst, gen, guess, simplified, phon=phon, mwe=mwe,
                                         suffix=suffix, v5=v5,
                                         segment=segment, translate=translate, experimental=experimental)
                        self.casc.append(fst)
                elif verbose:
                    print("Not recreating FST")
            elif verbose:
                print('  No cascade exists at', path, end=' ')
                if gen: print()
#        if gen:
#            # Look for or load generation FST
#            if not self.load_fst(compose=False, gen=True,
#                                 create_casc=create_casc, pickle=pickle, pos=pos,
#                                 guess=guess, simplified=simplified, experimental=experimental,
#                                 phon=phon, segment=segment, translate=translate, mwe=mwe,
#                                 suffix=suffix, v5=v5,
#                                 invert=True, verbose=verbose):
#                # Explicit generation FST not found, so invert the analysis FST
#                if verbose:
#                    print("... inverting analysis FST")
#                fst = fst or \
#                  self.get_fst(False, guess, simplified, phon=phon, mwe=mwe, suffix=suffix,
#                               v5=v5,
#                               segment=segment, translate=translate, experimental=experimental)
#                if fst:
#                    if setit:
#                        self.set_fst(fst.inverted(), True, guess, simplified, mwe=mwe,
#                                     suffix=suffix, v5=v5,
#                                     phon=phon, segment=segment, experimental=experimental)
#                    if create_casc:
#                        if not self.casc:
#                            casc = FSTCascade.load(path, seg_units=self.morphology.seg_units, posmorph=self,
#                                                   create_networks=True, subcasc=subcasc,
#                                                   gemination=gemination,
#                                                   language=self.language, gen=gen, pos=pos,
#                                                   verbose=verbose)
#                            if casc:
#                                self.casc = casc
#                                self.casc_inv = self.casc.inverted()
#                else:
#                    name = self.fst_name(False, guess, simplified, phon=phon, mwe=mwe, suffix=suffix,
#                                         segment=segment, translate=translate, experimental=experimental)
#                    path = os.path.join(self.morphology.get_cas_dir(), name + '.cas')
#                    # OK, as a last resort, try again to load the analysis cascade
#                    if os.path.exists(path):
#                        casc = FSTCascade.load(path, seg_units=self.morphology.seg_units, posmorph=self,
#                                               create_networks=True, subcasc=subcasc, gemination=gemination,
#                                               language=self.language, pos=pos, gen=gen,
#                                               verbose=verbose)
#                        if casc:
#                            self.casc = casc
#                            self.casc_inv = self.casc.inverted()
        if not setit:
            return fst
        return self.get_fst(gen, guess, simplified, phon=phon, mwe=mwe, suffix=suffix,
                            v5=v5,
                            segment=segment, translate=translate, experimental=experimental)
#            # FST found one way or another
#            return True

    def load_trans_fst(self, trg_pos_morph, pos, lextrpos=None, gen=True, suffix='', v5=False):
        """
        Create a translation FST by composing the source analysis FST with the target generation FST.
        If gen is False, only create an FST for source analysis and lexical translation.
        """
        print("*** Creating {} translation FST for {} -> {}".format(pos, self, trg_pos_morph))
        src_language = self.language
        trg_language = trg_pos_morph.language
        trg_abbrev = trg_language.abbrev

        def load_trans1(posmorph, gen=False):
            name = posmorph.fst_name(gen, False, suffix=suffix)
            path = os.path.join(posmorph.morphology.get_cas_dir(), name + '.cas')
            casc = FSTCascade.load(path, seg_units=posmorph.morphology.seg_units, seglevel=0, posmorph=posmorph,
                                   gemination=src_language.output_gemination,
                                   create_networks=True, language=posmorph.language, gen=gen, pos=pos)
            posmorph.casc = casc
            posmorph.casc_inv = posmorph.casc.inverted()
            fst = posmorph.casc.compose(backwards=False, relabel=True)
            if gen:
                fst = fst.inverted()
            # Do this after inversion or before?
            if posmorph.casc.insertions:
                start = fst._get_initial_state()
                end = fst._get_final_states()[0]
                for insertion in posmorph.casc.insertions:
                    fst.insert(insertion, start, end)
            posmorph.set_fst(fst, gen, False, False, segment=False, suffix=suffix, v5=v5)
            posmorph.casc.append(fst)
            return fst

        # Source FST
        src_fst = load_trans1(self, gen=False)
        # Target FST
        if gen:
            trg_fst = load_trans1(trg_pos_morph, gen=True)
        # Lextr FST
        lextrpos = lextrpos or pos
        lextrpath = os.path.join(self.morphology.get_fst_dir(), lextrpos + '.lextr')
        s = open(lextrpath, encoding='utf8').read()
        lextr_fst = LexTrans.parse("lextr", s, cascade=self.casc,
                                   fst=FST('lextr', cascade=self.casc, weighting=UNIFICATION_SR)
                                   )
        if gen:
            trans_fst = FST.compose([src_fst, lextr_fst, trg_fst], label='{}2{}'.format(self.language.abbrev, trg_pos_morph.language.abbrev), reverse=False)
        else:
            trans_fst = FST.compose2(src_fst, lextr_fst, label="{}2lextr".format(self.language.abbrev), reverse=False)
        # Translation FST
#        trans_fst = FST.compose2(src_fst, trg_fst, label="{}2{}".format(self.language.abbrev, trg_pos_morph.language.abbrev), reverse=False)
        self.set_fst(trans_fst, translate=True, tl=trg_abbrev, suffix=suffix, v5=v5)

    def pickle_all(self, replace=True, empty=True):
        """
        Pickle the FSTs for this POS. If replace is False, don't
        replace existing pickles.
        """
        directory = self.morphology.get_pickle_dir()
        explicit = self.fsts[0]
        empty_fsts = self.fsts[1]
        for fst in explicit:
            if fst:
                FST.pickle(fst, directory=directory, replace=replace)
        if empty:
            for fst in empty_fsts:
                if fst:
                    FST.pickle(fst, directory=directory, replace=replace)

#    def save(self, gen=True, pickle=False):
#        '''
#        Save analysis and generation FSTs to files.
#        '''
#        self.save_fst(generate=False, guess=False, phon=False, segment=False, translate=False, experimental=False,
#                      mwe=False, pickle=pickle)
#        if gen:
#            self.save_fst(generate=True, guess=False, phon=False, segment=False, translate=False, experimental=False,
#                          mwe=False, pickle=pickle)

    def save_fst(self, generate=False, guess=False, simplified=False,
                 phon=False, segment=False, translate=False, experimental=False, mwe=False,
                 features=True, defaultFS=True, stringsets=True, suffix='',
                 v5=False,
                 pickle=False):
        '''Save FST in a file.'''
        fname = self.fst_name(generate=generate, guess=guess, simplified=simplified,
                              experimental=experimental, mwe=mwe, suffix=suffix,
                              phon=phon, segment=segment, translate=translate)
#        print("FNAME {}".format(fname))
        extension = '.fst'
        fst = self.get_fst(generate=generate, guess=guess, simplified=simplified,
                           experimental=experimental, mwe=mwe, suffix=suffix,
                           v5=v5,
                           phon=phon, segment=segment, translate=translate)
#        print("FST to save: {}".format(fst))
        directory = self.morphology.directory
        if defaultFS:
            df = self.defaultFS.__repr__()
        else:
            df = ''
        directory = FST.get_pickle_dir(self.morphology.language)
        FST.write(fst, filename=os.path.join(directory, fname + extension),
                  defaultFS=df, stringsets=stringsets,
                  features=features, exclude_features=['t', 'm'])
        if pickle:
            FST.pickle(fst, directory=self.morphology.get_pickle_dir(), replace=True)
        else:
            self.delete_pickle(fname)

    def unsave_fst(self, fst_file=True):
        '''Get rid of saved FSTs.'''
        if fst_file:
            os.remove(os.path.join(self.morphology.get_pickle_dir(), self.pos + '.fst'))

    def delete_pickle(self, fname):
        '''
        Get rid of pickle for this POS (when saving new FST) if it exists.
        '''
        try:
            os.remove(os.path.join(self.morphology.get_pickle_dir(), fname + '.pkl'))
            print("Removing pickle file for {}".format(fname))
        except FileNotFoundError:
            pass

    def analyze(self, form, init_weight=None, guess=False):
        """Try analyzed list first; then run anal() if that fails."""
        preanal = self.get_analyzed(form, init_weight=init_weight)
        if preanal:
            # To make the comparable to anal(), a list of lists of analyses.
            return [preanal]
        else:
            return self.anal(form, init_weight=init_weight, guess=guess)

    def anal(self, form, init_weight=None, preproc=False,
             guess=False, simplified=False, phon=False, segment=False,
             result_limit=0, experimental=False, mwe=False, suffix='',
             to_dict=False, sep_anals=False, normalize=False, v5=False,
             timeit=False, trace=False, tracefeat='', verbosity=0):
        """
        Analyze form.
        """
        fst = self.get_fst(generate=False, guess=guess, phon=phon, segment=segment, v5=v5,
                           suffix=suffix, experimental=experimental, mwe=mwe, translate=False)

        # Get the right FST.
        # Experimental FSTs have priority over others, but note that segment will
        # also be true if experimental FST is a segmenter.
        # MWE or single word
        if fst:
            if mwe:
                form = form.replace(' ', Morphology.mwe_sep)
            if preproc:
                # For languages with non-roman orthographies
                form = self.language.preprocess(form)
            if init_weight and not isinstance(init_weight, FSSet):
                init_weight = FSSet(init_weight)
            # default increased to 100 because analyzer and segmenter fail to find best analyses of እንዳላቸው; 2022-09-28
            result_limit = result_limit if result_limit else 100
#            (40 if guess else 30)
#            print("** Analyzing {} with result limit {}".format(form, result_limit))
            # If result is same as form and guess is True, reject
            anals = fst.transduce(form, seg_units=self.morphology.seg_units, reject_same=guess,
                                  init_weight=init_weight, result_limit=result_limit,
                                  trace=trace, tracefeat=tracefeat, timeit=timeit,
                                  verbosity=verbosity)
            if sep_anals or normalize:
                # Normalization requires FeatStructs so separate
                # anals if it's True
                anals = self.separate_anals(anals, normalize=normalize)
            if to_dict:
                anals = self.anals_to_dicts(anals)
            if verbosity:
                print("** anal: {}".format(anals))
            return anals
        elif trace:
            print('No analysis FST loaded for', self.pos)

    def seganal(self, word):
        '''
        Convenient for running anal for segmentation.
        '''
        return self.anal(word, segment=True, experimental=True)

    ##
    ## Processing output of anal or gen, v.5.
    ##

    def process_segstring(self, string, **kwargs):
        '''
        Postprocess the segment string returned by POSMorph.anal(), degeminating and
        combining stem segs if indicated.
        Return the whole string, prefixes, stem, and suffixes
        kwargs: degem=False, mwe=False, combine_segs=False):
        '''
        if kwargs.get('degem', False):
            string = EES.degeminate(string)
        if kwargs.get('mwe', False):
            string.replace(Morphology.mwe_sep, ' ')
        match = POSMorphology.segment_re.match(string)
        pre, stem, suf = match.groups()
        if kwargs.get('combine_segs', False):
            stem = self.language.combine_segments(stem)
            string = "{}<{}>{}".format(pre, stem, suf)
        pre = pre.split(Morphology.morph_sep)
        suf = suf.split(Morphology.morph_sep)
#        print("** {} ; {} ; {}".format(pre, stem, suf))
        return string, pre, stem, suf
#        return {'string': string, 'pre': pre, 'stem': stem, 'suf': suf}

    def process_all5(self, token, analyses, raw_token, **kwargs):
        '''
        analyses is the output of anal(), a list of string, FSS pairs.
        If gemination is False, all gemination characters are removed.
        kwargs: mwe=False, degem=True, sep_feats=True, combine_segs=False
        Instance of Word is returned.
        '''
        analyses = self.separate_anals(analyses)
        result = []
        for string, FS in analyses:
            result.append(self.process5(token, string, FS, raw_token, **kwargs))
        return result

    def process5(self, token, string, features, raw_token, **kwargs):
        """
        string is a (probably segmented) analysis of a word or MWE.
        features is a FeatStruct.
        kwargs: mwe=False, sep_feats=True, combine_segs=False
        """
#        print("** process 5 {} {}".format(token, string))
        string, prefixes, stem, suffixes = self.process_segstring(string, **kwargs)
#        string = processed_string['string']
#        prefixes = processed_string['pre']
#        stem = processed_string['stem']
#        suffixes = processed_string['suf']
        procdict = {'token': token, 'feats': features, 'string': string}
        sep_feats = kwargs.get('sep_feats', False)
        if kwargs.get('mwe', False):
            # For properties, prefer specific lexical ones over generic lexical ones
            props = features.get('mwe') or self.mwe_feats
            token_dicts = self.get_mwe_tokens(token, self.mwe_feats)
            procdict['tokens'] = token_dicts
#            print("  ** token dicts {}".format(token_dicts))
        if raw_token:
            procdict['raw'] = raw_token
#        prefixes, stem, suffixes = self.get_segments(string, features)
        procdict['nsegs'] = len([p for p in prefixes if p]) + 1 + len([s for s in suffixes if s])
        root = features.get('root', stem)
        procdict['root'] = root
        lemma = self.gen_lemma(stem, root, features)
        procdict['lemma'] = lemma
        um = self.language.um.convert(features, pos=self.pos)
        procdict['um'] = um
        POS = features.get('pos', self.pos)
        procdict['pos'] = POS
        udfdict = self.language.um.convert2ud(um, self.pos, extended=True, return_dict=True) if um else None
#        udfdict = dict([u.split("=") for u in udfeats.split("|")])
#        procdict['udfeats'] = udfeats
        if self.segments:
            preprops, stemprops, sufprops = self.segments
            pre_dicts = []
            post_dicts = []
            aff_index = 0
            stem_index = len(prefixes)
            suff1_index = len(prefixes) + 1
            for pindex, (prefix, props) in enumerate(zip(prefixes, preprops)):
                pre_dicts.append(
                    self.process_morpheme5(prefix, props, pindex, stem_index, features, is_stem=False, udfdict=udfdict, sep_feats=sep_feats)
                    )
            prefixes = pre_dicts
            for sindex, (suffix, props) in enumerate(zip(suffixes, sufprops)):
                post_dicts.append(
                    self.process_morpheme5(suffix, props, sindex+suff1_index, stem_index, features, is_stem=False, udfdict=udfdict, sep_feats=sep_feats)
                    )
            suffixes = post_dicts
            if stemprops:
                stem_dict = \
                  self.process_morpheme5(stem, stemprops, stem_index, stem_index, features, is_stem=True, udfdict=udfdict, sep_feats=sep_feats)
                stem = stem_dict
        procdict['pre'] = prefixes
        procdict['suf'] = suffixes
        procdict['stem'] = stem

        return procdict

    def get_mwe_tokens(self, tokens, props):
        '''
        Return the tokens and their properties for a MWE output string.
        '''
#        print("** processing {} using feats {}".format(tokens, props))
        tokens = tokens.split()
        token_dicts = []
        if props:
            headfin = props.get('hdfin')
            deppos = props.get('deppos')
            headaff = props.get('hdaff')
            if headfin:
                for token in tokens[:-1]:
                    token_dicts.append({'token': token, 'pos': deppos, 'head': False})
                token_dicts.append({'token': tokens[-1], 'pos': self.pos, 'head': True})
            else:
                token_dicts.append({'token': tokens[0], 'pos': self.pos, 'head': True})
                for token in tokens[1:]:
                    token_dicts.append({'token': token, 'pos': deppos, 'head': False})
        return token_dicts

    def process_morpheme5(self, morpheme, props, index, stem_index, features, is_stem=False, udfdict=None, sep_feats=True):
        '''
        Create a dict for the affix or stem with properties from props.
        '''
        if not morpheme:
            # the morpheme could be the empty string
            return ''
#        print("** Processing morpheme {}: {} (stem i: {}, udfdict: {})".format(index, morpheme, stem_index, udfdict))
        dict = {'string': morpheme}
        pos = self.get_segment_pos(morpheme, props)
        dict['pos'] = pos
        dep, head = self.get_segment_dep_head(morpheme, props, index, stem_index, features, is_stem=is_stem)
        if dep:
            dict['dep'] = dep
        dict['head'] = head
        feats = None
        if sep_feats:
            feats = self.get_segment_feats(morpheme, props, udfdict)
        elif is_stem and udfdict:
            # Include all feats with stem if we're not separating feats by segment
            feats = list(udfdict.items())
            feats.sort()
            feats = '|'.join(['='.join([f, v]) for f, v in feats])
        if feats:
            dict['feats'] = feats
        return dict

#    def get_segment_props(self, string, segdict):
#        '''
#        string is a segment string.
#        segdict is the dict of properties for this segment position.
#        '''
#        pos = self.get_segment_pos(string, segdict)

    def get_segment_pos(self, string, segdict):
        posspec = segdict.get('pos')
        if not posspec:
            print("*** No POS in segdict {}".format(segdict))
            return
        if isinstance(posspec, dict):
            pos = posspec.get(EES.degeminate(string))
            if not pos:
                print("*** No POS for {} in seg postdict {}".format(string, posspec))
                return
            return pos
        return posspec

    def get_segment_feats(self, string, segdict, udfdict):
        '''
        Get the UD features that are specific to this segment.
        ufdict is a dict of UD features for the whole word.
        '''
        features = []
        # UD features relevant for this segment
        segfeats = segdict.get('feats')
        if not segfeats:
            return []
        for segfeat in segfeats:
            wordfeat = udfdict.get(segfeat)
            if wordfeat:
                features.append((segfeat, wordfeat))
        features.sort()
        return '|'.join(['='.join([f, v]) for f, v in features])

    def get_segment_dep_head(self, string, segdict, index, stem_index, features, framework='UD', is_stem=False):
        headspec = segdict.get('head')
        if headspec:
            # This is a relative index specifying the direction and distance of the head
            head_index = index + headspec
        else:
            # By default the head index is the stem index
            head_index = stem_index
        depspec = segdict.get('dep', '')
        dep = None
        if depspec:
            if isinstance(depspec, str):
                # string specifying the dep for all affixes in this position
                dep = depspec
            elif isinstance(depspec, tuple):
                # (feature, {...})
                depfeat = depspec[0]
                depvalue = features.get(depfeat)
                dep = depspec[1].get(depvalue)
#                print(" ** Value for feat {}: {}; dep {}".format(depfeat, depvalue, dep))
        return dep, head_index
 
    def gen_lemma(self, stem, root, features):
        lemmafeats = self.lemma_feats
        if not lemmafeats:
            return stem
        lemmafeat1, lemmafeats2 = lemmafeats
        if lemmafeat1:
            value1 = features.get(lemmafeat1, 0)
            if not value1:
                return stem
            initfeat = ["{}={}".format(lemmafeat1, value1)]
            for lf in lemmafeats2:
                value = features.get(lf)
                initfeat.append("{}={}".format(lf, value))
            initfeat = ','.join(initfeat)
            gen_out = self.gen(root, update_feats=initfeat)
            if gen_out:
                return gen_out[0][0]
            return
        initfeat = []
        for lf in lemmafeats2:
            value = features.get(lf)
            initfeat.append("{}={}".format(lf, value))
        initfeat = ','.join(initfeat)
        gen_out = self.gen(root, update_feats=initfeat)
        if gen_out:
            return gen_out[0][0]

    def separate_anals(self, analyses, normalize=False):
        """
        Separate list of root and FSSets into a list of roots and FeatStructs.
        If normalize is True, also normalize features in each FeatStruct.
        """
        result = []
        for root, anals in analyses:
            for anal in anals:
                if normalize:
                    anal = self.featconv(anal)
                result.append((root, anal))
        return result

    @staticmethod
    def separate_gens(gens, poss):
        """
        Separate list of output wordforms and associated analyses
        into wordform, FeatStruct tuples.
        poss is a list of POS tags for each gen
        """
        result = []
        pos_tags = []
        for gen, p in zip(gens, poss):
            # car and cadr are wordform and FSSet; there could also be score
            word = gen[0]
            fss = gen[1]
#            if len(fss) > 1:
#                print("MULT FS: {}".format(fss.__repr__()))
            for fs in fss:
                result.append((word, fs))
                pos_tags.append(p)
        return result, pos_tags

    def gen_from_pregen(self, root, features=None, only_one=True):
        """Generate word from saved generated dict."""
        generated = self.generated
        if generated:
            words = generated.get(root)
            if words:
                if not features:
                    if only_one:
                        return [[words[0][1], words[0][0]]]
                    else:
                        return [[word, feats] for feats, word in words]
                # Unify features with feats associated with wordform
                res = []
                for feats, word in words:
                    u = features.unify(feats)
                    if u:
                        if only_one:
                            return [[word, u]]
                        else:
                            res.append([word, u])
                return res

    def generate(self, root, features=None, guess=False, update_feats=None,
                 simplified=False, phon=False, segment=False, postproc=False,
                 print_word=False, print_prefixes=None, fst=None,
                 interact=True, timeit=False, timeout=100,
                 only_one=False, trace=False):
        """Generate word from root and features, first trying stored forms."""
        print("** Calling generate on {}".format(root))
        fss = None
        if not features:
            if interact and self.feat_list:
                features = self.fv_menu()
            else:
                features = self.defaultFS
        if update_feats:
            if isinstance(update_feats, (list, set)):
                fss = self.update_FSS(FeatStruct(features), update_feats)
            else:
                # Use explicit FS updates
                features = self.update_FS(FeatStruct(features), update_feats)
        if not features:
            return []
        if fss:
            features = fss
        else:
            features = FSSet.cast(features)
        pre_gen = self.gen_from_pregen(root, features, only_one=only_one)
        if pre_gen:
            return pre_gen
        fst = fst or self.get_fst(generate=True, guess=guess, simplified=simplified,
                                  phon=phon, segment=segment)
        if fst:
#            print('Transducing with features {}'.format(features.__repr__()))
            gens = fst.transduce(root, features, seg_units=self.morphology.seg_units, gen=True,
                                 print_word=print_word, print_prefixes=print_prefixes,
                                 trace=trace, timeit=timeit, timeout=timeout)
            if postproc:
                # For languages with non-roman orthographies
                for gen in gens:
                    # Replace the wordforms with postprocessed versions
                    gen[0] = self.language.postprocess(gen[0])
            return gens
        elif trace:
            print('No generation FST loaded')
            return []

    def gen(self, root, features=None, from_dict=False,
            postproc=False, update_feats=None, del_feats=None,
            guess=False, phon=False, segment=False, ortho=False,
            ortho_only=False, fst=None, sort=False, print_word=False, print_prefixes=None,
            interact=False, timeit=False, timeout=100, limit=10,
            trace=False, verbosity=0):
        """
        Generate word from root and features.
        2020.9.22: Added del_feats, a list of features or feature paths
          to delete from the features specified
        """
        fss = None
        if del_feats:
            # Transduction needs to run for a longer time when
            # there are fewer features
            timeout = 4000 * len(del_feats)
            limit = 4000 * len(del_feats)
        if interact and self.feat_list:
            # Get user input from menu
            features = self.fv_menu()
        else:
            features = features or self.defaultFS
        if del_feats:
            features = self.delete_from_FS(del_feats, fs=features)
        if update_feats:
            if isinstance(update_feats, (list, set)):
                fss = self.update_FSS(FeatStruct(features), update_feats)
            else:
                # Use explicit FS updates
                features = self.update_FS(FeatStruct(features), update_feats)
#        print("*** features {}".format(features.__repr__()))
        if not features:
            return []
        fst = fst or self.get_fst(generate=True, guess=guess, simplified=False,
                                  phon=phon, segment=segment)
#        print("*** fst {}".format(fst))
        if from_dict:
            # Features is a dictionary; it may contain the root if it's not specified
            anal = self.dict_to_anal(root, features)
            root = anal[0]
            features = anal[1]
        elif fss:
#            print("gen: FSS {}".format(fss.__repr__()))
            features = fss
        else:
            features = FSSet.cast(features)
#        print("GENERATING {}, features {}, fst {}".format(root, features.__repr__(),
#                                                          fst.__repr__()))
        if ortho and self.ortho2phon:
            # Have some way to check whether the root is already phonetic
            # There might be spaces in the orthographic form
            oroot = root.replace(' ', Morphology.mwe_sep)
            oroot = self.ortho2phon.get(oroot)
            if oroot:
                root = oroot
        if fst:

#            print('** Transducing with features {}'.format(features.__repr__()))
            gens = \
              fst.transduce(root, features,
                            seg_units=self.morphology.seg_units, gen=not del_feats,
                            print_word=print_word, print_prefixes=print_prefixes, trace=trace,
                            dup_output=del_feats,
                            timeit=timeit, timeout=timeout,
                            result_limit=limit, verbosity=verbosity)
#            print("gens {}".format(gens))
            if sort and len(gens) > 1:
                gens = self.score_gen_output(root, gens)
                gens.sort(key=lambda g: g[-1], reverse=True)
            if postproc:
                # For languages with non-roman orthographies
                for gen in gens:
                    # Replace the wordforms with postprocessed versions
                    gen[0] = self.finalize_output(gen[0], phon=phon, ortho_only=ortho_only)
            return gens
        elif trace:
            print('No generation FST loaded')

    def genfeats(self, root, feats=None):
        '''
        Shortcut for generating word with update features.
        '''
        return self.gen(root, update_feats=feats)

    @staticmethod
    def gen_output_feats(outputs, features):
        """
        Given a list of outputs (word, FeatStruct), return a list
        of words and the values of the features in the FeatStructs.
        """
#        print("GEN OUTPUT FEATS {}".format(outputs))
        result = []
        for output in outputs:
            word = output[0]
            fs = output[1]
            values = []
            for feature in features:
                value = fs.get(feature)
                if value:
                    values.append(value)
            if values:
                result.append((word, values))
        return result

    def translate(self, word, guess=False, phon=False, init_weight=None, tl='',
                  trace=0, tracefeat='', timeit=False, result_limit=0):
        """
        Using translation FST, translate word in source language
        to word in target language.
        """
        fst = self.get_fst(generate=False, guess=guess, phon=phon,
                           translate=True, segment=False, tl=tl)
#        print("*** trans fst: {}".format(fst))
#        if guess:
#            if phon:
#                fst = self.fsts[self.trans_i][self.guessphon_i]
#            else:
#                fst = self.fsts[self.trans_i][self.guess_i]
#        elif phon:
#            fst = self.fsts[self.trans_i][self.phon_i]
#        else:
#            fst = self.fsts[self.trans_i][0] or self.fsts[self.trans_i][self.guess_i] or self.fsts[self.trans_i][self.simp_i]
        if fst:
#            if preproc:
#                # For languages with non-roman orthographies
#                form = self.language.preprocess(form)
            if init_weight and not isinstance(init_weight, FSSet):
                init_weight = FSSet(init_weight)
            result_limit = result_limit or 20
            # If result is same as form and guess is True, reject
            anals = fst.transduce(word, seg_units=self.morphology.seg_units, reject_same=guess,
                                  init_weight=init_weight, result_limit=result_limit,
                                  trace=trace, tracefeat=tracefeat, timeit=timeit)
            return anals
        elif trace:
            print('No translation FST loaded for', self.pos)

    def finalize_output(self, word, phon=False, ipa=False,
                        ortho_only=False):
        """
        Finalize generation output: orthographic(|phonetic).
        """
        orthophon = self.language.postprocess(word, phon=phon, ipa=ipa,
                                              ortho_only=ortho_only)
        # word is presumably in phonetic representation; convert
        # it to conventional representation
#        if '|' in orthophon:
#            ortho, phon = orthophon.split('|')
#            phon = self.language.convert_phones(word, epenthesis=phon,
#                                                ipa=ipa)
#            return ortho + "|" + phon
        return orthophon

    # Feature conversion/normalization
    def featconv(self, fs):
        '''
        Convert the FeatStruct or FSSet fs to a normalized form based on
        the old subFS, new subFS pairs in subFSs.
        Unfreeze fs if its frozen, and return the new or updated
        FeatStruct.
        '''
        subFSs = self.featnorm
        if subFSs:
            return fs.featconv(subFSs)
        return fs

#    def segment(self, word, seg, feature, value, new_value=None):
#        """
#        If feature has value in word, segment the word into seg
#        and the word with feature changed to new_value.
#        """
#        anals = self.anal(word)
#        segmentations = []
#        for root, anal in anals:
#            # anal is a FSSet; check each FS
#            for a in anal:
#                if a.get(feature) != value:
#                    return
#            # only work with the first FS
#            a = list(anal)[0]
#            a = a.unfreeze()
#            a[feature] = new_value
#            new_word = self.gen(root, features=a)
#            if new_word:
#                segmentations.append((new_word[0][0], seg))
#        return segmentations

    def anals_to_dicts(self, analyses):
        '''Convert list of analyses to list of dicts.'''
        dicts = []
        for anal in analyses:
            root = anal[0]
            for fs in anal[1]:
                dicts.append(self.anal_to_dict(root, fs))
        return dicts

    def anal_to_gram(self, anal, gen_root=None):
        """Convert an analysis into a list of lists of morphs and grams."""
        gram = []
        for a in anal:
            # A single root, possibly multiple fss
            root = gen_root or a[0]
            # FeatStruct set
            for fs in a[1]:
                gram.append((self.fs_to_morphs(root, fs),
                             self.fs_to_feats(root, fs),
                             a[0]))
        return gram

    def postproc(self, analysis):
        '''Postprocess analysis (mutating it) according postproc attribute in Morphology.'''
        if self.postprocess:
            return self.postprocess(analysis)
        else:
            return analysis

    def update_FSS(self, fs1, fss2):
        """
        fs1: a FeatStruct, usually the defaultFS for a POS.
        fss2: a *list* of unfrozen FeatStructs or a FSSet
         or a list of FeatStruct strings.
        returns the result of adding features in fs1 to each
        FS in fss2, cast to a FSSet.
        """
#        print('update FSS')
        if isinstance(fss2, FSSet):
            fss2 = fss2.unfreeze()
        fss2upd = set()
        for fs in fss2:
            if isinstance(fs, str):
                fs = FeatStruct(fs)
            if fs.frozen():
                fs = fs.unfreeze()
#            print(" fss2 {}".format(fs.__repr__()))
            # an FS in the FSSet
            for key, value in fs1.items():
                value2 = fs.get(key)
                if not value2:
                    fs[key] = value
                elif isinstance(value, FeatStruct):
                    # dive down another level
                    if value2.frozen():
                        value2 = value2.unfreeze()
                    for subkey, subvalue in value.items():
                        if subkey not in value2:
                            value2[subkey] = subvalue
                        # otherwise keep the original value
            fs.freeze()
#            print(" fss2a after {}".format(fs.__repr__()))
            fss2upd.add(fs)
        fss2 = FSSet(fss2upd)
#        print("fss2 {}".format(fss2.__repr__()))
        return fss2

    def update_FS(self, fs, features, top=True):
        """Add or modify features (a FS or string) in fs."""
        fs = fs.copy()
        # First make sure features is a FeatStruct
        if isinstance(features, str):
            if features[0] != '[':
                # Add [] if not there
                features = '[' + features + ']'
            features = FeatStruct(features)
        for key, value in features.items():
            # Make True any features that are implied by key
            implications = self.FS_implic.get(key, [])
            # All of the implications associated with key
            for implic in implications:
                # Implications that are not represented as lists just mean
                # to make that feature True
                # (Make sure the feature doesn't have an explicit value)
                if not isinstance(implic, list) and not isinstance(implic, tuple) \
                        and implic not in features:
                    fs.update({implic: True})
            # Complex feature in features
            if isinstance(value, FeatStruct):
                # Recursively update value with value in fs for key
                if key not in fs:
                    return []
                value = self.update_FS(fs.get(key), value, top=False)
                # And make True any features that must be True in value
                for implic in implications:
                    if isinstance(implic, list):
                        for imp in implic:
                            # Should we make sure the feature doesn't have an explicit value?
#                            if imp not in value:
                            value.update({imp: True})
            fs.update({key: value})
        # Finally check all of the key, value pairs in self.FS_implic for
        # which the key is a tuple: (feat, value)
        if top:
            for key, implics in self.FS_implic.items():
                if isinstance(key, tuple):
                    # See whether this tuple represents the value of a feature
                    # in features
                    key_values = key[1]
                    # Could be a string or a list of strings; make sure it's a list
                    if not isinstance(key_values, tuple):
                        key_values = (key_values,)
                    if features.get(key[0], 'missing') in key_values:
                        # If so, apply the constraints, as long as they're not
                        # overridden by an explicit value in features
                        for f, v in implics:
                            # If v is a list, then make the value of the listed
                            # item in the list in fs[f] True
                            if isinstance(v, list):
                                if f in features and v[0] in features[f]:
                                    continue
                                fs[f][v[0]] = True
                            # If v is is tuple, then make the value of the item
                            # in the tuple False
                            elif isinstance(v, tuple):
                                if f in features and v[0] in features[f]:
                                    continue
                                fs[f][v[0]] = False
                            elif f not in features:
                                # Otherwise treat f as feature, v as value in fs
                                fs[f] = v
#        print('FS', fs.__repr__())
        return fs

    def delete_from_FS(self, featpaths, fs=None, freeze=False):
        """
        Return a copy of the FeatStruct (by default this POS's defaultFS)
        with value for feature removed.
        featlists is a list of feature path lists, one for each feature
        to be deleted.
        """
        fs = fs or self.defaultFS
        if isinstance(fs, str):
            fs = FeatStruct(fs)
        return fs.delete(featpaths, freeze=freeze)

    def o2p(self, form, guess=False):
        """Convert orthographic input to phonetic form.
        If rank is True, rank the analyses by the frequency of their roots."""
        output = {}
        analyzed = self.analyzed_phon[Morphology.complex].get(form, None)
        if analyzed:
            word, root, anals = analyzed
            output[word] = [(0, (self.pos, root, None, anal)) for anal in anals]
            return output
        gen_fst = self.get_fst(generate=True, guess=guess, phon=True)
        if not gen_fst:
            return
        analyses = self.anal(form, guess=guess)
#        print("Analyses {}".format(analyses))
        root_count = 0
        if analyses:
#            print("Analyses: {}".format(analyses))
            for root, anals in analyses:
                for anal in anals:
                    # The freq score is the count for the root-feature combination
                    # times the product of the relative frequencies of the grammatical features
                    root_count = self.morphology.get_root_freq(root, anal)
                    freq_count = self.morphology.get_feat_freq(anal)
                    root_count *= freq_count
                    out = self.gen(root, features=anal, phon=True, fst=gen_fst)
                    for o in out:
                        word = o[0]
                        word = self.language.convert_phones(word)
                        output[word] = output.get(word, []) + [(round(root_count), self.pos, root, None, anal)]
        return output

    ## Generating default FS from feature-value pairs in Morphology

    def make_default_fs(self):
        dct = {}
        lex_feats = self.lex_feats
        for feat, values in self.feat_list:
#            print('*** feat {}, values {}'.format(feat, values))
            if feat in lex_feats:
                continue
            if isinstance(values, list):
                dct2 = {}
                # feat is a complex feature; values is a list of feat-values tuples
                for feat2, values2 in values:
                    if feat2 in lex_feats:
                        continue
                    dct2[feat2] = values2[0]
                fs2 = FeatStruct(dct2)
                dct[feat] = fs2
            else:
                dct[feat] = values[0]
#        print("** dct {}".format(dct))
        fs = FeatStruct(dct)
        return fs

    ## Pretty printing and web dictionary analysis

    def pretty_anal(self, anal, webdict=None, root=None, fs=None):
        root = root or anal[1]
        fs = fs or anal[3]
#        print("pretty anal {}, {}".format(root, fs.__repr__()))
        # Leave out the part of speech for now
        root = self.language.postproc_root(self, root, fs, phonetic=False)
        s = self.language.T.tformat('{} = {}, {} = {}\n',
                                    ['POS', self.name, 'root', root],
                                    self.language.tlanguages)
        if webdict != None:
            webdict['POS'] = self.name
            if 'pos' not in anal and self.pos != 'all':
                # we don't want "pos: all" for Qu, for example
                webdict['pos'] = self.pos
            webdict['root'] = root
            # Citation form...
        s += self.pretty_fs(fs, webdict=webdict)
        return s

    def print_anal(self, anal, file=sys.stdout):
        '''Print out an analysis.'''
        s = self.pretty_anal(anal)
        print(s, file=file)

    def pretty_fs(self, fs, printit=False, file=sys.stdout, webdict=None):
        '''Print out an FS and/or store pretty values in webdict.'''
        s = ''
        expansions, feats_used = self.expfv(fs, webdict=webdict)
        for exp in expansions:
            s += '  {}\n'.format(exp)
        if feats_used is not True:
            for feat, val in fs.items():
                if feat == 'pos':
                    continue
                if self.excl(feat, val, feats_used):
                    continue
                if isinstance(val, FeatStruct):
                    webvals = []
                    abbrevs2, feats_used2 = self.expfv(val, top=feat, webdict=webdict)
                    fvstring = abbrevs2
                    if feats_used2 is not True:
                        for feat2, val2 in val.items():
                            if self.excl(feat2, val2, feats_used2):
                                continue
                            fvstring.append(self.fval_string(feat2, val2, webdict=None))
                            if webdict != None:
                                if val2 is True:
                                    webvals.append(self.exab(feat2))
                                elif val2 is not False:
                                    webvals.append("{}={}".format(self.exab(feat2), self.exab(val2)))
                    if fvstring:
                        fvstring = ', '.join(fvstring)
                        s += '  {} = {}\n'.format(self.exab(feat), fvstring)
                        if webdict != None and webvals:
                            webdict[self.exab(feat)] = webvals
                else:
                    if webdict != None:
                        webdict[self.exab(feat)] = val
                    s += '  {}\n'.format(self.fval_string(feat, val, webdict=webdict))
        if printit:
            print(s, file=file)
        return s

    def expfv(self, fs, top=None, webdict=None):
        '''Find feature value sets that have special names (expansions).'''
        expansions = []
        feats_used = []
        for fvs in self.fv_priority:
            match = True
            for f, v in fvs:
                if f not in fs or fs[f] != v:
                    match = False
                    break
            if match:
                # Found a fv combination with priority; look up its expansion
                # in fv_abbrevs
                expansion = some(lambda x: x[1] if x[0] == fvs else False, self.fv_abbrevs)
                if webdict != None:
                    webdict[self.exab(fvs[0][0])] = expansion
                return [expansion], True
        for fvs, exp in self.fv_abbrevs:
            match = True
            if all([(fv[0] in feats_used) for fv in fvs]):
                continue
            for f, v in fvs:
                if f not in fs or fs[f] != v:
                    match = False
                    break
            if match:
                if exp:
                    # The expansion may be empty
                    # Use the top feature if there is one, otherwise first of features in fvs
                    if not top:
                        if webdict != None:
                            webdict[self.exab(fvs[0][0])] = exp
                        exp = "{} = {}".format(fvs[0][0], exp)
                    elif webdict != None:
                        if top in webdict:
                            webdict[self.exab(top)] += ", " + exp
                        else:
                            webdict[self.exab(top)] = exp
                    expansions.append(exp)
                feats_used.extend([fv[0] for fv in fvs])
#        if expansions:
#            print("top {}, fs {}, expansions {}, feats_used {}".format(top, fs.__repr__(), expansions, feats_used))
        # Check feature groups
        if not top and self.feature_groups:
            groupnames = []
            for feats, properties in self.feature_groups:
#                if any([(feat in feats_used) for feat in feats]):
#                    continue
                for groupvalues, groupname, groupvalue, groupoper in properties:
                    found = True
                    for feat, value in zip(feats, groupvalues):
                        if ":" in feat:
#                            print("feats {}, properties {}, feat {}, value {}, oper {}".format(feats, properties, feat, value, groupoper))
#                            print("fs: {}".format(fs.__repr__()))
                            feat1, feat2 = feat.split(':')
                            if feat1 not in fs or not fs[feat1] or feat2 not in fs[feat1] or fs[feat1][feat2] != value:
                                found = False
                                break
                            else:
                                feats_used.append(feat1)
                        elif feat not in fs or fs[feat] != value:
                            found = False
                            break
                        else:
                            feats_used.append(feat)
                    if found:
                        if not groupname:
                            expansions.append("{}".format(groupvalue))
                        elif groupname in groupnames and groupoper:
                            # If this groupname already has a value and we're setting the value rather than
                            # appending it, stop here.
                            continue
                        else:
                            groupnames.append(groupname)
                            expansions.append("{} = {}".format(groupname, groupvalue))
                        if webdict != None:
                            if not groupoper:
#                                print("Adding {} to {}".format(groupvalue, groupname))
                                # Add the groupvalue to groupname's values
                                if groupname not in webdict:
                                    webdict[groupname] = [groupvalue]
                                else:
                                    v = webdict[groupname]
                                    if not isinstance(v, list):
                                        v = [v]
                                    v.append(groupvalue)
                                    webdict[groupname] = v
                            elif groupname:
                                # Set the value for groupname
                                webdict[groupname] = groupvalue

        return expansions, feats_used

    def excl(self, feat, val, feats_used):
        """Exclude the feature value pair from the printed output."""
        if feat in feats_used:
            return True
        if val == None or val == 0:
            return True
        if feat in self.excl_feats:
            return True
        if (feat, val) in self.excl_feats:
            return True
        return False

    def exab(self, string):
        """Just a short form for expand_abbrev."""
        return self.feat_abbrevs.get(string, string)

    def fval_string(self, feat, val, webdict=None, top=True):
        if webdict != None:
            webdict[self.exab(feat)] = self.exab(val)
        if isinstance(val, bool):
            return '{}{}'.format('+' if val else '-', self.exab(feat))
        else:
            return '{} = {}'.format(self.exab(feat), self.exab(val))

    def make_fv_lists(self):
        """Make lists of features and possible values
        and another corresponding dictionary with names for features and values.
        """
        fvs = []
        fv_names = []
        for feat, values in self.feat_list:
            if feat in self.excl_feats or feat in self.lex_feats:
                continue
            fvs.append((feat, values))
            if isinstance(values, list):
                # Nesting
                value_names = []
                for val in values:
                    value_names.append((self.exab(val[0]), [self.exab(v) for v in val[1]]))
            else:
                value_names = [self.exab(value) for value in values]
            fv_names.append((self.exab(feat), value_names))
        return fvs, fv_names

    def fv_menu(self, fs=None):
        """Display a menu for the user to make changes to FeatStruct fs."""
        # Start with a copy of the default if no FS is specified
        fs = fs or self.defaultFS.copy()
        fvs, fv_names = self.make_fv_lists()
        dmenu = DMenu(fvs, fv_names, self.fv_dependencies)
        changed_fvs = dmenu.top(fs,
                                tdict=self.language.T,
                                langs=self.language.tlanguages,
                                pretty=self.pretty_fs)
        for cfv in changed_fvs:
            dep = self.fv_dependencies.get(cfv)
            if dep:
                feat_path = tuple(dep[:-1])
                feat_value = dep[-1]
                if not fs.__getitem__(feat_path) == feat_value:
                    print('Changing dependent feature', feat_path, 'to value', feat_value)
                    fs.__setitem__(tuple(dep[:-1]), dep[-1])
        return fs

    def score_gen_output(self, root, output):
        """
        Given multiple outputs from gen(), score them on the features that
        distinguish them.
        """
        forms = [o[0] for o in output]
        feats = [o[1] for o in output]
        diffs = FSSet.compareFSS(feats)
        root_scores = [0.0] * len(forms)
        feat_scores = [0.0] * len(forms)
#        print("Scoring {}".format(output))
#        print(" diffs {}".format(diffs.__repr__()))
        # root-feature frequencies
        if self.root_freqs and root in self.root_freqs:
            root_freqs = self.root_freqs[root]
            for feat, values in diffs.items():
                if feat in root_freqs:
                    root_feat_freqs = root_freqs[feat]
                    root_feat_values = [root_feat_freqs.get(value, 0.0) for value in values]
                    root_scores = [(x + y) for x, y in zip(root_scores, root_feat_values)]
        # total feature frequencies
        if self.feat_freqs:
            for feat, values in diffs.items():
                if feat in self.feat_freqs:
                    feat_freqs = self.feat_freqs[feat]
                    feat_values = [feat_freqs.get(value, 0.0) for value in values]
                    feat_scores = [(x + y) for x, y in zip(feat_scores, feat_values)]
        # scale the feat_scores by the proportion of the total root_scores to the feat_scores
        rootsum = sum(root_scores)
        featsum = sum(feat_scores)
        if featsum:
            if rootsum:
                scaling = rootsum/featsum
                scores = [(r + f * scaling) for r, f in zip(root_scores, feat_scores)]
            else:
                scores = feat_scores
        else:
            scores = root_scores
#        print("scores {}".format(scores))
        # return the outputs with scores appended
        return [o + [s] for o, s in zip(output, scores)]

    ### New methods to process output of anal(), hopefully replacing the methods in Language.


class MorphCat(list):
    """A list of morphs, default first."""

    def __init__(self, label, *morphs):
        list.__init__(self, morphs)
        self.label = label
        self.default = morphs[0] if morphs else '0'

class GramCat(list):
    """A list of grams."""

    def __init__(self, label, *grams):
        list.__init__(self, grams)
        self.label = label
