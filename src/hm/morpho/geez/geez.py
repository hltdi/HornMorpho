"""
This file is part of HornMorpho, which is a project of PLoGS.

    <http://homes.soic.indiana.edu/gasser/plogs.html>

    Copyleft 2018, 2019, 2020, 2022, 2023. PLoGS and Michael Gasser <gasser@indiana.edu>.

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

-----------------------------------------------------------------
Support for romanizing Geez and geezifying romanized EthSem languages.

Makes use of a modified version of the SERA conventions for romanizing
Geez (Yitna & Yaqob, 1997).

2019.12
-- Gemination
-- Chaha palatalized consonants

"""

import re, os

DATA_DIR = os.path.dirname(__file__)

## AfSem segments
VOWELS = 'aeEiIou@AOU'
CONSONANTS = ["h", "l", "H", "m", "^s", "r", "s", "^s", "x", "q", "Q", "b", "t", "c",
              "^h", "n", "N", "'", "k", "K", "w", "`", "z", "Z", "y", "d", "j", "g",
              "T", "C", "P", "S", "^S", "f", "p"]
GEMINATION_GEEZ = "፟"
GEMINATION_ROMAN = '_'
EPENTHETIC = 'I'

## Regular expression objects for converting between "conventional" and
## "modified" SERA
SERA_GEM_RE = re.compile(r'(\w)(\1)')
SERA_GEM_SUB = r'\1_'
MINE_GEM_RE = re.compile(r'(\w)_')
MINE_GEM_SUB = r'\1\1'
SERA_VV_RE = re.compile(r'([aeEiou])([aeEiou])')
MINE_VV_SUB = r"\1'\2"
SERA_VI_RE = re.compile(r'([aeEiou])I')
MINE_VI_SUB = r"\1'"
SERA_V0_RE = re.compile(r'(\s)([aeEiou])')
MINE_V0_SUB = r"\1'\2"
SERA_I0_RE = re.compile(r'(\s)I')
MINE_I0_SUB = r"\1'"
MINE_IC_RE = re.compile(r"'([^aeEiou])")
SERA_IC_SUB = r"I\1"
SERA_LARYN_A = re.compile(r"['`hH]a.*")

# Punctuation to preserve in Geez->SERA->Geez translation
KEEP_PUNC = ",./"

# Special Geez characters
GEEZ_PUNCTUATION = "፡።፣፤፥፦፧፨"
# Non-Geez punctuation used in EES languages
EES_PUNCTUATION = '"?!'
GEEZ_NUMERALS = "፩፪፫፬፭፮፯፰፱፲፳፴፵፶፷፸፹፺፻፼"

## Geez consonants and vowels in traditional order
GEEZ_ALPHA_CONSONANTS = ['h', 'l', 'H', 'm', '^s', 'r', 's', 'x', 'q', 'Q', 'b',
                        't', 'c', '^h', 'n', 'N', "'", 'k', 'K', 'w',
                        "`", 'z', 'Z', 'y', 'd', 'j', 'g', 'T', 'C', 'P',
                        'S', '^S', 'f', 'p']
GEEZ_ALPHA_VOWELS = ['e', '@', 'u', 'i', 'a', 'E', 'A', 'I', 'o']

## Root boundaries and separators
ROOT_LEFT = '<'
ROOT_RIGHT = '>'
ROOT_SEP = '_'
ROOT_GEM = ':'
ROOT_Y = '።'

## Amharic palatals
AM_PAL = {'t': 'c', 'd': 'j', 'T': 'C', 's': 'x', 'z': 'Z', 'n': 'N', 'l': 'y'}

CONVERT_GEEZ = {
    # palatalize
    '^': {'ት': 'ች', 'ድ': 'ጅ',  'ስ': 'ሽ',  'ዝ': 'ዥ',  'ን': 'ኝ',  'ጥ': 'ጭ',  'ል': 'ይ',  'ቅ': 'ቕ',  'ክ': 'ኽ',  'ግ': 'ጝ',  'ሕ': '𞟥'},
    '-^': {'ች': 'ት', 'ጅ': 'ድ', 'ሽ': 'ስ', 'ዥ': 'ዝ',  'ኝ': 'ን',  'ጭ': 'ጥ',  'ይ': 'ል',  'ቕ': 'ቅ',  'ኽ': 'ክ',  'ጝ': 'ግ',  '𞟥': 'ሕ'}
    }

