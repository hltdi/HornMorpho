### Amharic, Tigrinya classification of roots by voice/valency.

from . import morpho
normalize = morpho.geez.normalize

IGN_ROOTS = {'a': ["ህልው:B"], 't': ["ህልው:B"]}

IGNORE = {'a': ["አሳማ", "አምባቸው", "ባምሳ", "አምሳ"]}

UM_FEATS = \
  ["1", "2", "3", "MASC", "FEM", "SG", "PL",
   "TR", "CAUS", "PASS", "ITER", "RECP", "CAUS+RECP", "RECP1", "CAUS+RECP1", "RECP2", "CAUS+RECP2",
   "AC1S", "AC2SM", "AC2SF", "AC3SM", "AC3SF", "AC1P", "AC2P", "AC3P", "{AC3SM/DEF}",
   # Tigrinya
   "AC2PM", "AC2PF", "AC3PM", "AC3PF",
   # Applicative suffixes, Am
   "DA3SM", "DA3SF", "DA3P", "DA1S", "DA1P", "DA2SM", "DA2SF", "DA2P",
   "MAL3SM", "MAL3SF", "MAL3P", "MAL1S", "MAL1P", "MAL2SM", "MAL2SF", "MAL2P",
   # Applicative suffixes, Ti
   "OB3SM", "OB3SF", "OB3PM", "OB3PF", "OB1S", "OB1P", "OB2SM", "OB2SF", "OB2PM", "OB2PF"
    ]

LV_ROOT2LEMMA = {
    'ብእል:base': 'አለ', 'ድርግ:caus1': 'አደረገ', 'ብእል:pass': 'ተባለ', 'ስኝይ:pass': 'ተሰነ', 'ስኝይ:caus2': 'አሰኘ', 'ድርግ:pass': 'ተደረገ',
    'ድርግ:caus': 'አደረገ', 'ስኝይ:caus': 'አሰኘ', 'base': 'አለ', 'ድርግ:base': 'አደረገ', 'ስኝይ:base': 'ተሰኘ'
    }

### Always object, always 3sm subj

def ambient(dct, root, aimad):
    return vrdict(dct, root, aimad, '3sm_*')

def passive(dct, root):
    return vrdict(dct, root, 'pass')

#def transitive(dct, root, aimod):
#    return vrdict(dct, root, aimad, '

def read_vroot_png(path, drop1=True):
    roots = {}
    aimad = {}
    root = ''
    count = 0
    with open(path, encoding='utf8') as file:
        for line in file:
            if line[0] != ' ':
                if root:
                    # Add last root to roots
                    roots[root] = aimad
                aimad = {}
                # New root
                root, count = line.split()
                count = int(count)
                aimad['count'] = count
            else:
                ai, acount, png = line.strip().split('\t')
                acount = int(acount)
                png = eval(png)
                png = dict(png)
                png['count'] = acount
                aimad[ai] = png
    # Last root
    roots[root] = aimad
    return roots

def combine_dicts(d1, d2):
    for root, feats in d2.items():
        if root not in d1:
            d1[root] = feats
        else:
            r1 = d1[root]
            for vc, png in feats.items():
                if vc not in r1:
                    r1[vc] = png
                else:
                    rvc = r1[vc]
                    for p, count in png.items():
                        if p not in rvc:
                            rvc[p] = count
                        else:
                            rvc[p] += count

def proc_am(light=False, constraints=None, thresh=[0, 0, 0], write_png=False):
    '''
    thresh is a triple with threshold totals for root, vc (voice class),
    and sbjobj (PNG, transitivity).
    '''
    AM = morpho.get_language('a', v5=True)
    V = AM.morphology['v']
    u, a, l = get_vroot_png(constraints=constraints)
