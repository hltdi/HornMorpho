#!/usr/bin/env python3

"""
This file is part of HornMorpho, which is part of the PLoGS project.

    <http://homes.soic.indiana.edu/gasser/plogs.html>

    Copyleft 2021, 2025.
    PLoGS and Michael Gasser <gasser@iu.edu>.

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

Creating UniMorph repositories.
Updated in 12.2025 to handle HM changes since 2021.
""" 

import hm

geezroman = hm.morpho.geez

segment_word = hm.morpho.utils.segment

def get_crawled():
    words = {}
    with open("../../../../Projects/LingData/Am/Crawl/all.txt", encoding='utf8') as file:
        for line in file:
            count, word = line.split()
            words[word.strip()] = int(count.strip())
    return words

CRAWLED = get_crawled()

AMH = None

ALT_PHONES = ['s', 'S', 'h', "'", 'sW', 'SW', 'hW']
ALT_PHONES2 = ['s', '^s', 'S', '^S', 'h', 'H', '^h', "'", "`", 'sW', '^sW', '^SW', '^hW']
ALT_PHONES3 = ['^s', '^S', 'H', '^h', "`", '^sW', '^SW', '^hW']
ALT_PHONES_V = ['^s', '^S', "`", '^sW', '^SW']
SIMP_PHONES = ['s', 'S', 'h', "'", 'sW', 'SW', 'hW']

### Final stuff

def find_Cwa(file="../UM/amh/n2.um"):
    wa = []
    Wa = []
    with open(file, encoding='utf8') as inf:
        for line in inf:
            line = line.strip()
            lemma, word, feats = line.split()
            if word.endswith("ዋ"):
                word0 = word[:-1]
                word0rom = geezroman.romanize(word0)
                if word0rom[-1] not in 'aeEiouy' and len(word) > 2:
                    wa.append(geezroman.romanize(word))
    with open(file, encoding='utf8') as inf:
        for line in inf:
            lemma, word, feats = line.split()
            wordrom = geezroman.romanize(word)
            if wordrom.endswith("Wa"):
                wordrom0 = wordrom[:-2] + "wa"
                if wordrom0 in wa:
                    Wa.append(wordrom)
    return wa, Wa

def find_dups(file="../UM/amh/n2.um", write="../UM/amh/n3.um"):
    lemmas = {}
    dups = []
    lines = []
    all_lemmas = set()
    with open(file, encoding='utf8') as inf:
        for line in inf:
            line = line.strip()
            lemma, word, feats = line.split()
            all_lemmas.add(lemma)
            if lemma in lemmas:
                l = lemmas[lemma]
                if feats in l:
                    lfeats = l[feats]
#                    print("{} {} {} {}".format(lemma, word, feats, lfeats))
                    if len(lfeats) == 1:
                        newfeats = feats + ";LGSPEC1"
                    elif len(l[feats]) == 2:
                        newfeats = feats + ";LGSPEC2"
                    elif len(l[feats]) == 3:
                        print("3")
                        newfeats = feats + ";LGSPEC3"
                    elif len(l[feats]) == 4:
                        print("4 options: {} - {} - {}".format(lemma, word, feats))
                        newfeats = feats + ";LGSPEC4"
#                    else:
#                        print("More than 4 options: {} - {} - {} [{}]".format(lemma, word, feats, l[feats]))
                    lfeats.append(word)
                    dups.append(((lemma, word, feats), lfeats))
                    lines.append("{}\t{}\t{}".format(lemma, word, newfeats))
                else:
                    l[feats] = [word]
                    lines.append(line)
            else:
                lemmas[lemma] = {}
                lemmas[lemma][feats] = [word]
                lines.append(line)
    lines.sort(key=lambda x: x.split('\t')[0::2])
    with open(write, 'w', encoding='utf8') as file:
        for line in lines:
            print(line, file=file)
    return dups, all_lemmas

def final_check(file="../UM/amh/n2.um", pos="N"):
    stems = []
    with open(file, encoding='utf8') as inf:
        for line in inf:
            line = line.strip()
            stem, word, feats = line.split()
            if not feats.startswith(pos):
                print(line)
            if feats == pos:
                if stem != word:
                    print("Mismatched stem {}".format(stem))
                elif stem in stems:
                    print("Duplicate {}!".format(stem))
                else:
                    stems.append(stem)
    return stems

## Getting alternate spellings and generating final forms

def alt_spellings(file="../UM/amh/n.um"):
    """
    Find alternate spellings for roots with ', h, s, and S in crawl database.
    And record counts for other roots.
    """
    alts = {}
    other = {}
    with open(file, encoding='utf8') as f:
        for line in f:
            line = line.strip()
            stem, word, feats = line.split("\t")
#            if reverse:
#                word, stem = stem, word
            if stem in alts:
                continue
            stem_rom = geezroman.romanize(stem)
            if has_alts(stem_rom):
                stem_simp = stem_rom.replace('_', '')
                if stem_simp in R2G:
                    entry = R2G[stem_simp]
#                    if len(entry) == 1 and list(entry.keys())[0] == stem_simp:
#                        continue
                    alts[stem] = R2G[stem_simp]
                else:
                    count = CRAWLED.get(stem, 0)
                    other[stem] = count
            else:
                count = CRAWLED.get(stem, 0)
                other[stem] = count
    other = list(other.items())
    other.sort(key=lambda x: x[1], reverse=True)
    return alts, other

def gen_alts_others(file="../UM/amh/n1.um", alts=None, other=None, thresh=5,
                    write="../UM/amh/n2.um"):
    """
    Generate alternate forms for roots according to counts.
    For other roots, copy the forms if they exceed the threshold.
    """
    if not alts:
        alts, other = alt_spellings(file=file)
    other = dict(other)
    lines = []
    stems = []
    stemtotal = 0
    with open(file, encoding='utf8') as f:
        for line in f:
            line = line.strip()
            stem, word, feats = line.split('\t')
