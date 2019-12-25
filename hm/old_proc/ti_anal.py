"""
This file is part of L3Morpho.

    L3Morpho is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    L3Morpho is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with L3Morpho.  If not, see <http://www.gnu.org/licenses/>.

Author: Michael Gasser <gasser@cs.indiana.edu>
"""

import l3
import time
import re
import os

##l3.load_lang('ti')
##
##TI = l3.morpho.get_language('ti')

#GD1 = {}
#GD2 = {}
#KD = {}
#GWD = {}
#KNOWN = [(KD, 'l3/Data/Ti/ti_kd_saved.txt', ['as','vc'], ['sb','ob'])]
#GUESS = [(GD1, 'l3/Data/Ti/ti_gd1_saved.txt', ['as', 'vc'], ['sb', 'ob']),
#         (GD2, 'l3/Data/Ti/ti_gd2_saved.txt', ['tm']),
#         (GWD, 'l3/Data/Ti/ti_gd3_saved.txt', 'words')]
IN = 'l3/Data/Ti/ti_crawl2.txt'
OUT = 'l3/Data/Ti/anal.txt'
ANAL = 'l3/Data/Ti/anal.txt'
ANAL_KNOWN = 'l3/Data/Ti/known_anal.txt'
ANAL_NOVEL = 'l3/Data/Ti/novel_anal.txt'
N_ANAL = 'l3/Data/Ti/n_anal.txt'
ROOT_K = 'l3/Data/Ti/root_k.txt'
ROOT_U = 'l3/Data/Ti/root_u.txt'
NON_VB = 'l3/Data/Ti/n_adj_adv.txt'
NON_VB_OUT = 'l3/Data/Ti/non_vb.txt'
DERS =  ['smp', 'psv', 'csv', 'recip1', 'recip2'] # 'iter', 'csv-recip1', 'csv-recip2']
ROOT_PROBS = {'known': 'l3/Data/Ti/known_prob.txt',
              'novel': 'l3/Data/Ti/novel_prob.txt'}
FILTERED = {'known': 'l3/Data/Ti/known_filt.txt',
            'novel': 'l3/Data/Ti/novel_filt.txt'}
ARGS = {'sbj': {'known': 'l3/Data/Ti/sbj_known.txt', 'novel': 'l3/Data/Ti/sbj_novel.txt'},
        'obj': {'known': 'l3/Data/Ti/obj_known.txt', 'novel': 'l3/Data/Ti/obj_novel.txt'}}
PNG = ['3ms', '3fs', '3mp', '3fp', '1s', '1p', '2ms', '2fs', '2mp', '2fp']

# This needs to be modified to separate known and novel analyses into
# different files
def raw_anal(infile=IN, outfile=OUT, non_verb=NON_VB_OUT, n_anal=N_ANAL, 
             start=0, nlines=0):
    t1 = time.time()
    infile = open(infile, 'r', encoding='utf-8')
    outfile = open(outfile, 'a', encoding='utf-8')
    in_nonvb = open(non_verb, 'r', encoding='utf8')
    nonvbs = [w.strip() for w in in_nonvb]
    # Each line is a word and a count
    lines = infile.readlines()
    if start or nlines:
        lines = lines[start:start+nlines]
    nlines = 0
    total_lines = len(lines)
    last_line = start + total_lines
    for line in lines:
        nlines += 1
        if nlines % 5000 == 0:
            print('Analyzed', nlines, 'words')
        # Separate punctuation from words
        line = TI.morphology.sep_punc(line)
        # Segment into words
        word, count = line.split()
        count = int(count)
        # Ignore "trivial" analysis
        if word not in nonvbs and not TI.morphology.trivial_anal(word):
            form = TI.preproc(word)
            analyses = TI.anal_word(form, fsts=None, guess=True, simplified=False,
                                    root=True, stem=False, citation=False, gram=True,
                                    preproc=False, postproc=False, only_anal=True)
            if analyses:
                anal_string = '- ' + line
                n_analyses = 0
                for analysis in analyses:
                    pos = analysis[0]
                    root = analysis[1]
                    if root not in ["'y", "al_e"]:
                        n_analyses += 1
                        root = root.replace("'", "!")
                        if '?' in pos:
                            root = '?' + root
                        anal = analysis[-1]
                        anal_string += '("' + root + '", ' + TI.analysis2dict(anal, ignore=['sub', 'pos']).__repr__() + ')\n'
#                    outfile.write('("' + root + '", ' + TI.analysis2dict(anal, ignore=['sub', 'pos']).__repr__() + ')\n')
                if n_analyses:
                    outfile.write(anal_string)
    print('Analysis took %0.1f seconds' % (time.time()-t1,))
    infile.close()
    outfile.close()
    in_nonvb.close()

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

def combine_anals(infile, outfile):
    infile = open(infile, 'r', encoding='utf8')
    out = open(outfile, 'w', encoding='utf8')
    roots = {}
    word = ''
    count = 0
    for line in infile:
        if line[0] == '-':
            line = line.split()
            word = line[1]
