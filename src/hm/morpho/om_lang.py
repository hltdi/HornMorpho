"""
This file is part of morfo.

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

Create Language, Morphology, and POSMorphology objects for Oromo.
"""
from . import language

OM = language.Language("Afaan Oromoo", 'orm',
                       seg_units=[['b', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'q', 'r', 't', 'w', 'x', 'y', "'", '-',
                                   # Only in foreign words
                                   'v', 'z',
                                   # Possible capital letters
                                   'B', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'Q', 'R', 'T', 'W', 'X', 'Y', 'V', 'Z'
                                   ],
                                  {'a': ['a', 'aa'], 'e': ['e', 'ee'], 'i': ['i', 'ii'], 'o': ['o', 'oo'], 'u': ['u', 'uu'],
                                   'c': ['c', 'ch'], 'd': ['d', 'dh'], 'n': ['n', 'ny'], 'p': ['p', 'ph'], 's': ['s', 'sh'],
                                   # Possible capital letters
                                   'A': ['A', 'Aa'], 'E': ['E', 'Ee'], 'I': ['I', 'Ii'], 'O': ['O', 'Oo'], 'U': ['U', 'Uu'],
                                   'C': ['C', 'Ch'], 'D': ['D', 'Dh'], 'N': ['N', 'Ny'], 'P': ['P', 'Ph'], 'S': ['S', 'Sh']}
                                  ])

## Create Morphology object and noun, verb, and copula POSMorphology objects for Oromo,
## including punctuation and ASCII characters that are part of the romanization.
OM.set_morphology(language.Morphology(
                                      pos_morphs=[('v',), ('n',)]))

## Default feature structures for POSMorphology objects
## Used in generation and production of citation form
OM.morphology['v'].defaultFS = \
    language.FeatStruct("[pos=v,tm=pst,sb=[-p1,-p2,-pl,-fem],cnj=None,-cont,-dat,-ins,-neg,case=bs,der=[-ps,-cs,-autoben],-1s_sb]")
OM.morphology['v'].FS_implic = {('tm', None): [['sb', None]],
                                ('inf', True): [['sb', None], ['tm', None]],
                                ('prt', True): [['sb', None], ['tm', None]],
                                ('ger', True): [['sb', None], ['tm', None]]}
# Citation form is infinitive
OM.morphology['v'].citationFS = \
    language.FeatStruct("[pos=v,+inf,tm=None,sb=None,cnj=None,-cont,-dat,-ins,-neg,case=bs,-1s_sb]")
OM.morphology['n'].defaultFS = \
    language.FeatStruct("[pos=n,cnj=None,case=bs,-gen,-fem,-pl,-def,-1s_sb]")
OM.morphology['n'].FS_implic = {}
OM.morphology['n'].citationFS = \
    language.FeatStruct("[pos=n,cnj=None,case=bs,-gen,-fem,-pl,-def,-1s_sb]")

def n_anal2string(anal, webdict=None, **kwargs):
    '''Convert a noun/adj analysis to a string.

    anal is ("(*)n", stem, citation, gramFS)
    '''
    stem = anal[1]
    citation = anal[2]
    fs = anal[3]
    # In case fs is anal[3] is None
    real_fs = anal[4]
    # Adjective in some cases?
    pos = 'noun'
    POS = '?POS: ' if '?' in anal[0] else 'POS: '
    s = POS + pos
    if stem:
        s += ', stem: ' + stem
    if citation:
        s += ', citation: ' + citation
    s += '\n'
    if fs:
        # Feature structure features
        # Case
        case = fs.get('case')
        if case:
            s += ' case: ' + case
            if fs.get('gen', False):
                s += '+gen'
            s += '\n'
        # Other features
        anygram = False
        fem = fs.get('fem', None)
        plr = fs.get('pl', None)
        if fem is not None:
            if anygram: s += ','
            if fem:
                s += ' feminine'
            else:
                s += ' masculine'
            anygram = True
        if plr is not None:
            if anygram: s += ','
            if plr:
                s += ' plural'
            else:
                s += ' singular'
            anygram = True
        if fs.get('def'):
            if anygram: s += ','
            s += ' definite'
            anygram = True
        if fs.get('cnj'):
            if anygram: s += ','
            s += ' conjunction: ' + fs.get('cnj')
            anygram = True
        if fs.get('1s_sb'):
            if anygram: s += ','
            s += ' 1s subj'
        if anygram:
            s += '\n'
    return s

