"""
Create Am<->Ks lexicon.
"""

from . import morpho

#AM = morpho.get_language('am')
KS = morpho.get_language('ks')
FS = morpho.FeatStruct

def read_dict(write=True):
    entries = {}
    kanals = {}
    kambig = {}
    newanals = {}
    unanal = []
    noanal = 0
    with open("../LingData/Ks/kanals2.txt", encoding='utf8') as file:
        for line in file:
            word, anals = line.split(';')
            anals = eval(anals)
            kanals[word] = anals
    with open("../LingData/Ks/kambig.txt", encoding='utf8') as file:
        for line in file:
            word, anals = line.split(';')
            anals = eval(anals)
            kambig[word] = anals
    with open("../LingData/Ks/v_am2ks2.txt", encoding='utf8') as file:
        for line in file:
#            print(line.strip())
            linesplit = line.split(';')
            if len(linesplit) != 3:
                print("problem with {}".format(line.strip()))
            am, a_anal, ks = linesplit
            if " አለ" in am:
                continue
            asplit = a_anal.split(':')
            if len(asplit) != 2:
                print("Something wrong in {}".format(linesplit))
            aroot, afeats = a_anal.split(':')
            afeats = FS(afeats)
            aas = afeats.get('as'); avc = afeats.get('vc')
            afeats = ''.join((aas if aas != 'smp' else '', avc if avc != 'smp' else ''))
            if am.endswith('ው') or am.endswith('ት'):
                afeats += '3'
            ks = ks.strip().split(':')
            k_anals = []
#            print(am)
            for k in ks:
                stored = True
                if "ባሎ" in k or "አበሎ" in k or "ባለን፟ት" in k:
                    continue
#                    balo.append((am, a_anal, k))
                else:
                    k_anal = kanals.get(k)
                    ambig = []
                    if not k_anal:
                        if k in kambig:
                            ambig = kambig[k]
                            k_anals.extend(ambig)
                        else:
                            stored = False
                    else:
                        k_anals.append(k_anal)
                    if k not in newanals:
                        k_proc = KS.anal_word(k,
                                              init_weight=FS("[tm=prf,sp=3,-rel,-sub]"),
                                              guess=True, preproc=True)
                        if k_proc:
                            k_proc = [(a[0], proc_source_feats(a[1], True)) for a in k_proc if a[1].get('op') != 1]
                            k_proc = [(a[0], a[1]['cls'], proc_targ_feats(a[1])) for a in k_proc]
                            if not stored:
#                                print("NEW ANALYSES FOR {}: {}".format(k, k_proc))
                                k_anals.extend(k_proc)
                            elif len(k_proc) > 1:
                                if k_anal not in k_proc and not set(k_proc).intersection(ambig):
                                    print("{}: analysis {} not in {}".format(k, k_anal, k_proc))
                                if ambig:
#                                    print("ambig {}".format(ambig))
                                    newanals[k] = ambig, list(set(k_proc) - set(ambig))
                                elif k_anal not in k_proc:
                                    print("Old anal {} not among new anals {}".format(k_anal, k_proc))
                                else:
                                    k_proc.remove(k_anal)
                                    newanals[k] = k_anal, k_proc
                        elif not stored:
                            others = len(ks)-1
                            if not others and k not in unanal:
#                                print("No analysis for {} in {} with no other translations".format(k, am))
                                unanal.append(k)
                                noanal += 1
            if k_anals:
                entries[(am, aroot, afeats)] = k_anals
#        if write:
#            with open("../LingData/Ks/v_new_entries.txt", 'w'
        print("{} words without analyses".format(noanal))
    return entries, newanals, unanal

def proc_targ_feats(feats):
    return ''.join(('cs' if feats['vc'].get('cs') else '',
                    'ps' if feats['vc'].get('ps') else '',
                    feats.get('as') or '',
                    str(feats.get('op')) if feats.get('op') else ''))

