"""
Analyze a list of Amharic words in a file.
Project/Morphology/am_anal.py
"""

from langs import *
import time
import re
import os

##AMV = get_pos('am', 'v', load_morph=True)
##AMN = get_pos('am', 'n', load_morph=True)
##AMm = AMV.morphology
##AM = AMm.language

#IN = 'hm/Data/Am/crawl.txt'
#OUT_KNOWN = 'hm/Data/Am/crawl_known.txt'
#OUT_NOVEL = 'hm/Data/Am/crawl_novel.txt'
#OUT_UNK = 'hm/Data/Am/crawl_unk.txt'
       
def proc_anal(anal):
    return [[a[0], [AM.analysis2dict(g) for g in a[1]]] for a in anal]

def anal_known(word):
    return AMN.anal(word, guess=False, preproc=False) or AMV.anal(word, guess=False, preproc=False)

def anal_novel(word):
    return AMN.anal(word, guess=True, preproc=False) + AMV.anal(word, guess=False, preproc=False)

def anal_words(infile=IN, out_known=OUT_KNOWN, out_novel=OUT_NOVEL, out_unk=OUT_UNK,
               start=0, nlines=50000):
    t1 = time.time()
    with open(infile, 'r', encoding='utf-8') as infile, \
         open(out_known, 'a', encoding='utf-8') as out_known,\
         open(out_novel, 'a', encoding='utf-8') as out_novel,\
         open(out_unk, 'a', encoding='utf-8') as out_unk:
        # Each line is a word and a count
        lines = infile.readlines()
        if start or nlines:
            lines = lines[start:start+nlines]
        nlines = 0
        total_lines = len(lines)
        last_line = start + total_lines
        for line in lines:
            nlines += 1
            count, word = line.split()
            word = AM.preproc(word)
            if AMm.is_word(word) or word in AMm.analyzed:
                continue
            count = int(count)
            # Known analyses
            known = anal_known(word)
            if known:
                print([word, count, proc_anal(known)], file=out_known)
            else:
                novel = anal_novel(word)
                if novel:
                    print([word, count, proc_anal(novel)], file=out_novel)
                else:
                    print([word, count], file=out_unk)
            if nlines % 5000 == 0:
                print('Analyzed', nlines, 'words')
    print('Analysis took %0.1f seconds' % (time.time()-t1,))

def count_anals(infile):
    multroots = 0
    multanals = 0
    n = 0
    with open(infile, encoding='utf-8') as inf:
        n += 1
        for line in inf:
            evaled = eval(line)
            anals = evaled[2]
            if len(anals) > 1:
                multroots += 1
            for root, anal in anals:
                if len(anal) > 1:
                    multanals += 1
    return n, multroots, multanals

# This needs to be modified to separate known and novel analyses into
# different files
##def raw_anal(infile=IN[0], start=0, nlines=0):
##    t1 = time.time()
##    out_known = infile[-4] + '_known.txt'
##    out_novel = infile[-4] + '_novel.txt'
##    infile = open(infile, 'r', encoding='utf-8')
##    out_novel = open(out_novel, 'a', encoding='utf-8')
##    out_known = open(out_known, 'a', encoding='utf-8')
##    # Each line is a word and a count
##    lines = infile.readlines()
##    if start or nlines:
##        lines = lines[start:start+nlines]
##    nlines = 0
##    total_lines = len(lines)
##    last_line = start + total_lines
##    for line in lines:
##        nlines += 1
##        if nlines % 100 == 0:
##            print('Analyzed', nlines, 'words')
##        # Separate punctuation from words
##        line = TI.morphology.sep_punc(line)
##        # Segment into words
##        word, count = line.split()
##        count = int(count)
##        # Ignore "trivial" analysis
##        if word not in nonvbs and not TI.morphology.trivial_anal(word):
##            form = TI.preproc(word)
##            analyses = TI.anal_word(form, fsts=None, guess=True, simplified=False,
##                                    root=True, stem=False, citation=False, gram=True,
##                                    preproc=False, postproc=False, only_anal=True)
##            if analyses:
##                anal_string = '- ' + line
##                n_analyses = 0
##                for analysis in analyses:
##                    pos = analysis[0]
##                    root = analysis[1]
##                    if root not in ["'y", "al_e"]:
##                        n_analyses += 1
##                        root = root.replace("'", "!")
##                        if '?' in pos:
##                            root = '?' + root
##                        anal = analysis[-1]
##                        anal_string += '("' + root + '", ' + TI.analysis2dict(anal, ignore=['sub', 'pos']).__repr__() + ')\n'
###                    outfile.write('("' + root + '", ' + TI.analysis2dict(anal, ignore=['sub', 'pos']).__repr__() + ')\n')
##                if n_analyses:
##                    outfile.write(anal_string)
##    print('Analysis took %0.1f seconds' % (time.time()-t1,))
##    infile.close()
##    outfile.close()
##    in_nonvb.close()