AMH_NORM = \
str.maketrans("ሐሑሒሓሔሕሖኅኁኂኃኄኅኆዐዑዒዓዔዕዖሠሡሢሣሤሥሦፀፁፂፃፄፅፆ",
              "ሀሂሂሃሄህሆሀሂሂሃሄህሆአኡኢኣኤእኦሰሱሲሳሴስሶጸጹጺጻጼጽጾ")

### TOP-LEVEL FUNCTIONS

def get_language(lang='am'):
    if lang in GEEZ_SERA:
        return GEEZ_SERA[lang]
    else:
        conv_path = os.path.join(DATA_DIR, lang + "_conv_sera.txt")
        dicts = read_conv(conv_path)
        GEEZ_SERA[lang] = dicts
        return dicts

def get_table(lang='am', fromgeez=True):
    language = get_language(lang)
    return language[0 if fromgeez else 1]

def geezify_alts(form, lang='am', gemination=True):
    """Return a list of possible geez outputs for roman form."""
    forms = convert_labial(form)
    g = [geezify(f, lang=lang, gemination=gemination) for f in forms]
    return g

#def geezify_root(root, lang='am'):
#    """Convert a sequence of root consonants (and other characters
#    used in HornMorpho representations of roots) to Geez.
#    >>> geezify_root("sbr")
#    '<ስ_ብ_ር>'
#    >>> geezify_root("bakn")
#    '<ባክ_ን>'
#    >>> geezify_root("Ty_q")
#    '<ጥ_ይ:_ቅ>'
#    >>> geezify_root("x|qWTqWT")
#    '<ሽቍ_ጥ_ቍ_ጥ>'
#    """
#    table = GEEZ_SERA.get(lang, [[],[]])[1]
#    if table:
#        return root2geez(table, root, lang=lang)

def normalize(string):
    return string.translate(AMH_NORM)

def degeminate(form, geez=True):
    """
    Remove the gemination character, if any.
    """
    if geez:
        return form.replace(GEMINATION_GEEZ, '')
    return form.replace(GEMINATION_ROMAN, '')

def to_sads(char, lang='ees', spec=None):
    '''
    Convert a Geez char to its ሳድስ version.
    '''
#    print("** to sads {}".format(char))
    rom = romanize(char, lang=lang, normalize=False)
    if rom[0] == '^':
        rom0 = rom[:2]
    else:
        rom0 = rom[0]
    g = geezify(rom0, lang=lang)
    if spec:
        g = convert_char(g, spec)
    return g

def convert_char(char, spec):
    '''
    Convert Geez char, given a spec such as ^ (palatalize), -^ (depalatalize).
    '''
#    print("** convert char {}, spec {}".format(char, spec))
    if spec in CONVERT_GEEZ:
        return CONVERT_GEEZ[spec].get(char)
    else:
        print("Conversion spec {} is not in CONVERT_GEEZ dict!".format(spec))
        return char

def geezify_morph(morph, lang='am', alt=True, gemination=True):
    """
    Convert a morpheme to Geez. If it begins with a vowel, prepend '.
    If it's already Geez, don't change it.
    """
    if is_geez(morph):
        if alt:
            return [morph]
        return morph
    if not morph:
        return '0'
    # other possible prepended chars? use RE to separate prepended chars?
    x, pre, morph = morph.rpartition('{')
    if morph[0] in VOWELS:
        morph = "'" + morph
    morph = pre + morph
    if alt:
        return geezify_alts(morph, lang='am', gemination=gemination)
    else:
        return geezify(morph, lang='am', gemination=gemination)

def is_geez_punc(form):
    '''
    Is this Geez punctuation or ? or !?
    '''
    return form in GEEZ_PUNCTUATION or form in EES_PUNCTUATION