#            count = line[2]
        elif word:
            # This is an analysis
            root, anal = eval(line)
            if root in roots:
                if word in roots[root]:
                    roots[root][word].append(anal)
                else:
                    roots[root][word] = [anal]
            else:
                roots[root] = {word: [anal]}
    for root, anals in roots.items():
#        out.write('- ' + root + '\n')
        out.write(root + ':\n')
        for word, anal in anals.items():
            out.write('  ' + word + ':\n')
            for a in anal:
                out.write('  - ' + a.__repr__() + '\n')
    infile.close()
    out.close()

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

def read_root_dict(infile=ROOT_K):
    infile = open(infile, 'r', encoding='utf8')
    roots = {}
    root = ''
    word = ''
    for line in infile:
        if '-' in line[:5]:
            # an analysis
            roots[root][word].append(eval(line.replace(' - ', '')))
        elif ' ' in line[:2]:
            # word
            word = line.strip().replace(":", '')
            roots[root][word] = []
        else:
            # new root
            root = line.strip().replace(':', '')
            roots[root] = {}
##        if line[0] == '-':
##            # new root
##            root = line.split()[-1]
##            roots[root] = {}
##        elif line.split()[-1].isdigit():
##            # word and count
##            word = line.split()[0]
##            roots[root][word] = []
##        else:
##            # an analysis
##            roots[root][word].append(eval(line))
    infile.close()
    return roots

RD_K = read_root_dict()
RD_U = read_root_dict(ROOT_U)
RD = {'known': RD_K, 'novel': RD_U}

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

def get_prob_dict():
    return dict([(line.split()[0], float(line.split()[1])) for line in open(ROOT_PROBS['novel'])])

def filter_roots_by_prob():
    probs = get_prob_dict()
    filter_out = open(FILTERED['novel'], 'w', encoding='utf8')
    eliminated = 0
    for root, entries in RD_U.items():
        prob = probs.get(root.replace('?', ''), 100.0)
        if prob < 50.0:
            filter_out.write('- ' + root + '\n')
            filter_out.write(entries.__repr__() + '\n')
        else:
            eliminated += 1
    filter_out.close()
    print('Eliminated', eliminated)

def agr2str(agr):
    if not agr or agr.get('xpl') == False or agr.get('prp'):
        return ''
    s = ''
    if agr.get('p1'):
        s += '1'
    elif agr.get('p2'):
        s += '2'
    else:
        s += '3'
    if agr.get('fem'):
        s += 'f'
    elif '1' not in s:
        s += 'm'
    if agr.get('plr'):
        s += 'p'
    else:
        s += 's'
    return s
    
def get_competitors(infile=ANAL_NOVEL): #, non_verb=NON_VB_OUT):
    infile = open(infile, 'r', encoding='utf8')
    probs = get_prob_dict()
    word_compets = {}
    word = ''
    for line in infile:
        if line[0] == '-':
            line = line.split()
            word = line[1]
            word_compets[word] = set()
        elif word:
            # This is an analysis
            root, anal = eval(line)
#            if '?' in root:
            # Ignore roots with low probability
            prob = probs.get(root)
            # Ignore roots that occur rarely
            if prob < 50 and len(RD_U[root]) > 9:
                word_compets[word].add(root)
    # Get rid of all of the words with only one item
    delete = []
    for word, compets in word_compets.items():
        if len(compets) <= 1:
            delete.append(word)
    for word in delete:
        del word_compets[word]
#    print('Ignored', ignored, 'non-verbs')
    infile.close()
    return list([set(roots) for roots in word_compets.values()])

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

def roots_compete(root1, root2, compets=None):
    '''Number of competitor sets containing both root1 and root2.'''
    compets = compets or get_competitors()
    return len([c for c in compets if root1 in c and root2 in c])

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

def elim_dup_csets(compets):
    # First make all elements of compets frozen
    for index, cset in enumerate(compets):
        compets[index] = frozenset(cset)
    return list(set(compets))
##    elim = 0
##    for index, cset1 in enumerate(compets[:-1]):
##        for cset2 in compets[index+1:]:
##            if cset1 == cset2:
##                compets.remove(cset1)
##                elim += 1
###        if index % 100 == 0:
###            print('Did', index)
##    print('Eliminated', elim)

def get_root_compet_sets1(root, compets=None):
    '''All competitor sets containing root.'''
    compets = compets or get_competitors()
    return [c for c in compets if root in c]

def get_root_compet_sets(roots, compets=None):
    compets = compets or get_competitors()
    sets = []
    for i1, root1 in enumerate(roots[:-1]):
        set1 = set()
        for root2 in roots[i1+1:]:
            if roots_compete(root1, root2, compets):
                set1.add(root2)
#                sets.append([root1, root2])
        if set1:
            set1.add(root1)
            sets.append(set1)
        if i1 % 100 == 0:
            print('Handled', i1, 'root competsets')
    return sets