#    if light:
#        l = combine_light(l)
    if write_png:
        write_vroot_png(u, language='a', light=light, constraints=constraints)
    trans = gen_trans_cats(constraints)
    c = count_voice_classes(l if light else u, scale=False, trans=trans,
                          light=light, constraints=constraints, thresh=thresh, vmorph=V)
    write_root_counts(c, light=light, constraints=constraints, comment=', '.join(trans))
    return u, a, l, c

def proc_ti(light=False, constraints=None, thresh=[0, 0, 0], write_png=False):
    TI = morpho.get_language('t', v5=True)
    V = TI.morphology['v']
    u, a, l = get_vroot_png(path='data/ti_classes.txt', language='t', constraints=constraints)
    if write_png:
        write_vroot_png(u, language='t', light=light, constraints=constraints)
    trans = gen_trans_cats(constraints)
    c = count_voice_classes(l if light else u, language='t', scale=False, trans=trans,
                          light=light, constraints=constraints, thresh=thresh, vmorph=V)
    write_root_counts(c, 't', light=light, constraints=constraints, comment=', '.join(trans))
    return u, a, l, c

def get_vroot_png(path="data/am_classes.txt", language='a', report='', constraints=None):
    '''
    Returns dicts for unambiguous roots, ambiguous roots, and
    multi-word (light verb) roots.
    '''
    unamb_roots = {}
    amb_roots = {}
    light_roots = {}
    items = get_vclass_data(path)
    ign_roots = IGN_ROOTS.get(language, [])
    ignore = IGNORE.get(language, [])
    if constraints and 'applic' in constraints:
        applic = constraints['applic']
    else:
        applic = 0

    print("N items {}".format(len(items)))

    # classify roots+vc by whether they have 1 or 2 person subjects
    s12 = set()
    reject_imp = []
    for index, word, anals in items:
        if word in IGNORE:
            continue
        if len(anals) == 1:
            anal = anals[0]
            if 'root' not in anal:
                continue
            root = anal['root']
            um = anal['um']
            sense = anal.get('sense', 0)
            vc = classify_um_vc2(um, language=language)
            pers = get_subpers(um)
            if pers == '12':
                s12.add((root, vc, sense))

    print("N s12 {}".format(len(s12)))

    for index, word, anals in items:
        word = normalize(word, language=language)
#        if word in IGNORE:
#            continue
        if len(anals) > 1:
            # ambiguous
            unique_anals = set()
            for anal in anals:
                if 'root' not in anal or 'pos' not in anal:
                    continue
                root = anal['root']
                pos = anal['pos']
#                if word == "አሳማ":
#                    print(" ** root {} pos {}".format(root, pos))
                if anal['pos'] != "V":
                    unique_anals.add((root, '~V', 0))
                    continue
                root = anal['root']
                um = anal['um']
                sense = anal.get('sense', 0)
                vc = classify_um_vc2(um, language=language)
                if (root, vc, sense) in reject_imp:
                    continue
                elif is_imperative(um) and (root, vc, sense) not in s12:
                    reject_imp.append((root, vc, sense))
#                    print("** Rejecting imperative reading of {} ({},{})".format(word, root, vc))
                    continue
                um = filter_um(um, language=language, applic=applic)
                unique_anals.add((root, um, sense))

            if len(unique_anals) > 1:
                if any([(u == '~V') for r, u, s in unique_anals]):
                    continue
                # still ambiguous
                tam = []
                for root, um, sense in unique_anals:
                    if " " in word:
                        if ' ' not in root:
                            root = word.split()[0] + ' ' + root
                        if root in ign_roots:
                            add_root_um(light_roots, root, um)
                    elif root not in ign_roots:
                        if sense:
                            root += ":{}".format(sense)
                        add_root_um(amb_roots, root, um)
            elif len(unique_anals) == 1:
                unique_anals = list(unique_anals)[0]
                root = unique_anals[0]
                um = unique_anals[1]
                sense = unique_anals[2]
                if " " in word:
                    if ' ' not in root:
                        root = word.split()[0] + ' ' + root
                    if root not in ign_roots:
                        add_root_um(light_roots, root, um)
                elif root not in ign_roots:
                    if report and report == root:
                        print("** {}: {}".format(word, um))
                    if sense:
                        root += ":{}".format(sense)
                    add_root_um(unamb_roots, root, um)
        else:
            anal = anals[0]
            if 'root' not in anal:
                continue
            root = anal['root']
            um = filter_um(anal['um'], language=language, applic=applic)
            sense = anal.get('sense', 0)
