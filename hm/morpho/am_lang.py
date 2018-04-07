"""
This file is part of HornMorpho, which is part of the PLoGS project.

    <http://homes.soic.indiana.edu/gasser/plogs.html>

    Copyleft 2011, 2012, 2013, 2016, 2018.
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

Create Language, Morphology, and POSMorphology objects for Amharic.

All functions specific to Amharic morphology are here (or imported
from geez.py).
"""

from . import language
from .geez import *

### Various functions that will be values of attributes of Amharic Morphology
### and POSMorphology objects.

def vb_get_citation(root, fs, guess=False, vc_as=False):
    '''Return the canonical (prf, 3sm) form for the root and featstructs in featstruct set fss.

    If vc_as is True, preserve the voice and aspect of the original word.
    '''
    if root == 'al_e':
        return "'ale"
    # Return root if no citation is found
    result = root
    # Unfreeze the feature structure
    fs = fs.unfreeze()
    # Update the feature structure to incorporate default (with or without vc and as)
    fs.update(AM.morphology['v'].citationFS if vc_as else AM.morphology['v'].defaultFS)
    # Refreeze the feature structure
    fs.freeze()
    # Find the first citation form compatible with the updated feature structure
    citation = AM.morphology['v'].gen(root, fs, from_dict=False, guess=guess)
    if citation:
        result = citation[0][0]
    elif not vc_as:
        # Verb may not occur in simplex form; try passive
        fs = fs.unfreeze()
        fs.update({'vc': 'ps'})
        fs.freeze()
        citation = AM.morphology['v'].gen(root, fs, from_dict=False, guess=guess)
        if citation:
            result = citation[0][0]
    return result

def n_get_citation(root, fs, guess=False, vc_as=False):
    '''Return the canonical (prf, 3sm) form for the root and featstructs in featstruct set fss.

    If vc_as is True, preserve the voice and aspect of the original word.
    '''
    if fs.get('v'):
        # It's a deverbal noun
        return vb_get_citation(root, fs, guess=guess, vc_as=vc_as)
    else:
        return root    

def simplify(word):
    """Simplify Amharic orthography."""
    word = word.replace("`", "'").replace('H', 'h').replace('^', '').replace('_', '')
    return word

def orthographize(word):
    '''Convert phonological romanization to orthographic.'''
    word = word.replace('_', '').replace('I', '')
    return word

def cop_anal2string(anal):
    '''Convert a copula analysis to a string.

    anal is ("cop", "new", "new", gramFS)
    '''
    s = 'POS: copula'
    if anal[1]:
        s += ', root: <' + anal[1] + '>'
    s += '\n'
    fs = anal[3]
    if fs:
        sb = fs['sb']
        s += ' subj:'
        s += arg2string(sb)
        if fs.get('neg'):
            s += ' negative\n'
        cj = fs.get('cj2')
        if cj:
            s += ' conjunctive suffix: ' + cj + '\n'
    return s

def n_anal2string(anal):
    '''Convert a noun analysis to a string.

    anal is ("(*)n", root, citation, gramFS)
    '''
    root = anal[1]
    citation = anal[2]
    fs = anal[3]
    deverbal = fs and fs.get('v')
    POS = '?POS: ' if '?' in anal[0] else 'POS: '
    s = POS
    if deverbal:
        if deverbal == 'agt':
            s += 'agentive noun'
        elif deverbal == 'man':
            s += 'manner noun'
        elif deverbal == 'inf':
            s += 'infinitive'
        else:
            s += 'instrumental noun'
        if root:
            s += ', root: <' + root + '>'
        if citation:
            s += ', citation: ' + citation
    else:
        s += 'noun'
        if citation:
            s += ', stem: ' + citation
        elif root:
            s += ', stem: ' + root
    s += '\n'
    if fs:
        poss = fs.get('poss')
        if poss and poss.get('expl'):
            s += ' possessor:'
            s += arg2string(poss, True)
        gram = ''
        # For agent, infinitive, instrumental, give aspect and voice unless both are simple
        asp = fs.get('as')
        vc = fs.get('vc')
        rl = fs.get('rl')
        any_gram = False
        if deverbal and asp == 'it':
            gram += ' iterative'
            any_gram = True
        elif deverbal and asp == 'rc':
            if any_gram: gram += ','
            gram += ' reciprocal'
            any_gram = True
        if deverbal and vc == 'ps':
            if any_gram: gram += ','
            gram += ' passive'
            any_gram = True
        elif vc == 'tr':
            if any_gram: gram += ','
            gram += ' transitive'
            any_gram = True
        elif vc == 'cs':
            if any_gram: gram += ','
            gram += ' causative'
            any_gram = True
        if fs.get('neg'):
            # Only possible for infinitive
            if any_gram: gram += ','
            gram += ' negative'
            any_gram = True
        if fs.get('plr'):
            if any_gram: gram += ','
            gram += ' plural'
            any_gram = True
        if fs.get('def'):
            if any_gram: gram += ','
            any_gram = True
            gram += ' definite'
        if fs.get('dis'):
            if any_gram: gram += ','
            any_gram = True
            gram += ' distrib(Iyye-)'
        if rl and rl.get('acc'):
            if any_gram: gram += ','
            any_gram = True
            gram += ' accusative'
        if rl and rl.get('gen'):
            if any_gram: gram += ','
            any_gram = True
            gram += ' genitive'
