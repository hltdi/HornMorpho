#!/usr/bin/env python3

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

Author: Michael Gasser <gasser@indiana.edu>
""" 

import hm

## displaying segmentations in Tkinter

C1 =  ["የውሾች ጩኸት ይሰማል ።", "ቤቴን መሸጥ እፈልጋለሁ ።", "ልጅቷ እውር ናት ።",
          "ተቀምጦ ነበር ።", "የሞት ቅጣት ተግባራዊ የሚያደርጉ አገሮችን እንቃወማለን ።", "እሱ ለመማር አይፈልግም ።"]
C2 = ["የውሾች ጩኸት ይሰማል ።", "አሁን ወደ ዋናው የጉዞ ፕሮግራም እንመለስ ።"]
C3 = ["በዚህም የተሻለ የሰብል ምርት ይጠበቃል ።"]
C4 = ["እሱ ለመማር አይፈልግም ።", "ለእውሩ ምን አደረግን ?", "እኔ መጣሁ ።"]
C5 = ["የሞት ቅጣት ተግባራዊ የሚያደርጉ አገሮችን እንቃወማለን ።"]
C6 = ["እኔ መጣሁ ።", "ሁላችንን ይወዳሉ ።"]
C7 = ["እርስ በርሳቸውን ይዋደዳሉ ።"]
CACO3_7 = "hm/ext_data/CACO/CACO1.1/CACO_TEXT_3-7tok.txt"
CACO0 = "../../TAFS/datasets/CACO/CACO_3-7tok_B0.txt"
CACO1 = "../../TAFS/datasets/CACO/CACO_3-7tok_B1.txt"
CACO2 = "../../TAFS/datasets/CACO/CACO_3-7tok_B2.txt"
CACO3 = "../../TAFS/datasets/CACO/CACO_3-7tok_B3.txt"
CACO4 = "../../TAFS/datasets/CACO/CACO_3-7tok_B4.txt"
CACO5 = "../../TAFS/datasets/CACO/CACO_3-7tok_B5.txt"
AS1 = "hm/ext_data/ከአብነት/mini1.txt"
CACO = "../../TAFS/datasets/CACO"
CACO_FILTERED = "CACO_verbs_B8.txt"
CONLLU = "../../TAFS/venv/conllu"
SEGS = "../../TAFS/segmentations"
LAST_CACO_LINE = 9061

def ASAI(start=600, id=2, n_sents=200):
    return \
           hm.create_corpus(
               read={'name': "ASAI.{}".format(id), 'id': id, 'filename': CACO_FILTERED},
               batch= {'n_sents': n_sents, 'start': start},
               disambiguate=False, seglevel=0, um=2
               )

def proc_ASAI(corpus, filename=False, append=False):
    sentences =  hm.extract_corpus_features(corpus, ['VERB'], [('Number', None), ('VerbForm', 'Main')])
    if filename:
        write_ASAI(sentences, filename, append=append)
    return sentences

def write_ASAI(sentences, filename, append=False):
    with open(filename, 'a' if append else 'w', encoding='utf8') as file:
        for sentence in sentences:
            print(sentence[0], file=file)
            for index, word, feats in sentence[1:]:
                print("{}\t{}\t{}".format(index, word, ','.join(feats)), file=file)
            print(file=file)

def AW(id, n_sents=100, start=0, write=True, append=True):
    return \
    hm.create_corpus(
        read={'filename': CACO_FILTERED},
        batch={'name': 'AW23.{}'.format(id), 'n_sents': n_sents, 'start': start, 'id': id, 'sentid': start},
        disambiguate=True,
        write={'folder': CONLLU, 'append': append}
        )

## translation
def load_trans(src, targ, pos, gen=True):
    src_posmorph = get_pos(src, pos, fidel=True)
    trg_posmorph = get_pos(targ, pos, fidel=True)
    src_posmorph.load_trans_fst(trg_posmorph, pos, gen=gen)
    return src_posmorph

def parse_lextr_file(src_pos, pos):
    import os
    src = src_pos.language.abbrev
    path = os.path.join("hm/languages/fidel", src, "fst", pos + '.lextr')
    print("** lextr path {}".format(path))
    s = open(path, encoding='utf8').read()
    hm.morpho.LexTrans.parse("lextr", s,
                             cascade=src_pos.casc,
                             fst=FST('lextr', cascade=src_pos.casc, weighting=hm.morpho.UNIFICATION_SR)
                             )

def corp(filename=CACO0, id=0, n_sents=50, start=0, write=True, um=1, seglevel=2):
    hm.create_corpus(read={'filename': filename},
                                        batch={'source': 'CACO', 'id': id, 'start': start, 'n_sents': n_sents, 'sent_length': '3-7'},
                                        write={"folder": SEGS} if write else {},
                                        um=um, seglevel=seglevel, degeminate=False)

def filtercorp(filename='CACO.txt', n_sents=50, start=0, id=1, gramfilt='verbs'):
    return \
    hm.create_corpus(
                       read={'filename': filename},
                       batch={'n_sents': n_sents, 'start': start, 'id': id},
                       disambiguate=False,
                       constraints={
                                                  'grammar': gramfilt, 'maxpunc': 1, 'maxnum': 0,
                                                  'maxunk': 3, 'maxtoks': 11, 'endpunc': True
                                                  }
                     )

def convfeat(fs, oldfs, newfs, replace=False):
    if u(fs, oldfs):
        # fs unifies with oldf
        fs.update(newfs)
        if replace:
            for oldf in oldfs.keys():
                del fs[oldf]
#    return fs

#def biling():
#    global AK, T
#    AK = hm.morpho.Biling('am', 'ks', srcphon=True, targphon=False)
#    T = hm.morpho.TransTask(AK)


def get_lang(abbrev, segment=True, guess=True, phon=False, cache='',
                           experimental=True,  pickle=True, verbose=False):
    """
    Return the language with abbreviation abbrev, loading it
    if it's not already loaded.
    """
    return hm.morpho.get_language(abbrev, cache=cache, phon=phon, guess=guess,
                                                                   pickle=pickle, segment=segment, experimental=experimental,
                                                                   load=True, verbose=verbose)

def get_pos(abbrev, pos, phon=False, segment=False, translate=False, load_morph=False,
                        fidel=False, guess=True, simplified=False, verbose=False):
    """
    Just a handy function for working with the POS objects when re-compiling
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
    hm.load_lang(abbrev, segment=segment, phon=phon, load_morph=load_morph, fidel=fidel,
                 translate=translate, guess=guess, simplified=simplified, verbose=verbose)
    lang = hm.morpho.get_language(abbrev, phon=phon, segment=segment, simplified=simplified,
                                  translate=translate, load=load_morph, load_morph=load_morph,
                                  fidel=fidel, verbose=verbose)
    if lang:
        return lang.morphology[pos]