def filt_roots_by_compets(roots, compets, write=False):
    '''Eliminate losers from each compet set.'''
    elim = set()
    for cset in compets:
        best, best_prob = None, 100.0
        for r in cset:
            prob = roots[r][3]
            if prob < best_prob:
                best, best_prob = r, prob
        # Eliminate all but best
        for r in cset:
            if r != best:
                elim.add(r)
    print('Eliminating', len(elim), 'by probability')
    for r in elim:
        del roots[r]
    if write:
        outf = open('l3/Data/Ti/roots_final.txt', 'w')
        for r in roots.items():
            outf.write(r.__repr__() + '\n')
        outf.close()

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

def get_sbj_counts(kind):
    sbjs = open(ARGS['sbj'][kind])
    counts = {}
    for line in sbjs:
        count = len(eval(line)[1])
        counts[count] = counts.get(count, 0) + 1
    sbjs.close()
    return counts
    
def get_obj_counts(kind):
    objs = open(ARGS['obj'][kind])
    counts = {}
    for line in objs:
        count = len(eval(line)[1])
        counts[count] = counts.get(count, 0) + 1
    objs.close()
    return counts

def get_arg_counts(kind):
    sbjs = DATA[kind]['sbjs']
    objs = DATA[kind]['objs']
    counts = {}
    for word, sb in sbjs.items():
        sbn = len(sb)
        obn = len(objs.get(word, []))
        n = sbn + obn
        counts[n] = counts.get(n, 0) + 1
    return counts

def get_data(kind, write=False):
    if write:
        outf = open(os.path.join('l3/Data/Ti/', kind + '_data.txt'), 'w')
    sbjs = DATA[kind]['sbjs']
    objs = DATA[kind]['objs']
    ders = DATA[kind]['ders']
    nonders = DATA[kind]['nonders']
    if kind == 'novel':
        probs = get_prob_dict()
    data = {}
    for word, sb in sbjs.items():
        argn = len(sb) + len(objs.get(word, []))
        nonder = nonders.get(word, [[],[0, 0]])
        tamn = len([x for x in nonder[0] if x])
        reln = nonder[1][0]
        d = [tamn, argn, reln]
        if kind == 'novel':
            d.append(probs.get(word, 100.0))
        data[word] = d
    if write:
        for item in data.items():
            outf.write(item.__repr__() + '\n')
        outf.close()
    return data

def filter_novel(root_data, write=False):
    dct = {}
    elim = 0
    elims = [0, 0, 0]
    if write:
        outfile = open('l3/Data/Ti/filtered_novel.txt', 'w')
    for root, data in root_data.items():
        ntam = data[0]
        narg = data[1]
        rel = data[2]
        prob = data[3]
        elimq = False
        if ntam < 3:
            elimq = True
            elims[0] += 1
#            print(root, 'lacks TAM variability')
        if rel < 7:
            elimq = True
            elims[1] += 1
#            print(root, 'lacks relativization variability')
        if narg < 5:
            elimq = True
            elims[2] += 1
#            print(root, 'lacks arg variability')
        if elimq:
            elim += 1
        else:
            dct[root] = data
    if write:
        for item in dct.items():
            outfile.write(item.__repr__() + '\n')
        outfile.close()
    print('Eliminated', elim, elims)
    return dct

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

def get_dercat(dct):
    vc = dct.get('vc')
    asp = dct.get('as')
    if vc == 'ps':
        if asp == 'smp':
            return 'psv'
        elif asp == 'rc':
            return 'recip1'
        else:
            return 'recip2'
    elif vc == 'tr':
        if asp == 'smp':
            return 'csv'
        elif asp == 'rc':
            return 'csv-recip1'
        else:
            return 'csv-recip2'
    elif asp == 'it':
        return 'iter'
    else:
        return 'smp'
        
def percent(num, den):
    return int((float(num)/den) * 100)
    
def write_ders(root_type, write=False):
    '''Write derivations for root type in file.'''
    roots = RD[root_type]
    if root_type == 'novel':
        probs = get_prob_dict()
    filename = 'ders_' + root_type + '.txt'
    outfile = 'l3/Data/Ti/' + filename
    all_ders = {}
    for root, entries in roots.items():
        if root_type == 'novel' and probs[root] > 50:
            continue
        n, ders = get_ders(None, root, entries)
        if n > 14:
            all_ders[root] = tuple([perc for d,  perc in ders])
    # Now write all_ders in outfile
    if write:
        outf = open(outfile, 'w')
        for root_ders in all_ders.items():
            outf.write(root_ders.__repr__() + '\n')
        outf.close()
    return all_ders
    
def get_ders(roots, root, entries=None):
    entries = entries or roots.get(root, {})
    counts = {}
    n = 0
    for word, anals in entries.items():
        der_dct = {}
        for anal in anals:
            der = get_dercat(anal)
            if der:
                if der in der_dct:
                    der_dct[der] += 1
                else:
                    der_dct[der] = 1
        max_der= ''
        for der, count in der_dct.items():
            if count >= len(anals) / 2:
                max_der = der
                n += 1
                break
        if max_der:
            if max_der in counts:
#                counts[max_arg].append(word)
                counts[max_der] += 1
            else:
#                counts[max_arg] = [word]
                counts[max_der] = 1
#        if ob_dct:
#            counts[word] = (len(anals), ob_dct)
    ders = dict([(der, percent(count, n)) for der, count in counts.items()])
    return n, [(der, ders.get(der, 0)) for der in DERS]
    
def write_nonders(root_type, write=False):
    '''Write TAM, polarity, relativization for root type in file.'''
    roots = RD[root_type]
    if root_type == 'novel':
        probs = get_prob_dict()
    filename = 'nonders_' + root_type + '.txt'
    outfile = 'l3/Data/Ti/' + filename
    all_attribs = {}
    for root, entries in roots.items():
        if root_type == 'novel' and probs[root] > 50:
            continue
        n, tam = get_tam(None, root, entries)
        if n > 9:
            all_attribs[root] = [tam]
##            n, neg = get_neg(None, root, entries)
##            all_attribs[root].append(neg)
            n, rel = get_rel(None, root, entries)
            all_attribs[root].append(rel)
    # Now write all_ders in outfile
    if write:
        outf = open(outfile, 'w')
        for root_attribs in all_attribs.items():
            outf.write(root_attribs.__repr__() + '\n')
        outf.close()
    return all_attribs

def write_sbj(root_type, write=False):
    '''Write percentages of subjects for root type in file.'''
    roots = RD[root_type]
    if root_type == 'novel':
        probs = get_prob_dict()
    filename = 'sbj_' + root_type + '.txt'
    outfile = 'l3/Data/Ti/' + filename
    all_sbj = {}
    for root, entries in roots.items():
        if root_type == 'novel' and probs[root] > 50:
            continue
        n, args = get_args(roots, root, 'sb')
        if n > 14:
            all_sbj[root] = tuple([perc for a, perc in args.items()])
    # Now write all_ders in outfile
    if write:
        outf = open(outfile, 'w')
        for root_sbjs in all_sbj.items():
            outf.write(root_sbjs.__repr__() + '\n')
        outf.close()
    return all_sbj
    
def write_obj(root_type, write=False):
    '''Write percentages of objects for root type in file.'''
    roots = RD[root_type]
    if root_type == 'novel':
        probs = get_prob_dict()
    filename = 'obj_' + root_type + '.txt'
    outfile = 'l3/Data/Ti/' + filename
    all_obj = {}
    for root, entries in roots.items():
        if root_type == 'novel' and probs[root] > 50:
            continue
        n, args = get_args(roots, root, 'ob')
        if n > 14:
            all_obj[root] = tuple([perc for a, perc in args.items()])
    # Now write all_ders in outfile
    if write:
        outf = open(outfile, 'w')
        for root_objs in all_obj.items():
            outf.write(root_objs.__repr__() + '\n')
        outf.close()
    return all_obj

def anal_arg(root_type, arg='ob', dercat='', write=False):
    roots = RD[root_type]
    if root_type == 'novel':
        probs = get_prob_dict()
    filename = arg + dercat + '_anal_' + root_type + '.txt'
    outfile = 'l3/Data/Ti/' + filename
    all_arg = {}
    for root, entries in roots.items():
        if root_type == 'novel' and probs[root] > 50:
            continue
        n_words = len(entries)
        n, args = anal_args(roots, root, arg, dercat=dercat)
        if n > 9:
            values = tuple([args.get(png, 0) for png in PNG])
#            all_arg[root] = tuple([perc for a, perc in args.items()])
            all_arg[root] = values
        else:
            all_arg[root] = (0,)
    # Now write all_ders in outfile
    if write:
        outf = open(outfile, 'w')
        for root_objs in all_arg.items():
            outf.write(root_objs.__repr__() + '\n')
        outf.close()
    return all_arg    
    
def get_neg(roots, root, entries=None):
    entries = entries or roots.get(root, {})
    counts = {'neg': 0, 'aff': 0}
    for word, anals in entries.items():
        neg = 0
        for anal in anals:
            neg = anal.get('neg', False)
            if neg:
                neg += 1
        if neg > len(anals) / 2:
            counts['neg'] += 1
        else:
            counts['aff'] += 1
    n_entries = len(entries)
    return n_entries, [percent(counts['neg'], n_entries), percent(counts['aff'], n_entries)]

def get_rel(roots, root, entries=None):
    entries = entries or roots.get(root, {})
    counts = {'rel': 0, 'nonrel': 0}
    for word, anals in entries.items():
        rel = 0
        for anal in anals:
            rel = anal.get('rel', False)
            if rel:
                rel += 1
        if rel > len(anals) / 2:
            counts['rel'] += 1
        else:
            counts['nonrel'] += 1
    n_entries = len(entries)
    return n_entries, [percent(counts['rel'], n_entries), percent(counts['nonrel'], n_entries)]
    