#        der = fs.get('der')
#        if der and der.get('ass'):
#            if any_gram: gram += ','
#            any_gram = True
#            gram += ' assoc(-awi)'
        if any_gram:
            s += ' grammar:' + gram + '\n'
        pp = fs.get('pp')
        cnj = fs.get('cnj')
        if pp or cnj:
            if pp:
                s += ' preposition: ' + pp
            if cnj:
                if pp: s += ','
                s += ' conjunctive suffix: ' + cnj
            s += '\n'        
    return s    

def vb_anal2string(anal):
    '''Convert a verb analysis to a string.

    anal is ("(*)v", root, citation, gramFS)
    '''
    pos = 'verb'
    root = anal[1]
    citation = anal[2]
    fs = anal[3]
    POS = '?POS: ' if '?' in anal[0] else 'POS: '
    s = POS + pos
    if root:
        if '{' in root:
            # Segmented form; not root
            s += ', segmentation: ' + root
        else:
            s += ', root: <' + root + '>'
    if citation:
        s += ', citation: ' + citation
    s += '\n'
    if fs:
        sb = fs['sb']
        s += ' subject:'
        s += arg2string(sb)
        ob = fs.get('ob')
        if ob and ob.get('expl'):
            s += ' object:'
            s += arg2string(ob, True)
        s += ' grammar:'
        rl = fs.get('rl')
        tm = fs.get('tm')
        if tm == 'prf':
            s += ' perfective'
        elif tm == 'imf':
            s += ' imperfective'
        elif tm == 'j_i':
            s += ' jussive/imperative'
        elif tm == 'ger':
            s += ' gerundive'
        else:
            s += ' present'
        if fs.get('ax'):
            s += ', aux:alle'
        asp = fs.get('as')
        if asp == 'it':
            s += ', iterative'
        elif asp == 'rc':
            s += ', reciprocal'
        vc = fs.get('vc')
        if vc == 'ps':
            s += ', passive'
        elif vc == 'tr':
            s += ', transitive'
        elif vc == 'cs':
            s += ', causative'
        if fs.get('rel') or fs.get('neg'):
            if fs.get('rel'):
                s += ', relative'
                if rl and rl.get('acc'):
                    s += ', accusative'
                if fs.get('def'):
                    s += ', definite'
            if fs.get('neg'):
                s += ', negative'
        s += '\n'
        cj1 = fs.get('cj1')
        cj2 = fs.get('cj2')
        prep = fs.get('pp')
        if cj1 or cj2 or prep:
            any_affix = False
            if prep:
                any_affix = True
                s += ' preposition: ' + prep
            if cj1:
                if any_affix: s += ','
                s += ' conjunctive prefix: ' + cj1
            if cj2:
                if any_affix: s += ','
                s += ' conjunctive suffix: ' + cj2
            s += '\n'
    return s

def arg2string(fs, obj=False):
    '''Convert an argument Feature Structure to a string.'''
    s = ''
    if fs.get('p1'):
        s += ' 1'
    elif fs.get('p2'):
        s += ' 2'
    else:
        s += ' 3'
    if fs.get('plr'):
        s += ', plur'
    else:
        s += ', sing'
    if not fs.get('plr') and (fs.get('p2') or not fs.get('p1')):
        if fs.get('fem'):
            s += ', fem'
        elif not fs.get('frm'):
            s += ', masc'
    if obj:
        if fs.get('p2'):
            if fs.get('frm'):
                s += ', formal'
        if fs.get('prp'):
            if fs.get('l'):
                s += ', prep: -l-'
            else:
                s += ', prep: -b-'
    s += '\n'
    return s