#            if um[0] == 'rcp':
#                continue
            if ' ' in word:
                if ' ' not in root:
                    root = word.split()[0] + ' ' + root
                if root not in ign_roots:
                    add_root_um(light_roots, root, um)
            elif root not in ign_roots:
                if report and report == root:
                    print("** {}: {}".format(word, um))
                if sense:
                    root += ":{}".format(sense)
                add_root_um(unamb_roots, root, um)
    for root, dct in unamb_roots.items():
#        if root == "እምም:A":
#            print("Adding {}: {}".format(root, dct))
        dct = group_by_vc(dct)
        unamb_roots[root] = dct
    for root, dct in amb_roots.items():
        dct = group_by_vc(dct)
        amb_roots[root] = dct
    for root, dct in light_roots.items():
        dct = group_by_vc(dct)
        light_roots[root] = dct
    light_roots = combine_light(light_roots)
#    print("{} verbs analyzed".format(nverbs))
    return unamb_roots, amb_roots, light_roots

def write_vroot_png(dct, language='a', light=False, filename='', vthresh=4, rthresh=10, pthresh=2, constraints=None):
    if not filename:
        filename = make_rvpng_filename(language=language, light=light, constraints=constraints)
    path = "../../SemVV/data/" + filename

    ls = list(dct.items())
    ls.sort()
    with open(path, 'w', encoding='utf8') as file:
        for root, classes in ls:
            rcount = 0
            classes = list(classes.items())
            classes.sort()
            lines = []
            for voice, trans in classes:
                trans = list(trans.items())
                # Eliminate png counts below pthresh
                trans = [t for t in trans if t[1] >= pthresh]
                if not trans:
                    continue
                trans.sort()
#                print(" ** trans {}".format(trans))
                vcount = sum([t[1] for t in trans])
                if vcount < vthresh:
                    continue
                rcount += vcount
                lines.append("  {}\t{}\t{}".format(voice, vcount, trans))
            if rcount < rthresh:
                continue
            print("{} {}".format(root, rcount), file=file)
            for line in lines:
                print(line, file=file)

def merge_png(png):
    '''
    png is *_, *_*, 3sm_*, 3_*, ~3sm_, ~3sm_*.
    '''
    match png:
        case '*_':
            # intransitive
            return ['3sm_', '12_', '3f|p_']
        case '*_*':
            # transitive
            return ['3sm_12', '3sm_3', '12_o', '3f|p_o']
        case '3sm_*':
            return ['3sm_12', '3sm_3']
        case '3_*':
            return ['3sm_', '3f|p_']
        case '~3sm_':
            return ['12_', '3f|p_']
        case '~3sm_*':
            return ['12_o', '3f|p_o']
        case _:
            return []

def vrdict_get(dct, root, aimad, png='', light=False, proportion=True, drop1=True):
    '''
    Get the count for root, aimad, and png within the root_dict.
    '''
    if ':' not in root and not light:
        root += ":A"
    if root_png := dct.get(root):
#        print("rpng {}".format(root_png))
        if root_aimad := root_png.get(aimad):
            total = root_png['count']
            subtot = 0
#            print("ra {}".format(root_aimad))
            subcount = root_aimad['count']
            if png == '':
                # Return all values
                subtot = subcount
#                sum(root_aimad.values())
            elif png in root_aimad:
                subtot = root_aimad[png]
            else:
                pngs = merge_png(png)
                if not pngs:
#                    print("No way to merge {}".format(png))
                    subtot = 0
