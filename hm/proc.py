"""
Create Am<->Ks lexicon.
"""

from . import morpho

AM = morpho.get_language('am')
KS = morpho.get_language('ks')
FS = morpho.FeatStruct

def proc_source_feats(feats):
    fs = FS()
    if feats:
        for feat in ['as', 'vc', 'neg']:
            fs[feat] = feats[feat]
    return fs

def read_dict1():
    entries = []
    multi = []
    n = 0
    bad = []
    with open("../LingData/Ks/v_am2ks.txt", encoding='utf8') as file:
        for line in file:
            n += 1
            if n % 25 == 0:
                print("{} lines".format(n))
            linesplit = line.split(';')
            if len(linesplit) != 2:
                print("line {} too long!".format(linesplit))
                continue
            am, ks = linesplit
            ks = ks.strip().split(':')
            if am.strip().endswith("አለ"):
                multi.append((am, ks))
#            if len(am.split()) > 1:
#                if "አለ" not in am:
#                    print("Couldn't analyze {} because it doesn't contain አለ".format(am))
            else:
                am_proc = AM.anal_word(am,
                                       init_weight=FS("[pos=v,tm=prf,sb=[-p1,-p2],-rel,-acc,ax=None,-sub]"),
                                       guess=False, preproc=True)
            if am_proc:
                entries.append(([(a[0], proc_source_feats(a[1])) for a in am_proc], ks))
            else:
                bad.append((am, ks))
#                am_proc_guess = AM.anal_word(am,
#                                             init_weight=FS("[pos=v,tm=prf,sb=[-p1,-p2],-rel,-acc,ax=None,-sub]"),
#                                             only_guess=True, preproc=True)
#                if am_proc_guess:
#                    roots = [a[0] for a in am_proc_guess]
#                    if roots not in newroots:
#                        newroots.append(roots)
#                else:
#                    print("Couldn't analyze {}".format(am))
    return entries, multi


