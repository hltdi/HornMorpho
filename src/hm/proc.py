"""
-- Miscellaneous functions to access and create lexicons, using
   data from LingData, as well as in HornMorpho language files.
---- Create Am<->Ks lexicon.
---- Recreate Ti lexicon, eliminating non-root characters.
---- Create reverse dictionary for noun roots.
---- Create Ti fidel lexicons.
---- Group analyzed corpora by voice-valency features.
---- Compile frequencies of Am roots and verb root+voice categories.
"""

from . import morpho
import re, math, os

from hm.root_anal import *

#from . import internet_search

#A = morpho.get_language('amh')
#KS = morpho.get_language('ks')
FS = morpho.FeatStruct
FSS = morpho.FSSet
geezify = morpho.geez.geezify
normalize = morpho.geez.normalize
is_geez = morpho.geez.is_geez
romanize = lambda x: morpho.geez.romanize(x, normalize=True)
OS = morpho.os
VPOS = FS("[pos=v,tm=prf,sb=[-p1,-p2,-plr],pp=None,cj2=None,-rel,-sub]")
INF = [FS("[v=inf,cls=A,-def]"), FS("[v=inf,cls=B,-def]")]
IMP = [FS("[pos=v,tm=j_i,cls=A]"), FS("[pos=v,tm=j_i,cls=B]")]
IMPFEM = [FS("[pos=v,tm=j_i,cls=A,sb=[+fem]]"), FS("[pos=v,tm=j_i,cls=B,sb=[+fem]]")]
IMPPL = [FS("[pos=v,tm=j_i,cls=A,sb=[+plr]]"), FS("[pos=v,tm=j_i,cls=B,sb=[+plr]]")]
#abyss = internet_search.abyssinica
#goog = internet_search.google
# VGEN = A.morphology['v'].gen
VPOSP = FS("[pos=v,tm=prf,sb=[-p1,-p2,-plr],vc=ps,pp=None,cj2=None,-rel,-sub]")
VPOST = FS("[pos=v,tm=prf,sb=[-p1,-p2,-plr],vc=tr,pp=None,cj2=None,-rel,-sub]")
VPOSR = FS("[pos=v,tm=prf,sb=[-p1,-p2,-plr],as=rc,vc=ps,pp=None,cj2=None,-rel,-sub]")
VPOSRT = FS("[pos=v,tm=prf,sb=[-p1,-p2,-plr],as=rc,vc=tr,pp=None,cj2=None,-rel,-sub]")

CONS = "bcCdfghHkKlmnNpPqrsStTwxyzZ"

ASVC = \
  {'[as=smp,vc=smp]': '0', '[as=smp,vc=ps]': 'te-', '[as=smp,vc=tr]': 'a-', '[as=smp,vc=cs]': 'as-',
   '[as=rc,vc=ps]': 'te-a', '[as=rc,vc=tr]': 'a-a', '[as=rc,vc=cs]': 'as-a',
   '[as=it,vc=smp]': 'R', '[as=it,vc=ps]': 'te-R', '[as=it,vc=tr]': 'a-R', '[as=it,vc=cs]': 'as=R'}

CODE2FS = \
  {'0':    "[cls={},as=smp,vc=smp,pos=v,tm=prf,sb=[-p1,-p2,-plr],pp=None,cj2=None,-rel,-sub]",
   'te_':  "[cls={},as=smp,vc=ps,pos=v,tm=prf,sb=[-p1,-p2,-plr],pp=None,cj2=None,-rel,-sub]",
   'a_':   "[cls={},as=smp,vc=tr,pos=v,tm=prf,sb=[-p1,-p2,-plr],pp=None,cj2=None,-rel,-sub]",
   'as_':  "[cls={},as=smp,vc=cs,pos=v,tm=prf,sb=[-p1,-p2,-plr],pp=None,cj2=None,-rel,-sub]",
   'te_a': "[cls={},as=rc,vc=ps,pos=v,tm=prf,sb=[-p1,-p2,-plr],pp=None,cj2=None,-rel,-sub]",
   'a_a':  "[cls={},as=rc,vc=tr,pos=v,tm=prf,sb=[-p1,-p2,-plr],pp=None,cj2=None,-rel,-sub]",
   'as_a': "[cls={},as=rc,vc=cs,pos=v,tm=prf,sb=[-p1,-p2,-plr],pp=None,cj2=None,-rel,-sub]",
   'R':    "[cls={},as=it,vc=smp,pos=v,tm=prf,sb=[-p1,-p2,-plr],pp=None,cj2=None,-rel,-sub]",
   'te_R': "[cls={},as=it,vc=ps,pos=v,tm=prf,sb=[-p1,-p2,-plr],pp=None,cj2=None,-rel,-sub]",
   'a_R':  "[cls={},as=it,vc=tr,pos=v,tm=prf,sb=[-p1,-p2,-plr],pp=None,cj2=None,-rel,-sub]",
   'as_R': "[cls={},as=it,vc=cs,pos=v,tm=prf,sb=[-p1,-p2,-plr],pp=None,cj2=None,-rel,-sub]"
   }

CODECLS2FS = \
  {'0':    {'A': FS("[cls=A,as=smp,vc=smp,pos=v,tm=prf,sb=[-p1,-p2,-plr],pp=None,cj2=None,-rel,-sub]")},
   'te_':  {'A': FS("[cls=A,as=smp,vc=ps,pos=v,tm=prf,sb=[-p1,-p2,-plr],pp=None,cj2=None,-rel,-sub]")},
   'a_':   {'A': FS("[cls=A,as=smp,vc=tr,pos=v,tm=prf,sb=[-p1,-p2,-plr],pp=None,cj2=None,-rel,-sub]")},
   'as_':  {'A': FS("[cls=A,as=smp,vc=cs,pos=v,tm=prf,sb=[-p1,-p2,-plr],pp=None,cj2=None,-rel,-sub]")},
   'te_a': {'A': FS("[cls=A,as=rc,vc=ps,pos=v,tm=prf,sb=[-p1,-p2,-plr],pp=None,cj2=None,-rel,-sub]")},
   'a_a':  {'A': FS("[cls=A,as=rc,vc=tr,pos=v,tm=prf,sb=[-p1,-p2,-plr],pp=None,cj2=None,-rel,-sub]")},
   'as_a': {'A': FS("[cls=A,as=rc,vc=cs,pos=v,tm=prf,sb=[-p1,-p2,-plr],pp=None,cj2=None,-rel,-sub]")},
   'R':    {'A': FS("[cls=A,as=it,vc=smp,pos=v,tm=prf,sb=[-p1,-p2,-plr],pp=None,cj2=None,-rel,-sub]")},
   'te_R': {'A': FS("[cls=A,as=it,vc=ps,pos=v,tm=prf,sb=[-p1,-p2,-plr],pp=None,cj2=None,-rel,-sub]")},
   'a_R':  {'A': FS("[cls=A,as=it,vc=tr,pos=v,tm=prf,sb=[-p1,-p2,-plr],pp=None,cj2=None,-rel,-sub]")},
   'as_R': {'A': FS("[cls=A,as=it,vc=cs,pos=v,tm=prf,sb=[-p1,-p2,-plr],pp=None,cj2=None,-rel,-sub]")}
   }

CODE2ASVC = \
  {'0':    {'as': 'smp', 'vc': 'smp'},
   'te_':  {'as': 'smp', 'vc': 'ps'},
   'a_':   {'as': 'smp', 'vc': 'tr'},
   'as_':  {'as': 'smp', 'vc': 'cs'},
   'te_a': {'as': 'rc', 'vc': 'ps'},
   'a_a':  {'as': 'rc', 'vc': 'tr'},
   'as_a': {'as': 'rc', 'vc': 'cs'},
   'R':    {'as': 'it', 'vc': 'smp'},
   'te_R': {'as': 'it', 'vc': 'ps'},
   'a_R':  {'as': 'it', 'vc': 'tr'},
   'as_R': {'as': 'it', 'vc': 'cs'}}

AS_WLD = ['', '', '', '0', 'te_', 'te_a', 'te_R', 'a_', 'a_a', 'a_R', 'as_', 'R', '', '']

CODE2AS = {'te_': 4, 'te_a': 5, 'te_R': 6, 'a_': 7, 'a_a': 8, 'a_R': 9, 'as_': 10, 'R': 11}

CODE2GCODE = {'te_': "ተ", 'te_a': "ተ_ኣ", 'te_R': "ተ_ደ", 'a_': "ኣ", 'a_a': "ኣ_ኣ", 'a_R': "ኣ_ደ", 'as_': "ኣስ", 'R': "ደ"}

POS_RE = re.compile(r'.*[,\[]pos=(\w+?)[,\]].*')

FINAL_PUNC_RE = re.compile(r'(\w)([።፡፣!])')

VC2FEATS = {
    'base_ብ': '', 'pass_ብ': 'v=p', 'caus1_ድ': 'v=a', 'pass_ድ': 'v=p', 'caus2_ስ': 'v=as', 'pass_ስ': 'v=p',
    'base': '', 'pass': 'v=p', 'caus1': 'v=a', 'caus2': 'v=as', 'caus': 'v=a',
    'iter': 'a=i', 'rcp1': 'a=a,v=p', 'rcp2': 'a=i,v=p', 'csrcp1': 'a=a,v=a', 'csrcp2': 'a=i,v=a'
    }

VC2FEATS_L1 = {
    'base': '', 'pass': 'v=p', 'caus1': 'v=ast', 'caus2': 'v=as',
    'iter': 'a=i', 'rcp2': 'a=i,v=p', 'csrcp2': 'a=i,v=ast'
    }

VC2FEATS_L = {
    'pass': 'v=test', 'caus1': 'v=ast', 'csrcp2': 'a=i,v=a'
    }

TI_VFEATS = ['c', 'root', 'sp', 'sn', 'sg', 'v', 'a', 't', 'cons', 'tmp', 'base']

### Amharic and Tigrinya roots and voice again
### Finding roots with no simplex form

def rewrite_tvroots(defective):
    with open("hm/languages/t/lex/vroot.lex", encoding='utf8') as infile:
        with open("tvroot.lex", 'w', encoding='utf8') as outfile:
            for line in infile:
                line = line.strip()
                if not line:
                    print(line, file=outfile)
                    continue
                if line[0] == "<":
                    # root line; it's here where we add the base feature
                    if "base=" in line:
                        # feature already added
                        print(line, file=outfile)
                    else:
                        root = re.match(r"<(.+)>", line).groups(0)[0]
                        cls = line.split()[-1].strip().replace('c=', '')
                        root = root.replace(' ', '')
                        if cls in ["G", "H", "J"]:
                            print("{},base=p".format(line), file=outfile)
                        elif (root, cls) in defective:
#                            print("{} : {} is in defective list".format(root, cls))
                            print("{},base={}".format(line, defective[(root, cls)]), file=outfile)
                        else:
                            print("{},base=0".format(line), file=outfile)
                else:
                    # other line; just print it
                    print("  " + line, file=outfile)

def get_ti_vroots():
    result = []
    with open("hm/languages/t/lex/vroot.lex", encoding='utf8') as file:
        contents = file.read().strip()
        lines = [l for l in contents.splitlines() if l.strip() and '#' not in l]
        ln = len(lines)
        for i in range(0, ln, 2):
            if i >= ln:
                break
            result.append((lines[i].strip(), lines[i+1].strip()))
    return result

def rewrite_avroots(defective):
    with open("hm/languages/a/lex/vroot.lex", encoding='utf8') as infile:
        with open("avroot.lex", 'w', encoding='utf8') as outfile:
            for line in infile:
                line = line.strip()
                if not line:
                    print(line, file=outfile)
                    continue
                if line[0] == "<":
                    # root line; it's here where we add the base feature
                    if "base=" in line:
                        # feature already added
                        print(line, file=outfile)
                    else:
                        root = re.match(r"<(.+)>", line).groups(0)[0]
                        cls = line.split()[-1].strip().replace('c=', '')
                        root = root.replace(' ', '')
                        if cls in ["G", "H", "J"]:
                            print("{},base=p".format(line), file=outfile)
                        elif (root, cls) in defective:
#                            print("{} : {} is in defective list".format(root, cls))
                            print("{},base={}".format(line, defective[(root, cls)]), file=outfile)
                        else:
                            print("{},base=0".format(line), file=outfile)
                else:
                    # other line; just print it
                    print(line, file=outfile)

def get_am_vroots():
    result = []
    with open("hm/languages/a/lex/vroot.lex", encoding='utf8') as file:
        contents = file.read().strip()
        lines = [l for l in contents.splitlines() if l.strip() and '#' not in l]
        ln = len(lines)
        for i in range(0, ln, 2):
            if i >= ln:
                break
            result.append((lines[i].strip(), lines[i+1].strip()))
    return result

def interactive_assign(u, assigned=None):
    '''
    Unassigned is a list of (root, class, voice) triples.
    '''
    assigned = assigned or {}
    unassigned = {}
    for root, cls, voice in u:
        voice = {x.replace('v=', '') for x in voice}
        assignment = input("Assign {} ({}) {} to P or A?\n>>> ".format(root, cls, voice))
        if assignment.lower() == 'p':
            assigned[(root, cls)] = 'p'
        elif assignment.lower() == 'a':
            assigned[(root, cls)] = 'a'
#        elif assignment.lower() == 'as':
#            assigned[(root, cls)] = 'as'
        else:
            unassigned[(root, cls)] = voice
    return assigned, unassigned

def group_no_base(rootfeats):
    '''
    Each rootfeats consist of root, cls, [a=0_feats, a=a_feats]
    '''
    assigned = {}
    unassigned = []
#    errors = []
#    {'a': [], 'p': [], 'as': [], 2: [], 3: []}
    for root, cls, (a0, aa) in rootfeats:
#        if not a0:
#            errors.append((root, cls))
        if len(a0) == 1:
            if 'v=p' in a0:
                assigned[(root, cls)] = 'p'
            elif 'v=a' in a0:
                assigned[(root, cls)] = 'a'
            else:
                assigned[(root, cls)] = 'as'
        else:
            unassigned.append((root, cls, a0))
    return assigned, unassigned

def all_group_amv_feats(entries):
    normal = []
    no_base = []
#    cc = []
    for entry in entries:
        if r := group_amv_feats(entry):
            if 'v=0' in r[2][0] or 'base' in r[1]:
                normal.append(r)
            else:
                no_base.append(r)
    return normal, no_base

def group_amv_feats(entry, skip_class=['G', 'H', 'I', 'J']):
    """
    entry is two lines from v.root.
    The first line is <root>\tc=*
    The second line is a ;-separated list of combinations of values of a and v
       <ህ ል ቅ>		c=A
       a=0,v=0 ; a=0,v=a
    Returns root, class, [{a=0_aimads}, {a=a_aimads}]
    """
    line1, line2 = entry
    root = re.match(r"<(.+)>", line1).groups(0)[0]
    cls = line1.split()[-1].strip().replace('c=', '')
    if cls in skip_class:
#        print("Skipping {}".format(root))
        return
    root = root.replace(' ', '')
    feats = [f for f in line2.split(';')]
    a0 = [f.strip().split(',') for f in feats if 'a=0' in f]
    a0 = [[x for x in a if 'v=' in x] for a in a0]
    a0 = set([a[0] for a in a0])
    aa = [f.strip().split(',') for f in feats if 'a=a' in f]
    aa = [[x for x in a if 'v=' in x] for a in aa]
    aa = set([a[0] for a in aa])
#    aa = aa[0] if aa else []
    return root, cls, [a0, aa]

### Tigrinya verb stems

def proc_ti_vroots(tvroots):
    '''
    tvroots is a list of pairs of strings: <r o o t>\tclass,sense,base and voice+aimad pairs
    '''
    result = []
    for line1, line2 in tvroots:
        line1split = line1.split("\t")
        root, cls = line1split[0], line1split[-1]
        root = ''.join(root[1:-1])
        av = line2.split(';')
        av = ["{},{}".format(cls, a.strip()) for a in av]
        av = ';;'.join(av)
        result.append("{}\t{}".format(root, av))
    return result

def get_irr_tstems():
    results = []
    with open("hm/languages/t/fst/v_irr.root", encoding='utf8') as file:
        contents = file.read()
        contents = contents.split('*')[1:]
        for entry in contents:
#            featstems = []
            entry = [e for e in entry.split('\n') if e]
            # first line has root, class, and global features
            #<ብ ህ ል>	c=A,tmp=[2=L],s=1
            split1 = entry[0].split()
            glob_feats = split1[-1]
            root = ''.join(split1[:-1])[1:-1]
            glob_feats = "{},root={}".format(glob_feats, root)
#            print("root {}, feats {}".format(root, feats))
            feats = None
            for line in entry[1:]:
                if line[0] == '#':
                    continue
                if line[0] == '[':
                    feats = line.strip()[1:-1]
                else:
                    stem = ''.join(line.strip().split())
                    results.append((stem, ','.join([feats, glob_feats])))
#                    featstems.append((stem, feats))
                    feats = None
#            results.append([glob_feats, featstems])
    return results

def gen_all_tstems(vsmorph=None):
    results = []
    n = 0
    vsmorph = vsmorph or get_t_vstem_morph()

    with open("data/t_vroots2.txt", encoding='utf8') as  file:
        for line in file:
            if n % 25 == 0:
                print("Generated {}".format(n))
            line = line.strip()
            results.append(gen_tstem(line, vsmorph=vsmorph))
            n += 1
    return results

def gen_tstem(entry, vsmorph= None, to_string=True, split_char='\t'):
    '''
    entry is a line from t_vroots2.txt
    '''
    root, feats = entry.split(split_char)
    if ' ' in root:
        root = root.replace(' ', '')
    feats = feats.split(';;')
    return combine_outputs(vsmorph, root, feats, to_string=to_string)

