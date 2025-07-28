"""
This file is part of HornMorpho, which is part of the PLoGS project.

    <http://homes.soic.indiana.edu/gasser/plogs.html>

    Copyleft 2022-2025.
    PLoGS and Michael Gasser <gasser@iu.edu>.

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
Author: Michael Gasser <gasser@iu.edu>

Corpora of sentences, raw and segmented.
"""

import os, re, sys
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
NUMERAL_RE = re.compile(r'(\w*?)(\d+(?:[\d,]*)(?:\.\d+)?)(\w*?)')

class Corpus():
    """
    A list of sentences, either from a list (data) or a file (path),
    possibly segmented and disambiguated.
    """

    ID = 0

    def __init__(self, data=None, path='',
                 start=0, n_sents=1000, max_sents=5000, start_sent=0,
                 name='', batch_name='', sentid=0,
                 analyze=False, language='', 
                 um=1, seglevel=2, nsegment=True, fsts=None,
                 constraints=None, local_cache=None, timeit=False,
                 v5=True,
                 sep_feats=True, gemination=False, sep_senses=False, degem=True,
                 combine_segs=True, unsegment=False,
                 props=None, pos=None, skip_mwe=True, skip=None,
                 report_freq=250,
                 ## only look for these roots and POS
                 feats=None,
                 ## ambiguity
                 # dict of ambiguous entries (after CG disambiguation, before manual disambiguation)
                 ambig=None,
                 # whether to do manual disambiguation
                 disambiguate=False,
                 # whether to do (automatic) CG disambiguation
                 CGdisambiguate = False,
                 # shortcut for CGdisambiguate
                 cg = False,
                 # Number of analyses eliminated using CG disambiguator.
                 disambiguations = 0,
                 # we may want to save unknown and/or ambiguous tokens
                 unk=None,
                 # a previous corpus to start from (local_cache and last_line)
                 corpus=None,
                 # whether there are (or may be) comment lines
                 comments=True,
                 # how to treat comments in the corpus; if True convert to CoNNL-U metadata following sentence
                 comments2meta=True,
                 # if non-negative, only analyze sentences with this position relative to last comment line
                 language_pos=-1,
                 print_sentence=False,
                 # Use CG rules, if available, to do some word-to-word annotation
                 annotate=False,
                 # version of .lg and .um files to use
                 morph_version=0,
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
        self.start = start
        # Unknown tokens
        self.unk = {}
        # Ambiguous tokens
        self.ambig = {}
        # Number of disambiguations
        self.disambiguations = disambiguations
        # Number of automatically annotated relations
        self.nrelations = 0
        # Number of automatically annotated unlabeled dependencies
        self.ndependencies = 0
        # Cache for storing segmentations
        if isinstance(local_cache, dict):
            self.local_cache = local_cache
        elif corpus:
            self.local_cache = corpus.local_cache
        else:
            self.local_cache = {}
        # Start from the end of the previous corpus if there is one
        if corpus:
            start = corpus.last_line
            self.start = start
            print("Starting from last line of previous corpus {}: {}".format(corpus, start))
        # Max number of words in sentence objects
        self.max_words = 1
        # Index of last line in file
        self.last_line = 0
        filter_cache = [[],[]]
        if not data and path:
            self.data = []
            try:
                filein = open(path, 'r', encoding='utf-8')
                all_lines = filein.readlines()
                lines = Corpus.get_corpus_lines(all_lines, start, n_sents, language_pos, comments, save_comments=comments2meta)
#                lines = filein.readlines()[start:start+max_sents]
                nlines = len(lines)
#                print("$$ file {}, nlines {}".format(filein, nlines))
                sentcount = 0
                skipped = 0
#                sentid = sentid + 1
                linepos = 0
                if segment:
                    if gramfilt:
                        print("Filtering sentences with grammar filter {}".format(gramfilt))
                        gramfilt = EES.get_filter(gramfilt)
                time0 = time.time()
                comment = ''
                label = ''
                meta = ''
                # current position within language list
                langpos = 0
                while sentcount < n_sents and linepos < nlines:
                    line = lines[linepos]
                    line = line.strip()
                    # Check if this is an empty line
                    if not line:
#                        print("Empty line")
                        linepos += 1
                        continue
                    # Check if this is a comment line
                    if line[0] == '#':
#                        print("{} is a comment line".format(line))
                        comment = line
                        langpos = 0
                        if comments2meta:
                            meta = comment
                        else:
                            label = line[1:].strip()
                        linepos += 1
                        continue
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
                        if start_sent and skipped < start_sent:
                            # Just skip the sentence since it's before the start sentence.
#                            print("Skipping sentence {}".format(skipped))
                            skipped += 1
                            continue
                        if start_sent and skipped == start_sent:
                            print("Skipped {} sentences".format(skipped))
                            skipped += 1
#                        if language_pos > -1 and langpos != language_pos:
#                            # Skip this sentence; it's not the right language
#                            langpos += 1
#                            continue
                        if v5:
                            if print_sentence:
                                print("$$ {}".format(line))
                            if sentcount and sentcount % report_freq == 0:
                                print("Analyzed {} sentences".format(sentcount))
                            if sentence_obj := \
                              self.anal_sentence(line, sentid=sentid, gemination=gemination, sep_senses=sep_senses, props=props,
                                                 skip_mwe=skip_mwe, skip=skip, cache=self.local_cache, meta=meta,
                                                 unsegment=unsegment, combine_segs=combine_segs, label=label,
                                                 CGdisambiguate=CGdisambiguate or cg, feats=feats,
                                                 batch_name=batch_name, pos=pos, verbosity=verbosity):
                                self.data.append(line)
                                if unk := sentence_obj.unk:
                                    for u in unk:
                                        if u in self.unk:
                                            self.unk[u] += 1
                                        else:
                                            self.unk[u] = 1
                                if ambig := sentence_obj.morphambig:
                                    for a in ambig:
                                        if len(a) == 1:
#                                            print("{} has only one analysis!".format(a.name))
                                            continue
                                        if a.name not in self.ambig:
                                            self.ambig[a.name] = [a, 1]
                                        else:
                                            self.ambig[a.name][1] += 1
                                sentcount += 1
                                sentid += 1
                                langpos += 1
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
                    print("Took {} seconds to segment {} sentences.".format(round(time.time() - time0), len(self.sentences)))
                self.last_line = start + linepos
                print("Last sentence line: {}".format(self.last_line))
            except IOError:
                print("There is no such file as {} (or it can't be opened); try another one!".format(path))
        elif data:
            # Raw sentences, but they may include comments
            self.data = data
            if v5 and segment:
                self.analyze(sep_feats=sep_feats, gemination=gemination, sep_senses=sep_senses,
                              cache=self.local_cache, unsegment=unsegment, comments2meta=comments2meta,
                              verbosity=verbosity, combine_segs=combine_segs, feats=feats,
                              props=props, skip_mwe=skip_mwe, pos=pos, skip=skip)
        else:
            self.data = []
#        if segment:
#            self.segment(timeit=timeit, filter=gramfilt, um=um, seglevel=seglevel, verbosity=verbosity)

    def __repr__(self):
        return "C_{}".format(self.name)

    ## Version 5 methods

    @staticmethod
    def get_corpus_lines(lines, start, n_sents, lang_pos, comments=True, save_comments=True):
        '''
        Given all the lines in a corpus, return those specified by bounds and language.
        (Later this should take the file object rather than the lines for more efficiency.)
        '''
#        print("** get_corpus_lines {}".format(lang_pos))
        if start > len(lines):
            return []
        elif lang_pos < 0 and not comments:
            # All of the sentences between start and start+n_sents
            return lines[start:start+n_sents]
        result = []
        position = 0
        rel_pos = 0
        started = False
        n = 0
        for line in lines:
            if position >= start and not started:
                started = True
            elif n >= n_sents:
                return result
            line = line.strip()
            if line[0] == '#':
                if save_comments and started:
                    result.append(line)
                rel_pos = 0
            elif lang_pos < 0 or rel_pos == lang_pos:
                if started:
                    result.append(line)
                    n += 1
                position += 1
                rel_pos += 1
            else:
                rel_pos += 1
        return result

    @staticmethod
    def create_seg_corpus(sentences, disambiguate=True):
        '''
        Create a Corpus of already segmented sentences
        '''
        return Corpus(data=sentences, segment=False, disambiguate=disambiguate)

    def anal_sentence(self, sentence, **kwargs):
        """
        Analyze one sentence.
        """
        if kwargs.get('verbosity', 0):
            print("Analyzing {}; meta {}".format(sentence, kwargs['meta']))
        sentence_obj = self.language.anal_sentence(sentence, **kwargs)
        if sentence_obj:
            self.sentences.append(sentence_obj)
            self.max_words = max([self.max_words, len(sentence_obj.words)])
#            print("** sentence words {}".format(sentence_obj.words))
            sentence_obj.postproc()
            if kwargs.get('CGdisambiguate', True) or kwargs.get('cg', True):
                # CG disambiguation
                disambiguated = self.language.disambiguate(sentence_obj, verbosity=kwargs.get('verbosity'))
                if disambiguated:
                    # disambiguated is a dict:: index:list of reading indices eliminated
                    self.disambiguations += sum([len(d) for d in disambiguated.values()])
            if props := kwargs.get('props'):
                sentence_obj.set_props(props)
#            sentence_obj.merge5(gemination=kwargs.get('gemination'), sep_senses=kwargs.get('sep_senses'))
        return sentence_obj

    def analyze(self, **kwargs):
        """
        Segment all the sentences in self.data.
        % Later have the option of segmenting only some??
        kwargs: timeit=False, gramfilter=None, um=1, seglevel=2, verbosity=0
        """
        print("Analyzing sentences in {}".format(self))
        if kwargs.get('verbosity', 0) > 1:
            print()
        sent_id = 1
        time0 = time.time()
        todelete = []
        meta = ''
        props = kwargs.get('props')
        for sindex, sentence in enumerate(self.data):
#            print("Analyzing {}, meta={}".format(sentence, meta))
            if sentence[0] == '#' and kwargs['comments2meta']:
#                        print("{} is a comment line".format(line))
                meta = sentence
                continue
            if kwargs.get('verbosity', 0):
                print("Segmenting {}".format(sentence))
            # metadata from previous line or default
            if meta:
                kwargs['meta'] = meta
                meta = ''
            else:
                kwargs['meta'] = ''
            sentence_obj = \
              self.language.anal_sentence(sentence, sent_id=sent_id, **kwargs)
            if not sentence_obj:
                # sentence may have been filtered out; delete from data
                print("  Failed grammar filter: {}".format(sentence))
                todelete.append(sindex)
            else:
#                sentence_obj.merge_segmentations()
                self.sentences.append(sentence_obj)
                if unk := sentence_obj.unk:
                    for u in unk:
                        if u in self.unk:
                            self.unk[u] += 1
                        else:
                            self.unk[u] = 1
                self.max_words = max([self.max_words, len(sentence_obj.words)])
                sentence_obj.postproc()
                disambiguated = self.language.disambiguate(sentence_obj, verbosity=kwargs.get('verbosity'))
                if disambiguated:
                    # a dict:: index:list of reading indices eliminated
                    self.disambiguations += sum([len(d) for d in disambiguated.values()])
                if props:
                    sentence_obj.set_props(props)
#                sentence_obj.merge5(gemination=kwargs.get('gemination'), sep_senses=kwargs.get('sep_senses'))
                sent_id += 1
        # Delete sentences that didn't pass the filter
        for delindex in todelete[::-1]:
            del self.data[delindex]
        if kwargs.get('timeit'):
            return print("Took {} seconds to segment {} sentences.".format(round(time.time() - time0), len(self.data)))

    def write(self, **kwargs):
        '''
        Write the contents of the Corpus, either to a file at a specified path or to standard output.
        Assumes analysis has already happened.
        What and where to write is specified in kwargs:
            attribs: list of strings: 'seg', 'lemma', 'pos', 'root'
            conllu: boolean, if True write CoNLL-U representations, ignoring attribs
            path: string or None
        '''
        path = kwargs.get('path')
        if path:
            try:
                file = open(path, 'w', encoding='utf8')
            except FileNotFoundError:
                print("Something is wrong with path {}; the file can't be opened!".format(path))
        else:
            file = sys.stdout
        attribs = kwargs.get('attribs', [])
        all_anals = kwargs.get('all_anals', False)
        # By default DON'T write CoNNLL-U representations
        conllu = kwargs.get('conllu', False)
        for index, sentence in enumerate(self.sentences):
            string = ''
            if conllu:
                string = sentence.create_conllu(update_ids=True)
#                sentence.print_conllu(update_ids=True, file=file)
            else:
                string = sentence.create_attrib_strings(attribs, all_anals=all_anals)
            print(string, file=file, end='')
            if not conllu and index < len(self.sentences) - 1:
                print(file=file)
        if path:
            file.close()
        
    def write_props(self, file, start=0):
        '''
        Write the props saved in corpus sentences to a file.
        '''
        for sindex, sentence in enumerate(self.sentences):
            count = start + sindex
            print("{} && {}".format(count, sentence.text), file=file)
            for word in sentence.props:
                print(word, file=file)
            print("##", file=file)

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
        Manual disambiguation (following CG disambiguation).
        Show the analyses in the GUI so words with multiple analyses can be disambiguated.
        '''
        if not self.sentences:
            # Segment all sentences before creating GUI.
            self.analyze(timeit=timeit)
#            self.segment(timeit=timeit)
        self.root = SegRoot(self, title=self.__repr__(), seglevel=seglevel, v5=self.v5)
        self.root.mainloop()

    def annotate(self, verbosity=0):
        '''
        Run language's CG dependency (annotation) rules, if any, on disambiguated sentences.
        '''
        if verbosity:
            print("Running annotation rules")
        for sentence in self.sentences:
            sentence.annotate(verbosity=verbosity)
            self.ndependencies += sentence.ndependencies
            self.nrelations += sentence.nrelations

    def write_cache(self, path):
        '''
        Write the current local cache.
        '''
#        filename = "{}_{}".format(self.name, self.last_line)
        with open(path, 'w', encoding='utf8') as file:
            for word, anals in self.local_cache.items():
                print("{}\t{}".format(word, anals.__repr__()), file=file)

    def read_cache(self, path, update=False):
        '''
        Read in a cache from a previous run, possibly updating the
        current cache.
        '''
        if not update:
            self.local_cache = {}
        with open(path, encoding='utf8') as file:
            for line in file:
                word, anals = line.split('\t')
                if update:
                    if word in self.local_cache:
                        continue
                anals = eval(anals)
                self.local_cache[word] = anals
            
    ### Old methods

    def segment(self, timeit=False, gramfilter=None, um=1, seglevel=2, verbosity=0):
        """
        Segment all the sentences in self.data.
        % Later have the option of segmenting only some??
        """
        print("Segmenting sentences in {}".format(self))
#        , end='')
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
              self.language.anal_sentence4(sentence, batch_name=self.batch_name, sentid=sentid,
                                          local_cache=self.local_cache, gramfilter=gramfilter,
                                          um=um, seglevel=seglevel)
            if not sentence_obj:
                # sentence may have been filtered out; delete from data
                print("  Failed grammar filter: {}".format(sentence))
                todelete.append(sindex)
            else:
                sentence_obj.merge_segmentations()
                self.sentences.append(sentence_obj)
                self.unk.update(set(sentence_obj.unk))
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
          self.language.anal_sentence4(sentence, batch_name=self.batch_name, sentid=sentid,
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
            self.unk.update(set(sentence_obj.unk))
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
            sentence = language.anal_sentence4(text, local_cache=self.local_cache, um=um, seglevel=seglevel)
            if sentence:
                self.all_sentences[sentindex] = sentence
        if sentence:
            self.root.segmentations = sentence.words
        return sentence

    def write4(self, conllu=False, filename='', data_folder=CACO_DIR, conllu_folder=CONLLU_DIR, append=False):
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
