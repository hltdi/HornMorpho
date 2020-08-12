import sys, os
import hm
import hm.morpho.geez.geez as geez

# analyses = {'lay': 'lay'}

DIR = 'hm/languages/Am/Data/martha_out'

AM = geez.read_conv("hm/morpho/geez/am_conv_sera.txt")

def geezify(string):
    return geez.sera2geez(AM[1], string)

def get_unambig(directory, outfile=None):
    infiles = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('txt')]
    unambig = set()
    words = set()
    for infile in infiles:
        get_unambig1(infile, unambig, words, count=0)
    print("{} words, {} unambiguous words".format(len(words), len(unambig)))
    if outfile:
        # Geezify and sort the words
        unambig = list(unambig)
        for i, u in enumerate(unambig):
            unambig[i] = geezify(u)
        unambig.sort()
        with open(outfile, 'w', encoding='utf8') as o:
            for u in unambig:
                print(u, file=o)
    else:
        return unambig

def get_unambig1(infile, unambig, words, count=0):
    print("Finding unambiguous words in {}".format(infile))
    print(" Current length of unambig: {}".format(len(unambig)))
#    unambig = unambig or []
    word = None
    anals = []
    with open(infile, encoding='utf-8') as inf:
        for line in inf:
            # Blank lines signal the end of word analyses
            if not line.strip():
                if word:
                    if not anals:
                        # Unanalyzed word
                        continue
                    if len(anals) == 1:
                        unambig.add(word)
#                        unambig.append((word, anals[0][0], anals[0][1]))
                word = None
                anals = []
                continue
            if line[0] == '-':
                word = line.split()[-1]
                words.add(word)
            elif ' ' in line.strip():
                # Analyzed word
                root, anal = line.split()
#                anal = FS(anal)
                anals.append((root, anal))

def FS(string):
#    print('Making FS from', string)
    return hm.morpho.fs.FeatStruct(string)

def get_stats(directory=None, infiles=None, root_file=None,
              root_out=None, fv_out=None,
              root_feats=None, feats=None):
    '''root_feats is a list of names of features that are to be combined with roots for
    stats.
    '''
    if not infiles:
        if not directory:
            directory = DIR
        infiles = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('txt')]
    feats = feats or []
    root_dct = {}
    word_dct = {}
    dis_dct = {}
    feat_dct = {}
    val_dct = {}
    # distinct words for unknown roots
    unknown_dct = {}
    tokens = 0
    nunanal = 0
    nunambig = 0
    nambig = 0
    roots = []
    # get roots
    if root_file:
        with open(root_file, encoding='utf-8') as inf:
            for line in inf:
                if line.strip():
                    roots.append(line.split()[0].strip())
                    
    for infile in infiles:
        tok, unan, amb, unamb = get_stats1(infile, root_dct=root_dct, word_dct=word_dct, dis_dct=dis_dct,
                                           feat_dct=feat_dct, val_dct=val_dct,
                                           root_feats=root_feats,
                                           feats=feats, roots=roots,
                                           unknown_dct=unknown_dct)
        tokens += tok
        nunanal += unan
        nambig += amb
        nunambig += unamb
    print('Tokens {}, unanalyzed {}, ambiguous {}, unambiguous {}'.format(tokens, nunanal, nambig, nunambig))
    if root_out:
        write_roots(root_dct, word_dct, dis_dct, unknown_dct, root_out, tokens)
    if fv_out:
        write_feats(feat_dct, val_dct, fv_out)
    return root_dct, word_dct, dis_dct, feat_dct, val_dct, unknown_dct

def write_roots(root_dct, word_dct, dis_dct, unknown_dct, outfile, tokens):
    print('Writing roots in', outfile)
    word_freq_thresh = tokens * 0.00002
    with open(outfile, 'w', encoding='utf-8') as outf:
        print('{', file=outf)
        for root, freq in root_dct.items():
            word_freq = word_dct.get(root, 0)
            dis_freq = dis_dct.get(root, 0)
            if freq > 2 or word_freq > word_freq_thresh:
                real_root = root.split('+')[0]
                if real_root in unknown_dct and len(unknown_dct[real_root]) < 2:
#                    print('Unknown root', real_root, 'has only one word')
                    continue
                print('"{}": {},'.format(root, freq + word_freq), file=outf)
        for root, freq in word_dct.items():
            if root not in root_dct:
                dis_freq = dis_dct.get(root, 0)
                if freq > 1:
                    print('"{}": {},'.format(root, freq), file=outf)
                    
        print('}', file=outf)

