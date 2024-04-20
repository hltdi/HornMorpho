"""
This file is part of HornMorpho, which is a project of PLoGS.

Copyleft 2008-2024. Michael Gasser

    HornMorpho is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    HornMorpho is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with HornMorpho.  If not, see <http://www.gnu.org/licenses/>.

Author: Michael Gasser <gasser@indiana.edu>
"""

# Version 5.0 includes many new features, especially languages represented
#   with fidel.  
# Version 4.5 includes the new segmenter for Amharic, accessed with
# seg_word and seg_file with experimental=True (the default setting).
# With conllu=True, the default, the segmentation functions return CoNLL-U
# style representations of sentences, including segmented words.
# Version 4.5.1 includes the disambiguation GUI and the Corpus class.
# Version 4.5.2 allows the segmenter to suppress segmentation but use
# the features of the segments for the whole word.

# experimental CoNLL-U segmenter for Amharic

#__cat__ = 'X'
#__version__ = '4.5.2.4'

#__cat__ = 'A'
#__version__ = '4.3.1'

__cat__ = '+'
__version__ = '5.0'

__author__ = 'Michael Gasser'

from . import morpho

print('\n@@@@ This is HornMorpho{}, version {} @@@@\n'.format(__cat__, __version__))

#print('\n@@@@ Welcome to HornMorpho! @@@@\n')

SEGMENT = False

###
### Version 5 analysis and generation.
###

def anal_corpus(language, **kwargs):
    '''
    Create a corpus of sentences, given a list of raw sentence strings.
    '''
    guess = kwargs.get('guess', False)
    language = morpho.get_language(language, v5=True, guess=guess)
    if language:
        corp = morpho.Corpus(language=language, v5=True, **kwargs)
        if kwargs.get('disambiguate', False):
            corp.disambiguate()
        return corp

def analyze(language, word, **kwargs):
    '''
    Analyze a word or MWE, returning a list of dicts.
    kwargs: mwe=False, degem=True, conllu=True, sep_feats=True, guess=False, combine_segs=False, verbosity=0
    '''
    kwargs['guess'] = kwargs.get('guess', False)
    kwargs['v5'] = True
    language = morpho.get_language(language, **kwargs)
    if language:
        return language.analyze(word, **kwargs)

anal = analyze

def anal_sentence(language, sentence, **kwargs):
    '''
    Analyze the sentence using Language.anal_sentence(), returning a Sentence object.
    '''
    kwargs['guess'] = kwargs.get('guess', False)
    kwargs['v5'] = True
    language = morpho.get_language(language, **kwargs)
    if language:
        if kwargs.get('mwe'):
            return language.anal_sent_mwe(sentence, None, **kwargs)
        return language.anal_sentence(sentence, **kwargs)

def write_conllu(sentences=None, path='', corpus=None, degeminated=False,
                 batch_name='', append=True, v5=True,
                 filter_sents=True, unk_thresh=0.3, ambig_thresh=1.0,
                 verbosity=0):
    '''
    Write the CoNNL-U representations of a list of sentences to a file.

    @param sentences: list of instances of Sentence
    @param path: path to file where the sentences will be written
    @param corpus: instance of Corpus (or None); if sentences is None, use corpus.sentences
    @param v5: whether this is HM version 5.
    @param degeminated: whether to write the degeminated sentences
    @param batch_name: name of batch of data
    @param version: version of input data (used to create batch_name if not provided)
    @param batch_name: string name for batch (not sure this is needed)
    @param append: whether to append sentences to file
    @param filter_sents: whether to filter sentences based on UNK tokes and ambiguity.
    @param unk_thresh: float representing maximum proportion of UNK tokens in sentence
    @param ambig_thresh: float representing maximum average number of additional segmentations for tokens.
    @param verbosity: int indicating how verbose messages should be
    '''
    sentences = sentences or corpus.sentences
    if path:
        file = open(path, 'a' if append else 'w', encoding='utf8')
        print("Writing CoNLL-U sentences {} to {}".format((corpus.__repr__() if corpus else ''), path))
    else:
        file = morpho.sys.stdout
    nrejected = 0
    rejected = []
    for index, sentence in enumerate(sentences):
        if filter_sents and sentence.reject(ambig_thresh=ambig_thresh, unk_thresh=unk_thresh, verbosity=verbosity):
            nrejected += 1
            rejected.append(sentence.sentid)
            continue
        if v5:
            sentence.print_conllu(update_ids=True, file=file)
        else:
            conll = sentence.alt_conllu if degeminated else sentence.conllu
            print(conll.serialize(), file=file, end='')
    if rejected:
        print("Rejected sentences {}".format(','.join([str(r) for r in rejected])))

