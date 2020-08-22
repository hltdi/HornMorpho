"""
-- Create Am<->Ks lexicon.
-- Recreate Ti lexicon, eliminating non-root characters.
-- Create reverse dictionary for noun roots.
"""

from . import morpho

A = morpho.get_language('amh')
#KS = morpho.get_language('ks')
FS = morpho.FeatStruct
geezify = morpho.geez.geezify

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
##
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
