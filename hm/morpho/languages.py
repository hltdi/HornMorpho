"""
This file is part of HornMorpho, which is part of the PLoGS project.

    <http://homes.soic.indiana.edu/gasser/plogs.html>

    Copyleft 2011, 2012, 2013, 2016, 2018, 2019.
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
# maps additional language abbreviations to ISO code
CODES = {'ch': 'sgw', 'sl': 'stv', 'ks': 'gru'}

def get_lang_id(string):
    '''Get a language identifier from a string which may be the name
    of the language.'''
    lang = string if len(string) <= 3 else string.replace("'", "")[:2]
    return lang.lower()

def get_lang_dir(abbrev):
    return os.path.join(LANGUAGE_DIR, abbrev)

def load_lang(lang, phon=False, segment=False, load_morph=True,
              # False, '', or the name of a cache file
              cache=True, guess=True, poss=None, verbose=True):
    """Load Morphology objects and FSTs for language with lang_id."""
    lang_id = get_lang_id(lang)
    language = None
    if lang_id == 'am':
        from . import am_lang
        language = am_lang.AM
    elif lang_id == 'amh':
        # 2020.3.14: new Amharic
        from . import amh_lang
        language = amh_lang.AMH
    elif lang_id == 'ti':
        from . import ti_lang
        language = ti_lang.TI
    elif lang_id == 'om':
        from . import om_lang
        language = om_lang.OM
#    elif lang_id == 'stv':
#        from . import stv_lang
#        language = stv_lang.STV
    if language:
        # Attempt to load additional data from language data file;
        # and FSTs if load_morph is True.
        loaded = language.load_data(load_morph=load_morph, segment=segment,
                                    phon=phon, guess=guess, poss=poss, verbose=verbose)
        if not loaded:
#            print("No additional data")
            # Impossible to load data somehow
            pass
    else:
        if lang_id in CODES:
            lang_id = CODES[lang_id]
        # Create the language from scratch
        language = Language.make('', lang_id, load_morph=load_morph,
                                 segment=segment, phon=phon, guess=guess, poss=poss,
                                 verbose=verbose)
        if not language:
            # Impossible to make language with desired FST
            return False
    if cache != False:
        language.read_cache(segment=segment)
    LANGUAGES[lang_id] = language
    for code in language.codes:
        LANGUAGES[code] = language
    if language.backup:
        # If there's a backup language, load its data file so the translations
        # can be used.
        load_lang(language.backup, load_morph=False, guess=guess, verbose=verbose)
    return True

def get_language(language, load=True, phon=False, segment=False, guess=True,
                 load_morph=True, cache='', verbose=False):
    """Get the language with lang_id, attempting to load it if it's not found
    and load is True."""
    if isinstance(language, Language):
        return language
    lang_id = get_lang_id(language)
    lang = LANGUAGES.get(lang_id, None)
    if not lang:
        if load:
            if not load_lang(lang_id, phon=phon, segment=segment, guess=guess,
                             load_morph=load_morph, cache=cache,
                             verbose=verbose):
                return False
        return LANGUAGES.get(lang_id, None)
    if load_morph and not lang.morpho_loaded:
        lang.load_morpho(phon=phon, segment=segment, guess=guess)
        return lang
    if not load_morph:
        return lang
    fst = lang.get_fsts(phon=phon, segment=segment)
    if not fst and load:
        print("You cannot do different kinds of analysis or generation in the same session!")
        print("Please exit() and start a new session!")
        return
    return lang
    
#            load_morpho or not lang.get_fsts(phon=phon, segment=segment)):
#    if not lang_id in LANGUAGES:
#        if not load_lang(lang_id, phon=phon, segment=segment, guess=guess,
#                         load_morph=load, cache=cache,
#                         verbose=verbose):
#            return False
#    return LANGUAGES.get(lang_id, None)

#def get_language(language, load=True, phon=False, segment=False, guess=True,
#                 cache='', verbose=False):
#    """Get the language with lang_id, attempting to load it if it's not found
#    and load is True."""
#    if isinstance(language, Language):
#        return language
#    lang_id = get_lang_id(language)
#    lang = LANGUAGES.get(lang_id, None)
#    if lang:
#        fst = lang.get_fsts(phon=phon, segment=segment)
#        if not fst and load:
#            print("You cannot do both morphological analysis and segmentation in the same session!")
#            if segment:
#                print("Please exit() and start a new session to do segmentation!")
#            else:
#                print("Please exit() and start a new session to do morphological analysis!")
#            return
#    elif not load_lang(lang_id, phon=phon, segment=segment, guess=guess,
#                       load_morph=load, cache=cache,
#                       verbose=verbose):
#        return False
#    return LANGUAGES.get(lang_id, None)

def load_pos(language, pos, scratch=False):
    """Load FSTs for a single POS, overriding compiled FST if scratch is True."""
    language.morphology[pos].load_fst(scratch, recreate=True, verbose=True)

def load_langs(abbrev, l1, poss1, l2, poss2,
               load_lexicons=True, verbose=True):
    """Load two languages for translation between them."""
    load_lang(l1, phon=False, segment=False, load_morph=True,
              guess=False, poss=poss1, verbose=verbose)
    load_lang(l2, phon=False, segment=False, load_morph=True,
              guess=False, poss=poss2, verbose=verbose)
    lang1 = get_language(l1, verbose=verbose)
    lang2 = get_language(l2, verbose=verbose)
    return Multiling(abbrev, (lang1, poss1), (lang2, poss2),
                     load_lexicons=load_lexicons)
    