def kroot_classes(write=False):
    rcf = {}
    kanal = {}
    kunanal = {}
    ambig = {}
    kmultanal = {}
    with open("../LingData/Ks/rcf2.txt", encoding='utf8') as file:
        for line in file:
            if not line.strip():
                continue
            rc, feats = line.split(';')
            feats = eval(feats.strip())
            r, c = rc.split(':')
            rcf[(r, c)]  = feats
    with open("../LingData/Ks/kanals2.txt", encoding='utf8') as file:
        for line in file:
            if not line.strip():
                continue
            word, feats = line.split(';')
            kanal[word] = eval(feats.strip())
    with open("../LingData/Ks/kmult2.txt", encoding='utf8') as file:
        for line in file:
            word, anals = line.split(';')
            anals = eval(anals.strip())
            roots = {a[0] for a in anals}
            feats = {a[2] for a in anals}
            classes = {a[1] for a in anals}
#            if len(roots) == 1:
#                # Same root for all choices
#                root = list(roots)[0]
#            if {'A', 'B', 'C'} == classes and feats == {'ps', 'psrc'}:
#                root = list(roots)[0]
#                if (root, 'C') in rcf:
#                    rcf[(root, 'C')].add('ps')
#                    kanal[word] = (root, 'C', 'ps')
#                elif (root, 'A') in rcf:
#                    rcf[(root, 'A')].add('psrc')
#                    kanal[word] = (root, 'A', 'psrc')
#                elif (root, 'B') in rcf:
#                    rcf[(root, 'B')].add('psrc')
#                    kanal[word] = (root, 'B', 'psrc')
#                else:
#                    # pick C otherwise
#                    rcf[(root, 'C')] = {'ps'}
#                    kanal[word] = (root, 'C', 'ps')
#            elif {'A', 'B'} < classes:
#                print("Causative ABC: {}".format(anals))
#                root = list(roots)[0]
#                feat = list(feats)[0]
#                if (root, 'A') in rcf:
#                    print("  but {} is already associated with A: {}".format(root, rcf[(root, 'A')]))
#                    rcf[(root, 'A')].add(feat)
#                    kanal[word] = (root, 'A', feat)
#                elif (root, 'B') in rcf:
#                    print("  but {} is already associated with B: {}".format(root, rcf[(root, 'B')]))
#                    rcf[(root, 'B')].add(feat)
#                    kanal[word] = (root, 'B', feat)
#                else:
            kmultanal[word] = anals
#    with open("../LingData/Ks/kwords1.txt", encoding='utf8') as file:
#        for line in file:
#            word, anals = line.split(';')
#            anals = eval(anals.strip())
#            ambig[word] = anals
    if write:
        with open("../LingData/Ks/kmult2.txt", 'w', encoding='utf8') as file:
            for word, anals in kmultanal.items():
                print("{};{}".format(word, anals), file=file)
        with open("../LingData/Ks/rcf2.txt", 'w', encoding='utf8') as file:
            for (root, cls), feats in rcf.items():
                print("{}:{};{}".format(root, cls, feats), file=file)
        with open("../LingData/Ks/kanals2.txt", 'w', encoding='utf8') as file:
            for word, prop in kanal.items():
                print("{};{}".format(word, prop), file=file)
            
    return rcf, kanal, kmultanal, ambig

def kroot_classes0(write=True):
    """Trying to figure out what the Ks verb roots and classes are by
    looking at possible analyses of all the verbs."""
    ambig = {}
    unambig = {}
    req = {}
    kwords = {}
    newreq = {}
    analwords = {}
    unanalwords = set()
    with open("../LingData/Ks/roots0.txt", encoding='utf8') as file:
        # 700+ root+classes that are required for analysis of the verbs.
        # For each a set of feature/word pairs
        for line in file:
            # feats is a set of feat, word pairs
            rc, feats = line.split(';')
            feats = list(eval(feats))
            r, c = rc.split('_')
            req[(r, c)] = {f[0] for f in feats}
            newwords = {f[1] for f in feats}
            for feat, word in feats:
                analwords[word] = (r, c, feat)
#            analword.update(newwords)
    with open("../LingData/Ks/roots1.txt", encoding='utf8') as file:
        for line in file:
            root, classfeats = line.split(';')
            # classfeats is a dict: {class, {word:feats}}
            classfeats = eval(classfeats)
            if len(classfeats) == 1:
                # only one class possible for this root
                classfeats = list(classfeats.items())[0]
                cls, feats = classfeats
                feats = [f for f in feats if '1' not in f]