def exit(save=True, cache=''):
    """Exit the program, caching any new analyses for each loaded language
    if save is True."""
    print("Quitting...")
    global SEGMENT
    if not save:
        really_save = input("Are you sure you want to discard new anaylses?\n[Y]es/[N]o ")
        if really_save and really_save[0].lower() == 'y':
            return
    for abbrev, language in morpho.languages.LANGUAGES.items():
        language.write_cache(segment=SEGMENT)
    morpho.languages.LANGUAGES.clear()

def load_lang(language, phon=False, segment=False, experimental=False, pickle=True, recreate=False,
              load_morph=True, cache='', translate=False, fidel=False, gen=False,
              guess=True, verbose=False):
    """Load a language's morphology.

    @param language: a language label
    """
#    print("** load_lang, load_morph = {}".format(load_morph))
    morpho.load_lang(language, pickle=pickle, recreate=recreate,
                     phon=phon, segment=segment, 
                     translate=translate, experimental=experimental, gen=gen,
                     load_morph=load_morph, cache=cache, fidel=fidel,
                     guess=guess, verbose=verbose)

# Version 4 methods

def seg_word(language, word, nbest=8, raw=False, realize=True, phonetic=False,
             transortho=True, experimental=False, udformat=True,
             mwe=False, conllu=True, verbosity=0):
    '''Segment a single word and print out the results.

    @param language (string): abbreviation for a language
    @param word (string):     word to be analyzed
    @param experimental (boolean):  whether to use the new "experimental" segmenter FST
    @param realize (boolean):  whether to realize individual morphemes (in particular
                     the stem of an Amharic verb or deverbal noun)
    @param transortho (boolean): whether to convert output to non-roman orthography
    @param phonetic (boolean): whether to output phonetic romanization (False by default for seg)
    @param udformat (boolean): whether to convert POS and features to UD format
    @param mwe (boolean): whether to run the FSTs for MWEs; if there is a space in word, set to True
    @param conllu (boolean): whether to return a dict for each morpheme that can be converted to
                     CoNLL-U format
    @return:         analyses (only if raw is True); 
                     list of (POS, segstring, count) triples or
                     a list of strings (if realize is True)
    '''
    # Use old format for old CACO segmenter
    if not experimental:
        udformat = False
        conllu = False
    language = morpho.get_language(language, phon=False, segment=True, experimental=experimental)
#    global SEGMENT
#    SEGMENT = True
    simps = None
    if language:
        mwe = mwe or ' ' in word
        # Process special cases
        analyses = language.preproc_special(word, segment=True)
        if not analyses:
           # Do the preprocessing first in order to save any character normalizations
           if language.preproc:
               word, simps = language.preproc(word)
           analyses = language.anal_word(word, preproc=False, postproc=True,
                                         segment=True, only_guess=False, phonetic=phonetic,
                                         experimental=experimental, mwe=mwe,
                                         print_out=(not raw and not realize),
                                         conllu=conllu, string=True, nbest=nbest, verbosity=verbosity)
        if realize:
#            print("** analysis {}".format(analysis))
            return [seg2string(word, s, language=language, transortho=transortho, udformat=udformat, simplifications=simps, conllu=conllu) for s in analyses]
        elif raw:
            return analyses

seg = seg_word

def seg_file(file='', language='amh', experimental=False,
             start=0, nlines=0, nbest=4, report_n=100, output_file=None,
             xml=None, multseg=True, csentences=True, sentid=0, batch_name='',
             um=1, seglevel=2, gramfilter=None,
             version='2.2', batch='1.0',
             local_cache=None, sep_punc=True, verbosity=0):
    '''
    Analyze the words in a file, by default creating CoNLL-U format.

    @param file:   path to a file to read the words from
    @param output_file:  path to a file where analyses are to be written
    @param preproc:  whether to preprocess inputs
    @param postproc: whether to postprocess outputs
    @param start:    line to start analyzing from
    @param nbest:    max number of segmentations to return for a word
    @param experimental: whether to use the experimental FST instead of
                      the default segmentation FST
    @param xml:      either None/False or True or an XML tree
    @param csentences: if True or a list, create and return CoNLL-U formatted sentences
    @param sentid: CoNLL-U id for first sentence (+1)
    @param local_cache: None or a local cache used in editing another file
                  provide this when segmenting a file in batches to use segmentations from
                  previous batches.
    @param sep_punc: whether to separate punctuation from words
    @param nlines:   number of lines to analyze (if it's not 0)
    @param report_n: how often to report current line
    @param batch_name: name of the input batch of data
    @param version: version of input data (used to create batch_name if not provided)
    @param batch:  number (string or float) of batch (used to create batch_name if not provided)
    '''
    if not file:
        print("No file path given!")
        return
    batch_name = batch_name or "TAFS{}_B{}".format(version, batch)
    language = morpho.get_language(language, phon=False, segment=True, experimental=experimental)
    global SEGMENT
    SEGMENT = True
    if language:
        return \
        language.anal_file(file, output_file,
                           pos=None, preproc=True, postproc=True, sep_punc=sep_punc,
                           segment=True, only_guess=False, guess=False, experimental=experimental,
                           realize=True, start=start, nlines=nlines, nbest=nbest, report_n=report_n,
                           xml=xml, multseg=multseg, csentences=csentences, sentid=sentid,
                           um=um, seglevel=seglevel, gramfilter=gramfilter,
                           local_cache=local_cache, batch_name=batch_name,
                           verbosity=verbosity)