#            if reverse:
#                word, stem = stem, word
            stemroman = geezroman.romanize(stem)
            if stem in alts:
                stemalts = alts[stem]
                for altstem, count in stemalts.items():
                    if count <= thresh:
                        continue
                    if stem not in stems:
                        stems.append(stem)
                        stemtotal += 1
                    if altstem == stemroman:
                        # Use the existing line
                        lines.append(line)
                    else:
                        # Replace characters in word
                        newword = modify_geez(word, altstem)
                        newstem = geezroman.geezify(altstem)
                        if newstem not in stems:
                            stems.append(newstem)
                            stemtotal += 1
                        lines.append("{}\t{}\t{}".format(newstem, newword, feats))
            else:
                stemcount = other[stem]
                if stemcount <= thresh:
                    continue
                if stem not in stems:
                    stems.append(stem)
                    stemtotal += 1
                lines.append(line)
    lines.sort()
    print("Total stems: {}".format(stemtotal))
    if write:
        with open(write, 'w', encoding='utf8') as out:
            for line in lines:
                print(line, file=out)
    else:
        return lines

def simplify_roman(roman):
    """
    Simplify ^s, ^S, H, ^h, ` to s, h, '.
    """
    roman = roman.replace('^', '')
    roman = roman.replace('H', 'h').replace('`', "'")
    return roman

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
    segrom = segment_word(romanized, seg_units)
    geezrom = segment_word(geezroman.romanize(geez), seg_units)
    changes = []
    for seg in segrom:
        if seg in SIMP_PHONES:
            changes.append((seg, seg))
        elif seg in ALT_PHONES3:
            changes.append((simplify_roman(seg), seg))
    altered = []
    for char in geezrom:
        if not changes or char != changes[0][0]:
            altered.append(char)
        else:
            altered.append(changes[0][1])
            changes.pop(0)
    altered = ''.join(altered)
    return geezroman.geezify(altered)

def has_alts(roman):
    return any([x in roman for x in ALT_PHONES2])

def r2g_dict(countthresh=3, propthresh=0.05):
    dct = {}
    for word, count in CRAWLED.items():
        if count <= countthresh:
            break
        roman = geezroman.romanize(word)
        if has_alts(roman):
            roman_simp = simplify_roman(roman)
            if roman_simp in dct:
                entry = dct[roman_simp]
                entry[roman] = count
            else:
                dct[roman_simp] = {}
                dct[roman_simp][roman] = count
    remove = []
    for stem, variants in dct.items():
        remove1 = []
        total = sum(variants.values())
        for v, c in variants.items():
            if c / total <= propthresh:
                remove1.append(v)
        for v in remove1:
            del variants[v]
        if not variants or (len(variants) == 1 and stem == list(variants.keys())[0]):
            remove.append(stem)
    for item in remove:
        del dct[item]
    return dct

R2G = r2g_dict()

## Amharic

def count_lemmas():
    verbs = set()
    nouns = set()
    adj = set()
    with open("../UM/amh/v.um", encoding='utf8') as v:
        for line in v:
            l, w, f = line.strip().split("\t")
            verbs.add(l)
    with open("../UM/amh/na.um", encoding='utf8') as n:
        for line in n:
            l, w, f = line.strip().split("\t")
            if "ADJ" in f:
                adj.add(l)
            else:
                nouns.add(l)
    vc = len(verbs)
    nc = len(nouns)
    ac = len(adj)
    tot = vc + nc + ac
    return "verbs {}, nouns {}, adj {}, total {}".format(vc, nc, ac, tot)

def noun_glosses():
    dct = {}
    with open("../src/hm/languages/amh/lex/n_stem.lex", encoding='utf8') as file:
        for line in file:
            stem, x, feats = line.strip().partition('[')
            feats = '[' + feats
            stem = stem.split()[0]
            stem = stem.replace('_', '')
            stem = simplify_roman(stem)
            feats = feats.split(';')
            feats1 = feats[0]
            gloss = feats1.partition('eng="')[2].partition('"')[0]
            if not gloss:
                pass
            elif stem in dct:
                if gloss not in dct[stem]:
                    dct[stem] = dct[stem] + ',' + gloss
            else:
                dct[stem] = gloss
    with open("../src/hm/languages/amh/lex/n_stem_an.lex", encoding='utf8') as file:
        for line in file:
            stem, x, feats = line.strip().partition('[')
            feats = '[' + feats
            stem = stem.split()[0]
            stem = stem.replace('_', '')
            stem = simplify_roman(stem)
            feats = feats.split(';')
            feats1 = feats[0]
            gloss = feats1.partition('eng="')[2].partition('"')[0]
            if not gloss:
                pass
            elif stem in dct:
                if gloss not in dct[stem]:
                    dct[stem] = dct[stem] + ',' + gloss
            else:
                dct[stem] = gloss
    return dct

def write_noun_glosses():
    dct = noun_glosses()
    not_found = []
    lemgls = []
    glosses = []
    with open("../UM/amh/na.gls", 'w', encoding='utf8') as gls:
        with open("../UM/amh/na.um", encoding='utf8') as na:
            for line in na:
                lemma, word, feats = line.split("\t")
                romlemma = simplify_roman(geezroman.romanize(lemma))
                if romlemma in glosses or romlemma in not_found:
                    continue
                gloss = dct.get(romlemma)
                if not gloss:
                    print("No gloss for {},{}".format(lemma, romlemma))
                    not_found.append(romlemma)
                else:
                    glosses.append(romlemma)
                    lemgls.append("{}\t{}".format(lemma, gloss))
        print(len(glosses))
        lemgls.sort()
        for g in lemgls:
            print(g, file=gls)

def combine_nadj():
    lines = []
    with open("../UM/amh/na.um", 'w', encoding='utf8') as na:
        with open("../UM/amh/n3.um", encoding='utf8') as nouns:
            for line in nouns:
                lines.append(line.strip())
        with open("../UM/amh/a3.um", encoding='utf8') as adj:
            for line in adj:
                lines.append(line.strip())
        lines.sort()
        for line in lines:
            print(line, file=na)

