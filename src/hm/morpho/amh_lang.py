"""
This file is part of morfo, which is part of the PLoGS project.

    <http://homes.soic.indiana.edu/gasser/plogs.html>

    Copyleft 2011, 2012, 2013, 2016, 2018, 2020, 2022.
    PLoGS and Michael Gasser <gasser@indiana.edu>.

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

Create Language, Morphology, and POSMorphology objects for Amharic.

All functions specific to Amharic morphology are here (or imported
from geez.py).
"""

from . import language
#from .geez import *
from .utils import segment, allcombs, isnumstring
from .rule import *
from .ees import *

print("Loading data for አማርኛ from amh_lang")

ROM2GEEZ = {'sI': "ስ", 'lI': "ል", 'bI': "ብ", 'IskI': "እስክ", 'IndI': "እንድ",
            'm': "ም", 'Inji': "እንጂ", 'na': "ና", 'sa': "ሳ", 's': "ስ", 'ma': "ማ",
            'sIle': "ስለ", 'le': "ለ", 'Iyye': "እየ", 'Iske': "እስከ", 'Inde': "እንደ", 'ke': "ከ", 'be': "በ", 'wede': "ወደ"}

ALT_PHONES = ['^s', '^S', 'H', '^h', "`", '^sW', '^SW', '^hW']
SIMP_PHONES = ['s', 'S', 'h', "'", 'sW', 'SW', 'hW']

# Features to exclude from string resulting from seg2string
SEG_DROP_FEATS = ['ውልድ']

### Analysis of numerals, etc.

#def trivial_anal(string):
#    if string.isdigit():
#        return int(string)
#    if isnumstring(string):
#        return float(string)
#    return no_convert(string)

### Various functions that will be values of attributes of Amharic Morphology
### and POSMorphology objects.

def vb_get_citation(root, fs, guess=False, vc_as=False, phonetic=True):
    '''
    Return the canonical (prf, 3sm) form for the root and featstructs in featstruct fs.

    If vc_as is True, preserve the voice and aspect of the original word.
    '''
#    print("** Getting V citation for {}:{}, vc_as: {}, phonetic {}".format(root, fs.__repr__(), vc_as, phonetic))
    if 'lemma' in fs and not phonetic:
        return fs['lemma']
    citation = ''
    if root in ('hlw', 'hl_w', 'al_'):
        return "'al_e"
    # Return root if no citation is found
    result = root
    # Unfreeze the feature structure
    fs = fs.unfreeze()
    fsa, fsv = fs.get('as'), fs.get('vc')
    # Update the feature structure to incorporate default (with or without vc
    # and as)
    fs.update(AMH.morphology['v'].defaultFS)
    # For non-passive te- verbs, te- is citation form
    if vc_as or fs.get('lexav') == True:
        # Lexical entry with explicit as, vc features
        fs.update({'as': fsa, "vc": fsv})
    elif fs.get('lexip') == True:
        # Lexical entry for as=it,vc=ps and as=it,vc=tr
        fs.update({'as': 'it', 'vc': 'ps'})
    elif fs.get('lexrp') == True:
        # Lexical entry for as=rc, vc=ps and as=rc,vc=tr
        fs.update({'as': 'rc', 'vc': 'ps'})
    elif fs.get('smp') == False:
        # No vc=smp form, vc=ps is base/citation form
        fs.update({'vc': 'ps'})
    # Refreeze the feature structure
    fs.freeze()
#    print("** fs {}".format(fs.__repr__()))
    # Find the first citation form compatible with the updated feature structure
    if ' ' in root:
        # This is a light verb, just generate the actual verb
        root_split = root.split()
        citation = AMH.morphology['v'].gen(root_split[-1], fs, from_dict=False,
                                           phon=True, postproc=False, guess=guess)
        if citation:
            result = ' '.join(root_split[:-1]) + ' ' + citation[0][0]
    else:
        citation = AMH.morphology['v'].gen(root, fs, from_dict=False,
                                           phon=True, postproc=False, guess=guess)
        if citation:
            result = citation[0][0]
    if not citation:
        if not vc_as:
            # Verb may not occur in simplex form; try passive
            fs = fs.unfreeze()
            fs.update({'vc': 'ps'})
            fs.freeze()
            citation = AMH.morphology['v'].gen(root, fs, from_dict=False, guess=guess)
            if citation:
                result = citation[0][0]
    return result

def n_get_citation(root, fs, guess=False, vc_as=False, phonetic=True):
    '''
    Only return citation for deverbal nouns.
    '''
    if fs.get('v') and fs['v'] == 'inf':
#        deriv = fs['v']
#        if deriv == 'man':
#            fss = language.FeatStruct("[pos=n,-def,v={}]".format(deriv))
#        else:
        # For agt, inf, and ins we need the aspect and voice features
        fsa, fsv = fs.get('as'), fs.get('vc')
        fss = language.FeatStruct("[pos=n,-def,-plr,-neg,-acc,v={}, as={}, vc={},cnj=None,prep=None]".format(deriv, fsa, fsv))
        citation = AMH.morphology['n'].gen(root, fss, from_dict=False, phon=True,
                                           postproc=False, guess=guess)
        if citation:
            return citation[0][0]
        else:
#            print("** Unable to generated deverbal noun")           
            return None
    else:
        return None

def simplify(word):
    """Simplify Amharic orthography."""
    word = word.replace("`", "'").replace('H', 'h').replace('^', '').replace('_', '')
    return word

def orthographize(word):
    '''Convert phonological romanization to orthographic.'''
    word = word.replace('_', '').replace('I', '')
    return word

def webfv(webdict, feature, value):
    if webdict != None:
        webdict[feature] = value

