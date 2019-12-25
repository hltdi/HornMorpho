from .__init__ import *
import random

TI_ROOTS1 = ['sbr', 'fS_m', 'mskr', 'kWrkWH', 
             's`m', 'bl`', "wd_'", 'mwt', 'ftw', 'xyT', 'sty', 'drby']
TI_ROOTS2 = ['bark', 'Hdr', 'klakl']         # No as=rc
TI_ROOTS3 = ['n|qTqT', 'n|saff']     # No vc=smp, no as=it, no as=rc

AM_ROOTS1 = ['sbr', 'fS_m', 'mskr', "b'b'", "sT*", "slc*",
             "s'm", "bl'", "TT_'", 'mwt', 'xyT', 'gyT']
AM_ROOTS2 = ['bark', "'dr", 'klakl']         # No as=rc
AM_ROOTS3 = ['C|brbr', 'n|saff']     # No vc=smp, no as=it, no as=rc

def am_gen(iters1=25, iters2=20, iters3=10):
    for root in AM_ROOTS1:
        am_gen_eval(root, iters=iters1)
    for root in AM_ROOTS2:
        am_gen_eval(root, no_rc=True, iters=iters2)
    for root in AM_ROOTS3:
        am_gen_eval(root, no_smp=True, no_rc=True, no_it=True, iters=iters3)

def ti_gen(iters1=25, iters2=20, iters3=10):
    for root in TI_ROOTS1:
        am_gen_eval(root, iters=iters1)
    for root in TI_ROOTS2:
        am_gen_eval(root, no_rc=True, iters=iters2)
    for root in TI_ROOTS3:
        am_gen_eval(root, no_smp=True, no_rc=True, no_it=True, iters=iters3)

def am_gen_eval(root, no_smp=False, no_rc=False, no_cs=False, no_it=False,
                iters=25):
    for i in range(iters):
        am_gen_eval1(root, no_smp=no_smp, no_rc=no_rc, no_it=no_it,
                     no_cs=no_cs)

def ti_gen_eval(root, no_smp=False, no_rc=False, no_it=False,
                iters=25):
    for i in range(iters):
        ti_gen_eval1(root, no_smp=no_smp, no_rc=no_rc, no_it=no_it)

def anal_am():
    anal_file('am', 'Data/Am/am_words1000.txt', outfile='Data/Am/am_words1000_out.txt',
              citation=False, preproc=False, postproc=False)

def anal_ti():
    anal_file('ti', 'Data/Ti/ti_words1000.txt', outfile='Data/Ti/ti_words1000_out.txt',
              citation=False, preproc=False, postproc=False)

def sep_am():
    sep_anal('Data/Am/am_words1000_out.txt', 'Data/Am/am1000')

def sep_ti():
    sep_anal('Data/Ti/ti_words1000_out.txt', 'Data/Ti/ti1000')

def sep_anal(infile, outfile):
    inf = open(infile)
    outfl = open(outfile + '_lex.txt', 'w')
    outfg = open(outfile + '_guess.txt', 'w')
    outfx = open(outfile + '_non.txt', 'w')
    lex = True
    non = False
    lines = inf.readlines()
    index = 0
    w = 0
    while index < len(lines):
        line = lines[index]
        if line[:5] == '?Word':
            w += 1
            outfx.write(str(w) + line[6:])
            non = True
        elif line[:4] == 'Word':
            w += 1
            line = '\n' + str(w) + line[5:]
            next_line = lines[index+1]
            non = False
            if next_line[0] == '?':
                lex = False
            else:
                lex = True
        if lex and not non:
            outfl.write(line)
        elif not non:
            outfg.write(line)
        index += 1
    inf.close()
    outfl.close()
    outfg.close()
    outfx.close()