#                    sum(root_aimad.values())
                else:
                    subtot = sum([root_aimad.get(p, 0) for p in pngs])
            if proportion:
                return round(subtot / total, 3), round(subtot / subcount, 3)
            else:
                return subtot
    return 0

def gen_lemma(language, vmorph, root, cls, label):
#    if ':' not in root:
#        print("*** {}".format(root))
#        return ''
    # root could have a sense element "ምእር:A:2"
#    root_split = root.split(':')
#    root = root_split[0]
#    cls = root_split[1]
#    root, cls = root.split(':')
    upd_feats = 'c={}'.format(cls)
    if language == 'a' and root[0] == 'እ':
        label_feats = VC2FEATS_L1[label]
    else:
        label_feats = VC2FEATS[label]
    if label_feats:
        upd_feats += ",{}".format(label_feats)
#    print("upd feats {}".format(upd_feats))
    if forms := vmorph.gen5(root, upd=upd_feats):
        return vmorph.postproc5(forms[0][0], gemination=False)
    # Fix cases where original feature is v=ast or v=test
    if language == 'a' and (root[0] == 'እ' or root[1] == 'እ'):
        label_feats = VC2FEATS_L.get(label)
        if label_feats:
            upd_feats = 'c={},{}'.format(cls, label_feats)
            if forms := vmorph.gen5(root, upd=upd_feats):
                return vmorph.postproc5(forms[0][0], gemination=False)
    return ''

def gen_trans_cats(constraints):
    if constraints:
        if 'reduce' in constraints:
            return ['3m_', '~3m_', '3m_o', '~3m_o']
        elif constraints.get('applic') == 1:
            return ['3sm_', '3sm_12', '3sm_3', '3sm_L', '12_', '12_o', '12_L', '3f|p_', '3f|p_o', '3f|p_L']
        elif constraints.get('applic') == 2:
            return ['3sm_', '3sm_12', '3sm_3', '3sm_L', '3sm_B', '12_', '12_o', '12_L', '12_B', '3f|p_', '3f|p_o', '3f|p_L', '3f|p_B']
        elif constraints.get('applic') == 3:
            return ['3sm_', '3sm_12', '3sm_3', '3sm_L12', '3sm_B12', '3sm_L3', '3sm_B3', '12_', '12_o', '12_L3', '12_B3', '12_L12', '12_B12', '3f|p_', '3f|p_o', '3f|p_L3', '3f|p_B3', '3f|p_L12', '3f|p_B12']
    return ['3sm_', '3sm_12', '3sm_3', '12_', '12_o', '3f|p_', '3f|p_o']

def classify_subj(um):
    if isinstance(um, str):
        um = um.split(';')
    if '1' in um or '2' in um:
        return '12'
    elif 'FEM' in um or 'PL' in um:
        return '3f|p'
#    elif 'FEM' in um and 'PL' not in um:
#        return '3sf'
#    elif 'PL' in um:
#        return '3p'
    else:
        return '3sm'

def classify_obj(um, ignore_png=False, applic=False):
    if isinstance(um, str):
        um = um.split(';')
    if ignore_png:
        if any([u.startswith("AC") for u in um]):
            return 'o'
        elif applic and any([(u.startswith('DA') or u.startswith('DA') or u.startswith("MAL")) for u in um]):
            return 'A'
        else:
            return ''
    if any([(o in um) for o in ["AC1S", "AC1P", "AC2SM", "AC2SF", "AC2P", "AC2PM", "AC2PF"]]):
        return '12'
    elif any ([(o in um) for o in ["AC3P", "AC3PM", "AC3PF", "AC3SM", "AC3SF"]]):
        return '3'
    elif applic and any ([(o in um) for o in ["DA1S", "DA1P", "DA2SM", "DA2SF", "DA2P", "OB1S", "OB1P", "OB2SM", "OB2SF", "OB2PM", "OB2PF"]]):
        if applic == 3:
            return 'L12'
        else:
            return 'L'
    elif applic and any ([(o in um) for o in ["DA3SM", "DA3SF", "DA3P", "OB3SM", "OB3SF", "OB3PM", "OB3PF"]]):
        if applic == 3:
            return 'L3'
        else:
            return 'L'
    elif applic and any ([(o in um) for o in ["MAL1S", "MAL1P", "MAL2SM", "MAL2SF", "MAL2P"]]):
        if applic == 3:
            return 'B12'
        elif applic == 2:
            return 'B'
        else:
            return 'L'
    elif applic and any ([(o in um) for o in ["MAL3SM", "MAL3SF", "MAL3P"]]):
        if applic == 3:
            return 'B3'
        elif applic == 2:
            return 'B'
        else:
            return 'L'
    else:
        return ''

