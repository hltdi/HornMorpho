"""
This file is part of HornMorpho, which is part of the PLoGS project.

    <http://homes.soic.indiana.edu/gasser/plogs.html>

    Copyleft 2022, 2023, 2024.
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

Representing sentences (or corpora as lists of sentences) with words
segmented by HornMorph.
Includes CoNLL-U and XML output options
"""

import xml.etree.ElementTree as ET
from conllu import TokenList, Token, Metadata
from conllu.parser import parse_comment_line
from .geez import degeminate
from .cg import CG
#from .gui import SegRoot
import sys

#class PseudoCorpus():
#    pass

class HMToken(Token):

    def __init__(self, dct, analysis=None):
        self.analysis = analysis
        Token.__init__(self, dct)

    @staticmethod
    def create_unal(index, token):
        return HMToken(
            {'id': index, 'form': token, 'lemma': None, 'upos': 'UNK', 'xpos': 'UNK',
             'feats': None, 'head': index, 'deprel': None, 'deps': None, 'misc': None},
             analysis=[])

    @staticmethod
    def create1(index, token, lemma, pos, feats, analysis, xpos=None, misc=None):
        '''
        Make an HMToken for an unsegmented token.
        '''
#        print(" ** creating HMT for {}, index {}".format(token, index))
        return HMToken(
            {'id': index, 'form': token, 'lemma': lemma, 'upos': pos, 'xpos': xpos or pos, 'feats': feats, 'head': index,
             'deprel': None, 'deps': None, 'misc': misc},
             analysis=analysis
             )

    @staticmethod
    def create_mult(start, end, token, analysis, misc=None):
        return HMToken(
            {'id': "{}-{}".format(start, end),
             'form': token, 'lemma': None, 'upos': None, 'xpos': None, 'feats': None, 'head': None, 'deprel': None, 'deps': None, 'misc': misc},
             analysis=analysis
             )

    @staticmethod
    def create_morph(index, string, lemma, pos, feats, head, deprel, analysis, xpos=None, misc=None):
        return HMToken(
            {'id': index, 'form': string, 'lemma': lemma, 'upos': pos, 'xpos': xpos or pos,
             'feats': feats, 'head': head, 'deprel': deprel, 'deps': None, 'misc': misc
                },
                analysis=analysis
                )

class Sentence():
    """
    Representation of HM output for a sentence in a corpus.
    """

    selectpos = \
      {
       'NADJ': ['NOUN', 'ADJ'], 'NPROPN': ['NOUN', 'PROPN'], 'VINTJ': ['VERB', 'INTJ'], 'NADV': ['NOUN', 'ADV'], 'PRONADJ': ['PRON', 'ADJ'],\
       'ADPCONJ': ['ADP', 'SCONJ'], 'ADVCONJ': ['ADV', 'SCONJ'], 'ADVADP': ['ADV', 'ADP'], 'PARTCONJ': ['PART', 'SCONJ'], 'ADVINTJ': ['ADV', 'INTJ']
      }

    um2udPOS = {'N': 'NOUN', 'V': 'VERB', 'N_V': 'NOUN'}

    colwidth = 20

    conllu_list = ['id', 'form', 'lemma', 'upos', 'xpos', 'feats', 'head', 'deprel', 'deps', 'misc']

    def __init__(self, text, language, **kwargs):
#                     tokens=[], batch_name='', sentid=0, language=None, label='', meta=''):
        """
        kwargs: 'tokens', 'batch_name', 'sentid', 'label', 'meta'
        """
        self.language = language
        self.um = language.um
        self.tokens = kwargs.get('tokens', [])
        self.text = text
        self.ntokens = len(text.split())
        self.words = []
        meta = kwargs.get('meta')
        metadata = Metadata(parse_comment_line(meta)) if meta else {}
        if metadata and 'text' not in metadata:
            metadata['text'] = text
        self.sentid = metadata.get('sent_id') or kwargs.get('sentid', 1)
        self.batch_name = kwargs.get('batch_name', '')
        self.label = kwargs.get('label') or "{}{}".format(self.batch_name + "_" if self.batch_name else '', self.sentid)
        self.xml = ''
        self.conllu = TokenList([])
        self.conllu.metadata = metadata if metadata else Metadata({'text': text, 'sent_id': self.label})
        # For degeminated (or eventually other modified) CoNLL-U representations of sentence
        self.alt_conllu = None
        # list of unknown tokens
        self.unk = []
        # list of morphologically ambiguous words
        self.morphambig = []
        # list of POS ambiguous words
        self.posambig = []
        # whether sentence has been disambiguated
        self.disambiguated = False
        self.conllu_string = ''
        self.complexity = {'ambig': 0, 'unk': 0, 'punct': 0}
        self.merges = []
        # Given a set of properties, like 'root' and 'um', a list of lists of word property dicts.
        self.props = []
        ## attributes added from CG rules
        # Sentence root, unless -1
        self.root = -1
        # dict {child_windex: (parent_windex, relation) ...}
        self.relations = {}
        # number of relations added
        self.nrelations = 0
        # number of unlabeled dependencies added
        self.ndependencies = 0

    def __repr__(self):
        return "S::{}::{}".format(self.sentid, self.text)

    def show(self):
        '''
        Show each words processed analyses.
        '''
        for word in self.words:
            word.show()

    def reinit_conllu():
        metadata = self.conllu.metadata
        self.conllu = TokenList([])
        self.conllu.metadata = metadata

    ### Version 5 methods

    def add_word5(self, word, unsegment=False):
        '''
        Version 5: given a Word object, convert it to ambiguous CoNLL-U format,
        and add it to self.words.
        '''
