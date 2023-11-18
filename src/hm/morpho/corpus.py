"""
This file is part of HornMorpho, which is part of the PLoGS project.

    <http://homes.soic.indiana.edu/gasser/plogs.html>

    Copyleft 2022, 2023.
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

import os, re
from .languages import *
from tkinter import *
from tkinter.ttk import *
from tkinter.font import *
import time
from .gui import *

# Note: these directories will probably be different for each user!
CACO_DIR = os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir, os.path.pardir, os.path.pardir, 'TAFS', 'datasets', 'CACO')
CONLLU_DIR = os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir, os.path.pardir, os.path.pardir, 'TAFS', 'segmentations')

PUNCTUATION = "“‘”’'…–—:;/,<>?.!%$()[]{}|#@&*_+=\"፡።፣፤፥፦፧፨"
NUMERAL_RE = re.compile('(\w*?)(\d+(?:[\d,]*)(?:\.\d+)?)(\w*?)')

class Corpus():
    """
    List of tokenized sentences to be segmented and displayed.
    """

    ID = 0

    def __init__(self, data=None, path='', start=0, n_sents=100, max_sents=1000,
                 name='', batch_name='', sentid=0, analyze=False, language='', 
                 um=1, seglevel=2, segment=True, fsts=None, disambiguate=False,
                 constraints=None, local_cache=None, timeit=False,
                 v5=False, sep_feats=True, gemination=False,
                 verbosity=0):
        self.batch_name = batch_name
        minlen = constraints and constraints.get('minlen', 0)
        maxlen = constraints and constraints.get('maxlen', None)
        maxnum = constraints and constraints.get('maxnum', None)
        maxpunc = constraints and constraints.get('maxpunc', None)
        endpunc = constraints and constraints.get('endpunc', False)
        maxunk = constraints and constraints.get('maxunk', 10)
        maxtoks = constraints and constraints.get('maxtoks', 30)
        gramfilt = constraints and constraints.get('grammar', None)
        self.v5 = v5
        # Sentence objects, with pre-CoNLL-U word representations
        self.sentences = []
        self.language = language or get_language('amh', phon=False, segment=True, experimental=True)
        self.name = name or batch_name or self.create_name()
        # Unknown tokens
        self.unks = set()
        # Cache for storing segmentations
        self.local_cache = local_cache if isinstance(local_cache, dict) else {}
        # Cache for storing grammatical filtered words
        # Max number of words in sentence objects
        self.max_words = 1
        # Index of last line in file
        self.last_line = 0
        filter_cache = [[],[]]
        if not data and path:
            self.data = []
            try:
                filein = open(path, 'r', encoding='utf-8')
                lines = filein.readlines()[start:start+max_sents]
                nlines = len(lines)
#                print("$$ file {}, nlines {}".format(filein, nlines))
                sentcount = 0
                sentid = sentid + 1
                linepos = 0
                if segment:
                    if gramfilt:
                        print("Filtering sentences with grammar filter {}".format(gramfilt))
                        gramfilt = EES.get_filter(gramfilt)
                time0 = time.time()
                while sentcount < n_sents and linepos < nlines:
                    line = lines[linepos]
                    line = line.strip()
                    print("  $$ {}".format(line))
                    if linepos and linepos % 25 == 0:
                        print("Checked {} sentences, included {}".format(linepos, len(self.data)))
                    linepos += 1
                    if constraints: # and maxnum != None or maxpunc != None:
                        tokens = line.split()
                        # todo: implement number, length, punctuation constraints
                        if len(tokens) > maxtoks:
                            print("  Too many tokens: {}".format(line[:100]))
                            continue
                        if maxpunc != None:
                            if Corpus.count_punc(tokens) > maxpunc:
                                print("  Too many punctuation marks: {}".format(line[:100]))
                                continue
                        if endpunc:
                            if tokens[-1] not in PUNCTUATION:
                                print("  No end punctuation: {}".format(line[:100]))
                                continue
                        if maxnum != None:
                            if Corpus.count_num(tokens) > maxnum:
                                print("  Too many numerals: {}".format(line[:100]))
                                continue
                    if segment:
                        if v5:
                            sentence_obj = self.seg_sentence5(line, sentid=sentid, gemination=gemination, verbosity=verbosity)
                            if sentence_obj:
                                self.data.append(line)
                                sentcount += 1
                                sentid += 1
                        elif (sentence_obj := \
                                self._segment(line, sentid, gramfilt=gramfilt, maxunk=maxunk,
                                              analyze=analyze,
                                              um=um, seglevel=seglevel, filter_cache=filter_cache,
                                              fsts=fsts, verbosity=verbosity)):
                            if gramfilt:
                                print("  ACCEPTED SENTENCE {}: {}".format(sentid, line))
                            self.data.append(line)
                            sentcount += 1
                            sentid += 1
                    else:
                        self.data.append(line)
                if timeit:
                    return print("Took {} seconds to segment {} sentences.".format(round(time.time() - time0), len(self.sentences)))
                self.last_line = start + linepos
                print("Last sentence line: {}".format(self.last_line))
            except IOError:
                print('No such file: {}; try another one.'.format(path))
        elif data:
            # Raw sentences
            self.data = data
            if v5 and segment:
                self.segment5(sep_feats=sep_feats, gemination=gemination)
        else:
            self.data = []
#        if segment:
#            self.segment(timeit=timeit, filter=gramfilt, um=um, seglevel=seglevel, verbosity=verbosity)

    def __repr__(self):
        return "C_{}".format(self.name)

    ## Version 5 methods

    def seg_sentence5(self, sentence, **kwargs):
        """
        Segment one sentence.
        """
        if kwargs.get('verbosity', 0):
            print("Segmenting {}".format(sentence))
        sentence_obj = self.language.anal_sentence5(sentence, **kwargs)
        if sentence_obj:
            self.sentences.append(sentence_obj)
            self.unks.update(set(sentence_obj.unk))
            self.max_words = max([self.max_words, len(sentence_obj.words)])
            sentence_obj.merge5()
        return sentence_obj

    def segment5(self, **kwargs):
        """
        Segment all the sentences in self.data.
        % Later have the option of segmenting only some??
        kwargs: timeit=False, gramfilter=None, um=1, seglevel=2, verbosity=0
        """
        print("** Segmenting sentences in {}".format(self), end='')
#        if gramfilter:
#            print(" with filter {}".format(gramfilter))
#        else:
#            print()
#        if gramfilter and isinstance(gramfilter, str):
#            gramfilter = EES.get_filter(gramfilter)
        sent_id = 1
        time0 = time.time()
        todelete = []
        for sindex, sentence in enumerate(self.data):
            if kwargs.get('verbosity', 0):
                print("Segmenting {}".format(sentence))
            sentence_obj = \
              self.language.anal_sentence5(sentence, sent_id=sent_id, **kwargs)
#            batch_name=self.batch_name, sentid=sentid,
#                                          local_cache=self.local_cache, gramfilter=gramfilter,
#                                          um=um, seglevel=seglevel)
            if not sentence_obj:
                # sentence may have been filtered out; delete from data
                print("  Failed grammar filter: {}".format(sentence))
                todelete.append(sindex)
            else:
#                sentence_obj.merge_segmentations()
                self.sentences.append(sentence_obj)
                self.unks.update(set(sentence_obj.unk))
                self.max_words = max([self.max_words, len(sentence_obj.words)])
                sentence_obj.merge5()
                sent_id += 1
        # Delete sentences that didn't pass the filter
        for delindex in todelete[::-1]:
            del self.data[delindex]
        if kwargs.get('timeit'):
            return print("Took {} seconds to segment {} sentences.".format(round(time.time() - time0), len(self.data)))

    def create_name(self):
        name = "{}".format(Corpus.ID)
        Corpus.ID += 1
        return name

    @staticmethod
    def count_punc(sentence):
        """
        Number of punctuation characters in sentence (list of strings).
        """
        return len([w for w in sentence if w in PUNCTUATION])

    @staticmethod
    def count_num(sentence):
        """
        Number of tokens in sentence (list of strings) that contain numerals.
        """
        return len([w for w in sentence if NUMERAL_RE.fullmatch(w)])

    def disambiguate(self, skip_unambig=True, seglevel=2, timeit=False, verbosity=0):
        '''
        Show the segmentations in the GUI so words with multiple
        segmentations can be disambiguated.
        '''
        if not self.sentences:
            # Segment all sentences before creating GUI.
            self.segment(timeit=timeit)
        self.root = SegRoot(self, title=self.__repr__(), seglevel=seglevel, v5=self.v5)
        self.root.mainloop()

    def segment(self, timeit=False, gramfilter=None, um=1, seglevel=2, verbosity=0):
        """
        Segment all the sentences in self.data.
        % Later have the option of segmenting only some??
        """
        print("Segmenting sentences in {}".format(self), end='')
        if gramfilter:
            print(" with filter {}".format(gramfilter))
        else:
            print()
        if gramfilter and isinstance(gramfilter, str):
            gramfilter = EES.get_filter(gramfilter)
        sentid = 1
        time0 = time.time()
        todelete = []
        for sindex, sentence in enumerate(self.data):
            if verbosity:
                print("Segmenting {}".format(sentence))
            sentence_obj = \
              self.language.anal_sentence(sentence, batch_name=self.batch_name, sentid=sentid,
                                          local_cache=self.local_cache, gramfilter=gramfilter,
                                          um=um, seglevel=seglevel)
            if not sentence_obj:
                # sentence may have been filtered out; delete from data
                print("  Failed grammar filter: {}".format(sentence))
                todelete.append(sindex)
            else:
                sentence_obj.merge_segmentations()
                self.sentences.append(sentence_obj)
                self.unks.update(set(sentence_obj.unk))
                self.max_words = max([self.max_words, len(sentence_obj.words)])
                sentid += 1
        # Delete sentences that didn't pass the filter
        for delindex in todelete[::-1]:
            del self.data[delindex]
        if timeit:
            return print("Took {} seconds to segment {} sentences.".format(round(time.time() - time0), len(self.data)))

    def _segment(self, sentence, sentid, analyze=False,
                 gramfilt=None, um=1, seglevel=2, maxunk=5, filter_cache=None, fsts=None, verbosity=0):
        '''
        Segment one sentence, applying gramfilter if any and checking if max unk words is exceeded.
        '''
        conllu = False if analyze else True
        segment = False if analyze else True
        experimental = False if analyze else True
        seglevel = 0 if analyze else seglevel
        um = 2 if analyze else um

        sentence_obj = \
          self.language.anal_sentence(sentence, batch_name=self.batch_name, sentid=sentid,
                                      local_cache=self.local_cache, gramfilter=gramfilt, fsts=fsts,
                                      filter_cache=filter_cache,
                                      um=um, seglevel=seglevel, conllu=conllu, segment=segment, experimental=experimental,
                                      verbosity=verbosity)
        if not sentence_obj:
            # sentence may have been filtered out; delete from data
            print("  Grammatical filter rejected: {}".format(sentence[:100]))
            return
        else:
            if maxunk and len(sentence_obj.unk) > maxunk:
                print("  Too many unknown tokens: {}".format(sentence[:100]))
                return
            if not analyze:
                sentence_obj.merge_segmentations()
            self.sentences.append(sentence_obj)
            self.unks.update(set(sentence_obj.unk))
            self.max_words = max([self.max_words, len(sentence_obj.words)])
            return sentence_obj

    def conlluify(self, degeminate=False, geminate=True, verbosity=0):
        """
        Convert all of the sentence pre-CoNNL-U representations to CoNNL-U.
        """
        print("Conlluifying sentences in {}".format(self))
        for sentence in self.sentences:
            sentence.words2conllu(update_indices=True, degem=degeminate, gem=geminate)

    def segment1(self, text='', sentindex=None, um=1, seglevel=2):
        """
        Segment one sentence.
        """
        text = text or self.data[sentindex] if sentindex < len(self.data) else None
        if text:
            language = get_language('amh', phon=False, segment=True, experimental=True)
            sentence = language.anal_sentence(text, local_cache=self.local_cache, um=um, seglevel=seglevel)
            if sentence:
                self.all_sentences[sentindex] = sentence
        if sentence:
            self.root.segmentations = sentence.words
        return sentence

    def write(self, conllu=False, filename='', data_folder=CACO_DIR, conllu_folder=CONLLU_DIR, append=False):
        '''
        Write the data in the corpus to a file, by default in the TAFS/datasets/CACO folder,
        appending it to an existing file if append is True.
        If conllu is True, also write the sentence CoNLL-U representations to a file, by default
        in the TAFS/connlu folder.
        '''
        if filename:
            path = os.path.join(data_folder, filename)
        else:
            path = os.path.join(data_folder, self.name + '.txt')
        with open(path, 'a' if append else 'w', encoding='utf8') as file:
            for sentence in self.data:
                print(sentence, file=file)
