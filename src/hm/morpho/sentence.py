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

    def reject(self, max_unk=0.3, max_ambig=1.0):
        """
        Should we reject this sentence, based on its complexity?
        """
        complexity = self.complexity
        npunct = complexity['punct']
        if npunct > 0 or complexity['ambig'] > max_ambig or complexity['unk'] > max_unk:
            return True
        return False

    def add_word(self, word, segmentations, morphid, conllu=True):
        w = self.make_word(word, segmentations, morphid, conllu=conllu)
        if conllu:
            self.conllu.extend(w)
#            self.add_conllu_word(word, segmentations, morphid)

#    def add_conllu_word(self, word, segmentations, morphid):
#        w = self.make_conllu_word(word, segmentations, morphid)
#        self.conllu.extend(w)

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
#            print("*** Segmentation {}, length {}".format(segmentation, nmorphs))
            if nmorphs == 1:
                # The word has only one morpheme
                props = segmentation[0].copy()
                props[0][1] = morphid
                upos = props[3][1]
                if upos == 'UNK':
                    self.complexity['unk'] += 1
                elif upos == 'PUNCT':
                    self.complexity['punct'] += 1
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
                for props in segmentation:
                    props = props.copy()
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
        self.words.append(segment_list)
        if conllu:
            return tokens

#def dict2element(tag, d):
#    elem = ET.Element(tag, d)
##    for key, val in d.items():
##        child = ET.SubElement(elem, key)
##        child.text = str(val)
#    return elem

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
    
