"""
This file is part of HornMorpho, which is part of the PLoGS project.

    <http://homes.soic.indiana.edu/gasser/plogs.html>

    Copyleft 2011-2023.
    PLoGS and Michael Gasser <gasser@indiana.edu>.

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
--------------------------------------------------------------------
Author: Michael Gasser <gasser@indiana.edu>

"""

from .language import *
# import anal_gui

###
### Loading languages
###

LANGUAGES = {}
# maps additional language abbreviations to ISO codes
CODES = {'am': 'amh',
         'chh': 'sgw',
         'gz': 'gez',
         'sl': 'stv', 'slt': 'stv', 'S': 'stv',
         'kst': 'gru',
#         'mh': 'muh',
#         'M': 'muh',
         'ms': 'mvz', 'msq': 'mvz',
#         'm': 'mvz',
         'so': 'som', 's': 'som',
         'ti': 'tir', 'tg': 'tir',
         'te': 'tig', 'T': 'tig',
         'om': 'orm', 'o': 'orm'}

FIDEL = ['a', 't', 'ch', 'g', 'k', 'm']

def get_lang_id(string):
    '''Get a language identifier from a string which may be the name
    of the language.'''
    lang = string if len(string) <= 3 else string.replace("'", "")[:2]
    lang = lang.lower()
    if lang in CODES:
        lang = CODES[lang]
    return lang

def get_lang_dir(abbrev):
    return os.path.join(LANGUAGE_DIR, abbrev)

def load_lang(lang, phon=False, segment=False, load_morph=True,
              translate=False, pickle=True, recreate=False, fidel=False,
              # False, '', or the name of a cache file
              cache=True, guess=False, mwe=True, gen=False,
              v5=False, experimental=False, poss=None, verbose=True):
    """Load Morphology objects and FSTs for language with lang_id."""
#    if verbose:
#        print("load_lang {}, phon={}, seg={}, load_morph={}, guess={}".format(lang, phon, segment, load_morph, guess))
    lang_id = get_lang_id(lang)
    language = None
    if lang_id == 'amh':
        # 2020.3.14: new Amharic
        from . import amh_lang
        language = amh_lang.AMH
    elif lang_id == 'tir':
        from . import ti_lang
        language = ti_lang.TI
    elif lang_id == 'orm':
        from . import om_lang
        language = om_lang.OM
#    elif lang_id == 'stv':
#        from . import stv_lang
#        language = stv_lang.STV
    if language:
        # Attempt to load additional data from language data file;
        # and FSTs if load_morph is True.
        loaded = language.load_data(load_morph=load_morph, segment=segment, experimental=experimental,
                                    pickle=pickle, translate=translate, recreate=recreate, gen=gen,
                                    phon=phon, guess=guess, mwe=mwe, fidel=fidel,
                                    v5=v5,
                                    poss=poss, verbose=verbose)
        if not loaded:
#            print("No additional data")
            # Impossible to load data somehow
            return False
    else:
#        if lang_id in CODES:
#            lang_id = CODES[lang_id]
        # Create the language from scratch
        ees = False
        if lang_id in ['sgw', 'gru', 'stv', 'tig', 'mvz', 'muh']:
            ees = True
#            from . import ees
#            EES = ees.EES()
#        print("** MAKING language")
        language = Language.make('', lang_id, load_morph=load_morph,
                                 pickle=pickle, translate=translate, gen=gen,
                                 experimental=experimental, mwe=mwe,
                                 segment=segment, phon=phon, guess=guess, recreate=recreate,
                                 poss=poss, ees=ees, fidel=fidel,
                                 v5=v5,
                                 verbose=verbose)
        if not language:
            # Impossible to make language with desired FST
            return False
    if cache != False:
        language.read_cache(segment=segment)
    LANGUAGES[lang_id] = language
    for code in language.codes:
        LANGUAGES[code] = language
#    if verbose:
#        print("Finished loading")
    if language.backup:
        if verbose:
            print("Loading backup language {}".format(language.backup))
        # If there's a backup language, load its data file so the translations
        # can be used.
        load_lang(language.backup, load_morph=False, recreate=recreate, mwe=mwe, gen=gen,
                  pickle=pickle, translate=translate, experimental=experimental, fidel=fidel,
                  guess=guess, verbose=verbose)
    return True

def get_language(language, **kwargs):
#    load=True, pickle=True,
#                 translate=False, experimental=False, fidel=False, phon=False, segment=False,
#                 guess=True, 
#                 v5=False,
#                 load_morph=True, cache='', verbose=False):
    """
    Get the language with lang_id, attempting to load it if it's not found
    and load is True.
    """
    load = kwargs.get('load') if 'load' in kwargs else True
    pickle = kwargs.get('pickle') if 'pickle' in kwargs else True
    guess = kwargs.get('guess') if 'guess' in kwargs else True
    load_morph = kwargs.get('load_morph') if 'load_morph' in kwargs else True
    translate = kwargs.get('translate', False)
    experimental = kwargs.get('experimental', False)
    fidel = kwargs.get('fidel', False)
    phon = kwargs.get('phon', False)
    segment = kwargs.get('segment', False)
    v5 = kwargs.get('v5', False)
    verbose = kwargs.get('verbose', False)
    cache = kwargs.get('cache', None)
#    print("** Getting language, load = {}, load_morpho = {}, guess = {}".format(load, load_morph, guess))
    if isinstance(language, Language):
        return language
    lang_id = get_lang_id(language)
    lang = LANGUAGES.get(lang_id, None)
    if not lang:
        if load:
            if not load_lang(lang_id, phon=phon, pickle=pickle,
                             segment=segment, guess=guess, experimental=experimental,
                             translate=translate, fidel=fidel,
                             load_morph=load_morph, cache=cache,
                             v5=v5,
                             verbose=verbose):
                return False
        return LANGUAGES.get(lang_id, None)
    if load_morph and not lang.morpho_loaded:
        if v5:
            lang.load_morpho5(phon=phon, guess=guess,
                              pickle=pickle, translate=translate)
        else:
            lang.load_morpho(phon=phon, segment=segment, guess=guess,
                             experimental=experimental,
                             pickle=pickle, translate=translate)
        return lang
    if not load_morph:
        return lang
    fst = lang.get_fsts(phon=phon, segment=segment, experimental=experimental, v5=v5)
    if not fst and load:
        print("You cannot do different kinds of analysis or generation in the same session!")
        print("Please exit() and start a new session!")
        return
    return lang

def load_pos(language, pos, scratch=False):
    """
    Load FSTs for a single POS, overriding compiled FST if scratch is True.
    """
    language.morphology[pos].load_fst(scratch, recreate=True, pos=pos, gemination=language.output_gemination, verbose=True)

def load_langs(abbrev, l1, poss1, l2, poss2, pickle=True, recreate=False,
               load_lexicons=True, verbose=True):
    """Load two languages for translation between them."""
    load_lang(l1, phon=False, segment=False, load_morph=True,
              pickle=pickle, recreate=recreate,
              guess=False, poss=poss1, verbose=verbose)
    load_lang(l2, phon=False, segment=False, load_morph=True,
              pickle=pickle, recreate=recreate,
              guess=False, poss=poss2, verbose=verbose)
    lang1 = get_language(l1, verbose=verbose)
    lang2 = get_language(l2, verbose=verbose)
    return Multiling(abbrev, (lang1, poss1), (lang2, poss2),
                     load_lexicons=load_lexicons)