#                print("feats {}".format(feats))
                if not feats:
                    continue
                feats1 = [k.split(':') for k in feats]
                feats0 = [k[1] for k in feats1]
#                words = [k[0] for k in feats]
                for word, feat in feats1:
                    if word not in analwords:
                        unanalwords.add(word)
                    if word in kwords:
                        kwords[word].add((root, cls, feat))
                    else:
                        kwords[word] = {(root, cls, feat)}
                if (root, cls) in req:
#                    print("unambig ({}, {}) already in required".format(root, cls))
                    req[(root, cls)].update(feats0)
                else:
#                if (root, cls) in unambig:
                    unambig[(root, cls)] = feats
            else:
                unanal = set()
                anal = set()
                for cls, feats in classfeats.items():
                    for wordfeat in feats:
                        if '1' in wordfeat:
                            continue
                        word, feat = wordfeat.split(':')
                        if word not in analwords:
                            unanalwords.add(word)
                        if word in kwords:
                            kwords[word].add((root, cls, feat))
                        else:
                            kwords[word] = {(root, cls, feat)}
                        if (root, cls) in req:
                            anal.add(wordfeat)
#                            print("({}, {}) for {} in required".format(root, cls, wordfeat))
                        else:
#                            print("({}, {}) for {} not in required".format(root, cls, wordfeat))
                            unanal.add(wordfeat)
                unanal = unanal - anal
                if unanal:
                    ambig[root] = classfeats

    kwords1 = {}
    kwords2 = {}
    for kword, rootclsfeats in kwords.items():
        if len(rootclsfeats) == 1:
            # only way to analyze this word
            # check if (root, cls) is already in req
            if kword not in analwords:
                rt, cl, ft = list(rootclsfeats)[0]
#                print("{}|{} has only 1 analysis but is not in analwords".format(kword, list(rootclsfeats)[0]))
#                analwords.add(kword)
                analwords[kword] = (rt, cl, ft)
                unanalwords.remove(kword)
                if (rt, cl) in req:
                    req[(rt, cl)].add(ft)
                else:
                    req[(rt, cl)] = {ft}
#            root, cls, feats = list(rootclsfeats)[0]
#            if (root, cls) not in req:
#                print("({}, {}) required for {}".format(root, cls, kword))
#                if (root, cls) in newreq:
#                    newreq[(root, cls)].add(feats)
#                else:
#                    newreq[(root, cls)] = {feats}
        else:
            req1 = []
            notreq1 = []
            for root, cls, feats in rootclsfeats:
                if (root, cls) in req:
                    req1.append((root, cls, feats))
                else:
                    notreq1.append((root, cls, feats))
            if req1:
                kwords1[kword] = req1
                if len(req1) == 1:
                    rt, cl, ft = req1[0]
                    if kword not in analwords:
#                        print("One required anal for {}: {}".format(kword, (
                        analwords[kword] = (rt, cl, ft)
#                        analwords.add(kword)
                        unanalwords.remove(kword)
                    if (rt, cl) not in req:
                        print("Something wrong: {} not in req".format((rt, cl)))
                    else:
                        req[(rt, cl)].add(ft)
            else:
                kwords2[kword] = notreq1
    # try filtering by which classes and features are alternatives
    delete = []
    change = []
    for kword, rootclsfeats in kwords2.items():
        if len(rootclsfeats) == 2:
            classes = {rootclsfeats[0][1], rootclsfeats[1][1]}
            features = {rootclsfeats[0][2], rootclsfeats[1][2]}
            # C and E are alternatives
            if classes == {'C', 'E'}:
                rcf = ''
                if rootclsfeats[0][1] == 'C':
                    rcf = rootclsfeats[0]
                else:
                    rcf = rootclsfeats[1]
#                print("Simplifying C/E analysis of {}|{}".format(kword, rcf))
                kwords1[kword] = [rcf]
                delete.append(kword)
                unanalwords.remove(kword)
                r, c, f = rcf
                analwords[kword] = (r, c, f)