def combine_glosses():
    lines = []
    with open("../UM/amh/amh.gloss", 'w', encoding='utf8') as out:
        with open("../UM/amh/vi.gls", encoding='utf8') as vi:
            for line in vi:
                lines.append(line.strip())
        with open("../UM/amh/vp.gls", encoding='utf8') as vp:
            for line in vp:
                lines.append(line.strip())
        with open("../UM/amh/na.gls", encoding='utf8') as na:
            for line in na:
                lines.append(line.strip())
        lines.sort()
        for line in lines:
            print(line, file=out)

def combine_verbs():
    lines = []
    with open("../UM/amh/v.um", 'w', encoding='utf8') as v:
        with open("../UM/amh/vp.um", encoding='utf8') as vp:
            for line in vp:
                lines.append(line.strip())
        with open("../UM/amh/vi.um", encoding='utf8') as vi:
            for line in vi:
                lines.append(line.strip())
        lines.sort()
        for line in lines:
            print(line, file=v)

def combine_all():
    lines = []
    with open("../UM/amh/amh", 'w', encoding='utf8') as out:
        with open("../UM/amh/n.um", encoding='utf8') as n:
            for line in n:
                lines.append(line.strip())
        with open("../UM/amh/v.um", encoding='utf8') as v:
            for line in v:
                lines.append(line.strip())
        lines.sort()
        for line in lines:
            print(line, file=out)

DEL = ['ኧ', 'ኦ', 'ኡ', 'ቁዋ', 'ጉዋ', 'ኩዋ', 'ሙዋ', 'ቈ', 'ኰ', 'ጐ', 'ቍ', 'ጕ', 'ኵ']

def filter_verbs(verbs):
    delete = []
    for verb in verbs:
        if any([d in verb for d in DEL]):
#        if 'ኧ' in verb or 'ጉዋ' in verb or 'ቁዋ' in verb or 'ኩዋ' in verb:
            delete.append(verb)
    for d in delete:
        verbs.remove(d)
#    if any(['ጓ' in v for v in verbs]):
#        for verb in verbs:
#            if 'ጉዋ' in verb:
#                delete.append(verb)
#    if any(['ቋ' in v for v in verbs]):
#        for verb in verbs:
#            if 'ቁዋ' in verb:
#                delete
#            results.append(verb)
#    if any(['ኳ' in v for v in results]):
#        for verb in results:
#            if 'ኩዋ' in verb:
#                continue
#            results.append(verb)
#    return results

def combine_feats(feats):
    """
    feats is a list of strings of the form [features].
    """
    return '[' + ','.join([f for f in feats if f]) + ']'

def gen_inf(root, feats):
    feats = combine_feats([feats, "v=inf,pos=n,-def"])
    inf = hm.gen('amh', root, feats, ortho_only=True)
    if not inf:
        return
    if len(inf) > 1:
        filter_verbs(inf)
    if len(inf) > 1:
        print("Multiple infinitives for {} - {}: {}".format(root, feats, inf))
    return (inf[0], "V.MSDR")

def gen_lemma(root, feats):
    feats = combine_feats([feats, "pos=v"])
    lemma = hm.gen('amh', root, feats, ortho_only=True)
    if not lemma:
        return
    if len(lemma) > 1:
        filter_verbs(lemma)
    if len(lemma) > 1:
        print("Multiple lemmas: {}".format(lemma))
    return lemma[0]

