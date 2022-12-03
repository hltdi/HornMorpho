"""
This file is part of HornMorpho, which is part of the PLoGS project.

    <http://homes.soic.indiana.edu/gasser/plogs.html>

    Copyleft 2022.
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
from conllu import parse, TokenList, Token
import os

CACO_DIR = os.path.join(os.path.dirname(__file__), os.path.pardir, 'ext_data', 'CACO')
TB_DIR = os.path.join(os.path.dirname(__file__), os.path.pardir, 'ext_data', 'AmhTreebank')
DATA_PATH = os.path.join(os.path.dirname(__file__), os.path.pardir, 'ext_data', 'CACO', 'CACO1.1', "CACO_TEXT.txt")

def get_caco_data(sort=False, filter_sentences=True, min_length=3, max_length=7, write=False):
    with open(DATA_PATH) as file:
        data = [l.strip().split() for l in file.readlines()]
        if sort:
            data.sort(key=lambda x: len(x))
        if filter_sentences:
            data = [d for d in data if d[-1] in ('።?!') and min_length <= len(d) <= max_length]
        data = [' '.join(d) for d in data]
        if write:
            with open(os.path.join(CACO_DIR, 'CACO1.1', "CACO_TEXT_{}.txt".format(write)), 'w', encoding='utf8') as file:
                for sentence in data:
                    print(sentence, file=file)
            return
        return data

def tb_path(file="am_att-ud-test.conllu"):
    return os.path.join(TB_DIR, file)

def parse_tb(file="am_att-ud-test.conllu"):
    with open(tb_path(), encoding='utf8') as file:
        return file.read()

def caco_path(version, file):
    return os.path.join(CACO_DIR, "CACO{}".format(version), file)

class Sentence():
    """
    Representation of HM output for a sentence in a corpus.
    """

    selectpos = {'NADJ': ['NOUN', 'ADJ']}

    colwidth = 20

    def __init__(self, text, tokens=[], batch_name='', sentid=0):
        self.tokens = tokens
        self.text = text
        self.ntokens = len(text.split())
        self.words = []
        self.batch_name = batch_name
        self.sentid = sentid
        self.label = "{}_s{}".format(batch_name, sentid)
        self.xml = ''
        self.conllu = TokenList([])
        self.conllu.metadata = {'text': text, 'sent_id': self.label}
        self.complexity = {'ambig': 0, 'unk': 0, 'punct': 0}

    def __repr__(self):
        return "S{}::{}".format(self.sentid, self.text)

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

    def reject(self, unk_thresh=0.3, ambig_thresh=1.0):
        """
        Should we reject this sentence, based on its complexity?
        """
        complexity = self.complexity
        npunct = complexity['punct']
        if npunct > 0 or complexity['ambig'] > ambig_thresh or complexity['unk'] > unk_thresh:
            return True
        return False

    def words2conllu(self, update_indices=True):
        '''
        Convert a pre-CoNLL-U list of lists of dicts to a list of Tokens.
        '''
        # Use only the first segmentation for each word
        wordsegs = [w[0] for w in self.words]
        # Update the indices in case the number of morphemes in a word has changed
        index = 1
        conllu = []
        for wordseg in wordsegs:
#            print("** Wordseg {}".format(wordseg))
            if len(wordseg) == 1:
                # No segments: use current index
                wordseg[0]['id'] = index
                conllu.append(wordseg[0])
                index += 1
            else:
                wholeword = wordseg[0]
                morphsegs = wordseg[1:]
                nmorphs = len(morphsegs)
                end = index + nmorphs
                headindex = index
                wholeword['id'] = (index, '-', end-1)
                # Get rid of the index that's stored here
                wholeword['misc'] = None
                conllu.append(wholeword)
                for morphseg in morphsegs:
                    morphseg['id'] = index
                    morphseg['head'] = headindex
                    conllu.append(morphseg)
                    index += 1
        return conllu

    def add_word(self, word, segmentations, morphid, conllu=True):
        w = self.make_word(word, segmentations, morphid, conllu=conllu)
        if conllu:
            self.conllu.extend(w)

    def make_word(self, word, segmentations, morphid, conllu=True):
        '''
        Creates a new word.
        If conllu is True, returns a list of morpheme Tokens.
        '''
        segment_list = []
        tokens = []
        self.complexity['ambig'] += len(segmentations) - 1
#        print("*** word {}, segmentations {}".format(word, segmentations))
        for index, segmentation in enumerate(segmentations):
#        segmentation = segmentations[0]
            segments = []
            nmorphs = len(segmentation)
#            print("  *** Segmentation {}, length {}".format(segmentation, nmorphs))
            if nmorphs == 1:
                # The word has only one morpheme
                props = segmentation[0].copy()
                props[0][1] = morphid
                upos = props[3][1]
                if upos == 'UNK':
                    self.complexity['unk'] += 1
                elif upos == 'PUNCT':
                    self.complexity['punct'] += 1
                elif upos in Sentence.selectpos:
                    # ambiguous POS
                    self.complexity['ambig'] += 1
                props.extend([('deps', None), ('misc', None)])
                pdict = dict(props)
                segments.append(pdict)
                if conllu and index == 0:
                    tokens.append(Token(pdict))
            else:
#                tokens = []
                endid = morphid + nmorphs
                ids = (morphid, '-', endid-1)
                props = [('id', ids), ('form', word), ('lemma', None), ('upos', None), ('xpos', None),
                         ('feats', None), ('head', None), ('deprel', None), ('deps', None), ('misc', None)]
                pdict = dict(props)
                segments.append(pdict)
                if conllu and index == 0:
                    tokens.append(Token(pdict))
                id = morphid
                # Get the index of the head
                headi = -1
                for i, props in enumerate(segmentation):
                    # Check deprel
                    if props[-1][1] is None:
                        if headi >= 0:
                            print("** Two heads for {}!".format(segmentation))
                        headi = i + morphid
                        pdict['misc'] = i
                for props in segmentation:
                    props = props.copy()
                    upos = props[3][1]
                    if upos in Sentence.selectpos:
                        self.complexity['ambig'] += 1
                    props[0][1] = id
                    # Set the head id for dependent morphemes
                    if id != headi:
                        props[-2][1] = headi
                    props.extend([('deps', None), ('misc', None)])
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

    def show_segmentation(self, segmentation):
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
        features = Sentence.get_features(segmentation)
        headindex = Sentence.get_headindex(segmentation)
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
    def get_lemmas(segmentation, forms):
        '''
        The lemmas in a segmentation in any is different from the form.
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
            lemmas = [('' if l == f else l) for l, f in zip(lemmas, forms)]
            if not any(lemmas):
                return []
            else:
                return lemmas

    @staticmethod
    def get_word(segmentation):
        '''
        The form for the whole word.
        '''
        return segmentation[0].get('form')

    @staticmethod
    def get_headindex(segmentation):
        '''
        Index of the morpheme that's the head.
        All dependencies start here.
        '''
        return segmentation[0].get('misc')

    @staticmethod
    def get_dependencies(segmentation):
        '''
        Return a list of lists of leftward and rightward dependencies.
        '''
        headindex = Sentence.get_headindex(segmentation)
        dependencies = [(s.get('deprel', ''), i) for i, s in enumerate(segmentation[1:]) if i != headindex]
        left = []
        right = []
        for dependency in dependencies:
            if dependency[1] < headindex:
                left.append(dependency)
            else:
                right.append(dependency)
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
    def get_features(segmentation):
        if len(segmentation) == 1:
            feats = [Sentence.simplify_feats(segmentation[0].get('feats', None))]
        else:
            feats = [morpheme.get('feats', '') for morpheme in segmentation[1:]]
            feats = [Sentence.simplify_feats(f) for f in feats]
        if any(feats):
            return feats
        return []

    @staticmethod
    def simplify_feats(feats):
        if not feats:
            return None
        feats = feats.split("|")
        feats = [f.split('=') for f in feats]
        feats = [(f[0] if f[1] == 'Yes' else f[1]) for f in feats]
        feats = ','.join(feats)
        return feats

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
    