def no_convert(form):
    '''
    Skip conversion for simple cases: non-Geez, punctuation, numerals.
    '''
    if not is_geez(form) or form in GEEZ_PUNCTUATION or is_geez_num(form):
        return form

def is_geez_num(form):
    '''Is form a Geez numeral?'''
    return set(form) & set(GEEZ_NUMERALS)

def is_geez(form):
    '''Are any of the chars in form Geez?

    form must be UTF8 decoded.
    '''
    for char in form:
        c = ord(char)
        if 4608 <= c <= 5017:
            return True
        if 11648 <= c <= 11742:
            # Ethiopic Extended
            return True
        if 43776 <= c <= 43822:
            # Ethiopic Extended-A
            return True
        if 124896 <= c <= 124926:
            # Ethiopic Extended-B
            return True
#        # new characters for Feqede Gurage orthography
#        if 57412 <= c <= 57415:
#            return True
    return False

def convert_labial(form):
    """For Amharic and Tigrinya, convert *We to *o, *WI to *u.
    For syllables other than the following, return only this form.
    kWe, ^hWe, gWe, qWe, kW(I), ^hW(I), gW(I), kW(I)
    """
    if 'W' in form:
        accum = []
        already_added = False
        changed = False
        previous = ''
        reject_original = False
        for index, char in enumerate(form):
            if already_added:
                if char == '_':
                    continue
                else:
                    already_added = False
            elif char == 'W':
                previous = form[index-1]
                if previous not in ['k', 'g', 'q', 'Q']:
                    reject_original = True
                elif previous == '^' and form[index-2] != 'h':
                    reject_original = True
                if len(form) > index + 1:
                    if form[index+1] == 'e':
                        accum.append('o')
                        already_added = True
                        changed = True
                    elif form[index+1] == 'I':
                        accum.append('u')
                        already_added = True
                        changed = True
                    elif form[index+1] == '_':
                        if len(form) > index + 2:
                            if form[index+2] in 'aiuE':
                                accum.append('_')
                            elif form[index+2] == 'e':
                                accum.append('_o')
                                already_added = True
                                changed = True
                            elif form[index+2] == 'I':
                                accum.append('_u')
                                already_added = True
                                changed = True
                            else:
                                accum.append('_u' + form[index+2])
                                already_added = True
                                changed = True
                        else:
                            accum.append('_')
                    elif form[index+1] in 'aiuE':
                        accum.append('W')
                    else:
                        accum.append('u')
                        changed = True
            else:
                accum.append(char)
        if changed:
            altform = ''.join(accum)
            if reject_original:
                return [altform]
            else:
                return [form, altform]
    return [form]

def read_conv(filename, simple=False):
    '''Create translation tables (dict), using simple conversions if simple.'''
    fileobj = open(filename, encoding='utf8')
    # encoding information
    convs = fileobj.read().split()
    syl2seg = {}
    seg2syl = {}
    for conv in convs:
        conv_pair = conv.split('=')
        syl = conv_pair[0]
        seg = conv_pair[-1] if simple else conv_pair[1]
        if ',' in seg and len(seg) > 2:
            # There is more than one way to romanize the character; first is the default
            segs = seg.split(',')
            syl2seg[syl] = segs[0]
            for s in segs:
                seg2syl[s] = syl
        else:
            if '*' in seg:
                # Only associate syl to seg
                syl2seg[syl] = seg.replace('*', '')
            else:
                syl2seg[syl] = seg
                seg2syl[seg] = syl
    return syl2seg, seg2syl

#def larynA(form):

def sera2geez(table, form, lang='am', gemination=False, deepenthesize=True, laryngealA=False, gem_geez=GEMINATION_GEEZ):
    '''
    Convert form in SERA to Geez, using translation table.
    (This is increasingly ugly; it needs to be cleaned up at some point.)
    '''
    if not table:
        table = get_table(lang, False)
    # First delete gemination characters
    if not gemination:
        form = form.replace(GEMINATION_ROMAN, '')
    # there may be epenthetic vowels
    if deepenthesize:
        form = form.replace(EPENTHETIC, '')
    if laryngealA:
        form = form.larynA(form)
    # Segment
    res = ''
    n = 0
    nochange = False
    # punctuation before roman chars
    while n < len(form):
        char = form[n]