def am_gen_eval1(root, sbob='', tam='', asp='', vc='',
                 neg='', rel='', prp='', cj1='',
                 no_smp=False, no_rc=False, no_cs=False, no_it=False,
                 outfile=False):
    fs = ''
    sb, ob = sbob or make_sbob()
    tam = tam or random.choice(['imf', 'j_i', 'ger', ''])
    asp_opts = ['']
    if not no_rc:
        asp_opts.append('rc')
    if not no_it:
        asp_opts.append('it')
    asp = asp or random.choice(asp_opts)
    vc_opts = ['ps', 'tr']
    if asp != 'rc' and not no_smp:
        vc_opts.append('')
    if not no_cs and asp != 'rc':
        vc_opts.append('cs')
    vc = vc or random.choice(vc_opts)
    if tam != 'ger' and tam != 'j_i':
        neg = neg or random.choice(['True', ''])
        rel = rel or random.choice(['True', ''])
        if rel:
            prp = prp or random.choice(['be', ''])
        if not rel and not prp and tam == 'imf':
            cj1 = cj1 or random.choice(['sI', ''])
    prec = False
    f_string = root + ': '
    for name, feats in [('sb', sb), ('ob', ob), ('tm', tam),
                        ('as', asp), ('vc', vc), ('neg', neg),
                        ('rel', rel), ('pp', prp), ('cj1', cj1)]:
        if feats:
            f_string += name + ':' + feats + ' '
            if prec: fs += ','
            fs += name + '=' + feats
            prec = True
    if fs:
        fs = '[' + fs + ']'
    if outfile:
        outfile.write(f_string + '\n')
    else:
        print(f_string)
    return gen('am', root, features=fs if fs else [], non_roman=False)

def ti_gen_eval1(root, sbob='', tam='', asp='', vc='',
                 neg='', rel='', prp='', cj1='',
                 no_smp=False, no_rc=False, no_it=False,
                 outfile=None):
    fs = ''
    tam = tam or random.choice(['imf', 'j_i', 'ger', ''])
    sb, ob = sbob or make_sbob(False, tam)
    asp_opts = ['']
    if not no_rc:
        as_opts.append('rc')
    if not no_it:
        as_opts.append('it')
    asp = asp or random.choice(as_opts)
    vc_opts = ['ps', 'tr']
    if asp != 'rc' and not no_smp:
        vc_opts.append('')
    vc = vc or random.choice(vc_opts)
    if tam != 'ger' and tam != 'j_i':
        neg = neg or random.choice(['True', ''])
        rel = rel or random.choice(['True', ''])
        if rel:
            prp = prp or random.choice(['bI', ''])
        if not rel and not prp:
            if tam == 'imf':
                cj1 = cj1 or random.choice(['kI', ''])
            elif tam == 'prf':
                cj1 = cj1 or random.choice(['mIs', ''])
    prec = False
    f_string = root + ': '
    for name, feats in [('sb', sb), ('ob', ob), ('tm', tam),
                        ('as', asp), ('vc', vc), ('neg', neg),
                        ('rel', rel), ('pp', prp), ('cj1', cj1)]:
        if feats:
            f_string += name + ':' + feats + ' '
            if prec: fs += ','
            fs += name + '=' + feats
            prec = True
    if fs:
        fs = '[' + fs + ']'
    if outfile:
        outfile.write(f_string + '\n')
    else:
        print(f_string)
    return gen('ti', root, features=fs if fs else [], non_roman=False)

def make_sbob(am=True, tm='prf'):
    sb = ''
    sb_pers = random.choice([1, 2, 3])
    ob = ''
    ob_xpl = random.choice([True, False])
    if ob_xpl:
        ob_prp = random.choice([True, False])
        if sb_pers == 3:
            ob_pers = random.choice([1, 2, 3])
        elif sb_pers == 1:
            ob_pers = random.choice([2, 3])
        else:
            ob_pers = random.choice([1, 3])
        ob = '['
        prev = False
        if ob_pers == 1:
            ob += '+p1'
            prev = True
        if ob_pers == 2:
            ob += '+p2'
            prev = True
        ob_plr = random.choice([True, False])
        if ob_plr:
            if prev: ob += ','
            ob += '+plr'
            prev = True
        if ob_pers != 1 and (not ob_plr or not am):
            ob_fem = random.choice([True, False])
            if ob_fem:
                if prev: ob += ','
                ob += '+fem'
                prev = True
        if ob_prp:
            if prev: ob += ','
            ob += '+prp'
            if am:
                ob_prp_p = random.choice(['l', 'b'])
                ob += ',+' + ob_prp_p
            prev = True
        if prev: ob += ','
        ob += '+xpl]'
    prev = False
    if sb_pers == 1:
        sb += '[+p1'
        prev = True
    if sb_pers == 2:
        sb += '[+p2'
        prev = True
    sb_plr = random.choice([True, False])
    if sb_plr:
        if prev: sb += ','
        else: sb += '['
        sb += '+plr'
        prev = True
    if sb_pers != 1 and (not sb_plr or not am):
        sb_fem = random.choice([True, False])
        if sb_fem:
            if prev: sb += ','
            else: sb += '['
            sb += '+fem'
            prev = True
    if prev: sb += ']'
    return sb, ob