##def proc_non_vb(infile=NON_VB, outfile=NON_VB_OUT):
##    infile = open(infile , 'r', encoding='utf8')
##    outfile = open(outfile, 'w', encoding='utf8')
##    for line in infile:
##        line = line.strip()
##        if ' ' not in line:
##            outfile.write(line + '\n')
##    infile.close()
##    outfile.close()

##def fix_quotes(infile=OUT):
##    inf=open(infile, 'r')
##    outf=open(infile[:-4]+'fixed.txt', 'w')
##    for line in inf:
##        if line[0] == '-':
##            outf.write(line)
##        else:
##            start, sep, end = line.partition("', ")
##            preparen, root = start.split("('")
##            if "'" in root:
##                root_repl = root.replace("'", "!")
##                line = line.replace(root, root_repl, 1)
##            outf.write(line)
##    inf.close()
##    outf.close()

##def combine_anals(infile=ANAL, outfile_known=ROOT_K, outfile_unknown=ROOT_U):
##    infile = open(infile, 'r', encoding='utf8')
##    outfile_k = open(outfile_known, 'w', encoding='utf8')
##    outfile_u = open(outfile_unknown, 'w', encoding='utf8')
##    roots = {}
##    word = ''
##    count = 0
##    for line in infile:
##        if line[0] == '-':
##            line = line.split()
##            word = line[1]
##            count = line[2]
##        elif word:
##            # This is an analysis
##            root, anal = eval(line)
##            if root in roots:
##                if word in roots[root]:
##                    roots[root][word].append(anal)
##                else:
##                    roots[root][word] = [count, anal]
##            else:
##                roots[root] = {word: [count, anal]}
###    print('Ignored', ignored, 'non-verbs')
##    for root, anals in roots.items():
##        if '?' in root:
##            out = outfile_u
##        else:
##            out = outfile_k
##        out.write('- ' + root + '\n')
##        for word, anal in anals.items():
##            out.write('  ' + word + ' ' + anal[0] + '\n')
##            for a in anal[1:]:
##                out.write('  ' + a.__repr__() + '\n')
##    infile.close()
##    outfile_k.close()
##    outfile_u.close()

##def combine_anals(infile, outfile):
##    infile = open(infile, 'r', encoding='utf8')
##    out = open(outfile, 'w', encoding='utf8')
##    roots = {}
##    word = ''
##    count = 0
##    for line in infile:
##        if line[0] == '-':
##            line = line.split()
##            word = line[1]
###            count = line[2]
##        elif word:
##            # This is an analysis
##            root, anal = eval(line)
##            if root in roots:
##                if word in roots[root]:
##                    roots[root][word].append(anal)
##                else:
##                    roots[root][word] = [anal]
##            else:
##                roots[root] = {word: [anal]}
##    for root, anals in roots.items():
###        out.write('- ' + root + '\n')
##        out.write(root + ':\n')
##        for word, anal in anals.items():
##            out.write('  ' + word + ':\n')
##            for a in anal:
##                out.write('  - ' + a.__repr__() + '\n')
##    infile.close()
##    out.close()

##def elim_a_gem(infile=ROOT_U):
##    inf = open(infile, 'r', encoding='utf8')
##    outf = open(infile + 'fixed', 'w', encoding='utf8')
##    root = ''
##    elim = 0
##    for line in inf:
##        if line[0] == '-':
##            root = line.split()[-1]
##            if '_' in root and root[2] == 'a' or root[3] == 'a':
###                print('Ignoring', root)
##                elim += 1
##                root = ''
##            else:
##                outf.write(line.replace('?', ''))
##        elif root:
##            outf.write(line)
##    inf.close()
##    outf.close()
##    print('Eliminated', elim)
##
##def elim_ww(infile=ROOT_U):
##    '''Get rid of roots with sequences of w and labialized consonant or w+w.'''
##    inf = open(infile,  'r', encoding='utf8')
##    outf = open(infile + 'fixed', 'w', encoding='utf8')
##    root = ''
##    elim = 0
##    kept = 0
##    for line in inf:
##        if line[0] == '-':
##            root = line.split()[-1]
##            if 'ww' in root or 'Ww' in root:
###                print('Ignoring', root)
##                elim += 1
##                root = ''
##            else:
##                kept += 1
##                outf.write(line.replace('?', ''))
##        elif root:
##            outf.write(line)
##    inf.close()
##    outf.close()
##    print('Eliminated', elim, 'kept', kept)