def extract_corpus_features(corpus, pos=None, searchfeats=None):
    '''
    For each sentence in the corpus, return a list of words that have features and whose POS is in the pos list.
    searchfeats is a list of feature, default pairs which limits the features that are returned.
    '''
    def extract_features(featstring, searchfeats):
        featstring = dict([fv.split('=') for fv in featstring.split('|')])
        return [featstring.get(feat, dflt) for feat, dflt in searchfeats]
    sentences = []
    for sentence in corpus.sentences:
        words = [sentence.text]
        for index, word in enumerate(sentence.words):
            word = word[0][0]
            if pos and word.get('upos') not in pos:
                continue
            if feats := word.get('feats'):
                if searchfeats:
                    feats = extract_features(feats, searchfeats)
                words.append((index+1, word.get('form'), feats))
        sentences.append(words)
    return sentences

def create_corpus(data=None, read={}, write={}, batch={}, constraints={},
                  analyze=False,
                  segment=True, disambiguate=True, conlluify=True, degeminate=False,
                  um=1, seglevel=2, timeit=False, local_cache=None, fsts=None,
                  verbosity=0):
    '''
    Create a corpus (instance of Corpus) of raw sentences, to be segmented (with segment_all()),
    disambiguated in a GUI (with disambiguate()), converted to CoNLL-U (with conlluify()), and
    written to a file (with write_conllu()).
    Only works for Amharic.

    @param data: list of unsegmented, tokenized sentence strings or None, in which case data
       is read in from file
    @param read: dict with keys 'path', 'folder', 'filename', as possible keys, ignored
       in case data is not None
    @param write: dict with keys 'stdout', 'path', 'folder', 'filename', 'annotator', 'append' as possible keys
    @param batch: dict with keys 'name', 'id', 'start', 'n_sents', 'sent_length', 'source', 'version', 'max_sents', 'sentid'
    @param constraints: dict with keys 'grammar', 'minlen', 'maxlen', 'maxpunc', 'maxnum', 'maxunk', 'maxtoks'
       grammar value is a string label for a grammar filter dict; filters exclude or include sentences
       that satisfy or don't satisfy the filter conditions. See conditions in EES.filters.
    @param segment: whether to segment the data with HM after it is loaded
    @param disambiguate: whether to disambiguate the data using the HM GUI after it is segmented
    @param conlluify: whether to run Corpus.conlluify() on the disambiguated pre-CoNLL-U lists
    @param degeminate: whether to geminate lemmas, as well as forms, when running conlluify()
       and to write both geminated and ungeminated files
    @param timeit: whether to time segmentation
    @param local_cache: cache to store segmentations
    @param um: int indicating whether (1|2 vs. 0) to use UM features converted to UD features and if so,
       how many features (2 indicates features not in UD and possibly in UM guidelines)
    @param seglevel: int indicating whether to segment words and if so, how much; 2 is maximum
    @param filter: if not None, either a string label for a filter or a filter dict; filters exclude
       sentences from the corpus that don't satisfy the filter conditions. See conditions in EES.filters.
    @param verbosity: int controlling how verbose messages should be
    '''
    disambiguate = False if analyze else disambiguate
    conlluify = False if analyze else conlluify

    n_sents = batch.get('n_sents', 100)
    max_sents = batch.get('max_sents', 1000)
    start = batch.get('start', 0)
    sentnum = "{}".format(n_sents) #"{}-{}".format(start+1, start+n_sents) if start else "{}".format(n_sents)
    sent_length = batch.get('sent_length', '')
    gramfilt = constraints.get('grammar')
    batch_name = batch.get('name') or \
      "{}{}{}_B{}_{}s".format(batch.get('source', 'CACO'),
                              "_{}".format(gramfilt) if gramfilt else '',
                              "_{}w".format(sent_length) if sent_length else '',
                              batch.get('id', 1),
                              sentnum)
    def make_path(path, folder, filename, extension):
        if path:
            return path
        if not filename.endswith(extension):
            filename += extension
        return morpho.os.path.join(folder, filename)
    path = ''
    readpath = ''
    if data:
        # We may be deleting sentences, so better make a copy.
        data = data.copy()
    if not data:
        readpath = make_path(read.get('path', ''), read.get('folder', morpho.CACO_DIR), read.get('filename', ''), '.txt')
    corpus = morpho.Corpus(data=data, path=readpath, start=start, n_sents=n_sents, max_sents=max_sents,
                           batch_name=batch_name, sentid=batch.get('sentid', 0), fsts=fsts, seglevel=seglevel, um=um,
                           analyze=analyze,
                           constraints=constraints, local_cache=local_cache, timeit=timeit,
                           segment=segment,
#                           disambiguate=disambiguate, conlluify=conlluify, degeminate=degeminate,
                           verbosity=verbosity)
    if not corpus or not corpus.data:
        print("No corpus found!")
        return
