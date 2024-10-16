"""
This file is part of HornMorpho, which is part of the PLoGS project.

    <http://homes.soic.indiana.edu/gasser/plogs.html>

    Copyleft 2011-2024.
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
import requests, tarfile
#import shutil
#from tqdm.auto import tqdm

###
### Loading languages
###

LANGUAGES = {}
# maps additional language abbreviations to ISO codes
CODES = {'am': 'a',
         'chh': 'ch', 'sgw': 'ch',
         'gz': 'g',
         'sl': 'stv', 'slt': 'stv', 'S': 'stv',
         'kst': 'k', 'gru': 'k', 'ks': 'k',
         'mh': 'muh',
         'ms': 'mvz', 'msq': 'mvz',
         'so': 'som', 's': 'som',
         'ti': 't',
         'T': 'te',
         'om': 'o', 'orm': 'o'}

ABBREV2LANG = {'a': 'አማርኛ',
               't': 'ትግርኛ',
               'o': 'Afaan Oromoo',
               'te': 'ትግረ',
               'g': 'ግዕዝ',
               'ch': 'ቸሃ',
               'eng': 'English',
               'stv': 'የስልጤ አፍ',
               'k': 'ክስታንኛ',
               'አ': 'አማርኛ',
               'ት': 'ትግርኛ'}

def lang_not_found_interactive(abbrev, language):
    response = input("Would you like to download the data for {}? ([y]es/[n]o)\n--> ".format(language))
    if not response or (response and response.lower() == 'y'):
        return True
    return False

def get_language_url(abbrev, format='tgz'):
    '''
    URL for the compressed language file in GitHub for the language with abbreviation abbrev.
    '''
    
    url = "https://github.com/hltdi/HornMorpho/raw/master/src/hm/languages/"
    lang = abbrev + "." + format
    return url + lang

def is_downloaded(abbrev):
    '''
    Is the language with abbrev downloaded?
    '''
    lang_dir = Language.get_lang_dir(abbrev)
    if lang_dir:
        return lang_dir
    return False

def download_language(abbrev, dest='', uncompress=True):
    '''
    Download the compressed language file for language with abbreviation abbrev.
    '''
    url = get_language_url(abbrev)
    language = ABBREV2LANG.get(abbrev)
    print("Downloading data for {}\n  from {}".format(language, url))
    fileout = dest or compressed_lang_filename(abbrev)
    with requests.get(url, stream=True) as r:
        total_size = int(r.headers.get('Content-Length'))
        print("File size {}".format(total_size))
#        print(r.content)
        chunk_size = 1024 * 2056
        with open(fileout, 'wb') as file:
            loaded = 0
            for i, chunk in enumerate(r.iter_content(chunk_size = chunk_size)):
                loaded += chunk_size
                fraction = min(100, round(100 * loaded / total_size))
                if fraction < 100:
                    print("...{}%".format(fraction))
                file.write(chunk)
    if uncompress:
        uncompress_lang(abbrev, source=dest)

def compressed_lang_filename(abbrev):
    '''
    Where to put or find the compressed file for a language.
    '''
    return os.path.join(LANGUAGE_DIR, abbrev + ".tgz")

def compress_lang(abbrev):
    '''
    Create a compressed tarball of all of the files in the language folder, except
    compiled FST files, given language abbreviation.
    '''
    updateQ = input("Did you update the version number?\n>>> ")
    if updateQ[0] not in ('y', 'Y'):
        return
    directory = Language.get_lang_dir(abbrev)
    outfile = compressed_lang_filename(abbrev)
    def exclude(tarinfo):
        filename = tarinfo.name
        for suff in ('fst', '.DS', '.cas', '.txt', '.lex'):
            if filename.endswith(suff):
                return None
        return tarinfo
    with tarfile.open(outfile, "w:gz") as tar:
        tar.add(directory, arcname=os.path.basename(directory), filter=exclude)

def uncompress_lang(abbrev, dest='', source=''):
    '''
    Uncompress a compressed language tarball.
    '''
    language = ABBREV2LANG.get(abbrev)
    filename = source or compressed_lang_filename(abbrev)
    print("Uncompressing data for {}\n in {}".format(language, filename))
    tar = tarfile.open(filename, "r:gz")
    tar.extractall(path=dest or LANGUAGE_DIR)
    tar.close()

def get_lang_id(string):
    '''
    Get a language identifier from a string which may be the name
    of the language.
    '''
    lang = string if len(string) <= 3 else string.replace("'", "")[:2]
    lang = lang.lower()
    if lang in CODES:
        lang = CODES[lang]
    return lang

#def get_lang_dir(abbrev):
#    return os.path.join(LANGUAGE_DIR, abbrev)

def get_downloaded_languages():
    languages = [l for l in os.listdir(LANGUAGE_DIR) if not l.startswith('.') and l not in ['e', 'eng']]
    if not languages:
        print("No Horn languages downloaded!")
        return False
    return languages

def load_lang(lang,
              lang_name='', phon=False, segment=False, load_morph=True,
              translate=False, pickle=True, recreate=False,
              # False, '', or the name of a cache file
              cache=True, guess=False, mwe=True, gen=False,
              v5=True, experimental=False, poss=None, verbose=True):
    """Load Morphology objects and FSTs for language with lang_id."""
#    if verbose:
#        print("load_lang {}, phon={}, seg={}, load_morph={}, guess={}".format(lang, phon, segment, load_morph, guess))
    lang_id = get_lang_id(lang)
    language = None
    if lang_id == 'stv':
        from . import stv_lang
        language = stv_lang.STV
    if language:
        # Attempt to load additional data from language data file;
        # and FSTs if load_morph is True.
        loaded = language.load_data(load_morph=load_morph, segment=segment, experimental=experimental,
                                    pickle=pickle, translate=translate, recreate=recreate, gen=gen,
                                    phon=phon, guess=guess, mwe=mwe,
                                    v5=v5,
                                    poss=poss, verbose=verbose)
        if not loaded:
            # Impossible to load data somehow
            return False
    else:
        # Create the language from scratch
        ees = False
        if lang_id in ['a', 't', 'g', 'ch', 'stv', 'te', 'mvz', 'muh']:
            ees = True
#            from . import ees
#            EES = ees.EES()
        lang_dir = is_downloaded(lang_id)
        if not lang_dir:
            print("Language {} not found !!".format(lang_name))
            download = lang_not_found_interactive(lang_id, lang_name)
            if download:
                download_language(lang_id)
            return False
        language = Language.make('', lang_id, load_morph=load_morph,
                                 pickle=pickle, translate=translate, gen=gen,
                                 ldir=lang_dir,
                                 experimental=experimental, mwe=mwe,
                                 segment=segment, phon=phon, guess=guess, recreate=recreate,
                                 poss=poss, ees=ees,
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
                  pickle=pickle, translate=translate, experimental=experimental,
                  guess=guess, verbose=verbose)
    return True

def get_language(language, **kwargs):
#    load=True, pickle=True,
#                 translate=False, experimental=False, phon=False, segment=False,
#                 guess=True, 
#                 v5=False,
#                 load_morph=True, cache='', verbose=False):
    """
    Get the language with lang_id, attempting to load it if it's not found
    and load is True.
    """
    if language not in ABBREV2LANG:
        print("HornMorpho has no language with the abbreviation {}".format(language))
        return False
    lang_name = ABBREV2LANG.get(language)
    load = kwargs.get('load') if 'load' in kwargs else True
    pickle = kwargs.get('pickle') if 'pickle' in kwargs else True
    guess = kwargs.get('guess') if 'guess' in kwargs else True
    load_morph = kwargs.get('load_morph') if 'load_morph' in kwargs else True
    translate = kwargs.get('translate', False)
    experimental = kwargs.get('experimental', False)
    phon = kwargs.get('phon', False)
    segment = kwargs.get('segment', False)
    v5 = kwargs.get('v5', True)
    verbose = kwargs.get('verbose', False)
    cache = kwargs.get('cache', None)
#    print("** Getting language, load = {}, load_morpho = {}, guess = {}".format(load, load_morph, guess))
    if isinstance(language, Language):
        return language
    lang_id = get_lang_id(language)
    lang = LANGUAGES.get(lang_id, None)
    if not lang:
        if load:
            if not load_lang(lang_id, lang_name=lang_name,
                             phon=phon, pickle=pickle,
                             segment=segment, guess=guess, experimental=experimental,
                             translate=translate, 
                             load_morph=load_morph, cache=cache,
                             v5=v5,
                             verbose=verbose):
                return False
        return LANGUAGES.get(lang_id, None)
    if load_morph and not lang.morpho_loaded:
        if v5:
            lang.load_morpho(phon=phon, guess=guess,
                              pickle=pickle, translate=translate)
        else:
            lang.load_morpho4(phon=phon, segment=segment, guess=guess,
                             experimental=experimental,
                             pickle=pickle, translate=translate)
        return lang
    if not load_morph:
        return lang
    fst = lang.get_fsts(phon=phon, segment=segment, experimental=experimental, v5=v5)
#    if not fst and load:
#        print("You cannot do different kinds of analysis or generation in the same session!")
#        print("Please exit() and start a new session!")
#        return
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