def gen_from_entry(entry):
    """
    entry is two lines from v.root.
    The first line is <root>\tc=*
    The second line is a ;-separated list of combinations of values of a and v
       <ህ ል ቅ>		c=A
       a=0,v=0 ; a=0,v=a
    """
    line1, line2 = entry
    root = re.match(r"<(.+)>", line1).groups(0)[0]
    cls = line1.split()[-1]
    root = root.replace(' ', '')
    feats = cls.strip()
    featcombs = line2.split(';')
    result = []
    for fc in featcombs:
        fc = "{},{}".format(cls, fc.strip())
        result.append(fc)
    return root, result

#def root2tmp(root):
#    tmp = {1: 'X', 2: 'X', 3: 'X', 4: '0'}
#    for index, c in enumerate(root):
#        if c in ('እ', 'ዕ', 'ህ', 'ሕ'):
#            tmp[index+1] = 'L'
#        elif c == 'ው':
#            tmp[index+1] = 'ው'
#        elif c == 'ይ':
#            tmp[index+1] = 'ይ'

def rootlex2entries():
    result = []
    with open('hm/languages/t/lex/vroot.lex', encoding='utf8') as file:
        contents = file.read().strip()
        lines = contents.splitlines()
        for i in range(0, len(lines), 2):
            result.append((lines[i].strip(), lines[i+1].strip()))
    return result
        
def combine_outputs(vsmorph, root, feats, to_string=True):
    vsmorph = vsmorph or get_t_vstem_morph()
    result = []
    for f in feats:
        for ff in [",+cons,+suf", ",+cons,-suf", ",-cons,+suf"]:
            fff = "[" + f + ff + "]"
            output = vsmorph.gen_all(root, feats=fff, save_feats=TI_VFEATS)
            result.extend(output)
    grouped = {}
    for form, fss in result:
#        print("{}  {}".format(form, fss.__repr__()))
        if form in grouped:
            grouped[form] = grouped[form].union(fss)
        else:
            grouped[form] = fss
    if to_string:
        strings = []
        for form, feats in grouped.items():
            strings.append("{}\t{}".format(form, format_FSS(feats)))
        return '\n'.join(strings)
    return grouped

def read_tvstems():
    stems = []
    with open("hm/languages/t/lex/v_stem.lex", encoding='utf8') as file:
        stem = ''
        feats = []
        for line in file:
            if not line.strip():
                continue
            if line[0] != '\t':
                # add previous stem, except for first time
                if stem:
                    stems.append([stem, [FS(f, freeze=True) for f in feats]])
                feats = []
                stem, feat = line.strip().split()
                feats.extend([f for f in feat.split(';') if f])
            else:
                feats.extend([f for f in line.strip().split(';') if f])
        # last stem
        stems.append([stem, [FS(f, freeze=True) for f in feats]])

    return stems

def prune_tvstems(stemlist):
    pruned = 0
    for stem, featlist in stemlist:
        flen = len(featlist)
        compare_FS_list(featlist, 'cons')
        compare_FS_list(featlist, 'suf')
        newflen = len(featlist)
        pruned += flen - newflen
    return pruned

def write_tvstems(stemlist):
    with open("hm/languages/t/lex/v_stem.lex", 'w', encoding='utf8') as file:
        for stem, featlist in stemlist:
            print("{}\t{}".format(stem, format_FSS(featlist, True)), file=file)