#    if segment:
#        corpus.segment(timeit=timeit, filter=gramfilt, um=um, seglevel=seglevel, verbosity=verbosity)
    if disambiguate:
        # Checks to see whether segment() has already been called
        corpus.disambiguate(timeit=timeit, seglevel=seglevel, verbosity=verbosity)
    # Normally disambiguation should happen before this, but it doesn't have to.
    if conlluify:
        corpus.conlluify(degeminate=degeminate, verbosity=verbosity)
        if write:
            # 'write' dict must contain something for write to happen
            if write.get('stdout'):
                path = ''
            elif write.get('path'):
                # Explicit path
                path = write['path']
            else:
                folder = write.get('folder', '')
                filename = write.get('filename', '')
                if not filename:
                    # Make the filename from the batch_name
                    filename = "{}_MA{}".format(batch_name, write.get("annotator", 1))
                path = morpho.os.path.join(folder, filename)
            gempath = ungempath = ''
            append = write.get('append', False)
            # geminated corpus
            if path:
                # write to file
                gempath = path + '-G.conllu'
            # conlluify() has to happen before write_conllu
            write_conllu(corpus=corpus, path=gempath, degeminated=False, append=append,
                         batch_name=batch_name, verbosity=verbosity)
            if degeminate:
                # ungeminated corpus
                if path:
                    # write to file
                    ungempath = path + '-U.conllu'
                write_conllu(corpus=corpus, path=ungempath, degeminated=True, append=append,
                             batch_name=batch_name, verbosity=verbosity)
    return corpus

def seg_sentence4(sentence, language='amh', remove_dups=True, um=0, seglevel=2,
                 gramfilter=None, fsts=None, verbosity=0):
    '''
    Segment a sentence, returning an instance of Sentence.
    Only works for Amharic.
    um controls whether to created UD features from UM features (and which ones).
    seglevel controls whether to segment the word (and how much).
    gramfilter is a string label for a filter dict for excluding or including sentences with
    particular morphological properties. See EES.filters.
    '''
    language = morpho.get_language(language, phon=False, segment=True, experimental=True)
    return \
      language.anal_sentence4(sentence, remove_dups=remove_dups, um=um, seglevel=seglevel,
                             gramfilter=gramfilter, fsts=fsts, verbosity=verbosity)

def anal_sentence4(sentence, language='amh', remove_dups=True, fsts=None, verbosity=0):
    '''
    Analyze a sentence, returning an instance of Sentence.
    Only works for Amharic.
    '''
    language = morpho.get_language(language, phon=False, segment=False, experimental=False)
    return \
      language.anal_sentence4(sentence, remove_dups=remove_dups, verbosity=verbosity,
                             segment=False, experimental=False, conllu=False, fsts=fsts)

def anal_word4(language, word, 
              gloss=True, 
              roman=False, segment=False, guess=False, freq=False, simplify=True,
              experimental=False, dont_guess=True, cache='', init_weight=None,
              lemma_only=False, ortho_only=False, normalize=True,
              nbest=5, um=0, phonetic=True, raw=True,
              pos=[], verbosity=0):
    '''
    Analyze a single word, trying all available analyzers, and print out
    the analyses.

    @param language (str): abbreviation for a language
    @param word (str):     word to be analyzed
    @param gloss (bool):   whether to include an English gloss if available
    @param roman (bool):    whether the language is written in roman script
    @param segment (bool):  whether to return the segmented input string rather than
                     the root/stem
    @param experimental (bool): whether to use the experimental FST instead of the
                     default analysis FST
    @param guess (bool):    try only guesser analyzer
    @param dont_guess (bool):    try only lexical analyzer
    @param phonetic (bool): whether to convert root to phonetic form (from SERA)
    @param lemma_only: whether to print out only the lemma
    @paran ortho_only: whether to include phonetic forms of lemmas and roots
    @param normalize: whether to normalize features
    @param freq (bool):     whether to report frequencies of roots
    @param nbest (int):    maximum number of analyses to return or print out
    @param um (int):       whether to output UniMorph features; 1 and 2 represent different
                           levels of features
    @param raw (bool):      whether the analyses should be returned in "raw" form
    @param gloss (str):    language to return gloss for, or ''
    @return:         a list of analyses (only if raw is True)
    '''
    language = morpho.get_language(language, cache=cache,
                                   phon=False, segment=segment, experimental=experimental)
    if language:
        print_out = not raw and not um
        # Process special cases
        analyses = language.preproc_special(word, segment=segment, print_out=print_out)
        if not analyses:
#        numeral = language.morphology.match_numeral(word)
#        if numeral:
#            prenum, num, postnum = numeral
##            print("** Found numeral word: {} - {} - {}".format(prenum, num, postnum))
#            analysis = language.process_numeral(word, prenum, num, postnum, segment=False)
#        else:
            analyses = \
              language.anal_word(word, preproc=not roman, postproc=not roman,
                             gloss=gloss,
                             phonetic=phonetic, segment=segment, only_guess=guess,
                             lemma_only=lemma_only, ortho_only=ortho_only,
                             guess=not dont_guess, cache=False, simplify=simplify,
                             nbest=nbest, report_freq=freq, um=um, normalize=normalize and raw,
                             init_weight=init_weight, string=not raw and not um,
                             print_out=print_out, fsts=pos, verbosity=verbosity)
        if raw or um:
            return analyses

anal4 = anal_word4

def anal_files4(language, infiles, outsuff='.out',
               lemma_only=False, ortho_only=False,
               normalize=False, preproc=True, postproc=True, guess=False, raw=False,
               xml=None, dont_guess=False, freq=True, nbest=3):
    """Analyze the words in a set of files, writing the analyses to
    files whose names are the infile names with outpre prefixed to them.
    See anal_file for description of parameters."""
    language = morpho.get_language(language)
    if language:
        # Dict for saving analyses
        saved = {}
        for infile in infiles:
            outfile = infile + outsuff
            language.anal_file(infile, outfile, 
                               pos=None, preproc=preproc, postproc=postproc,
                               nbest=nbest, normalize=normalize and raw,
                               only_guess=guess, guess=not dont_guess,
                               ortho_only=ortho_only, lemma_only=lemma_only,
                               xml=xml,
                               raw=raw, saved=saved)

def anal_file4(language, infile, outfile=None,
              um=0,
              lemma_only=False, ortho_only=False, normalize=False,
              preproc=True, postproc=True, guess=False, raw=False,
              dont_guess=False, sep_punc=True, lower_all=False,
              feats=None, simpfeats=None, word_sep='\n', sep_ident=False, minim=False,
              nbest=100, start=0, nlines=0, report_n=1000,
              xml=None, local_cache=None,
              verbosity=0):
    '''Analyze the words in a file, writing the analyses to outfile.

    @param infile:   path to a file to read the words from
    @param outfile:  path to a file where analyses are to be written
    @param preproc:  whether to preprocess inputs
    @param postproc: whether to postprocess outputs
    @param guess:    try only guesser analyzer
    @param dont_guess: try only lexical analyzer
    # added 2021.4.15
    @param lemma_only: whether to print out only the lemma
    # added 2021.12.10
    @param normalize: whether to normalize features
    @param feats:    list of grammatical features to be printed out for each analysis
    @param simpfeats: dict of simplifications (FS->string) for recording FSs
    @param word_sep: character to separate words (unless minim is True)
    @param minim:    whether to print simplified descriptions of each word, separated
                     by spaces
    @param sep_ident: whether there are tab-separated identifiers in the source file
                     that should be maintained in the output
    @param raw:      whether the analyses should be printed in "raw" form
    @param start:    line to start analyzing from
    @param nlines:   number of lines to analyze (if not 0)
    @param local_cache: None or a local cache used in editing another file
    @param xml:      either None/False or True or an XML tree
    '''
    language = morpho.get_language(language)
    if language:
        return \
        language.anal_file(infile, outfile, 
                           um=um, pos=None, preproc=preproc, postproc=postproc,
                           only_guess=guess, guess=not dont_guess, raw=raw,
                           lemma_only=lemma_only, ortho_only=ortho_only,
                           nbest=nbest, normalize=normalize and raw,
                           sep_punc=sep_punc, feats=feats, simpfeats=simpfeats,
                           word_sep=word_sep, sep_ident=sep_ident, minim=minim,
                           lower_all=lower_all, start=start, nlines=nlines, report_n=report_n,
                           xml=xml, local_cache=local_cache,
                           verbosity=verbosity)