##def read_root_dict(infile=ROOT_K):
##    infile = open(infile, 'r', encoding='utf8')
##    roots = {}
##    root = ''
##    word = ''
##    for line in infile:
##        if '-' in line[:5]:
##            # an analysis
##            roots[root][word].append(eval(line.replace(' - ', '')))
##        elif ' ' in line[:2]:
##            # word
##            word = line.strip().replace(":", '')
##            roots[root][word] = []
##        else:
##            # new root
##            root = line.strip().replace(':', '')
##            roots[root] = {}
####        if line[0] == '-':
####            # new root
####            root = line.split()[-1]
####            roots[root] = {}
####        elif line.split()[-1].isdigit():
####            # word and count
####            word = line.split()[0]
####            roots[root][word] = []
####        else:
####            # an analysis
####            roots[root][word].append(eval(line))
##    infile.close()
##    return roots
##
##RD_K = read_root_dict()
##RD_U = read_root_dict(ROOT_U)
##RD = {'known': RD_K, 'novel': RD_U}

##def clean_up_novel():
##    outfile = open('l3/Data/Ti/known_it.txt', 'w', encoding='utf-8')
##    novel = set()
##    for anals in RD_U.values():
##        for word in anals.keys():
##            novel.add(word)
##    print('Found', len(novel), 'novel words')
##    count = 0
##    analyzed = 0
##    analyzed_words = []
##    for word in novel:
##        form = TI.preproc(word)
##        analyses = TI.anal_word(form, fsts=None, guess=False, simplified=False,
##                                root=True, stem=False, citation=False, gram=True,
##                                preproc=False, postproc=False, only_anal=True)
##        if analyses:
##            anal_string = '- ' + word + '\n'
##            for analysis in analyses:
##                pos = analysis[0]
##                root = analysis[1]
##                root = root.replace("'", "!")
##                anal = analysis[-1]
##                string += '("' + root + '", ' + TI.analysis2dict(anal, ignore=['sub', 'pos']).__repr__() + ')\n'
###            print('Analyzed', form)
##            analyzed += 1
##            outfile.write(anal_string)
##            analyzed_words.append(word)
##        count += 1
##        if count % 2000 == 0:
##            print('Considered', count, 'words')
##    print('Analyzed', analyzed, 'new words')
##    outfile.close()
##    return analyzed_words

# KNOWN_IT = clean_up_novel()

##def clean_up_anal():
##    analin = open(ANAL, encoding='utf-8')
##    analout = open('l3/Data/Ti/anal_cleaned.txt', 'w', encoding='utf-8')
##    word = ''
##    for line in analin:
##        if line[0] == '-':
##            split_line = line.split()
##            word = split_line[1]
##            if word in KNOWN_IT:
##                word = ''
##                continue
##            else:
##                analout.write(line)
##        elif word:
##            # An analysis for a word not in KNOWN_IT
##            analout.write(line)
##    analin.close()
##    analout.close()
##
##def reanal_novel():
##    outfile = open('l3/Data/Ti/novel_anal.txt', 'w', encoding='utf-8')
##    novel = set()
##    for anals in RD_U.values():
##        for word in anals.keys():
##            novel.add(word)
##    print('Found', len(novel), 'novel words')
##    novel = novel.difference(KNOWN_IT)
##    print('Analyzing', len(novel), 'novel words')
##    count = 0
##    for word in novel:
##        form = TI.preproc(word)
##        analyses = TI.morphology['v'].anal(form, guess=True)
##        if analyses:
##            analyses = TI.proc_anal(form, analyses, 'v', show_root=True,
##                                    citation=False, stem=False, simplified=False,
##                                    guess=True, postproc=False, gram=True)
##            anal_string = '- ' + word + '\n'
##            for analysis in analyses:
##                pos = analysis[0]
##                root = analysis[1]
##                root = root.replace("'", "!")
##                anal = analysis[-1]
##                anal_string += '("' + root + '", ' + TI.analysis2dict(anal, ignore=['sub', 'pos']).__repr__() + ')\n'
##            outfile.write(anal_string)
##        count += 1
##        if count % 1000 == 0:
##            print('Analyzed', count, 'words')
##    outfile.close()
##
##def separate_known():
##    infile = open(ANAL, encoding='utf-8')
##    outfile = open('l3/Data/Ti/known_anal.txt', 'w', encoding='utf-8')
##    wordline = ''
##    known = 0
##    for line in infile:
##        if line[0] == '-':
##            # A word
##            wordline = line
##        elif '?' in line:
##            # A guessed analysis
##            wordline = ''
##        elif wordline:
##            outfile.write(wordline)
##            known += 1
##            outfile.write(line)
##            # Don't repeat the word line for other analyses
##            wordline = ''
##        else:
##            # Just print the analysis
##            outfile.write(line)
##    print('Found', known, 'words')
##    outfile.close()