def get_tam(roots, root, entries=None):
    entries = entries or roots.get(root, {})
    if not entries:
        0, None
    counts = [0,  0,  0,  0]
    n = 0
    for word, anals in entries.items():
        tam = [0,  0,  0,  0]
        for anal in anals:
            tam1 = anal.get('tm')
            if tam1 == 'prf':
                tam[0] += 1
            elif tam1 == 'imf':
                tam[1] += 1
            elif tam1 == 'j_i':
                tam[2] += 1
            else:
                tam[3] += 1
        max_tam = -1
        for index, t in enumerate(tam):
            if t > len(anals) / 2:
                max_tam = index
                break
        if max_tam >= 0:
            n += 1
            counts[max_tam] += 1
    if n == 0:
        return 0, None
    return n, [percent(count, n) for count in counts]

def anal_args(roots, root, arg, dercat=''):
    # If dercat is not empty, use number satisfying for calculating percentages
    entries = roots.get(root, {})
    counts = {}
    n = 0
    for word, anals in entries.items():
        arg_dct = {}
        for anal in anals:
            a = agr2str(anal.get(arg))
            if arg == 'sb' and not a:
                a = '3ms'
            der = not dercat or get_dercat(anal) == dercat
            if der:
                n += 1
            if a and der:
                if a in arg_dct:
                    arg_dct[a] += 1
                else:
                    arg_dct[a] = 1
        max_arg= ''
        for ar, count in arg_dct.items():
            if count > len(anals) / 2:
                max_arg = ar
                break
        if max_arg:
            n += 1
            if max_arg in counts:
                counts[max_arg] += 1
            else:
                counts[max_arg] = 1
    if n:
        args = dict([(arg, percent(count, n)) for arg, count in counts.items()])
        return n, args
    else:
        return 0, {}

def get_args(roots, root, arg, dercat=''):
    entries = roots.get(root, {})
    counts = {}
    n = 0
    for word, anals in entries.items():
        arg_dct = {}
        for anal in anals:
            a = agr2str(anal.get(arg))
            if arg == 'sb' and not a:
                a = '3ms'
            der = not dercat or get_dercat(anal) == dercat
            if a and der:
                if a in arg_dct:
                    arg_dct[a] += 1
                else:
                    arg_dct[a] = 1
        max_arg= ''
        for ar, count in arg_dct.items():
            if count > len(anals) / 2:
                max_arg = ar
                break
        if max_arg:
            n += 1
            if max_arg in counts:
#                counts[max_arg].append(word)
                counts[max_arg] += 1
            else:
#                counts[max_arg] = [word]
                counts[max_arg] = 1
#        if ob_dct:
#            counts[word] = (len(anals), ob_dct)
    args = dict([(arg, percent(count, n)) for arg, count in counts.items()])
    return len(entries), args
#    return len(entries), counts

### Derivational and valency categories

def get_smp_psv_roots(kind, write=False):
    '''Separate roots that appear in simple from those whose base form is passive.'''
    ders = DATA[kind]['ders']
    smp = []
    psv = []
    for root, ders in ders.items():
        # Percentage of simple
        if ders[0] < 10:
            psv.append((root, ders))
        else:
            smp.append((root, ders))
    if write:
        outsmp = open('l3/Data/Ti/' + kind + '_smp.txt', 'w')
        outpsv = open('l3/Data/Ti/' + kind + '_psv.txt', 'w')
        for rd in smp:
            outsmp.write(rd.__repr__() + '\n')
        for rd in psv:
            outpsv.write(rd.__repr__() + '\n')
        outsmp.close()
        outpsv.close()
    return smp, psv

def get_psv_recip_roots(kind, psv, write=False):
    real_psv = []
    recip = []
    for root, ders in psv:
        sum_der = sum(ders)
        if ders[3] > 0.5 * sum_der:
            recip.append((root, ders))
        else:
            real_psv.append((root, ders))
    if write:
        outrec = open('l3/Data/Ti/' + kind + '_recip.txt', 'w')
        outpsv = open('l3/Data/Ti/' + kind + '_psvpsv.txt', 'w')
        for rd in recip:
            outrec.write(rd.__repr__() + '\n')
        for rd in real_psv:
            outpsv.write(rd.__repr__() + '\n')
        outrec.close()
        outpsv.close()
    return real_psv, recip

def get_intrans(roots, write=False):
    '''Get known roots within roots that have no passive.'''
    ders = DATA['known']['ders']
    intr = []
    for root in roots:
        der = ders[root]
        # Percentage of passive less than 3
        if der[1] < 3:
            intr.append((root, der))
    if write:
        out = open('l3/Data/Ti/known_intrans.txt', 'w')
        for rd in intr:
            out.write(rd.__repr__() + '\n')
        out.close()
    return intr

def get_impersonal(sbj_anal):
    res = []
    for root, anal in sbj_anal.items():
        if len(anal) == 1:
            continue
        anal_sum = sum(anal)
        if anal_sum > 0.0 and anal[0] / float(anal_sum) > 0.8:
            res.append((root, anal))
    return res

DATA = {'known': {'nonders': write_nonders('known'), 'ders': write_ders('known'),
                  'sbjs': write_sbj('known'), 'objs': write_obj('known')},
        'novel': {'nonders': write_nonders('novel'), 'ders': write_ders('novel'),
                  'sbjs': write_sbj('novel'), 'objs': write_obj('novel')}}