def v_anal2string(anal, webdict=None, **kwargs):
    '''Convert a verb analysis to a string.

    anal is ("(*)v", root, citation, gramFS)
    '''
    root = anal[1]
    citation = anal[2]
    fs = anal[3]
    # In case fs is anal[3] is None
    real_fs = anal[4]
    pos = 'deverbal noun' if (real_fs.get('inf') or real_fs.get('agt')) else 'verb'
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
        # Feature structure features
        sb = fs.get('sb')
        der = fs.get('der')
        if sb:
            s += ' subject:'
            s += arg2string(sb)
        if der:
            ps = der.get('ps')
            cs = der.get('cs')
            ab = der.get('autoben')
            if ps or cs or ab:
                s += ' derivation:'
                if ps:
                    s += ' passive'
                if cs:
                    s += ' causative'
                if ab:
                    s += ' autobenefactive'
                s += '\n'
        anygram = False
        if fs.get('tm'):
            tam = fs.get('tm')
            s += ' TAM: '
            if tam == 'pst':
                s += 'past'
            elif tam == 'prs':
                s += 'present'
            elif tam == 'imv':
                s += 'imperative'
            elif tam == 'sub':
                s += 'subordinate'
            elif tam == 'contemp':
                s += 'contemporary'
            elif tam == 'prf':
                s += 'perfect'
            anygram = True
        if fs.get('neg'):
            if anygram: s += ','
            s += ' negative'
            anygram = True
        if fs.get('dat'):
            if anygram: s += ','
            s += ' 3pers/dative'
            anygram = True
        if fs.get('ins'):
            if anygram: s += ','
            s += ' 3pers/instrumental'
            anygram = True
        if fs.get('prt'):
            if anygram: s += ','
            s += ' participle'
            anygram = True
        if fs.get('ger'):
            if anygram: s += ','
            s += ' gerund'
            anygram = True
        if fs.get('inf'):
            if anygram: s += ','
            s += ' infinitive'
            anygram = True
        if fs.get('agt'):
            if anygram: s += ','
            s += ' agent'
            if fs.get('fem'):
                s += ' feminine'
            anygram = True
        if fs.get('case'):
            if anygram: s += ','
            s += ' case: ' + fs.get('case')
            anygram = True
        if fs.get('cont'):
            if anygram: s += ','
            s += ' continuative'
            anygram = True
        if fs.get('cnj'):
            if anygram: s += ','
            s += ' conjunction: ' + fs.get('cnj')
            anygram = True
        if fs.get('1s_sb'):
            if anygram: s += ','
            s += ' 1s subj'
        s += '\n'
    return s

def arg2string(fs, web=False):
    '''Convert an argument Feature Structure to a string.'''
    s = '' if web else ' '
    if fs.get('p1'):
        s += '1'
    elif fs.get('p2'):
        s += '2'
    else:
        s += '3'
    if fs.get('pl'):
        s += ', plur'
    else:
        s += ', sing'
    if not fs.get('pl') and not fs.get('p2') and not fs.get('p1'):
        if fs.get('fem'):
            s += ', fem'
        else:
            s += ', masc'
    if not web:
        s += '\n'
    return s

def v_get_citation(root, fs, guess=False):
    '''Return the canonical (infinitive) form for the root and featstructs in featstruct set fss.'''
    # Return root if no citation is found
    result = root
    # Unfreeze the feature structure
    fs = fs.unfreeze()
    # Update the feature structure to incorporate default (with or without vc and as)
    fs.update(OM.morphology['v'].citationFS)
    # Refreeze the feature structure
    fs.freeze()
    # Find the first citation form compatible with the updated feature structure
    citation = OM.morphology['v'].gen(root, fs, from_dict=False, guess=guess)
    if citation:
        result = citation[0][0]
    return result

## Function that converts analyses to strings
OM.morphology['v'].anal2string = lambda fss, webdict, **kwargs: v_anal2string(fss, webdict=webdict, **kwargs)
## Function that converts analyses to strings
OM.morphology['n'].anal2string = lambda fss, webdict, **kwargs: n_anal2string(fss, webdict=webdict, **kwargs)
## Functions that return the citation forms for words
OM.morphology['v'].citation = lambda root, fss, guess, vc_as, phonetic: v_get_citation(root, fss, guess)
## Functions that return the citation forms for words
OM.morphology['n'].citation = lambda root, fss, guess, vc_as, phonetic: root