##def get_prob_dict():
##    return dict([(line.split()[0], float(line.split()[1])) for line in open(ROOT_PROBS['novel'])])
##
##def filter_roots_by_prob():
##    probs = get_prob_dict()
##    filter_out = open(FILTERED['novel'], 'w', encoding='utf8')
##    eliminated = 0
##    for root, entries in RD_U.items():
##        prob = probs.get(root.replace('?', ''), 100.0)
##        if prob < 50.0:
##            filter_out.write('- ' + root + '\n')
##            filter_out.write(entries.__repr__() + '\n')
##        else:
##            eliminated += 1
##    filter_out.close()
##    print('Eliminated', eliminated)
##
##def agr2str(agr):
##    if not agr or agr.get('xpl') == False or agr.get('prp'):
##        return ''
##    s = ''
##    if agr.get('p1'):
##        s += '1'
##    elif agr.get('p2'):
##        s += '2'
##    else:
##        s += '3'
##    if agr.get('fem'):
##        s += 'f'
##    elif '1' not in s:
##        s += 'm'
##    if agr.get('plr'):
##        s += 'p'
##    else:
##        s += 's'
##    return s
##    
##def get_competitors(infile=ANAL_NOVEL): #, non_verb=NON_VB_OUT):
##    infile = open(infile, 'r', encoding='utf8')
##    probs = get_prob_dict()
##    word_compets = {}
##    word = ''
##    for line in infile:
##        if line[0] == '-':
##            line = line.split()
##            word = line[1]
##            word_compets[word] = set()
##        elif word:
##            # This is an analysis
##            root, anal = eval(line)
###            if '?' in root:
##            # Ignore roots with low probability
##            prob = probs.get(root)
##            # Ignore roots that occur rarely
##            if prob < 50 and len(RD_U[root]) > 9:
##                word_compets[word].add(root)
##    # Get rid of all of the words with only one item
##    delete = []
##    for word, compets in word_compets.items():
##        if len(compets) <= 1:
##            delete.append(word)
##    for word in delete:
##        del word_compets[word]
###    print('Ignored', ignored, 'non-verbs')
##    infile.close()
##    return list([set(roots) for roots in word_compets.values()])

##def get_competitors(infile=ANAL): #, non_verb=NON_VB_OUT):
##    infile = open(infile, 'r', encoding='utf8')
##    probs = get_prob_dict()
##    word_compets = {}
##    word = ''
##    for line in infile:
##        if line[0] == '-':
##            line = line.split()
##            word = line[1]
##            word_compets[word] = set()
##        elif word:
##            # This is an analysis
##            root, anal = eval(line)
##            if '?' in root:
##                # Ignore roots with low probability
##                prob = probs.get(root.replace('?', ''))
##                # Ignore roots that occur rarely
##                if prob < 50 and len(RD_U[root]) > 9:
##                    word_compets[word].add(root)
##    # Get rid of all of the words with only one item
##    delete = []
##    for word, compets in word_compets.items():
##        if len(compets) <= 1:
##            delete.append(word)
##    for word in delete:
##        del word_compets[word]
###    print('Ignored', ignored, 'non-verbs')
##    infile.close()
##    return list([set(roots) for roots in word_compets.values()])

##def roots_compete(root1, root2, compets=None):
##    '''Number of competitor sets containing both root1 and root2.'''
##    compets = compets or get_competitors()
##    return len([c for c in compets if root1 in c and root2 in c])

##def reduce_competsets(roots, compets):
##    rootset = set(roots.keys())
##    elim = 0
##    for index, cset in enumerate(compets):
##        inters = cset & rootset
##        if inters:
##            compets[index] = inters
##        else:
##            elim += 1
##            compets.remove(cset)
##    print('Eliminated', elim)

##def elim_dup_csets(compets):
##    # First make all elements of compets frozen
##    for index, cset in enumerate(compets):
##        compets[index] = frozenset(cset)
##    return list(set(compets))
##    elim = 0
##    for index, cset1 in enumerate(compets[:-1]):
##        for cset2 in compets[index+1:]:
##            if cset1 == cset2:
##                compets.remove(cset1)
##                elim += 1
###        if index % 100 == 0:
###            print('Did', index)
##    print('Eliminated', elim)