def gen4(language, root, features=[], pos=None, guess=False,
        phon=False, ortho=True, ortho_only=False,
        um='', all_words=True, del_feats=None, report_um=True,
        roman=False, interact=False, return_words=True,
        verbosity=0):
    '''
    Generate a word, given stem/root and features (replacing those in default).
    If pos is specified, check only that POS; otherwise, try all in order until
    one succeeeds.

    @param root <str (roman)>:     root or stem of a wor
    @param features <str: [sb=[+p1,+plr]>: grammatical features to be added
       to default
    @param pos <str>:    part-of-speech: use only the generator for this POS
    @param guess <bool>:    whether to use guess generator if lexical generator fails
    @param phon <bool>:     whether to use the 'phonetic' generation FST
    @param ortho <bool>:    whether to first convert the root from orthographic form
    @param ortho_only <bool>: whether to not return/print romanized/phonetic form
    @param roman <bool>:    whether the languages uses a roman script
    @param return_words <bool>: whether to return the words, rather than printing
      them out
    @param um <str>:       UniMorph features
    @param all_words <bool>: whether to return all words
    @param del_feats <list of strings>: features to be deleted from default so that all
      values can be generated
    @param report_um <bool>: whether to report UM features if del_feats is True
    '''
    language = morpho.get_language(language, segment=False, phon=phon)
    if language:
        is_not_roman = not roman
        morf = language.morphology
        if language.procroot:
            root, features = language.procroot(root, features, pos)
        outputs = []
        um_converted = False
        # list of POS strings for each output
        poss = []
        if pos:
            posmorph = morf[pos]
            if um:
                lang_um = language.um
                if lang_um:
                    features = lang_um.convert_um(pos, um)
                if features:
                    um_converted = True
            if features or not um:
                output = posmorph.gen(root, update_feats=features, interact=interact,
                                      del_feats=del_feats, ortho=ortho, phon=phon,
                                      ortho_only=ortho_only, postproc=is_not_roman, guess=guess,
                                      verbosity=verbosity)
                if output:
                    outputs.extend(output)
                    poss.extend([pos] * len(output))
        if not outputs:
            for posmorph in list(morf.values()):
                pos1 = posmorph.pos
                if um:
                    lang_um = language.um
                    if lang_um:
                        features = lang_um.convert_um(posmorph.pos, um)
                    if features:
                        um_converted = True
                if features or not um:
                    output = posmorph.gen(root, update_feats=features,
                                          interact=interact, del_feats=del_feats,
                                          ortho=ortho, phon=phon, ortho_only=ortho_only,
                                          postproc=is_not_roman, guess=guess,
                                          verbosity=verbosity)
                    if output:
                        outputs.extend(output)
                        poss.extend([pos1] * len(output))
        if um and not um_converted:
            print("Couldn't convert UM to HM features")
            return

        if outputs:
            if del_feats:
                # For del_feats, we need to print out relevant
                # values of del_feats for each output word
                o, poss = morpho.POSMorphology.separate_gens(outputs, poss)
                if report_um:
                    o = language.gen_um_outputs(o, poss)
                else:
                    o = morpho.POSMorphology.gen_output_feats(o, del_feats)
            elif all_words:
                o = [out[0] for out in outputs]
            else:
                o = outputs[0][0]
            # Eliminate copies
            o = list(set(o))
            if return_words:
                return o
            else:
                print(o)
                return
        f = um if um else features
        print("{}:{} can't be generated!".format(root, f))

def phon_word(lang_abbrev, word, raw=False, postproc=False, nbest=100, freq=False,
              return_string=False):
    '''Convert a form in non-roman to roman, making explicit features that are missing in the orthography.
    @param lang_abbrev: abbreviation for a language
    @param word:     word to be analyzed
    @param postproc: whether to run postpostprocess on the form
    @param nbest:    maximum number of analyses to return or print out
    @param freq:     whether to report frequencies of roots
    @return:         a list of analyses
    '''
    language = morpho.get_language(lang_abbrev, phon=True, segment=False)
    if language:
        return language.ortho2phon(word, report_freq=freq, nbest=nbest,
                                   postpostproc=postproc, 
                                   raw=raw, return_string=return_string)

phon = phon_word

