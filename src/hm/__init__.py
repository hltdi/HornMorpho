"""
This file is part of HornMorpho, which is a project of PLoGS.

Copyleft 2008-2025. Michael Gasser

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

Author: Michael Gasser <gasser@iu.edu>
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

__cat__ = ''
__version__ = '5.3.2'

__author__ = 'Michael Gasser'

import os

from . import morpho

print('\n@@@@ This is HornMorpho{}, version {} @@@@\n'.format(__cat__, __version__))

SEGMENT = False

#USER_DIR = os.path.join(os.path.dirname(__file__), os.pardir, 'usr')

USER_DIR = os.path.join(os.path.dirname(__file__), 'usr')

###
### Version 5 functions.
###

def anal_corpus(language, **kwargs):
    """
    Create a corpus of sentences, given a list of raw sentence strings.
    To save unknown words, do 'save_unk' = True.
    To save ambiguous words, do 'save_ambig' = True.
    """
    guess = kwargs.get('guess', False)
    verbosity = kwargs.get('verbosity', 0)
    disambiguate = kwargs.get('disambiguate', False)
    annotate = kwargs.get('annotate', False)
    morph_version = kwargs.get('morph_version', 0)
    cg = kwargs.get('CGdisambiguate', kwargs.get('cg', False))
    annotate = cg and kwargs.get('annotate', False)
    language = morpho.get_language(language, guess=guess, morph_version=morph_version, cg=cg, annotate=annotate)
    if language:
        # Create the corpus, by default analyzing sentences and running CG disambiguation on them.
        corp = morpho.Corpus(language=language, **kwargs)
        # Run manual disambiguation on the sentences.
        if disambiguate:
            if verbosity:
                print("Starting manual disambiguation...")
            corp.disambiguate(verbosity=verbosity)
            if annotate:
                # Only do this after disambiguation
                corp.annotate(verbosity=verbosity)
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
                 batch_name='', append=True, update_ids=True,
                 filter_sents=True, unk_thresh=0.3, ambig_thresh=1.0,
                 verbosity=0):
    '''
    Write the CoNNL-U representations of a list of sentences to a file.

    @param sentences: list of instances of Sentence
    @param path: path to file where the sentences will be written
    @param corpus: instance of Corpus (or None); if sentences is None, use corpus.sentences
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
#        if v5:
        sentence.print_conllu(update_ids=update_ids, file=file, close=False)
#        else:
#            conll = sentence.alt_conllu if degeminated else sentence.conllu
#            print(conll.serialize(), file=file, end='')
    if path:
        file.close()
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
              load_morph=True, cache='', translate=False, gen=False,
              guess=True, verbose=False):
    """Load a language's morphology.

    @param language: a language label
    """
#    print("** load_lang, load_morph = {}".format(load_morph))
    morpho.load_lang(language, pickle=pickle, recreate=recreate,
                     phon=phon, segment=segment, 
                     translate=translate, experimental=experimental, gen=gen,
                     load_morph=load_morph, cache=cache,
                     guess=guess, verbose=verbose)

def gen(language, root, features=[], replace_features=[],
        pos=None, guess=False, phon=False, ortho=True, ortho_only=False,
        um='', all_words=True, del_feats=None, report_um=True,
        interact=False, verbosity=0):
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
    @param um <str>:       UniMorph features
    @param all_words <bool>: whether to return all words
    @param del_feats <list of strings>: features to be deleted from default so that all
      values can be generated
    @param report_um <bool>: whether to report UM features if del_feats is True
    '''
    language = morpho.get_language(language)
    if language:
        mwe = False
        if ' ' in root:
            mwe = True
        morf = language.morphology
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
                                      features=replace_features, mwe=mwe,
                                      del_feats=del_feats, ortho=ortho, phon=phon, v5=True,
                                      postproc=False, guess=guess,
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
                                          features=replace_features,
                                          mwe=mwe,
                                          interact=interact, del_feats=del_feats, v5=True,
                                          ortho=ortho, phon=phon,
                                          postproc=False, guess=guess,
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
            return o
        f = um if um else features
        print("{}:{} can't be generated!".format(root, f))

def download(lang_abbrev, uncompress=True, overwrite=True):
    '''
    Download language abbreviated lang_abbrev, unless it's already downloaded.
    '''
    if lang_abbrev not in morpho.ABBREV2LANG:
        print("HornMorpho doesn't know of any language abbreviated {}.".format(lang_abbrev))
        return
    if morpho.is_downloaded(lang_abbrev):
        if not overwrite:
            print("{} ({}) is already downloaded!".format(morpho.ABBREV2LANG[lang_abbrev], lang_abbrev))
            if not input("Do you want to overwrite it?  ") in ('y', 'Y', 'yes', 'YES'):
                return
        else:
            print("Overwriting current distribution for {}...".format(morpho.ABBREV2LANG[lang_abbrev]))
    morpho.download_language(lang_abbrev, uncompress=uncompress)

# Internal use only.

def compile(abbrev, pos, gen=True, phon=False, segment=False, guess=False,
            translate=False, experimental=False, mwe=False, seglevel=2,
            gemination=True, split_index=0, verbose=True):
    """
    Create a new composed cascade for a given language (abbrev) and part-of-speech (pos),
    returning the morphology POS object for that POS.
    If gen is True, create both the analyzer and generator, inverting the analyzer to create
    the generator.
    Note: the resulting FSTs are not saved (written to a file). To do this, use the method
    save_fst(), with the right options, for example, gen=True, segment=True.
    """
    pos_morph = get_pos(abbrev, pos, phon=phon, segment=segment, translate=translate, guess=guess,
                        load_morph=False, verbose=verbose)
    if verbose:
        print(">>> CREATING ANALYZER <<<")
    fst = pos_morph.load_fst(True, segment=segment, gen=False, invert=False, guess=guess,
                             translate=translate, recreate=True, 
                             experimental=experimental, mwe=mwe, pos=pos, seglevel=seglevel,
                             create_fst=True, relabel=True, gemination=gemination,
                             v5=True,
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
                                         translate=translate, recreate=True,
                                         experimental=experimental, mwe=mwe, pos=pos, seglevel=0,
                                         create_fst=True, relabel=True, gemination=gemination,
                                         compose_backwards=False, split_index=split_index,
                                         setit=False, v5=True,
                                         phon=phon, verbose=verbose)
            print("Inverting analysis FST for generation")
            genfst = analfst.inverted()
        pos_morph.set_fst(genfst, generate=True, guess=False, phon=phon, segment=False, translate=translate,
                          experimental=experimental, mwe=mwe, v5=True)
    return pos_morph

def compress(language):
    '''
    Compress language, given abbreviation, saving resulting .tgz file in languages directory.
    '''
    morpho.compress_lang(language)

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

def get_pos(abbrev, pos, phon=False, segment=False, load_morph=False, gen=False,
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
    load_lang(abbrev, segment=segment, phon=phon, load_morph=load_morph, gen=gen,
              translate=translate, guess=guess, experimental=experimental, verbose=verbose)
    lang = morpho.get_language(abbrev, phon=phon, segment=segment, experimental=experimental,
                               load_morph=load_morph, load=load_morph, verbose=verbose)
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
    """Get the language with the abbreviation if it's loaded.
    Load it if it's not.
    """
    return morpho.get_language(abbrev)

## Shortcuts for Amharic
A = lambda w: anal('a', w)
G = lambda r, features=None: gen('a', r, features=features)