def classify_png(um, applic=0):
    s = classify_subj(um)
    o = classify_obj(um, s in ['12', '3f|p'], applic=applic)
    return s, o

def get_sbj_count(png_dict, include=None, trans=0):
    '''
    trans=0; don't care
    trans=-1; intransitive only
    trans=1; transitive only
    '''
    include = include or ['12', '3p', '3sf', '3pm', '3pf', '3f|p']
    total = 0
    for png, count in png_dict.items():
        sb, ob = png.split('_')
        if trans == 1:
            if not ob:
                continue
        elif trans == -1:
            if ob:
                continue
        if sb in include:
            total += count
    return total

def get_obj_count(png_dict, include=None):
    '''
    If include is None, all objects are included.
    '''
    total = 0
    for png, count in png_dict.items():
        sb, ob = png.split('_')
        if ob and (not include or ob in include):
            total += count
    return total

def binarize(root_dict, thresh=1):
    '''
    Make features binary.
    '''
    for root, values in root_dict.items():
#        print("root {} values {}".format(root, values))
        if isinstance(values, list):
            for index, v in enumerate(values):
                if v > thresh:
                    values[index] = 1
                else:
                    values[index] = 0
        else:
            for png, count in values.items():
                if count > thresh:
                    values[png] = 1
                else:
                    values[png] = 0

def logarithmize(root_dict):
    '''
    Convert features to base e logs.
    '''
    for root, values in root_dict.items():
        for png, count in values.items():
            values[png] = math.log(count)

def consol_trans(root_dict, filter=[1, 5], sep_png=True):
    '''
    Combine transitive features.
    '''
    root_trans = {}
    for val, valdict in root_dict.items():
        valtrans = [0, 0, 0, 0]
        for png, count in valdict.items():
            if filter and count <= filter[0]:
                continue
            s, o = png.split('_')
            if o:
                if sep_png:
                    if s == '3sm':
                        valtrans[2] += count
                    else:
                        valtrans[3] += count
                else:
                    valtrans[2] += count
            elif sep_png:
                if s == '3sm':
                    valtrans[0] += count
                else:
                    valtrans[1] += count
            else:
                valtrans[0] += count
        if filter and (sum(valtrans) <= filter[1]):
            continue
        root_trans[val] = valtrans if sep_png else [valtrans[0], valtrans[2]]
    return root_trans

def consolidate(png_dict, constraints=None, filter=False):
    '''
    constraints is a triple: (subj_feats, obj_feats, new_name)
    '*' is a wild card. '' means no object.
    '''
    to_del = []
    total = 0
    if not constraints:
        return
    else:
        sfeats, ofeats, new_name = constraints
    for png, count in png_dict.items():
        s, o = png.split('_')
        if (sfeats == '*' or s in sfeats) and ((not o and not ofeats) or (o and ofeats == '*' or o in ofeats)):
            to_del.append(png)
            total += count
    if new_name:
        png_dict[new_name] = total
    if to_del:
        for d in to_del:
            del png_dict[d]

def filter_um(um, language='a', applic=False):
    if isinstance(um, str):
        um = um.split(';')
    um_ = []
    for u in um:
        if u in UM_FEATS:
            um_.append(u)
    cls = classify_um_vc2(um_, language=language)
    s, o = classify_png(um, applic=applic)
    return cls, s, o