def vb_anal_to_dict(root, fs):
    '''Convert a verb analysis Feature Structure to a dict.'''
    args = []
    # List of features that are true
    bools = []
    strings = {}

    gram = {}

    gram['root'] = root

    sbj = fs['sb']
    obj = fs.get('ob', None)
    vc = fs.get('vc')
    asp = fs.get('as')
    tm = fs['tm']
    cj1 = fs.get('cj1', None)
    cj2 = fs.get('cj2', None)
    prp = fs.get('pp', None)
    rl = fs.get('rl', {})

    # Subject and object
    prep = False
    formal = False
    labels = ['person', 'number', 'gender']
    if obj.get('expl'):
        if obj.get('p2'):
            formal = True
            labels.append('formality')
        prep = True
        labels.append('prepositional')
    args.append(labels)
    args1 = []
    args1.append(agr_to_list(sbj, 'subject', formal))
    if obj.get('expl'):
        args1.append(agr_to_list(obj, 'object', formal))
    args.append(args1)

    # TAM
    if tm == 'imf':
        strings['tense/mood'] = 'imperfective'
    elif tm == 'prf':
        strings['tense/mood'] = 'perfective'
    elif tm == 'ger':
        strings['tense/mood'] = 'gerundive'
    else:
        strings['tense/mood'] = 'jussive/imperative'

    # DERIVATIONAL STUFF
    if vc == 'ps':
        strings['voice'] = 'passive'
    elif vc == 'tr':
        strings['voice'] = 'transitive'
    elif vc == 'cs':
        strings['voice'] = 'causative'

    if asp == 'it':
        strings['aspect'] = 'iterative'
    elif asp == 'rc':
        strings['aspect'] = 'reciprocal'

    # NEGATION
    if fs.get('neg'):
        bools.append('negative')
    # RELATIVIZATION
    if fs.get('rel'):
        bools.append('relative')
    # CASE
    if rl and rl.get('acc'):
        bools.append('accusative')
    # CONJUNCTIONS AND PREPOSITIONS
    if cj1:
        strings['prefix conjunction'] = cj1
    if cj2:
        strings['suffix conjunction'] = cj2
    if prp:
        strings['preposition'] = prp

    gram['args'] = args
    gram['strings'] = strings
    gram['bools'] = bools

    return gram

def vb_dict_to_anal(root, dct, freeze=True):
    '''Convert a verb analysis dict to a Feature Structure.'''
    fs = FeatStruct()
    root = root or dct['root']

    # Arguments
    sbj = list_to_arg(dct, 'sbj')
    if dct.get('obj'):
        obj = list_to_arg(dct, 'obj')
    else:
        obj = FeatStruct()
        obj['expl'] = False
    fs['sb'] = sbj
    fs['ob'] = obj
    
    # TAM: labels are the same as FS values
    fs['tm'] = dct.get('tam', 'prf')

    # DERIVATIONAL STUFF
    fs['as'] = dct.get('asp', 'smp')
    fs['vc'] = dct.get('voice_am', 'smp')

    # OTHER GRAMMAR
    fs['neg'] = dct.get('neg', False)
    fs['rel'] = dct.get('rel', False)
    fs['acc'] = dct.get('acc', False)
    if dct.get('aux'):
        fs['aux'] = 'al'
    else:
        fs['aux'] = None

    # PREPOSITIONS and CONJUNCTIONS
    fs['pp'] = dct.get('prep_am')
    if fs['pp']:
        fs['sub'] = True

    fs['cj1'] = dct.get('preconj_am')
    if fs['cj1']:
        fs['sub'] = True

    fs['cj2'] = dct.get('sufconj_am')

    return [root, FSSet(fs)]

def agr_to_list(agr, cat, formal=False):
    '''Convert an agreement Feature Structure to a list.

    Category, then person, number, gender, formality (2nd prs), prepositional.
    '''
    gram = [cat]

    if agr.get('p1'):
        gram.append('1')
    elif agr.get('p2'):
        gram.append('2')
    else:
        gram.append('3')

    if agr.get('plr'):
        gram.append('plural')
    else:
        gram.append('singular')

    if not agr.get('p1') and not agr.get('plr'):
        # Gender only for 2nd and 3rd person singular
        if agr.get('fem'):
            gram.append('feminine')
        else:
            gram.append('masculine')
    else:
        gram.append('')

    if formal:
        if cat == 'object' and agr.get('p2'):
            if agr.get('frm'):
                gram.append('formal')
            else:
                gram.append('informal')

    if agr.get('prp'):
        if agr.get('b'):
            gram.append('b-')
        else:
            gram.append('l-')
    elif cat == 'object':
        gram.append('no')

    return gram