NOVEL_DATA = get_data('novel')
FILTER_NOVEL = filter_novel(NOVEL_DATA)

novel = open('l3/Data/Ti/novel_data.txt', 'w')
for d in NOVEL_DATA.items():
    novel.write(d.__repr__() + '\n')
novel.close()

COMPETITORS = get_competitors()
### Eliminate all roots in competition sets that are not in filtered root set
##reduce_competsets(FILTER_NOVEL, COMPETITORS)
### Eliminate duplicate competition sets
COMPETITORS = elim_dup_csets(COMPETITORS)
NOVEL_CSETS = get_root_compet_sets(list(FILTER_NOVEL.keys()), COMPETITORS)
filt_roots_by_compets(FILTER_NOVEL, NOVEL_CSETS)

KNOWN_SMP, KNOWN_PSV = get_smp_psv_roots('known')

#### Geez consonants and vowels in traditional order
##GEEZ_ALPHA_CONSONANTS = ['h', 'l', 'H', 'm', 'r', 's', 'x', 'q', 'Q', 'b',
##                        't', 'c', 'n', 'N', "!", 'k', 'K', 'w',
##                        "`", 'z', 'Z', 'y', 'd', 'j', 'g', 'T', 'C', 'P',
##                        'S', 'f', 'p', '_', '|', 'W']
##GEEZ_ALPHA_VOWELS = ['e', '@', 'u', 'i', 'a', 'E', 'I', 'o']
##CONSONANTS = ["h", "l", "H", "m", "^s", "r", "s", "x", "q", "Q", "b", "t", "c",
##              "^h", "n", "N", "'", "k", "K", "w", "`", "z", "Z", "y", "d", "j", "g",
##              "T", "C", "P", "S", "^S", "f", "p"]
##
##def alphabetize_roots(roots):
##    roots.sort(key=geez_key)
##
##def geez_alpha(s1, s2, pos1 = 0, pos2 = 0):
##    """Comparator function for two strings or lists using Geez order."""
##    if s1 == s2:
##        return 0
##    elif pos1 >= len(s1):
##        return -1
##    elif pos2 >= len(s2):
##        return 1
##    else:
##        seg1 = s1[pos1]
##        seg2 = s2[pos2]
##        if seg1 == seg2:
##            return geez_alpha(s1, s2, pos1 + 1, pos2 + 1)
##        elif seg1 in VOWELS and seg2 in VOWELS:
##            if GEEZ_ALPHA_VOWELS.index(seg1) < GEEZ_ALPHA_VOWELS.index(seg2):
##                return -1
##            else:
##                return 1
##        elif seg1 == 'W':
##            return 1
##        elif seg2 == 'W':
##            return -1
##        elif seg1 in CONSONANTS and seg2 in CONSONANTS:
##            if GEEZ_ALPHA_CONSONANTS.index(seg1) < GEEZ_ALPHA_CONSONANTS.index(seg2):
##                return -1
##            else:
##                return 1
##        # Otherwise one of the vowels is a missing 6th order vowel
##        elif seg1 in CONSONANTS:
##            if seg2 in VOWELS and 5 < GEEZ_ALPHA_VOWELS.index(seg2):
##                return -1
##            else:
##                return 1
##        elif seg2 in CONSONANTS:
##            if seg1 in VOWELS:
##                if GEEZ_ALPHA_VOWELS.index(seg1) < 5:
##                    return -1
##                else:
##                    return 1
##            else:
##                return -1
##        else:
##            # Both are non-Ethiopic characters
##            return cmp(s1[pos1:], s2[pos2:])
##
##def CmpToKey(mycmp):
##    'Convert a cmp= function into a key= function'
##    class K(object):
##        def __init__(self, obj, *args):
##            self.obj = obj
##        def __cmp__(self, other):
##            return mycmp(self.obj, other.obj)
##    return K

##def filter_novel(nonders_dct=NONDERS_U, outf=True):
##    dct = {}
##    elim = 0
##    if outf:
##        outfile = open('l3/Data/Ti/filtered_novel.txt', 'w')
##    for root, data in nonders_dct.items():
##        tam = data[0]
##        pol = data[1]
##        rel = data[2]
##        if tam.count(0) >= 2:
##            elim += 1
##            print(root, 'lacks TAM variability')
##        elif rel[0] > 92 or rel[1] > 92:
##            elim += 1
##            print(root, 'lacks relativization variability')
##        else:
##            dct[root] = data
##    if outf:
##        for item in dct.items():
##            outfile.write(item.__repr__() + '\n')
##        outfile.close()
##    print('Eliminated', elim)
##    return dct
    