def classify_um_vc2(um, language='a'):
#    print("Classifying {}".format(um))
    if isinstance(um, str):
        um = um.split(';')
    if language == 'a':
        if '*TEDERAGI' in um or 'PASS' in um:
            return 'pass'
        if '*ADRAGI' in um or '*ASDERAGI' in um or 'CAUS' in um or 'TR' in um:
            return 'caus'
        if '*TEDARAGI' in um or '*TEDERARAGI' in um or 'RECP1' in um or 'RECP2' in um:
            return 'rcp'
        if '*ADARAGI' in um or '*ADERARAGI' in um or 'CAUS+RECP1' in um or 'CAUS+RECP2' in um:
            return 'causrcp'
        if '*DERARAGI' in um:
            return 'iter'
        return 'base'
    if 'PASS' in um:
        return 'pass'
    elif 'CAUS+RECP1' in um:
        return 'causrcp'
    elif 'CAUS+RECP2' in um:
        return 'causrcp'
    elif 'CAUS' in um:
        return 'caus'
    elif 'TR' in um:
        return 'caus'
    elif 'ITER' in um:
        return 'iter'
    elif 'RECP1' in um:
        return 'rcp'
    elif 'RECP2' in um:
        return 'rcp'
    else:
        return 'base'

def get_vc(um):
    um = um.split(';')
    if 'PASS' in um:
        return 'pass'
    elif 'TR' in um:
        return 'caus1'
    elif 'CAUS' in um:
        return 'caus2'
    elif 'RECP' in um:
        return 'rcp'
    elif 'CAUS+RECP' in um:
        return 'caurcp'
    elif 'ITER' in um:
        return 'iter'
    else:
        return 'base'

def add_root_um(dct, root, um):
    if root in dct:
        if um in dct[root]:
            dct[root][um] += 1
        else:
            dct[root][um] = 1
    else:
        dct[root] = {um: 1}

def get_vclass_data(path):
    items = []
    nverbs = 0
    with open(path, encoding='utf8') as file:
        contents = file.read().split('\n##\n')
        # index, word, anals triples
        for item in contents:
#            print("ITEM\n{}".format(item))
            lines = item.split("\n")
            if len(lines) == 1:
                continue
            sentence = lines[0]
#            print(sentence)
            for line in lines[1:]:
                line = eval(line)
                index, word, anals = line
                anals = filter_anals_by_pos(anals)
#                if word == "አሳማ":
#                    print("... anals {}".format(anals))
                if anals:
                    nverbs += 1
                    items.append((index, word, anals))
    return items
    
def group_by_vc(vcpng):
    '''
    vcpng is a dict of vc, sb, ob triples with counts as values.
    '''
    result = {}
    for (vc, s, o), count in vcpng.items():
        so = '_'.join([s, o])
        if vc not in result:
            result[vc] = {}
        result[vc][so] = count
    return result

def make_rvpng_filename(language='a', light=False, constraints=None):
    if language == 'a':
        filename = 'am'
    else:
        filename = 'ti'
    if light:
        filename += '_light'
    if constraints:
        if 'rcp' in constraints:
            filename += '_rcp'
        if 'applic' in constraints:
            filename += '_app'
    return filename + '_rvpng.txt'

def make_feat_filename(language='a', light=False, constraints=None):
    sep_vc = constraints.get('sep_vc', 0) if constraints else 0
    if language == 'a':
        filename = 'am'
    else:
        filename = 'ti'
    if light:
        filename += '_light'
    if constraints:
        if 'reduce' in constraints:
            filename += '_red'
        if 'rcp' in constraints:
            filename += '_rcp'
        if 'applic' in constraints:
            filename += '_app'
        if 'binary' in constraints:
            filename += '_bin'
        if 'log' in constraints:
            filename += '_log'
    return filename + ('_rvf.txt' if sep_vc else '_rf.txt')