#                analwords.add(kword)
                if (r, c) in req:
#                    print("Something wrong: {}".format((r, c)))
                    req[(r, c)].add(f)
                else:
                    req[(r, c)] = {f}
            elif classes == {'A'} and len(features) == 1:
                roots = [rootclsfeats[0][0], rootclsfeats[1][0]]
                f = list(features)[0]
                # pick the shorter root
                roots.sort()
                r = roots[0]
                delete.append(kword)
                unanalwords.remove(kword)
                analwords[kword] = (r, 'A', f)
                if (r, 'A') in req:
                    req[(r, 'A')].add(f)
                else:
                    req[(r, 'A')] = {f}
            elif classes == {'A'} and features == {'', 'csps'}:
                rcf = ''
                if rootclsfeats[0][2] == '':
                    rcf = rootclsfeats[0]
                else:
                    rcf = rootclsfeats[1]
#                print("Simplifying A/A analysis of {}|{}".format(kword, rcf))
                kwords1[kword] = [rcf]
                delete.append(kword)
                unanalwords.remove(kword)
                r, c, f = rcf
                analwords[kword] = (r, c, f)
#                analwords.add(kword)
                if (r, c) in req:
#                    print("Something wrong: {}".format((r, c)))
                    req[(r, c)].add(f)
                else:
                    req[(r, c)] = {f}
            elif classes == {'A', 'Aw'}:
                rcfa = ''
                rcfw = ''
                r = ''; c = ''; f = ''
                if rootclsfeats[0][1] == 'Aw':
                    rcfw = rootclsfeats[0]
                    rcfa = rootclsfeats[1]
                else:
                    rcfw = rootclsfeats[1]
                    rcfa = rootclsfeats[0]
                # choose Aw if final root C is y
                delete.append(kword)
                unanalwords.remove(kword)
                if rcfw[0][-1] == 'y':
                    kwords1[kword] = [rcfw]
                    r, c, f = rcfw
                else:
                    kwords1[kword] = [rcfa]
                    r, c, f = rcfa
                analwords[kword] = (r, c, f)
                if (r, c) in req:
                    req[(r, c)].add(f)
                else:
                    req[(r, c)] = {f}
            elif classes == {'E', 'F'}:
                # arbitrarily pick F over E
                rcf = ''
                if rootclsfeats[0][1] == 'F':
                    rcf = rootclsfeats[0]
                else:
                    rcf = rootclsfeats[1]
                r, c, f = rcf
                delete.append(kword)
#                analwords.add(kword)
                analwords[kword] = (r, c, f)
                unanalwords.remove(kword)
                kwords1[kword] = [rcf]
                if (r, c) in req:
                    req[(r, c)].add(f)
                else:
                    req[(r, c)] = {f}
        elif len(rootclsfeats) == 3:
            classes = {rootclsfeats[0][1], rootclsfeats[1][1], rootclsfeats[2][1]}
            roots = {rootclsfeats[0][0], rootclsfeats[1][0], rootclsfeats[2][0]}
            features = {rootclsfeats[0][2], rootclsfeats[1][2], rootclsfeats[2][2]}
            if classes == {'A', 'B', 'C'} and len(features) == 1 and len(roots) == 1:
                r = list(roots)[0]
                f = list(features)[0]
#                print('Selecting A from A/B/C for {}, root: {}'.format(kword, r))
                delete.append(kword)
                analwords[kword] = r, 'A', f
                unanalwords.remove(kword)
                kwords1[kword] = [(r, c, f)]
                if (r, c) in req:
                    req[(r, c)].add(f)
                else:
                    req[(r, c)] = {f}
        else:
            # 4 or more alternatives
            updrcf = []
            for r, c, f in rootclsfeats:
                if c == 'E' and (r[1] == 'h' or (r[1] == 'W' and r[2] == 'h')):
                    # Eliminate E roots like thrr
#                    print("Eliminating {} for {}".format(r, kword))
                    continue
                updrcf.append((r, c, f))
            change.append((kword, updrcf))
                    
    for dl in delete:
#        print("Deleting {} from kwords2".format(dl))
        del kwords2[dl]
    for kw, f in change:
        kwords2[kw] = f
            
    kwords2 = list(kwords2.items())
    kwords2.sort()
    with open("../LingData/Ks/kwords2.txt", 'w', encoding='utf8') as file:
        for kword, analyses in kwords2:
            print("{};{}".format(kword, analyses), file=file)
    kwords1 = list(kwords1.items())
    kwords1.sort()
    with open("../LingData/Ks/kwords1.txt", 'w', encoding='utf8') as file:
        for kword, analyses in kwords1:
            print("{};{}".format(kword, analyses), file=file)
    analwords = list(analwords.items())
    analwords.sort()
    with open("../LingData/Ks/kanals.txt", 'w', encoding='utf8') as file:
        for kword, anal in analwords:
            print("{};{}".format(kword, anal), file=file)
    unanalwords = list(unanalwords)
    unanalwords.sort()
    with open("../LingData/Ks/kunanals.txt", 'w', encoding='utf8') as file:
        for kword in unanalwords:
            print("{}".format(kword), file=file)
    req = list(req.items())
    req.sort()
    with open("../LingData/Ks/rcf.txt", 'w', encoding='utf8') as file:
        for (r, c), f in req:
            print("{}:{};{}".format(r, c, f), file=file)

    return req, analwords, unanalwords

def proc_source_feats(feats, cls=False):
    fs = FS()
    if feats:
        values = ['as', 'vc']
        if cls:
            values.append('cls')
            values.append('op')
        for feat in values:
            fs[feat] = feats.get(feat, None)
    return fs

def read_dict0(write=True):
    n = 0
    bad = set()
    balo = []
    roots0 = {}
    roots1 = {}
    am_words = {}
    entries0 = {}
    entries1 = {}
    kroots0 = {}
    kroots1 = {}
    with open("../LingData/Ks/v_am2ks2.txt", encoding='utf8') as file:
        for line in file:
            n += 1
            if n % 50 == 0:
                print("{} lines".format(n))
            linesplit = line.split(';')
            am, a_anal, ks = linesplit
            if " አለ" in am:
                continue
            asplit = a_anal.split(':')
            if len(asplit) != 2:
                print("Something wrong in {}".format(linesplit))
            aroot, afeats = a_anal.split(':')
            afeats = FS(afeats)
            aas = afeats.get('as'); avc = afeats.get('vc')
            afeats = ''.join((aas if aas != 'smp' else '', avc if avc != 'smp' else ''))
            ks = ks.strip().split(':')
            k_anal = []
#            print(am)
            for k in ks:
                if "ባሎ" in k or "አበሎ" in k or "ባለን፟ት" in k:
                    balo.append((am, a_anal, k))
#                    k_anal.append(morpho.geez.romanize(k, 'gru', gemination=True))
                else:
                    k_proc = KS.anal_word(k,
                                          init_weight=FS("[tm=prf,sp=3,-rel,-sub]"),
                                          guess=True, preproc=True)
                    if k_proc:
                        k_proc = [(a[0], proc_source_feats(a[1], True)) for a in k_proc]
                        kp = []
                        if len(k_proc) == 1:
                            k_proc0 = k_proc[0]
                            r1 = k_proc0[0]
                            ff = k_proc0[1]
                            c1 = ff['cls']
                            rootclass = r1 + "_" + c1
                            f1 = ''.join(('cs' if ff['vc'].get('cs') else '', 'ps' if ff['vc'].get('ps') else '', ff.get('as') or '', str(ff.get('op')) if ff.get('op') else ''))
                            if rootclass in roots0:
                                roots0[rootclass].add((f1, k))
                            else:
                                roots0[rootclass] = {(f1, k)}
