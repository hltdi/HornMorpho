#!/usr/bin/env python3

"""
This file is part of HornMorpho, which is part of the PLoGS project.

    <http://homes.soic.indiana.edu/gasser/plogs.html>

    Copyleft 2011, 2012, 2013, 2016, 2018, 2019, 2020.
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

Author: Michael Gasser <gasser@indiana.edu>
""" 

import hm

##def proc_ti_verbs():
##    with open("hm/languages/tir/lex/v_root.lex", encoding='utf8') as infile:
##        with open("v_root.lex", 'w', encoding='utf8') as outfile:
##            for line in infile:
##                line = line.strip()
##                if len(line.split()) > 1:
##                    print(line, file=outfile)
##                else:
##                    print("{}  ''  [cls=A]".format(line), file=outfile)                    

def sort_nouns(items):
    order = ['3P', '2P', '1P', '3SF', '3SM', '2SF', '2SM', '1S', 'DEF']
    def order_func(item):
        feat = item[3]
        for i, o in enumerate(order):
            if o in feat:
                return i
        return len(order)
    # items is list of (lemma, gloss, word, feat) tuples
    items.sort(key=order_func, reverse=True)

def ti_sort_verbs(items):
#    if ax:
#        tm = ['V.CVB', 'IPFV;NFIN', 'IMP', 'PRF', 'IPFV', 'PFV']
#    else:
#        tm = ['V.CVB', 'IMP', 'IPFV', 'PFV']
    tm = ['IMP', 'IPFV', 'PFV', 'PFV;NFIN;*RELC']
    sb = ['1;SG', '2;SG;MASC', '2;SG;FEM', '3;SG;MASC', '3;SG;FEM',
          '1;PL', '2;PL;MASC', '2;PL;FEM', '3;PL;MASC', '3;PL;FEM']
    sb.reverse()
    i = []
#    tmsets = [set(t.split(';')) for t in tm]
    items = [item for item in items if any([t in item[3] for t in tm])]
    def order_func(item):
        feat = item[3]
        score = 0
        for i, o in enumerate(tm):
            if o in feat:
                score += i * len(sb)
                break
        for i, o in enumerate(sb):
            if o in feat:
                score += i
                break
        return score
    items.sort(key=order_func, reverse=True)
    return items

def ti_n_poss(stem, gloss='', plr=False, printit=True):
    # All possessive and definite forms of the noun stem
    anal = hm.anal('tir', stem, init_weight="[pp=0]", raw=True)[0]
    gloss = gloss or anal['gloss']
    root = anal['root']
    features = None
    if plr:
        features="[+pl]"
    words_feats = hm.gen('tir', root, del_feats=["pp", "pn", "pg"], ortho_only=True,
                    features=features)
    if not words_feats:
        return
    result = [(stem, gloss, word, feat) for word, feat in words_feats]
    sort_nouns(result)
    if printit:
        for stem, gloss, word, feat in result:
            print("{}\t{}\t{}\t{}".format(stem, gloss, word, feat))
    else:
        return result

def ti_v_sb_tm(lemma, ps=False, printit=True, gloss=''):
    # All subject and simple TAM forms forms of the verb root associated with the lemma
    anal = hm.anal('tir', lemma, init_weight="[tm=prf,sb=[-p1,-p2,-plr,-fem]]",
                   raw=True, phonetic=False)[0]
    g, root = anal.get('gloss'), anal['root']
    gloss = g or gloss
    features = None
    if ps:
        features="[vc=ps]"
    words_feats = hm.gen('tir', root, del_feats=["sb", "tm", "rel", "sub"],
                         ortho_only=True, features=features)
    result = [(lemma, gloss, word, feat) for word, feat in words_feats if feat]
    result = [r for r in result if "NFIN" not in r[3] or "*RELC" in r[3]]
    result = ti_sort_verbs(result)
    result = [(l, g, w, f.replace(';*RELC', '')) for l, g, w, f in result]
    if printit:
        for lemma, gloss, word, feat in result:
            print("{}\t{}\t{}\t{}".format(lemma, gloss, word, feat))
    else:
        return result

def sort_verbs(items, ax=True):
    if ax:
        tm = ['V.CVB', 'IPFV;NFIN', 'IMP', 'PRF', 'IPFV', 'PFV']
    else:
        tm = ['V.CVB', 'IMP', 'IPFV', 'PFV']
    sb = ['1;SG', '2;SG;MASC', '2;SG;FEM', '3;SG;MASC', '3;SG;FEM', '1;PL', '2;PL', '3;PL']
    sb.reverse()
    def order_func(item):
        feat = item[3]
        score = 0
        for i, o in enumerate(tm):
            if o in feat:
                score += i * len(sb)
                break
        for i, o in enumerate(sb):
            if o in feat:
                score += i
                break
        return score
    items.sort(key=order_func, reverse=True)