#        print("$$ add_word {}, known {}".format(word, word.is_known()))
#        word.show()
        conllus = []
        for analysis in word:
            conllu = Sentence.anal2conllu(word.name, analysis, unsegment=unsegment)
#            print("&& conllu for {}: {}".format(word, conllu.serialize()))
            conllus.append(conllu)
        # Add the CoNLL-U representations to the Word
        word.conllu = conllus
        # Add the Word to self.words
        self.words.append(word)
        # If Word is ambiguous, add it to morphambig
        if len(word) > 1:
            self.morphambig.append(word)
        elif not word.is_known():
            self.unk.append(word.name)

    def set_annotation(self, root, relations):
        '''
        Add attributes from the output of CG annotation rules.
        '''
        if root >= 0:
            self.root = root

    def print_conllu(self, update_ids=True, file=None):
        '''
        Print the string of CoNLL-U representations for the sentence,
        using the first if there are still ambiguities.
        If update_ids is True, update the id and head fields based
        on each word's position in the sentence.
        '''
        file = file or sys.stdout
        print(self.create_conllu(update_ids=update_ids), file=file, end='')

    def create_conllu(self, update_ids=True, add_rels=True, verbosity=0):
        '''
        Return the string of CoNLL-U representations for the sentence,
        using the first if there are still ambiguities.
        Apply root and relation information from CG rules.
        If update_ids is True, update the id and head fields based
        on each word's position in the sentence.
        '''
        if not update_ids and self.conllu_string:
            return self.conllu_string
        elif self.conllu_string:
            # start over with new sentence conllu
            self.reinit_conllu()
        string = ''
        index = 0
        windex2id = {}
        for windex, word in enumerate(self.words):
            # Assume disambiguation has happened or we trust the first analysis
            conllu = word.conllu[0]
            if update_ids:
                index = self.update_conllu_ids(conllu, windex2id, windex, index=index)
            self.conllu.extend(conllu)
        if verbosity:
            print("windex2id: {}".format(windex2id))
        if add_rels:
            self.update_conllu_rels(windex2id, verbosity=verbosity)
        # Add the root and relation information
        self.conllu_string = self.conllu.serialize()
        return self.conllu_string

    def update_conllu_rels(self, windex2id, verbosity=0):
        if verbosity:
            print("Updating relations")
        root = self.root
        relations = self.relations
        idrelations = {}
        if root >= 0:
            rootid = windex2id[root]
            idrelations[rootid] = (0, 'root')
        if relations:
            for childindex, (parentindex, label) in relations.items():
                childid = windex2id[childindex]
                parentid = windex2id[parentindex]
                idrelations[childid] = (parentid, label)
        if verbosity:
            print("idrelations {}".format(idrelations))
        for c in self.conllu:
            id = c['id']
            if par_rel := idrelations.get(id):
                parent, rel = par_rel
                c['head'] = parent
                if rel:
                    c['deprel'] = rel
                    self.nrelations += 1
                else:
                    self.ndependencies += 1

    def update_conllu_ids(self, conllu, windex2id, windex, index=0):
        '''
        Update the position fields (id and head) for a representation based on
        the word's position within the sentence.
        '''
        new_index = index
        # Don't update if the index is 0
        length = len(conllu)
        if length == 1:
            conllu[0]['id'] += index
            conllu[0]['head'] = None
            windex2id[windex] = conllu[0]['id']
            new_index += 1
        else:
            # Update all of the segments
            # First the range in the whole-word line
            whole = conllu[0]
            if index:
                current_range = whole.get('id')
                start, end = current_range.split('-')
                start = int(start) + index
                end = int(end) + index
                whole['id'] = "{}-{}".format(start, end)
                # Then the id and head for each of the segments
                for c in conllu[1:]:
                    c['id'] += index
                    c['head'] += index
                    if c['id'] == c['head']:
                        # This is the head of the word, so add it to the windex2id dict
                        windex2id[windex] = c['id']
                        c['head'] = None
            else:
                for c in conllu[1:]:
                    if c['id'] == c['head']:
                        # This is the head of the word, so add it to the windex2id dict
                        windex2id[windex] = c['id']
                        c['head'] = None
            new_index += len(conllu)-1