def get_cascade(abbrev, pos, guess=False, gen=False, phon=False,
                translate=False, segment=False, verbose=False):
    pos = get_pos(abbrev, pos, phon=phon, segment=segment,
                  translate=translate, load_morph=False, verbose=verbose)
    pos.load_fst(True, guess=guess, create_fst=False,
                 phon=phon, generate=gen, translate=translate,
                 invert=gen, segment=segment, verbose=verbose)
    return pos.casc

def recompile(abbrev, pos, gen=False, phon=False, segment=False, guess=False,
                            translate=False, experimental=False, mwe=False, seglevel=2,
                            fidel=False, create_fst=True, relabel=True, gemination=True,
                            simplified=False, backwards=False, split_index=0, verbose=True):
    """
    Create a new composed cascade for a given language (abbrev) and part-of-speech (pos),
    returning the morphology POS object for that POS.
    Note 1: this can take a very long time for some languages.
    Note 2: the resulting FST is not saved (written to a file). To do this, use the method
    save_fst(), with the right options, for example, gen=True, segment=True.
    """
    pos_morph = get_pos(abbrev, pos, phon=phon, segment=segment, translate=translate,
                                            fidel=fidel,
                                            simplified=simplified, load_morph=False, verbose=verbose)
    fst = pos_morph.load_fst(True, segment=segment, generate=gen, invert=gen, guess=guess,
                             translate=translate, simplified=simplified, recreate=True, fidel=fidel,
                             experimental=experimental, mwe=mwe, pos=pos, seglevel=seglevel,
                             create_fst=create_fst, relabel=relabel, gemination=gemination,
                             compose_backwards=backwards, split_index=split_index,
                             phon=phon, verbose=verbose)
    if not fst and gen == True:
        print('Generation FST not found')
        # Load analysis FST
        pos_morph.load_fst(True, seglevel=seglevel, verbose=True)
        # ... and invert it for generation FST
        pos_morph.load_fst(generate=True, invert=True, gen=True, experimental=experimental,
                                                 relabel=relabel,
                                                 fidel=fidel, mwe=mwe, guess=guess, verbose=verbose)
    return pos_morph