## Generating word lists for UM
def n_poss(stem, fem=False, plr=False, printit=True):
    # All possessive and definite forms of the noun stem
    anal = hm.anal('amh', stem, init_weight="[poss=[-expl],-def]",
                     raw=True)[0]
    gloss = anal['gloss']
    features = None
    if fem:
        features="[+fem]"
    elif plr:
        features="[+plr]"
    words_feats = hm.gen('amh', stem, del_feats=["def", "poss"], ortho_only=True,
                    features=features)
    result = [(stem, gloss, word, feat) for word, feat in words_feats]
    sort_nouns(result)
    if printit:
        for stem, gloss, word, feat in result:
            print("{}\t{}\t{}\t{}".format(stem, gloss, word, feat))
    else:
        return result

def v_sb_tm(lemma, ax=True, ps=False, printit=True):
    # AMH:
    # All subject and simple TAM forms forms of the verb root associated with the lemma
    anal = hm.anal('amh', lemma, init_weight="[tm=prf,sb=[-p1,-p2,-plr]]",
                   raw=True, phonetic=False)[0]
    gloss, root = anal['gloss'], anal['root']
    features = None
    if ps:
        features="[vc=ps]"
    words_feats = hm.gen('amh', root, del_feats=["sb", "tm"],
                            ortho_only=True, features=features)
    result = [(lemma, gloss, word, feat) for word, feat in words_feats if feat]
    if ax:
        if ps:
            features = "[ax=al,vc=ps]"
        else:
            features = "[ax=al]"
        words_feats = hm.gen('amh', root, del_feats=["sb", "tm"],
                                  ortho_only=True, features=features)
        result.extend([(lemma, gloss, word, feat) for word, feat in words_feats if feat])
    sort_verbs(result)
    if printit:
        for lemma, gloss, word, feat in result:
            print("{}\t{}\t{}\t{}".format(lemma, gloss, word, feat))
    else:
        return result

##def v_sb_tm_ax(lemma):
##    # All main clause impf and ger forms of the verb root
##    anal = hm.anal('amh', lemma, raw=True)[0]
##    gloss, root = anal['gloss'], anal['root']
##    words_feats = hm.gen('amh', root, del_feats=["sb", "tm"], ortho_only=True, features="[ax=al]")
##    return [(lemma, gloss, word, feat) for word, feat in words_feats]

## test items for UM
##words = ["ቤታችንን", "የቤቴ", "ከቤቱስ",
##         "ሰበራት", "የሰበርናቸው", "ትስበርልን", "ተሰበሩ", "ሰባብሮበት", "አሰባበራቸው",
##         "መስበሬም", "የመስበሪያ", "ስላሰባበሩ", "መሰበራቸው", "መሰባበር"
##         ]
##def hmtest():
##    for word in words:
##        print(word, hm.anal('amh', word))
##
## 2019.12.23
## Am->Ks translation
# AK = T = None

#def biling():
#    global AK, T
#    AK = hm.morpho.Biling('am', 'ks', srcphon=True, targphon=False)
#    T = hm.morpho.TransTask(AK)

def get_lang(abbrev, segment=False, guess=True, phon=False, cache='', verbose=False):
    """Return the language with abbreviation abbrev, loading it
    if it's not already loaded."""
    return hm.morpho.get_language(abbrev, cache=cache, phon=phon, guess=guess,
                                  segment=segment, load=True, verbose=verbose)

def get_pos(abbrev, pos, phon=False, segment=False, load_morph=False,
            guess=True, simplified=False, verbose=False):
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
    hm.load_lang(abbrev, segment=segment, phon=phon, load_morph=load_morph,
                 guess=guess, simplified=simplified, verbose=verbose)
    lang = hm.morpho.get_language(abbrev, phon=phon, segment=segment, simplified=simplified,
                                  load=load_morph, load_morph=load_morph,
                                  verbose=verbose)
    if lang:
        return lang.morphology[pos]

def get_cascade(abbrev, pos, guess=False, gen=False, phon=False, segment=False, verbose=False):
    pos = get_pos(abbrev, pos, phon=phon, segment=segment, load_morph=False, verbose=verbose)
    pos.load_fst(True, guess=guess, create_fst=False,
                 phon=phon, generate=gen, invert=gen, segment=segment, verbose=verbose)
    return pos.casc