##def anal_counts(infile=IN, guess=GUESS, known=KNOWN, writefreq=5, start=0, nlines=0):
##    t1 = time.time()
##    infile = open(infile, 'r', encoding='utf-8')
##    # Each line is a word and a count
##    lines = infile.readlines()
##    if start or nlines:
##        lines = lines[start:start+nlines]
##    nlines = 0
##    for line in lines:
##        nlines += 1
##        if nlines % 5000 == 0:
##            print('Analyzed', nlines, 'words')
##        # Separate punctuation from words
##        line = TI.morphology.sep_punc(line)
##        # Segment into words
##        word, count = line.split()
##        count = int(count)
##        # Ignore "trivial" analysis
##        if not TI.morphology.trivial_anal(word):
##            form = TI.preproc(word)
##            analyses = TI.anal_word(form, fsts=None, guess=True, simplified=False,
##                                    root=True, stem=False, citation=False, gram=True,
##                                    preproc=False, postproc=False, only_anal=True)
##            if analyses:
##                anal_score = 1.0 / len(analyses)
##                for anal in analyses:
##                    pos, root, fs = anal[0], anal[1], anal[-1]
##                    if pos == '?v':
##                        for g in guess:
##                            incorporate(g[0], root, fs, anal_score, count * anal_score, g[2:], form)
##                    else:
##                        for k in known:
##                            incorporate(k[0], root, fs, anal_score, count * anal_score, k[2:], form)
##        if nlines % writefreq == 0:
##            print('Writing dicts')
##            for k in known:
##                if k[1]:
##                    if k[2:]:
##                        write_anal_dict(k[1], k[0])
##                    else:
##                        write_word_dict(k[1], k[0])
##            for g in guess:
##                if g[1]:
##                    if g[2:]:
##                        write_anal_dict(g[1], g[0])
##                    else:
##                        write_word_dict(g[1], g[0])
##    print('Analysis took %0.1f seconds' % (time.time()-t1,))
##    infile.close()
##
##def incorporate(outdict, root, anal, typescore, tokscore, feats, form):
##    if feats and feats[0] == 'words':
##        # Just record the wordform
##        if root in outdict:
##            outdict[root].add(form)
##        else:
##            outdict[root] = set([form])
##    else:
##        feats1 = feats[0] if len(feats) > 0 else None
##        feats2 = feats[1] if len(feats) > 1 else None
##        if feats1:
##            # Create new FeatStructs to store the significant features in fsin
##            fsout1 = l3.morpho.fs.FeatStruct()
##            if not incorporate_feats(anal, fsout1, feats1):
##                return
##            fsout1.freeze()
##            if feats2:
##                fsout2 = l3.morpho.fs.FeatStruct()
##                if not incorporate_feats(anal, fsout2, feats2):
##                    return
##                fsout2.freeze()
##            else:
##                fsout2 = None
##        else:
##            fsout1 = None
##
##        if fsout1:
##            if root in outdict:
##                root_entry = outdict[root]
##                if fsout1 not in root_entry:
##                    if fsout2:
##                        # Create a new dict for this combination of root and sig feats
##                        outdict[root][fsout1] = {fsout2: [typescore, tokscore]}
##                    else:
##                        outdict[root][fsout1] = [typescore, tokscore]
##                elif fsout2:
##                    if fsout2 not in root_entry[fsout1]:
##                        # Add an entry for sig feats2 in the root sig feats dict
##                        outdict[root][fsout1][fsout2] = [typescore, tokscore]
##                    else:
##                        # Increment the score for the root/sig feats2/sig feats2 combination
##                        outdict[root][fsout1][fsout2][0] += typescore
##                        outdict[root][fsout1][fsout2][1] += tokscore
##                else:
##                    outdict[root][fsout1][0] += typescore
##                    outdict[root][fsout1][1] += tokscore
##            elif fsout2:
##                # Create a new dict of dicts for this root
##                outdict[root] = {fsout1: {fsout2: [typescore, tokscore]}}
##            else:
##                outdict[root] = {fsout1: [typescore, tokscore]}
##        elif root in outdict:
##            outdict[root].append(anal)
##        else:
##            outdict[root] = [anal]
##
##def incorporate_feats(analfs, outfs, feats):
##    for feat in feats:
##        if feat not in analfs:
##            return False
##        elif feat == 'ob':
##            incorporate_obj(analfs['ob'], outfs)
##        else:
##            outfs[feat] = analfs[feat]
##    return True
##
##def incorporate_obj(objfs, fs):
##    """Incorporate obj fs into fs only if it's explicit and non-prepositional."""
##    if objfs.get('xpl', None) and not objfs.get('prp'):
##        fs['ob'] = objfs
    
