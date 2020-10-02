"""
This file is part of HornMorpho, which is part of the PLoGS project.

    <http://homes.soic.indiana.edu/gasser/plogs.html>

    Copyleft 2020.
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

Functions common to some or all Ethio-Eritrean Semitic languages.
"""

from . import language
from .geez import *
from .utils import segment, allcombs
from .rule import *

class EES:

    # later extend to include preps and conjs from other languages
    ROM2GEEZ = {'sI': "ስ", 'lI': "ል", 'bI': "ብ", 'IskI': "እስክ", 'IndI': "እንድ",
                'm': "ም", 'Inji': "እንጂ", 'na': "ና", 'sa': "ሳ", 's': "ስ", 'ma': "ማ",
                'sIle': "ስለ", 'le': "ለ", 'Iyye': "እየ", 'Iske': "እስከ", 'Inde': "እንደ", 'ke': "ከ", 'be': "በ", 'wede': "ወደ"}

    def __init__(self, language):
        # language is a Language instance
        self.language = language

    def vb_get_citation(self, root, fs,
                        guess=False, vc_as=False):
        '''Return the canonical (prf, 3sm) form for the root and featstructs in
        featstruct fs.
        If at is True, use Amharic/Tigrinya features.
        If vc_as is True, preserve the voice and aspect of the original word.
        '''
        citation = ''
        if root == 'hlw':
            return "አለ"
        # Return root if no citation is found
        result = root
        # Unfreeze the feature structure
        fs = fs.unfreeze()
        fsa, fsv = fs.get('as'), fs.get('vc')
        # Update the feature structure to incorporate default (with or without vc and as)
        fs.update(self.language.morphology['v'].defaultFS)
        # For non-passive te- verbs, te- is citation form
        if fs.get('lexav') == True:
            # Lexical entry with explicit as, vc features
            fs.update({'as': fsa, "vc": fsv})
        elif fs.get('lexip') == True:
            # Lexical entry for as=it,vc=ps and as=it,vc=tr
            fs.update({'as': 'it', 'vc': 'ps'})
        elif fs.get('lexrp') == True:
            # Lexical entry for as=rc, vc=ps and as=rc,vc=tr
            fs.update({'as': 'rc', 'vc': 'ps'})
        elif fs.get('smp') == False:
            # No vc=smp form, vc=ps is base/citation form
            fs.update({'vc': 'ps'})
        # Refreeze the feature structure
        fs.freeze()
        # Find the first citation form compatible with the updated feature structure
        if ' ' in root:
            # This is a light verb, just generate the actual verb
            root_split = root.split()
            citation = self.language.morphology['v'].gen(root_split[-1], fs, from_dict=False,
                                               phon=True, postproc=False, guess=guess)
            if citation:
                result = ' '.join(root_split[:-1]) + ' ' + citation[0][0]
        else:
    #        print("Generating citation from {}".format(fs.__repr__()))
            citation = self.language.morphology['v'].gen(root, fs, from_dict=False,
                                               phon=True, postproc=False, guess=guess)
            if citation:
                result = citation[0][0]
        if not citation:
            if not vc_as:
                # Verb may not occur in simplex form; try passive
                fs = fs.unfreeze()
                fs.update({'vc': 'ps'})
                fs.freeze()
                citation = self.language.morphology['v'].gen(root, fs, from_dict=False, guess=guess)
                if citation:
                    result = citation[0][0]
        return result

    def n_get_citation(self, root, fs, guess=False, vc_as=False):
        '''Return the canonical (prf, 3sm) form for the root and featstructs in featstruct set fss.

        If vc_as is True, preserve the voice and aspect of the original word.
        '''
        if fs.get('v'):
            # It's a deverbal noun
            return vb_get_citation(root, fs, guess=guess, vc_as=vc_as)
        else:
            return None

    def simplify(self, word):
        """Simplify Amharic orthography."""
        word = word.replace("`", "'").replace('H', 'h').replace('^', '').replace('_', '')
        return word

    def orthographize(self, word):
        '''Convert phonological romanization to orthographic.'''
        word = word.replace('_', '').replace('I', '')
        return word

    def webfv(self, webdict, feature, value):
        if webdict != None:
            webdict[feature] = value

    def preproc_root(self, root, fs, pos):
        """
        Preprocess root for generation.
        """
        if is_geez(root):
            anal = self.language.morphology['v'].anal(root, preproc=True)
            if anal:
                root, ffss = anal[0]
                cls = ffss.get('cls')
                root, fs = language.Language.dflt_procroot("{}:{}".format(root, cls), fs)
            else:
    #            print("Couldn't analyze {}".format(root))
                return root, fs
        else:
            root, fs = language.Language.dflt_procroot(root, fs)
        return root, fs

    def postpostproc_root(self, root, fs):
        """
        Convert root to root:class format, also changing internal
        HM root representation to an alternate conventional
        representation.
        """
        return "<{}:{}>".format(self.language.convert_root(root), fs['cls'])

    def postproc_nroot(self, root, fs):
        """
        Convert citation (lemma) to conventional phonetic representation.
        """
        if fs.get('pos') == 'n_dv':
            return "<{}:{}>".format(self.language.convert_root(root), fs['cls'])
        else:
            return "{}|{}".format(geezify(root), self.language.convert_phones(root))

    def postproc_word(self, word, ipa=False):
        """
        Convert output word to ortho|phon representation, also
        changing internal HM representation to an alternate
        conventional representation.
        """
        return "{}|{}".format(geezify(word), self.language.convert_phones(word))

    def load_anal(self, pos='v', lex=True, guess=False):
        if lex:
            self.language.morphology[pos].load_fst(True, verbose=True)
        if guess:
            self.language.morphology[pos].load_fst(True, guess=True, verbose=True)

    def load_gen(self, pos='v', lex=True, guess=False):
        if lex:
            self.language.morphology[pos].load_fst(True, generate=True, invert=True, verbose=True)
        if guess:
            self.language.morphology[pos].load_fst(True, generate=True, invert=True, guess=True, verbose=True)

    @staticmethod
    def postproc_root(root):
        """Final adjustments to romanized root."""
        # Replace __ with space.
        if '//' in root:
            root = root.replace('//', ' ')
        return root

    @staticmethod
    def roman2geez(value):
        """Convert a value (prep or conj) to geez."""
        return EES.ROM2GEEZ.get(value, value)

    def seg2string(self, segmentation, sep='-', geez=True, features=False,
                   arules=False):
        """Convert a segmentation to a string, including features if features is True."""
        # The segmentation string is second in the list
    #    print("Converting {} to string".format(segmentation))
        morphs, rootindex = self.language.seg2morphs(segmentation[1])
        # Root string and features
        root, rootfeats = morphs[rootindex]
        # Separate the consonants and template, and realize the root
        root = root2string(root)
        # Replace the root in the morphemes list
        morphs[rootindex] = root, rootfeats
        if geez:
            # First make sure separate morphemes are geez
            morphs2 = [[(g, f) for g in geezify_morph(m, alt=True)] for m, f in morphs]
        else:
            morphs2 = []
            for m, f in morphs:
                conv = convert_labial(m)
                morphs2.append([(c, f) for c in conv])
        morphs = allcombs(morphs2)
    #    print(" Morphs {}".format(morphs))
        if not features:
            morphs = [[w[0] for w in word] for word in morphs]
        else:
            # Rejoin morpheme and features for each word
            morphs = [[''.join(m) for m in word] for word in morphs]
        return [sep.join(m) for m in morphs]

    def root2string(self, root):
        """If root contains '+', it consists of a root and a template, which need to be
        integrated."""
        if '+' in root:
            cons, temp = root.split('+')
            cons = segment(cons, self.language.seg_units)
            cons = [c for c in cons if c not in ['a', '_']]
    #        print("root cons: {}, temp {}".format(cons, temp))
            if 'tt' in temp:
                temp = temp.replace('tt', 't_')
            temp = [(int(t) if t.isdigit() else t) for t in temp]
            form = []
            last_cons = ''
            for index, t in enumerate(temp):
                if isinstance(t, int):
                    # Template positions are 1-based, not 0-based
                    c = cons[t-1]
                    if c != last_cons:
                        form.append(cons[t-1])
                    else:
                        # Identical consonants; geminate
                        form.append('_')
                    last_cons = c
                elif index == 0 and t in "aeiouIE":
                    form.append("'" + t)
                elif t in "stm":
                    form.append(t)
                    last_cons = t
                else:
                    form.append(t)
                    # A vowel or _ character was added so clear the last consonant
                    last_cons = ''
            return '{' + ''.join(form) + '}'
        else:
            return '{' + root + '}'