#        print("char {}".format(char))
        if char == 'O' and lang == 'am':
            # Combining 'O' following vowel other than 'a'
            trans = table.get('wo')
        elif char == '@' and lang == 'am':
            # 'ityoPyawi@n -> ኢትዮጵያዊያን
            trans = table.get('ya')
        elif n < len(form) - 1:
            next_char = form[n + 1]
#            print(" next_char {}".format(next_char))
            if next_char in VOWELS:
                if n < len(form) - 2 and lang == 'am' and form[n + 2] == 'O' and next_char == 'a':
                    # Combining 'O' in Amharic; lElaOc -> ሌሎች
                    trans = table.get(char + 'o')
                    n += 1
                elif n < len(form) - 2 and lang == 'stv' and form[n + 2] in VOWELS:
                    # long Silte vowel
                    trans = table.get(form[n : n + 3], char + next_char + form[n + 2])
                    n += 1
                elif next_char == 'O' and lang == 'am':
                    # bEtOc -> ቤቶች
                    trans = table.get(char + 'o')
                elif next_char == '@' and lang == 'am':
                    trans = table.get(char + 'a')
                else:
                    trans = table.get(form[n : n + 2], char + next_char)
                n += 1
            elif next_char == 'W' or next_char == 'Y' or char == '^':
                # Consonant represented by 2 roman characters
#                print("*** char {}, next char {}".format(char, next_char))
                if n < len(form) - 2 and form[n + 2] in VOWELS:
                    # followed by vowel
                    chars3 = form[n:n+3]
                    vowel2 = form[n+2]
                    if vowel2 == 'O' and lang == 'am':
#                        print("**** Replacing O with o")
                        vowel2 = 'o'
                        chars3 = chars3[:-1] + 'o'
                    elif vowel2 == '@' and lang == 'am':
                        vowel2 = 'a'
                        chars3 = chars3[:-1] + 'a'
                    trans = table.get(chars3, char + next_char + vowel2)
                    n += 1
                # followed by consonant
                elif n < len(form) - 2 and form[n + 2] == GEMINATION_ROMAN:
                    # followed by gemination character
                    if n < len(form) - 3 and form[n + 3] in VOWELS:
                        # and then a vowel
                        char = form[n:n+2] + form[n+3]
                        trans = table.get(char, char)
                        trans += gem_geez
                        n += 2
                    else:
                        char = form[n:n+2]
                        trans = table.get(char, char)
                        trans += gem_geez
                        n += 1
                else:
                    trans = table.get(form[n : n + 2], char + next_char)
                n += 1
            elif next_char == GEMINATION_ROMAN:
                 if n < len(form) - 2 and form[n + 2] in VOWELS:
                    v = form[n + 2]
                    if v == 'O' and lang == 'am':
                        # Combining 'O' in Amh following gemination; wendm_Oc
                        v = 'o'
                    trans = table.get(char + v, char + v) + gem_geez
                    n += 2
                 else:
                    trans = table.get(char, char) + gem_geez
                    n += 1
            else:
                trans = table.get(char, char)
        elif char == GEMINATION_ROMAN:
            trans = gem_geez
        else:
#            if prepunc and char in table:
#                prepunc = False
            trans = table.get(char, char)
        res += trans
        n += 1
    return res

def geezify(form, lang='am', gemination=False, deepenthesize=True, laryngealA=False, gem_geez=GEMINATION_GEEZ):
    return \
      sera2geez(get_table(lang, False), form, lang=lang,
                gemination=gemination, deepenthesize=deepenthesize, gem_geez=gem_geez)

def romanize(form, lang='am', normalize=True, gemination=False):
    return geez2sera(get_table(lang, True), form, lang=lang, gemination=gemination, simp=normalize)