def get_root_instances(root, path="data/am_v_classes.txt"):
    '''
    Get all instances of the root from the corpus.
    '''
    words = {}
    wc = {}
    items, nverbs = get_vclass_data(path)
    for index, word, anals in items:
        res = []
        for anal in anals:
            if 'root' not in anal:
                continue
            r = anal['root']
            if r == root:
                um = anal['um']
                res.append(um)
        if res:
            if len(res) < len(anals):
                # ignore words that ambiguous for class
                pass
            elif word in words:
              wc[word] += 1
            else:
              words[word] = res
              wc[word] = 1
    return words, wc

def is_imperative(um):
    um = um.split(';')
    return 'IMP' in um and '2' in um

def get_subpers(um):
    um = um.split(';')
    if '1' in um or '2' in um:
        return '12'
    else:
        return '3'

def combine_light(dct):
    '''
    Combine the pngs for roots for each particle.
    '''
    result = {}
    for part_root, png in dct.items():
        part, root = part_root.split()
        if part not in result:
            result[part] = {}
        result[part][root] = png
    result2 = {}
    for part, root_dcts in result.items():
        if part not in result2:
            result2[part] = {}
        part_dct = result2[part]
        for root, root_dct in root_dcts.items():
            root = root.split(':')[0]
#            if not root:
#                print("No root for {}".format(root_dct))
            for aimad, png in root_dct.items():
                root_a = root + ':' + aimad if root else aimad
                root_a = LV_ROOT2LEMMA[root_a]
                part_dct[root_a] = png
    return result2

def count_voice_classes(dct, language='a', scale=True, trans=None, constraints=None, light=False,
                        thresh=[0, 0, 0], vmorph=None):
    """
    Constraints is a dict of features constraints:
    'reduce', 'rcp', 'binary'
    """
    classes = []
    if language == 'a' and light:
        classes = ['base_ብ', 'pass_ብ', 'caus_ድ', 'pass_ድ', 'caus_ስ', 'pass_ስ']
#        if light:
#            classes = ['base_ብ', 'pass_ብ', 'caus1_ድ', 'pass_ድ', 'caus2_ስ', 'pass_ስ']
#        else:
#            classes = ['base', 'pass', 'caus1', 'caus2']
    else:
        classes = ['base', 'pass', 'caus']
    if constraints and 'rcp' in constraints:
        classes.extend(['iter', 'rcp', 'causrcp'])
#        classes.extend(['iter', 'rcp1', 'rcp2', 'causrcp1', 'causrcp2'])
    counts = {}
    roots_entries = []
    nelim = 0
    if any(thresh):
        # filter out entries that don't satisfy threshold
        new_entries = {}
        for root, entry in dct.items():
            rtotal = 0
            new_root = {}
            for vc, sbjobj in entry.items():
                vctotal = 0
                new_vc = {}
                for so, count in sbjobj.items():
                    if thresh[2] and count < thresh[2]:
#                        print("   ** Eliminating {} {} for {} {}".format(so, count, vc, root))
                        continue
                    new_vc[so] = count
                    vctotal += count
                if thresh[1] and vctotal < thresh[1]:
#                    print("  ** Eliminating {} {} for {}".format(vc, vctotal, root))
                    continue
                new_root[vc] = new_vc
                rtotal += vctotal
            if rtotal == 0 or (thresh[0] and rtotal < thresh[0]):