## Various shortcuts for working with new cascades

def segrecompile(lang, pos, mwe=False, seglevel=2, fidel=False, create_fst=True, verbose=True):
    """
    Shortcut for recompiling Amh (experimental) segmenter FST.
    """
    return recompile(lang, pos, segment=True, experimental=True, mwe=mwe, fidel=fidel,
                                       create_fst=create_fst, seglevel=seglevel, verbose=verbose)

def genrecompile(lang, pos, create_fst=True):
    '''
    Recompile the generation FST for a language in the fidel folder.
    '''
    return recompile(lang, pos, gen=True, fidel=True, create_fst=create_fst)

def analrecompile(lang, pos, create_fst=True, seglevel=2, gemination=True):
    '''
    Recompile  the analysis FST for a language in the fidel folder.
    '''
    return recompile(lang, pos, fidel=True, create_fst=create_fst, seglevel=seglevel,
                                       gemination=gemination)

def transrecompile(src, trg, pos):
    '''
    Recompile analysis and generation FSTs for source and target language, and create
    translation FST.
    '''
    src_pos_morph = get_pos(src, pos, segment=False, fidel=True, load_morph=False)
    trg_pos_morph = get_pos(trg, pos, segment=False, fidel=True, load_morph=False)
    fst = src_pos_morph.load_trans_fst(trg_pos_morph, pos)
    return src_pos_morph, trg_pos_morph

##def parse_lextr_file(src_pos, pos):
##    import os
##    src_pos
##    src = src_pos.language.abbrev
##    path = os.path.join("hm/languages/fidel", src, "fst", pos + '.lextr')
##    print("** lextr path {}".format(path))
##    s = open(path, encoding='utf8').read()
##    hm.morpho.LexTrans.parse("lextr", s,
##                             cascade=src_pos.casc,
##                             fst=FST('lextr', cascade=src_pos.casc, weighting=hm.morpho.UNIFICATION_SR)
##                             )

FST = hm.morpho.FST
FF = hm.morpho.FSSet

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
#            print(s)
            print(res)
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

## Analyzing a word type corpus.
## Each line is count, word
WORD_CORPUS = "../../../../Projects/LingData/Am/Crawl/all.txt"
##def word_corpus(report_freq=100, start=0, n=10000, corpus=None):
##    corpus = corpus or []
##    with open(WORD_CORPUS, encoding='utf8') as file:
##        linen = start
##        lines = file.readlines()[start:start+n]
##        for line in lines:
##            count, word = line.split()
##            count = int(count)
##            if count == 1:
##                break
##            analyses = hm.anal_word('amh', word, um=2, phonetic=False)
##            if analyses:
##                anals = []
##                for analysis in analyses:
##                    pos = analysis.get('POS', '')
##                    root = analysis.get('root', '')
##                    if '|' in root:
##                        root = root.split('|')[0]
##                    gram = analysis.get('gram', '')
##                    anals.append("{}.{}.{}".format(pos, root, gram))
##                analyses = "|".join(anals)
##                corpus.append((count, word, analyses))
##            linen += 1
##            if linen % report_freq == 0:
##                print("Analyzed {} words".format(linen))
##    return corpus