def phon_file(lang_abbrev, infile, outfile=None, word_sep='\n', anal_sep=' ', print_ortho=True,
              postproc=False, freq=True, nbest=100, start=0, nlines=0):
    '''Convert non-roman forms in file to roman, making explicit features that are missing in the orthography.
    @param lang_abbrev: abbreviation for a language
    @param infile:   path to a file to read the words from
    @param outfile:  path to a file where analyses are to be written
    @param word_sep: separator between words
    @param anal_sep: separator between analyses
    @param print_ortho: whether to print out orthographic form
    @param postproc: whether to run postpostprocess on the form
    @param freq:     whether to report frequencies of roots
    @param nbest:    maximum number of analyses to return or print out for each word
    @param start:    line to start analyzing from
    @param nlines:   number of lines to analyze (if not 0)
    '''
    language = morpho.get_language(lang_abbrev, phon=True, segment=False)
    if language:
        language.ortho2phon_file(infile, outfile=outfile,
                                 word_sep=word_sep, anal_sep=anal_sep, print_ortho=print_ortho,
                                 postpostproc=postproc, nbest=nbest,
                                 report_freq=freq,
                                 start=start, nlines=nlines)

def get_features(language, pos=None):
    '''Return a dict of features and their possible values for each pos.

    @param language:  abbreviation for a language
    @param pos:       part-of-speech; if provided, return only
                      features for this POS
    @return:          dictionary of features and possible values; if
                      there is more than one POS, list of such
                      dictionaries.
    '''
    language = morpho.get_language(language)
    if language:
        morf = language.morphology
        if pos:
            return morf[pos].get_features()
        elif len(morf) == 1:
            return list(morf.values())[0].get_features()
        else:
            feats = []
            for pos, posmorph in list(morf.items()):
                feats.append((pos, posmorph.get_features()))
            return feats

def seg2string(word, segmentation, language='am', sep='-', transortho=True,
               udformat=False, simplifications=None, conllu=True):
    """Convert a segmentation (triple with seg string as second item)
    to a series of spelled out morphemes, ignoring any alternation rules.
    @param word:        the word segmented
    @param language:     abbreviation for a language
    @param segmentation: triple with seg string as second item
    @param sep:          character to separate morphemes in return string
    @param transortho:   for languages written in Geez, whether to output this
    @param udformat:   whether to format POS and features as UD
    @param conllu:     whether to format as dicts for CoNLL-U format
    @return:             word form as string
    """
    language = morpho.get_language(language, segment=True)
    return language.segmentation2string(word, segmentation, sep=sep, transortho=transortho,
                                        udformat=udformat, simplifications=simplifications, conllu=conllu)

### Functions for debugging and creating FSTs

def cascade(language, pos, gen=False, phon=False, segment=False,
            seglevel=2, translate=False, verbose=False):
    '''Returns a cascade for the language and part-of-speech.
    @param language: abbreviation for a language, for example, 'gn'
    @param pos:    part-of-speech for the cascade, for example, 'v'
    @param phon:   whether the cascade is for phonology
    @param segment: whether the cascade is for segmentation
    @param invert: whether to return the inverted cascade (for generation).
    @param verbose: whether to print out various messages
    @return:       cascade for the the language and POS: a list of FSTs
    '''
    pos = get_pos(language, pos, phon=phon, segment=segment, translate=translate,
                  load_morph=False, verbose=verbose)
    if not gen and pos.casc:
        return pos.casc
    if gen:
        if pos.casc_inv:
            return pos.casc_inv
        if pos.casc:
            casc_inv = pos.casc.inverted()
            pos.casc_inv = casc_inv
            return casc_inv
    pos.load_fst(True, create_fst=False, generate=gen, invert=gen, gen=gen, seglevel=seglevel,
                 translate=translate, segment=segment, verbose=verbose)
    if gen:
        return pos.casc_inv
    return pos.casc