def cop_anal2string(anal, webdict=None, **kwargs):
    '''
    Convert a copula analysis to a string.
    '''
    s = ' POS = copula'
    root = anal[1]
    citation = anal[2]
    if kwargs.get('lemma_only'):
        return "{}".format(citation)
    fs = anal[3]
    if kwargs.get('lemma_only'):
        return "ነው"
    webfv(webdict, 'POS', 'copula')
    webfv(webdict, 'pos', 'cop')
    webfv(webdict, 'root', "ነ-")
#    root = anal.get('root')
#    if root:
#        s += ', root: ' + root
    s += ', lemma = ነው/nǝw, gloss = be'
    s += '\n'
#    fs = anal.get('gram')
    if fs:
        sb = fs['sb']
        s += ' subject ='
        s += arg2string(sb)
        webfv(webdict, 'subject', arg2string(sb, web=True))
        if fs.get('neg'):
            s += ' negative\n'
            webfv(webdict, 'negative', True)
        cj = fs.get('cj2')
        if cj:
            webfv(webdict, 'conj suffix', roman2geez(cj))
            s += ' conj suffix = ' + cj + '\n'
    return s

def n_anal2string(anal, webdict=None, **kwargs):
    '''Convert a noun analysis to a string.

    anal is ("(*)n", root, citation, gramFS)
    '''
    pos = anal[0]
    root = anal[1]
    citation = anal[2]
    if kwargs.get('lemma_only'):
        return "{}".format(citation)
    fs = anal[3]
    deverbal = fs and fs.get('v')
    POS = " POS = "
#    POS = '?POS: ' if '?' in anal[0] else 'POS: '
    s = POS
    root = AMH.postproc_root(AMH.morphology.get('n'), root, fs)
    webfv(webdict, 'POS', 'noun')
    webfv(webdict, 'pos', 'n')
    if deverbal:
        if deverbal == 'agt':
            s += 'agentive noun'
            webfv(webdict, 'deverbal', 'agentive')
        elif deverbal == 'man':
            s += 'manner noun'
            webfv(webdict, 'deverbal', 'manner')
        elif deverbal == 'inf':
            webfv(webdict, 'deverbal', 'infinitive')
            s += 'infinitive'
        else:
            webfv(webdict, 'deverbal', 'instrumental')
            s += 'instrumental noun'
        if root:
            s += ', root = ' + root
            if citation:
                root = "{}({})".format(root, citation)
            webfv(webdict, 'root', root)
        if citation:
            s += ', lemma = ' + citation
        if 't' in fs:
            if 'eng' in fs['t']:
                gloss = fs['t']['eng']
                s += ', gloss = ' + gloss
#            webfv(webdict, 'citation', citation)
    else:
        s += 'noun'
#        rc = geezify(root)
        rc = root
        if citation:
            rc = "{}({})".format(root, citation)
        webfv(webdict, 'root', rc)
        if citation:
            s += ', lemma = ' + citation
        elif root:
            s += ', lemma = ' + root
        if 't' in fs:
            if 'eng' in fs['t']:
                gloss = fs['t']['eng']
                s += ', gloss = ' + gloss
    s += '\n'
    if fs:
        poss = fs.get('poss')
        if poss and poss.get('expl'):
            s += ' possessor:'
            s += arg2string(poss, True)
            webfv(webdict, 'possessor', arg2string(poss, True, True))
        gram = ''
        # For agent, infinitive, instrumental, give aspect and voice unless both are simple
        asp = fs.get('as')
        vc = fs.get('vc')
        any_gram = False
        if deverbal and asp == 'it':
            gram += ' iterative'
            any_gram = True
            webfv(webdict, 'aspect', 'iterative')
        elif deverbal and asp == 'rc':
            if any_gram: gram += ','
            gram += ' reciprocal'
            any_gram = True
            webfv(webdict, 'aspect', 'reciprocal')
        if deverbal and vc == 'ps':
            if any_gram: gram += ','
            gram += ' passive'
            any_gram = True
            webfv(webdict, 'voice', 'passive')
        elif vc == 'tr':
            if any_gram: gram += ','
            gram += ' transitive'
            any_gram = True
            webfv(webdict, 'voice', 'transitive')
        elif vc == 'cs':
            if any_gram: gram += ','
            gram += ' causative'
            any_gram = True
            webfv(webdict, 'voice', 'causative')
        if fs.get('neg'):
            # Only possible for infinitive
            if any_gram: gram += ','
            gram += ' negative'
            any_gram = True
            webfv(webdict, 'negative', '+')
        if fs.get('plr'):
            if any_gram: gram += ','
            gram += ' plural'
            any_gram = True
            webfv(webdict, 'number', 'plural')
        if fs.get('def'):
            if any_gram: gram += ','
            any_gram = True
            gram += ' definite'
            webfv(webdict, 'definite', '+')
        if fs.get('dis'):
            if any_gram: gram += ','
            any_gram = True
            gram += ' distrib(Iyye-)'
            webfv(webdict, 'distributive', '+')
        if fs.get('acc'):
            if any_gram: gram += ','
            any_gram = True
            gram += ' accusative'
            webfv(webdict, 'accusative', '+')
        if fs.get('gen'):
            if any_gram: gram += ','
            any_gram = True
            gram += ' genitive'
            webfv(webdict, 'genitive', '+')
        if any_gram:
            s += ' other:' + gram + '\n'
        pp = fs.get('prep')
        cnj = fs.get('cnj')
        if pp or cnj:
            if pp:
                s += ' preposition = ' + pp
                webfv(webdict, 'preposition', roman2geez(pp))
            if cnj:
                if pp: s += ','
                s += ' conj suffix = ' + cnj
                webfv(webdict, 'conj suffix', roman2geez(cnj))
            s += '\n'
    return s

