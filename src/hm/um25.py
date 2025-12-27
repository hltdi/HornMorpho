'''
Updated for HM 5. Generation of verbs for UM repository and ASh project.
'''

from .morpho import *
from .morpho.geez import *

CONV_FEATS = \
           {'vc=ps': 'v=p',
            'vc=tr': 'v=a',
            'vc=cs': 'v=as',
            'as=it': 'a=i',
            'as=rc': 'a=a',
            'sb=[+plr]': 'sn=2'}

PNG = [('sp=1,sn=1', '1;SG'), ('sp=1,sn=2', '1;PL'),
       ('sp=2,sg=m,sn=1', '2;MASC;SG'), ('sp=2,sg=f,sn=1', '2;FEM;SG'), ('sp=2,sn=2', '2;PL'),
       ('sp=3,sg=m,sn=1', '3;MASC;SG'), ('sp=3,sg=f,sn=1', '3;FEM;SG'), ('sp=3,sn=2', '3;PL')]

TAM = [('t=p', 'PFV'), ('t=i', 'IFPV'), ('t=j', 'IMP'), ('t=c', 'PRF')]

DISPREFS = ['ቅክ', 'ቅኩ', 'ክክ', 'ክኩ', 'አለሁ', 'ያለሁ', 'አለሽ', 'ዋል', 'አል', 'ህ', 'ሁ', 'ያለሽ',
            'ዪ', 'ቺ', 'ሺ', 'ጂ', 'ዢ', 'ኚ', 'ጪ']

DISPREFSPRE = ['አስ', 'ያስ', 'እናስ', 'ታስ', 'ላስ']

DISPREFSIN = ['ትተ', 'ትታ', 'ትቷ']

AM = languages.get_language('a')
AMV = AM.morphology['v']

def filter(forms, feats=None):
    if len(forms) == 1:
        return forms
    for dp in DISPREFS:
        todel = []
        for f in forms:
            if f.endswith(dp):
                todel.append(f)
        if todel:
            for td in todel:
                forms.remove(td)
                if len(forms) == 1:
                    return forms
    if len(forms) > 1:
        for dp in DISPREFSPRE:
#            print("Checking {}".format(dp))
            todel = []
            for f in forms:
#                print("  Checking {}".format(f))
                if f.startswith(dp):
                    forms.remove(f)
                    if len(forms) == 1:
                        return forms
    if len(forms) > 1:
        for dp in DISPREFSIN:
#            print("Checking {}".format(dp))
            todel = []
            for f in forms:
#                print("  Checking {}".format(f))
                if dp in f and not f.startswith(dp):
                    forms.remove(f)
                    if len(forms) == 1:
                        return forms
    return forms

def generate():
    forms = []
    count = 0
    with open("../UM/a_vp_feats5.txt") as file:
        for line in file:
            count += 1
            if count % 25 == 0:
                print("Processed {} lines".format(count))
            line = line.strip()
#            print(line)
            f = generate_line(line)
            forms.extend(f)
    return forms

def generate_line(line):
    root, gloss, feats = line.split(';;')
    forms = generate_verb_all(root, feats)
    return forms

##def convert():
##    lines = []
##    with open("../UM/a_vp_feats.txt") as file:
##        for line in file:
##            root, gloss, feats = line.split(';;')
##            root = root.strip()[1:-1]
##            root, cls = root.split(':')
##            root = geezify(root)
##            clsfeat = "c={}".format(cls)
##            feats = feats.strip().split(',')
###            f = []
###            for feat in feats:
###                if feat in CONV_FEATS:
###                    f.append(CONV_FEATS[feat])
##            feats.append(clsfeat)
##            feats = ','.join(feats)
##            lines.append("{};;{};;{}".format(root, gloss.strip(), feats))
##    return lines

def generate_verb_all(root, feats):
    forms = []
    lemma = AMV.gen5(root, feats)
    if not lemma:
        print("No lemma for {} : {}".format(root, feats))
        return []
    lemma = lemma[0][0]
    for tam, tamfeat in TAM:
        ff = "{},{}".format(feats, tam)
        form = generate_verb(root, ff, tamfeat, lemma)
        forms.extend(form)
    return forms

def generate_verb(root, feats, um, lemma):
    forms = []
    for png, pngfeats in PNG:
        f = "{},{}".format(feats, png)
        form = AMV.gen5(root, f)
        allfeats = "{};{}".format(um, pngfeats)
        if form:
            form = [ff[0] for ff in form]
            form = filter(form)
            if len(form) > 1:
                print("Too many forms generated for {}: {}:: {}".format(root, feats, form))
                forms.append((form, lemma, allfeats))
            else:
                forms.append((form[0], lemma, allfeats))
        else:
            print("No form generated for {}: {}: {}".format(root, lemma, allfeats))
    return forms

def generate_recip():
    forms = []
    roots = []
    with open("../UM/a_vp_feats.txt") as file:
        for line in file:
            if "as=it,vc=ps" in line:
                root, gloss, feat = line.split(" ;; ")
                root = root[1:-1]
                root, cls = root.split(':')
                root = geezify(root)
                form = AMV.gen5(root, "a=i,v=p,c={}".format(cls))
                if form:
                    forms.append(form[0][0])
    return forms
                
            