##def verb_corpus(report_freq=1000, start=0, n=10000, corpus=[]):
##    amh = get_lang('amh', guess=False, experimental=False, segment=False)
##    with open(WORD_CORPUS, encoding='utf8') as file:
##        linen = start
##        lines = file.readlines()[start:start+n]
##        for line in lines:
##            count, word = line.split()
##            count = int(count)
##            if count == 1:
##                break
##            analyses = hm.anal_word('amh', word, um=0, phonetic=False, simplify=False)
##            anals = []
##            if analyses:
##                for analysis in analyses:
##                    pos = analysis.get('POS', '')
##                    if pos != 'v':
##                        continue
##                    root = analysis.get('root')
##                    if not root:
##                        continue
##                    gram = analysis.get('gram')
##                    if not gram:
##                        continue
##                    asp = gram.get('as', 'smp')
##                    if asp == 'smp':
##                        asp = 0
##                    vc = gram.get('vc', 'smp')
##                    if vc == 'smp':
##                        vc = 0
##                    sbj = gram.get('sb')
##                    sbj = simplify_sbj(sbj)
##                    obj = gram.get('ob')
##                    obj = simplify_obj(obj)
##                    anals.append("{}::{}:{}:{}:{}".format(root, asp, vc, sbj, obj))
##            if anals:
##                anals = ';;'.join(anals)
##                corpus.append("{} {} {}".format(count, word, anals))
##            linen += 1
##            if linen % report_freq == 0:
##                print("Analyzed {} words".format(linen))
##
##def simplify_sbj(feats):
##    if not feats:
##        return ''
##    person = feats.get('p1', False), feats.get('p2', False)
##    person = 1 if person[0] else (2 if person[1] else 3)
##    number = feats.get('plr', False)
##    number= 'p' if number else 's'
##    gender = ''
##    if number == 's' and person != 1:
##        gender = feats.get('fem', False)
##        gender = 'f' if gender else 'm'
##    return "{}{}{}".format(person, number, gender)
##
##def simplify_obj(feats):
##    if not feats:
##        return ''
##    expl = feats.get('expl')
##    if not expl:
##        return ''
##    person = feats.get('p1', False), feats.get('p2', False)
##    person = 1 if person[0] else (2 if person[1] else 3)
##    number = feats.get('plr', False)
##    number= 'p' if number else 's'
##    gender = ''
##    if number == 's' and person != 1:
##        gender = feats.get('fem', False)
##        gender = 'f' if gender else 'm'
##    prep = 'A'
##    if feats.get('prp'):
##        if feats.get('l'):
##            prep = 'B'
##        else:
##            prep = 'M'
##    return "{}{}{}{}".format(person, number, gender,prep)

## shortcuts
FS = hm.morpho.FeatStruct
FSS = hm.morpho.FSSet

R = lambda pos: recompile('amh', pos, segment=True, experimental=True)

##AMTEST1 = ["አውቄ", "እወቂ", "ተዋውቄ", "አስተዋውቄ", "እዪ", "ትይ", "ታይቼ",
##           "ተያይቷል", "ይተያይ", "ፈስሼ", "ደምስሳ", "ፈሶ", "ሰልችቼ"]
##
##def crawl_test_amh(limit=5000):
##    """
##    Test Amharic analyzer on words in Crawl list.
##    """
##    with open("../../LingData/Am/Crawl/all.txt", encoding='utf8') as file:
##        nwords = 0
##        for line in file:
##            nwords += 1
##            if nwords >= limit:
##                return
##            count, word = line.strip().split()
##            anal = hm.anal('amh', word, raw=True)
##            if not anal:
##                print("Failed on {}".format(word))

## shortcuts for Chaha ('sgw')
#GA = lambda form: hm.anal('sgw', form, raw=True)
#GG = lambda form, pos, feats=None: hm.gen('sgw', form, pos=pos, features=hm.morpho.FSSet(feats) if feats else None)

def main():
    pass

if __name__ == "__main__": main()

# am = recompile('am', 'v', verbose=True)
# aa = am.fsts[0][0]
# seg = am.morphology.seg_units