def vb_anal2string(anal, webdict=None, **kwargs):
    '''Convert a verb analysis to a string.

    anal is ("(*)v", root, citation, gramFS)
    '''
#    print("verb anal {}".format(anal))
    pos = 'verb'
    if 'noroot' in kwargs:
        root = None
    else:
        root = anal[1]
    if 'nolemma' in kwargs:
        citation = None
    else:
        citation = anal[2]
    if 'nogram' in kwargs:
        fs = ''
    else:
        fs = anal[3]
#    POS = '?POS: ' if '?' in anal[0] else 'POS: '
    POS = ' POS = '
    s = POS + pos
    if kwargs.get('lemma_only'):
        return "{}".format(citation)
    webfv(webdict, 'POS', 'verb')
    webfv(webdict, 'pos', 'v')
    if root:
#        print("root: {}".format(root))
        if '{' in root:
            # Segmented form; not root
            s += ', segmentation = ' + root
        else:
            root = AMH.postproc_root(AMH.morphology['v'], root, fs)
            s += ', root = ' + root
#        else:
#            s += ', root: <' + root + '>'
#        rc = '<' + root + '>'
        if citation:
            root = "{}({})".format(root, citation)
        webfv(webdict, 'root', root)
    if citation:
#        citation = AMH.finalize_citation(citation)
        s += ', lemma = ' + citation
    if 't' in fs:
        if 'eng' in fs['t']:
            gloss = fs['t']['eng']
            s += ', gloss = ' + gloss
    s += '\n'
    if fs:
        sb = fs['sb']
        s += ' subject ='
        s += arg2string(sb)
        webfv(webdict, 'subject', arg2string(sb, web=True))
        ob = fs.get('ob')
        if ob and ob.get('expl'):
            s += ' object ='
            s += arg2string(ob, True)
            webfv(webdict, 'object', arg2string(ob, True, web=True))
        s += ' aspect/voice/tense ='
        rl = fs.get('rl')
        tm = fs.get('tm')
        if tm == 'prf':
            s += ' perfective'
            webfv(webdict, 'TAMH', 'perfective')
        elif tm == 'imf':
            s += ' imperfective'
            webfv(webdict, 'TAMH', 'imperfective')
        elif tm == 'j_i':
            s += ' jussive/imperative'
            webfv(webdict, 'TAMH', 'jussive/imperative')
        elif tm == 'ger':
            s += ' gerundive'
            webfv(webdict, 'TAMH', 'gerundive')
        else:
            s += ' present'
            webfv(webdict, 'TAMH', 'present')
        if fs.get('ax'):
            s += ', aux:alle'
            webfv(webdict, 'auxiliary', 'alle')
        asp = fs.get('as')
        if asp == 'it':
            s += ', iterative'
            webfv(webdict, 'aspect', 'iterative')
        elif asp == 'rc':
            s += ', reciprocal'
            webfv(webdict, 'aspect', 'reciprocal')
        vc = fs.get('vc')
        if vc == 'ps':
            s += ', passive'
            webfv(webdict, 'voice', 'passive')
        elif vc == 'tr':
            s += ', transitive'
            webfv(webdict, 'voice', 'transitive')
        elif vc == 'cs':
            s += ', causative'
            webfv(webdict, 'voice', 'causitive')
        if fs.get('rel') or fs.get('neg'):
            if fs.get('rel'):
                s += ', relative'
                webfv(webdict, 'relative', True)
                if rl and rl.get('acc'):
                    s += ', accusative'
                    webfv(webdict, 'accusative', True)
                if fs.get('def'):
                    s += ', definite'
                    webfv(webdict, 'definite', True)
            if fs.get('neg'):
                s += ', negative'
                webfv(webdict, 'negative', True)
        s += '\n'
        cj1 = fs.get('cj1')
        cj2 = fs.get('cj2')
        prep = fs.get('pp')
        if cj1 or cj2 or prep:
            any_affix = False
            if prep:
                any_affix = True
                s += ' preposition = ' + prep
                webfv(webdict, 'preposition', roman2geez(prep))
            if cj1:
                if any_affix: s += ','
                s += ' conj prefix = ' + cj1
                webfv(webdict, 'conj prefix', roman2geez(cj1))
            if cj2:
                if any_affix: s += ','
                s += ' conj suffix = ' + cj2
                webfv(webdict, 'conj suffix', roman2geez(cj2))
            s += '\n'
    return s

def arg2string(fs, obj=False, web=False):
    '''Convert an argument Feature Structure to a string.'''
    s = '' if web else ' '
    if fs.get('p1'):
        s += '1'
    elif fs.get('p2'):
        s += '2'
    else:
        s += '3'
    if fs.get('plr'):
        s += ' plur'
    else:
        s += ' sing'
    if not fs.get('plr') and (fs.get('p2') or not fs.get('p1')):
        if fs.get('fem'):
            s += ' fem'
        elif not fs.get('frm'):
            s += ' mas'
    if obj:
        if fs.get('p2'):
            if fs.get('frm'):
                s += ' frml'
        if fs.get('prp'):
            if fs.get('l'):
                s += ' prep: ል'
            else:
                s += ' prep: ብ'
    if not web:
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

    # TAMH
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
        strings['prefix conj'] = cj1
    if cj2:
        strings['suffix conj'] = cj2
    if prp:
        strings['preposition'] = prp

    gram['args'] = args
    gram['strings'] = strings
    gram['bools'] = bools

    return gram

