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

Integrating HornMorpho with the updated CACO corpus.
"""

import xml.etree.ElementTree as ET
import os

CACO_DIR = os.path.join(os.path.dirname(__file__), os.path.pardir, 'ext_data', 'CACO')

def caco_path(version, file):
    return os.path.join(CACO_DIR, "CACO{}".format(version), file)

#def dict2element(tag, d):
#    elem = ET.Element(tag, d)
##    for key, val in d.items():
##        child = ET.SubElement(elem, key)
##        child.text = str(val)
#    return elem

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
    if not multseg:
        e = dict2element('w', segmentations[0])
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
    