def geezify_root(root, lang='am'):
    """Convert a sequence of root consonants (and other characters
    used in HornMorpho representations of roots) to Geez.
    >>> geezify_root("sbr")
    '<ስ_ብ_ር>'
    >>> geezify_root("bakn")
    '<ባክ_ን>'
    >>> geezify_root("Ty_q")
    '<ጥ_ይ:_ቅ>'
    >>> geezify_root("x|qWTqWT")
    '<ሽቍ_ጥ_ቍ_ጥ>'
    """
    table = GEEZ_SERA.get(lang, [[],[]])[1]
    if table:
        return root2geez(table, root, lang=lang)

def root2geez(table, root, lang='am'):
    '''Convert a verb root to Geez.'''
    # Irregular
    if root == "al_e":
        return "<አለ:>"
    res = ROOT_LEFT
    n = 0
    while n < len(root):
        sep = True
        char = root[n]
        if n < len(root) - 1:
            next_char = root[n + 1]
            if next_char == '|' or next_char == '_':
                sep = False
            if char == '|':
                trans = ''
                sep = False
            elif char == '_':
                trans = ROOT_GEM
            elif next_char in VOWELS:
                if n < len(root) - 2 and lang == 'stv' and root[n + 2] in VOWELS:
                    # long Silte vowel
                    trans = table.get(root[n : n + 3], char + next_char + root[n + 2])
                    n += 1
                else:
                    trans = table.get(root[n : n + 2], char + next_char)
                n += 1
                sep = False
            elif next_char == 'W' or char == '^':
                # Consonant represented by 2 roman characters
                if n < len(root) - 2:
                    if root[n + 2] in VOWELS:
                        # followed by vowel
                        trans = table.get(root[n : n + 3], char + next_char + root[n + 2])
                        n += 1
                        sep = False
                    else:
                        trans = table.get(root[n : n + 2], char + next_char)
                        if root[n + 2] == '|':
                            n += 1
                            sep = False
                        elif root[n + 2] == '_':
                            sep = False
                else:
                    # Last consonant
                    trans = table.get(root[n : n + 2], char + next_char)
                    sep = False
                n += 1
            elif char == 'Y':
                trans = ROOT_Y
            else:
                trans = table.get(char, char)
        else:
            # Last consonant
            if char == 'Y':
                trans = ROOT_Y
            else:
                trans = table.get(char, char)
            sep = False
        res += trans
        if sep:
            res += ROOT_SEP
        n += 1
    return res + ROOT_RIGHT

def geez2sera(table, form, lang='am', simp=False, delete='',
              gemination=False, report_simplification=False):
    '''Convert form in Geez to SERA, using translation table.'''
    if not table:
        table = get_table(lang, True)
    if form.isdigit():
        if report_simplification:
            return form, []
        return form
    res = ''
    simplifications = []
    geminated = []
    for char in form:
        if char == GEMINATION_GEEZ:
            if gemination:
                geminated.append(len(res))
                res += '_'
                continue
            else:
                continue
        translation = table.get(char)
        if translation:
            res += translation
        else:
            res += char
    if simp:
        if report_simplification:
            res_simp, simpn = simplify_sera(res, language=lang, record=True)
            simplifications += simpn
        else:
            res_simp = simplify_sera(res, language=lang, record=False)
        res = res_simp
    if delete:
        res = res.replace(delete, '')
    if gemination and geminated:
        res1 = ''
        for i, c in enumerate(res):
            if c in VOWELS and i+1 in geminated:
                res1 += '_' + c
            elif c == '_':
                if res[i-1] not in VOWELS:
                    res1 += '_'
            else:
                res1 += c
        res = res1
    if report_simplification:
        return res, simplifications
    return res

def geez2sera_file(table, infile, outfile, first_out=True, simp=False):
    '''Convert forms in infile from Geez to SERA, using translation table, writing them in outfile.'''
    inobj = open(infile)
    outobj = open(outfile, 'a')
    res = ''
    for line in inobj.readlines():
        n = 0
        while n < len(line):
            char = line[n]
            if n < len(line) - 1:
                next_char = line[n + 1]
                if next_char in VOWELS:
                    trans = table.get(line[n : n + 2], char + next_char)
                    n += 1
                else:
                    trans = table.get(char, char)
            else:
                trans = table.get(char, char)
            res += trans
            n += 1
    outobj.write(res)