def vb_dict_to_anal(root, dct, freeze=True):
    '''Convert a verb analysis dict to a Feature Structure.'''
    fs = language.FeatStruct()
    root = root or dct['root']

    # Arguments
    sbj = list_to_arg(dct, 'sbj')
    if dct.get('obj'):
        obj = list_to_arg(dct, 'obj')
    else:
        obj = language.FeatStruct()
        obj['expl'] = False
    fs['sb'] = sbj
    fs['ob'] = obj

    # TAMH: labels are the same as FS values
    fs['tm'] = dct.get('tam', 'prf')

    # DERIVATIONAL STUFF
    fs['as'] = dct.get('asp', 'smp')
    fs['vc'] = dct.get('voice_am', 'smp')

    # OTHER GRAMHMAR
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
        gram.append('plur')
    else:
        gram.append('sing')

    if not agr.get('p1') and not agr.get('plr'):
        # Gender only for 2nd and 3rd person singular
        if agr.get('fem'):
            gram.append('fem')
        else:
            gram.append('mas')
    else:
        gram.append('')

    if formal:
        if cat == 'object' and agr.get('p2'):
            if agr.get('frm'):
                gram.append('frml')
            else:
                gram.append('infrml')

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
    arg = language.FeatStruct()
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
    if number == 'plural':
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

def preproc_root(root, fs, pos):
    """
    Preprocess root for generation.
    """
    if is_geez(root):
        anal = AMH.morphology['v'].anal(root, preproc=True)
        if anal:
            root, ffss = anal[0]
            cls = ffss.get('cls')
            root, fs = language.Language.dflt_procroot("{}:{}".format(root, cls), fs)
        else:
#            print("Couldn't analyze {}".format(root))
            return root, fs
    else:
        root, fs = language.Language.dflt_procroot(root, fs)
    return root, fs

def postpostproc_root(root, fs, phonetic=True, simplifications=None):
    """
    Convert root to root:class format, also changing internal
    HM root representation to an alternate conventional
    representation.
    """
#    print("** postprocessing {}, simps {}".format(root, simplifications))
    if phonetic:
        root = AMH.convert_root(root)
    elif simplifications:
        root = complicate_stem(root, simplifications)
#    if 'cls' not in fs:
#        print("No cls for {} {}".format(root, fs.__repr__()))
    return "<{}:{}>".format(root, fs.get('cls', ''))

def postproc_nroot(root, fs, phonetic=True, simplifications=None):
    """
    Convert citation (lemma) to conventional phonetic representation.
    """
#    print("** postprocessing {}, simps {}".format(root, simplifications))
    root_conv = root
    if phonetic:
        root_conv = AMH.convert_root(root)
    elif simplifications:
        root = complicate_stem(root, simplifications)
    if fs and fs.get('pos') == 'n_dv':
        return "<{}:{}>".format(root_conv, fs['cls'])
    else:
        return "{}|{}".format(geezify(root), root_conv)

def dflt_postproc_root(root, fs, phonetic=True, simplifications=None):
    if phonetic:
        return AMH.convert_root(root)
    elif simplifications:
        root = complicate_stem(root, simplifications)
    return geezify(root)

def postproc_word(word, ipa=False, phon=True, ortho_only=False,
                  phonetic=True):
    """
    Convert output word to ortho|phon representation, also
    changing internal HM representation to an alternate
    conventional representation.
    """
#    print("** Amh postprocessing {}, phon={}".format(word, phon))
    if '//' in word:
        word = word.replace('//', ' ')
    if is_geez(word):
        ortho = word
        word = romanize(word)
    else:
        ortho = geezify(word, deepenthesize=phon)
    if ortho_only:
        return ortho
    if phonetic:
        word = AMH.convert_phones(word, epenthesis=phon, ipa=ipa)
    return "{}|{}".format(ortho, word)

def postproc_root(root):
    """Final adjustments to romanized root."""
    # Replace __ with space.
    if '//' in root:
        root = root.replace('//', ' ')
    return root