def format_FSS(fss, islist=False):
    '''
    Format FSS or FS list in file.
    '''
    if not islist:
        string = fss.__repr__()
        strings = string.split(';')
    else:
        strings = [f.__repr__() for f in fss]
    groups = []
    for i in range(len(strings)+1//2):
        item = strings[2*i:2*i+2]
        if item:
            groups.append(';'.join(item))
    return ';\n\t'.join(groups)

def compare_FS_list(fs, exclude):
    to_del = []
    to_add = []
    for i1, fs1 in enumerate(fs[:-1]):
#        print("Comparing {} ({})".format(fs1.__repr__(), i1))
        for fs2 in fs[i1+1:]:
#            print("Comparing {} and {}".format(fs1.__repr__(), fs2.__repr__()))
            if compare_FS(fs1, fs2, exclude):
                to_add.append(fs2.delete([exclude]))
                to_del.extend([fs1, fs2])
    fs.extend(to_add)
    for d in to_del:
        fs.remove(d)
    return fs

def compare_FS(f1, f2, exclude):
    '''
    Are f1 and f2 equal except for their value on feature exclude?
    '''
    f1x = f1.delete([exclude])
    f2x = f2.delete([exclude])
    return f1x.equal_values(f2x)

def simplify_feats(formfeats):
    '''
    For a single asp/voice combination, simplify the features.
    '''
    # Check t=c
#    result = {}
    allindict = {'i': [], 'p': [], 'j': [], 'c': []}
    noneindict = {'i': [], 'p': [], 'j': [], 'c': []}
    for form, feats in formfeats.items():
#        print("{}".format(form))
        for tense in ['i', 'p', 'j', 'c']:
            allin = True
            nonein = True
            for feat in feats:
                t = feat.get('t')
#                print("  {}".format(feat.__repr__()))
                if t != tense:
                    allin = False
                elif t == tense:
                    nonein = False
            if allin:
                allindict[tense].append(form)
            if nonein:
                noneindict[tense].append(form)
    # delete cons, suf, sp, sn, and sg
    results = []
    for tense in ['i', 'p', 'j', 'c']:
        allin = allindict.get(tense)
        if len(allin) == 1 and len(noneindict.get(tense)) == len(formfeats) - 1:
            ff = formfeats[allin[0]]
            feats = ff.delete(['cons', 'suf', 'sp', 'sn', 'sg'])
            formfeats[allin[0]] = feats
#            results.append((ff[0], feats))
#        result[form] =  feats
#    return result
    return allindict, noneindict

def get_t_vstem_morph():
    return hm.morpho.get_language('t').morphology['v_stem']

def get_t_vforms(root, featsets, vsmorph=None):
    vsmorph = vsmorph or get_t_vstem_morph()
    results = []
    for featset in featsets:
        output = vsmorph.gen_all(root, feats=featset, save_feats=TI_VFEATS)
        results.extend(output)
    return results

### Amharic root/stem frequencies

AM_V_FEATS = ['PASS', 'RECP1', 'RECP2', 'ITER', 'CAUS+RECP1', 'CAUS+RECP2', 'TR', 'CAUS']

MERGE_ROOTS = {'ንብብ:B': 'ንብብ:A'}

def split_o_verbs():
    simple = []
    derived = []
    with open("languages/o/lex/v_stems.lex", encoding='utf8') as file:
        for stem in file:
            stem = stem.strip()
            if stem.endswith("am"):
                # passive
                derived.append(stem)
            elif stem.endswith('adh') and len(stem) > 6:
                # auto-benefactive
                derived.append(stem)
            elif stem.endswith("siis") or stem.endswith("sis") or stem.endswith('chis') or stem.endswith('chiis'):
                # causative
                derived.append(stem)
            else:
                simple.append(stem)
    return simple, derived

def get_as_nouns():
    nouns = []
    directory = "hm/ext_data/ከአብነት/Nouns"
    files = os.listdir(directory)
    for file in files:
        if file.endswith('mpd.txt'):
            with open("{}/{}".format(directory, file), encoding='utf8') as inf:
                for line in inf:
                    line = line.split('\t')
                    token = line[1]
                    if token not in nouns:
                        nouns.append(token)
    nouns.sort()
    with open("hm/ext_data/ከአብነት/n_mwe.txt", 'w', encoding='utf8') as outf:
        for noun in nouns:
            print(noun, file=outf)
    return nouns

def kane_mwes():
    with open("../../../../Projects/LingData/Ti/Kane/n_mwe.txt", encoding='utf8') as inf:
        with open("../../../../Projects/LingData/Ti/Kane/n_mwe2.txt", 'w', encoding='utf8') as outf:
            for line in inf:
                line = line.strip()
                if '#' not in line and ';' not in line:
                    if line[0] in 'aeEiouI':
                        line = "'" + line
                    line = line.replace(" a", " 'a")
                    line = morpho.geez.geezify(line, 'ti', double2gem=True)
                print(line, file=outf)

#def root_freq(infile="data/am_classes.txt", outfile="data/am_freqs.txt"):
#    with open(infile, encoding='utf8') as file:
#    return

def count_unal(path="../../TAFS/datasets/CACO/CACO.txt", n=80000):
    unal = morpho.get_language('a', v5=True).morphology.words1
    count = 0
    counts = {}
    with open(path, encoding='utf8') as file:
        for line in file:
            if count >= n:
                break
            if not line.strip():
                continue
            words = line.split()
            for word in words:
                if word in unal:
                    if word not in counts:
                        counts[word] = 0
                    counts[word] += 1
            count += 1
    return counts

def get_classes(path="data/am_classes.txt", include_ambig=False, write="data/am_freq.txt"):
    amb = {}
    unamb = {}
    mwe = {}
    with open(path, encoding='utf8') as file:
        contents = file.read().split('\n##\n')
        # index, word, anals triples
        for item in contents:
#            print("ITEM\n{}".format(item))
            lines = item.split("\n")
            if len(lines) == 1:
                # Empty sentence
                continue
            sentence = lines[0]
#            print(sentence)
            for line in lines[1:]:
                line = eval(line)
                index, word, anals = line
                if ' ' in word:
                    # MWE
                    word = normalize(word)
                    if word not in mwe:
                        mwe[word] = 0
                    mwe[word] += 1
                    continue
                if not is_geez(word):
                    continue
                if anals:
                    if len(anals) == 1:
                        anal = simplify_anals(word, anals)[0]
                        cls = anal2class(anal)
#                        if cls == "አበበ":
#                            print("Found instance of አበበ")
                        if not cls:
#                            print("No lemma for {}".format(word))
                            # Abbreviations don't have lemmas; ignore them
                            continue
#                        print("&& word {} class {}".format(word, cls))
                        if cls not in unamb:
                            unamb[cls] = 0
#                        if word not in unamb:
#                            unamb[word] = []
#                        unamb[word].append(anal)
                        unamb[cls] += 1
                    else:
                        anals = simplify_anals(word, anals)
                        if len(anals) == 1:
                            anal = anals[0]
                            cls = anal2class(anal)
                            if not cls:
                                continue
                            if cls not in unamb:
                                unamb[cls] = 0
                            unamb[cls] += 1
#                            if word not in unamb:
#                                unamb[word] = []
#                            unamb[word].append(anal)
                        elif include_ambig:
                            if word not in amb:
                                amb[word] = []
                            amb[word].append(anals)
    if write:
        unamb = list(unamb.items())
        unamb.sort()
        with open(write, 'w', encoding='utf8') as file:
            for root, freq in unamb:
                print("{}\t{}".format(root, freq), file=file)
    return unamb, amb, mwe

def anal2class(anal):
    if anal['pos'] == 'V':
        return "{}:{}".format(anal['root'], anal['um'])
    else:
        lemma = anal.get('lemma', '')
        if lemma and not is_geez(lemma):
            return ''
        return lemma

def simplify_anals(word, anals):
    result = []
    for anal in anals:
        simplify_root(anal)
        u = anal.get('um')
        a = {}
        u_ = u
        if not u:
            if anal not in result:
                result.append(anal)
        elif anal['pos'] == 'V':
            u_ = simplify_v_um(u)
            a['um'] = u_
            a['root'] = anal['root']
            a['pos'] = 'V'
        else:
            lemma = anal['lemma']
            a['lemma'] = lemma
            a['pos'] = 'N'
        if a not in result:
            result.append(a)
    return result

def simplify_root(anal):
    if anal.get('pos') != 'V':
        return
    root = anal.get('root')
    if root and root in MERGE_ROOTS:
        anal['root'] = MERGE_ROOTS[root]

def simplify_n_um(um):
    return ''

def simplify_v_um(um, incl=AM_V_FEATS, elim=['TOP', 'NEG', '3', '2', '1', 'SG', 'MASC', 'FEM', 'PL', 'DEF', 'AC3SM'], combine=True, verbose=False):
    um = um.split(';')
    if incl:
        um_ = [u for u in um if u in incl]
    else:
        um_ = []
        for u in um:
            if u not in elim:
                um_.append(u)
        um_.sort()
    if combine:
        um_ = ';'.join(um_)
    return um_

### Older versions

def group_vroots(path="data/am_v_classes.txt", language='a', prune=True, scale_vc=False, sep_png=True):
    ignore = []

    def simplify_um(um, verbose=False):
        # exclude all but information about subject agreement, object agreement, and voice
        um = um.split(';')
        um_ = []
        for u in um:
            if u in ["1", "2", "3", "MASC", "FEM", "SG", "PL",
                     "TR", "CAUS", "PASS", "ITER", "RECP", "CAUS+RECP", "RECP1", "CAUS+RECP1", "RECP2", "CAUS+RECP2",
                     "AC1S", "AC2SM", "AC2SF", "AC3SM", "AC3SF", "AC1P", "AC2P", "AC3P", "{AC3SM/DEF}",
                     # Tigrinya
                     "AC2PM", "AC2PF", "AC3PM", "AC3PF"
                    ]:
                um_.append(u)
        um_.sort()
        return classify_um(um_, verbose=verbose)

    def classify_val_um(um, sep12=True, verbose=False):
        sb12 = ['1', '2']
        sb3fp = ['PL', 'FEM']
        o = ["AC1S", "AC2SM", "AC2SF", "AC3SM", "AC3SF", "AC1P", "AC2P", "AC3P", "AC2PM", "AC2PF", "AC3PM", "AC3PF"]
        hasobj = any([(u in o) for u in um])
        if sep12:
            if any([(u in sb12) for u in um]):
                if hasobj:
                    return '12+o'
                else:
                    return '12-o'
            elif any([(u in sb3fp) for u in um]):
                if hasobj:
                    return '3fp+o'
                else:
                    return '3fp-o'
            elif hasobj:
                return '3sm+o'
            else:
                return '3sm-o'
        else:
            if any([(u in sb12 or u in sb3fp) for u in um]):
                # sb not 3sm
                if hasobj:
                    # trans
                    return '*+o'
                else:
                    return '+-o'
            elif hasobj:
                return '3sm+o'
            else:
                return '3sm-o'

    def classify_um(um, sep12=False, verbose=False):
        cls = []
        if 'PASS' in um:
            cls.append('pass')
        elif 'CAUS' in um:
            if language == 'a':
                cls.append('caus2')
            else:
                cls.append('caus')
        elif 'TR' in um:
            cls.append('caus1')
        elif 'ITER' in um:
            cls.append('iter')
#        elif 'RECP' in um:
#            cls.append('rcp')
#        elif 'CAUS+RECP' in um:
#            cls.append('csrcp')
        elif 'RECP1' in um:
            cls.append('rcp1')
        elif 'RECP2' in um:
            cls.append('rcp2')
        elif 'CAUS+RECP1' in um:
            cls.append('csrcp1')
        elif 'CAUS+RECP2' in um:
            cls.append('csrcp2')
        else:
            cls.append('base')
        if isinstance(um, str):
            um = um.split(';')
        val = classify_val_um(um, sep12=sep12)
        cls.append(val)
        return tuple(cls)
        
    unamb_roots = {}
    amb_roots = {}
    light_roots = {}
    items, nverbs = get_vclass_data(path)

    # classify roots+vc by whether they have 1 or 2 person subjects
    s12 = set()
    reject_imp = []
    for index, word, anals in items:
        if len(anals) == 1:
            anal = anals[0]
            if 'root' not in anal:
                continue
            root = anal['root']
            um = anal['um']
            sense = anal.get('sense', 0)
            vc = get_vc(um)
            pers = get_subpers(um)
            if pers == '12':
                s12.add((root, vc, sense))
    for index, word, anals in items:
        if len(anals) > 1:
            # ambiguous
            unique_anals = set()
            for anal in anals:
                if 'root' not in anal:
                    continue
                root = anal['root']
                um = anal['um']
                vc = get_vc(um)
                sense = anal.get('sense', 0)
                if (root, vc, sense) in reject_imp:
                    continue
                elif is_imperative(um) and (root, vc, sense) not in s12:
                    reject_imp.append((root, vc, sense))
#                    print("** Rejecting imperative reading of {} ({},{})".format(word, root, vc))
                    continue
                um = simplify_um(um)
                unique_anals.add((root, um))
            if len(unique_anals) > 1:
                # still ambiguous
                tam = []
                for root, um in unique_anals:
                    if " " in word:
                        if ' ' not in root:
                            root = word.split()[0] + ' ' + root
                        add_root_um(light_roots, root, um)
                    else:
                        add_root_um(amb_roots, root, um)
            elif len(unique_anals) == 1:
                unique_anals = list(unique_anals)[0]
                root = unique_anals[0]
                um = unique_anals[1]
                if " " in word:
                    if ' ' not in root:
                        root = word.split()[0] + ' ' + root
                    add_root_um(light_roots, root, um)
                else:
                    add_root_um(unamb_roots, root, um)
        else:
            anal = anals[0]
            if 'root' not in anal:
                continue
            root = anal['root']
            um = simplify_um(anal['um'])
            if ' ' in word:
                if ' ' not in root:
                    root = word.split()[0] + ' ' + root
                add_root_um(light_roots, root, um)
            else:
                add_root_um(unamb_roots, root, um)
    for root, features in unamb_roots.items():
        new_features = {}
        for (voice, trans), count in features.items():
            if voice in new_features:
                new_features[voice][trans] = count
            else:
                new_features[voice] = {trans: count}
        unamb_roots[root] = new_features
    for root, features in light_roots.items():
        new_features = {}
        for (voice, trans), count in features.items():
            if voice in new_features:
                new_features[voice][trans] = count
            else:
                new_features[voice] = {trans: count}
        light_roots[root] = new_features
    print("Found {} verbs".format(nverbs))
    counts = count_voice_classes(unamb_roots, language=language, scale=scale_vc)
    proc_voice_class(unamb_roots, prune=prune)
#        proc_voice_class(amb_roots)
    proc_voice_class(light_roots, prune=prune)
    return unamb_roots, amb_roots, light_roots, counts, s12

def proc_voice_class(dct, limit=10, prune=True, png_thresh=0.06):
    eliminate = 0
    def get_root_total(entry):
        root_total = 0
        vc_del = []
        for vc, trans in entry.items():
            tdel = []
            for tt, ttcount in trans.items():
                if ttcount <= 2:
                    # Eliminate any trans type with fewer than 3 instances
                    tdel.append(tt)
            for tt in tdel:
#                print("** deleting {} from {}".format(tt, trans))
                del trans[tt]
            vc_total = 0
            for tlabel, count in trans.items():
                vc_total += count
            if vc_total < 3 and prune:
                vc_del.append(vc)
                continue
#            else:
#                root_total += vc_total
            tv = [trans.get('3sm+o', 0), trans.get('*+o', 0)]
            iv = [trans.get('3sm-o', 0), trans.get('*-o', 0)]
            tvsum = tv[0] + tv[1]
            if tvsum > 5:
                tvprop = round(tv[1] / tvsum, 3)
                if tvprop < png_thresh:
                    vc_total -= tv[1]
                    trans['t3'] = round(tv[0] / vc_total, 3)
                else:
                    trans['t'] = round(tvsum / vc_total, 3)
#                    trans['t3'] = tvprop
            ivsum = iv[0] + iv[1]
            if ivsum > 5:
                ivprop = round(iv[1] / ivsum, 3)
                if ivprop < png_thresh:
                    vc_total -= iv[1]
                    trans['i3'] = round(iv[0] / vc_total, 3)
                else:
                    trans['i'] = round(ivsum / vc_total, 3)
#                    trans['iv'] = ivprop
            if prune and vc_total < 3:
                vc_del.append(vc)
                vc_total = 0
            else:
                trans['count'] = vc_total
            root_total += vc_total
        if prune:
            for vc in vc_del:
#                print("** pruning {} from {}".format(vc, entry))
                del entry[vc]
        return root_total
    to_del = []
    for root, entry in dct.items():
        root_total = get_root_total(entry)
        if root_total < limit:
            eliminate += 1
            to_del.append(root)
        else:
            entry['count'] = root_total
    if prune:
        for d in to_del:
            del dct[d]

def write_voice_class(dct, language='a', light=False):
    if language == 'a':
        if light:
            path = "../../SemVV/data/am_light_voice.txt"
        else:
            path = "../../SemVV/data/am_voice.txt"
    elif light:
        path = "../../SemVV/data/ti_light_voice.txt"
    else:
        path = "../../SemVV/data/ti_voice.txt"
    ls = list(dct.items())
    ls.sort()
    with open(path, 'w', encoding='utf8') as file:
        for root, classes in ls:
            if len(classes) == 1:
                # only 'count', no transitivity classes
                continue
            count = classes['count']
            print("{} ; {}".format(root, count), file=file)
            classes = list(classes.items())
            classes.sort()
            for voice, trans in classes:
                if voice == 'count':
                    continue
                tcount = trans['count']
                del trans['count']
                trans = list(trans.items())
                trans.sort()
                trans = [t for t in trans if t[0] in ['t', 'i', 't3', 'i3']]
                trans = ["{} ({})".format(x, y) for x, y in trans]
                trans = '\t'.join(trans)
                if trans:
                    print("   {}\t{}\t{}".format(voice, tcount, trans), file=file)

### Cleaning Tigrinya corpora

def fix_ti_corpus(train=True):
    lines = []
    path = "../../TT/data/tlmd_v1.0.0/train.txt" if train else "../../TT/data/tlmd_v1.0.0/valid.txt"
    with open(path, encoding='utf8') as file:
        for line in file:
            line = line.strip()
            # add space before final punc
            line = re.sub(r'(\w)([።፡፣፤!?\]\)])', r"\1 \2", line)
            # add space after preceding punc
            line = re.sub(r'(["\(\[])(\w)', r"\1 \2", line)
            # change አ to ኣ
            if line[0] == 'አ':
                line = 'ኣ' + line[1:]
            line = line.replace(" አ", " ኣ")
            lines.append(line)
    path = "../../TT/data/tlmd_v1.0.0/train1.txt" if train else "../../TT/data/tlmd_v1.0.0/valid1.txt"
    with open(path, 'w', encoding='utf8') as file:
        for line in lines:
            print(line, file=file)
    return lines

### Processing Kane Tigrinya dictionary

def ti_kane_verbs():
    roots = {}
    senses = {}
    def convert_feats(feats):
        match feats:
            case "[v=0]":
                return "a=0,v=0"
            case "[v=t]":
                return "a=0,v=p"
            case "[v=a]":
                return "a=0,v=a"
            case "[v=t_a]":
                return "a=a,v=p"
            case "[v=a_a]":
                return "a=a,v=a"
            case "[v=R]":
                return "a=i,v=0"
            case "[v=t_R]":
                return "a=i,v=p"
            case "[v=a_R]":
                return "a=i,v=a"
    with open("../../../../Projects/LingData/Ti/verbs.txt", encoding='utf8') as file:
        contents = file.read().split('##\n')
        for entry in contents:
            entry = entry.strip()
            lines = entry.split("\n")
            main = lines[0]
            if not main.strip():
                continue
            if len(main.split(';;')) != 3:
                print("** {}".format(main))
            lemma, rootfeats, gloss = main.split(';;')
            root, cls, mainfeats = rootfeats.split(':')
            root = geezify(root.replace('W', 'u'), 'ees')
            mainfeats = convert_feats(mainfeats.strip())
            feats = [mainfeats]
            for line in lines[1:]:
                if not line.strip():
                    continue
                if len(line.split(';;')) != 3:
                    print("** {}".format(line))
                lemma1, feats1, gloss1 = line.split(';;')
                feats1 = convert_feats(feats1.strip())
                feats.append(feats1)
            feats = ' ; '.join(feats)
            sense = 1
            if (root, cls) in senses:
                sense = senses[(root, cls)] + 1
                senses[(root, cls)] += 1
            else:
                senses[(root, cls)] = 1
#                print("** ({}, {}) already in roots".format(root, cls))
#                oldfeats = roots[(root, cls)]
#                if oldfeats == feats:
#                    print("** ({} {}); feats are the same: {}".format(root, cls, feats))
            roots[(root, cls, sense)] = feats
    roots = list(roots.items())
    roots.sort()
    with open("data/t_verbs.txt", 'w', encoding='utf8') as file:
        for (root, cls, sense), feats in roots:
            s = ''
            if senses[(root, cls)] > 1:
                s = ",s={}".format(sense)
            print("<{}>\t\tc={}{}".format(' '.join(list(root)), cls, s), file=file)
            print("  {}".format(feats), file=file)
    return roots, senses

def get_pos(fs):
    match = POS_RE.match(fs)
    if match:
        return match.groups()[0]
    return ''

def change_pos(fs, pos):
    if "pos=" in fs:
        return re.sub(r"(pos=\w+)([,\]])", r'pos={}\2'.format(pos), fs)
    if "[]" in fs:
        return fs[:-1] + "pos={}]".format(pos)
    return fs[:-1] + ",pos={}]".format(pos)

def add_feat(fs, feat):
    if feat in fs:
        return fs
    if '[]' in fs:
        return '[' + feat + ']'
    return fs[:-1] + ",{}]".format(feat)

def kane_lv2lex():
    done = []
    with open("/Users/michael/Projects/LingData/Ti/Kane/cmpd_ted.txt", encoding='utf8') as file:
        entries = file.read().split('###\n')
        print("n entries {}".format(len(entries)))
        for entry in entries[1:]:
            entry = entry.split('\n')[0].strip()
#            if len(entry) > 50:
#                print(entry)
            entry = entry.split(';;')
            e1 = entry[0].strip()
            if e1.count(' ') > 4:
                if 'DB' in e1:
                    e1 = e1.split('DB')[0]
                    done.append(e1.split())
                elif 'CS' in e1:
                    e1 = e1.split('CS')[0]
                    done.append(e1.split())
                elif 'TA' in e1:
                    e1 = e1.split('TA')[0]
                    done.append(e1.split())
                elif '<RE' in e1:
                    e1 = e1.split('<RE')[0]
                    done.append(e1.split())
            else:
                if not entry[-1]:
                    entry = entry[:2]
                if 'TA' in entry[1]:
                    entry[1] = entry[1].split('TA')[0].strip()
                done.append(entry)
    with open("/Users/michael/Projects/LingData/Ti/Kane/cmpd_ted2.txt", 'w', encoding='utf8') as file:
        for item in done:
            if len(item) == 2:
                x = item[0].split()
                y = item[1].split()
                if len(x) == 3:
                    x = ' '.join(x[:2])
                    y = ' '.join(y[:2])
                else:
                    x = x[0]
                    y = y[0]
#                print(x, y)
                print("{} ; {}".format(x, y), file=file)
            elif len(item) == 4:
                print("{} ; {}".format(item[0], item[2]), file=file)
            elif len(item) == 3:
                print("{} ; {} ; {}".format(item[0].split()[0], item[1].split()[0], item[2]), file=file)
            else:
                print("{} {} ; {} {}".format(item[0], item[1], item[3], item[4]), file=file)
#    return done

def kane_lv2lex2():
    results = []
    with open("/Users/michael/Projects/LingData/Ti/Kane/cmpd_ted2.txt", encoding='utf8') as file:
        for line in file:
            line = line.split(' ; ')
            g = line[0]
            r = line[1]
            s = line[2] if len(line) == 3 else 0
            gr = geezify(r, 'ees')
            gr = '//'.join(gr.split())
            results.append((gr, s))
    with open("hm/languages/fidel/t/lex/v_light.lex", 'w', encoding='utf8') as file:
        for g, s in results:
            if s == 0:
                print(g, file=file)
#    return results

def kane_nouns2lex():
    results = []
    with open("/Users/michael/Projects/LingData/Ti/Kane/n_ted10.txt") as file:
        entries = file.read().split('###\n')
        count = 0
        for entry in entries[1:]:
            # ignore the English gloss
            entry = entry.split('\n')[0]
            singulars, plurals = entry.split(';;')
            sgeez = []
            pgeez = []
            singulars = singulars.split(';')
            for singular in singulars:
                if len(singular.split(',')) != 2:
                    print("** singular {}".format(singular))
                sg, sr = singular.split(',')
                sr = post2pregem(sr)
                sgeez.append(geezify(sr, 'ees'))
            if plurals:
                plurals = plurals.split(';')
                for plural in plurals:
                    pg, proman = plural.split(',')
                    proman = post2pregem(proman)
                    pg = geezify(proman, 'ees')
                    pgeez.append(geezify(proman, 'ees'))
#            print("sing {}, plur {}".format(sgeez, pgeez))
            for sing in sgeez:
                results.append("{}\t''\t[-pl]".format(sing))
            for plur in pgeez:
                results.append("{}\t{}\t[+pl]".format(plur, sgeez[0]))

    with open("hm/languages/fidel/t/lex/n_stem.lex", 'w', encoding='utf8') as file:
        for result in results:
            print(result, file=file)
    return results

def kane_adj2lex():
    results = []
    with open("/Users/michael/Projects/LingData/Ti/Kane/a_ted2.txt") as file:
        entries = file.read().split('###\n')
        count = 0
        for entry in entries[1:]:
            entry = entry.split('\n')[0]
            forms = entry.split(';;')
            masc = forms[0].strip()
            zey = False
            if not masc:
                continue
            masc = masc.split(';')
            if len(masc) > 1:
                alt = masc[0]
                dflt = masc[1]
                alt = alt.split(',')[-1]
                dflt = dflt.split(',')[-1]
                alt = geezify(post2pregem(alt), 'ees')
                dflt = geezify(post2pregem(dflt), 'ees')
                masc = [alt, dflt]
                results.append("{}\t{}\t[-pl,pos=ADJ]".format(alt, dflt))
            else:
                masc = masc[0].split(',')[-1]
                masc = geezify(post2pregem(masc), 'ees')
                feats = "-pl,pos=ADJ"
                if masc.startswith("ዘይ") or masc.startswith("ዘ/ይ"):
                    zey = True
                    feats += ",-neg"
                results.append("{}\t''\t[{}]".format(masc, feats))
            fem = ''
            plur = ''
            if len(forms) > 1:
                plur = forms[1].strip()
                if plur:
                    plur = plur.split(';')
#                if len(plur) > 1:
#                    print("** multiple plur: {}".format(plur))
                    p = []
                    for pp in plur:
                        if ',' in pp:
                            p.append(pp.split(',')[-1].strip())
                        elif ' ' in pp:
                            p.append(pp.split()[-1].strip())
                        else:
                            p.append(pp.strip())
                    plur = [geezify(post2pregem(pp), 'ees') for pp in p]
                    feats = "+pl,pos=ADJ"
                    if zey:
                        feats += ",-neg"
                    for p in plur:
                        results.append("{}\t{}\t[{}]".format(p, masc, feats))
            if len(forms) == 3:
                # there's a feminine form
                fem = forms[2].strip()
                if ' ' in fem:
                    fem = fem.split()[-1].strip()
                fem = geezify(post2pregem(fem), 'ees')
                results.append("{}\t''\t[+fem,-pl,pos=ADJ]".format(fem))
    return results

### Conversion of romanized lexicons to fidel.

def ti_nouns2fidel():
    lines = []
    with open("hm/languages/tir/lex/n_stem.lex") as file:
        for line in file:
            form1, x, fs = line.split()
            # form2 could have post-gemination character '_'; convert to pre-gemination '/'
            form1 = post2pregem(form1)
            form2 = geezify(form1, 'ees')
#            pos = get_pos(fs) or 'n'
            fs = fs.replace('plr', 'pl')
#            new_fs = "[mwe=[+hdfin,-hdaff,deppos=adj],pos=N]".format(pos)
            lines.append("{}  ''  {}".format(form2, fs))
    with open("hm/languages/fidel/t/lex/n_stem.lex", 'w', encoding='utf8') as file:
        for line in lines:
            print(line, file=file)
#    return lines

def mwe_nouns2fidel():
    lines = []
    with open("hm/languages/amh/lex/n_stemMX.lex") as file:
        for line in file:
            form1, x, fs = line.split()
            # form2 could have post-gemination character '_'; convert to pre-gemination '/'
            form2 = post2pregem(form1)
            pos = get_pos(fs) or 'n'
            new_fs = "[mwe=[+hdfin,-hdaff,deppos=adj],pos={}]".format(pos)
            lines.append("{}  ''  {}".format(geezify(form2), new_fs))
    with open("hm/languages/fidel/a/lex/n_stemM.lex", 'w', encoding='utf8') as file:
        for line in lines:
            print(line, file=file)
    return lines

def words2fidel(mwe=False):
    lines = []
    if mwe:
        f = "hm/languages/amh/lex/wordsM.lex"
    else:
        f = "hm/languages/amh/lex/words1.lex"
    with open(f) as file:
        for line in file:
            if line[0] == '#':
                continue
            line = line.strip()
            form1, form2, pos = line.split()
            form2 = post2pregem(form2)
            # form2 could have post-gemination character '_'; convert to pre-gemination '/'
            lines.append("{}  {}  {}".format(geezify(form1), geezify(form2), pos))
    with open("new_words.lex", 'w', encoding='utf8') as file:
        for line in lines:
            print(line, file=file)
    return lines

### Miscellaneous 

def change_nlex_pos(stems, pos, roman=True):
    lines = []
    changed = []
    with open("hm/languages/fidel/a/lex/n_stem.lex", encoding='utf8') as file:
        for line in file:
            line = line.strip()
            stem = line.split()[0]
            if roman:
                stem = romanize(stem)
                stem = stem.replace("_", "")
            if stem in stems:
                changed.append(stem)
                line = change_pos(line, pos)
            lines.append(line)
    print("Changed {}".format(changed))
    with open("changed.lex", 'w', encoding='utf8') as file:
        for line in lines:
            print(line, file=file)

def n_pos(pos, degem=True):
    res = []
    with open("hm/languages/amh/lex/n_stem1X.lex") as file:
        for line in file:
            p = get_pos(line)
            if p == pos:
                stem = line.split()[0]
                if degem:
                    stem = stem.replace("_", "")
                res.append(stem)
    return res

def post2pregem(string):
    '''
    Move and convert post-gemination character _ to pre-gemination character /.
    '''
    chars = ''
    string = string.replace("W_", "_W")
    for index, char in enumerate(string[:-1]):
        if string[index+1] == '_':
            chars += '/' + char
        elif char != '_':
            chars += char
    if string[-1] != '_':
        chars += string[-1]
    return chars

def degem_clean_nouns(fidel=True, f="new_n.lex"):
    if not f:
        f = "hm/languages/fidel/a/lex/n_stem.lex" if fidel else "hm/languages/amh/lex/n_stem1X.lex"
    wf = "new_degem_n.lex"
    lines = {}
    lines0 = {}
    dups = []
    with open(f, encoding='utf8') as file:
        for line in file:
            line = line.strip()
            line_split = line.split()
            stem = line_split[0]
            stem0 = stem.replace("_", "")
            if stem != stem0:
                # stem has gemination character
                if stem in lines or stem0 in lines:
                    lines0[stem0] = line
                    dups.append(stem)
                else:
                    lines[stem] = line
            else:
                lines[stem] = line
    return dups
    
def clean_nouns(fidel=True):
    f = "hm/languages/fidel/a/lex/n_stem.lex" if fidel else "hm/languages/amh/lex/n_stem1X.lex"
    wf = "new_n.lex"
    lines = {}
    dups = []
    with open(f, encoding='utf8') as file:
        for line in file:
            line = line.strip()
            line_split = line.split()
            stem = line_split[0]
            if stem in lines:
                stemline = lines[stem]
                if len(line) > len(stemline):
                    lines[stem] = line
                dups.append(stem)
            else:
                lines[stem] = line
    with open(wf, 'w', encoding='utf8') as file:
        for line in lines.values():
            print(line, file=file)
    return dups

def sort_nouns(return_class=False, write=True):
    res = {}
    stems = []
    lines = {}
    with open(file="hm/languages/fidel/a/lex/n_stem.lex", encoding='utf8') as file:
        for line in file:
            line = line.strip()
            tokens = line.split()
            stem = tokens[0]
            rest = ' '.join(tokens[1:]).strip()
            res = class_nstem(stem, res=res, return_class=return_class)
            if return_class:
                # POS, other features
                if res in ("Na", "am"):
                    rest = change_pos(rest, 'nadj')
                elif res in ("ins", "net"):
                    rest = change_pos(rest, 'n')
                    rest = add_feat(rest, "-fem")
                elif res == 'eaa':
                    rest = change_pos(rest, 'adj')
                # stem changes
                if res == 'net':
                    if not stem.endswith("ነ_ት"):
                        stem = stem[:-2] + "ነ_ት"
                elif res == 'eaa':
                    if not stem.endswith("_"):
                        stem = stem + '_'
                elif res == 'Na':
                    if not stem.endswith("_"):
                        stem = stem + '_'
                lines[stem] = rest
            else:
                stems.append(stem)
    if write:
        with open("new_nstem.lex", 'w', encoding='utf8') as file:
            for stem, rest in lines.items():
                print("{}\t{}".format(stem, rest), file=file)
    if return_class:
        return lines
    return res

def class_nstem(stem, res=None, return_class=False):
    def dup(form, pos1):
        return len(form) > pos1+2 and form[pos1] == form[pos1+2] and form[pos1+1] == 'a'
    res = res or \
      {'am': [],
       'ma': [],
       'Na': [],
       'net': [],
       'Iu': [],
       'eaa': [],
       'ins': [],
       'agt': [],
       'man': [],
       'check': [],
       'misc': []
      }
    stem0 = stem.replace("_", '')
    rom = romanize(stem0)
    if len(rom) >= 4 and rom[-1] == 'i' and rom[-3] == 'a':
        if return_class:
            return 'agt'
        res['agt'].append(stem)
    elif len(rom) >= 3 and rom[-1] in "cCjxZNy" and rom[-2] == 'a':
        if return_class:
            return 'agt'
        res['agt'].append(stem)
    elif len(rom) >= 4 and rom[-1] == 'i' and rom[-3] == 'e':
        if return_class:
            return 'check'
        res['check'].append(stem)
    elif len(rom) >= 3 and rom[-1] in "cCjxZNy" and rom[-2] == 'e':
        if return_class:
            return 'check'
        res['check'].append(stem)
    elif rom.startswith("'a") and (dup(rom, 2) or dup(rom, 3) or dup(rom, 4) or dup(rom, 5) or dup(rom, 6)):
        if return_class:
            return 'man'
        res['man'].append(stem)
    elif len(rom) == 7 and rom[1] == 'e' and rom[4] == 'a' and rom[6] == 'a':
        if return_class:
            return 'eaa'
        res['eaa'].append(stem)
    elif rom.endswith('am') and len(rom) >= 5:
        if return_class:
            return 'am'
        res['am'].append(stem)
    elif rom.endswith('ma') and len(rom) >= 5:
        if return_class:
            return 'ma'
        res['ma'].append(stem)
    elif rom.endswith('net') and len(rom) >= 6:
        if return_class:
            return 'net'
        res['net'].append(stem)
    elif rom.endswith('Na') and len(rom) >= 6:
        if return_class:
            return "Na"
        res['Na'].append(stem)
    elif (len(rom) == 3 or len(rom) == 4) and rom[1] in CONS and rom[2] == 'u':
        if return_class:
            return "Iu"
        res['Iu'].append(stem)
    elif stem[0] in 'መማ' and stem[-1] == 'ያ':
        if return_class:
            return 'ins'
        res['ins'].append(stem)
    else:
        if return_class:
            return 'misc'
        res['misc'].append(stem)
    return res

def geezify_light(file="hm/languages/amh/lex/v_light.lex"):
    results = []
    with open(file) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            word = geezify(line, gemination=True, gem_geez='_')
            index = 0
            w = ''
            while index < len(word):
                c = word[index]
                if index < len(word) - 1 and word[index+1] == '_':
                    w += "/" + c
                    index += 2
                else:
                    w += c
                    index += 1
            results.append(w)
    with open("light.lex", 'w', encoding='utf8') as f:
        for word in results:
            print(word, file=f)

def check_awi(file1="n_stem_an.lex", file2="n_stem1X.lex"):
    words1 = []
    words2 = []
    with open("hm/languages/amh/lex/" + file1) as f1:
        for line in f1:
            if line[0] == '#' or not line.strip():
                continue
            word = line.split()[0]
            if word.endswith("awi"):
                word = word.replace('_', '')
                words1.append(word)
    with open("hm/languages/amh/lex/" + file2) as f2:
        for line in f2:
            if line[0] == '#' or not line.strip():
                continue
            word = line.split()[0]
            word = word.replace('_', '')
            if word.endswith("awi") and word not in words1:
                word = geezify(word)
                words2.append(word)
    return words2

def geezify_lex(filename="n_stemX.lex", write=True, word_only=True):
    lines = []
    with open("hm/languages/amh/lex/" + filename, encoding='utf8') as file:
        for line in file:
            if line[0] == '#' or not line.strip():
                continue
            line = line.split()
            if len(line) < 3:
                print("** Something wrong with {}".format(line))
            word = line[0]
            word = geezify(word, gemination=True, gem_geez="_")
            root = line[1]
            if root != "''" and not word_only:
                root = geezify(root, gemination=True, gem_geez="_")
            if word_only:
                lines.append(word)
            else:
                lines.append("{} {} {}".format(word, root, ' '.join(line[2:])))
    if write:
        with open("hm/languages/fidel/a/lex/" + filename, 'w', encoding='utf8') as file:
            for line in lines:
                print(line, file=file)
    else:
        return lines

def fix_nadj():
    '''
    Chnange NADJ to N or ADJ for words in n_stemX.lex.
    '''
    lines = []
    adj = []
    n = []
    with open(OS.path.join(OS.path.join(OS.path.dirname(__file__), 'languages', 'amh', 'lex', 'n_stem_old.lex'))) as old:
        for line in old:
            root, x, rest = line.partition(' ')
            x, y, feats = rest.partition(' ')
            feats = FS(feats)
            pos = feats.get('pos')
            if pos == 'n':
                n.append(root)
            elif pos == 'adj':
                adj.append(root)
    with open(OS.path.join(OS.path.join(OS.path.dirname(__file__), 'languages', 'amh', 'lex', 'n_stem1X.lex'))) as file:
        for line in file:
            line = line.strip()
            if line.count('\t') != 2:
                stem, x, rest = line.partition(' ')
                root, y, feats = rest.partition(' ')
            else:
                stem, root, feats = line.split('\t')
            feats = FS(feats)
            if feats.get('pos') == 'nadj':
                if stem in n or root in n:
                    feats['pos'] = 'n'
                elif stem in adj or root in adj:
                    feats['pos'] = 'adj'
            lines.append("{}\t{}\t{}".format(stem, root, feats.__repr__()))
    with open(OS.path.join(OS.path.join(OS.path.dirname(__file__), 'languages', 'amh', 'lex', 'n_stem_newX.lex')), 'w') as file:
        for line in lines:
            print(line, file=file)

def mwe_2_3(n=True):
    w2 = []
    w3 = []
    inp = 'n_stemMX.lex' if n else 'v_light.lex'
    out2 = 'n_stem2X.lex' if n else 'v_light1.lex'
    out3 = 'n_stem3x.lex' if n else 'v_light2.lex'
    with open(OS.path.join(OS.path.join(OS.path.dirname(__file__), 'languages', 'amh', 'lex', inp))) as file:
        for line in file:
            line = line.strip()
            if '\t' not in line:
                alt, x, rest = line.partition(' ')
                root, x, rest = rest.partition(' ')
                line = "{}\t{}\t{}".format(alt, root, rest)
            nword = line.count('//') + 1
            if not n:
                nword += 1
            if nword == 2:
                w2.append(line)
            else:
                w3.append(line)
    with open(OS.path.join(OS.path.join(OS.path.dirname(__file__), 'languages', 'amh', 'lex', out2)), 'w') as file:
        for line in w2:
            print(line, file=file)
    with open(OS.path.join(OS.path.join(OS.path.dirname(__file__), 'languages', 'amh', 'lex', out3)), 'w') as file:
        for line in w3:
            print(line, file=file)

def sep_mwe_name():
    mwe = []
    simple = []
    with open(OS.path.join(OS.path.join(OS.path.dirname(__file__), 'languages', 'amh', 'lex', 'n_place.lex'))) as file:
        for line in file:
            line = line.strip()
            if '\t' not in line:
                alt, x, rest = line.partition(' ')
                root, x, rest = rest.partition(' ')
                line = "{}\t{}\t{}".format(alt, root, rest)
            if '//' in line:
                mwe.append(line)
            else:
                simple.append(line)
    with open(OS.path.join(OS.path.join(OS.path.dirname(__file__), 'languages', 'amh', 'lex', 'n_place1X.lex')), 'w') as file:
        for line in simple:
            print(line, file=file)
    with open(OS.path.join(OS.path.join(OS.path.dirname(__file__), 'languages', 'amh', 'lex', 'n_placeMX.lex')), 'w') as file:
        for line in mwe:
            print(line, file=file)

def sep_mwe_n():
    mwe = []
    simple = []
    with open(OS.path.join(OS.path.join(OS.path.dirname(__file__), 'languages', 'amh', 'lex', 'n_stemX.lex'))) as file:
        for line in file:
            line = line.strip()
            if '\t' not in line:
                alt, x, rest = line.partition(' ')
                root, x, rest = rest.partition(' ')
                line = "{}\t{}\t{}".format(alt, root, rest)
            if '//' in line:
                mwe.append(line)
            else:
                simple.append(line)
    with open(OS.path.join(OS.path.join(OS.path.dirname(__file__), 'languages', 'amh', 'lex', 'n_stem1X.lex')), 'w') as file:
        for line in simple:
            print(line, file=file)
    with open(OS.path.join(OS.path.join(OS.path.dirname(__file__), 'languages', 'amh', 'lex', 'n_stem_mweX.lex')), 'w') as file:
        for line in mwe:
            print(line, file=file)
#    return simple, mwe

def proc_irr_nplur():
    stems = []
    with open(OS.path.join(OS.path.join(OS.path.dirname(__file__), 'languages', 'amh', 'lex', 'irr_plrX.lex'))) as file:
        for line in file:
            if line[0] == '#' or not line.strip():
                continue
            stem, root, feats = line.strip().split('\t')
            feats = FS(feats)
#            feats = feats.split(';')
#            feats = FSS(*feats)
            stems.append([stem, root, feats])
    for srf in stems:
        stem, root, feats = srf
        srf[1] = stem
        feats['lemma'] = geezify(root)
    with open("irr_nplur.lex", 'w', encoding='utf8') as file:
        for stem, root, feats in stems:
            print("{}\t{}\t{}".format(stem, root, feats.__repr__()), file=file)
#    return stems

def proc3_vroots():
    roots = get_vroots()
    newroots = []
    for root, features in roots:
        cls = features.get('cls')
        if cls == 'G':
            cls = 'K'
        elif cls == 'H':
            cls = 'L'
        elif cls == 'J':
            cls = 'E'
        rootFS = make_FS(cls)
        rootG = VGEN(root, update_feats=rootFS, guess=True)
        if not rootG:
            print("No root for {} : {}".format(root, cls))
            rootG = '?'
        else:
            rootG = geezify(rootG[0][0])
        features = features.unfreeze()
        for f in features:
            f['root'] = rootG
        newfeats = FSS(*features)
        newroots.append("{}\t''\t{}".format(root, newfeats.__repr__()))
    with open("newvroot.txt", 'w') as file:
        for newroot in newroots:
            print(newroot, file=file)

def proc2_vroots():
    roots = get_vroots()
    newroots = []
    for root, features in roots:
        cls = features.get('cls')
        features = features.unfreeze()
        for f in features:
            bs = f['bs']
            lemmaFS = make_FS(cls, bs)
            lemma = VGEN(root, update_feats=lemmaFS)
            if not lemma:
                print("No lemma for {} : {}".format(root, bs))
            else:
                lemma = lemma[0][0]
                f['lemma'] = geezify(lemma)
        newfeats = FSS(*features)
        newroots.append("{}\t''\t{}".format(root, newfeats.__repr__()))
    with open("newvroot.txt", 'w') as file:
        for newroot in newroots:
            print(newroot, file=file)

def proc_vroots():
    roots = get_vroots()
    senses = get_vsenses(True)
    newroots = []
    for root, features in roots:
        rootclass = "{}:{}".format(root, features.get('cls'))
        if rootclass in senses:
            sensefeats = senses[rootclass]
            senseFSS = FSS(*sensefeats)
        else:
            features = features.unfreeze()
            for f in features:
                voice = f.get('vc')
                aspect = f.get('as')
                if aspect == 'it':
                    f['bs'] = 'te_R'
                elif aspect == 'rc':
                    f['bs'] = 'te_a'
                elif voice == 'ps':
                    f['bs'] = 'te_'
                elif voice == 'tr':
                    f['bs'] = 'a_'
                elif voice == 'cs':
                    f['bs'] = 'as_'
                elif f.get('smp', True) == False:
                    f['bs'] = 'te_'
#                    print("Confused about {} : {}".format(root, features.__repr__()))
                else:
                    f['bs'] = '0'
            senseFSS = FSS(*features)
        newroots.append("{}\t''\t{}".format(root, senseFSS.__repr__()))
    with open("newvroot.txt", 'w') as file:
        for newroot in newroots:
            print(newroot, file=file)
#    return newroots

def get_vroots():
    roots = []
    with open(amh_vroot_file()) as file:
        for line in file:
            if line[0] == '#' or not line.strip():
                continue
            root, X, feats = line.strip().split('\t')
            feats = feats.split(';')
            feats = FSS(*feats)
            roots.append((root, feats))
    return roots

def get_vsenses(make_feats=True):
    senses = {}
    with open(amh_vroot_senses(), encoding='utf8') as file:
        for line in file:
            root, rootG, sense, wld, lemma, gloss = line.strip().split('\t')
            if make_feats:
                r, c = root.split(":")
                sense = int(sense)
                feats = FS("[sns={},cls={},bs={},t=[eng='{}'],-lt]".format(sense, c, wld, gloss))
            else:
                feats = (sense, wld, rootG, lemma, gloss)
            if root in senses:
                senses[root].append(feats)
            else:
                senses[root] = [feats]
    return senses

def ssline2code(line):
    '''
    Convert a line from Abnet's spreadsheet to a WP code.
    '''
    codes = []
    for l, a in zip(line, AS_WLD):
        if a:
            # there is a form here.
            if a == '0':
                if l == 'm':
                    codes.append('0')
            elif l:
                codes.append(a)
    return morpho.EES.assign_WPattern(codes)

def proc_v_senses():
    result = []
    with open(amh_vroot_senses()) as file:
        for line in file:
            rootcls, sense, gloss, code, pattern = line.split(";")
            root, cls = rootcls.split(':')
            fs = make_FS(cls)
            rootG = VGEN(root, update_feats=fs, guess=True)
            if not rootG:
                rootG = VGEN(root, update_feats=fs, guess=False)
            rootG = rootG[0][0]
            rootG = geezify(rootG)
#            print(rootG)
            ውልድ = gen_ውልድ(root, code)
            result.append("{}\t{}\t{}\t{}\t{}\t{}".format(rootcls, rootG, sense, code, ውልድ, gloss))
    with open("v_senses.txt", 'w', encoding='utf8') as file:
        for line in result:
            print(line, file=file)

def make_FS(cls, code='', asp='smp', vc='smp'):
    if code and cls:
        if cls in CODECLS2FS[code]:
            return CODECLS2FS[code][cls]
        else:
            fs = FS(CODE2FS[code].format(cls))
            CODECLS2FS[code][cls] = fs
            return fs
#        av = CODE2ASVC[code]
#        asp = av['as']
#        vc = av['vc']
    if not cls:
        return FS("[pos=v,as={},vc={},tm=prf,sb=[-p1,-p2,-plr],pp=None,cj2=None,-rel,-sub]".format(asp, vc))
    return FS("[cls={},pos=v,tm=prf,sb=[-p1,-p2,-plr],pp=None,cj2=None,-rel,-sub]".format(cls))

def gen_ውልድ(root, code):
    fs = make_FS(None, code=code)
    root = VGEN(root, update_feats=fs)
    if not root:
        return []
    return geezify(root[0][0])

def amsalu_vroots():
    roots = {}
    with open("v_amheng.txt") as file:
        for line in file:
            root, feats, gloss = line.split(" || ")
            root = old2new_am_root(root)
            feats = ASVC[feats]
            if root in roots:
                if feats not in roots[root]:
                    roots[root].append(feats)
            else:
                roots[root] = [feats]
    return roots

def get_roots_patterns():
    roots = {}
    missing = []
    with open('root_patterns.txt') as file:
        for line in file:
            root, pattern = line.strip().split('\t')
            pattern = get_root_form_pattern(pattern)
            if root in roots:
                roots[root].append(pattern)
            else:
                roots[root] = [pattern]
    with open(amh_vroot_file()) as file:
        for line in file:
            root = line.partition(' ')[0]
            if root in roots:
                continue
            if root[0] == 'n':
                if root[1:] in roots:
                    pass
#                    print("{} in list with missing n-".format(root))
                else:
                    missing.append(line.strip())
            else:
                missing.append(line.strip())
    missing = [lexline2rootFSS(line) for line in missing]
    missing = [x for x in missing if x]
    missing = [(root, rootclass2Root(root, fss)) for root, fss in missing]
    with open("missing_vroots2.txt", 'w', encoding='utf8') as file:
        for root, (r, lemma) in missing:
            print("{}".format(root), file=file)
    with open("root_patterns2.txt", 'w') as file:
        for root, patterns in roots.items():
            print("{}\t{}".format(root, "\t".join(patterns)), file=file)
    return roots, missing

def lexline2rootFSS(line):
    '''
    Convert a line in v_root.lex to a root and FSSet
    '''
    if '#' in line:
        return None
    line = line.split(' ')
    root = line[0]
    feats = ' '.join(line[2:])
    feats = feats.split(';')
    fss = FSS(*feats)
    return root, fss

def rootclass2Root(root, fss):
    '''
    Generate a lemma-like verb root, e.g., በለጨለጨ, from an HM root and class.
    '''
    # generate real lemma
    cls = fss.get('cls')
    vc = fss.get('vc')
    asp = fss.get('as')
    
    if vc == 'tr':
        if asp == 'rc':
            f = VPOSRT
        else:
            f = VPOST
    elif cls in "GJ" or vc == 'ps' or fss.get('smp') is False:
        if asp == 'rc':
            f = VPOSR
        else:
            f = VPOSP
    elif asp == 'rc':
        f = VPOSR
    else:
        f = VPOS
    l = VGEN(root, update_feats=f)
    if l:
        l = l[0][0]
    else:
        print("Couldn't generate {}:{}".format(root, cls))
    # irregulars
    if root == "b'l":
        return "አለ"
    if root == "tw":
        return "ተወ"
    # delete initial n in classes G and J
    if root[0] == 'n' and cls in 'GHJ':
        root = root[1:]
    chars = ''
    for i, char in enumerate(root):
        if char == 'W':
            if root[i+1] == "'":
                chars += 'W'
            else:
                chars += 'o'
        elif char == '*':
            chars += "e"
        elif char == "'":
            chars += 'a'
        else:
            chars += char
    root = chars
#    root = root.replace("'", "a").replace("W", "o").replace("*", "e")
    if root[1] == 'w' and cls == 'A':
        root = root.replace("w", "o")
    if root[1] == 'y' and cls == 'A':
        if root[0] in "cCjxZ":
            root = root.replace('y', 'e')
        else:
            root = root.replace('y', 'E')
    result = ''
    for i, char in enumerate(root):
        result += char
        if char in CONS:
            # end of root, need -e
            if i == len(root) - 1 or root[i+1] in CONS:
                result += 'e'
    result = geezify(result)
    return result, geezify(l)

def get_root_form_pattern(forms):
    '''
    forms is a list of 
    returns: 
    '''
    s = ''
    for pos in [(0,), (1,), (4,), (7,), (2,5), (3,6), (8,)]:
        x = '0'
        for p in pos:
            if len(forms) > p:
               if forms[p] == '1':
                   x = '1'
                   break
        s += x
    return s
        
    # 0 ደራጊ
    # 1 ተደራጊ
    # 2 አድራጊ
    # 3 አስደራጊ
    # 4 ተዳራጊ አዳራጊ
    # 5 ተደራራጊ አደራራጊ
    # 6 ደራራጊ

def Root2root(Root):
    """
    Convert a 'Root', a lemma-like, Geez representation of a verb root, to an HM root.
    """
    cls = 'A'
    if len(Root) > 4:
        cls = 'G'
    rom = romanize(Root)
    if cls == 'G':
        if rom[1] == 'o':
            if rom[0] in 'mbf':
                rom = rom[0] + 'u' + rom[2:]
            else:
                rom = rom[0] + 'W' + rom[2:]
        else:
            rom = rom[0] + rom[2:]
        rom = 'te' + rom
    anal = A.morphology['v'].anal(rom, guess=False, init_weight=VPOS)
    if not anal:
        anal = A.morphology['v'].anal(rom, guess=True, init_weight=VPOS)
    if not anal:
        print("Couldn't analyze {}".format(Root))
        return
    else:
        return anal[0][0]

def proc_wuld():
    result = []
    roots = {}
    with open(wuld_file(), encoding='utf16') as file:
        file.readline()
        for line in file:
            items = line.strip().split('\t')
            Root = items[1]
            root = Root2root(Root)
            if not root:
                continue
#            if root in roots:
#                print("{} already in roots".format(root))
            pattern = items[3:]
            if root in roots:
                roots[root].append(pattern)
            else:
                roots[root] = [pattern]
            result.append((root, pattern))
#            roots.append(root)
    return roots

def wuld_file():
    return OS.path.join(OS.path.join(OS.path.dirname(__file__), 'ext_data', "ከአብነት", "WuldVerbs"), 'WuldVerbs.txt')

def amh_vroot_file(experimental=True):
    return OS.path.join(OS.path.join(OS.path.dirname(__file__), 'languages', 'amh', 'lex'), ('v_rootX.lex' if experimental else 'v_root.lex'))

def amh_vroot_senses():
    return OS.path.join(OS.path.join(OS.path.dirname(__file__), 'languages', 'amh', 'lex'), 'v_senses.txt')

def filter_amh_vroots():
    roots1 = {}
    roots2 = {}
    with open(amh_vroot_file()) as file:
        for line in file:
            if "t=[e" in line and "=G" not in line and "=H" not in line and "=J" not in line:
                # There has to be a gloss for idioms, and assume there aren't any for G,H,J classes
                if ("-smp" in line or "+lex" in line or "as=r" in line or "as=i" in line or "vc=p" in line or "vc=c" in line or "vc=t" in line):
                    linesplit = line.split()
                    root = linesplit[0]
                    feats = ' '. join(linesplit[2:])
                    feats = feats.split(';')
                    f = []
                    nfeats = len(feats)
                    for feat in feats:
                        for ff in ("-smp", "+lex", "vc=p", "vc=t", "vc=c", "as=r", "as=i"):
                            if ff in feat:
                                f.append(feat)
                                break
#                        if "+lex" not in feat and "-smp" not in feat and "vc=p" not in feat and "vc=t" not in feat and "vc=c" not in feat and "as=r" not in feat):
#                            continue
#                        f.append(feat)
                    if len(f) != nfeats:
                        roots2[root] = f
                    else:
                        roots1[root] = f
    with open("v_except_simp.txt", 'w') as file:
        for root, feats in roots1.items():
            print("{}\t{}".format(root, ';'.join(feats)), file=file)
    with open("v_except_mult.txt", 'w') as file:
        for root, feats in roots2.items():
            print("{}\t{}".format(root, ';'.join(feats)), file=file)
#    return roots1, roots2

def get_old_am_root_stats():
    statfile = OS.path.join(OS.path.join(OS.path.dirname(__file__), 'languages', 'amh', 'stat'), 'root_freqs.dct')
    with open(statfile) as file:
        return eval(file.read())

def old2new_am_roots():
    '''
    Convert old Am verb root/feat strings in root_freqs.dct to new roots.
    Tb_q+smp+smp => Tbq+B+smp+smp
    '''
    # Get the old dct of roots
    oldrootfreq = list(get_old_am_root_stats().items())
    for i, (item, count) in enumerate(oldrootfreq):
        if '+' not in item:
            # noun, adj or unknown
            continue
        # Verb root
        root, vc, asp = item.split('+')
        root, cls = old2new_am_root(root)
        newrf = "{}+{}+{}+{}".format(root, cls, vc, asp)
        oldrootfreq[i] = newrf, count
    return dict(oldrootfreq)

def old2new_am_root(root):
    """Convert old root to (new root, class)."""
    if '|' in root:
        cls = 'G'
        if 'a' in root:
            rootW = root.replace('W', '')
            # cls=H or cls=J
            if len(root) >= 7:
                cls = 'H'
            else:
                cls = 'J'
        elif len(root) < 6:
            cls = 'I'
        root = root.replace('|', '').replace('a', '')
#        feats = add_class_to_feats(feats, cls)
#        result.append("{}  ''  {}".format(root, feats))
    elif '_' in root:
        cls = 'B'
        root = root.replace('_', '')
#        feats = add_class_to_feats(feats, cls)
#        result.append("{}  ''  {}".format(root, feats))
    elif 'a' in root:
        cls = 'C'
        rootW = root.replace('W', '')
        if len(rootW) > 4:
            cls = 'F'
        root = root.replace('a', '')
    else:
        cls = 'A'
        rootW = root.replace('W', '')
        if len(rootW) > 4:
            cls = 'K'
        elif len(rootW) > 3:
            cls = 'E'
    return root, cls

def update_adv():
    '''
    Add new adverbs from AS to Amh unanalyzed words.
    '''
    aa = get_external_roots("ከአብነት", "AllAdverbs.txt", encoding='utf8')
    misc = get_words('amh')
    for word in aa:
        if word not in misc:
            misc[word] = (word, 'adv')
    return misc

def AS_NA(new_noun="nouns.txt", new_adj="adjs.txt"):
    '''
    Process the new roots from Abnet.
    '''
    # nouns and adjectives
    n = get_roots('amh', 'n', ["n_stem.lex", "irr_n.lex"], check_pos=True, degeminate=True)
    a = get_roots('amh', 'adj', ["n_stem.lex", "irr_n.lex"], check_pos=True, degeminate=True)
    N, A, j = get_external_roots2("ከአብነት", "AllNouns.txt", "AllAdjectives.txt")
    rn1, rn2, rj = filter_roots(N, n, external2=j, internal2=a)
    ra1, ra2 = filter_roots(A, a, internal2=n)
    addedwords=rewrite_lex('amh', "n_stem.lex", rn1, rn2, jointroots=rj, pos='n', writeto=new_noun)
    rewrite_lex('amh', None, ra1, ra2, addedwords=addedwords, pos='adj', writeto=new_adj)
#    return (rn1, rn2), (ra1, ra2)

def AS_verbs(new_roots="verbs.txt"):
    ir = get_roots('amh', 'v', ['v_root.lex', 'irr_stem.lex'], get_cls=True)
    v = get_external_verbs("ከአብነት", "AllVerbs.txt", encoding="utf16")
    xr = anal_verbs(v, ir)
    with open(new_roots, 'w') as f:
        for x in xr:
            # x a list of root, class pairs
            for r, c in x:
                print("{} {}".format(r, c), file=f)
            print('##', file=f)
#    return xr

def sep_verb_roots(file='verbs.txt', unam='v_unambig.txt', amb='v_ambig.txt'):
    ambig2=[]
    ambig3=[]
    unambig=[]
    with open(file) as f:
        contents = f.read().split('##')
        for word in contents:
            word = word.strip()
            word = word.split('\n')
            word = set(word)
            if len(word) == 1:
                unambig.append(list(word)[0])
            elif len(word) == 2:
                ambig2.append(word)
            else:
                ambig3.append(word)
    with open(unam, 'w') as out:
        for word in unambig:
            print(word, file=out)
    with open(amb, 'w') as out:
        for word in ambig2:
            word = ' ; '.join(list(word))
            print(word, file=out)
        print("##", file=out)
        for word in ambig3:
            word = ' ; '.join(list(word))
            print(word, file=out)
#    return unambig, ambig2, ambig3

#def filter_unambig():
#    irc = get_roots('amh', 'v', ['v_root.lex', 'irr_stem.lex'], get_cls=True)
#    unamb = []
#    with open('v_unambig.txt') as file:
#        for line in file:
#            line = line.strip()
#            if not line:
#                continue
#            root, x, feats = line.split()
#            cls = feats.split('=')[1].split(',')[0]
#            print("Checking {}".format((root, cls)))
#            if (root, cls) in irc:
#                print("{} {} in roots".format(root, cls))

def choose_classes():
    unamb = []
    amb = []
    with open('v_ambig.txt') as infile:
        for line in infile:
            line = line.split()
            root = line[0]
            cls = choose_class(root)
            if cls:
                unamb.append((root, cls))
            else:
                amb.append(root)
    return unamb, amb

def choose_class(root):
    """
    Check Abyssinica dictionary to see whether A or B infinitives are found,
    selecting one or the other if only one is found.
    """
    print("Checking {}".format(root))
    iA = check_inf(root, 'A')
    iB = check_inf(root, 'B')
    if iA and not iB:
        return 'A'
    elif iB and not iA:
        return 'B'
    return

def gen_inf(root, cls):
    if root[-1] == "'":
        return gen_Linf(root, cls)
    fs = INF[0] if cls=='A' else INF[1]
    form = A.morphology['n'].gen(root, update_feats=fs, guess=True)
    if form:
        return geezify(form[0][0])

def gen_imp(root, cls, fem=False, plur=False):
    if fem:
        fs = IMPFEM[0] if cls=='A' else IMPFEM[1]
    elif plur:
        fs = IMPPL[0] if cls=='A' else IMPPL[1]
    else:
        fs = IMP[0] if cls=='A' else IMP[1]
    form = A.morphology['v'].gen(root, update_feats=fs, guess=True)
    if form:
        return geezify(form[0][0])

def check_imp(root, cls):
    imp = gen_inf(root, cls)
    if not imp:
        return
    try:
        ab = abyss(imp)
        return ab
    except TypeError:
        print("Couldn't check {}".format((root, cls)))
        return

def check_inf(root, cls):
    inf = gen_inf(root, cls)
    if not inf:
        return
    try:
        ab = abyss(inf)
        return ab
    except TypeError:
        print("Couldn't check {}".format((root, cls)))
        return

def search_class(root):
    """
    Do a google search for infinitive or imperative forms
    of root in class A and B, comparing the number of references
    to the word in the results.
    """
    print("Checking {}".format(root))
    if root[0] == "'" or not gen_inf(root, 'A'):
        # root starts with ', so infinitive doesn't distinguish A from B; use imperative
        Aword = search_root_imp(root)
        Awordfem = search_root_imp(root, fem=True)
        Awordplr = search_root_imp(root, plur=True)
        Atotal = Aword + Awordfem + Awordplr
        print("A counts for {}: {}, {}, {}".format(root, Aword, Awordfem, Awordplr))
        Bword = search_root_imp(root, cls='B')
        Bwordfem = search_root_imp(root, fem=True, cls='B')
        Bwordplr = search_root_imp(root, plur=True, cls='B')
        Btotal = Bword + Bwordfem + Bwordplr
        print("B counts for {}: {}, {}, {}".format(root, Bword, Bwordfem, Bwordplr))
        if Atotal > 10 and (Atotal > Btotal * 1.4):
            return 'A'
        elif Btotal > 10 and (Btotal > Atotal * 1.4):
            return 'B'
        else:
            return ''
    Aword = gen_inf(root, 'A')
    Bword = gen_inf(root, 'B')
    if not Bword:
        return ''
    searchA = goog(Aword)
    searchB = goog(Bword)
    if searchA and searchB:
        searchA = searchA.prettify().count(Aword)
        searchB = searchB.prettify().count(Bword)
        print("A count {}, B count {}".format(searchA, searchB))
        if searchA > 5 and (searchA > searchB):
            return 'A'
        elif searchB > 5 and (searchB > searchA * 1.8):
            # B infinitive can also be passive A (መሰበር)
            return 'B'
        else:
            return ''

def search_classes():
    unamb = []
    amb = []
    with open("v_amb2.txt") as file:
        for line in file:
            root = line.strip()
            cls = search_class(root)
            if cls:
                unamb.append((root, cls))
            else:
                amb.append(root)
    return unamb, amb

def search_root(root, cls):
    word = gen_inf(root, cls)
    if not word:
        return search_root_imp(root)
    search = goog(word)
    if search:
        search = search.prettify()
        return search.count(word)
    return 0

def search_root_imp(root, fem=False, plur=False, cls='A'):
    word = gen_imp(root, cls, fem=fem, plur=plur)
    if not word:
        print("No word for {}:{}".format(root, cls))
        return 0
    search = goog(word)
    if search:
        search = search.prettify()
        return search.count(word)
    return 0

def gen_Linf(root, cls):
    if cls=='A':
        rom = "me{}{}at".format(root[0], root[1])
    else:
        rom = "me{}e{}at".format(root[0], root[1])
    return geezify(rom)
        
def rewrite_lex(lang, file, newroots, modroots, addedwords=None, jointroots=None, pos='n', modpos='nadj', writeto=None):
    newfile = []
    newwords = []
    if file:
        ld = lex_dir(lang)
        with open(OS.path.join(ld, file)) as f:
            for line in f:
                line = line.strip()
                contents, x, comment = line.partition('#')
                contents = contents.strip()
                if not contents and comment:
                    newfile.append(line)
                    continue
                if line in newfile:
                    continue
                word, x, rest = contents.partition(' ')
                newwords.append(word)
                if word not in modroots:
                    # No changes to this line
                    newfile.append(line)
                    continue
                # word is in modroots; change POS to modpos
                root, x, feats = rest.partition(' ')
                feats = FSS.parse(feats)
                feats = feats.set_all('pos', modpos)
                newline = "{} {} {}".format(word, root, feats.__repr__())
                newfile.append(newline)
    for root in newroots:
        if addedwords and root in addedwords:
            continue
        newline = "{} '' [pos={}]".format(root, pos)
        newfile.append(newline)
        newwords.append(root)
    if jointroots:
        for root in jointroots:
            if addedwords and root in addedwords:
                continue
            newline = "{} '' [pos={}]".format(root, modpos)
            newfile.append(newline)
            newwords.append(root)
    if writeto:
        with open(writeto, 'w') as f:
            for line in newfile:
                print(line, file=f)
    return newwords

def lex_dir(lang):
    return OS.path.join(OS.path.dirname(__file__), 'languages', lang, 'lex')

def get_ext_data(folder, file):
    return OS.path.join(OS.path.dirname(__file__), 'ext_data', folder, file)

def get_words(lang):
    '''
    Get unanalyzed words for language.
    '''
    words = {}
    lexd = lex_dir(lang)
    with open(OS.path.join(lexd, "words.lex")) as f:
        for line in f:
            word, wordP, pos = line.split()
            if word in words:
                print("{} already in words!".format(word))
                continue
            words[word] = (wordP, pos)
    return words

def get_roots(lang, pos, files, degeminate=False, check_pos=False, trans=False, get_cls=False):
    """Get stems or roots from lex files for lang (a string)."""
    roots = []
    translations = []
    ld = lex_dir(lang)
    for file in files:
        with open(OS.path.join(ld, file)) as f:
            for line in f:
                line = line.strip()
                line = line.split('#')[0].strip()
                if not line:
                    continue
                word, x, rest = line.partition(' ')
                root, x, feats = rest.partition(' ')
                # treat alternate forms as 'roots'
                if len(root) == 2 and root[0] == "'":
                    root = word
                if degeminate:
                    root = root.replace('_', '')
                if root in roots:
                    continue
                feats = FSS.parse(feats)
                if check_pos:
                    pos1 = feats.get('pos')
                    if pos not in pos1:
                        continue
                if get_cls:
                    cls = feats.get('cls')
                    root = root, cls
#                print ("root {}, feats {}".format(root, feats.__repr__()))
                roots.append(root)
                if trans:
                    trans1 = feats.get('t')
                    translations.append(trans1)
    if trans:
        return zip(roots, translations)
    return roots

def get_external_verbs(folder, file, rom=False, sep='\t', ncols=3, rootcol=1, encoding='utf8'):
    verbs = []
    path = get_ext_data(folder, file)
    with open(path, encoding=encoding) as f:
        for line in f:
            line = line.strip()
            splitline = line.split(sep)
            verb = splitline[rootcol]
            if not verb:
                print("No verb in {}".format(line))
                continue
            if verb not in verbs:
                verbs.append(verb)
    return verbs

def anal_novel_verb(verb, ignore):
    """
    Analyze a verb, returning a list of roots and classes if it's novel, otherwise None.
    """
    anals = A.anal_word(verb, guess=True, only_guess=False, preproc=True, phonetic=False, init_weight=VPOS)
    roots = []
    if not anals:
        print("No analyses for {}".format(verb))
        return None
    for anal in anals:
        if '?' not in anal['POS']:
            return None
        root = anal['root']
        if ':' not in root:
            print("No class for {} / {}".format(verb, root))
            return None
        root = root.replace('<', '').replace('>', '')
        root, cls = root.split(':')
        if (root, cls) in ignore:
            continue
        roots.append((root, cls))
    return roots

def anal_verbs(verbs, ignore=None):
    ignore = ignore or []
    roots = []
    n = 1
    for verb in verbs:
        if n % 100 == 0:
            print("Analyzed {} verbs".format(n))
        anal = anal_novel_verb(verb, ignore=ignore)
        if anal and anal not in roots:
            roots.append(anal)
        n += 1
    return roots

def get_external_roots(folder, file, rom=True, sep='\t', ncols=3, rootcol=1, encoding='utf16'):
    roots = []
    path = get_ext_data(folder, file)
    with open(path, encoding=encoding) as f:
        for line in f:
            line = line.strip()
            splitline = line.split(sep)
            root = splitline[rootcol]
            if not root:
                print("Empty root {}".format(line))
                continue
            if rom:
                root = romanize(root)
            root = root.replace(' ', '//')
            if root in roots:
                continue
#            print(root)
            roots.append(root)
    return roots

def get_external_roots2(folder, file1, file2, rom=True, sep='\t', ncols=3, rootcol=1, encoding1='utf16', encoding2='utf8'):
    roots1 = []
    roots2 = []
    joint = []
    path1 = get_ext_data(folder, file1)
    path2 = get_ext_data(folder, file2)
    overlong = 0
    with open(path1, encoding=encoding1) as f1:
        for line in f1:
            line = line.strip()
            splitline = line.split(sep)
            root = splitline[rootcol]
            if not root:
#                print("Empty root {}".format(line))
                continue
            if len(root.split()) > 2:
                overlong += 1
                continue
            if rom:
                root = romanize(root)
            root = root.replace(' ', '//')
            if root in roots1:
                continue
            roots1.append(root)
    with open(path2, encoding=encoding2) as f2:
        for line in f2:
            line = line.strip()
            splitline = line.split(sep)
            root = splitline[rootcol]
            if not root:
#                print("Empty root {}".format(line))
                continue
            if len(root.split()) > 2:
                overlong += 1
                continue
            if rom:
                root = romanize(root)
            root = root.replace(' ', '//')
            if root in roots2:
                continue
            if root in roots1:
#                print("{} is in nouns".format(root))
                joint.append(root)
                roots1.remove(root)
                continue
            roots2.append(root)
    print("Found {} overlong phrases".format(overlong))
    return roots1, roots2, joint

def filter_roots(external1, internal1, external2=None, internal2=None):
    '''
    external1 and internal1 are lists of roots.
    external2 is None or a list of roots for two POSs.
    internal2 is None or a second list of roots for a different POS.
    Returns external roots that are not in internal1 and a separate
    list of those that are in internal2 but not internal1.
    '''
    roots = []
    roots2 = []
    roots3 = []
    for root in external1:
        if root in internal1:
            continue
        roots.append(root)
        if internal2 and root in internal2:
            roots2.append(root)
    if external2:
        for root in external2:
            if root in internal1 and root in internal2:
                # Already joint POS
                continue
            roots3.append(root)
    if roots2:
        if roots3:
            return roots, roots2, roots3
        else:
            return roots, roots2
    else:
        return roots

def reverse_stems(write=True):
    dct = {}
    with open("hm/languages/amh/lex/n_stem.lex", encoding='utf8') as file:
        for line in file:
            line = line.split()
            if len(line) == 1:
                stem = line[0].strip()
            elif line[1] == "''":
                stem = line[0].strip()
            else:
                stem = line[1].strip()
            g = geezify(stem)
#            g = g.replace("//", " ")
#            if stem in dct:
#                print("{} already in dict".format(stem))
            dct[stem] = g
    with open("hm/languages/amh/lex/n_place.lex", encoding='utf8') as file:
        for line in file:
            stem = line.split()[0].strip()
            g = geezify(stem)
#            g = g.replace('//', ' ')
            dct[stem] = g
    with open("hm/languages/amh/lex/n_name.lex", encoding='utf8') as file:
        for line in file:
            stem = line.split()[0].strip()
            g = geezify(stem)
#            g = g.replace('//', ' ')
            dct[stem] = g
    if write:
        lst = list(dct.items())
        lst.sort()
        with open("hm/languages/amh/lex/n_ortho.lex", 'w', encoding='utf8') as file:
            for stem, geez in lst:
                print("{}  {}".format(geez, stem), file=file)
    else:
        return dct

##def convert_am_root(root, rc=None):
##    rc = rc or convert_am_roots()
##    reduced = root.replace('_', '').replace('|', '').replace('a', '')
##    entry = rc.get(reduced)
##    if not entry:
##        print("Something wrong: {} not in lexicon".format(root))
##        return None, ''
##    elif len(entry) == 1:
##        return reduced, entry[0]
##    else:
##        if '_' in root and 'B' in entry:
##            return reduced, 'B'
##        elif 'a' in root:
##            if 'C' in entry:
##                return reduced, 'C'
##            elif 'F' in entry:
##                return reduced, 'F'
##            elif 'J' in entry:
##                return reduced, 'J'
##        elif 'A' in entry:
##            return reduced, 'A'
##        elif 'E' in entry:
##            return reduced, 'E'
##        else:
##            print("Something wrong with {}, {}".format(root, entry))
##            return None, ''
##
##def convert_am_roots(write=True):
##    """Convert old root to (new root, class)."""
##    new_rc = {}
##    with open("hm/languages/amh/lex/v_root.lex", encoding='utf8') as file:
##        for line in file:
##            cls = 'A'
##            line = line.strip().split()
##            root = line[0]
##            if len(line) > 1:
##                features = line[-1]
##                if 'cls' in features:
##                    cls = features.split("cls=")[1][0]
##            if root in new_rc:
##                new_rc[root].append(cls)
##            else:
##                new_rc[root] = [cls]
##    if write:
##        with open("../LingData/Am/roots2class.txt", 'w', encoding='utf8') as file:
##            for root, cls in new_rc.items():
##                print("{} {}".format(root, ','.join(cls)), file=file)
##    return new_rc

##def add_class_to_feats(feats, cls):
##    feats = feats.split(';')
##    feats = ["[cls={},{}".format(cls, f[1:]) for f in feats]
##    return ';'.join(feats)
##
##def recreate_am(write=True):
##    result = []
##    with open("hm/languages/amh/lex/vb_root.lex", encoding='utf8') as file:
##        for line in file:
##            line = line.strip()
##            line = line.split('#')[0].strip()
##            linesplit = line.split()
##            if len(linesplit) != 3:
##                print(line)
##            root, lexeme, feats = line.split()
##            cls = ''
##            if '|' in root:
##                cls = 'G'
##                if 'a' in root:
##                    rootW = root.replace('W', '')
##                    # cls=H or cls=J
##                    if len(root) >= 7:
##                        cls = 'H'
##                    else:
##                        cls = 'J'
##                elif len(root) < 6:
##                    cls = 'I'
##                root = root.replace('|', '').replace('a', '')
##                feats = add_class_to_feats(feats, cls)
##                result.append("{}  ''  {}".format(root, feats))
##            elif '_' in root:
##                cls = 'B'
##                root = root.replace('_', '')
##                feats = add_class_to_feats(feats, cls)
##                result.append("{}  ''  {}".format(root, feats))
##            elif 'a' in root:
##                cls = 'C'
##                rootW = root.replace('W', '')
##                if len(rootW) > 4:
##                    cls = 'F'
##                root = root.replace('a', '')
##                feats = add_class_to_feats(feats, cls)
##                result.append("{}  ''  {}".format(root, feats))
##            else:
##                rootW = root.replace('W', '')
##                if len(rootW) > 4:
##                    cls = 'K'
##                elif len(rootW) > 3:
##                    cls = 'E'
##                if cls:
##                    feats = add_class_to_feats(feats, cls)
##                    result.append("{}  ''  {}".format(root, feats))
##                else:
##                    result.append(line)
##        if write:
##            with open("hm/languages/amh/lex/v_root.lex", 'w', encoding='utf8') as file:
##                for line in result:
##                    print(line, file=file)
##    return result
##
##def convert_ti_root(root, rc=None):
##    rc = rc or convert_ti_roots()
##    reduced = root.replace('_', '').replace('|', '').replace('a', '')
##    entry = rc.get(reduced)
##    if not entry:
##        print("Something wrong: {} not in lexicon".format(root))
##        return None, ''
##    elif len(entry) == 1:
##        return reduced, entry[0]
##    else:
##        if '_' in root and 'B' in entry:
##            return reduced, 'B'
##        elif 'a' in root:
##            if 'C' in entry:
##                return reduced, 'C'
##            elif 'F' in entry:
##                return reduced, 'F'
##            elif 'J' in entry:
##                return reduced, 'J'
##        elif 'A' in entry:
##            return reduced, 'A'
##        elif 'E' in entry:
##            return reduced, 'E'
##        else:
##            print("Something wrong with {}, {}".format(root, entry))
##            return None, ''
##
##def convert_ti_roots(write=True):
##    """Convert old root to (new root, class)."""
##    new_rc = {}
##    with open("hm/languages/ti/lex/v_root.lex", encoding='utf8') as file:
##        for line in file:
##            cls = 'A'
##            line = line.strip().split()
##            root = line[0]
##            if len(line) > 1:
##                features = line[-1]
##                if 'cls' in features:
##                    cls = features.replace(']','').split('cls=')[1]
##            if root in new_rc:
##                new_rc[root].append(cls)
##            else:
##                new_rc[root] = [cls]
##    if write:
##        with open("../LingData/Ti/roots2class.txt", 'w', encoding='utf8') as file:
##            for root, cls in new_rc.items():
##                print("{} {}".format(root, ','.join(cls)), file=file)
##    return new_rc
##
##def recreate_ti(write=True):
##    result = []
##    with open("hm/languages/ti/lex/vb_root.lex", encoding='utf8') as file:
##        for line in file:
##            line = line.strip()
##            if '|' in line:
##                cls = 'G'
##                if len(line.split()) > 1:
##                    print("Extra stuff in {}".format(line))
##                else:
##                    root = line
##                    if 'a' in root:
##                        # cls=H or cls=J
##                        if len(root) >= 7:
##                            cls = 'H'
##                        else:
##                            cls = 'J'
##                    elif len(root) < 6:
##                        cls = 'I'
##                root = root.replace('|', '').replace('a', '')
##                result.append("{}  ''  [cls={}]".format(root, cls))
##            elif '_' in line:
##                cls = 'B'
##                if len(line.split()) > 1:
##                    print("Extra stuff in {}".format(line))
##                else:
##                    root = line
##                    root = root.replace('_', '')
##                    result.append("{}  ''  [cls={}]".format(root, cls))
##            elif 'a' in line.split()[0]:
##                cls = 'C'
##                if len(line.split()) > 1:
##                    print("Extra stuff in {}".format(line))
##                else:
##                    root = line
##                    if len(root) > 4:
##                        cls = 'F'
##                    root = root.replace('a', '')
##                    result.append("{}  ''  [cls={}]".format(root, cls))
##            else:
##                linesplit = line.split()
##                root = linesplit[0]
##                rootW = root.replace('W', '')
##                if len(rootW) > 3:
##                    if len(line.split()) > 1:
##                        print("Extra stuff in {}".format(line))
##                    else:
##                        result.append("{}  ''  [cls=E]".format(root))
##                else:
##                    result.append(line)
##        if write:
##            with open("hm/languages/ti/lex/v_root.lex", 'w', encoding='utf8') as file:
##                for line in result:
##                    print(line, file=file)
##    return result
##
##IGN_ROOTS = ["'mm", "hwn", "b'l", "drg", "c'l", "gN*", "hyd", "nbr", "'y*", "hl_w", "nwr"]
##
##def classify_ras(anals=None, rootasps=None, write=True):
##    anals = anals or read_aroots()
##    rootasps = rootasps or read_root_trans()
##    missing = 0
##    total = 0
##    ra = {}
##    counted = 0
##    for root, asps in rootasps:
##        if root in IGN_ROOTS:
##            continue
##        anals1 = anals.get(root)
##        if not anals1:
##            missing += len(asps)
##            total += len(asps)
##        else:
##            dct = {}
##            total += len(asps)
##            fp = get_asp_props(anals1)
##            for asp in asps:
##                if asp not in fp:
##                    missing += 1
##                else:
##                    fp1 = fp.get(asp)
##                    so = ra_sbj_obj(fp1)
##                    if so[-1] < 5:
##                        missing += 1
##                        continue
##                    dct[asp] = so
##            if dct:
##                if len(dct) == 1:
##                    soc = list(dct.values())[0]
##                    if soc[0]:
##                        ra[root] = dct
##                        counted += 1
##                else:
##                    ra[root] = dct
##                    counted += len(dct)
##    print("Counted {}".format(counted))
##    if write:
##        ra = list(ra.items())
##        ra.sort()
##        with open("../LingData/Am/vcats0.txt", 'w', encoding='utf') as file:
##            for root, asps in ra:
##                asps = list(asps.items())
##                asps = [(a, c[0]) for a, c in asps]
##                print("{};{}".format(root, asps), file=file)
##                    
##    return ra
##
##def ra_sbj_obj(aspcount, categorize=True):
##    s = ra_sbj(aspcount)
##    o = ra_obj(aspcount)
##    total = sum([c for c in aspcount.values()])
##    if categorize:
##        cat = 0
##        if s < 0.1 and o > 0.05:
##            # multiple objects
##            cat = 1
##        elif s >= 0.1 and o <= 0.05:
##            # multiple subjects
##            cat = 2
##        elif s >= 0.1 and o > 0.05:
##            # multiple subjects and objects
##            cat = 3
##        return cat, total
##    else:
##        return s, o, total
##    
##def ra_obj(aspcount, summary=True):
##    total = 0
##    obj = 0
##    noobj = 0
##    for feat, count in aspcount.items():
##        total += count
##        o = feat[1]
##        if o:
##            obj += count
##        else:
##            noobj += count
##    return round(obj/total, 3)
##
##def ra_sbj(aspcount, summary=True):
##    """Given subject feature counts for root+aspectual, are multiple subjects possible?"""
##    total = 0
##    onetwo = 0
##    three = 0
##    for feat, count in aspcount.items():
##        total += count
##        if isinstance(feat, tuple):
##            feat = feat[0]
##        if summary:
##            if feat > 1:
##                # non 3sm/3p subject
##                onetwo += count
##            else:
##                three += count
##        elif '3' in feat:
##            # 3prs subject
##            three += count
##        else:
##            onetwo += count
##    return round(onetwo/total, 3)
##
##def get_tam(f):
##    return f['tm']
##
##def get_asp(f):
##    asp = f.get('as')
##    vc = f.get('vc')
##    if asp == 'smp':
##        if vc == 'smp':
##            return ''
##        elif vc == 'ps':
##            return 'ps'
##        elif vc == 'tr':
##            return 'tr'
##        else:
##            return 'cs'
##    elif asp == 'rc':
##        if vc == 'ps':
##            return 'psrc'
##        else:
##            return 'trrc'
##    elif vc == 'smp':
##        return 'it'
##    elif vc == 'ps':
##        return 'psit'
##    elif vc == 'cs':
##        return 'csit'
##    else:
##        return 'trit'
##
##def get_sb1(f, number=False, gender=True, summarize=True):
##    s = f.get('sb')
##    prs = (s.get('p1'), s.get('p2'), s.get('fem'), s.get('plr'))
##    string = ''
##    if not prs[0] and not prs[1]:
##        string += '3'
##        # 3 person
##        if gender and prs[2]:
##            string += 'f'
##    elif prs[0]:
##        # 1 person
##        string += '1'
##    elif prs[1]:
##        string += '2'
##        if gender and prs[2]:
##            string += 'f'
##    if number and prs[3]:
##        string += 'p'
##    if summarize:
##        if string == '3':
##            return 0
##        elif string == '3p':
##            return 1
##        else:
##            return 2
##    return string
##    
##def get_ob1(f, number=False, gender=True, app=False, summarize=True):
##    o = f.get('ob')
##    if not o.get('expl'):
##        if summarize:
##            return 0
##        else:
##            return ''
##    prs = (o.get('p1'), o.get('p2'), o.get('fem'), o.get('plr'), o.get('b'), o.get('l'))
##    if not app and o.get('prp'):
##        if summarize:
##            return 0
##        else:
##            return ''
##    string = ''
##    if not prs[0] and not prs[1]:
##        # 3 person
##        string += '3'
##        if gender and prs[2]:
##            string += 'f'
##    elif prs[0]:
##        # 1 person
##        string += '1'
##    # 2 person
##    elif prs[1]:
##        string += '2'
##        if gender and prs[2]:
##            string += 'f'
##    if number and prs[3]:
##        string += 'p'
##    if app:
##        if prs[4]:
##            string += "_b"
##        elif prs[5]:
##            string += "_l"
##    if summarize:
##        if string == '3':
##            return 1
##        else:
##            return 2
##    return string
##    
##def get_asp_props(fs, obj=True, tam=False, number=True, summarize=True):
##    result = {}
##    for f in fs:
##        res = []
##        asp = get_asp(f)
##        if tam:
##            res.append(get_tam(f))
##        prs = get_sb1(f, number=number, summarize=summarize)
##        res.append(prs)
##        if obj:
##            res.append(get_ob1(f, number=number, summarize=summarize))
##        if len(res) == 1:
##            res = res[0]
##        else:
##            res = tuple(res)
##        if asp not in result:
##            result[asp] = {}
##        r = result[asp]
##        if res in r:
##            r[res] += 1
##        else:
##            r[res] = 1
##    return result
##
##def read_aroots():
##    aroots = {}
##    impersonal = []
##    trans = []
##    with open("../LingData/Am/vroots0.txt", encoding='utf8') as file:
##        for line in file:
##            root, anals = line.split(';')
##            anals = anals.strip().split(':')
##            anals = [FS(a) for a in anals]
##            aroots[root] = anals
##    return aroots
##
##def aroots_from_corpus(start=0, number=25000, result=None, write=False):
##    result = result or {}
##    n = 0
##    with open("../LingData/Am/Crawl/all.txt", encoding='utf8') as file:
##        lines = list(file)
##        for line in lines[start:start+number]:
##            n += 1
##            if n % 500 == 0:
##                print("{} words processed, {} verb roots".format(n, len(result)))
##            x, am = line.split()
##            am = am.strip()
##            anal = AM.anal_word(am, preproc=True, guess=False)
##            if anal and len(anal) == 1: #all([x[1] for x in anal]):
##                for root, feats, count in anal:
##                    if not feats or root in IGN_ROOTS or feats.get('pos') != 'v':
##                        continue
##                    if root in result:
##                        rootentry = result[root]
##                        if len(rootentry) > 99:
##                            # already enough examples for this root
##                            continue
##                        if feats not in rootentry:
##                            result[root].append(feats)
##                    else:
##                        result[root] = [feats]
##    print("Processed from {} to {}".format(start, start+number))
##    if write:
##        res = list(result.items())
##        res.sort()
##        with open("../LingData/Am/vroots0.txt", 'w', encoding='utf8') as file:
##            for root, anals in res:
##                anals = ':'.join([a.__repr__() for a in anals])
##                print("{};{}".format(root, anals), file=file)
##    return result
##
##def make_new_ks_entries(old=None, new=None, write=True):
##    old = old or get_current_ks_roots()
##    new = new or get_new_ks_roots()
##    entries = []
##    for root, asp in new.items():
##        if root in old:
##            continue
##        root, cls = root.split('.')
##        feats = "[cls={}".format(cls)
##        if cls == 'A':
##            feats += ",-je"
##            if root[1] == root[2]:
##                feats += ",+dup"
##            else:
##                feats += ",-dup"
##        feats += "]"
##        entries.append("{}  {}".format(root, feats))
##        entries.sort(key=lambda e: e[e.index('=')+1])
##    if write:
##        with open("../LingData/Ks/new_v_roots.lex", 'w', encoding='utf8') as file:
##            for entry in entries:
##                print(entry, file=file)
##    return entries
##
##def get_current_ks_roots():
##    roots = set()
##    def get_class(feats):
##        if "=Aw" in feats:
##            return 'Aw'
##        elif "=AW" in feats:
##            return 'AW'
##        elif "=A" in feats:
##            return 'A'
##        elif "=B" in feats:
##            return 'B'
##        elif "=C" in feats:
##            return 'C'
##        elif "=E" in feats:
##            return 'E'
##        elif "=F" in feats:
##            return 'F'
##        else:
##            print("No class for {}".format(root))
##    with open("hm/languages/gru/lex/v_root.lex", encoding='utf8') as file:
##        for line in file:
##            if line[0] == '#' or not line.strip():
##                continue
##            root, feats = line.split()
##            cls = get_class(feats)
##            roots.add("{}.{}".format(root, cls))
##    with open("hm/languages/gru/lex/v_irr_stem.lex", encoding='utf8') as file:
##        for line in file:
##            stem, root, feats = line.split()
##            cls = get_class(feats)
##            roots.add("{}.{}".format(root, cls))
##    return roots
##
##def get_new_ks_roots():
##    roots = {}
##    with open("../LingData/Ks/am_v_entries.txt", encoding='utf8') as file:
##        for line in file:
##            aspects = []
##            root, feattrans = line.split(';')
##            feattrans = eval(feattrans.strip())
##            for ft in feattrans:
##                feat, trans = ft.split(':')
##                rootcls, asp = trans.split('_')
##                if rootcls in roots:
##                    roots[rootcls].add(asp)
##                else:
##                    roots[rootcls] = {asp}
##    return roots
##
##def read_root_trans():
##    rt = {}
##    rf = []
##    with open("../LingData/Ks/am_v_entries.txt", encoding='utf8') as file:
##        for line in file:
##            aspects = []
##            root, feattrans = line.split(';')
##            feattrans = eval(feattrans.strip())
##            for ft in feattrans:
##                feat, trans = ft.split(':')
##                feat = feat.replace('3', '')
##                if feat not in aspects:
##                    aspects.append(feat)
##            rf.append((root, aspects))
##    return rf
##
##def read_dict(write=True):
##    ak_roots = {}
##    ka_roots = {}
##    v_unambig = {}
##    v_unambig2 = {}
##    v_a2krf = {}
##    v_entries = {}
##    proc_entries = {}
##    unproc_entries = {}
##    feat_mismatch = {}
##    with open("../LingData/Ks/ak_roots.txt", encoding='utf8') as file:
##        for line in file:
##            a, k = line.split(';')
##            ak_roots[a] = eval(k.strip())
##    with open("../LingData/Ks/ka_roots.txt", encoding='utf8') as file:
##        for line in file:
##            k, a = line.split(';')
##            ka_roots[k] = eval(a.strip())
##    with open("../LingData/Ks/v_unambig.txt", encoding='utf8') as file:
##        for line in file:
##            a, k = line.split(';')
##            if ':' in k:
##                v_unambig2[a] = [kk.strip() for kk in k.split(':')]
##            else:
##                v_unambig[a] = k.strip()
##    with open("../LingData/Ks/v_a2krf.txt", encoding='utf8') as file:
##        for line in file:
##            a, k = line.split(';')
##            v_a2krf[a] = eval(k.strip())
##    with open("../LingData/Ks/v_new_entries1.txt", encoding='utf8') as file:
##        for line in file:
##            a, k = line.split(';')
##            v_entries[a] = eval(k.strip())
##    for aroot, aktrans in v_entries.items():
##        kroots = []
##        if aroot in v_unambig:
##            kroots = [v_unambig[aroot]]
##        elif aroot in v_unambig2:
##            kroots = v_unambig2[aroot]
##        not_found = 0
##        entry = {}
##        if kroots:
##            for afeat, ktrans in aktrans.items():
##                ktrans1 = [kt.split('_') for kt in ktrans]
##                found = False
##                for kr, kf in ktrans1:
##                    if kr in kroots:
##                        entry[afeat] = (kr, kf)
##                        found = True
##                        break
##                if not found:
##                    not_found += 1
##            if len(entry) < 2 and not_found > 1:
##                unproc_entries[aroot] = aktrans
##            else:
##                proc_entries[aroot] = entry
##        else:
##            unproc_entries[aroot] = aktrans
##    delete = []
##    for aroot, entries in unproc_entries.items():
##        aroot1 = aroot.replace('_', '').replace('a', '').replace("'", 'h').replace('|', '').replace('*', 'y')
##        if len(entries) == 1:
##            # Check on entries with only one feature and a root that resembles Am root
##            afeat, k = list(entries.items())[0]
##            if len(k) == 1:
##                # Only one root given
##                krf = list(k)[0]
##                kroot, kfeat = krf.split(krf)
##                proc_entries[aroot] = {afeat: (kroot, kfeat)} 
##                delete.append(aroot)
##                continue
##            for kk in k:
##                kroot, kfeat = kk.split('_')
##                kr = kroot.split('.')[0]
##                if kr == aroot1:
##                    delete.append(aroot)
##                    proc_entries[aroot] = {afeat: (kroot, kfeat)}
##        else:
##            # Check for repeating roots that match Am root
##            kroots = {}
##            # 2, 3 -> 1, 4, 5 -> 2
##            thresh = round(len(entries) / 2)
##            for afeat, k in entries.items():
##                for kk in k:
##                    kroot, kfeat = kk.split('_')
##                    if kroot in kroots:
##                        kroots[kroot] += 1
##                    else:
##                        kroots[kroot] = 1
##            kroots = list(kroots.items())
##            kroots.sort(key=lambda x: x[1], reverse=True)
##            match_root = ''
##            for kroot, count in kroots:
##                if count > 1:
##                    kr = kroot.split('.')[0]
##                    if kr == aroot1:
##                        match_root = kroot
##                        break
##                    elif count >= thresh:
##                        # kroot is in every feat entry
##                        match_root = kroot
##                        break
##            if match_root:
##                new_entry = {}
##                for afeat, k in entries.items():
##                    for kk in k:
##                        kroot, kfeat = kk.split('_')
##                        if kroot == match_root:
##                            new_entry[afeat] = (kroot, kfeat)
##                            break
##                proc_entries[aroot] = new_entry
##                delete.append(aroot)
##
##    for d in delete:
##        del unproc_entries[d]
##
##    print("Processed {}, unprocessed {}".format(len(proc_entries), len(unproc_entries)))
##
##    proc_entries = list(proc_entries.items())
##    proc_entries.sort()
##
##    if write:
##        with open("../LingData/Ks/am_v_entries.txt", 'w', encoding='utf8') as file:
##            for aroot, afeats in proc_entries:
##                afeats = list(afeats.items())
##                afeats = ["{}:{}".format(a[0], '_'.join(a[1])) for a in afeats]
##                print("{};{}".format(aroot, afeats), file=file)
##        
##    return proc_entries, unproc_entries
##
##def read_dict1(write=True):
##    entries = {}
##    kanals = {}
##    kambig = {}
##    newanals = {}
##    unanal = []
##    noanal = 0
##    a2kroots = {}
##    k2aroots = {}
##    a2krf = {}
##    with open("../LingData/Ks/kanals2.txt", encoding='utf8') as file:
##        for line in file:
##            word, anals = line.split(';')
##            anals = eval(anals)
##            kanals[word] = anals
##    with open("../LingData/Ks/kambig.txt", encoding='utf8') as file:
##        for line in file:
##            word, anals = line.split(';')
##            anals = eval(anals)
##            kambig[word] = anals
##    with open("../LingData/Ks/v_am2ks2.txt", encoding='utf8') as file:
##        for line in file:
##            linesplit = line.split(';')
##            if len(linesplit) != 3:
##                print("problem with {}".format(line.strip()))
##            am, a_anal, ks = linesplit
##            if " አለ" in am:
##                continue
##            asplit = a_anal.split(':')
##            if len(asplit) != 2:
##                print("Something wrong in {}".format(linesplit))
##            aroot, afeats = a_anal.split(':')
##            afeats = FS(afeats)
##            aas = afeats.get('as'); avc = afeats.get('vc')
##            afeats = ''.join((aas if aas != 'smp' else '', avc if avc != 'smp' else ''))
##            if am.endswith('ው') or am.endswith('ት'):
##                afeats += '3'
##            ks = ks.strip().split(':')
##            k_anals = []
##            for k in ks:
##                stored = True
##                if "ባሎ" in k or "አበሎ" in k or "ባለን፟ት" in k:
##                    continue
##                else:
##                    k_anal = kanals.get(k)
##                    ambig = []
##                    if not k_anal:
##                        if k in kambig:
##                            ambig = kambig[k]
##                            k_anals.extend(ambig)
##                        else:
##                            stored = False
##                    else:
##                        k_anals.append(k_anal)
##            if k_anals:
##                k_anals = [("{}.{}".format(ka[0], ka[1]), ka[2]) for ka in k_anals]
##                kroots = {ka[0] for ka in k_anals}
##                if aroot in a2kroots:
##                    a2kroots[aroot].update(kroots)
##                else:
##                    a2kroots[aroot] = kroots
##                if aroot not in a2krf:
##                    a2krf[aroot] = {}
##                ak = a2krf[aroot]
##                for kr, kf in k_anals:
##                    if kr in ak:
##                        ak[kr].add(kf)
##                    else:
##                        ak[kr] = {kf}
##                for kroot in kroots:
##                    if kroot in k2aroots:
##                        k2aroots[kroot].add(aroot)
##                    else:
##                        k2aroots[kroot] = {aroot}
##                k_anals = ['_'.join(ka) for ka in k_anals]
##                k_anals = set(k_anals)
##                if aroot in entries:
##                    e = entries[aroot]
##                    e[afeats] = k_anals
##                else:
##                    entries[aroot] = {afeats: k_anals}
##        # first isolate unambiguous translations
##        unambig = {}
##        unambig2 = {}
##        kassigned = {}
##        ambig = {}
##        delete = []
##        for a, k in a2kroots.items():
##            if len(k) == 1:
##                # only 1 translation for Am root
##                k = list(k)[0]
##                unambig[a] = k
##                delete.append(a)
##                kassigned[k] = a
##            else:
##                # dict of feature sets for each Ks root
##                ka = a2krf[a]
##                lendict = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: []}
##                for kk, aa in ka.items():
##                    lendict[len(aa)].append((kk, aa))
##                lendict = list(lendict.items())
##                lendict = [d for d in lendict if d[1]]
##                if len(lendict) > 1:
##                    lendict.sort(reverse=True)
##                    lendict0 = lendict[0][1]
##                    lendict0 = [l for l in lendict0 if '' in l[1]]
##                    if lendict0:
##                         if len(lendict0) == 1:
##                             # only one translation left after filtering
##                             unambig[a] = lendict0[0][0]
##                             delete.append(a)
##                         else:
##                             unambig2[a] = [l[0] for l in lendict0]
##                             delete.append(a)
##                
##        for d in delete:
##            del a2kroots[d]
##        if write:
##            a2kroots = list(a2kroots.items())
##            a2kroots.sort()
##            k2aroots = list(k2aroots.items())
##            k2aroots.sort()
##            unambig = list(unambig.items())
##            unambig.sort()
##            with open("../LingData/Ks/ak_roots.txt", 'w', encoding='utf8') as file:
##                for aroot, kroots in a2kroots:
##                    print("{};{}".format(aroot, kroots), file=file)
##            with open("../LingData/Ks/ka_roots.txt", 'w', encoding='utf8') as file:
##                for kroot, aroots in k2aroots:
##                    print("{};{}".format(kroot, aroots), file=file)
##            with open("../LingData/Ks/v_unambig.txt", 'w', encoding='utf8') as file:
##                for a, k in unambig:
##                    print("{};{}".format(a, k), file=file)
##            with open("../LingData/Ks/v_new_entries1.txt", 'w', encoding='utf8') as file1:
##                with open("../LingData/KS/v_new_entries2.txt", 'w', encoding='utf8') as file2:
##                    for am, afeats in entries.items():
##                        for af, ks in afeats.items():
##                            if len(ks) > 1:
##                                print("{}:{}".format(am, af), file=file2)
##                                for k in ks:
##                                    print("  {}".format(k), file=file2)
##                        print("{};{}".format(am, afeats.__repr__()), file=file1)
##            with open("../LingData/Ks/v_unal.txt", 'w', encoding='utf8') as file:
##                for word in unanal:
##                    print(word, file=file)
##    return a2krf, unambig2, kassigned
##
##def proc_targ_feats(feats):
##    return ''.join(('cs' if feats['vc'].get('cs') else '',
##                    'ps' if feats['vc'].get('ps') else '',
##                    feats.get('as') or '',
##                    str(feats.get('op')) if feats.get('op') else ''))
##
##def kroot_classes(write=False):
##    rcf = {}
##    kanal = {}
##    kunanal = {}
##    ambig = {}
##    kmultanal = {}
##    with open("../LingData/Ks/rcf2.txt", encoding='utf8') as file:
##        for line in file:
##            if not line.strip():
##                continue
##            rc, feats = line.split(';')
##            feats = eval(feats.strip())
##            r, c = rc.split(':')
##            rcf[(r, c)]  = feats
##    with open("../LingData/Ks/kanals2.txt", encoding='utf8') as file:
##        for line in file:
##            if not line.strip():
##                continue
##            word, feats = line.split(';')
##            kanal[word] = eval(feats.strip())
##    with open("../LingData/Ks/kmult2.txt", encoding='utf8') as file:
##        for line in file:
##            word, anals = line.split(';')
##            anals = eval(anals.strip())
##            roots = {a[0] for a in anals}
##            feats = {a[2] for a in anals}
##            classes = {a[1] for a in anals}
##            kmultanal[word] = anals
##    if write:
##        with open("../LingData/Ks/kmult2.txt", 'w', encoding='utf8') as file:
##            for word, anals in kmultanal.items():
##                print("{};{}".format(word, anals), file=file)
##        with open("../LingData/Ks/rcf2.txt", 'w', encoding='utf8') as file:
##            for (root, cls), feats in rcf.items():
##                print("{}:{};{}".format(root, cls, feats), file=file)
##        with open("../LingData/Ks/kanals2.txt", 'w', encoding='utf8') as file:
##            for word, prop in kanal.items():
##                print("{};{}".format(word, prop), file=file)
##            
##    return rcf, kanal, kmultanal, ambig
##
##def kroot_classes0(write=True):
##    """Trying to figure out what the Ks verb roots and classes are by
##    looking at possible analyses of all the verbs."""
##    ambig = {}
##    unambig = {}
##    req = {}
##    kwords = {}
##    newreq = {}
##    analwords = {}
##    unanalwords = set()
##    with open("../LingData/Ks/roots0.txt", encoding='utf8') as file:
##        # 700+ root+classes that are required for analysis of the verbs.
##        # For each a set of feature/word pairs
##        for line in file:
##            # feats is a set of feat, word pairs
##            rc, feats = line.split(';')
##            feats = list(eval(feats))
##            r, c = rc.split('_')
##            req[(r, c)] = {f[0] for f in feats}
##            newwords = {f[1] for f in feats}
##            for feat, word in feats:
##                analwords[word] = (r, c, feat)
##    with open("../LingData/Ks/roots1.txt", encoding='utf8') as file:
##        for line in file:
##            root, classfeats = line.split(';')
##            # classfeats is a dict: {class, {word:feats}}
##            classfeats = eval(classfeats)
##            if len(classfeats) == 1:
##                # only one class possible for this root
##                classfeats = list(classfeats.items())[0]
##                cls, feats = classfeats
##                feats = [f for f in feats if '1' not in f]
##                if not feats:
##                    continue
##                feats1 = [k.split(':') for k in feats]
##                feats0 = [k[1] for k in feats1]
##                for word, feat in feats1:
##                    if word not in analwords:
##                        unanalwords.add(word)
##                    if word in kwords:
##                        kwords[word].add((root, cls, feat))
##                    else:
##                        kwords[word] = {(root, cls, feat)}
##                if (root, cls) in req:
##                    req[(root, cls)].update(feats0)
##                else:
##                    unambig[(root, cls)] = feats
##            else:
##                unanal = set()
##                anal = set()
##                for cls, feats in classfeats.items():
##                    for wordfeat in feats:
##                        if '1' in wordfeat:
##                            continue
##                        word, feat = wordfeat.split(':')
##                        if word not in analwords:
##                            unanalwords.add(word)
##                        if word in kwords:
##                            kwords[word].add((root, cls, feat))
##                        else:
##                            kwords[word] = {(root, cls, feat)}
##                        if (root, cls) in req:
##                            anal.add(wordfeat)
##                        else:
##                            unanal.add(wordfeat)
##                unanal = unanal - anal
##                if unanal:
##                    ambig[root] = classfeats
##
##    kwords1 = {}
##    kwords2 = {}
##    for kword, rootclsfeats in kwords.items():
##        if len(rootclsfeats) == 1:
##            # only way to analyze this word
##            # check if (root, cls) is already in req
##            if kword not in analwords:
##                rt, cl, ft = list(rootclsfeats)[0]
##                analwords[kword] = (rt, cl, ft)
##                unanalwords.remove(kword)
##                if (rt, cl) in req:
##                    req[(rt, cl)].add(ft)
##                else:
##                    req[(rt, cl)] = {ft}
##        else:
##            req1 = []
##            notreq1 = []
##            for root, cls, feats in rootclsfeats:
##                if (root, cls) in req:
##                    req1.append((root, cls, feats))
##                else:
##                    notreq1.append((root, cls, feats))
##            if req1:
##                kwords1[kword] = req1
##                if len(req1) == 1:
##                    rt, cl, ft = req1[0]
##                    if kword not in analwords:
##                        analwords[kword] = (rt, cl, ft)
##                        unanalwords.remove(kword)
##                    if (rt, cl) not in req:
##                        print("Something wrong: {} not in req".format((rt, cl)))
##                    else:
##                        req[(rt, cl)].add(ft)
##            else:
##                kwords2[kword] = notreq1
##    # try filtering by which classes and features are alternatives
##    delete = []
##    change = []
##    for kword, rootclsfeats in kwords2.items():
##        if len(rootclsfeats) == 2:
##            classes = {rootclsfeats[0][1], rootclsfeats[1][1]}
##            features = {rootclsfeats[0][2], rootclsfeats[1][2]}
##            # C and E are alternatives
##            if classes == {'C', 'E'}:
##                rcf = ''
##                if rootclsfeats[0][1] == 'C':
##                    rcf = rootclsfeats[0]
##                else:
##                    rcf = rootclsfeats[1]
##                kwords1[kword] = [rcf]
##                delete.append(kword)
##                unanalwords.remove(kword)
##                r, c, f = rcf
##                analwords[kword] = (r, c, f)
##                if (r, c) in req:
##                    req[(r, c)].add(f)
##                else:
##                    req[(r, c)] = {f}
##            elif classes == {'A'} and len(features) == 1:
##                roots = [rootclsfeats[0][0], rootclsfeats[1][0]]
##                f = list(features)[0]
##                # pick the shorter root
##                roots.sort()
##                r = roots[0]
##                delete.append(kword)
##                unanalwords.remove(kword)
##                analwords[kword] = (r, 'A', f)
##                if (r, 'A') in req:
##                    req[(r, 'A')].add(f)
##                else:
##                    req[(r, 'A')] = {f}
##            elif classes == {'A'} and features == {'', 'csps'}:
##                rcf = ''
##                if rootclsfeats[0][2] == '':
##                    rcf = rootclsfeats[0]
##                else:
##                    rcf = rootclsfeats[1]
##                kwords1[kword] = [rcf]
##                delete.append(kword)
##                unanalwords.remove(kword)
##                r, c, f = rcf
##                analwords[kword] = (r, c, f)
##                if (r, c) in req:
##                    req[(r, c)].add(f)
##                else:
##                    req[(r, c)] = {f}
##            elif classes == {'A', 'Aw'}:
##                rcfa = ''
##                rcfw = ''
##                r = ''; c = ''; f = ''
##                if rootclsfeats[0][1] == 'Aw':
##                    rcfw = rootclsfeats[0]
##                    rcfa = rootclsfeats[1]
##                else:
##                    rcfw = rootclsfeats[1]
##                    rcfa = rootclsfeats[0]
##                # choose Aw if final root C is y
##                delete.append(kword)
##                unanalwords.remove(kword)
##                if rcfw[0][-1] == 'y':
##                    kwords1[kword] = [rcfw]
##                    r, c, f = rcfw
##                else:
##                    kwords1[kword] = [rcfa]
##                    r, c, f = rcfa
##                analwords[kword] = (r, c, f)
##                if (r, c) in req:
##                    req[(r, c)].add(f)
##                else:
##                    req[(r, c)] = {f}
##            elif classes == {'E', 'F'}:
##                # arbitrarily pick F over E
##                rcf = ''
##                if rootclsfeats[0][1] == 'F':
##                    rcf = rootclsfeats[0]
##                else:
##                    rcf = rootclsfeats[1]
##                r, c, f = rcf
##                delete.append(kword)
##                analwords[kword] = (r, c, f)
##                unanalwords.remove(kword)
##                kwords1[kword] = [rcf]
##                if (r, c) in req:
##                    req[(r, c)].add(f)
##                else:
##                    req[(r, c)] = {f}
##        elif len(rootclsfeats) == 3:
##            classes = {rootclsfeats[0][1], rootclsfeats[1][1], rootclsfeats[2][1]}
##            roots = {rootclsfeats[0][0], rootclsfeats[1][0], rootclsfeats[2][0]}
##            features = {rootclsfeats[0][2], rootclsfeats[1][2], rootclsfeats[2][2]}
##            if classes == {'A', 'B', 'C'} and len(features) == 1 and len(roots) == 1:
##                r = list(roots)[0]
##                f = list(features)[0]
##                delete.append(kword)
##                analwords[kword] = r, 'A', f
##                unanalwords.remove(kword)
##                kwords1[kword] = [(r, c, f)]
##                if (r, c) in req:
##                    req[(r, c)].add(f)
##                else:
##                    req[(r, c)] = {f}
##        else:
##            # 4 or more alternatives
##            updrcf = []
##            for r, c, f in rootclsfeats:
##                if c == 'E' and (r[1] == 'h' or (r[1] == 'W' and r[2] == 'h')):
##                    # Eliminate E roots like thrr
##                    continue
##                updrcf.append((r, c, f))
##            change.append((kword, updrcf))
##                    
##    for dl in delete:
##        del kwords2[dl]
##    for kw, f in change:
##        kwords2[kw] = f
##            
##    kwords2 = list(kwords2.items())
##    kwords2.sort()
##    with open("../LingData/Ks/kwords2.txt", 'w', encoding='utf8') as file:
##        for kword, analyses in kwords2:
##            print("{};{}".format(kword, analyses), file=file)
##    kwords1 = list(kwords1.items())
##    kwords1.sort()
##    with open("../LingData/Ks/kwords1.txt", 'w', encoding='utf8') as file:
##        for kword, analyses in kwords1:
##            print("{};{}".format(kword, analyses), file=file)
##    analwords = list(analwords.items())
##    analwords.sort()
##    with open("../LingData/Ks/kanals.txt", 'w', encoding='utf8') as file:
##        for kword, anal in analwords:
##            print("{};{}".format(kword, anal), file=file)
##    unanalwords = list(unanalwords)
##    unanalwords.sort()
##    with open("../LingData/Ks/kunanals.txt", 'w', encoding='utf8') as file:
##        for kword in unanalwords:
##            print("{}".format(kword), file=file)
##    req = list(req.items())
##    req.sort()
##    with open("../LingData/Ks/rcf.txt", 'w', encoding='utf8') as file:
##        for (r, c), f in req:
##            print("{}:{};{}".format(r, c, f), file=file)
##
##    return req, analwords, unanalwords
##
##def proc_source_feats(feats, cls=False):
##    fs = FS()
##    if feats:
##        values = ['as', 'vc']
##        if cls:
##            values.append('cls')
##            values.append('op')
##        for feat in values:
##            fs[feat] = feats.get(feat, None)
##    return fs
##
##def read_dict0(write=True):
##    n = 0
##    bad = set()
##    balo = []
##    roots0 = {}
##    roots1 = {}
##    am_words = {}
##    entries0 = {}
##    entries1 = {}
##    kroots0 = {}
##    kroots1 = {}
##    with open("../LingData/Ks/v_am2ks2.txt", encoding='utf8') as file:
##        for line in file:
##            n += 1
##            if n % 50 == 0:
##                print("{} lines".format(n))
##            linesplit = line.split(';')
##            am, a_anal, ks = linesplit
##            if " አለ" in am:
##                continue
##            asplit = a_anal.split(':')
##            if len(asplit) != 2:
##                print("Something wrong in {}".format(linesplit))
##            aroot, afeats = a_anal.split(':')
##            afeats = FS(afeats)
##            aas = afeats.get('as'); avc = afeats.get('vc')
##            afeats = ''.join((aas if aas != 'smp' else '', avc if avc != 'smp' else ''))
##            ks = ks.strip().split(':')
##            k_anal = []
##            for k in ks:
##                if "ባሎ" in k or "አበሎ" in k or "ባለን፟ት" in k:
##                    balo.append((am, a_anal, k))
##                else:
##                    k_proc = KS.anal_word(k,
##                                          init_weight=FS("[tm=prf,sp=3,-rel,-sub]"),
##                                          guess=True, preproc=True)
##                    if k_proc:
##                        k_proc = [(a[0], proc_source_feats(a[1], True)) for a in k_proc]
##                        kp = []
##                        if len(k_proc) == 1:
##                            k_proc0 = k_proc[0]
##                            r1 = k_proc0[0]
##                            ff = k_proc0[1]
##                            c1 = ff['cls']
##                            rootclass = r1 + "_" + c1
##                            f1 = ''.join(('cs' if ff['vc'].get('cs') else '', 'ps' if ff['vc'].get('ps') else '', ff.get('as') or '', str(ff.get('op')) if ff.get('op') else ''))
##                            if rootclass in roots0:
##                                roots0[rootclass].add((f1, k))
##                            else:
##                                roots0[rootclass] = {(f1, k)}
##                        for root, feats in k_proc:
##                            cls = feats.get('cls')
##                            rootclass = root + "_" + cls
##                            feats = ''.join(('cs' if feats['vc'].get('cs') else '', 'ps' if feats['vc'].get('ps') else '', feats.get('as') or '', str(feats.get('op')) if feats.get('op') else ''))
##                            formfeats = "{}:{}".format(k, feats)  # feats.__repr__())
##                            if root in roots1:
##                                entry = roots1[root]
##                                if cls in entry:
##                                    entry[cls].add(formfeats)
##                                else:
##                                    entry[cls] = {formfeats}
##                            else:
##                                roots1[root] = {cls: {formfeats}}
##                            kp.append((rootclass, feats))
##                        k_anal.append((k, kp))
##                    else:
##                        bad.add(k)
##            if k_anal:
##                if len(k_anal) == 1:
##                    # Only one translation
##                    entries0[(aroot, afeats)] = k_anal[0]
##                else:
##                    if aroot in entries1:
##                        rootentry = entries1[aroot]
##                        if afeats in rootentry:
##                            rootentry[afeats] = k_anal
##                        else:
##                            rootentry[afeats] = k_anal
##                    else:
##                        entries1[aroot] = {afeats: k_anal}
##                        
##    for kroot, kclasses in roots1.items():
##        if len(kclasses) == 1:
##            # only one class for kroot
##            kclass = list(kclasses.keys())[0]
##            kroots0["{}_{}".format(kroot, kclass)] = list(kclasses.values())[0]
##        else:
##            kroots1[kroot] = kclasses
##    roots0 = list(roots0.items())
##    roots0.sort()
##    roots1 = list(roots1.items())
##    roots1.sort()
##    entries0 = list(entries0.items())
##    entries0.sort()
##    entries1 = list(entries1.items())
##    entries1.sort()
##    kroots0 = list(kroots0.items())
##    kroots0.sort()
##    kroots1 = list(kroots1.items())
##    kroots1.sort()
##    if write:
##        with open("../LingData/Ks/roots0.txt", 'w', encoding='utf8') as file:
##            for k, v in roots0:
##                print("{};{}".format(k, v), file=file)
##        with open("../LingData/Ks/roots1.txt", 'w', encoding='utf8') as file:
##            for k, v in roots1:
##                print("{};{}".format(k, v), file=file)
##        with open("../LingData/Ks/kroots0.txt", 'w', encoding='utf8') as file:
##            for k, v in kroots0:
##                print("{};{}".format(k, v), file=file)
##        with open("../LingData/Ks/v_lex0.txt", 'w', encoding='utf8') as file:
##             for (aroot, afeats), k_anal in entries0:
##                 print("{}:{};{}:{}".format(aroot, afeats, k_anal[0], k_anal[1]), file=file)
##        with open("../LingData/Ks/v_lex1.txt", 'w', encoding='utf8') as file:
##             for aroot, aclasses in entries1:
##                 print("{};;{}".format(aroot, aclasses), file=file)
##    return (entries0, entries1), (kroots0, kroots1) #, (roots1, roots2)
##
##def read_dict1(write=True):
##    entries = []
##    multi = []
##    n = 0
##    bad = []
##    with open("../LingData/Ks/v_am2ks.txt", encoding='utf8') as file:
##        for line in file:
##            n += 1
##            if n % 25 == 0:
##                print("{} lines".format(n))
##            linesplit = line.split(';')
##            if len(linesplit) != 2:
##                print("line {} too long!".format(linesplit))
##                continue
##            am, ks = linesplit
##            am = am.strip()
##            ks = ks.strip()
##            if am.endswith("አለ"):
##                multi.append((am, ks))
##            else:
##                am_proc = AM.anal_word(am,
##                                       init_weight=FS("[pos=v,tm=prf,sb=[-p1,-p2],-rel,-acc,ax=None,-sub]"),
##                                       guess=False, preproc=True)
##                if am_proc:
##                    entries.append((am, [(a[0], proc_source_feats(a[1])) for a in am_proc], ks))
##                else:
##                    bad.append((am, ks))
##    if write:
##        with open("../LingData/Ks/v_am2ks2.txt", 'w', encoding='utf8') as efile:
##            for am, anals, ks in entries:
##                print("{};{};{}".format(am, '::'.join([a[0] + ':' + a[1].__repr__() for a in anals]), ks),
##                      file=efile)
##        with open("../LingData/Ks/v_am2ks_comp.txt", 'w', encoding='utf8') as mfile:
##            for am, ks in multi:
##                print("{};{}".format(am, ks), file=mfile)