def write_feats(feat_dct, val_dct, outfile):
    print('Writing feats in', outfile)
    with open(outfile, 'w', encoding='utf-8') as outf:
        print('{', file=outf)
        for feat, feat_freq in feat_dct.items():
            vals = val_dct[feat]
            print('"{}":'.format(feat), file=outf)
            print(' {', file=outf)
            for val, val_freq in vals.items():
                freq = val_freq / feat_freq
                if val in (True, False, None):
                    print(' {}: {},'.format(val, freq), file=outf)
                else:
                    print(' "{}": {},'.format(val, freq), file=outf)
            print(' },', file=outf)
        print('}', file=outf)

def read_roots(root_file):
    with open(root_file, encoding='utf-8') as inf:
        return eval(inf.read())

def feat_name(values):
    if any(values):
        return '+'.join(values)
    else:
        return ''

def rv_name(root, value):
    if value:
        return root + '+' + value
    else:
        return root

def root_fv(anals, root_feats):
    roots = [x[0] for x in anals]
    values = [feat_name([x[1].get(f, '') for f in root_feats]) for x in anals]
    return [rv_name(r, v) for r, v in zip(roots, values)]

def get_fv(feats, anal):
    a = anal
    for f in feats:
        if f in a:
            a = a.get(f)
        else:
            return 'nothing'
    return a
        
def get_stats1(infile, root_dct=None, word_dct=None, dis_dct=None,
               feat_dct=None, val_dct=None,
               tokens=0, nunanal=0, nunambig=0, nambig=0,
               root_feats=None,
               feats=None,
               roots=None,
               unknown_dct=None):
    print('Getting statistics from', infile)
    feats = feats or []
    roots = roots or []
    if root_dct is None:
        root_dct = {}
    if word_dct is None:
        word_dct = {}
    if dis_dct is None:
        dis_dct = {}
    if feat_dct and feats:
        feat_dct = {}
        val_dct = {}
    if unknown_dct is None:
        unknown_dct = {}
    word = None
    anals = []
    tokens = 0
    nunanal = 0
    nunambig = 0
    nambig = 0
    with open(infile, encoding='utf-8') as inf:
        for line in inf:
            # Blank lines signal the end of word analyses
            if not line.strip():
                tokens += 1
                if word:
                    if not anals:
                        nunanal += 1
                        # Unanalyzed word
                        word_dct[word] = word_dct.get(word, 0) + 1
                    else:
                        ## roots
                        rts = [x[0] for x in anals]
                        known_roots = [(not roots or r in roots) for r in rts]
                        if root_feats:
                            rv = root_fv(anals, root_feats)
                        else:
                            rv = rts
                        rv = set(rv)
#                        print('word', word, 'rv', rv)
                        if len(rv) == 1:
                            nunambig += 1
                            # Unambiguous analyzed word
                            if not known_roots[0]:
                                rt = rts[0]
                                unknown_dct[rt] = unknown_dct.get(rt, set()).union({word})
                            root = list(rv)[0]
                            root_dct[root] = root_dct.get(root, 0) + 1
                        else:
                            nambig += 1
                            # Ambiguous analyzed word
                            dis_dct[word] = dis_dct.get(word, 0.0) + 1/len(rv)
                        ## grams
                        if len(anals) == 1 and feats:
                            # only count unambiguous cases
                            an = anals[0][1]
                            for f in feats:
                                anal_v = get_fv(f, an)
                                if anal_v != 'nothing':
                                    feat_name = '+'.join(f)
                                    feat_dct[feat_name] = feat_dct.get(feat_name, 0) + 1
                                    if feat_name not in val_dct:
                                        val_dct[feat_name] = {}
                                    val_dct[feat_name][anal_v] = val_dct[feat_name].get(anal_v, 0) + 1
                    anals = []
                line = line.strip()
                continue
            if line[0] == '-':
                word = line.split()[-1]
            elif ' ' in line.strip():
                # Analyzed word
                root, anal, freq = line.split()
                anal = FS(anal)
                anals.append((root, anal))
                
#    print('Tokens {}, unanalyzed {}, ambiguous {}, unambiguous {}'.format(tokens, nunanal, nambig, nunambig))
    return tokens, nunanal, nambig, nunambig

def dict2sortlist(dct):
    l = list(dct.items())
    l.sort(key=lambda x: x[1])
    return l

#a, b, c, d, e, f = get_stats(
#    infiles=['hm/Data/Am/martha_out/out_martha_bigtext0.txt'],
#                             root_feats=['vc', 'as'],
#                             feats=[['poss', 'expl'], ['cnj'], ['cj1'], ['cj2'], ['pp'], ['rel']],
#                             root_file='roots.txt',
#                             root_out='hm/Data/Am/roots_out.txt',
#                             fv_out='hm/Data/Am/feats_out.txt'
#                             )