#        print("** Updated index: {}".format(new_index))
        return new_index

    @staticmethod
    def convertPOS(analdict):
        umPOS = analdict.get('pos')
        if umPOS:
            if isinstance(umPOS, list):
                return [Sentence.um2udPOS.get(u, u) for u in umPOS]
            else:
                return Sentence.um2udPOS.get(umPOS, umPOS)
        return None

    @staticmethod
    def format_misc(analdict):
        '''
        value is either None or a list of feature=value strings.
        '''
        value = analdict.get('misc') or None
        if value:
            value.sort()
            value = '|'.join(value)
        return value

    @staticmethod
    def anal2conllu(token, analdict, index=1, unsegment=False):
        '''
        Create a CoNLL-U representation from a token's analysis dict.
        '''
#        print("**anal2conllu {}".format(token))
        if not analdict:
            # Unanalyzed token
            return TokenList([HMToken.create_unal(index, token)])

        if unsegment:
            pos = Sentence.convertPOS(analdict)
            return TokenList(
                [HMToken.create1(
                    index, token, analdict.get('lemma', token), pos, analdict.get('udfeats'), analdict, analdict.get('xpos'), Sentence.format_misc(analdict))]
                )

        if analdict['nsegs'] == 1:
            pos = Sentence.convertPOS(analdict)
            return TokenList([HMToken.create1(index, token, analdict.get('lemma', token), pos, analdict.get('udfeats'), analdict, analdict.get('xpos'), Sentence.format_misc(analdict))])

        conllu = TokenList()
        # Create the line for the whole token
        conllu.append(
            HMToken.create_mult(index, index+analdict['nsegs']-1, token, analdict, misc=Sentence.format_misc(analdict))
            )
        stemdict = analdict['stem']

        mwe_first = False
        mwe = 'tokens' in analdict
        if mwe:
            mwe_feats = analdict['feats']
#            print("mwe feats {}".format(mwe_feats.__repr__()))
            if mwe_feats and mwe_feats.get('segpart', False):
                if mwe_feats.get('hdfin', False):
                    mwe_first = True
                    token = analdict['tokens'][0]
                    string = token['token']
                    pos = token.get('pos', mwe_feats.get('pos'))
                    xpos = token.get('xpos', None)
                    misc = Sentence.format_misc(mwe_feats)
                    head = stemdict.get('head', 0)+2
#                    print("** MWE token {} pos {} head {}".format(token, pos, head))
                    conllu.append(
                        HMToken.create_morph(index, string, string, pos, None, head, mwe_feats.get('dep'), analdict, xpos=xpos, misc=misc)
                        )
                    index += 1
#                else:
#                    print("**  Last position")

        for p in analdict.get('pre', []):
            if not p:
                continue
            # This should be a list
            pos = Sentence.convertPOS(p)
            string = p['seg']
            head = p.get('head', 0)+1
            if mwe_first:
                head += 1
#            print(" *** lemma for prefix {}".format(string))
            if ' ' in string:
                strings = string.split()
                for string, ps in zip(strings, pos):
                    conllu.append(
                        HMToken.create_morph(index, string, p.get('lemma', string), ps, p.get('udfeats'), head, p.get('dep'), p, xpos=p.get('xpos'), misc=Sentence.format_misc(p))
                        )
                    index += 1
            else:
                conllu.append(
                        HMToken.create_morph(index, string, p.get('lemma', string), pos, p.get('udfeats'), head, p.get('dep'), p, xpos=p.get('xpos'), misc=Sentence.format_misc(p))
                        )
                index += 1

        pos = Sentence.convertPOS(stemdict)
        head = stemdict.get('head', 0)+1
        if mwe_first:
            head += 1
        stem_string = stemdict['seg']
        conllu.append(
            HMToken.create_morph(
                index, stem_string, stemdict.get('lemma', analdict.get('lemma', stem_string)), pos, stemdict.get('udfeats'), head,
                stemdict.get('dep'), stemdict, xpos=stemdict.get('xpos'), misc=Sentence.format_misc(stemdict)
                ))
        index += 1

        for s in analdict.get('suf', []):
            if not s:
                continue
            pos = Sentence.convertPOS(s)
            string = s['seg']
            head = s.get('head', 0)+1
            if mwe_first:
                head += 1
            conllu.append(
                HMToken.create_morph(index, string, s.get('lemma', string), pos, s.get('udfeats'), head, s.get('dep'), s, s.get('xpos'), Sentence.format_misc(s)
                ))
            index += 1
        
        return conllu

    @staticmethod
    def updatePOS(analdict, pos):
#        print("&& Updating POS in {} to {}".format(analdict, pos))
        analdict['pos'] = pos

    @staticmethod
    def update_feats(analdict, udfeats):
#        print("&& Updating feats in {} to {}".format(analdict, udfeats))
        if 'udfeats' in analdict:
            analdict['udfeats'] = udfeats

    def postproc(self, verbosity=0):
        '''
        Attempt to simplify disambiguation by eliminating some duplication at the Word level.
        '''
        if verbosity:
            print("Post processing {}".format(self))
        # Eliminate derivational analyses that duplicate unsegmented forms.
        for word in self.words:
            todel = word.elim_segmented_dups()
            if todel:
#                print("** postprocessing deleting {}".format(todel))
                word.remove(todel)
                if len(word) == 1:
                    self.morphambig.remove(word)

    def merge5(self, gemination=False, sep_senses=False, verbosity=0):
        '''
        Attempt to merge segmentations of each word.
        '''
        self.merges = [(word.name, word.merge(gemination=gemination, sep_senses=sep_senses, verbosity=verbosity)) for word in self.words]
#        print("&& merges: {}".format(self.merges))

    def set_props(self, props):
        '''
        Props is a list of properties (like 'root' and 'um').
        Creates a list of (word, property_dicts) pairs.
        '''
        if not props:
            return
        result = []
        for windex, word in enumerate(self.words):
            if not word.is_empty():
                result.append((windex, word.name, word.to_dicts(props)))
        self.props = result

    def create_attrib_strings(self, attribs, all_anals=True):
        '''
        Create strings with the specified attributes (tab-separated) for word analyses,
        only the first unless all_anals is True
        '''
        lines = [self.text]
        for word in self.words:
            word_string = word.create_attrib_string(attribs, all_anals=all_anals)
            lines.append(word_string)
        return '\n'.join(lines)

    def disambiguate(self, verbosity=0):
        '''
        Shortcut for CG disambiguation.
        '''
        if verbosity:
            print("Disambiguating {}".format(self))
        return self.language.disambiguate(self, verbosity=verbosity)

    def annotate(self, verbosity=0):
        '''
        Shortcut for CG annotation.
        '''
        if verbosity:
            print("Annotating {}".format(self))
        return self.language.annotate(self, verbosity=verbosity)

    def toCG(self, verbosity=0):
        '''
        Shortcut for conversion to CG format.
        '''
        return CG.sentence2cohorts(self, verbosity=verbosity)

    def printCG(self, verbosity=0):
        '''
        Shortcut for printing out CG format.
        '''
        print(self.toCG().format())

    #####
        
    def is_ambiguous(self):
        """
        Are there multiple segmentations or ambiguous POSs for any word in the sentence?
        """
        return self.complexity['ambig'] > 0.0

    def finalize(self):
        '''
        Finalize complexity counts.
        '''
        # Average ambiguity of tokens
        self.complexity['ambig'] /= self.ntokens
        # Proportion of unknown tokens
        self.complexity['unk'] /= self.ntokens
        # Expect one punctuation mark
        self.complexity['punct'] -= 1

    def filter(self, filterconds):
        '''
        Filter out the sentence if it satisfies any of filterconds.
        Each filtercond has the form a list of lists of word filterconds
        '''

    def reject(self, unk_thresh=0.3, ambig_thresh=1.0, verbosity=0):
        """
        Should we reject this sentence, based on its complexity?
        """
        complexity = self.complexity
        npunct = complexity['punct']
        if npunct > 0:
            if verbosity:
                print("Rejecting {} because there are {} punctuation marks".format(self, npunct))
            return True
        if complexity['ambig'] > ambig_thresh:
            if verbosity:
                print("Rejecting {} because ambiguity {} > threshold {}".format(self, round(complexity['ambig'], 2), ambig_thresh))
                if self.posambig:
                    print("POS ambiguous tokens: {}".format(self.posambig))
                if self.morphambig:
                    print("Morphologically ambiguous tokens: {}".format(self.morphambig))
            return True
        if complexity['unk'] > unk_thresh:
            if verbosity:
                print("Rejecting {} because percentage of unknown tokens {} > threshold {}".format(self, round(complexity['unk'], 2), unk_thresh))
                print("Unknown tokens: {}".format(self.unk))
            return True
        return False

    def record_ambiguities(self, v5=False):
        '''
        Return the number of ambiguities (POS, segmentation) in the sentence.
        '''
        count = 0
        ambig = []
        for index, word in enumerate(self.words):
            if v5:
                word = word.conllu
            if len(word) == 0:
                continue
            elif len(word) > 1:
                # multiple segmentations
                ambig.append(index)
                count += 1
            else:
                # first segmentation
                word = word[0]
#                print("** word {}".format(word))
                for morph in word:
                    pos = morph.get('upos')
                    if pos in Sentence.selectpos:
                        # an ambiguous POS
                        ambig.append(index)
                        count += 1
                    feats = morph.get('feats')
                    if feats and '&' in feats:
                        # Features beginning in & need to be disambiguated manually
#                        print("** ambiguous feats {}, appending to ambig {}".format(feats, ambig))
                        ambig.append(index)
                        count += 1
