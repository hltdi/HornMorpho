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

import morpho
import time
import codecs

morpho.load_lang('ti')

TI = morpho.get_language('ti')

GD1 = {}
GD2 = {}
KD = {}
GWD = {}
KNOWN = [(KD, 'Data/ti_kd_saved.txt', ['as','vc'], ['sb','ob'])]
GUESS = [(GD1, 'Data/ti_gd1_saved.txt', ['as', 'vc'], ['sb', 'ob']),
         (GD2, 'Data/ti_gd2_saved.txt', ['tm']),
         (GWD, 'Data/ti_gd3_saved.txt', 'words')]
IN = 'Data/ti_crawl2.txt'

def anal_counts(infile=IN, guess=GUESS, known=KNOWN, writefreq=10000, start=0, nlines=0):
    t1 = time.time()
    infile = codecs.open(infile, 'r', 'utf-8')
    # Each line is a word and a count
    lines = infile.readlines()
    if start or nlines:
        lines = lines[start:start+nlines]
    nlines = 0
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
        if not TI.morphology.trivial_anal(word):
            form = TI.preproc(word)
            analyses = TI.anal_word(form, fsts=None, guess=True, simplified=False,
                                    root=True, stem=False, citation=False, gram=True,
                                    preproc=False, postproc=False, only_anal=True)
            if analyses:
                anal_score = 1.0 / len(analyses)
                for anal in analyses:
                    pos, root, fs = anal[0], anal[1], anal[-1]
                    if pos == '?v':
                        for g in guess:
                            incorporate(g[0], root, fs, anal_score, count * anal_score, g[2:], form)
                    else:
                        for k in known:
                            incorporate(k[0], root, fs, anal_score, count * anal_score, k[2:], form)
        if nlines % writefreq == 0:
            print('Writing dicts')
            for k in known:
                if k[1]:
                    if k[2:]:
                        write_anal_dict(k[1], k[0])
                    else:
                        write_word_dict(k[1], k[0])
            for g in guess:
                if g[1]:
                    if g[2:]:
                        write_anal_dict(g[1], g[0])
                    else:
                        write_word_dict(g[1], g[0])
    print('Analysis took %0.1f seconds' % (time.time()-t1,))
    infile.close()

def incorporate(outdict, root, anal, typescore, tokscore, feats, form):
    if feats and feats[0] == 'words':
        # Just record the wordform
        if root in outdict:
            outdict[root].add(form)
        else:
            outdict[root] = set([form])
    else:
        feats1 = feats[0] if len(feats) > 0 else None
        feats2 = feats[1] if len(feats) > 1 else None
        if feats1:
            # Create new FeatStructs to store the significant features in fsin
            fsout1 = morpho.fs.FeatStruct()
            if not incorporate_feats(anal, fsout1, feats1):
                return
            fsout1.freeze()
            if feats2:
                fsout2 = morpho.fs.FeatStruct()
                if not incorporate_feats(anal, fsout2, feats2):
                    return
                fsout2.freeze()
            else:
                fsout2 = None
        else:
            fsout1 = None

        if fsout1:
            if root in outdict:
                root_entry = outdict[root]
                if fsout1 not in root_entry:
                    if fsout2:
                        # Create a new dict for this combination of root and sig feats
                        outdict[root][fsout1] = {fsout2: [typescore, tokscore]}
                    else:
                        outdict[root][fsout1] = [typescore, tokscore]
                elif fsout2:
                    if fsout2 not in root_entry[fsout1]:
                        # Add an entry for sig feats2 in the root sig feats dict
                        outdict[root][fsout1][fsout2] = [typescore, tokscore]
                    else:
                        # Increment the score for the root/sig feats2/sig feats2 combination
                        outdict[root][fsout1][fsout2][0] += typescore
                        outdict[root][fsout1][fsout2][1] += tokscore
                else:
                    outdict[root][fsout1][0] += typescore
                    outdict[root][fsout1][1] += tokscore
            elif fsout2:
                # Create a new dict of dicts for this root
                outdict[root] = {fsout1: {fsout2: [typescore, tokscore]}}
            else:
                outdict[root] = {fsout1: [typescore, tokscore]}
        elif root in outdict:
            outdict[root].append(anal)
        else:
            outdict[root] = [anal]

def incorporate_feats(analfs, outfs, feats):
    for feat in feats:
        if feat not in analfs:
            return False
        elif feat == 'ob':
            incorporate_obj(analfs['ob'], outfs)
        else:
            outfs[feat] = analfs[feat]
    return True

def incorporate_obj(objfs, fs):
    """Incorporate obj fs into fs only if it's explicit and non-prepositional."""
    if objfs.get('xpl', None) and not objfs.get('prp'):
        fs['ob'] = objfs
    
def anal_new_roots(dct, roots=None, thresh=7, outfile=None):
    roots = roots if roots != None else {}
    if outfile:
        outfile = open(outfile, 'w')
    for root, stems in dct.items():
        count = sum([len(x) for x in list(stems.values())])
        # There are enough different contexts and at least two different der cats
        if count >= thresh and len(stems) > 1:
            roots[root] = count
            if outfile:
                outfile.write(root + ' ' + str(count) + '\n')
    if outfile:
        outfile.close()
                