def list_to_arg(dct, prefix):
    '''Convert a dict to an argument Feature Structure.'''
    arg = FeatStruct()
    person = dct.get(prefix + '_pers')
    number = dct.get(prefix + '_num')
    gender = dct.get(prefix + '_gen')
    arg['expl'] = True

    # Person
    if person == '1':
        arg['p1'] = True
        arg['p2'] = False
    elif person == '2':
        arg['p2'] = True
        arg['p1'] = False
    else:
        # 3rd person the default
        arg['p1'] = False
        arg['p2'] = False
    # Number
    if number == 'plur':
        arg['plr'] = True
    else:
        # Singular the default
        arg['plr'] = False
    # Gender
    if person != '1':
        if gender == 'fem':
            arg['fem'] = True
        else:
            arg['fem'] = False

    # 2nd person: formality
    if person == '2':
        formality = dct.get(prefix + '_form')
        if formality == 'form':
            arg['frm'] = True
        else:
            # Informal the default
            arg['frm'] = False

    # Prepositional (object only)
    if prefix == 'obj':
        prep = dct.get(prefix + '_prep_am')
        if prep == 'l':
            arg['prp'] = 'l'
        elif prep == 'b':
            arg['prp'] = 'b'
        else:
            arg['prp'] = None

    return arg

def n_postproc(analysis):
    '''Postprocess a noun, replacing the root, if deverbal with postprocessed form.
    analysis is a root and a single FS.'''
    gram1 = analysis[1]
#    gram1 = list(analysis[1])[0]
    if analysis[0]:
        # There is a root
        if not gram1.get('v'):
            # This is not deverbal; convert the "root" (really the stem) to Geez
            # (It's a tuple, so can't mutate it.)
            analysis = (sera2geez(GEEZ_SERA['am'][1], analysis[0], lang='am'),) + analysis[1:]
#            analysis[0] = sera2geez(GEEZ_SERA['am'][1], analysis[0], lang='am')

## Create Language object for Amharic, including preprocessing, postprocessing,
## and segmentation units (phones).
AM = language.Language("Amharic", 'am',
              postproc=lambda form: sera2geez(GEEZ_SERA['am'][1], form, lang='am'),
              preproc=lambda form: geez2sera(GEEZ_SERA['am'][0], form, lang='am', simp=True),
              postpostproc=lambda form: postproc_root(form),
              stat_root_feats=['vc', 'as'],
              stat_feats=[['poss', 'expl'], ['cnj'], ['cj1'], ['cj2'], ['pp'], ['rel']],
              seg_units=[["a", "e", "E", "i", "I", "o", "u", "H", "w", "y", "'", "`", "_", "|", "*", "/"],
                         {"b": ["b", "bW"], "c": ["c", "cW"], "C": ["C", "CW"],
                          "d": ["d", "dW"], "f": ["f", "fW"], "g": ["g", "gW"],
                          "h": ["h", "hW"], "j": ["j", "jW"], "k": ["k", "kW"],
                          "l": ["l", "lW"], "m": ["m", "mW"], "n": ["n", "nW"],
                          "p": ["p", "pW"], "P": ["P", "PW"],
                          "N": ["N", "NW"], "q": ["q", "qW"], "r": ["r", "rW"],
                          "s": ["s", "sW"], "S": ["S", "SW"], "t": ["t", "tW"],
                          "T": ["T", "TW"], "v": ["v", "vW"], "x": ["x", "xW"],
                          "z": ["z", "zW"], "Z": ["Z", "ZW"],
                          "^": ["^s", "^S", "^h", "^hW", "^sW", "^SW"]}])

## Create Morphology object and noun, verb, and copula POSMorphology objects for Amharic,
## including punctuation and ASCII characters that are part of the romanization.
AM.set_morphology(language.Morphology(
                             pos_morphs=[('cop',), ('n',), ('v',)],
                             # Exclude ^ and - (because it can be used in compounds)
                             punctuation=r'[“‘”’–—:;/,<>?.!%$()[\]{}|#@&*\_+=\"፡።፣፤፥፦፧፨]',
                             # Include digits?
                             characters=r'[a-zA-Zሀ-ፚ\'`^]'))

### Assign various attributes to Morphology and POSMorphology objects