#                    print("  ** feats {}".format(feats))
        return ambig

    @staticmethod
    def get_clist_field(clist, attrib):
        '''
        From a pre-CoNNL-U list, get the attrib
        '''
        cindex = Sentence.conllu_list.index(attrib)
        return clist[cindex][1]

    @staticmethod
    def set_clist_field(clist, attrib, value):
        '''
        Set the value for attrib in a pre-CoNLL-U list to value.
        '''
        cindex = Sentence.conllu_list.index(attrib)
        clist[cindex][1] = value
                
    @staticmethod
    def copy_clist_field(clist_src, clist_targ, attrib):
        '''
        Set the value for attrib in a pre-CoNLL-U list to value.
        '''
        value = Sentence.get_clist_field(clist_src, attrib)
        Sentence.set_clist_field(clist_targ, attrib, value)

    def words2conllu(self, update_indices=True, gem=True, degem=False, verbosity=0):
        '''
        Convert a pre-CoNLL-U list of lists of Token dicts to a list of Tokens.
        If gem is True (always?), create the unmodified geminated CoNNL-U. If degem is True,
        create a degeminated version (stored in Sentence.alt_conllu).
        '''
        if self.disambiguated:
            # Some disambiguation took place; recalculate morphological ambiguity
            self.posambig = []
            self.morphambig = []
            self.complexity['ambig'] = 0
            for wordsegs in self.words:
                if len(wordsegs) > 1:
                    word = wordsegs[0][0]['form']
                    self.morphambig.append(word)
                    self.complexity['ambig'] += len(wordsegs) - 1
        # To convert to CoNLL-U, use only the first segmentation for each word.
        # Either disambiguation has taken place, and this is the only segmentation,
        # or the first (hopefully best) segmentation will be selected.
        wordsegs = [w[0] for w in self.words]
        # Update the indices in case the number of morphemes in a word has changed
        index = 1
        conllu = []
        if degem and self.alt_conllu == None:
            self.alt_conllu = TokenList([])
            alt_conllu = []
        for wordseg in wordsegs:
            if len(wordseg) == 1:
                # No segments: use current index
                ws = wordseg[0]
                ws['id'] = index
#                # Degeminate form always
#                ws['form'] = degeminate(ws['form'])
                # Degem lemma too if degem is True
                if degem:
                    altws = ws.copy()
                    Sentence.degeminate_seg(altws)
                    alt_conllu.append(altws)
                conllu.append(ws)
                index += 1
                if self.disambiguated:
                    # Update POS ambiguity
                    upos = ws['upos']
                    if upos in Sentence.selectpos:
                        self.complexity['ambig'] += 1
                        self.posambig.append(ws['form'])
            else:
                wholeword = wordseg[0]
                morphsegs = wordseg[1:]
                nmorphs = len(morphsegs)
                end = index + nmorphs
                # headindex is current index (of the whole word) + index offset stored in misc
                headindex = index + wholeword['misc']
                wholeword['id'] = (index, '-', end-1)
                # Get rid of the index offset that's stored here so that it doesn't appear in final CoNLL-U
                wholeword['misc'] = None
                # Degeminate form always
#                wholeword['form'] = degeminate(wholeword['form'])
                if degem:
                    altwholeword = wholeword.copy()
                    Sentence.degeminate_seg(altwholeword)
                    alt_conllu.append(altwholeword)
                conllu.append(wholeword)
                for morphseg in morphsegs:
#                    print("  ** morphseg {}, index {}, headindex {}".format(morphseg, index, headindex))
                    morphseg['id'] = index
                    if index == headindex:
                        # We don't know what the head of the head of the word is, so make it None ('_')
                        morphseg['head'] = None
                    else:
                        morphseg['head'] = headindex
                    # Degeminate form always
                    morphseg['form'] = degeminate(morphseg['form'])
                    if degem:
                        altmorphseg = morphseg.copy()
                        Sentence.degeminate_seg(altmorphseg)
                        alt_conllu.append(altmorphseg)
                    conllu.append(morphseg)
                    index += 1
        conllu = TokenList(conllu)
        conllu.metadata = self.conllu.metadata
        self.conllu = conllu
        if degem:
            alt_conllu = TokenList(alt_conllu)
            alt_conllu.metadata = self.conllu.metadata
            self.alt_conllu = alt_conllu
        if self.disambiguated:
            # Recalculate ambiguity score
            self.complexity['ambig'] /= self.ntokens

    @staticmethod
    def degeminate_seg(seg):
#        seg['form'] = degeminate(seg['form'])
        if seg.get('lemma'):
            seg['lemma'] = degeminate(seg['lemma'])

    def add_word(self, word, segmentations, morphid, conllu=True, seglevel=0, um=0):
        w = self.make_word(word, segmentations, morphid, conllu=conllu, seglevel=seglevel, um=um)
        if conllu:
            self.conllu.extend(w)

    def merge_segmentations(self):
        '''
        Merge identical or similar segmentations.
        '''
        for windex, word in enumerate(self.words):
            if len(word) > 1:
#                print("** Attempting to merge word {} segmentations".format(windex))
                merges = self.merge_word(word)
                if merges:
#                    print("*** merges for {}: {}".format(windex, merges))
                    # Only make one change for each word
                    merge = merges[0]
                    if len(merge) == 2:
                        # two segmentations are identical
                        i1, i2 = merge
                    elif len(merge) == 4:
                        # combine features from the two segmentations in the first one
                        i1, i2, mindex, changes = merge
                        morph = word[i1][mindex]
                        for field, value in changes:
                            morph[field] = value
                    # delete the second (redundant) segmentation
                    del word[i2:i2+1]

    def merge_word(self, word):
        '''
        Possibly merge segmentations for word, if there are alternatives
        '''
        merges = []
        POSs = [('NOUN', 'PROPN'), ('PROPN', 'NOUN')]
        for index1, segs1 in enumerate(word[:-1]):
            for index2, segs2 in enumerate(word[index1+1:]):
                i2 = index1+index2+1
#                print("*** Comparing segmentations {} and {}".format(segs1, segs2))
                c = self.compare_segs(segs1, segs2)
                if c is False:
                    # seg1 and seg2 are identical
                    merges.append((index1, i2))
                elif c is True:
                    # seg1 and seg2 are different lengths
                    continue
                else:
                    for mindex, merged in c.items():
                        if merged.get('upos') in POSs:
                            merges.append((index1, i2, mindex, [('upos', 'NPROPN'), ('xpos', 'NPROPN')]))
        return merges

    def compare_anals(self, anal1, anal2):
        '''
        V5: compare anals to merge if possible
        '''
        pos1 = anal1.get('pos')
        pos2 = anal2.get('pos')

    def compare_feats(self, anal1, anal2):
        '''
        Check whether two analyses are the same except for particular features.
        So far: DEF vs. PSS3SM or PSS3SF for nouns and DEF vs. AC3SM for relative verbs
        '''

    def compare_segs(self, seg1, seg2):
        '''
        Return differences between seg1 and seg2.
        '''
        # indexed dicts of differences
        if seg1 == seg2:
            # Segmentations are identical
            return False
        if len(seg1) != len(seg2):
            # Segmentations are different lengths; no point in merging
            return True
        diffs = {}
        for index, (morph1, morph2) in enumerate(zip(seg1, seg2)):
            # skip id and head?
            for key in ('form', 'lemma', 'upos', 'xpos', 'feats', 'deprel'):
                v1 = morph1.get(key)
                v2 = morph2.get(key)
                if v1 != v2:
                    if index not in diffs:
                        diffs[index] = {key: (v1, v2)}
                    else:
                        diffs[index][key] = (v1, v2)
        return diffs

    def make_unsegmented_word(self, word, segmentations, morphid, conllu=True, um=0):
        '''
        Use pre-CoNLL-U lists to produce an unsegmented CoNLL-U representation for a word.
        '''
#        print("**** Creating unsegmented word for {}".format(segmentations))
        tokens = []
        cdicts = []
        for segmentation in segmentations:
            dicts = []
            upos = lemma = headfeats = wordfeats = ''
            clist = [['id', morphid], ['form', word], ['lemma', None],  ['upos', None], ['xpos', None],
                     ['feats', None], ['head', None], ['deprel', None], ['deps', None], ['misc', None]]
            for morph in segmentation:
#                print("***  morph {}".format(morph))
                deprel = Sentence.get_clist_field(morph, 'deprel')
                if not deprel:
                    # This is the head of the word
                    Sentence.copy_clist_field(morph, clist, 'upos')
                    Sentence.copy_clist_field(morph, clist, 'xpos')
                    Sentence.copy_clist_field(morph, clist, 'lemma')
                    wordfeats = Sentence.get_clist_field(morph, 'misc')
#                    print("**** feats {}".format(wordfeats))
                    if um:
                        Sentence.set_clist_field(clist, 'feats', wordfeats)
                    else:
                        Sentence.copy_clist_field(morph, clist, 'feats')
            cdict = dict(clist)
            cdicts.append([cdict])
            tokens.append(Token(cdict))
        self.words.append(cdicts)
#                self.words.append([[cdict]])
#        return [Token(cdict)]
        return tokens

    def make_word(self, word, segmentations, morphid, conllu=True, um=0, seglevel=2):
        '''
        Creates a new word from a list of (lists of) segmentations.
        If conllu is True, returns a list of morpheme Tokens.
        um and seg control the features and the level of segmentation.
        '''
#        print("*** make_word segmentations {}".format(segmentations))
        if not conllu:
            self.words.append(segmentations)
            return segmentations
        if seglevel == 0:
            return self.make_unsegmented_word(word, segmentations, morphid, conllu=conllu, um=um)
        segment_list = []
        tokens = []
        self.complexity['ambig'] += len(segmentations) - 1
        if len(segmentations) > 1:
            self.morphambig.append(word)
#        print("*** word {}, segmentations {}".format(word, segmentations))
        for index, segmentation in enumerate(segmentations):
            segments = []
            nmorphs = len(segmentation)
#            print("  *** Segmentation {}, length {}".format(segmentation, nmorphs))
            if nmorphs == 1:
                # The word has only one morpheme
                props = segmentation[0].copy()
                Sentence.set_clist_field(props, 'id', morphid)