#                            newent = (k, rootclass, f1)
#                            if newent not in roots1:
#                                roots1.append(newent)
                        for root, feats in k_proc:
                            cls = feats.get('cls')
                            rootclass = root + "_" + cls
                            feats = ''.join(('cs' if feats['vc'].get('cs') else '', 'ps' if feats['vc'].get('ps') else '', feats.get('as') or '', str(feats.get('op')) if feats.get('op') else ''))
                            formfeats = "{}:{}".format(k, feats)  # feats.__repr__())
                            if root in roots1:
                                entry = roots1[root]
                                if cls in entry:
                                    entry[cls].add(formfeats)
                                else:
                                    entry[cls] = {formfeats}
                            else:
                                roots1[root] = {cls: {formfeats}}
                            kp.append((rootclass, feats))
                        k_anal.append((k, kp))
                    else:
                        bad.add(k)
            if k_anal:
                if len(k_anal) == 1:
                    # Only one translation
                    entries0[(aroot, afeats)] = k_anal[0]
                else:
                    if aroot in entries1:
                        rootentry = entries1[aroot]
                        if afeats in rootentry:
                            rootentry[afeats] = k_anal
                        else:
                            rootentry[afeats] = k_anal
                    else:
                        entries1[aroot] = {afeats: k_anal}
#                    if aroot in am_words:
#                        rootentry = am_words[aroot]
#                        am_words[aroot][afeats] = am
#                    else:
#                        am_words[aroot] = {afeats: am}
                        
#                entries.append((am, a_anal, k_anal))
    for kroot, kclasses in roots1.items():
        if len(kclasses) == 1:
            # only one class for kroot
            kclass = list(kclasses.keys())[0]
            kroots0["{}_{}".format(kroot, kclass)] = list(kclasses.values())[0]
        else:
            kroots1[kroot] = kclasses
#    roots1.sort()
    roots0 = list(roots0.items())
    roots0.sort()
    roots1 = list(roots1.items())
    roots1.sort()
    entries0 = list(entries0.items())
    entries0.sort()
    entries1 = list(entries1.items())
    entries1.sort()
    kroots0 = list(kroots0.items())
    kroots0.sort()
    kroots1 = list(kroots1.items())
    kroots1.sort()
    if write:
#        with open("../LingData/Ks/am_words.txt", 'w', encoding='utf8') as file:
#            for aroot, adict in am_words.items():
#                print("{};{}".format(aroot, adict), file=file)
        with open("../LingData/Ks/roots0.txt", 'w', encoding='utf8') as file:
            for k, v in roots0:
                print("{};{}".format(k, v), file=file)
        with open("../LingData/Ks/roots1.txt", 'w', encoding='utf8') as file:
            for k, v in roots1:
                print("{};{}".format(k, v), file=file)
        with open("../LingData/Ks/kroots0.txt", 'w', encoding='utf8') as file:
            for k, v in kroots0:
                print("{};{}".format(k, v), file=file)
        with open("../LingData/Ks/v_lex0.txt", 'w', encoding='utf8') as file:
             for (aroot, afeats), k_anal in entries0:
                 print("{}:{};{}:{}".format(aroot, afeats, k_anal[0], k_anal[1]), file=file)
        with open("../LingData/Ks/v_lex1.txt", 'w', encoding='utf8') as file:
             for aroot, aclasses in entries1:
                 print("{};;{}".format(aroot, aclasses), file=file)
    return (entries0, entries1), (kroots0, kroots1) #, (roots1, roots2)

def read_dict1(write=True):
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
            am = am.strip()
            ks = ks.strip()
#            ks = ks.strip().split(':')
            if am.endswith("አለ"):
                multi.append((am, ks))
            else:
                am_proc = AM.anal_word(am,
                                       init_weight=FS("[pos=v,tm=prf,sb=[-p1,-p2],-rel,-acc,ax=None,-sub]"),
                                       guess=False, preproc=True)
                if am_proc:
                    entries.append((am, [(a[0], proc_source_feats(a[1])) for a in am_proc], ks))
                else:
                    bad.append((am, ks))
    if write:
        with open("../LingData/Ks/v_am2ks2.txt", 'w', encoding='utf8') as efile:
            for am, anals, ks in entries:
                print("{};{};{}".format(am, '::'.join([a[0] + ':' + a[1].__repr__() for a in anals]), ks),
                      file=efile)
        with open("../LingData/Ks/v_am2ks_comp.txt", 'w', encoding='utf8') as mfile:
            for am, ks in multi:
                print("{};{}".format(am, ks), file=mfile)
#    return entries, multi