# Functions that simplifies Amharic orthography
AM.morphology.simplify = lambda word: simplify(word)
AM.morphology.orthographize = lambda word: orthographize(word)

# Function that performs trivial analysis on forms that don't require romanization
AM.morphology.triv_anal = lambda form: no_convert(form)

## Functions converting between feature structures and simple dicts
AM.morphology['v'].anal_to_dict = lambda root, anal: vb_anal_to_dict(root, anal)
AM.morphology['v'].dict_to_anal = lambda root, anal: vb_dict_to_anal(root, anal)

## Default feature structures for POSMorphology objects
## Used in generation and production of citation form
AM.morphology['v'].defaultFS = \
    language.FeatStruct("[pos=v,tm=prf,as=smp,vc=smp,sb=[-p1,-p2,-plr,-fem],ob=[-expl,-p1,-p2,-plr,-fem,-b,-l,-prp,-frm],cj1=None,cj2=None,pp=None,ax=None,-neg,-rel,-sub,-def,-acc,-ye,rl=[-p,-acc]]")
AM.morphology['v'].FS_implic = {'rel': ['def', 'sub'],
                                'cj1': ['sub'],
                                'pp': ['rel', 'sub'],
                                ('pp', ('be', 'le', 'ke', 'wede', 'Inde', 'sIle', 'Iske', 'Iyye')): [['rl', ['p']]],
                                'def': ['rel', 'sub'],
                                'l': ['prp'],
                                'b': ['prp'],
                                'ob': [['expl']]}
# defaultFS with voice and aspect unspecified
AM.morphology['v'].citationFS = language.FeatStruct("[pos=v,tm=prf,sb=[-p1,-p2,-plr,-fem],ob=[-expl],cj1=None,cj2=None,pp=None,ax=None,-neg,-rel,-sub,-def,-ye,-acc,rl=[-p,-acc]]")
AM.morphology['n'].defaultFS = \
    language.FeatStruct("[pos=n,-acc,-def,-neg,-fem,-itu,as=smp,cnj=None,-dis,-gen,-plr,poss=[-expl,-p1,-p2,-plr,-fem,-frm],pp=None,v=None,vc=smp,rl=[-p,-gen,-acc]]")
AM.morphology['n'].FS_implic = {'poss': [['expl'], 'def'],
                                ('pp', ('be', 'le', 'ke', 'wede', 'Inde', 'sIle', 'Iske')): [['rl', ['p']]],
                                ('gen', True): [['rl', ['gen']]],
                                ('acc', True): [['rl', ['acc']]]}
# defaultFS with voice and aspect unspecified
AM.morphology['n'].citationFS = language.FeatStruct("[-acc,-def,-neg,cnj=None,-dis,-gen,-plr,poss=[-expl],pp=None,v=inf]")
AM.morphology['cop'].defaultFS = language.FeatStruct("[cj2=None,-neg,ob=[-expl],-rel,sb=[-fem,-p1,-p2,-plr,-frm],-sub,tm=prs]")

## Functions that return the citation forms for words
AM.morphology['v'].citation = lambda root, fss, guess, vc_as: vb_get_citation(root, fss, guess, vc_as)
AM.morphology['n'].citation = lambda root, fss, guess, vc_as: n_get_citation(root, fss, guess, vc_as)

## Functions that convert analyses to strings
AM.morphology['v'].anal2string = lambda fss: vb_anal2string(fss)
AM.morphology['n'].anal2string = lambda fss: n_anal2string(fss)
AM.morphology['cop'].anal2string = lambda fss: cop_anal2string(fss)

## Postprocessing function for nouns (treats roots differently)
# AM.morphology['v'].postproc = lambda analysis: vb_postproc(analysis)
AM.morphology['n'].postproc = lambda analysis: n_postproc(analysis)
# AM.morphology['cop'].postproc = lambda analysis: cop_postproc(analysis)

def load_anal(pos='v', lex=True, guess=False):
    if lex:
        AM.morphology[pos].load_fst(True, verbose=True)
    if guess:
        AM.morphology[pos].load_fst(True, guess=True, verbose=True)

def load_gen(pos='v', lex=True, guess=False):
    if lex:
        AM.morphology[pos].load_fst(True, generate=True, invert=True, verbose=True)
    if guess:
        AM.morphology[pos].load_fst(True, generate=True, invert=True, guess=True, verbose=True)

def postproc_root(root):
    """Final adjustments to romanized root."""
    # Replace __ with space.
    if '//' in root:
        root = root.replace('//', ' ')
    return root