#                props[0][1] = morphid
#                upos = props[3][1]
                upos = Sentence.get_clist_field(props, 'upos')
                if upos == 'UNK':
                    self.complexity['unk'] += 1
                    self.unk.append(word)
                elif upos == 'PUNCT':
                    self.complexity['punct'] += 1
                elif upos in Sentence.selectpos:
                    # ambiguous POS
                    self.complexity['ambig'] += 1
                    self.posambig.append(word)
#                props.extend([('deps', None), ('misc', None)])
                pdict = dict(props)
                # Degeminate form
                pdict['form'] = degeminate(word)
                # Removed features from 'misc'
                pdict['misc'] = None
                segments.append(pdict)
                if conllu and index == 0:
                    tokens.append(Token(pdict))
            else:
#                tokens = []
                endid = morphid + nmorphs
                ids = (morphid, '-', endid-1)
                props = [('id', ids), ('form', degeminate(word)), ('lemma', None), ('upos', None), ('xpos', None),
                         ('feats', None), ('head', None), ('deprel', None), ('deps', None), ('misc', None)]
                pdict = dict(props)
                segments.append(pdict)
                if conllu and index == 0:
                    tokens.append(Token(pdict))
                id = morphid
                # Get the index of the head
                headi = -1
                for i, props in enumerate(segmentation):
#                    print("    **** i {}, all props {}".format(i, props))
                    # Check deprel
                    if Sentence.get_clist_field(props, 'deprel') is None:
#                    if props[7][1] is None:
                        if headi >= 0:
                            print("** Two heads for {}!".format(segmentation))
                        headi = i + morphid
                        pdict['misc'] = i
                for i, props in enumerate(segmentation):
                    props = props.copy()
#                    print("     **** props {}".format(props))
                    upos = props[3][1]
                    if upos in Sentence.selectpos:
                        self.complexity['ambig'] += 1
                        self.posambig.append(word)
                    Sentence.set_clist_field(props, 'id', id)
#                    props[0][1] = id
                    # Set the head id for dependent morphemes
                    if (headincr := Sentence.get_clist_field(props, 'head')): #props[-2][1]):
                        Sentence.set_clist_field(props, 'head', i + headincr + morphid)
#                        props[6][1] = i + headincr + morphid
                    elif id != headi:
                        Sentence.set_clist_field(props, 'head', headi)
#                        props[6][1] = headi
#                    print("      ***** head {}".format(props[6]))
#                    props.extend([('deps', None), ('misc', None)])
                    # get rid of the word features
                    Sentence.set_clist_field(props, 'misc', None)
                    pdict = dict(props)
                    segments.append(pdict)
                    if conllu and index == 0:
                        tokens.append(Token(pdict))
                    id += 1
            segment_list.append(segments)
#                if conllu and index == 0:
#                    return tokens
#        print("*** segment_list")
#        print(segment_list)
        self.words.append(segment_list)
        if conllu:
            return tokens

    ### Graphical representation of segmentations

    def show_segmentation(self, segmentation, featlevel=1, v5=False):
        '''
        Returns a string representing the segmentation with a line for each dependency,
        for forms, for POS tags, and for features.
        '''
        forms = Sentence.get_forms(segmentation)
        nforms = len(forms)
        # Hack to handle problem of fidel width
#        forms = ["{{:_^{}}}".format(Sentence.pad_geez(form)).format(form) for form in forms]
#        forms = ['_' + form + '_' for form in forms]
        pos = Sentence.get_pos(segmentation)
        features = Sentence.get_features(segmentation, None)
        headindex = Sentence.get_headindex(segmentation, v5=v5)
        centers = Sentence.get_centers(nforms)
        string = len(forms) * "{{:^{}}}".format(Sentence.colwidth)
        formstring = string.format(*forms)
        posstring = string.format(*pos)
        featstring = string.format(*features)
        return "{}\n{}\n{}".format(formstring, posstring, featstring)

    @staticmethod
    def show_dep(label, start, end, left=True):
        width = end-start
        if left:
            return start * ' ' + "<{{:-^{}}}*".format(width).format(label)
        return start * ' ' + "*{{:-^{}}}>".format(width).format(label)

    @staticmethod
    def get_centers(nmorphs):
        start = Sentence.colwidth // 2
        return [(start + i * Sentence.colwidth) for i in range(nmorphs)]

    ### Access functions in pseudo-CoNLL-U

    @staticmethod
    def get_forms(segmentation):
        if len(segmentation) == 1:
            return [Sentence.get_word(segmentation)]
        return [s.get('form') for s in segmentation[1:]]

    @staticmethod
    def get_lemmas(segmentation, forms, headindex):
        '''
        The lemmas in a segmentation if any is different from the form.
        '''
        if len(segmentation) == 1:
            lemma = segmentation[0].get('lemma')
            if not lemma:
                return []
            if lemma != forms[0]:
                return [lemma]
            return []
        else:
            lemmas = [s.get('lemma') for s in segmentation[1:]]
            # Only show lemmas if they're different from form, but always show the head lemma
            lm = []
            for i, (l, f) in enumerate(zip(lemmas, forms)):
                if i == headindex or l != f:
                    lm.append(l)
                else:
                    lm.append('')
            lemmas = lm