def sera2geez_file(table, infile, outfile, has_encoding = False):
    '''Convert forms infile from SERA to Geez, using translation table, writing them in outfile.'''
    outobj = open(outfile, 'a')
    inobj = open(infile)
    res = []
    text = inobj.read()
    lines = text.split('\n')
    if has_encoding:
        # Leave off the lines with encoding info
        lines = lines[2:]
    all_res = ''
    n_lines = 0
    for line in lines:
        res = ''
        words = line.split(' ')
        for word in words:
            for char in word:
                res += table.get(char, char)
            res += ' '
        res = res.encode('utf8')
        if outfile:
            outobj.write(res)
            outobj.write('\n')
        all_res += res
        n_lines += 1
        if n_lines % 1000 == 0:
            print('Transcribed', n_lines, 'lines', 'line', res)
    inobj.close()
    outobj.close()

def simplify_sera(text, language='am', record=False):
    '''Convert alternate consonants to the default for Amharic or Tigrinya.
    '''
#    # Protect ^hW (not needed because ኋ, etc. converted to hW)
#    text = text.replace('^hW', '!!!')
    # ^h -> h, ^s -> s, ^S -> S
    simps = []
#    simplified = False
    if record:
        for i, char in enumerate(text):
#            print("** {}: {}, {}".format(text, i, char))
            if char == 'H':
                simps.append(('h', 'H'))
#                simplified = True
            elif char == "`":
                simps.append(("'", '`'))
#                simplified = True
            elif char == '^':
                s = text[i+1]
                simps.append((s, '^' + s))
#            elif char == 'A' and i == 1 and text[0] in 'Hh':
#                simps.append(('a', 'A'))
#            elif char == 'A' and i == 2 and text[:2] == "^h":
#                simps.append(('e', char))
    text = text.replace('^', '')
#    # Replace ^hW
#    text = text.replace('!!!', '^hW')
    # Amharic only: H, `, K
    if language == 'am':
        # H -> h
        text = text.replace('H', 'h')
        # ` -> '
        text = text.replace('`', "'")
        # Protect Ke
        text = text.replace('Ke', '!!')
        # K -> h
        text = text.replace('K', 'h')
        # Replace Ke
        text = text.replace('!!', 'Ke')
        # ሙዋ ፉዋ ቡዋ -> ሟ ፏ ቧ
        text = text.replace("muwa", "mWa")
        text = text.replace('fuwa', 'fWa')
        text = text.replace('buwa', 'bWa')
        # Replace special character A with a, in any position
        # This is not currently recorded as a simplification
        text = text.replace('A', 'a')
        if text.endswith('We'):
            text = text[:-2] + 'o'
        # Do the same thing for "...W"?
#        if text.startswith("hA"):
#            text = "ha" + text[2:]
#        if text.startswith("'A"):
#            text = "'a" + text[2:]
    if record:
        return text, simps
    return text

def to_real_sera(text, phon=True):
    '''Convert text from "modified" to "standard" SERA.

    Delete initial glottal stop before vowel; insert I if no explicit vowel. If phon, C_ -> CC.
    '''
    # Replace ' with I before consonant
    text = MINE_IC_RE.sub(SERA_IC_SUB, text)
    # Delete other glottal stops
    text = text.replace("'", "")
    if phon:
        text = MINE_GEM_RE.sub(MINE_GEM_SUB, text)
    return text