##def get_root_compet_sets1(root, compets=None):
##    '''All competitor sets containing root.'''
##    compets = compets or get_competitors()
##    return [c for c in compets if root in c]
##
##def get_root_compet_sets(roots, compets=None):
##    compets = compets or get_competitors()
##    sets = []
##    for i1, root1 in enumerate(roots[:-1]):
##        set1 = set()
##        for root2 in roots[i1+1:]:
##            if roots_compete(root1, root2, compets):
##                set1.add(root2)
###                sets.append([root1, root2])
##        if set1:
##            set1.add(root1)
##            sets.append(set1)
##        if i1 % 100 == 0:
##            print('Handled', i1, 'root competsets')
##    return sets
##
##def filt_roots_by_compets(roots, compets, write=False):
##    '''Eliminate losers from each compet set.'''
##    elim = set()
##    for cset in compets:
##        best, best_prob = None, 100.0
##        for r in cset:
##            prob = roots[r][3]
##            if prob < best_prob:
##                best, best_prob = r, prob
##        # Eliminate all but best
##        for r in cset:
##            if r != best:
##                elim.add(r)
##    print('Eliminating', len(elim), 'by probability')
##    for r in elim:
##        del roots[r]
##    if write:
##        outf = open('l3/Data/Ti/roots_final.txt', 'w')
##        for r in roots.items():
##            outf.write(r.__repr__() + '\n')
##        outf.close()

##def merge_root_compets(compets):
##    '''Compets a list of sets of roots.'''
##    sets = []
##    # Indices of sets already merged
##    merged = []
##    for index1, c1 in enumerate(compets[:-1]):
##        if index1 in merged:
##            continue
##        merged1 = c1.copy()
##        for n, c2 in enumerate(compets[index1+1:]):
##            index2 = index1 + n + 1
##            merged2 = merged1 & c2
##            if merged2:
##                # Some element of c2 is in merged1
##                merged1.update(c2)
##                # Save the index of c2 to delete it later
##                merged.append(index2)
##        if merged1 != c1:
##            # Something was added
##            sets.append(merged1)
##        if index1 % 50 == 0:
##            print('Handled', index1)
##    return sets

##def get_sbj_counts(kind):
##    sbjs = open(ARGS['sbj'][kind])
##    counts = {}
##    for line in sbjs:
##        count = len(eval(line)[1])
##        counts[count] = counts.get(count, 0) + 1
##    sbjs.close()
##    return counts
##    
##def get_obj_counts(kind):
##    objs = open(ARGS['obj'][kind])
##    counts = {}
##    for line in objs:
##        count = len(eval(line)[1])
##        counts[count] = counts.get(count, 0) + 1
##    objs.close()
##    return counts
##
##def get_arg_counts(kind):
##    sbjs = DATA[kind]['sbjs']
##    objs = DATA[kind]['objs']
##    counts = {}
##    for word, sb in sbjs.items():
##        sbn = len(sb)
##        obn = len(objs.get(word, []))
##        n = sbn + obn
##        counts[n] = counts.get(n, 0) + 1
##    return counts
##
##def get_data(kind, write=False):
##    if write:
##        outf = open(os.path.join('l3/Data/Ti/', kind + '_data.txt'), 'w')
##    sbjs = DATA[kind]['sbjs']
##    objs = DATA[kind]['objs']
##    ders = DATA[kind]['ders']
##    nonders = DATA[kind]['nonders']
##    if kind == 'novel':
##        probs = get_prob_dict()
##    data = {}
##    for word, sb in sbjs.items():
##        argn = len(sb) + len(objs.get(word, []))
##        nonder = nonders.get(word, [[],[0, 0]])
##        tamn = len([x for x in nonder[0] if x])
##        reln = nonder[1][0]
##        d = [tamn, argn, reln]
##        if kind == 'novel':
##            d.append(probs.get(word, 100.0))
##        data[word] = d
##    if write:
##        for item in data.items():
##            outf.write(item.__repr__() + '\n')
##        outf.close()
##    return data
##
##def filter_novel(root_data, write=False):
##    dct = {}
##    elim = 0
##    elims = [0, 0, 0]
##    if write:
##        outfile = open('l3/Data/Ti/filtered_novel.txt', 'w')
##    for root, data in root_data.items():
##        ntam = data[0]
##        narg = data[1]
##        rel = data[2]
##        prob = data[3]
##        elimq = False
##        if ntam < 3:
##            elimq = True
##            elims[0] += 1
###            print(root, 'lacks TAM variability')
##        if rel < 7:
##            elimq = True
##            elims[1] += 1
###            print(root, 'lacks relativization variability')
##        if narg < 5:
##            elimq = True
##            elims[2] += 1
###            print(root, 'lacks arg variability')
##        if elimq:
##            elim += 1
##        else:
##            dct[root] = data
##    if write:
##        for item in dct.items():
##            outfile.write(item.__repr__() + '\n')
##        outfile.close()
##    print('Eliminated', elim, elims)
##    return dct

#def group_compets(compets):
#    '''Convert a dict of word: {root_competitors} to a dict
#    of root: {root_competitors}'''
#    compets = {}
#    for word, roots in compets.items():
#        # roots a set of strings
#        for root1 in roots:
#            for root2 in roots:
#                if root1 != root2:
#                    if root1 not in compets:
#                        compets[root1] = {root2: 1}
#                    elif root2 in compets[root1]:
#                        compets[root1][root2] += 1
#                    else:
#                        compets[root1][root2] = 1