#                if root == "ቅምጥ:B":
#                    print("** Eliminating {} ({})".format(root, rtotal))
                nelim += 1
                continue
            new_entries[root] = new_root
        dct = new_entries
        print("** Eliminated {} roots".format(nelim))
    for root, entry in dct.items():
        root_split = root.split(':')
        root = root_split[0]
        root_cls = root_split[1]
        sense = root_split[2] if len(root_split) == 3 else 0
        if constraints:
            if 'reduce' in constraints:
                entry = consol_trans(entry)
            if 'binary' in constraints:
                binarize(entry)
            elif 'log' in constraints:
                logarithmize(entry)
        if constraints.get('sep_vc', False):
            for vc_cls in classes:
                vc_count = get_vc_counts(entry.get(vc_cls), scale, trans=trans, constraints=constraints)
                if sum(vc_count):
                    lemma_label = ''
                    lemma = gen_lemma(language, vmorph, root, root_cls, vc_cls)
                    if lemma:
                        lemma_label = "{}:{}".format(lemma, root_cls)
                        if sense:
                            lemma_label += ":{}".format(sense)
                    label = lemma_label if lemma else "{}_{}".format(root, vc_cls)
                    # Don't include empty VCs
                    counts[label] = vc_count
        else:
            result = []
            for cls in classes:
                if cls == 'caus':
                    if language == 'a':
                        # For Amharic prefer caus1 (ኣ-) over caus2 (ኣስ-)
                        if 'caus1' in entry:
                            result.extend(get_vc_counts(entry.get('caus1'), scale, trans=trans, constraints=constraints))
                        else:
                            result.extend(get_vc_counts(entry.get('caus2'), scale, trans=trans, constraints=constraints))
                    else:
                        result.extend(get_vc_counts(entry.get('caus'), scale, trans=trans, constraints=constraints))
                else:
                    result.extend(get_vc_counts(entry.get(cls), scale, trans=trans, constraints=constraints))
            counts[root] = result
    return counts

def get_vc_counts(vc_dct, scale=False, trans=None, constraints=None):
    """
    For a given voice class dictionary,
    return a vector of counts for each of the transitivity categories.
    constraints is list of constraints on features:
    'reduce', 'binary', 'log'
    """
#    print("** get vc counts {}".format(vc_dct))
    reduce = constraints and 'reduce' in constraints
    applic = constraints and constraints.get('applic')
    if not vc_dct:
        if reduce:
            return [0, 0, 0, 0]
        elif applic == 1:
            return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        elif applic == 2:
            return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        elif applic == 3:
            return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        else:
            return [0, 0, 0, 0, 0, 0, 0]
    if reduce:
        return vc_dct
    result = []
    for t in trans:
        result.append(vc_dct.get(t, 0))
    if scale:
        total = sum(result)
        if total > 0:
            result = [round(c/total, 3) for c in result]
    return result

def write_root_counts(dct, language='a', light=False, filename='', constraints=None, comment=''):
    binary = False
    if constraints and 'binary' in constraints:
        binary = True
#    if binary:
#        thresh = 0
    directory = "../../SemVV/data/"
#    sep_vc = constraints.get('sep_vc', 0)
    if not filename:
        filename = make_feat_filename(language=language, light=light, constraints=constraints)
    path = directory + filename
    ls = list(dct.items())
#    ls.sort()
    with open(path, 'w', encoding='utf8') as file:
        if comment:
            print("##\t{}".format(comment), file=file)
        for root, classes in ls:
            total = sum(classes)
#            if root == 'ምጥእ:A':
#                print("** total {}, classes {}".format(total, classes))
            if total == 0:
                continue
#            if thresh and total < thresh:
#                continue
            if constraints and 'log' in constraints:
                classes = [round(c, 3) for c in classes]
            print("{}\t{}".format(root, classes), file=file)

def filter_anals_by_um(anals, exclude=['TOP', 'NEG']):
    res = []
    for anal in anals:
        um = anal.get('um')
        if not um:
            continue
        um = um.split(';')
        if any([x in um for x in exclude]):
#            print("** Excluding {}".format(um))
            continue
        res.append(anal)
    return res

def filter_anals_by_pos(anals, pos='V'):
    if any([(anal.get('pos') != pos) for anal in anals]):
        return []
    res = []
    for anal in anals:
        p = anal.get('pos')
        if not p or p != pos:
            continue
        res.append(anal)
    return res