def anal_der_class(dct, roots=None, thresh=4.0, outfile=None):
    roots = roots if roots != None else {}
    if outfile:
        outfile = open(outfile, 'w')
    for root, stems in dct.items():
        # Does the root occur in simplex? passive? causative?
        s_count = 0
        other_count = 0
        for stem, args in stems.items():
            voice = stem['vc']
            if voice == 'smp':
                s_count += sum([x[0] for x in list(args.values())])
            else:
                other_count += sum([x[0] for x in list(args.values())])
        # Now compare simplex and other counts
        if s_count < 1.0 and other_count > thresh:
            roots[root] = 2
            if outfile:
                outfile.write(root + ' ' + '2\n')
        elif s_count > thresh and other_count > thresh:
            roots[root] = 1
            if outfile:
                outfile.write(root + ' ' + '1\n')
    if outfile:
        outfile.close()
        
def anal_valency(dct, stems=None, thresh=2, outfile=None):
    stems = stems if stems != None else {}
    if outfile:
        outfile = open(outfile, 'w')
    stem_cat = ''
    for root, stms in dct.items():
        for stm, args in stms.items():
            voice = stm['vc']
            aspect = stm['as']
        if aspect == 'smp':
            # Only consider simplex aspect
            if voice == 'smp':
                stem_cat = 'simplex'
            elif voice == 'ps':
                stem_cat = 'passive'
            subjects = set([])
            objects = set([])
            for arg, count in args.items():
                subjects.add(arg['sb'])
                obj = arg['ob']
                if obj.get('xpl') and not obj.get('prp'):
                    objects.add(obj)
            if len(subjects) == 1:
                sbj = list(subjects)[0]
                if not sbj.get('p1') and not sbj.get('p2') and not sbj.get('plr') and not sbj.get('fem'):
                    if len(objects) > 1:
                        stems[(root, stem_cat)] = 'impersonal'
                        if outfile:
                            outfile.write(root + ' ' + stem_cat + ' impersonal\n')
            elif len(objects) == 0 and len(subjects) > thresh:
                stems[(root, stem_cat)] = 'intransitive'
                if outfile:
                    outfile.write(root + ' ' + stem_cat + ' intransitive\n')
            elif len(objects) > (thresh + 1) and len(subjects) > thresh:
                stems[(root, stem_cat)] = 'transitive'
                if outfile:
                    outfile.write(root + ' ' + stem_cat + ' transitive\n')
    if outfile:
        outfile.close()
    
def combine_anal_dicts(dct1, dct2):
    for root, stems in dct2.items():
        if root not in dct1:
            dct1[root] = stems
        else:
            root1 = dct1[root]
            for stem, args in stems.items():
                if stem not in root1:
                    root1[stem] = args
                else:
                    stem1 = root1[stem]
                    for arg, count in args.items():
                        if arg in stem1:
                            stem1[arg][0] += count[0]
                            stem1[arg][1] += count[1]
                        else:
                            stem1[arg] = count

def write_anal_dict(outfile, dct):
    outf = open(outfile, 'w')
    for root, stems in dct.items():
        outf.write("%r " + root + "\n")
        outf.write(stems.__repr__() + "\n")
##        for stem, args in stems.iteritems():
##            outf.write('%1 ' + str(stem) + "\n")
##            for arg, count in args.iteritems():
##                outf.write('%2 ' + str(arg) + " " + str(count) + '\n')
    outf.close()

def write_word_dict(outfile, dct):
    outf = open(outfile, 'w')
    for root, words in dct.items():
        outf.write('%r ' + root + '\n')
        for word in words:
            outf.write(word + '\n')
    outf.close()

def read_anal_dict(infile, dct=None):
    dct = dct if dct != None else {}
    infile = open(infile)
    current_root = {}
    for line in infile:
        split = line.split()
        if split[0] == '%r':
            # This is the beginning of a root entry
            root = split[-1]
            current_root = {}
        else:
            # This line is the entry for a root
            entry = line.strip()
            # Separate the entries for different der cats
            ders = entry.split('}, ')
            for der_args in ders:
                # Separate the der key from the args value
                der, args = der_args.split(': {')
                der = der.replace('{', '')
                # Convert to feat struct
                der = morpho.fs.FeatStruct(der)
                der.freeze()
                der_entry = {}
                for arg_count in args.split(', ['):
                    # Separate the args from the counts
                    arg, count = arg_count.split(': ')
                    if arg[0] != '[':
                        arg = '[' + arg
                    # Convert args to feat struct
                    arg = morpho.fs.FeatStruct(arg)
                    arg.freeze()
                    count = count.replace('}', '')
                    # Convert to list of floats
                    count = eval(count)
                    der_entry[arg] = count
                current_root[der] = der_entry
            dct[root] = current_root
    infile.close()

