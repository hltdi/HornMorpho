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

Corpora of sentences, raw and segmented.
"""
from .languages import *
from tkinter import *
from tkinter.ttk import *
from tkinter.font import *
import time
from .gui import *

class Corpus():
    """
    List of tokenized sentences to be segmented and displayed.
    """

    ID = 0

    def __init__(self, data=None, path='', start=0, n_sents=0, name='', batch_name='',
                 local_cache=None):
        self.batch_name = batch_name
        if not data and path:
            self.data = []
            try:
                filein = open(path, 'r', encoding='utf-8')
                lines = filein.readlines()
                if start or n_sents:
                    lines = lines[start:start+n_sents]
                for line in lines:
                    self.data.append(line.strip())
            except IOError:
                print('No such file: {}; try another one.'.format(path))
        elif data:
            # Raw sentences
            self.data = data
        else:
            self.data = []
        # Sentence objects, with pre-CoNLL-U word representations
        self.sentences = []
        self.language = get_language('amh', phon=False, segment=True, experimental=True)
        self.name = name or batch_name or self.create_name()
        # Unknown tokens
        self.unks = set()
        # Cache for storing segmentations
        self.local_cache = local_cache if isinstance(local_cache, dict) else {}
        # Max number of words in sentence objects
        self.max_words = 1

    def __repr__(self):
        return "C_{}".format(self.name)

    def create_name(self):
        name = "{}".format(Corpus.ID)
        Corpus.ID += 1
        return name

    def disambiguate(self, skip_unambig=True, timeit=False, verbosity=0):
        '''
        Show the segmentations in the GUI so words with multiple
        segmentations can be disambiguated.
        '''
        if not self.sentences:
            # Segment all sentences before creating GUI.
            self.segment(timeit=timeit)
        self.root = SegRoot(self, title=self.__repr__())
        self.root.mainloop()

    def segment(self, timeit=False, verbosity=0):
        """
        Segment all the sentences in self.data.
        % Later have the option of segmenting only some??
        """
        print("Segmenting sentences in {}".format(self))
        sentid = 1
        time0 = time.time()
        for sentence in self.data:
            if verbosity:
                print("Segmenting {}".format(sentence))
            sentence_obj = \
              self.language.anal_sentence(sentence, batch_name=self.batch_name, sentid=sentid, local_cache=self.local_cache)
            self.sentences.append(sentence_obj)
            self.unks.update(set(sentence_obj.unk))
            self.max_words = max([self.max_words, len(sentence_obj.words)])
            sentid += 1
        if timeit:
            return print("Took {} seconds to segment {} sentences.".format(round(time.time() - time0), len(self.data)))

    def conlluify(self, degeminate=False, geminate=True, verbosity=0):
        """
        Convert all of the sentence pre-CoNNL-U representations to CoNNL-U.
        """
        print("Conlluifying sentences in {}".format(self))
        for sentence in self.sentences:
            sentence.words2conllu(update_indices=True, degem=degeminate, gem=geminate)

    def segment1(self, text='', sentindex=None):
        """
        Segment one sentence.
        """
        text = text or self.data[sentindex] if sentindex < len(self.data) else None
        if text:
            language = get_language('amh', phon=False, segment=True, experimental=True)
            sentence = language.anal_sentence(text, local_cache=self.local_cache)
            if sentence:
                self.all_sentences[sentindex] = sentence
        if sentence:
            self.root.segmentations = sentence.words
        return sentence