def recompile(abbrev, pos, gen=False, phon=False, segment=False, guess=False,
              simplified=False, backwards=False, split_index=0, verbose=True):
    """Create a new composed cascade for a given language (abbrev) and part-of-speech (pos),
    returning the morphology POS object for that POS.
    Note 1: this can take a very long time for some languages.
    Note 2: the resulting FST is not saved (written to a file). To do this, use the method
    save_fst(), with the right options, for example, gen=True, segment=True.
    """
    pos_morph = get_pos(abbrev, pos, phon=phon, segment=segment,simplified=simplified,
                        load_morph=False, verbose=verbose)
    fst = pos_morph.load_fst(True, segment=segment, generate=gen, invert=gen, guess=guess,
                             simplified=simplified, recreate=True,
                             compose_backwards=backwards, split_index=split_index,
                             phon=phon, verbose=verbose)
    if not fst and gen == True:
        print('Generation FST not found')
        # Load analysis FST>
        pos_morph.load_fst(True, verbose=True)
        # ... and invert it for generation FST
        pos_morph.load_fst(generate=True, invert=True, gen=True,
                           guess=guess, verbose=verbose)
    return pos_morph

### Simple FSTs and cascades (in test directory)

def make_casc(name):
    import os
    filename = os.path.join("hm/languages/test/cas/", name + '.cas')
    with open(filename, encoding='utf8') as infile:
        castext = infile.read()
        casc = hm.morpho.FSTCascade.parse("simple", castext,
                                          seg_units=['a', 'b', 'c', 'd', 'e', 'f'])
    fst = casc.compose(backwards=False, relabel=True)
    return fst

### Debugging functions

def get_subcas(cascade, name, language):
    """
    Get a cascade that is a sub-cascade of a POS cascade.
    """
    abbrev = language.abbrev
    return hm.morpho.FSTCascade.load("hm/languages/" + abbrev + "/cas/" + name,
                                            cascade.seg_units, language=language)

def get_mincasc(language, cascname):
    """Get a minor cascade, not a POS, for example, v_stem.cas."""
    su = language.seg_units
    ab = language.abbrev
    return \
    hm.morpho.FSTCascade.load("hm/languages/" + ab + "/cas/" + cascname,
                                    language=language, seg_units=g.seg_units)

def get_feats(fs, feats):
    """Print values for features feats within feature structure fs."""
    values = []
    for feat in feats:
        values.append("{}={}".format(feat, fs.get(feat)))
    return ",".join(values)

def casc_anal(casc, string, start_i, end_i=0, limit=20, timeout=200,trace=0):
    seg_units = casc.seg_units
    s = string
    if end_i:
        for index in range(start_i, end_i):
            res = casc[index].transduce(s, seg_units=seg_units,
                                             timeout=timeout,
                                             result_limit=limit,
                                             trace=trace)
            if not res:
                print('Analysis failed at {}'.format(index))
                return
            i = 0
            if len(res) > 1:
                print('FST {}, analyses: {}'.format(index, [a[0] for a in res]))
                x = input("Index of analysis (or quit)? ")
                if not x.isdigit():
                    return
                i = int(x)
            s = res[i][0]
            print(s)
    else:
        return casc[start_i].transduce(s, seg_units=seg_units, timeout=10)

def casc_gen(casc, string, fs, start_i, end_i=0, trace=0):
    """Generate a form from a cascade, given an input string, features, and a start and end
    index (start_i > end_i).
    """
    seg_units = casc.seg_units
    s = string
    if not isinstance(fs, hm.morpho.semiring.FSSet):
        f = hm.morpho.semiring.FSSet(fs)
    else:
        f = fs
    if end_i != None:
        for index in range(start_i, end_i-1, -1):
            res = casc[index].inverted().transduce(s, f, seg_units=seg_units,
                                                   timeout=10, trace=trace)
            if not res:
                print('Generation failed at {}'.format(index))
                return
            i = 0
            if len(res) > 1:
                print('FST {}, output: {}'.format(index, res))
                x = input("Index to select next (or quit)? ")
                if not x.isdigit():
                    return
                i = int(x)
            s = res[i][0]
            f = res[i][1]
            print(index, s, f)
    else:
        return casc[start_i].inverted().transduce(s, f, seg_units=seg_units, timeout=10)

## shortcuts
FS = hm.morpho.FeatStruct
FSS = hm.morpho.FSSet

## shortcuts for Chaha ('sgw')
#GA = lambda form: hm.anal('sgw', form, raw=True)
#GG = lambda form, pos, feats=None: hm.gen('sgw', form, pos=pos, features=hm.morpho.FSSet(feats) if feats else None)

def main():
    pass

if __name__ == "__main__": main()

# am = recompile('am', 'v', verbose=True)
# aa = am.fsts[0][0]
# seg = am.morphology.seg_units
