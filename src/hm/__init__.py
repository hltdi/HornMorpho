"""
This file is part of HornMorpho, which is a project of PLoGS.

Copyleft 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2017, 2018, 2019, 2020

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

__version__ = '4.01'
__author__ = 'Michael Gasser'

from . import morpho

print('\n@@@@ This is HornMorpho, version {} @@@@\n'.format(__version__))

SEGMENT = False

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

def load_lang(language, phon=False, segment=False,
              load_morph=True, cache='', simplified=False,
              guess=True, verbose=False):
    """Load a language's morphology.

    @param language: a language label
    @type  language: string
    """
    morpho.load_lang(language,
                     phon=phon, segment=segment, simplified=simplified,
                     load_morph=load_morph, cache=cache,
                     guess=guess, verbose=verbose)

def seg_word(language, word, nbest=100, raw=False, realize=False, features=True,
             transortho=True):
    '''Segment a single word and print out the results.

    @param language: abbreviation for a language
    @type  language: string
    @param word:     word to be analyzed
    @type  word:     string or unicode
    @param realize:  whether to realize individual morphemes (in particular
                     the stem of an Amharic verb or deverbal noun)
    @type realize:   boolean
    @param features: whether to show the grammatical feature labels
    @type features:  boolean
    @param transortho: whether to convert output to non-roman orthography
    @type transortho: boolean
    @return:         analyses (only if raw is True)
    @rtype:          list of (POS, segstring, count) triples or a list of strings
                     (if realize is True)
    '''
    language = morpho.get_language(language, phon=False, segment=True)
    global SEGMENT
    SEGMENT = True
    if language:
        analysis = language.anal_word(word, preproc=True, postproc=True,
                                      gram=False, segment=True, only_guess=False,
                                      print_out=(not raw and not realize),
                                      string=True, nbest=nbest)
        if realize:
            return [seg2string(s, language=language, features=features, transortho=transortho) for s in analysis]
        elif raw:
            return analysis

seg = seg_word

def seg_file(language, infile, outfile=None,
             preproc=True, postproc=True, start=0, nlines=0):
    '''Analyze the words in a file, writing the analyses to outfile.

    @param infile:   path to a file to read the words from
    @type  infile:   string
    @param outfile:  path to a file where analyses are to be written
    @type  outfile:  string
    @param preproc:  whether to preprocess inputs
    @type  preproc:  boolean
    @param postproc: whether to postprocess outputs
    @type  postproc: boolean
    @param start:    line to start analyzing from
    @type  start:    int
    @param nlines:   number of lines to analyze (if not 0)
    @type  nlines:   int
    '''
    language = morpho.get_language(language, phon=False, segment=True)
    global SEGMENT
    SEGMENT = True
    if language:
        language.anal_file(infile, outfile, gram=False,
                           pos=None, preproc=preproc, postproc=postproc,
                           segment=True, only_guess=False, guess=False,
                           start=start, nlines=nlines)

def anal_word(language, word, root=True, citation=True, gram=True,
              roman=False, segment=False, guess=False, gloss=True,
              dont_guess=True, cache='', init_weight=None,
              rank=True, freq=False, nbest=5, um=False,
              phonetic=True, raw=False):
    '''Analyze a single word, trying all available analyzers, and print out
    the analyses.

    @param language (str): abbreviation for a language
    @param word (str):     word to be analyzed
    @param root (bool):     whether a root is to be included in the analyses
    @param citation (bool): whether a citation form is to be included in the analyses
    @param gram (bool):     whether a grammatical analysis is to be included
    @param roman (bool):    whether the language is written in roman script
    @param segment (bool):  whether to return the segmented input string rather than
                     the root/stem
    @param guess (bool):    try only guesser analyzer
    @param dont_guess (bool):    try only lexical analyzer
    @param phonetic (bool): whether to convert root to phonetic form (from SERA)
    @param rank (bool):     whether to rank the analyses by the frequency of their roots
    @param freq (bool):     whether to report frequencies of roots
    @param nbest (int):    maximum number of analyses to return or print out
    @param um (bool):       whether to output UniMorph features
    @param raw (bool):      whether the analyses should be returned in "raw" form
    @param gloss (str):    language to return gloss for, or ''
    @return:         a list of analyses (only if raw is True)
    '''
    language = morpho.get_language(language, cache=cache,
                                   phon=False, segment=segment)
    if language:
        analysis = language.anal_word(word, preproc=not roman,
                                      postproc=not roman,
                                      root=root, citation=citation,
                                      gram=gram, gloss=gloss,
                                      phonetic=phonetic,
                                      segment=segment, only_guess=guess,
                                      guess=not dont_guess, cache=False,
                                      nbest=nbest, report_freq=freq,
                                      um=um, init_weight=init_weight,
                                      string=not raw and not um,
                                      print_out=not raw and not um)
        if raw or um:
            return analysis

anal = anal_word

def anal_files(language, infiles, outsuff='.out',
               root=True, citation=True, gram=True,
               preproc=True, postproc=True, guess=False, raw=False,
               dont_guess=False, rank=True, freq=True, nbest=5):
    """Analyze the words in a set of files, writing the analyses to
    files whose names are the infile names with outpre prefixed to them.
    See anal_file for description of parameters."""
    language = morpho.get_language(language)
    if language:
        # Dict for saving analyses
        saved = {}
        for infile in infiles:
            outfile = infile + outsuff
            language.anal_file(infile, outfile, root=root, citation=citation, gram=gram,
                               pos=None, preproc=preproc, postproc=postproc,
                               nbest=nbest,
                               only_guess=guess, guess=not dont_guess,
                               raw=raw, saved=saved)

def anal_file(language, infile, outfile=None,
              root=True, citation=True, gram=True, um=False,
              preproc=True, postproc=True, guess=False, raw=False,
              dont_guess=False, sep_punc=True, lower_all=False,
              feats=None, simpfeats=None,
              word_sep='\n', sep_ident=False, minim=False,
              rank=True, freq=True, nbest=100,
              start=0, nlines=0):
    '''Analyze the words in a file, writing the analyses to outfile.

    @param infile:   path to a file to read the words from
    @param outfile:  path to a file where analyses are to be written
    @param root:     whether a root is to be included in the analyses
    @param citation: whether a citation form is to be included in the analyses
    @param gram:     whether a grammatical analysis is to be included
    @param preproc:  whether to preprocess inputs
    @param postproc: whether to postprocess outputs
    @param guess:    try only guesser analyzer
    @param dont_guess: try only lexical analyzer
    @param feats:    list of grammatical features to be printed out for each analysis
    @param simpfeats: dict of simplifications (FS->string) for recording FSs
    @param word_sep: character to separate words (unless minim is True)
    @param minim:    whether to print simplified descriptions of each word, separated
                     by spaces
    @param sep_ident: whether there are tab-separated identifiers in the source file
                     that should be maintained in the output
    @param rank:     whether to rank the analyses by the frequency of their roots
    @param freq:     whether to report frequencies of roots
    @param raw:      whether the analyses should be printed in "raw" form
    @param start:    line to start analyzing from
    @param nlines:   number of lines to analyze (if not 0)
    '''
    language = morpho.get_language(language)
    if language:
        language.anal_file(infile, outfile, root=root, citation=citation,
                           gram=gram, um=um,
                           pos=None, preproc=preproc, postproc=postproc,
                           only_guess=guess, guess=not dont_guess, raw=raw,
                           nbest=nbest,
                           sep_punc=sep_punc, feats=feats, simpfeats=simpfeats,
                           word_sep=word_sep, sep_ident=sep_ident, minim=minim,
                           lower_all=lower_all,
                           start=start, nlines=nlines)

def gen(language, root, features=[], pos=None, guess=False,
        phon=False, ortho=True, ortho_only=False,
        um='', all_words=True, del_feats=None, report_um=True,
        roman=False, interact=False, return_words=True):
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
                output = posmorph.gen(root, update_feats=features,
                                      interact=interact,
                                      del_feats=del_feats,
                                      ortho=ortho, phon=phon,
                                      ortho_only=ortho_only,
                                      postproc=is_not_roman, guess=guess)
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
#                    print("Generating {}, {} (POS={})".format(root, features.__repr__(),
#                                                              posmorph.pos))
                    output = posmorph.gen(root, update_feats=features,
                                          interact=interact,
                                          del_feats=del_feats,
                                          ortho=ortho, phon=phon,
                                          ortho_only=ortho_only,
                                          postproc=is_not_roman, guess=guess)
#                    print("Output for {}: {}".format(posmorph.pos, output))
                    if output:
                        outputs.extend(output)
                        poss.extend([pos1] * len(output))
#                    if output:
#                        break
        if um and not um_converted:
            print("Couldn't convert UM to HM features")
            return

        if outputs:
            if del_feats:
                # For del_feats, we need to print out relevant
                # values of del_feats for each output word
#                print("O {}".format(outputs))
                o, poss = morpho.POSMorphology.separate_gens(outputs, poss)
                if report_um:
                    o = language.gen_um_outputs(o, poss)
                else:
                    o = morpho.POSMorphology.gen_output_feats(o, del_feats)
            elif all_words:
                o = [out[0] for out in outputs]
            else:
                o = outputs[0][0]
            if return_words:
                return o
            else:
                print(o)
                return

        print("This word can't be generated!")

def phon_word(lang_abbrev, word, gram=False, raw=False,
              postproc=False, rank=True, nbest=100, freq=False,
              return_string=False):
    '''Convert a form in non-roman to roman, making explicit features that are missing in the orthography.
    @param lang_abbrev: abbreviation for a language
    @type  lang_abbrev: string
    @param word:     word to be analyzed
    @type  word:     string or unicode
    @param gram:     whether a grammatical analysis is to be included
    @type  gram:     boolean
    @param postproc: whether to run postpostprocess on the form
    @type  postproc: boolean
    @param rank:     whether to rank the analyses by the frequency of their roots
    @type  rank:     boolean
    @param nbest:    maximum number of analyses to return or print out
    @type  nbest:    int
    @param freq:     whether to report frequencies of roots
    @type  freq:     boolean
    @return:         a list of analyses
    @rtype:          list of (root, feature structure) pairs
    '''
    language = morpho.get_language(lang_abbrev, phon=True, segment=False)
    if language:
        return language.ortho2phon(word, gram=gram,
                                   report_freq=freq, nbest=nbest,
                                   postpostproc=postproc, rank=rank,
                                   raw=raw, return_string=return_string)

phon = phon_word

def phon_file(lang_abbrev, infile, outfile=None, gram=False,
              word_sep='\n', anal_sep=' ', print_ortho=True,
              postproc=False, rank=True, freq=True, nbest=100,
              start=0, nlines=0):
    '''Convert non-roman forms in file to roman, making explicit features that are missing in the orthography.
    @param lang_abbrev: abbreviation for a language
    @type  lang_abbrev: string
    @param infile:   path to a file to read the words from
    @type  infile:   string
    @param outfile:  path to a file where analyses are to be written
    @type  outfile:  string
    @param gram:     whether a grammatical analysis is to be included
    @type  gram:     boolean
    @param word_sep: separator between words (when gram=False)
    @type  word_sep: string
    @param anal_sep: separator between analyses (when gram=False)
    @type  anal_sep: string
    @param print_ortho: whether to print out orthographic form (when gram=False)
    @type  print_ortho: boolean
    @param postproc: whether to run postpostprocess on the form
    @type  postproc: boolean
    @param rank:     whether to rank the analyses by the frequency of their roots
    @type  rank:     boolean
    @param freq:     whether to report frequencies of roots
    @type  freq:     boolean
    @param nbest:    maximum number of analyses to return or print out for each word
    @type  nbest:    int
    @param start:    line to start analyzing from
    @type  start:    int
    @param nlines:   number of lines to analyze (if not 0)
    @type  nlines:   int
    '''
    language = morpho.get_language(lang_abbrev, phon=True, segment=False)
    if language:
        language.ortho2phon_file(infile, outfile=outfile, gram=gram,
                                 word_sep=word_sep, anal_sep=anal_sep, print_ortho=print_ortho,
                                 postpostproc=postproc, rank=rank, nbest=nbest,
                                 report_freq=freq,
                                 start=start, nlines=nlines)

def get_features(language, pos=None):
    '''Return a dict of features and their possible values for each pos.

    @param language:  abbreviation for a language
    @type  language:  string
    @param pos:       part-of-speech; if provided, return only
                      features for this POS
    @type  pos:       string
    @return:          dictionary of features and possible values; if
                      there is more than one POS, list of such
                      dictionaries.
    @rtype:           dictionary of feature (string): possible values (list)
                      pairs or list of (pos, dictionary) pairs
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

def seg2string(segmentation, language='am', sep='-', transortho=True, features=False):
    """Convert a segmentation (triple with seg string as second item)
    to a series of spelled out morphemes, ignoring any alternation rules.
    @param language:     abbreviation for a language
    @type language:      string
    @param segmentation: triple with seg string as second item
    @type segmentation:  tuple
    @param sep:          character to separate morphemes in return string
    @type sep:           string
    @param transortho:   for languages written in Geez, whether to output this
    @type transortho:    boolean
    @param features:     whether to output feature labels
    @type features:      boolean
    @return:             word form
    @rtype:              string
    """
    language = morpho.get_language(language, segment=True)
    return language.segmentation2string(segmentation, sep=sep, transortho=transortho,
                                        features=features)

### Functions for debugging and creating FSTs

def cascade(language, pos, gen=False, phon=False, segment=False,
            verbose=False):
    '''Returns a cascade for the language and part-of-speech.
    @param language: abbreviation for a language, for example, 'gn'
    @type  language: string
    @param pos:    part-of-speech for the cascade, for example, 'v'
    @type  pos:    string
    @param phon:   whether the cascade is for phonology
    @type  phon:   boolean
    @param segment: whether the cascade is for segmentation
    @type  segment: boolean
    @param invert: whether to return the inverted cascade (for generation).
    @type  invert: boolean
    @param verbose: whether to print out various messages
    @type  verbose: boolean
    @return:       cascade for the the language and POS: a list of FSTs
    @rtype:        instance of the FSTCascade class (subclass of list)
    '''
    pos = get_pos(language, pos, phon=phon, segment=segment, load_morph=False, verbose=verbose)
    if not gen and pos.casc:
        return pos.casc
    if gen:
        if pos.casc_inv:
            return pos.casc_inv
        if pos.casc:
            casc_inv = pos.casc.inverted()
            pos.casc_inv = casc_inv
            return casc_inv
    pos.load_fst(True, create_fst=False, generate=gen, invert=gen, gen=gen,
                 segment=segment, verbose=verbose)
    if gen:
        return pos.casc_inv
    return pos.casc

def recompile(language, pos, phon=False, segment=False, gen=False, backwards=False,
              save=True, verbose=True):
    '''Recompiles the cascade FST for the language and part-of-speech.
    @param language: abbreviation for a language, for example, 'gn'
    @type  language: string
    @param pos:    part-of-speech for the cascade, for example, 'v'
    @type  pos:    string
    @param phon:   whether the cascade is for phonology
    @type  phon:   boolean
    @param segment: whether the cascade is for segmentation
    @type  segment: boolean
    @param gen:    whether to compile the cascade for generation (rather than analysis)
    @type  gen:    boolean
    @param backwards: whether to compile the FST from top (lexical) to bottom (surface)
                      for efficiency's sakd
    @type  backwards: boolean
    @param save:   whether to save the compiled cascade as an FST file
    @type  save:   boolean
    @param verbose: whether to print out various messages
    @type  verbose: boolean
    @return:       the POS morphology object
    @rtype:        instance of the POSMorphology class
    '''
    pos_morph = get_pos(language, pos, phon=phon, segment=segment, load_morph=False, verbose=verbose)
    fst = pos_morph.load_fst(True, segment=segment, generate=gen, invert=gen,
                             compose_backwards=backwards,
                             phon=phon, verbose=verbose)
    if not fst and gen == True:
        # Load analysis FST
        pos_morph.load_fst(True, verbose=True)
        # ... and invert it for generation FST
        pos_morph.load_fst(generate=True, invert=True, gen=True, verbose=verbose)
    if save:
        pos_morph.save_fst(generate=gen, segment=segment, phon=phon)
    return pos_morph

def test_fst(language, pos, string, gen=False, phon=False, segment=False,
             fst_label='', fst_index=0):
    """Test a individual FST within a cascade, identified by its label or its index,
    on the transduction of a string.
    @param language: abbreviation for a language, for example, 'gn'
    @type  language: string
    @param pos:    part-of-speech for the cascade, for example, 'v'
    @type  pos:    string
    @param phon:   whether the cascade is for phonology
    @type  phon:   boolean
    @param segment: whether the cascade is for segmentation
    @type  segment: boolean
    @param gen:     whether to use the inverted cascade (for generation).
    @type  gen:     boolean
    @param verbose: whether to print out various messages
    @type  verbose: boolean
    @return:       a list of analyses, each a list consisting of a root and a feature-structure set
    @rtype:        list of lists, each of the form [str, FSSet]
    """
    casc = cascade(language, pos, gen=gen, phon=phon, segment=segment)
    if not casc:
        print('No cascade found')
        return
    return casc.transduce1(string, fst_label=fst_label, fst_index=fst_index)

def get_pos(abbrev, pos, phon=False, segment=False, load_morph=False,
            guess=True, verbose=False):
    """Just a handy function for working with the POS objects when re-compiling
    and debugging FSTs.
    @param abbrev: abbreviation for a language, for example, 'am'
    @type  abbrev: string
    @param pos:    part-of-speech for the FST, for example, 'v'
    @type  pos:    string
    @param phon:   whether the FST is for phonology
    @type  phon:   boolean
    @param segment: whether the FST is for segmentation
    @type  segment: boolean
    @param verbose: whether to print out various messages
    @type  verbose: boolean
    @return:       POS object for the the language and POS
    @rtype:        instance of the POSMorphology class

    """
    load_lang(abbrev, segment=segment, phon=phon, load_morph=load_morph,
              guess=guess, verbose=verbose)
    lang = morpho.get_language(abbrev, phon=phon, segment=segment, load=load_morph,
                               verbose=verbose)
    if lang:
        return lang.morphology[pos]

def join(language, POS, segstring):
    """Join the sequence of morphemes in segstring, using rules (instances of Rule)
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
A = lambda w, raw=False: anal_word('am', w, raw=raw)
S = lambda w, raw=False, realize=True, features=True, transortho=True: seg_word('am', w, raw=raw, realize=realize, features=features, transortho=transortho)
P = lambda w, raw=False: phon_word('am', w, raw=raw)
G = lambda r, features=None: gen('am', r, features=features)
AF = lambda infile, outfile=None, raw=False, gram=True: anal_file('am', infile, outfile=outfile, raw=raw, gram=False)
SF = lambda infile, outfile=None: seg_file('am', infile, outfile=outfile)
PF = lambda infile, outfile=None: phon_file('am', infile, outfile=outfile)