#            lemmas = [('' if l == f else l) for l, f in zip(lemmas, forms)]
            if not any(lemmas):
                return []
            else:
                return lemmas

    @staticmethod
    def get_glosses(segmentation):
        '''
        The glosses if any (possible only for the head).
        '''
        if len(segmentation) == 1:
            return []
        glosses = [s.get('misc') for s in segmentation]
        if not any(glosses):
            return []
        glosses = [(g if (g and "Gloss" in g) else '') for g in glosses]
        if not any(glosses):
            return []
        return glosses

    @staticmethod
    def get_word(segmentation):
        '''
        The form for the whole word.
        '''
        return segmentation[0].get('form')

    @staticmethod
    def get_headindex(segmentation, v5=False):
        '''
        Index of the morpheme that's the head.
        All dependencies start here.
        '''
        seg0 = segmentation[0]
#        print("  ** get_headindex seg0 {}; {}; {}".format(seg0, type(seg0), seg0.analysis))
        if v5:
            return seg0.analysis.get('head')
        return segmentation[0].get('misc')

    @staticmethod
    def get_dependencies(segmentation, v5=False):
        '''
        Return a list of lists of leftward and rightward dependencies.
        '''
        if len(segmentation) == 1:
            return None
#        print("** get dependencies; segmentation: {}, v5 {}".format(segmentation, v5))
        headindex = Sentence.get_headindex(segmentation, v5=v5)
#        print("  ** headindex {}".format(headindex))
        if headindex is not None:
            headid = segmentation[1:][headindex].get('id')
#            print("  ** headid {}".format(headid))
            idiff = headid - headindex
            dependencies = [(s.get('deprel', ''), i, s.get('head', '') - idiff) for i, s in enumerate(segmentation[1:]) if i != headindex]
            dependencies = [d for d in dependencies if d[1] != d[2]]
#            print("  ** dependencies {}".format(dependencies))
            left = []
            right = []
            for dependency in dependencies:
                source, dest = dependency[2], dependency[1]
#                print("    *** dependency src {}, dest {}, headindex {}".format(source, dest, headindex))
                if source >= headindex and dest >= headindex:
                    right.append(dependency)
                elif source <= headindex and dest <= headindex:
                    left.append(dependency)
            if left or right:
                return left, right

    @staticmethod
    def get_pos(segmentation):
        def get_pos1(morpheme):
            u, x = morpheme.get('upos'), morpheme.get('xpos')
            if u != x:
                u = ','.join([u, x])
            return u
        if len(segmentation) == 1:
            # Word with no segmentation
            return [get_pos1(segmentation[0])]
        return [get_pos1(s) for s in segmentation[1:]]

    @staticmethod
    def get_features(segmentation, um, expand_ambig=True):
        def get1(seg):
            feats = seg.get('feats', None)
            if feats:
                feats = feats.split('|')
                unamb = []
                amb = []
                for ff in feats:
                    if ff[0] == '&':
                        # Ambiguous feature, like &Acc3SMDef
#                        print("** get features, ambig {}, ".format(ff))
                        if expand_ambig:
                            ff = um.expand_feat(ff)
                            ff = ff.split('/')
                            ff = [a.replace(',', '\n') for a in ff]
                        print("&& ambiguous feature expanded to {}".format(ff))
                        amb.append(ff)
#                            amb = [a.split(',') for a in amb]
                    else:
                        unamb.append(ff)
                return unamb, amb
            return None, None
            
        if len(segmentation) == 1:
            feats = [get1(segmentation[0])]
        else:
            feats = [get1(morpheme) for morpheme in segmentation[1:]]
        if any(feats):
#            print("&& get_features {}".format(feats))
            return feats
        return []

### XML stuff; later incorporate this into the Sentence class

def make_caco():
    '''
    Create the XML tree for a CACO document.
    '''
    root = ET.Element('cacoDoc')
    tree = ET.ElementTree(root)
    title = ET.SubElement(root, 'title')
    title.text = "Contemporary Amharic Corpus (CACO) - Version 2.0"
    return tree

def make_caco_word(word, segmentations, multseg=True):
    '''
    Create an XML Element for word with props dict.
    '''
    if not segmentations:
        e = ET.Element('w')
    elif not multseg:
        e = ET.Element('w', segmentations[0])
    else:
        e = ET.Element('w')
        for segmentation in segmentations:
            # segmentation is a dict with 'morphemes' and 'lemma'
            seg = ET.SubElement(e, 'seg', segmentation)
    e.text = word
    return e

def add_caco_sentence(root):
    return ET.SubElement(root, 's')

def add_caco_word(sentence, word, segmentations, multseg=True):
    w = make_caco_word(word, segmentations, multseg=multseg)
    sentence.append(w)

def make_caco_sentence(sentence, multseg=True):
    '''
    Make an XML Element from a sentence, a list of word, segmentation pairs.
    '''
    s = ET.Element('s')
    for word, segmentations in sentence:
        w = make_caco_word(word, segmentations, multseg=multseg)
        s.append(w)
    return s
    