##def anal_new_roots(dct, roots=None, thresh=7, outfile=None):
##    roots = roots if roots != None else {}
##    if outfile:
##        outfile = open(outfile, 'w')
##    for root, stems in dct.items():
##        count = sum([len(x) for x in list(stems.values())])
##        # There are enough different contexts and at least two different der cats
##        if count >= thresh and len(stems) > 1:
##            roots[root] = count
##            if outfile:
##                outfile.write(root + ' ' + str(count) + '\n')
##    if outfile:
##        outfile.close()
##                
##def anal_der_class(dct, roots=None, thresh=4.0, outfile=None):
##    roots = roots if roots != None else {}
##    if outfile:
##        outfile = open(outfile, 'w')
##    for root, stems in dct.items():
##        # Does the root occur in simplex? passive? causative?
##        s_count = 0
##        other_count = 0
##        for stem, args in stems.items():
##            voice = stem['vc']
##            if voice == 'smp':
##                s_count += sum([x[0] for x in list(args.values())])
##            else:
##                other_count += sum([x[0] for x in list(args.values())])
##        # Now compare simplex and other counts
##        if s_count < 1.0 and other_count > thresh:
##            roots[root] = 2
##            if outfile:
##                outfile.write(root + ' ' + '2\n')
##        elif s_count > thresh and other_count > thresh:
##            roots[root] = 1
##            if outfile:
##                outfile.write(root + ' ' + '1\n')
##    if outfile:
##        outfile.close()
##        
##def anal_valency(dct, stems=None, thresh=2, outfile=None):
##    stems = stems if stems != None else {}
##    if outfile:
##        outfile = open(outfile, 'w')
##    stem_cat = ''
##    for root, stms in dct.items():
##        for stm, args in stms.items():
##            voice = stm['vc']
##            aspect = stm['as']
##        if aspect == 'smp':
##            # Only consider simplex aspect
##            if voice == 'smp':
##                stem_cat = 'simplex'
##            elif voice == 'ps':
##                stem_cat = 'passive'
##            subjects = set([])
##            objects = set([])
##            for arg, count in args.items():
##                subjects.add(arg['sb'])
##                obj = arg['ob']
##                if obj.get('xpl') and not obj.get('prp'):
##                    objects.add(obj)
##            if len(subjects) == 1:
##                sbj = list(subjects)[0]
##                if not sbj.get('p1') and not sbj.get('p2') and not sbj.get('plr') and not sbj.get('fem'):
##                    if len(objects) > 1:
##                        stems[(root, stem_cat)] = 'impersonal'
##                        if outfile:
##                            outfile.write(root + ' ' + stem_cat + ' impersonal\n')
##            elif len(objects) == 0 and len(subjects) > thresh:
##                stems[(root, stem_cat)] = 'intransitive'
##                if outfile:
##                    outfile.write(root + ' ' + stem_cat + ' intransitive\n')
##            elif len(objects) > (thresh + 1) and len(subjects) > thresh:
##                stems[(root, stem_cat)] = 'transitive'
##                if outfile:
##                    outfile.write(root + ' ' + stem_cat + ' transitive\n')
##    if outfile:
##        outfile.close()
##    
##def combine_anal_dicts(dct1, dct2):
##    for root, stems in dct2.items():
##        if root not in dct1:
##            dct1[root] = stems
##        else:
##            root1 = dct1[root]
##            for stem, args in stems.items():
##                if stem not in root1:
##                    root1[stem] = args
##                else:
##                    stem1 = root1[stem]
##                    for arg, count in args.items():
##                        if arg in stem1:
##                            stem1[arg][0] += count[0]
##                            stem1[arg][1] += count[1]
##                        else:
##                            stem1[arg] = count
##
##def write_anal_dict(outfile, dct):
##    outf = open(outfile, 'w')
##    for root, stems in dct.items():
##        outf.write("%r " + root + "\n")
##        outf.write(stems.__repr__() + "\n")
####        for stem, args in stems.iteritems():
####            outf.write('%1 ' + str(stem) + "\n")
####            for arg, count in args.iteritems():
####                outf.write('%2 ' + str(arg) + " " + str(count) + '\n')
##    outf.close()
##
##def write_word_dict(outfile, dct):
##    outf = open(outfile, 'w')
##    for root, words in dct.items():
##        outf.write('%r ' + root + '\n')
##        for word in words:
##            outf.write(word + '\n')
##    outf.close()
##
##def read_anal_dict(infile, dct=None):
##    dct = dct if dct != None else {}
##    infile = open(infile)
##    current_root = {}
##    for line in infile:
##        split = line.split()
##        if split[0] == '%r':
##            # This is the beginning of a root entry
##            root = split[-1]
##            current_root = {}
##        else:
##            # This line is the entry for a root
##            entry = line.strip()
##            # Separate the entries for different der cats
##            ders = entry.split('}, ')
##            for der_args in ders:
##                # Separate the der key from the args value
##                der, args = der_args.split(': {')
##                der = der.replace('{', '')
##                # Convert to feat struct
##                der = l3.morpho.fs.FeatStruct(der)
##                der.freeze()
##                der_entry = {}
##                for arg_count in args.split(', ['):
##                    # Separate the args from the counts
##                    arg, count = arg_count.split(': ')
##                    if arg[0] != '[':
##                        arg = '[' + arg
##                    # Convert args to feat struct
##                    arg = l3.morpho.fs.FeatStruct(arg)
##                    arg.freeze()
##                    count = count.replace('}', '')
##                    # Convert to list of floats
##                    count = eval(count)
##                    der_entry[arg] = count
##                current_root[der] = der_entry
##            dct[root] = current_root
##    infile.close()
##