## Create Language object for Amharic, including preprocessing, postprocessing,
## and segmentation units (phones).
AMH = language.Language("አማርኛ", 'amh',
              postproc=postproc_word,
              preproc=lambda form: geez2sera(None, form, lang='am', simp=True, report_simplification=True),
              procroot=preproc_root,
              postpostproc=lambda form: postproc_root(form),
              dflt_postproc_root=dflt_postproc_root,
              seg2string=lambda word, string, sep='-', features=False, transortho=True, udformat=False, simplifications=None, conllu=True: \
                            seg2string(word, string, sep=sep, geez=transortho, features=features, udformat=udformat, simplifications=simplifications, conllu=conllu),
              stat_root_feats=['cls', 'vc', 'as'],
              stat_feats=[['poss', 'expl'], ['cnj'], ['cj1'], ['cj2'], ['pp'], ['rel']],
              # We need + and numerals for segmentation of irregular verbal nouns
              seg_units=[["a", "e", "E", "i", "I", "o", "u", "O", "@",
                          "H", "w", "y",
                          "'", "`", "_", "|", "*", "/", "+", "2", "3"],
                         {"1": ["1", "1W"], "b": ["b", "bW"], "c": ["c", "cW"], "C": ["C", "CW"],
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
AMH.set_morphology(language.Morphology(
                             pos_morphs=[('cop',), ('n',), ('v',)],
                             # Exclude ^ and - (because they can be used in compounds)
                             punctuation=r'[“‘”’–—:;/,<>?.!%$()[\]{}|#@&*\_+=\"፡።፣፤፥፦፧፨]',
                             # Include digits?
                             characters=r'[a-zA-Zሀ-ፚ\'`^]'))

### Assign various attributes to Morphology and POSMorphology objects

# Functions that simplifies Amharic orthography
AMH.morphology.simplify = lambda word: simplify(word)
AMH.morphology.orthographize = lambda word: orthographize(word)

# Function that performs trivial analysis on forms that don't require romanization
#AMH.morphology.triv_anal = trivial_anal

## Functions converting between feature structures and simple dicts
AMH.morphology['v'].anal_to_dict = lambda root, anal: vb_anal_to_dict(root, anal)
AMH.morphology['v'].dict_to_anal = lambda root, anal: vb_dict_to_anal(root, anal)
AMH.morphology['v'].name = 'verb'

## Default feature structures for POSMorphology objects
## Used in generation and production of citation form
AMH.morphology['v'].defaultFS = \
    language.FeatStruct("[pos=v,tm=prf,as=smp,vc=smp,sb=[-p1,-p2,-plr,-fem],ob=[-expl,-p1,-p2,-plr,-b,-l,-prp,-frm,-fem],cj1=None,cj2=None,pp=None,ax=None,-neg,-rel,-sub,-acc,-ye]")
AMH.morphology['v'].FS_implic = {'rel': ['sub'],
                                'cj1': ['sub'],
                                'pp': ['rel', 'sub'],
                                ('pp', ('be', 'le', 'ke', 'wede', 'Inde', 'sIle', 'Iske', 'Iyye')): [['rl', ['p']]],
#                                'def': ['rel', 'sub'],
                                'l': ['prp'],
                                'b': ['prp']
#                                'ob': [['expl']]
                                }
# defaultFS with voice and aspect unspecified
AMH.morphology['v'].citationFS = language.FeatStruct("[pos=v,tm=prf,sb=[-p1,-p2,-plr,-fem],ob=[-expl],cj1=None,cj2=None,pp=None,ax=None,-neg,-rel,-sub,-ye,-acc]")
AMH.morphology['v'].explicit_feats = ["sb", "ob", "tm", "neg", "rel", "def", "cj1", "cj2", "pp"]
AMH.morphology['v'].feat_list = \
  [('cj1', ('sI', 'IskI', 'bI', 'lI', 'IndI')),
   ('vc', ('ps', 'cs', 'tr', 'smp')),
  ('ye', (False, True)),
  ('v', ('man', 'inf', 'agt', 'ins', None)),
  ('pp', ('wede', 'Iske', 'ke', 'be', 'le', 'Iyye', 'sIle', 'Inde')),
  ('pos', ('n', 'v')),
  ('def', (False, True)),
  ('ax', (None, 'al')),
  ('as', ('it', 'rc', 'smp')),
  ('cj2', ('s', 'm', 'Inji')),
  ('acc', (False, True)),
  ('tm', ('ger', 'j_i', 'imf', 'prf', 'prs')),
  ('rel', (False, True)),
  ('ob', [('b', (False, True)), ('plr', (False, True)), ('prp', (False, True)), ('p1', (False, True)), ('frm', (False, True)),
          ('l', (False, True)), ('expl', (False, True)), ('p2', (False, True)), ('fem', (False, True))]),
  ('sub', (False, True)),
  ('neg', (False, True)),
  ('sb', [('p1', (False, True)), ('frm', (False, True)), ('plr', (False, True)), ('fem', (False, True)), ('p2', (False, True))])]
AMH.morphology['v'].feat_abbrevs = \
  {'cj1': "conj prefix", 'cj2': "conj suffix", "vc": "voice",
   "sb": "subject", "ob": "object", "tm": "TAMH", "neg": "negative", "rel": "relative", "def": "definite",
   "pp": "preposition"}
AMH.morphology['v'].fv_abbrevs = \
  (([['p1', True], ['p2', False], ['plr', False]], "1 prs sng"),
   ([['p1', True], ['p2', False], ['plr', True]], "1 prs plr"),
   ([['p1', False], ['p2', True], ['plr', False], ['fem', False]], "2 prs sng mas"),
   ([['p1', False], ['p2', True], ['plr', False], ['fem', True]], "2 prs sng fem"),
   ([['p1', False], ['p2', True], ['plr', False], ['frm', True]], "2 prs frml"),
   ([['p1', False], ['p2', True], ['plr', True]], "2 prs plr"),
   ([['p1', False], ['p2', False], ['plr', False]], "3 prs sng"),
   ([['p1', False], ['p2', False], ['plr', False], ['frm', True]], "3 prs frml"),
   ([['p1', False], ['p2', False], ['plr', True]], "3 prs plr")
   )
# Set this here rather than automatically with POSMorphology.set_web_feats() since all web features have a single value
AMH.morphology['v'].web_feats = \
  [('sb', 1), ('ob', 1), ('tm', 1), ('neg', 1), ('rel', 1), ('pp', 1), ('cj1', 1), ('cj2', 1), ('def', 1)]
AMH.morphology['v'].root_proc = postpostproc_root
AMH.morphology['n'].root_proc = postproc_nroot
# AMH.morphology['nm'].root_proc = postproc_nroot
AMH.morphology['cop'].root_proc = lambda root, fs, phonetic=True, simplifications=None: "ን"

AMH.morphology['n'].name = 'noun'
AMH.morphology['n'].defaultFS = \
    language.FeatStruct("[-acc,-det,-neg,-itu,as=smp,cnj=None,-dis,-gen,-plr,poss=[-expl,-p1,-p2,-plr,-fem,-frm],prep=None,v=None,vc=smp]")
AMH.morphology['n'].FS_implic = {'poss': [['expl'], 'def']}
# defaultFS with voice and aspect unspecified
AMH.morphology['n'].citationFS = language.FeatStruct("[-det,-acc,-neg,cnj=None,-dis,-gen,-plr,poss=[-expl],prep=None,v=inf]")
AMH.morphology['n'].explicit_feats = ["plr", "poss", "def", "det", "acc", "gen", "pp", "dis"]
AMH.morphology['n'].feat_abbrevs = \
  {'plr': "plural", 'poss': "possessor", "def": "definite", "acc": "accusative", "dis": "distributive", "gen": "genitive",
   'prep': 'preposition'}

# AMH.morphology['nm'].name = 'name'
# AMH.morphology['nm'].defaultFS = language.FeatStruct("[-acc,cnj=None,-gen,prep=None]")
# # defaultFS with voice and aspect unspecified
# AMH.morphology['nm'].citationFS = language.FeatStruct("[-acc,cnj=None,-gen,prep=None]")
# AMH.morphology['nm'].explicit_feats = ["acc", "gen", "prep"]
# AMH.morphology['nm'].feat_abbrevs = \
#   {"acc": "accusative", "gen": "genitive", 'prep': 'preposition'}

AMH.morphology['cop'].name = 'copula'
AMH.morphology['cop'].defaultFS = language.FeatStruct("[cj2=None,-neg,sb=[-fem,-p1,-p2,-plr,-frm],tm=prs]")
AMH.morphology['cop'].citationFS = language.FeatStruct("[cj2=None,-neg,sb=[-fem,-p1,-p2,-plr,-frm],tm=prs]")
AMH.morphology['cop'].explicit_feats = ["sb", "neg", "cj2"]
AMH.morphology['cop'].feat_abbrevs = \
  {'sb': "subject", 'cj2': "conj suffix", "neg": "negative"}
AMH.morphology['cop'].fv_abbrevs = \
  (([['p1', True], ['p2', False], ['plr', False]], "1 prs sng"),
   ([['p1', True], ['p2', False], ['plr', True]], "1 prs plr"),
   ([['p1', False], ['p2', True], ['plr', False], ['fem', False]], "2 prs sng mas"),
   ([['p1', False], ['p2', True], ['plr', False], ['fem', True]], "2 prs sng fem"),
   ([['p1', False], ['p2', True], ['plr', False], ['frm', True]], "2 prs frml"),
   ([['p1', False], ['p2', True], ['plr', True]], "2 prs plr"),
   ([['p1', False], ['p2', False], ['plr', False]], "3 prs sng"),
   ([['p1', False], ['p2', False], ['plr', False], ['frm', True]], "3 prs frml"),
   ([['p1', False], ['p2', False], ['plr', True]], "3 prs plr")
   )

## Functions that return the citation forms for words
AMH.morphology['v'].citation = lambda root, fss, guess, vc_as, phonetic: vb_get_citation(root, fss, guess, vc_as, phonetic)
AMH.morphology['n'].citation = lambda root, fss, guess, vc_as, phonetic: n_get_citation(root, fss, guess, vc_as, phonetic)
AMH.morphology['cop'].citation = lambda root, fss, guess, vc_as, phonetic: 'new'

## Functions that convert analyses to strings
AMH.morphology['v'].anal2string = lambda fss, webdict, **kwargs: vb_anal2string(fss, webdict=webdict, **kwargs)
AMH.morphology['n'].anal2string = lambda fss, webdict, **kwargs: n_anal2string(fss, webdict=webdict, **kwargs)
AMH.morphology['cop'].anal2string = lambda fss, webdict, **kwargs: cop_anal2string(fss, webdict=webdict, **kwargs)

## Postprocessing function for nouns (treats roots differently)
# AMH.morphology['v'].postproc = lambda analysis: vb_postproc(analysis)
# AMH.morphology['n'].postproc = lambda analysis: n_postproc(analysis)
# AMH.morphology['cop'].postproc = lambda analysis: cop_postproc(analysis)

# Interface language
AMH.if_language = 'eng'

def load_anal(pos='v', lex=True, guess=False):
    if lex:
        AMH.morphology[pos].load_fst(True, verbose=True)
    if guess:
        AMH.morphology[pos].load_fst(True, guess=True, verbose=True)

def load_gen(pos='v', lex=True, guess=False):
    if lex:
        AMH.morphology[pos].load_fst(True, generate=True, invert=True, verbose=True)
    if guess:
        AMH.morphology[pos].load_fst(True, generate=True, invert=True, guess=True, verbose=True)

def roman2geez(value):
    """Convert a value (prep or conj) to geez."""
    return ROM2GEEZ.get(value, value)

def seg2string(word, segmentation, sep='-', geez=True, features=False, udformat=False,
               arules=False, simplifications=None, conllu=True):
    """
    Convert a segmentation to a string, including features if features is True.
    """
#    print("*** seg2string {} {} {}".format(segmentation, simplifications, features))
    # The segmentation string is second in the list
    pos = segmentation[0]
    morphstring = segmentation[1]
    citation = segmentation[2]
    if not morphstring:
        if conllu:
#            word = geezify(word)
            return [[ ['id', '*'], ['form', word], ['lemma', word], ['upos', pos.upper()], ['xpos', pos.upper()], ['feats', None], ['head', None], ['deprel', None ] ]]
        else:
            result = {'pos': pos.upper()}
            if citation:
                result['lemma'] = citation
            return result
    morphs, rootindex = AMH.seg2morphs(morphstring, pos)
    # Root string and features
    root, rootfeats = morphs[rootindex]
    if pos:
        # Add POS to root features
        posstring = "@{}".format(pos)
        if not rootfeats:
            rootfeats = "(" + posstring + ")"
        else:
            rootfeats = "({},{})".format(posstring, rootfeats[1:-1])
    # Separate the root consonants and template, and realize the root
    root = root2string(root, simplifications=simplifications)
    # Replace the root in the morphemes list
    morphs[rootindex] = root, rootfeats
    if udformat:
        morphs = [(m, language.Language.udformat_posfeats(f)) for m, f in morphs]
#    print("** morphs {}".format(morphs))
#    for m, f in morphs:
#        print("***  morph {}, feats {}".format(m, f))
    if geez:
        # First make sure separate morphemes are geez
        morphs2 = [[(g, f) for g in geezify_morph(m, alt=True)] for m, f in morphs]
    else:
        morphs2 = []
        for m, f in morphs:
            conv = convert_labial(m)
            morphs2.append([(c, f) for c in conv])
#    print("*** morphs {}".format(morphs2))
    morphs = allcombs(morphs2)
    # For now ignore multiple spellings for syllables like qWe; just use the first one
    morphs = morphs[0]
    if conllu:
        morphs = [conllu_morpheme(form, props, citation) for form, props in morphs]
        return morphs
    else:
        if not features:
            morphs = [[w[0] for w in word] for word in morphs]
        else:
            # Rejoin morpheme and features for each word
            morphs = [''.join(m) for m in morphs]
#            morphs = [[''.join(m) for m in word] for word in morphs]
#            print("**** morphs {}".format(morphs))
        result = {'morphemes': sep.join(morphs)}
    if citation:
        result['lemma'] = citation
    if pos:
        result['pos'] = pos.upper()
    return result

def conllu_morpheme(form, props, citation):
    '''
    Create a dict with CoNLL-U properties for a morpheme.
    props is a POS;feats string surrounded by parentheses.
    '''
    # The head is surrounded by {}
    ishead = False
    if '{' in form:
        ishead = True
#    print("**** conllu_morpheme: form {} props {} citation {}".format(form, props, citation))
    if ishead:
        form = form.replace('{', '').replace('}', '')
#    props = props.replace('(', '').replace(')', '').split(';')
    pos = props.get('pos')
#    pos = pos.split(',')
    upos = pos[0]
    xpos = pos[1] if len(pos) == 2 else upos
#    pos = props[0]
    feats = props.get('feats')
    deprel = props.get('deprel')
    if deprel:
        deprel = deprel.replace('.', ':')
    if (lemma := props.get('lemma')) is None:
        if not ishead or (lemma := citation) is None:
            lemma = form
#    feats = props[1] if len(props) == 2 else '_'
    return [ ['id', '*'], ['form', form], ['lemma', lemma], ['upos', upos], ['xpos', xpos], ['feats', feats], ['head', None], ['deprel', deprel] ]
#    return {'form': form, 'lemma': form, 'upos': upos, 'xpos': xpos, 'feats': feats}

def root2string(root, simplifications=None):
    """
    If root contains '+', it consists of a root and a template, which need to be
    integrated.
    simplifications is a list of (normal, alternate) character pairs saved when
    word was normalized, for example ('s', '^s').
    """
    if '++' in root:
        # For irregular stems, the root is followed by explicit form rather than template
        cons, form = root.split('++')
#        return '{' + form + '}'
    elif '+' in root:
        cons, temp = root.split('+')
        cons = segment(cons, AMH.seg_units)
        cons = [c for c in cons if c not in ['a', '_']]
#        print("root cons: {}, temp {}".format(cons, temp))
        if 'tt' in temp:
            temp = temp.replace('tt', 't_')
        temp = [(int(t) if t.isdigit() else t) for t in temp]
        form = []
        last_cons = ''
        for index, t in enumerate(temp):
            if isinstance(t, int):
                # Template positions are 1-based, not 0-based
                c = cons[t-1]
                if c != last_cons:
                    form.append(cons[t-1])
                else:
                    # Identical consonants; geminate
                    form.append('_')
                last_cons = c
            elif index == 0 and t in "aeiouIE":
                form.append("'" + t)
            elif t in "stm":
                form.append(t)
                last_cons = t
            else:
                form.append(t)
                # A vowel or _ character was added so clear the last consonant
                last_cons = ''
        # handle palatalization of agent and instrument forms (later check features for this?)
        if form[-1] == 'i':
            if form[-2] in AM_PAL:
                form[-2:] = [AM_PAL[form[-2]]]
        elif form[-3:] == ['i', 'y', 'a']:
            if form[-4] in AM_PAL:
                form[-4:] = [AM_PAL[form[-4]], 'a']
        form = ''.join(form)
#        return '{' + ''.join(form) + '}'
    else:
        form = root
    if simplifications:
        form = complicate_stem(form, simplifications)
    return '{' + form + '}'

def modify_geez(geez, romanized):
    """
    romanized is a romanized stem/root. geez is the Geez form of a word,
    which may be an inflected form of the stem/root.
    Based on the alternate characters (^s, H, etc.) in the stem/root,
    an altered version of the word is returned.
    """
    global AMH
    if not AMH:
        AMH = hm.morpho.get_language('amh', load=True)
    seg_units = AMH.seg_units
    segrom = segment(romanized, seg_units)
    geezrom = segment(romanize(geez), seg_units)
    changes = []
    for seg in segrom:
        if seg in SIMP_PHONES:
            changes.append((seg, seg))
        elif seg in ALT_PHONES:
            changes.append((simplify_roman(seg), seg))
    altered = []
    for char in geezrom:
        if not changes or char != changes[0][0]:
            altered.append(char)
        else:
            altered.append(changes[0][1])
            changes.pop(0)
    altered = ''.join(altered)
    return geezify(altered)

def simplify_roman(roman):
    """
    Simplify ^s, ^S, H, ^h, ` to s, h, '.
    """
    roman = roman.replace('^', '')
    roman = roman.replace('H', 'h').replace('`', "'")
    return roman

def complicate_stem(stem, simplifications):
    '''
    stem is a romanized stem.
    simplifications is a list of (simple, complex) pairs
    of character normalizations made to the word based on the stem.
    Returns the stem with original characters.
    For example,
    complicate_stem("SSt", [(S, ^S), (S, ^S)]) => ^S^St
    '''
    # We're going to mutate this list and might need it later
    # for another analysis.
    simplifications = simplifications.copy()
    segrom = segment(stem, AMH.seg_units)
    result = []
    for char in segrom:
        if simplifications and char == simplifications[0][0]:
            result.append(simplifications[0][1])
            simplifications.pop(0)
        else:
            result.append(char)
    return ''.join(result)

VOWELS = '[aeEiIou@AOU]'
CONS = "[hlHmrsxqbtcnN'kw`zZydjgTCPSfp]|^S|^s|^h"
LABIALIZE = "[lHmrsxqbtcnNkzZdjgTCPSfp]|^S|^s|^h"

### verb RE rules
RULES = Rules(language = AMH)

RULES.add(Del(delpart="'", pre="-{?", post=VOWELS))
RULES.add(Del(delpart="0-"))

## CC
RULES.add(Repl("[lmrsxbtnzdgTSf]", "}-", "h", "", "", "k"))
RULES.add(SimpRepl("Tt", "t_"))
RULES.add(SimpRepl("[kg]}-k", "k_"))

## VV
# (a|e)(a|e) ## a => a
RULES.add(Del(delpart="[ae]?[ae]-*{?}?-?", post="a"))
# a ## e => a
RULES.add(Del(pre="a", delpart="-*{?}?-?e"))
# e ## e => e
RULES.add(Del(delpart="e", post="}-e"))
# a|e ## u => u
RULES.add(Del(delpart="[ae]", post="}-u"))
# a ## i => i
RULES.add(Del(delpart="a", post="}-i"))

## palatalization, y, i
RULES.add(Repl("[bsdlk]", "", "-y", "-{", CONS, "i"))
RULES.add(Repl("[bsdlk]", "", "-y", "-{", VOWELS, "iy"))
RULES.add(Assim({'t': 'c', 'd': 'j', 'T': 'C', 's': 'x', 'z': 'Z', 'n': 'N', 'l': 'y'},
                inter="_?}?-_?", post="[iE]", prog=True, replace=False))
RULES.add(Repl("[cjCxZNy]", "_?}?-_?", "[iE]-?", "", VOWELS, ""))
RULES.add(Insert(pre="[iE]-?{?}?-?", post=VOWELS, insertion="y"))
RULES.add(Del(delpart="i", pre="[aeEiou]y}?-?"))

## labialization
RULES.add(Repl(LABIALIZE, r"_?}?-?", "[ou]", "-", "[aeEIi]", "W"))

## VV again oa->o'a; ua->u'a
RULES.add(Insert(pre="[uo]-", post="a", insertion="'"))

## cleanup
RULES.add(Del(delpart="[-_{}I]"))

AMH.morphology['v'].rules = RULES

### noun RE rules

VNRULES = Rules(language=AMH)

# palatalization, y, i in deverbal nouns
VNRULES.add(Assim({'t': 'c', 'd': 'j', 'T': 'C', 's': 'x', 'z': 'Z', 'n': 'N', 'l': 'y'},
                 inter="", post="i}", prog=True, replace=False))
VNRULES.add(Assim({'t': 'c', 'd': 'j', 'T': 'C', 's': 'x', 'z': 'Z', 'n': 'N', 'l': 'y'},
                 inter="", post="iya}", prog=True, replace=False))
VNRULES.add(Repl("[cjCxZNy]", "", "iya", "", "}", "a"))
VNRULES.add(Del(delpart="i", pre="[aeEiou]y", post="}"))
#VNRULES.add(Del(delpart="i", pre="[cjCxZNy]", post="}-"+VOWELS))

NRULES = Rules(language=AMH)

# exceptions
NRULES.add(Repl("e", "-{", "y", '', "h}", "z_i"))
NRULES.add(Repl("e", "-{", "yc_i", '', "}", "z_ic"))
NRULES.add(Insert(pre="e-{", post="ya}", insertion="z_i"))
NRULES.add(Repl("e", "-{", "yac_i", '', "}", "z_iyac"))

# glottal stop
NRULES.add(Del(delpart="'", pre="-{?", post=VOWELS))
# aa
NRULES.add(Del(delpart="a", pre="a}-"))
# optional: aoc => oc
#NRULES.add(Del(delpart="a", post="}-oc"))

# epenthesis
NRULES.add(Insert(pre=VOWELS + "}?-", post="E", insertion="y"))
NRULES.add(Insert(pre=VOWELS + "}?-", post="o", insertion="w"))
NRULES.add(Insert(pre="[iE]}?-", post="a", insertion="y"))
NRULES.add(Insert(pre="[ou]}?-", post="a", insertion="w"))

# -u, -wa
NRULES.add(Repl(VOWELS, "}-", "u", "", "", "w"))
# modified 2022.3.15 to exclude yW, 'W, 1W, wW'
NRULES.add(Repl(LABIALIZE, "}?-", "w", "", "", "W"))

# prefix VV
NRULES.add(Del(delpart="e", post="-{?'?a"))
NRULES.add(Del(delpart="'", pre="e-{", post=CONS))

NRULES.add(Del(delpart="[-_{}]"))

# ' between vowels
NRULES.add(Insert(pre=VOWELS, post=VOWELS, insertion="'"))

NRULES.add(Del(delpart="I"))

VNRULES.add_rules(NRULES)

AMH.add_rules('n', NRULES)
AMH.add_rules('v', RULES)
AMH.add_rules('n_dv', VNRULES)
