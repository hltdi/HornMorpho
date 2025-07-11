"""
This file is part of HornMorpho, which is part of the PLoGS project.

    <http://homes.soic.indiana.edu/gasser/plogs.html>

    Copyleft 2020-2025.
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

from .geez import *
from .utils import segment, allcombs
from .semiring import UNIFICATION_SR
from .fs import FeatStruct

SOURCE_WT_CONV = [("gem", "sgem"), ("c=", "sc="), ("v=", "sv="), ("t=", "st="), ("strong", "sstrong")]
TARGET_WT_CONV = [("gem", "tgem"), ("c=", "tc="), ("v=", "tv="), ("t=", "tt="), ("strong", "tstrong")]

class EES:

    # later extend to include preps and conjs from other languages
    ROM2GEEZ = \
    {'amh':
        {'sI': "ስ", 'lI': "ል", 'bI': "ብ", 'IskI': "እስክ", 'IndI': "እንድ",
         'm': "ም", 'Inji': "እንጂ", 'na': "ና", 'sa': "ሳ", 's': "ስ", 'ma': "ማ",
         'sIle': "ስለ", 'le': "ለ", 'Iyye': "እየ", 'Iske': "እስከ",
         'Inde': "እንደ", 'ke': "ከ", 'be': "በ", 'wede': "ወደ"
         }
    }

    VERB_POS = {'v', 'vp', 'vi', 'vj'}

    src_feats = ['c', 'v']

    # Positions on WPatterns corresponding to particular ውልድ forms. Some are
    # treated as synonymous.
    wcodes2patindex = {'0': 0, 'te_': 1, 'a_': 2, 'as_': 3, 'te_a': 4, 'a_a': 4, 'as_a': 4, 'te_R': 5, 'a_R': 5, 'R': 6}
    wpatcodes = [('0',), ('te_',), ('a_',), ('as_',), ('te_a', 'a_a'), ('te_R', 'a_R'), ('R',)]

    pre_gem_char = '/'
    # exclude ː for cases where we want the gemination indicated even when degeminating
    post_gem_chars = '፟_:'

    morph_sep = '-'

    #    mwe_space = '//'

    # Filters to use with anal_sentence to restrict syntax/morphology.
    filters = \
    {
      'core':
         # Only core arguments: nsubj, obj, iobj, expl?, csubj, xcomp, ccomp; no obl
         {'out': ( (('pos', 'n'), ('featfail', FeatStruct("[prep=None]"))),
                 ) },

      'verbs':
         {(1, 3): ( (('pos', ('v', 'cop', 'aux')),),
                  )},

      'verbs5':
         {(1, 5): ( (('pos', 'v'),),
                  )},

      'simple':
         # Only simple clauses with verb heads; no relative verbs, converbs, infinitives, or other subordinate verbs; no copulas
         # Problem: ነበረ is excluded, but it could be the past of አለ (favoring precision, not recall)
         {'out': ( (('pos', 'v'), ('feats', FeatStruct("[+sub]"))),
                   (('pos', 'v'), ('feats', FeatStruct("[tm=ger,ax=None]"))),
                   (('pos', ('n', 'n_dv')), ('feats', FeatStruct("[v=inf]"))),
                   (('pos', ('cop', 'aux')),),
                   (('pos', 'v'), ('lemma', 'ነበረ'))
                   ),
          'in': ( (('pos', 'v'), ('feats', FeatStruct("[-sub]")), ('featfail', FeatStruct("[tm=ger,ax=None]"))),
                ) },

      'complex':
         # Only complex clauses
         {'in': ( (('pos', 'v'), ('feats', FeatStruct("[+sub]"))),
                  # but these can also be part of compound tense: ገብቶ ነበር; need to check following word
                  # could leave this, missing all instances of subordinate converb
                  (('pos', 'v'), ('feats', FeatStruct("[tm=ger,ax=None]"))),
                  (('pos', ('n', 'n_dv')), ('feats', FeatStruct("[v=inf]"))) 
                  ) },

       'nonverbal':
         # Only non-verbal clauses: copula. ነበረ is included though this could be the past of እለ (favoring recall, not precision).
         # Cleft sentences are excluded
         {'in': ( (('pos', ('cop', 'aux')),),  # , ('feats', FeatStruct("[tm=prs]"))),
                  ),
          # Exclude all verbs except ነበር , but allow infinitives
          'out': ( (('pos', 'v'), ('lemmafail', 'ነበረ')),
                  ) },

       'ነበር':
         # Only clauses with some form of ነበር, either as aux or main verb.
         {'in': ( (('pos', ('cop', 'aux', 'v')), ('lemma', ('ነበር', 'ነበረ', 'ነበ፟ር'))),
                  ) }
       
         }

    def __init__(self):
#        print("Creating EES language {}".format(self))
        # EES pre-and post-processing: geezification, romanization,
        # handling of multi-word lexemes
        if not self.postpostproc:
            self.postpostproc = lambda form: form.replace('//', ' ')

#    @staticmethod
#    def char2space(string):
#        return string.replace(EES.mwe_space, ' ')

#    @staticmethod
#    def postproc(string, degem=True, mwe=False):
#        '''
#        Post-process by replacing spaces for MWEs and degeminating.
#        '''
#        if mwe:
#            string = EES.char2space(string)
#        if degem:
#            string = EES.degeminate(string)
#        return string

    @staticmethod
    def degeminate(string, elim_bounds=True):
        '''
        Remove gemination characters froms string (but do not replace MWE space chars //).
        If elim_bounds is True, also drop trailing morpheme boundary characters.
        '''
#        print("** Degeminating {}; {}".format(string, elim_bounds))
        for char in EES.pre_gem_char + EES.post_gem_chars:
            string = string.replace(char, '')
        if elim_bounds:
            if string[0] == EES.morph_sep:
                string = string[1:]
            if string[-1] == EES.morph_sep:
                string = string[:-1]
        return string

    @staticmethod
    def elim_bounds(string):
        '''
        Remove trailing morpheme boundaries.
        '''
        if string[0] == EES.morph_sep:
            string = string[1:]
        if string[-1] == EES.morph_sep:
            string = string[:-1]
        return string

    @staticmethod
    def unicode_geminate(string):
        '''
        Use the Unicode gemination character for gemination.
        '''
        chars = []
        gem_next = False
        for char in string:
            if char == EES.pre_gem_char:
                gem_next = True
            elif char == '_' or char == '፟':
                chars.append("፟")
            elif gem_next:
                chars.append(char + '፟')
                gem_next = False
            else:
                chars.append(char)
        return ''.join(chars)

    @staticmethod
    def make_weight(string, source=False, target=False):
        '''
        Make a weight, possibly for the source language in a translation FST.
        '''
        if source:
            string = EES.conv_string(string, SOURCE_WT_CONV)
        elif target:
            string = EES.conv_string(string, TARGET_WT_CONV)
        return UNIFICATION_SR.parse_weight(string)

    @staticmethod
    def sourcify_feats(feat_string):
        '''
        Modify features for source language, changing those in EES.src_feats.
        '''
        if not feat_string:
            return None
        feat_string = feat_string.split(',')
        strings = []
        for fv in feat_string:
            if '=' in fv:
                f, v = fv.split('=')
                if f in EES.src_feats:
                    strings.append("s{}={}".format(f, v))
                else:
                    strings.append(fv)
            else:
                strings.append(fv)
        return ','.join(strings)

    @staticmethod
    def targetify_feats(feat_string):
        '''
        Modify features for target language, changing those in EES.src_feats.
        '''
        if not feat_string:
            return None
        feat_string = feat_string.split(',')
        strings = []
        for fv in feat_string:
            if '=' in fv:
                f, v = fv.split('=')
                if f in EES.src_feats:
                    strings.append("t{}={}".format(f, v))
                else:
                    strings.append(fv)
            else:
                strings.append(fv)
        return ','.join(strings)

    @staticmethod
    def combine_src_targ_feats(src_feats, targ_feats):
        if src_feats:
            if targ_feats:
                return "[{},{}]".format(src_feats,targ_feats)
            else:
                return "[" + src_feats + "]"
        else:
            return "[" + targ_feats + "]"

    @staticmethod
    def get_filter(label):
        '''
        Get the filter conditions for given label, for example, 'simple'.
        '''
        return EES.filters.get(label)

    @staticmethod
    def conv_string(string, conversions):
#        print("** Converting {}".format(string))
        if conversions:
            for src, trg in conversions:
                if src in string:
                    string = re.sub(r"(\W){}".format(src), r"\1{}".format(trg), string)
#                                        .replace(src, trg)
        return string

    def geezify(self, form, gemination=False, deepenthesize=False):
        """
        Convert a romanized to a geez form.
        """
        return geezify(lang=self.abbrev, gemination=gemination,
                       deepenthesize=deepenthesize)

    def romanize(self, form, ipa=True):
        return romanize(form, lang=self.abbrev, ipa=ipa)

    ### Verb ውልድ templates
    ### A WPattern is a pattern of occurrences of particular verb ውልድ forms for
    ### a particular root-sense combination, represented as a string of 0s and 1s
    ### A WTemplate is a category of verb roots, consisting of a pattern of occurrences
    ### of particular verb ውልድ forms, with one singled out as the basic ውልድ.

    @staticmethod
    def score_WPattern(WP, WT):
        '''
        Assigns a score to WPattern in terms of how well it matches WTemplate.
        Non-occurrence of forms is penalized; scores are <= 0.
        '''
        score = 0
        if len(WP) < len(WT):
            # Make sure the pattern is as long as the template
            WP = WP + '*' * (len(WT) - len(WP))
        for p, t in zip(WP, WT):
            if t == '2':
                # The basic form for the template, must be present in WP
                if p != '1':
                    return -10
            elif t == '1':
                # A non-basic form found in the template; penalize non-occurrence
                if p == '0':
                    score -= 1
                elif p == '*':
                    score -= 0.5
            elif t == '0':
                # A form not found in the template; penalize occurrence
                if p == '1':
                    score -= 1
                elif p == '*':
                    score -= 0.5
        return score

    @staticmethod
    def assign_WPattern(wcodes):
        '''
        wcodes: a list of ውልድ codes, e.g., '0', 'te_', 'a_a', etc., for 
        forms occurring for a root/sense.
        '''
        code = []
        for cs in EES.wpatcodes:
            if any([(c in wcodes) for c in cs]):
                code.append('1')
            else:
                code.append('0')
        return ''.join(code)

    def postproc_root(self, posmorph, root, fs, phonetic=True, simplifications=None):
        """
        Create the <root:class> representation if this is possible.
        """
        cls = None
        if 'cls' in fs:
            cls = fs['cls']
        elif 'root' in fs and 'cls' in fs['root']:
            cls = fs['root']['cls']
        if cls:
            return "<{}:{}>".format(root, cls)
        else:
            root = "<{}>".format(geezify(root, self.abbrev))
            return root

    def preproc_root(self, root, fs, pos):
        """
        Preprocess root for generation.
        """
        if is_geez(root):
            if pos and pos.startswith('v'):
                # This is a verb root; we need the class
                anal = self.morphology[pos].anal(root, preproc=True)
                if anal:
                    root, ffss = anal[0]
                    cls = ffss.get('cls')
                    root, fs = \
                      self.dflt_procroot("{}:{}".format(root, cls), fs)
                else:
    #            print("Couldn't analyze {}".format(root))
                    return root, fs
            else:
                # Romanize noun roots
                root = geez2sera(None, root, self.abbrev)
                return root, fs
        else:
            root, fs = self.dflt_procroot(root, fs)
        return root, fs

    def verb_citation(self, root, fs, guess=False, vc_as=True, phonetic=True):
        '''
        Return the canonical (prf, 3sm) form for the root and featstructs
        in featstruct fs.

        If vc_as is True, preserve the voice and aspect of the original word.
        '''
        citation = ''
        if root == 'hlw':
            return "'al_e"
        # Return root if no citation is found
        result = root
        # Unfreeze the feature structure
        fs = fs.unfreeze()
        fsa, fsv = fs.get('as'), fs.get('vc')
        # Update the feature structure to incorporate default (with or without vc
        # and as)
        fs.update(AMH.morphology['v'].defaultFS)
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
    #    print("fs {}".format(fs.__repr__()))
        # Find the first citation form compatible with the updated feature structure
        if ' ' in root:
            # This is a light verb, just generate the actual verb
            root_split = root.split()
            citation = AMH.morphology['v'].gen(root_split[-1], fs, from_dict=False,
                                               phon=True, postproc=False, guess=guess)
            if citation:
                result = ' '.join(root_split[:-1]) + ' ' + citation[0][0]
        else:
    #        print("Generating citation from {}".format(fs.__repr__()))
            citation = AMH.morphology['v'].gen(root, fs, from_dict=False,
                                               phon=True, postproc=False,
                                               guess=guess)
            if citation:
                result = citation[0][0]
        if not citation:
            if not vc_as:
                # Verb may not occur in simplex form; try passive
                fs = fs.unfreeze()
                fs.update({'vc': 'ps'})
                fs.freeze()
                citation = AMH.morphology['v'].gen(root, fs, from_dict=False, guess=guess)
                if citation:
                    result = citation[0][0]
        return result

    # def vb_get_citation(self, root, fs,
    #                     guess=False, vc_as=False):
    #     '''Return the canonical (prf, 3sm) form for the root and featstructs in
    #     featstruct fs.
    #     If at is True, use Amharic/Tigrinya features.
    #     If vc_as is True, preserve the voice and aspect of the original word.
    #     '''
    #     citation = ''
    #     if root == 'hlw':
    #         return "አለ"
    #     # Return root if no citation is found
    #     result = root
    #     # Unfreeze the feature structure
    #     fs = fs.unfreeze()
    #     fsa, fsv = fs.get('as'), fs.get('vc')
    #     # Update the feature structure to incorporate default (with or without vc and as)
    #     fs.update(self.language.morphology['v'].defaultFS)
    #     # For non-passive te- verbs, te- is citation form
    #     if fs.get('lexav') == True:
    #         # Lexical entry with explicit as, vc features
    #         fs.update({'as': fsa, "vc": fsv})
    #     elif fs.get('lexip') == True:
    #         # Lexical entry for as=it,vc=ps and as=it,vc=tr
    #         fs.update({'as': 'it', 'vc': 'ps'})
    #     elif fs.get('lexrp') == True:
    #         # Lexical entry for as=rc, vc=ps and as=rc,vc=tr
    #         fs.update({'as': 'rc', 'vc': 'ps'})
    #     elif fs.get('smp') == False:
    #         # No vc=smp form, vc=ps is base/citation form
    #         fs.update({'vc': 'ps'})
    #     # Refreeze the feature structure
    #     fs.freeze()
    #     # Find the first citation form compatible with the updated feature structure
    #     if ' ' in root:
    #         # This is a light verb, just generate the actual verb
    #         root_split = root.split()
    #         citation = self.language.morphology['v'].gen(root_split[-1], fs, from_dict=False,
    #                                            phon=True, postproc=False, guess=guess)
    #         if citation:
    #             result = ' '.join(root_split[:-1]) + ' ' + citation[0][0]
    #     else:
    # #        print("Generating citation from {}".format(fs.__repr__()))
    #         citation = self.language.morphology['v'].gen(root, fs, from_dict=False,
    #                                            phon=True, postproc=False, guess=guess)
    #         if citation:
    #             result = citation[0][0]
    #     if not citation:
    #         if not vc_as:
    #             # Verb may not occur in simplex form; try passive
    #             fs = fs.unfreeze()
    #             fs.update({'vc': 'ps'})
    #             fs.freeze()
    #             citation = self.language.morphology['v'].gen(root, fs, from_dict=False, guess=guess)
    #             if citation:
    #                 result = citation[0][0]
    #     return result
    #
    # def n_get_citation(self, root, fs, guess=False, vc_as=False):
    #     '''Return the canonical (prf, 3sm) form for the root and featstructs in featstruct set fss.
    #
    #     If vc_as is True, preserve the voice and aspect of the original word.
    #     '''
    #     if fs.get('v'):
    #         # It's a deverbal noun
    #         return vb_get_citation(root, fs, guess=guess, vc_as=vc_as)
    #     else:
    #         return None
    #
    # def simplify(self, word):
    #     """Simplify Amharic orthography."""
    #     word = word.replace("`", "'").replace('H', 'h').replace('^', '').replace('_', '')
    #     return word
    #
    # def orthographize(self, word):
    #     '''Convert phonological romanization to orthographic.'''
    #     word = word.replace('_', '').replace('I', '')
    #     return word
    #
    # def webfv(self, webdict, feature, value):
    #     if webdict != None:
    #         webdict[feature] = value
    #
    # def postpostproc_root(self, root, fs):
    #     """
    #     Convert root to root:class format, also changing internal
    #     HM root representation to an alternate conventional
    #     representation.
    #     """
    #     return "<{}:{}>".format(self.language.convert_root(root), fs['cls'])
    #
    # def postproc_nroot(self, root, fs):
    #     """
    #     Convert citation (lemma) to conventional phonetic representation.
    #     """
    #     if fs.get('pos') == 'n_dv':
    #         return "<{}:{}>".format(self.language.convert_root(root), fs['cls'])
    #     else:
    #         return "{}|{}".format(geezify(root), self.language.convert_phones(root))
    #
    # def postproc_word(self, word, ipa=False):
    #     """
    #     Convert output word to ortho|phon representation, also
    #     changing internal HM representation to an alternate
    #     conventional representation.
    #     """
    #     return "{}|{}".format(geezify(word), self.language.convert_phones(word))
    #
    # def load_anal(self, pos='v', lex=True, guess=False):
    #     if lex:
    #         self.language.morphology[pos].load_fst(True, verbose=True)
    #     if guess:
    #         self.language.morphology[pos].load_fst(True, guess=True, verbose=True)
    #
    # def load_gen(self, pos='v', lex=True, guess=False):
    #     if lex:
    #         self.language.morphology[pos].load_fst(True, generate=True, invert=True, verbose=True)
    #     if guess:
    #         self.language.morphology[pos].load_fst(True, generate=True, invert=True, guess=True, verbose=True)
    #
    # @staticmethod
    # def postproc_root(root):
    #     """Final adjustments to romanized root."""
    #     # Replace __ with space.
    #     if '//' in root:
    #         root = root.replace('//', ' ')
    #     return root
    #
    # @staticmethod
    # def roman2geez(value):
    #     """Convert a value (prep or conj) to geez."""
    #     return EES.ROM2GEEZ.get(value, value)
    #
    # def seg2string(self, segmentation, sep='-', geez=True, features=False,
    #                arules=False):
    #     """Convert a segmentation to a string, including features if features is True."""
    #     # The segmentation string is second in the list
    # #    print("Converting {} to string".format(segmentation))
    #     morphs, rootindex = self.language.seg2morphs(segmentation[1])
    #     # Root string and features
    #     root, rootfeats = morphs[rootindex]
    #     # Separate the consonants and template, and realize the root
    #     root = root2string(root)
    #     # Replace the root in the morphemes list
    #     morphs[rootindex] = root, rootfeats
    #     if geez:
    #         # First make sure separate morphemes are geez
    #         morphs2 = [[(g, f) for g in geezify_morph(m, alt=True)] for m, f in morphs]
    #     else:
    #         morphs2 = []
    #         for m, f in morphs:
    #             conv = convert_labial(m)
    #             morphs2.append([(c, f) for c in conv])
    #     morphs = allcombs(morphs2)
    # #    print(" Morphs {}".format(morphs))
    #     if not features:
    #         morphs = [[w[0] for w in word] for word in morphs]
    #     else:
    #         # Rejoin morpheme and features for each word
    #         morphs = [[''.join(m) for m in word] for word in morphs]
    #     return [sep.join(m) for m in morphs]
    #
    # def root2string(self, root):
    #     """If root contains '+', it consists of a root and a template, which need to be
    #     integrated."""
    #     if '+' in root:
    #         cons, temp = root.split('+')
    #         cons = segment(cons, self.language.seg_units)
    #         cons = [c for c in cons if c not in ['a', '_']]
    # #        print("root cons: {}, temp {}".format(cons, temp))
    #         if 'tt' in temp:
    #             temp = temp.replace('tt', 't_')
    #         temp = [(int(t) if t.isdigit() else t) for t in temp]
    #         form = []
    #         last_cons = ''
    #         for index, t in enumerate(temp):
    #             if isinstance(t, int):
    #                 # Template positions are 1-based, not 0-based
    #                 c = cons[t-1]
    #                 if c != last_cons:
    #                     form.append(cons[t-1])
    #                 else:
    #                     # Identical consonants; geminate
    #                     form.append('_')
    #                 last_cons = c
    #             elif index == 0 and t in "aeiouIE":
    #                 form.append("'" + t)
    #             elif t in "stm":
    #                 form.append(t)
    #                 last_cons = t
    #             else:
    #                 form.append(t)
    #                 # A vowel or _ character was added so clear the last consonant
    #                 last_cons = ''
    #         return '{' + ''.join(form) + '}'
    #     else:
    #         return '{' + root + '}'