def from_real_sera(text, phon=True, punc=True, language='am'):
    '''Convert text from "standard" to "modified" SERA.

    Add glottal stop before initial vowel, deleting I if it's the vowel. If phon, CC -> C_.
    VV -> V'V.
    '''
    text0 = text[0]
    if not phon and text0 == 'I':
        text = "'" + text[1:]
    elif text0 in VOWELS:
        text = "'" + text
    text = SERA_V0_RE.sub(MINE_V0_SUB, text)
    text = SERA_I0_RE.sub(MINE_I0_SUB, text)
    if phon:
        text = SERA_GEM_RE.sub(SERA_GEM_SUB, text)
        if language == 'am':
            # Replace ^h, ^s, ^S, ` with h, s, S, ' but only in Amharic
            text = text.replace('^h', 'h').replace('^s', 's').replace('^S', 'S').replace('`', "'")
    # Add glottal stop between adjacent vowels
    text = SERA_VV_RE.sub(MINE_VV_SUB, text)
    # Replace I with glottal stop
    text = text.replace('I', "'")
    # Change Le to La
    text = text.replace("'e", "'a").replace("`e", "`a").replace("he", "ha").replace("He", "Ha").replace("^he", "^ha")
    # Separate punctuation
    if punc:
        text = PUNC0_RE.sub(PUNC0_SUB, text)
        text = PUNC_RE.sub(PUNC_SUB, text)
    return text

def to_real_sera_file(infile, outfile=None, phon=True, language='am'):
    '''Convert text in infile from "modified" to "conventional" SERA.

    Delete initial glottal stop before vowel; insert I if no explicit vowel. If phon, C_ -> CC.
    '''
    in_f = open(infile)
    if outfile:
        out_f = open(outfile, 'w')
    for line in in_f:
        converted = to_real_sera(line, phon=phon)
        if outfile:
            out_f.write(converted)
        else:
            print(converted, end=' ')
    in_f.close()
    if outfile:
        out_f.close()

def from_real_sera_file(infile, outfile=None, phon=True, language='am'):
    '''Convert text in infile from "conventional" to "modified" SERA.'''
    in_f = open(infile)
    if outfile:
        out_f = open(outfile, 'w')
    for line in in_f:
        converted = from_real_sera(line, phon=phon, language=language)
        if outfile:
            out_f.write(converted)
        else:
            print(converted, end=' ')
    in_f.close()
    if outfile:
        out_f.close()

## GEEZ<->SERA (modified) conversion tables
GEEZ_SERA = {'am': read_conv(os.path.join(DATA_DIR, 'am_conv_sera.txt'))
#             'ti': read_conv(os.path.join(DATA_DIR, 'ti_conv_sera.txt')),
#             'sgw': read_conv(os.path.join(DATA_DIR, 'sgw_conv_sera.txt')),
#             'gru': read_conv(os.path.join(DATA_DIR, 'gru_conv_sera.txt')),
#             'sgw_old': read_conv(os.path.join(DATA_DIR, 'sgw_old_conv_sera.txt')),
#             'stv': read_conv(os.path.join(DATA_DIR, 'stv_conv_sera.txt'))
}

def geez_alpha(s1, s2, pos1 = 0, pos2 = 0):
    """Comparator function for two strings or lists using Geez order."""
    if s1 == s2:
        return 0
    elif pos1 >= len(s1):
        return -1
    elif pos2 >= len(s2):
        return 1
    else:
        seg1 = s1[pos1]
        seg2 = s2[pos2]
        if seg1 == seg2:
            return geez_alpha(s1, s2, pos1 + 1, pos2 + 1)
        elif seg1 in VOWELS and seg2 in VOWELS:
            if GEEZ_ALPHA_VOWELS.index(seg1) < GEEZ_ALPHA_VOWELS.index(seg2):
                return -1
            else:
                return 1
        elif seg1 == 'W':
            return 1
        elif seg2 == 'W':
            return -1
        elif seg1 in CONSONANTS and seg2 in CONSONANTS:
            if GEEZ_ALPHA_CONSONANTS.index(seg1) < GEEZ_ALPHA_CONSONANTS.index(seg2):
                return -1
            else:
                return 1
        # Otherwise one of the vowels is a missing 6th order vowel
        elif seg1 in CONSONANTS:
            if seg2 in VOWELS and 5 < GEEZ_ALPHA_VOWELS.index(seg2):
                return -1
            else:
                return 1
        elif seg2 in CONSONANTS:
            if seg1 in VOWELS:
                if GEEZ_ALPHA_VOWELS.index(seg1) < 5:
                    return -1
                else:
                    return 1
            else:
                return -1
        else:
            # Both are non-Ethiopic characters
            return cmp(s1[pos1:], s2[pos2:])