def gen_verbs(file="../UM/amh_vp_feats.txt", personal=True, write="../UM/amh/vp.um"):
    result = []
    with open(file, encoding='utf8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            root, gloss, feats = line.split(' ;;')
            forms = gen_verb(root.strip(), feats.strip(), personal=personal)
            result.extend(forms)
    if write:
        with open(write, 'w', encoding='utf8') as out:
            for line in result:
                print(line, file=out)
    else:
        return result

def verb_glosses(file="../UM/amh_vp_feats.txt", write="../UM/amh/vp.gls"):
    result = []
    with open(file, encoding='utf8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            root, gloss, feats = line.split(' ;;')
            lemma = get_lemma(root, feats)
            result.append("{}\t{}".format(lemma, gloss))
    if write:
        with open(write, 'w', encoding='utf8') as out:
            for line in result:
                print(line, file=out)
    else:
        return result

def get_verb_ortho_alt(lemma):
    romlemma = geezroman.romanize(lemma)
    alts = R2G.get(romlemma)
    if alts:
        # alternative spellings for lemma in crawl list
        alts = list(alts.items())
        alts.sort(key=lambda x: x[1], reverse=True)
        # most common alternative
        alt, score = alts[0]
        if any([a in alt for a in ALT_PHONES_V]):
            altlemma = geezroman.geezify(alt)
            print("Ortho alt {}, lemma {}".format(alt, altlemma))
            # alt contains one of the alternate characters
            return alt, lemma
    return '', ''

def get_lemma(root, feats):
    if "sb=[+plr]" in feats:
        feats = feats.replace(",sb=[+plr]", "")
    lemma = gen_lemma(root, feats)
    ortho_alt, alt_lemma = get_verb_ortho_alt(lemma)
    if alt_lemma:
        return alt_lemma
    return lemma    

def gen_verb(root, feats, personal=True):
    plural = False
    results = []
    if "sb=[+plr]" in feats:
        feats = feats.replace(",sb=[+plr]", "")
        plural = True
    lemma = gen_lemma(root, feats)
    if not lemma:
        return None, None
    ortho_alt, alt_lemma = get_verb_ortho_alt(lemma)
    inf = gen_inf(root, feats)
    forms = [inf]
    delf = ['tm']
    if personal:
        delf.append('sb')
    npng = 1
    if personal:
        if plural:
            npng = 3
        else:
            npng = 8
    forms1 = gen_verb1(root, make_features(feats), delf)
    forms2 = gen_verb1(root, make_features(feats, aux=True), delf)
    forms1 = filter_vout(forms1, plural=plural)
    forms2 = filter_vout(forms2, plural=plural)
    find_verb_dups(forms1)
    find_verb_dups(forms2)
    if len(forms1) != npng * 4:
        print("Wrong number of forms1 for {}:{} -- {}".format(root, feats, len(forms1)))
    if len(forms2) != npng * 2:
        print("Wrong number of forms2 for {}:{} -- {}".format(root, feats, len(forms2)))
    forms.extend(forms1)
    forms.extend(forms2)
    if ortho_alt:
        lemma = alt_lemma
        result = []
        for word, feats in forms:
            modword = modify_geez(word, ortho_alt)
            result.append((modword, feats))
        forms = result
    forms.sort(key=lambda x: x[1])
    for word, feats in forms:
        results.append("{}\t{}\t{}".format(lemma, word, feats))
    return results

def gen_verb1(root, feats, delfeats):
    items = hm.gen('a', root, feats, del_feats=delfeats, ortho_only=True)
    delete = []
    for item in items:
        form, fts = item
        if any([d in form for d in DEL]):
            delete.append(item)
    for d in delete:
        items.remove(d)
    return items

def gen_cop():
    items = hm.gen('amh', 'ne', "[tm=prs]", del_feats=['sb'], ortho_only=True)
    items.sort()
    return ["ነው\t{}\t{}".format(i[0], 'V;' + i[1]) for i in items]

def gen_exist():
    items = hm.gen('amh', 'hlw', "[tm=prs]", del_feats=['sb'], ortho_only=True)
    items.sort()
    return ["አለ\t{}\t{}".format(i[0], i[1]) for i in items]

def gen_was():
    items = hm.gen('amh', 'nbr', "[tm=prf]", del_feats=['sb'], ortho_only=True)
    items.sort()
    return ["ነበረ\t{}\t{}".format(i[0], i[1]) for i in items]

def find_verb_dups(verbfeats):
    featdict = {}
    delete = []
    for item in verbfeats:
        feats = item[1]
        if feats in featdict:
            if item not in featdict[feats]:
                featdict[feats].append(item)
            else:
                delete.append(item)
        else:
            featdict[feats] = [item]
    if delete:
        for d in delete:
            verbfeats.remove(d)
    if not featdict:
        return
    featlist = list(featdict.items())
    featlist = [f for f in featlist if len(f[1]) > 1]
    if featlist:
        delete = []
        deldup = []
        for dups in featlist:
            for p in V_PREF:
#                print("Checking dups {} against {}".format(dups, p))
                if any([v[0].endswith(p[0]) for v in dups[1]]):
                    # preferred item is there; delete the others
                    for dup in dups[1]:
                        if not dup[0].endswith(p[0]):
#                            print(" Deleting {}".format(dup))
                            delete.append(dup)
                    deldup.append(dups)
                    # don't check any more preferences
                    break
            for dp in V_DISPREF:
                if any([dp in v[0] for v in dups[1]]):
                    for dup in dups[1]:
                        if dp in dup[0]:
                            delete.append(dup)
                    deldup.append(dups)
                    break
        for d in deldup:
            if d in featlist:
                featlist.remove(d)
        for d in delete:
            verbfeats.remove(d)
        if featlist:
            print("Found dups: {}".format(featlist))
    return featlist

V_PREF = [('ቅሁ', 'ቅኩ', 'ኩ'), ('ቅህ', 'ቅክ', 'ክ'),
          ('ግሁ', 'ግኩ', 'ኩ'), ('ግህ', 'ግክ', 'ክ'),
          ('ክ', 'ህ'), ('ኩ', 'ሁ'),
#          ("ጥቶ", "ቶ"), ("ጥቷል", "ቷል"), ("ጥተው", "ተው"), ("ጥተን", "ተን"),
#          ("ጥተህ", "ተህ"), ("ጥታችሁ", "ታችሁ"),
          ("ሺ", "ሽ "), ("ቺ", "ች"), ("ጂ", "ጅ"), ("ዢ", "ዥ"),
          ("ዪ", "ይ"), ("ጪ", "ጭ"), ("ኚ", "ኝ")]

V_DISPREF = ["ዪያ", "ጪያ", "ኚያ", "ጂያ", "ሺያ", "ቺያ", "ዬያ", "ሼያ"]

def make_features(feats, aux=False):
    feats = [feats, 'pos=v']
#    if plural:
#        feats.append('sb=[+plr]')
    if aux:
        feats.append('ax=al')
    return combine_feats(feats)

DEL_FEATS = ['CAUS', 'TR', 'RECP', '*CON', 'PASS']

def filter_vout(forms, plural=False):
    """
    Remove aspect/valency features we're not dealing with, and delete
    plural forms if plural is True.
    """
    result = []
    for form, feats in forms:
        if plural and 'PL' not in feats.split(';'):
            continue
        for df in DEL_FEATS:
            feats = feats.replace(";" + df, '')
        result.append((form, feats))
    return result

def get_eng_verbs():
    '''
    Create stem-to-ppp dict for English verbs.
    '''
    verbs = {}
    with open("../../../../Projects/LingData/En/v_analyzed.lex") as file:
        for line in file:
            if "tam=pp" in line:
                pp, stem, feats = line.split()
                verbs[stem] = pp
    return verbs

ENG_PP = get_eng_verbs()

def eng_passive(stem):
    if ' ' in stem:
        stem = stem.split()
        return "be " + ENG_PP[stem[0]] + " " + ' '.join(stem[1:])
    return "be " + ENG_PP[stem]

LEXFEATS = [("vc=ps", "ps"), ("-smp", "-smp"), # ("+lextr", "lextr"),
            ("+lexip", "lexip"), ("+lexav", "lexav"), ("+lexrp", "lexrp"),
            ("vc=cs", "cs"), ("vc=tr", "tr"), ("as=rc", "rc"), ("as=it", "it"),
            ("as=smp", "smpas")]

def get_verb_feats():
    verbs = {}
    with open("../old/languages/old/amh/lex/v_root.lex", encoding='utf8') as file:
        for line in file:
            root, x, feats = line.strip().partition('[')
            feats = '[' + feats
            root = root.split()[0]
            feats = feats.split(';')
            for feat in feats:
                cls, x, feat = feat.partition(',')
                cls = cls.partition('=')[2]
                gloss = feat.partition("eng='")[2].partition("'")[0]
                if not gloss:
                    continue
                rootcls = "<{}:{}>".format(root, cls)
                lex = [x[1] for x in LEXFEATS if x[0] in feat]
                if rootcls in verbs:
                    verbs[rootcls].append((gloss, lex))
                else:
                    verbs[rootcls] = [(gloss, lex)]
    with open("../old/languages/old/amh/lex/irr_stem.lex", encoding='utf8') as file:
        for line in file:
            if line[0] == '#':
                continue
            root, x, feats = line.strip().partition('[')
            feats = '[' + feats
#            print("{} {}".format(root, feats))
            root = root.split()[1]
#            print(root)
            feats = feats.split(';')
            for feat in feats:
                cls, x, feat = feat.partition(',')
                cls = cls.partition('=')[2]
                gloss = feat.partition('eng="')[2].partition('"')[0]
                rootcls = "<{}:{}>".format(root, cls)
#                if root == "x'":
#                    print("{} {}".format(rootcls, gloss))
                if not gloss:
                    continue
                rootcls = "<{}:{}>".format(root, cls)
                lex = [x[1] for x in LEXFEATS if x[0] in feat]
                if rootcls in verbs:
                    if (gloss, lex) not in verbs[rootcls]:
                        verbs[rootcls].append((gloss, lex))
                else:
                    verbs[rootcls] = [(gloss, lex)]
    return verbs

AMH_VROOTS = get_verb_feats()

LEXVAL2VAL = {'smp': '', 'ps': 'vc=ps', 'tr': 'vc=tr', 'cs': 'vc=cs',
              'con': 'as=rc,vc=ps', 'contr': 'as=rc,vc=tr',
              'recp': 'as=it,vc=ps', 'recpcs': 'as=it,vc=tr',
              'iter': 'as=it'}

def change_glosses(glosses, feat):
    glosses = glosses.split(',')
    glosses = [change_gloss(g, feat) for g in glosses]
    if glosses:
        return ','.join([g for g in glosses if g])
    return None

def change_gloss(stem, feat):
    if feat == 'smp':
        return stem
    elif feat == 'ps':
        return eng_passive(stem)
    elif feat in ['tr', 'cs']:
        return "cause to " + stem
    elif feat == 'iter':
        return stem + " repeatedly"
    elif feat == 'recp':
        return stem + " one another"
    elif feat == 'recpcs':
        return "cause to " + stem + " one another"
#    else:
#        print("Don't know how to change gloss {} for feature {}".format(stem, feat))

def lex2vals(file="../UM/amh_vp_cats.txt", write="../UM/amh_vp_feats.txt"):
    result = []
    with open(file, encoding='utf8') as f:
        for line in f:
            line = line.strip().split()
            root, feat = line[0], line[1]
            lv = lex2val(root, feat)
            if lv:
                result.append(lv)
    if write:
        with open(write, 'w', encoding='utf8') as f:
            for item in result:
                for root, gloss, feats in item:
                    print("{} ;; {} ;; {}".format(root, gloss, feats), file=f)
    return result

def filter_lexvalfeats(lexfeats, lexval):
    '''
    Each of lexfeats is root, gloss, feats (all roots the same).
    lexval is one of smp, ps, cs, etc.
    '''
    if lexval == 'smp':
        # prefer vc=ps over other values
        ps = None
        empty = None
        other = []
        for root, gloss, feats in lexfeats:
            if feats == 'vc=ps':
                ps = root, gloss, feats
            elif feats == '':
                empty = root, gloss, feats
            else:
                other.append((root, gloss, feats))
        if empty and other:
            return [empty]
        elif ps and other:
            return [ps]
            
    return lexfeats

def lex2val(root, lexval):
    """
    Given a root and a 'lexical valency'
    (smp, ps, tr, cs, con, contr, recp, recpcs, iter),
    output a 'raw' valency (as and vc features) for generation.
    Return the features and the associated gloss.
    """
    entry = AMH_VROOTS[root]
    result = []
    for gloss, lexfeats in entry:
        val = None
        if not lexfeats:
            val = LEXVAL2VAL[lexval]
            gloss = change_glosses(gloss, lexval)
        elif lexval == 'smp':
            if 'rc' in lexfeats and '-smp' in lexfeats:
                val = LEXVAL2VAL['recp']
            elif 'tr' in lexfeats and '-smp' in lexfeats:
                val = LEXVAL2VAL['tr']
            elif 'cs' in lexfeats and '-smp' in lexfeats:
                val = LEXVAL2VAL['cs']
            elif 'it' in lexfeats and '-smp' in lexfeats:
                val = LEXVAL2VAL['iter']
            elif '-smp' in lexfeats:
                val = LEXVAL2VAL['ps']
            else:
                continue
#                print("Not sure what to do with {} ; {}".format(root, lexval))
        elif lexval == 'ps':
            if '-smp' in lexfeats:
                if 'it' in lexfeats:
                    continue
                if 'ps' in lexfeats or len(lexfeats) == 1:
                    val = LEXVAL2VAL['ps']
            elif 'ps' in lexfeats and 'lexav' in lexfeats and 'rc' not in lexfeats:
                val = LEXVAL2VAL['ps']
#                else:
#                    print("Not sure what to do with {} ; {}".format(root, lexval))
#            else:
#                print("Not sure what to do with {} ; {}".format(root, lexval))
        elif lexval == 'tr':
            if 'tr' in lexfeats and 'rc' not in lexfeats:
                val = LEXVAL2VAL['tr']
            elif "-smp" in lexfeats:
                gloss = change_glosses(gloss, 'tr')
                val = LEXVAL2VAL['tr']
        elif lexval == 'cs':
            if 'rc' in lexfeats or 'it' in lexfeats:
                continue
            if 'cs' in lexfeats:
                val = LEXVAL2VAL['cs']
#            elif 'tr' in lexfeats and 'rc' not in lexfeats:
#                val = LEXVAL2VAL['tr']
            elif "-smp" in lexfeats or 'smpas' in lexfeats or 'lexav' in lexfeats:
                gloss = change_glosses(gloss, 'cs')
                val = LEXVAL2VAL['cs']
        elif lexval == 'con':
            if 'rc' in lexfeats and 'tr' not in lexfeats:
                val = LEXVAL2VAL['con']
            elif 'lexrp' in lexfeats and 'tr' not in lexfeats:
                val = LEXVAL2VAL['con']
        elif lexval == 'contr':
            if 'rc' in lexfeats and 'tr' in lexfeats:
                val = LEXVAL2VAL['contr']
        elif lexval == 'recp':
            if 'rc' in lexfeats or 'smpas' in lexfeats:
                continue
            if 'lexrp' in lexfeats:
                val = LEXVAL2VAL['recp']
            elif 'lexip' in lexfeats:
                if 'tr' in lexfeats:
                    continue
                val = LEXVAL2VAL['recp']
            elif "-smp" in lexfeats:
                if 'it' not in lexfeats:
                    if 'ps' in lexfeats:
                        continue
                    gloss = change_glosses(gloss, 'recp')
                val = LEXVAL2VAL['recp']
        elif lexval == 'recpcs':
            if ("-smp" in lexfeats) and ('it' in lexfeats) and ('tr' in lexfeats):
                val = LEXVAL2VAL['recpcs']
            elif 'lexip' in lexfeats and 'tr' in lexfeats:
                val = LEXVAL2VAL['recpcs']
        elif lexval == 'recpcs':
            if 'it' in lexfeats:
                val = LEXVAL2VAL['iter']
        if val != None and gloss != '' and (root, gloss, val) not in result:
            result.append((root, gloss, val))
    if not result:
        print("No result for {}, {}".format(root, lexval))
    if len(result) > 1:
        elim = []
        for r, g, v in result:
            if "cause to " in g:
                elim.append((r, g, v))
        if elim and len(elim) < len(result):
            for e in elim:
                result.remove(e)
    if len(result) > 1:
        result = filter_lexvalfeats(result, lexval)
    if len(result) > 1:
        print("Multiple results for {}, {}: {}".format(root, lexval, result))
    return result

def make_FS(feats):
    """
    feats is a list of strings, e.g., "sb=[+p2]".
    Returns a list that can be converted directly to FeatStruct.
    """
    feats = '[' + ','.join([f for f in feats if f]) + ']'
    return feats

HM2UM = {'sb=[+p1]': '1;SG',
         'sb=[+p2]': '2;SG;MASC',
         'sb=[+p2,+fem]': '2;SG;FEM',
         'tm=prf': 'PFV',
         'tm=imf,ax=None': 'IPFV;NFIN',
         'tm=imf,ax=al': 'IPFV',
         'tm=j_i': 'IMP',
         'tm=ger,ax=al': 'PRF',
         'tm=ger,ax=None': 'V.CVB',
         'pos=n,v=inf,-def': 'V.MSDR'}

TAM = ['tm=prf', 'tm=imf,ax=None', 'tm=imf,ax=al',
       'tm=j_i', 'tm=ger,ax=None', 'tm=ger,ax=al']

PNG = ['sb=[+p1]', 'sb=[+p1,+plr]', 'sb=[+p2]', 'sb=[+p2,+fem]', 'sb=[+p2,+plr]',
       'sb=[-p1,-p2]', 'sb=[-p1,p2,+fem]', 'sb=[-p1,-p2,+plr]']

def hm2um(tam, png, val):
    um = HM2UM.get(tam)
    upng = HM2UM.get(png)
    if upng:
        um += ';' + upng
    return um

##def gen_verb1(root, cat, png='', tam=''):
##    um = hm2um(tam, png, None)
##    feats = [png, tam]
##    if cat == 'tr':
##        feats.append('vc=tr')
##    elif cat == 'cs':
##        feats.append('vc=cs')
##    elif cat == 'ps':
##        feats.append('vc=ps')
##    elif cat == 'iter':
##        feats.append('as=it')
##    feats = make_FS(feats)
##    print(feats)
##    form = hm.gen('amh', root, feats, ortho_only=True)
##    if form:
##        return form, um

def prefer(forms, preferences, length=True):
    """
    Preferences is a list of pairs, with the preferred element first.
    Returns the form(s) within forms that satisfy the preferences.
    If length is True, prefer longer forms.
    """
    delete = []
    if length:
        lengths = [len(form) for form in forms]
        if len(set(lengths)) > 1:
            # lengths are not all equal
            maxlength = max(lengths)
            for f, l in zip(forms, lengths):
                if l < maxlength:
                    delete.append(f)
        for d in delete:
            forms.remove(d)
    if len(forms) > 1:
        for prefs in preferences:
            p1 = prefs[0]
            p2 = prefs[1:]
            preferred = []
            dispreferred = []
            for form in forms:
                if form.endswith(p1):
                    preferred.append(form)
                elif any([form.endswith(pp2) for pp2 in p2]):
                    dispreferred.append(form)
            if preferred and dispreferred:
                delete.extend(dispreferred)
        for d in delete:
            forms.remove(d)

def check_lemmas(file="../UM/amh/n.um", pos='N'):
    lemmas = []
    with open(file, encoding='utf8') as inf:
        for line in inf:
            form, root, feats = line.split("\t")
            feats = feats.strip()
            if feats == pos and form != root:
                lemmas.append((form, root))
    return lemmas

def sort_nouns(items, featpos=1):
    order = ['3P', '2P', '1P', '3SF', '3SM', '2SF', '2SM', 'FORM', '1S', 'DEF']
    def order_func(item):
        feat = item[featpos]
        for i, o in enumerate(order):
            if o in feat:
                return i
        return len(order)
    # items is list of (lemma, gloss, word, feat) tuples
    items.sort(key=order_func, reverse=True)

def gen1noun(stem, ps=False, pl=False, write=True):
    forms = []
    geezstem = geezroman.geezify(stem)
    bare = gen_line(stem, "N")
    masc = gen_line(stem, "N;DEF;MASC")
    fem = gen_line(stem, "N;DEF;FEM", ["wa", "Wa"], [("Wa", "wa")], True)
    if masc or fem:
        forms.extend(bare)
        if masc:
            forms.extend(masc)
        if fem:
            forms.extend(fem)
    if pl:
        plur = gen_line(stem, "N;PL")
        pldef = gen_line(stem, "N;DEF;PL")
        if plur or pldef:
            forms.extend(plur)
            forms.extend(pldef)
    if ps:
        poss = hm.gen('amh', stem, pos='n', ortho_only=True, del_feats=["poss"], features="[-det,+def,-prp]")
        del_dispref(poss, [("Wa", "wa")])
        sort_nouns(poss)
        poss = ["{}\t{}\t{}".format(geezstem, form, feats) for form, feats in poss]
        forms.extend(poss)
    if ps and pl:
        plposs = hm.gen('amh', stem, pos='n', ortho_only=True, del_feats=["poss"], features="[-det,+def,+plr,-prp]")
        del_dispref(plposs, [("Wa", "wa")])
        sort_nouns(plposs)
        plposs = ["{}\t{}\t{}".format(geezstem, form, feats) for form, feats in plposs]
        forms.extend(plposs)
    if write:
        for form in forms:
            print(form)
    else:
        return forms

def gen_noun4(write=False):
    """
    Nouns with plural and possessive suffixes.
    """
    nongen = []
    lines = []
    with open("../UM/amh_nplposs_um.txt", encoding='utf8') as file:
        for line in file:
            forms = []
            if not line.strip():
                continue
            stem = line.split()[0].strip()
            bare = gen_line(stem, "N")
            if not bare:
                continue
            geezstem = geezroman.geezify(stem)
            masc = gen_line(stem, "N;DEF;MASC")
            fem = gen_line(stem, "N;DEF;FEM", ["wa", "Wa"], [("Wa", "wa")], True)
            if masc or fem:
                forms.append(bare)
                if masc:
                    forms.append(masc)
                if fem:
                    forms.append(fem)
            plur = gen_line(stem, "N;PL")
            pldef = gen_line(stem, "N;DEF;PL")
            poss = hm.gen('amh', stem, pos='n', ortho_only=True, del_feats=["poss"], features="[-det,+def,-prp]")
            del_dispref(poss, [("Wa", "wa")])
            sort_nouns(poss)
            poss = ["{}\t{}\t{}".format(geezstem, form, feats) for form, feats in poss]
            forms.append(poss)
            plposs = hm.gen('amh', stem, pos='n', ortho_only=True, del_feats=["poss"], features="[-det,+def,+plr,-prp]")
            del_dispref(plposs, [("Wa", "wa")])
            sort_nouns(plposs)
            plposs = ["{}\t{}\t{}".format(geezstem, form, feats) for form, feats in plposs]
            forms.append(plposs)
            if plur or pldef:
                forms.extend([plur, pldef])
            if not forms:
                nongen.append(stem)
            for form in forms:
                for f in form:
                    if write:
                        lines.append(f)
                    else:
                        print(f)
    if write:
        with open("../UM/nplposs.um", 'w', encoding='utf8') as file:
            for line in lines:
                print(line, file=file)
    return nongen

def gen_noun3(write=False):
    """
    Nouns with plural, but not possessive, suffixes.
    """
    nongen = []
    lines = []
    with open("../UM/amh_npl_um.txt", encoding='utf8') as file:
        for line in file:
            forms = []
            stem = line.split()[0].strip()
            bare = gen_line(stem, "N")
            if not bare:
                continue
            masc = gen_line(stem, "N;DEF;MASC")
            fem = gen_line(stem, "N;DEF;FEM", ["wa", "Wa"], [("Wa", "wa")], True)
            if masc or fem:
                forms.append(bare)
                if masc:
                    forms.append(masc)
                if fem:
                    forms.append(fem)
            plur = gen_line(stem, "N;PL")
            pldef = gen_line(stem, "N;DEF;PL")
            if plur or pldef:
                forms.extend([plur, pldef])
            if not forms:
                nongen.append(stem)
            for form in forms:
                for f in form:
                    if write:
                        lines.append(f)
                    else:
                        print(f)
    if write:
        with open("../UM/amh/npl.um", 'w', encoding='utf8') as file:
            for line in lines:
                print(line, file=file)
    return nongen

def gen_noun2(write=False):
    """
    Nouns with possessive, but not plural, suffixes.
    """
    nongen = []
    lines = []
    with open("../UM/amh_nposs_um.txt", encoding='utf8') as file:
        for line in file:
            forms = []
            stem = line.split()[0].strip()
            bare = gen_line(stem, "N")
            geezstem = geezroman.geezify(stem)
            if not bare:
                continue
            masc = gen_line(stem, "N;DEF;MASC")
            fem = gen_line(stem, "N;DEF;FEM", ["wa", "Wa"], [("Wa", "wa")], True)
            if masc or fem:
                forms.append(bare)
                if masc:
                    forms.append(masc)
                if fem:
                    forms.append(fem)
            poss = hm.gen('amh', stem, ortho_only=True, del_feats=["poss"], features="[-det,+def]")
            del_dispref(poss, [("Wa", "wa")])
            sort_nouns(poss)
            poss = ["{}\t{}\t{}".format(geezstem, form, feats) for form, feats in poss]
            forms.append(poss)
#            plur = gen_line(stem, "ADJ;PL")
#            pldef = gen_line(stem, "ADJ;DEF;PL")
#            if plur or pldef:
#                forms.extend([plur, pldef])
            if not forms:
                nongen.append(stem)
            for form in forms:
                for f in form:
                    if write:
                        lines.append(f)
                    else:
                        print(f)
    if write:
        with open("../UM/amh/nposs.um", 'w', encoding='utf8') as file:
            for line in lines:
                print(line, file=file)
    return nongen

def gen_noun1(write=False):
    nongen = []
    lines = []
    with open("../UM/amh_n_um.txt", encoding='utf8') as file:
        for line in file:
            forms = []
            stem = line.split()[0].strip()
            bare = gen_line(stem, "N")
            if not bare:
                continue
            masc = gen_line(stem, "N;DEF;MASC")
            fem = gen_line(stem, "N;DEF;FEM", ["wa", "Wa"], [("Wa", "wa")], True)
            if masc or fem:
                forms.append(bare)
                if masc:
                    forms.append(masc)
                if fem:
                    forms.append(fem)
#            plur = gen_line(stem, "ADJ;PL")
#            pldef = gen_line(stem, "ADJ;DEF;PL")
#            if plur or pldef:
#                forms.extend([plur, pldef])
            if not forms:
                nongen.append(stem)
            for form in forms:
                for f in form:
                    if write:
                        lines.append(f)
                    else:
                        print(f)
    if write:
        with open("../UM/amh/n.um", 'w', encoding='utf8') as file:
            for line in lines:
                print(line, file=file)
    return nongen

def del_dispref(forms, prefer):
    """
    forms is a list of form, feature pairs.
    prefer is a list of string pairs, the first being a suffix to prefer over the second.
    """
    for preferred, other in prefer:
        pref = []
        dispref = []
        for form, feats in forms:
            rom = geezroman.romanize(form)
            if rom.endswith(preferred):
                pref.append((form, feats))
            elif rom.endswith(other):
                dispref.append((form, feats))
        if pref and dispref:
            # Preferred form appears; delete dispreferred
#                    print("Found preferred {} and dispreferred {}".format(pref, nonpref))
            for dp in dispref:
                forms.remove(dp)

def gen_lines(stem, featlist, retain=[], prefer=[], check=False):
    """
    Return a list of lines for the given stem and each of the UM feat clusters in featlist.
    """
    result = []
    for feats in featlist:
        lines = gen_line(stem, feats, retain=retain, prefer=prefer, check=check)
        if lines:
            result.extend(lines)
    return result

def gen_line(stem, feats, retain=[], prefer=[], check=False):
    result = []
    forms = hm.gen('amh', stem, um=feats, ortho_only=True)
    if forms:
        if len(forms) > 1:
            crawled_forms = [form for form in forms if form in CRAWLED]
            if not crawled_forms:
                if retain:
                    crawled_forms = \
                        [form for form in forms if any([geezroman.romanize(form).endswith(r) for r in retain])]
                    if not crawled_forms:
                        print("None found: {}".format(forms))
                        return []
                    else:
                        forms = crawled_forms
            else:
                forms = crawled_forms
        if prefer:
            for preferred, other in prefer:
                pref = []
                nonpref = []
                for form in forms:
                    rom = geezroman.romanize(form)
                    if rom.endswith(preferred):
                        pref.append(form)
                    elif rom.endswith(other):
                        nonpref.append(form)
                if pref and nonpref:
                    # Preferred form appears; delete dispreferred
#                    print("Found preferred {} and dispreferred {}".format(pref, nonpref))
                    for np in nonpref:
                        forms.remove(np)
        if check:
            remove = []
            for form in forms:
                if form not in CRAWLED:
                    remove.append(form)
            for f in remove:
                forms.remove(f)
        for form in forms:
            geezstem = geezroman.geezify(stem)
            result.append("{}\t{}\t{}".format(geezstem, form, feats))
    return result

def gen_adj(write=False):
    insing = True
    nongen = []
    lines = []
    with open("../UM/amh_adj_um.txt", encoding='utf8') as file:
        for line in file:
            forms = []
            stem = line.strip()
            if not stem:
                insing = False
            else:
                bare = gen_line(stem, "ADJ")
                if not bare:
                    continue
                masc = gen_line(stem, "ADJ;DEF;MASC")
                fem = gen_line(stem, "ADJ;DEF;FEM", ["wa", "Wa"], [("Wa", "wa")])
                if masc or fem:
                    forms.extend([bare, masc, fem])
                if not insing:
                    plur = gen_line(stem, "ADJ;PL")
                    pldef = gen_line(stem, "ADJ;DEF;PL")
                    if plur or pldef:
                        forms.extend([plur, pldef])
                if not forms:
                    nongen.append(stem)
                for form in forms:
                    for f in form:
                        if write:
                            lines.append(f)
                        else:
                            print(f)
    if write:
        with open("../UM/amh/adj.um", 'w', encoding='utf8') as file:
            for line in lines:
                print(line, file=file)
    return nongen

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

##def proc_ti_verbs():
##    with open("hm/languages/tir/lex/v_root.lex", encoding='utf8') as infile:
##        with open("v_root.lex", 'w', encoding='utf8') as outfile:
##            for line in infile:
##                line = line.strip()
##                if len(line.split()) > 1:
##                    print(line, file=outfile)
##                else:
##                    print("{}  ''  [cls=A]".format(line), file=outfile)                    

## Tigrinya

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

def main():
    pass

if __name__ == "__main__": main()