##def get_dercat(dct):
##    vc = dct.get('vc')
##    asp = dct.get('as')
##    if vc == 'ps':
##        if asp == 'smp':
##            return 'psv'
##        elif asp == 'rc':
##            return 'recip1'
##        else:
##            return 'recip2'
##    elif vc == 'tr':
##        if asp == 'smp':
##            return 'csv'
##        elif asp == 'rc':
##            return 'csv-recip1'
##        else:
##            return 'csv-recip2'
##    elif asp == 'it':
##        return 'iter'
##    else:
##        return 'smp'
##        
##def percent(num, den):
##    return int((float(num)/den) * 100)
##    
##def write_ders(root_type, write=False):
##    '''Write derivations for root type in file.'''
##    roots = RD[root_type]
##    if root_type == 'novel':
##        probs = get_prob_dict()
##    filename = 'ders_' + root_type + '.txt'
##    outfile = 'l3/Data/Ti/' + filename
##    all_ders = {}
##    for root, entries in roots.items():
##        if root_type == 'novel' and probs[root] > 50:
##            continue
##        n, ders = get_ders(None, root, entries)
##        if n > 14:
##            all_ders[root] = tuple([perc for d,  perc in ders])
##    # Now write all_ders in outfile
##    if write:
##        outf = open(outfile, 'w')
##        for root_ders in all_ders.items():
##            outf.write(root_ders.__repr__() + '\n')
##        outf.close()
##    return all_ders
##    
##def get_ders(roots, root, entries=None):
##    entries = entries or roots.get(root, {})
##    counts = {}
##    n = 0
##    for word, anals in entries.items():
##        der_dct = {}
##        for anal in anals:
##            der = get_dercat(anal)
##            if der:
##                if der in der_dct:
##                    der_dct[der] += 1
##                else:
##                    der_dct[der] = 1
##        max_der= ''
##        for der, count in der_dct.items():
##            if count >= len(anals) / 2:
##                max_der = der
##                n += 1
##                break
##        if max_der:
##            if max_der in counts:
###                counts[max_arg].append(word)
##                counts[max_der] += 1
##            else:
###                counts[max_arg] = [word]
##                counts[max_der] = 1
###        if ob_dct:
###            counts[word] = (len(anals), ob_dct)
##    ders = dict([(der, percent(count, n)) for der, count in counts.items()])
##    return n, [(der, ders.get(der, 0)) for der in DERS]
##    
##def write_nonders(root_type, write=False):
##    '''Write TAM, polarity, relativization for root type in file.'''
##    roots = RD[root_type]
##    if root_type == 'novel':
##        probs = get_prob_dict()
##    filename = 'nonders_' + root_type + '.txt'
##    outfile = 'l3/Data/Ti/' + filename
##    all_attribs = {}
##    for root, entries in roots.items():
##        if root_type == 'novel' and probs[root] > 50:
##            continue
##        n, tam = get_tam(None, root, entries)
##        if n > 9:
##            all_attribs[root] = [tam]
####            n, neg = get_neg(None, root, entries)
####            all_attribs[root].append(neg)
##            n, rel = get_rel(None, root, entries)
##            all_attribs[root].append(rel)
##    # Now write all_ders in outfile
##    if write:
##        outf = open(outfile, 'w')
##        for root_attribs in all_attribs.items():
##            outf.write(root_attribs.__repr__() + '\n')
##        outf.close()
##    return all_attribs
##
##def write_sbj(root_type, write=False):
##    '''Write percentages of subjects for root type in file.'''
##    roots = RD[root_type]
##    if root_type == 'novel':
##        probs = get_prob_dict()
##    filename = 'sbj_' + root_type + '.txt'
##    outfile = 'l3/Data/Ti/' + filename
##    all_sbj = {}
##    for root, entries in roots.items():
##        if root_type == 'novel' and probs[root] > 50:
##            continue
##        n, args = get_args(roots, root, 'sb')
##        if n > 14:
##            all_sbj[root] = tuple([perc for a, perc in args.items()])
##    # Now write all_ders in outfile
##    if write:
##        outf = open(outfile, 'w')
##        for root_sbjs in all_sbj.items():
##            outf.write(root_sbjs.__repr__() + '\n')
##        outf.close()
##    return all_sbj
##    
##def write_obj(root_type, write=False):
##    '''Write percentages of objects for root type in file.'''
##    roots = RD[root_type]
##    if root_type == 'novel':
##        probs = get_prob_dict()
##    filename = 'obj_' + root_type + '.txt'
##    outfile = 'l3/Data/Ti/' + filename
##    all_obj = {}
##    for root, entries in roots.items():
##        if root_type == 'novel' and probs[root] > 50:
##            continue
##        n, args = get_args(roots, root, 'ob')
##        if n > 14:
##            all_obj[root] = tuple([perc for a, perc in args.items()])
##    # Now write all_ders in outfile
##    if write:
##        outf = open(outfile, 'w')
##        for root_objs in all_obj.items():
##            outf.write(root_objs.__repr__() + '\n')
##        outf.close()
##    return all_obj
##
##def anal_arg(root_type, arg='ob', dercat='', write=False):
##    roots = RD[root_type]
##    if root_type == 'novel':
##        probs = get_prob_dict()
##    filename = arg + dercat + '_anal_' + root_type + '.txt'
##    outfile = 'l3/Data/Ti/' + filename
##    all_arg = {}
##    for root, entries in roots.items():
##        if root_type == 'novel' and probs[root] > 50:
##            continue
##        n_words = len(entries)
##        n, args = anal_args(roots, root, arg, dercat=dercat)
##        if n > 9:
##            values = tuple([args.get(png, 0) for png in PNG])
###            all_arg[root] = tuple([perc for a, perc in args.items()])
##            all_arg[root] = values
##        else:
##            all_arg[root] = (0,)
##    # Now write all_ders in outfile
##    if write:
##        outf = open(outfile, 'w')
##        for root_objs in all_arg.items():
##            outf.write(root_objs.__repr__() + '\n')
##        outf.close()
##    return all_arg    
##    
##def get_neg(roots, root, entries=None):
##    entries = entries or roots.get(root, {})
##    counts = {'neg': 0, 'aff': 0}
##    for word, anals in entries.items():
##        neg = 0
##        for anal in anals:
##            neg = anal.get('neg', False)
##            if neg:
##                neg += 1
##        if neg > len(anals) / 2:
##            counts['neg'] += 1
##        else:
##            counts['aff'] += 1
##    n_entries = len(entries)
##    return n_entries, [percent(counts['neg'], n_entries), percent(counts['aff'], n_entries)]
##
##def get_rel(roots, root, entries=None):
##    entries = entries or roots.get(root, {})
##    counts = {'rel': 0, 'nonrel': 0}
##    for word, anals in entries.items():
##        rel = 0
##        for anal in anals:
##            rel = anal.get('rel', False)
##            if rel:
##                rel += 1
##        if rel > len(anals) / 2:
##            counts['rel'] += 1
##        else:
##            counts['nonrel'] += 1
##    n_entries = len(entries)
##    return n_entries, [percent(counts['rel'], n_entries), percent(counts['nonrel'], n_entries)]
##    
##def get_tam(roots, root, entries=None):
##    entries = entries or roots.get(root, {})
##    if not entries:
##        0, None
##    counts = [0,  0,  0,  0]
##    n = 0
##    for word, anals in entries.items():
##        tam = [0,  0,  0,  0]
##        for anal in anals:
##            tam1 = anal.get('tm')
##            if tam1 == 'prf':
##                tam[0] += 1
##            elif tam1 == 'imf':
##                tam[1] += 1
##            elif tam1 == 'j_i':
##                tam[2] += 1
##            else:
##                tam[3] += 1
##        max_tam = -1
##        for index, t in enumerate(tam):
##            if t > len(anals) / 2:
##                max_tam = index
##                break
##        if max_tam >= 0:
##            n += 1
##            counts[max_tam] += 1
##    if n == 0:
##        return 0, None
##    return n, [percent(count, n) for count in counts]
##
##def anal_args(roots, root, arg, dercat=''):
##    # If dercat is not empty, use number satisfying for calculating percentages
##    entries = roots.get(root, {})
##    counts = {}
##    n = 0
##    for word, anals in entries.items():
##        arg_dct = {}
##        for anal in anals:
##            a = agr2str(anal.get(arg))
##            if arg == 'sb' and not a:
##                a = '3ms'
##            der = not dercat or get_dercat(anal) == dercat
##            if der:
##                n += 1
##            if a and der:
##                if a in arg_dct:
##                    arg_dct[a] += 1
##                else:
##                    arg_dct[a] = 1
##        max_arg= ''
##        for ar, count in arg_dct.items():
##            if count > len(anals) / 2:
##                max_arg = ar
##                break
##        if max_arg:
##            n += 1
##            if max_arg in counts:
##                counts[max_arg] += 1
##            else:
##                counts[max_arg] = 1
##    if n:
##        args = dict([(arg, percent(count, n)) for arg, count in counts.items()])
##        return n, args
##    else:
##        return 0, {}
##
##def get_args(roots, root, arg, dercat=''):
##    entries = roots.get(root, {})
##    counts = {}
##    n = 0
##    for word, anals in entries.items():
##        arg_dct = {}
##        for anal in anals:
##            a = agr2str(anal.get(arg))
##            if arg == 'sb' and not a:
##                a = '3ms'
##            der = not dercat or get_dercat(anal) == dercat
##            if a and der:
##                if a in arg_dct:
##                    arg_dct[a] += 1
##                else:
##                    arg_dct[a] = 1
##        max_arg= ''
##        for ar, count in arg_dct.items():
##            if count > len(anals) / 2:
##                max_arg = ar
##                break
##        if max_arg:
##            n += 1
##            if max_arg in counts:
###                counts[max_arg].append(word)
##                counts[max_arg] += 1
##            else:
###                counts[max_arg] = [word]
##                counts[max_arg] = 1
###        if ob_dct:
###            counts[word] = (len(anals), ob_dct)
##    args = dict([(arg, percent(count, n)) for arg, count in counts.items()])
##    return len(entries), args
###    return len(entries), counts
##
##### Derivational and valency categories
##
##def get_smp_psv_roots(kind, write=False):
##    '''Separate roots that appear in simple from those whose base form is passive.'''
##    ders = DATA[kind]['ders']
##    smp = []
##    psv = []
##    for root, ders in ders.items():
##        # Percentage of simple
##        if ders[0] < 10:
##            psv.append((root, ders))
##        else:
##            smp.append((root, ders))
##    if write:
##        outsmp = open('l3/Data/Ti/' + kind + '_smp.txt', 'w')
##        outpsv = open('l3/Data/Ti/' + kind + '_psv.txt', 'w')
##        for rd in smp:
##            outsmp.write(rd.__repr__() + '\n')
##        for rd in psv:
##            outpsv.write(rd.__repr__() + '\n')
##        outsmp.close()
##        outpsv.close()
##    return smp, psv
##
##def get_psv_recip_roots(kind, psv, write=False):
##    real_psv = []
##    recip = []
##    for root, ders in psv:
##        sum_der = sum(ders)
##        if ders[3] > 0.5 * sum_der:
##            recip.append((root, ders))
##        else:
##            real_psv.append((root, ders))
##    if write:
##        outrec = open('l3/Data/Ti/' + kind + '_recip.txt', 'w')
##        outpsv = open('l3/Data/Ti/' + kind + '_psvpsv.txt', 'w')
##        for rd in recip:
##            outrec.write(rd.__repr__() + '\n')
##        for rd in real_psv:
##            outpsv.write(rd.__repr__() + '\n')
##        outrec.close()
##        outpsv.close()
##    return real_psv, recip
##
##def get_intrans(roots, write=False):
##    '''Get known roots within roots that have no passive.'''
##    ders = DATA['known']['ders']
##    intr = []
##    for root in roots:
##        der = ders[root]
##        # Percentage of passive less than 3
##        if der[1] < 3:
##            intr.append((root, der))
##    if write:
##        out = open('l3/Data/Ti/known_intrans.txt', 'w')
##        for rd in intr:
##            out.write(rd.__repr__() + '\n')
##        out.close()
##    return intr
##
##def get_impersonal(sbj_anal):
##    res = []
##    for root, anal in sbj_anal.items():
##        if len(anal) == 1:
##            continue
##        anal_sum = sum(anal)
##        if anal_sum > 0.0 and anal[0] / float(anal_sum) > 0.8:
##            res.append((root, anal))
##    return res
##
##DATA = {'known': {'nonders': write_nonders('known'), 'ders': write_ders('known'),
##                  'sbjs': write_sbj('known'), 'objs': write_obj('known')},
##        'novel': {'nonders': write_nonders('novel'), 'ders': write_ders('novel'),
##                  'sbjs': write_sbj('novel'), 'objs': write_obj('novel')}}
##
##NOVEL_DATA = get_data('novel')
##FILTER_NOVEL = filter_novel(NOVEL_DATA)
##
##novel = open('l3/Data/Ti/novel_data.txt', 'w')
##for d in NOVEL_DATA.items():
##    novel.write(d.__repr__() + '\n')
##novel.close()
##
##COMPETITORS = get_competitors()
##### Eliminate all roots in competition sets that are not in filtered root set
####reduce_competsets(FILTER_NOVEL, COMPETITORS)
##### Eliminate duplicate competition sets
##COMPETITORS = elim_dup_csets(COMPETITORS)
##NOVEL_CSETS = get_root_compet_sets(list(FILTER_NOVEL.keys()), COMPETITORS)
##filt_roots_by_compets(FILTER_NOVEL, NOVEL_CSETS)
##
##KNOWN_SMP, KNOWN_PSV = get_smp_psv_roots('known')

