#!/usr/bin/env python3

"""
This file is part of HornMorpho, which is part of the PLoGS project.

    <http://homes.soic.indiana.edu/gasser/plogs.html>

    Copyleft 2011, 2012, 2013, 2016, 2018, 2019, 2020, 2021.
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

#def conv_amh_words():
#    with open("hm/languages/amh/lex/words.lex") as infile:
#        with open("hm/languages/amh/lex/words1.lex", 'w') as outfile:
#            for line in infile:
#                word, pos, root = line.strip().split()
#                print("{} {} {}".format(word, root, pos), file=outfile)

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

def get_lang(abbrev, segment=False, guess=True, phon=False, cache='',
             pickle=True, verbose=False):
    """Return the language with abbreviation abbrev, loading it
    if it's not already loaded."""
    return hm.morpho.get_language(abbrev, cache=cache, phon=phon, guess=guess,
                                  pickle=pickle,
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

def get_casc(language, cascname):
    """Get a cascade, for example, v_stem.cas, v.cas."""
    if isinstance(language, str):
        language = get_lang(language)
    su = language.seg_units
    ab = language.abbrev
    return \
    hm.morpho.FSTCascade.load("hm/languages/" + ab + "/cas/" + cascname,
                                    language=language, seg_units=su)

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
    To run from the start of the cascade, start_i = len(casc) - 1.
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
    
def time(code, times=1):
    import timeit
    return timeit.timeit(code, number=times)

## shortcuts
FS = hm.morpho.FeatStruct
FSS = hm.morpho.FSSet

AMTEST1 = ["አውቄ", "እወቂ", "ተዋውቄ", "አስተዋውቄ", "እዪ", "ትይ", "ታይቼ",
           "ተያይቷል", "ይተያይ", "ፈስሼ", "ደምስሳ", "ፈሶ", "ሰልችቼ"]

def crawl_test_amh(limit=5000):
    """
    Test Amharic analyzer on words in Crawl list.
    """
    with open("../../LingData/Am/Crawl/all.txt", encoding='utf8') as file:
        nwords = 0
        for line in file:
            nwords += 1
            if nwords >= limit:
                return
            count, word = line.strip().split()
            anal = hm.anal('amh', word, raw=True)
            if not anal:
                print("Failed on {}".format(word))

## shortcuts for Chaha ('sgw')
#GA = lambda form: hm.anal('sgw', form, raw=True)
#GG = lambda form, pos, feats=None: hm.gen('sgw', form, pos=pos, features=hm.morpho.FSSet(feats) if feats else None)

def main():
    pass

if __name__ == "__main__": main()

# am = recompile('am', 'v', verbose=True)
# aa = am.fsts[0][0]
# seg = am.morphology.seg_units