def compile(abbrev, pos, gen=True, phon=False, segment=False, guess=False,
            translate=False, experimental=False, mwe=False, seglevel=2,
            v5=True,
            gemination=True, split_index=0, verbose=True):
    """
    Create a new composed cascade for a given language (abbrev) and part-of-speech (pos),
    returning the morphology POS object for that POS.
    If gen is True, create both the analyzer and generator, inverting the analyzer to create
    the generator.
    Note: the resulting FSTs are not saved (written to a file). To do this, use the method
    save_fst(), with the right options, for example, gen=True, segment=True.
    """
    # Look in the fidel directory for languages with these abbreviations
    fidel = abbrev in morpho.FIDEL
    pos_morph = get_pos(abbrev, pos, phon=phon, segment=segment, translate=translate, guess=guess,
                        fidel=fidel, load_morph=False, verbose=verbose)
    if verbose:
        print(">>> CREATING ANALYZER <<<")
    fst = pos_morph.load_fst(True, segment=segment, gen=False, invert=False, guess=guess,
                             translate=translate, recreate=True, fidel=fidel,
                             experimental=experimental, mwe=mwe, pos=pos, seglevel=seglevel,
                             create_fst=True, relabel=True, gemination=gemination,
                             v5=v5,
                             compose_backwards=False, split_index=split_index,
                             phon=phon, verbose=verbose)
    if gen == True: # and mwe == False:
        # Also create the generation FST ##, but not for MWEs
        if seglevel == 0:
            # Just invert the analyzer
            if verbose:
                print(">>> INVERTING ANALYZER FOR GENERATOR <<<")
            genfst = fst.inverted()
        else:
            if verbose:
                print(">>> CREATING GENERATOR <<<")
            analfst = pos_morph.load_fst(True, segment=segment, gen=False, invert=False, guess=guess,
                                         translate=translate, recreate=True, fidel=fidel,
                                         experimental=experimental, mwe=mwe, pos=pos, seglevel=0,
                                         create_fst=True, relabel=True, gemination=gemination,
                                         compose_backwards=False, split_index=split_index,
                                         setit=False, v5=v5,
                                         phon=phon, verbose=verbose)
            print("Inverting analysis FST for generation")
            genfst = analfst.inverted()
        pos_morph.set_fst(genfst, generate=True, guess=False, phon=phon, segment=False, translate=translate,
                          experimental=experimental, mwe=mwe, v5=v5)
    return pos_morph

def test_fst(language, pos, string, gen=False, phon=False, segment=False,
             fst_label='', fst_index=0):
    """Test a individual FST within a cascade, identified by its label or its index,
    on the transduction of a string.
    @param language: abbreviation for a language, for example, 'gn'
    @param pos:    part-of-speech for the cascade, for example, 'v'
    @param phon:   whether the cascade is for phonology
    @param segment: whether the cascade is for segmentation
    @param gen:     whether to use the inverted cascade (for generation).
    @param verbose: whether to print out various messages
    @return:       a list of analyses, each a list consisting of a root and a feature-structure set
    """
    casc = cascade(language, pos, gen=gen, phon=phon, segment=segment)
    if not casc:
        print('No cascade found')
        return
    return casc.transduce1(string, fst_label=fst_label, fst_index=fst_index)

def get_pos(abbrev, pos, phon=False, segment=False, load_morph=False, gen=False, fidel=False,
            translate=False, experimental=False, guess=True, verbose=False):
    """Just a handy function for working with the POS objects when re-compiling
    and debugging FSTs.
    @param abbrev: abbreviation for a language, for example, 'am'
    @param pos:    part-of-speech for the FST, for example, 'v'
    @param phon:   whether the FST is for phonology
    @param segment: whether the FST is for segmentation
    @param translate: whether the FST is for translation
    @param verbose: whether to print out various messages
    @return:       POS object for the the language and POS
    """
    load_lang(abbrev, segment=segment, phon=phon, load_morph=load_morph, gen=gen, fidel=fidel,
              translate=translate, guess=guess, experimental=experimental, verbose=verbose)
    lang = morpho.get_language(abbrev, phon=phon, segment=segment, experimental=experimental,
                               load_morph=load_morph, fidel=fidel, load=load_morph, verbose=verbose)
    if lang:
        return lang.morphology[pos]

def join(language, POS, segstring):
    """
    Join the sequence of morphemes in segstring, using rules
    (instances of Rule)
    implementing alternation rules at the morpheme boundaries.
    For Amharic, POS is 'v', 'n', or 'n_dv'.
    """
    language = morpho.get_language(language, segment=True, load_morph=False)
    return language.join_segments(POS, segstring)

def show_segs(segmentation):
    """Display the segments in a segmentation."""
    if isinstance(segmentation, tuple):
        segmentation = segmentation[1]
    for seg in segmentation.split('-'):
        print(seg)

def get_language(abbrev):
    """Get the language with the abbreviation if it's loaded."""
    return morpho.LANGUAGES.get(abbrev)

## Shortcuts for Amharic
A = lambda w, raw=False: anal_word('amh', w, raw=raw)
S = lambda w, raw=False, realize=True, features=True, transortho=True: seg_word('amh', w, raw=raw, realize=realize, features=features, transortho=transortho, experimental=False)
P = lambda w, raw=False: phon_word('amh', w, raw=raw)
G = lambda r, features=None: gen('amh', r, features=features)
AF = lambda infile, outfile=None, raw=False: anal_file('amh', infile, outfile=outfile, raw=raw)
SF = lambda infile, outfile=None: seg_file('amh', infile, outfile=outfile, experimental=False)
XF = lambda infile, outfile=None: seg_file('amh', infile, outfile=outfile, experimental=True)
PF = lambda infile, outfile=None: phon_file('amh', infile, outfile=outfile)
