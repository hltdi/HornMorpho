### Process verbs in canonical form to find root, aspect, and voice

import l3

#l3.load_lang('am', load_morph=True)
#VMORPH = l3.morpho.get_language('am').morphology['v']
#l3.load_lang('eng', load_morph=True)
#ENG = l3.morpho.get_language('eng').morphology['v']
#PAST = l3.morpho.FSSet("[tam=pst]")
#PP = l3.morpho.FSSet("[tam=pp]")

def sort_dict(dct):
    """Convert a dct to a list and sort it."""
    dct = list(dct.items())
    dct.sort()
    return dct

def adj_groups():
    with open("../LingData/am/a_mdt3.txt", encoding='utf8') as f:
        with open("../mainumby/kuaa/languages/eng/grp/a.grp", 'w', encoding='utf8') as o:
            results = {}
            for line in f:
                eng, amh = line.strip().split("||")
                print("*** {}_a ; ^ {}_n 0".format(eng, eng), file=o)
                for a in amh.split(';'):
                    print("->amh {}_a ; 0==0 plr:plr,def:def,poss:poss".format(a), file=o)

def noun_groups():
    with open("../LingData/am/n_mdt3.txt", encoding='utf8') as f:
        with open("../mainumby/kuaa/languages/eng/grp/n.grp", 'w', encoding='utf8') as o:
            results = {}
            for line in f:
                eng, amh = line.strip().split("||")
                print("*** {}_n ; ^ {}_n 0".format(eng, eng), file=o)
                for a in amh.split(';'):
                    print("->amh {}_n ; 0==0 plr:plr,def:def,poss:poss".format(a), file=o)

def verb_groups():
    with open("../LingData/am/v_mdt2.txt", encoding='utf8') as f:
        results = {}
        beresult = {}
        psvresult = {}
        for line in f:
            eng, amh = line.strip().split(" || ")
            if ' ' in eng and eng.startswith('be_v') or eng.startswith('become_v'):
                becomp = eng.split()[-1]
#                # Try to parse becomp as a past participle
#                psvcomp = ENG.analyze(becomp, PP)
                if becomp in beresult:
                    beresult[becomp].add(amh)
                else:
                    beresult[becomp] = {amh}
            if eng in results:
                results[eng].add(amh)
            else:
                results[eng] = {amh}
        results = sort_dict(results)
        beresult = sort_dict(beresult)
        with open("../LingData/am/v0.grp", 'w', encoding='utf8') as g:
            for eng, amh in results:
                print("*** {}".format(eng), file=g)
                for a in amh:
                    print("->amh {}".format(a), file=g)
            for eng, amh in beresult:
                print("*** be_v {} ; ^ {} 1".format(eng, eng), file=g)
                for a in amh:
                    print("->amh {}".format(a), file=g)

def reverse_verbs():
    """Reverse Am->Eng verbs, keeping all English translations with 1 or 2 words."""
    unparse = 0
    with open("../LingData/am/v_mdt1.txt", encoding='utf8') as f:
        with open("../LingData/am/v_mdt2.txt", 'w', encoding='utf8') as o:
            for line in f:
                root, features, english = line.split(" || ")
                # replace commas with semicolons
                english = english.replace(',', ';')
                # separate translations
                for ephrase in english.split(';'):
                    ephrase = ephrase.strip()
                    # Get words in one translation
                    ephrase_words = ephrase.split()
                    if not ephrase_words or len(ephrase_words) > 2:
                        continue
                    # Try to analyze first word, which should be past
                    everb = ephrase_words[0]
                    everb_anal = ENG.analyze(everb, PAST)
                    if everb_anal:
                        # Only use the first one
                        everb_anal = everb_anal[0]
                        stem = everb_anal[0]
#                            print("Stem {} phrase {}".format(stem, ephrase_words))
                        ephrase_words[0] = stem + '_v'
                        print("{} || {}_v{}".format(' '.join(ephrase_words), root, features), file=o)
                    else:
                        unparse += 1
#                        print("Couldn't analyze {}".format(everb))
    return unparse

def anal_mult_verbs():
    results = []
    with open("../LingData/am/v_mdt_mult.txt", encoding='utf8') as f:
        with open("../LingData/am/v_mdt_mult2.txt", 'w', encoding='utf8') as o:
            for line in f:
                amh, eng = line.strip().split(" || ")
                analyses = VMORPH.analyze(amh, "[tm=prf]")
                result1 = []
                for analysis in analyses:
                    root = analysis[0]
                    features = analysis[1]
                    for feat in features:
                        asp = feat.get('as')
                        vc = feat.get('vc')
                    featstring = "[as={},vc={}]".format(asp, vc)
                    result1.append((root, featstring))
                results.append((eng, result1))
                print("{}".format(eng), file=o)
                for result in result1:
                    r = result[0]
                    f = result[1]
                    print("  {} || {}".format(r, f), file=o)
    return results

def anal_unal_verbs():
    mult = []
    unanal = []
    with open("../LingData/am/v_mdt_un.txt", encoding='utf8') as f:
        with open("../LingData/am/v_mdt_un1.txt", 'w', encoding='utf8') as o:
            for line in f:
                amh, eng = line.strip().split(" || ")
                changed = False
                # Adjust orthography
                if '^' in amh:
                    changed = True
                    amh = amh.replace('^', '')
                elif '`' in amh:
                    changed = True
                    amh = amh.replace('`', "'")
                elif 'x' in amh:
                    changed = True
                    amh = amh.replace('x', 'h')
                if not changed:
                    unanal.append(amh)
                    continue
                analyses = VMORPH.analyze(amh, "[tm=prf]")
                if not analyses:
                    unanal.append(amh)
                    continue
                if len(analyses) > 1:
                    mult.append(amh)
                else:
                    analysis = analyses[0]
                    root = analysis[0]
                    features = analysis[1]
                    for feat in features:
                        asp = feat.get('as')
                        vc = feat.get('vc')
                    print("{} || [as={},vc={}] || {}".format(root, asp, vc, eng), file=o)
    return mult, unanal

def anal_verbs():
    unparsed = []
    mult = []
    parsed = []
    count = 0
    with open("../LingData/am/v_mdt0.txt", encoding='utf8') as f:
        for line in f:
            count += 1
            if count % 100 == 0:
                print("Analyzed {} verbs".format(count))
            amh, eng = line.split(" || ")
            eng = eng.strip()
            initfeat="[tm=prf"
            if "[" in amh:
                amh, x, specfeat = amh.partition("[")
                specfeat = specfeat[:-1]
                initfeat = initfeat + "," + specfeat
            initfeat = initfeat + "]"
            analysis = VMORPH.analyze(amh, initfeat)
            if not analysis:
                unparsed.append((amh, eng))
            elif len(analysis) > 1:
                mult.append((amh, eng))
            else:
                analysis = analysis[0]
                root = analysis[0]
                features = analysis[1]
                asp = ''; vc = ''
                for feat in features:
                    asp = feat.get('as')
                    vc = feat.get('vc')
                featstring = "[as={},vc={}]".format(asp, vc)
                parsed.append((root, featstring, eng))
    return parsed, unparsed, mult
                
                