# ## Create Language object for Amharic, including preprocessing, postprocessing,
# ## and segmentation units (phones).
# AMH = language.Language("አማርኛ", 'amh',
#               postproc=postproc_word,
#               preproc=lambda form: geez2sera(None, form, lang='am', simp=True),
#               procroot=preproc_root,
#               postpostproc=lambda form: postproc_root(form),
#               seg2string=lambda string, sep='-', features=False, transortho=True: seg2string(string, sep=sep, geez=transortho, features=features),
#               stat_root_feats=['vc', 'as'],
#               stat_feats=[['poss', 'expl'], ['cnj'], ['cj1'], ['cj2'], ['pp'], ['rel']],
#               # We need + and numerals for segmentation of irregular verbal nouns
#               seg_units=[["a", "e", "E", "i", "I", "o", "u", "H", "w", "y",
#                           "'", "`", "_", "|", "*", "/", "+", "2", "3"],
#                          {"1": ["1", "1W"], "b": ["b", "bW"], "c": ["c", "cW"], "C": ["C", "CW"],
#                           "d": ["d", "dW"], "f": ["f", "fW"], "g": ["g", "gW"],
#                           "h": ["h", "hW"], "j": ["j", "jW"], "k": ["k", "kW"],
#                           "l": ["l", "lW"], "m": ["m", "mW"], "n": ["n", "nW"],
#                           "p": ["p", "pW"], "P": ["P", "PW"],
#                           "N": ["N", "NW"], "q": ["q", "qW"], "r": ["r", "rW"],
#                           "s": ["s", "sW"], "S": ["S", "SW"], "t": ["t", "tW"],
#                           "T": ["T", "TW"], "v": ["v", "vW"], "x": ["x", "xW"],
#                           "z": ["z", "zW"], "Z": ["Z", "ZW"],
#                           "^": ["^s", "^S", "^h", "^hW", "^sW", "^SW"]}])
#
# ## Create Morphology object and noun, verb, and copula POSMorphology objects for Amharic,
# ## including punctuation and ASCII characters that are part of the romanization.
# AMH.set_morphology(language.Morphology(
#                              pos_morphs=[('cop',), ('n',), ('v',)],
#                              # Exclude ^ and - (because it can be used in compounds)
#                              punctuation=r'[“‘”’–—:;/,<>?.!%$()[\]{}|#@&*\_+=\"፡።፣፤፥፦፧፨]',
#                              # Include digits?
#                              characters=r'[a-zA-Zሀ-ፚ\'`^]'))
#
# ### Assign various attributes to Morphology and POSMorphology objects
#
# # Functions that simplifies Amharic orthography
# AMH.morphology.simplify = lambda word: simplify(word)
# AMH.morphology.orthographize = lambda word: orthographize(word)
#
# # Function that performs trivial analysis on forms that don't require romanization
# AMH.morphology.triv_anal = lambda form: no_convert(form)
#
# ## Functions converting between feature structures and simple dicts
# AMH.morphology['v'].anal_to_dict = lambda root, anal: vb_anal_to_dict(root, anal)
# AMH.morphology['v'].dict_to_anal = lambda root, anal: vb_dict_to_anal(root, anal)
# AMH.morphology['v'].name = 'verb'
#
# ## Default feature structures for POSMorphology objects
# ## Used in generation and production of citation form
# AMH.morphology['v'].defaultFS = \
#     language.FeatStruct("[pos=v,tm=prf,as=smp,vc=smp,sb=[-p1,-p2,-plr,-fem],ob=[-expl,-p1,-p2,-plr,-b,-l,-prp,-frm,-fem],cj1=None,cj2=None,pp=None,-neg,-rel,-sub,-acc,-ye]")
# AMH.morphology['v'].FS_implic = {'rel': ['sub'],
#                                 'cj1': ['sub'],
#                                 'pp': ['rel', 'sub'],
#                                 ('pp', ('be', 'le', 'ke', 'wede', 'Inde', 'sIle', 'Iske', 'Iyye')): [['rl', ['p']]],
# #                                'def': ['rel', 'sub'],
#                                 'l': ['prp'],
#                                 'b': ['prp']
# #                                'ob': [['expl']]
#                                 }
# # defaultFS with voice and aspect unspecified
# AMH.morphology['v'].citationFS = language.FeatStruct("[pos=v,tm=prf,sb=[-p1,-p2,-plr,-fem],ob=[-expl],cj1=None,cj2=None,pp=None,-neg,-rel,-sub,-ye,-acc]")
# AMH.morphology['v'].explicit_feats = ["sb", "ob", "tm", "neg", "rel", "def", "cj1", "cj2", "pp"]
# AMH.morphology['v'].feat_list = \
#   [('cj1', ('sI', 'IskI', 'bI', 'lI', 'IndI')),
#    ('vc', ('ps', 'cs', 'tr', 'smp')),
#   ('ye', (False, True)),
#   ('v', ('man', 'inf', 'agt', 'ins', None)),
#   ('pp', ('wede', 'Iske', 'ke', 'be', 'le', 'Iyye', 'sIle', 'Inde')),
#   ('pos', ('n', 'v')),
#   ('def', (False, True)),
#   ('ax', ('al')),
#   ('as', ('it', 'rc', 'smp')),
#   ('cj2', ('s', 'm', 'Inji')),
#   ('acc', (False, True)),
#   ('tm', ('ger', 'j_i', 'imf', 'prf', 'prs')),
#   ('rel', (False, True)),
#   ('ob', [('b', (False, True)), ('plr', (False, True)), ('prp', (False, True)), ('p1', (False, True)), ('frm', (False, True)),
#           ('l', (False, True)), ('expl', (False, True)), ('p2', (False, True)), ('fem', (False, True))]),
#   ('sub', (False, True)),
#   ('neg', (False, True)),
#   ('sb', [('p1', (False, True)), ('frm', (False, True)), ('plr', (False, True)), ('fem', (False, True)), ('p2', (False, True))])]
# AMH.morphology['v'].feat_abbrevs = \
#   {'cj1': "conj prefix", 'cj2': "conj suffix", "vc": "voice",
#    "sb": "subject", "ob": "object", "tm": "TAMH", "neg": "negative", "rel": "relative", "def": "definite",
#    "pp": "preposition"}
# AMH.morphology['v'].fv_abbrevs = \
#   (([['p1', True], ['p2', False], ['plr', False]], "1 prs sng"),
#    ([['p1', True], ['p2', False], ['plr', True]], "1 prs plr"),
#    ([['p1', False], ['p2', True], ['plr', False], ['fem', False]], "2 prs sng mas"),
#    ([['p1', False], ['p2', True], ['plr', False], ['fem', True]], "2 prs sng fem"),
#    ([['p1', False], ['p2', True], ['plr', False], ['frm', True]], "2 prs frml"),
#    ([['p1', False], ['p2', True], ['plr', True]], "2 prs plr"),
#    ([['p1', False], ['p2', False], ['plr', False]], "3 prs sng"),
#    ([['p1', False], ['p2', False], ['plr', False], ['frm', True]], "3 prs frml"),
#    ([['p1', False], ['p2', False], ['plr', True]], "3 prs plr")
#    )
# # Set this here rather than automatically with POSMorphology.set_web_feats() since all web features have a single value
# AMH.morphology['v'].web_feats = \
#   [('sb', 1), ('ob', 1), ('tm', 1), ('neg', 1), ('rel', 1), ('pp', 1), ('cj1', 1), ('cj2', 1), ('def', 1)]
# AMH.morphology['v'].root_proc = postpostproc_root
# AMH.morphology['n'].root_proc = postproc_nroot
# AMH.morphology['cop'].root_proc = lambda root, fs: "ነው"
#
# AMH.morphology['n'].name = 'noun'
# AMH.morphology['n'].defaultFS = \
#     language.FeatStruct("[-acc,-def,-neg,-fem,-itu,as=smp,cnj=None,-dis,-gen,-plr,poss=[-expl,-p1,-p2,-plr,-fem,-frm],pp=None,v=None,vc=smp]")
# AMH.morphology['n'].FS_implic = {'poss': [['expl'], 'def']}
# # defaultFS with voice and aspect unspecified
# AMH.morphology['n'].citationFS = language.FeatStruct("[-def,-acc,-neg,-fem,cnj=None,-dis,-gen,-plr,poss=[-expl],pp=None,v=inf]")
# AMH.morphology['n'].explicit_feats = ["plr", "poss", "def", "acc", "gen", "pp", "dis"]
# AMH.morphology['n'].feat_abbrevs = \
#   {'plr': "plural", 'poss': "possessor", "def": "definite", "acc": "accusative", "dis": "distributive", "gen": "genitive",
#    'pp': 'preposition'}
#
# AMH.morphology['cop'].name = 'copula'
# AMH.morphology['cop'].defaultFS = language.FeatStruct("[cj2=None,-neg,sb=[-fem,-p1,-p2,-plr,-frm],tm=prs]")
# AMH.morphology['cop'].citationFS = language.FeatStruct("[cj2=None,-neg,sb=[-fem,-p1,-p2,-plr,-frm],tm=prs]")
# AMH.morphology['cop'].explicit_feats = ["sb", "neg", "cj2"]
# AMH.morphology['cop'].feat_abbrevs = \
#   {'sb': "subject", 'cj2': "conj suffix", "neg": "negative"}
# AMH.morphology['cop'].fv_abbrevs = \
#   (([['p1', True], ['p2', False], ['plr', False]], "1 prs sng"),
#    ([['p1', True], ['p2', False], ['plr', True]], "1 prs plr"),
#    ([['p1', False], ['p2', True], ['plr', False], ['fem', False]], "2 prs sng mas"),
#    ([['p1', False], ['p2', True], ['plr', False], ['fem', True]], "2 prs sng fem"),
#    ([['p1', False], ['p2', True], ['plr', False], ['frm', True]], "2 prs frml"),
#    ([['p1', False], ['p2', True], ['plr', True]], "2 prs plr"),
#    ([['p1', False], ['p2', False], ['plr', False]], "3 prs sng"),
#    ([['p1', False], ['p2', False], ['plr', False], ['frm', True]], "3 prs frml"),
#    ([['p1', False], ['p2', False], ['plr', True]], "3 prs plr")
#    )
#
# ## Functions that return the citation forms for words
# AMH.morphology['v'].citation = lambda root, fss, guess, vc_as: vb_get_citation(root, fss, guess, vc_as)
# AMH.morphology['n'].citation = lambda root, fss, guess, vc_as: n_get_citation(root, fss, guess, vc_as)
# AMH.morphology['cop'].citation = lambda root, fss, guess, vc_as: 'new'
#
# ## Functions that convert analyses to strings
# AMH.morphology['v'].anal2string = lambda fss, webdict: vb_anal2string(fss, webdict=webdict)
# AMH.morphology['n'].anal2string = lambda fss, webdict: n_anal2string(fss, webdict=webdict)
# AMH.morphology['cop'].anal2string = lambda fss, webdict: cop_anal2string(fss, webdict=webdict)
#
# ## Postprocessing function for nouns (treats roots differently)
# # AMH.morphology['v'].postproc = lambda analysis: vb_postproc(analysis)
# # AMH.morphology['n'].postproc = lambda analysis: n_postproc(analysis)
# # AMH.morphology['cop'].postproc = lambda analysis: cop_postproc(analysis)
#
# # Interface language
# AMH.if_language = 'eng'
#
#
# VOWELS = '[aeEiIou@AOU]'
# CONS = "[hlHmrsxqbtcnN'kw`zZydjgTCPSfp]|^S|^s|^h"
#
# ### verb RE rules
# RULES = Rules(language = AMH)
#
# RULES.add(Del(delpart="'", pre="-{?", post=VOWELS))
# RULES.add(Del(delpart="0-"))
#
# ## CC
# RULES.add(Repl("[lmrsxbtnzdgTSf]", "}-", "h", "", "", "k"))
# RULES.add(SimpRepl("Tt", "t_"))
# RULES.add(SimpRepl("[kg]}-k", "k_"))
#
# ## VV
# # (a|e)(a|e) ## a => a
# RULES.add(Del(delpart="[ae]?[ae]-*{?}?-?", post="a"))
# # a ## e => a
# RULES.add(Del(pre="a", delpart="-*{?}?-?e"))
# # e ## e => e
# RULES.add(Del(delpart="e", post="}-e"))
# # a|e ## u => u
# RULES.add(Del(delpart="[ae]", post="}-u"))
# # a ## i => i
# RULES.add(Del(delpart="a", post="}-i"))
#
# ## palatalization, y, i
# RULES.add(Repl("[bsdlk]", "", "-y", "-{", CONS, "i"))
# RULES.add(Repl("[bsdlk]", "", "-y", "-{", VOWELS, "iy"))
# RULES.add(Assim({'t': 'c', 'd': 'j', 'T': 'C', 's': 'x', 'z': 'Z', 'n': 'N', 'l': 'y'},
#                 inter="_?}?-_?", post="[iE]", prog=True, replace=False))
# RULES.add(Repl("[cjCxZNy]", "_?}?-_?", "[iE]-?", "", VOWELS, ""))
# RULES.add(Insert(pre="[iE]-?{?}?-?", post=VOWELS, insertion="y"))
# RULES.add(Del(delpart="i", pre="[aeEiou]y}?-?"))
#
# ## labialization
# RULES.add(Repl(CONS, r"_?}?-?", "[ou]", "-", "[aeEIi]", "W"))
#
# ## cleanup
# RULES.add(Del(delpart="[-_{}I]"))
#
# AMH.morphology['v'].rules = RULES
#
# ### noun RE rules
#
# VNRULES = Rules(language=AMH)
#
# # palatalization, y, i in deverbal nouns
# VNRULES.add(Assim({'t': 'c', 'd': 'j', 'T': 'C', 's': 'x', 'z': 'Z', 'n': 'N', 'l': 'y'},
#                  inter="", post="i}", prog=True, replace=False))
# VNRULES.add(Assim({'t': 'c', 'd': 'j', 'T': 'C', 's': 'x', 'z': 'Z', 'n': 'N', 'l': 'y'},
#                  inter="", post="iya}", prog=True, replace=False))
# VNRULES.add(Repl("[cjCxZNy]", "", "iya", "", "}", "a"))
# VNRULES.add(Del(delpart="i", pre="[aeEiou]y", post="}"))
# #VNRULES.add(Del(delpart="i", pre="[cjCxZNy]", post="}-"+VOWELS))
#
# NRULES = Rules(language=AMH)
#
# # exceptions
# NRULES.add(Repl("e", "-{", "y", '', "h}", "z_i"))
# NRULES.add(Repl("e", "-{", "yc_i", '', "}", "z_ic"))
# NRULES.add(Insert(pre="e-{", post="ya}", insertion="z_i"))
# NRULES.add(Repl("e", "-{", "yac_i", '', "}", "z_iyac"))
#
# # glottal stop
# NRULES.add(Del(delpart="'", pre="-{?", post=VOWELS))
# # aa
# NRULES.add(Del(delpart="a", pre="a}-"))
# # optional: aoc => oc
# #NRULES.add(Del(delpart="a", post="}-oc"))
#
# # epenthesis
# NRULES.add(Insert(pre=VOWELS + "}?-", post="E", insertion="y"))
# NRULES.add(Insert(pre=VOWELS + "}?-", post="o", insertion="w"))
# NRULES.add(Insert(pre="[iE]}?-", post="a", insertion="y"))
# NRULES.add(Insert(pre="[ou]}?-", post="a", insertion="w"))
#
# # -u, -wa
# NRULES.add(Repl(VOWELS, "}-", "u", "", "", "w"))
# NRULES.add(Repl(CONS, "}?-", "w", "", "", "W"))
#
# # prefix VV
# NRULES.add(Del(delpart="e", post="-{?'?a"))
# NRULES.add(Del(delpart="'", pre="e-{", post=CONS))
#
# NRULES.add(Del(delpart="[-_{}]"))
#
# # ' between vowels
# NRULES.add(Insert(pre=VOWELS, post=VOWELS, insertion="'"))
#
# NRULES.add(Del(delpart="I"))
#
# VNRULES.add_rules(NRULES)
#
# AMH.add_rules('n', NRULES)
# AMH.add_rules('v', RULES)
# AMH.add_rules('n_dv', VNRULES)
