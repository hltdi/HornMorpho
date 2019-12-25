# -*- coding: utf-8 -*-

import random
import codecs

def filt1(inf, outf):
    inf = codecs.open(inf, 'r', 'utf-8')
    outf = codecs.open(outf, 'w', 'utf-8')
    words = {}
    napos = 0
    shortened = 0
    for line in inf:
        count, word = line.split()
        if u"'" in word:
            napos += 1
            word = word[:(word.index(u"'"))]
            if word not in words:
                words[word] = count
                outf.write(word + ' ' + count + '\n')
            else:
                shortened += 1
        else:
            words[word] = count
            outf.write(word + ' ' + count + '\n')
    print 'N Apost', napos, 'shortened by', shortened
#    return words

def filt2(inf, outf):
    '''Get rid of words with less than three characters and words with v.'''
    inf = codecs.open(inf, 'r', 'utf-8')
    outf = codecs.open(outf, 'w', 'utf-8')
    nwords = 0
    elim = 0
    for line in inf:
        word, count = line.split()
        if len(word) < 3 or len(word) > 11 or \
            u"ቨ" in word or u"ቩ" in word or u"ቪ" in word or u"ቫ" in word or \
            u"ቬ" in word or u"ቭ" in word or u"ቮ" in word:
            elim += 1
        else:
            outf.write(word + ' ' + count + '\n')
            nwords += 1
    inf.close()
    outf.close()
    print 'Eliminated', elim, 'n words', nwords

##def filt3(inf, outf):
##    '''Just get rid of the numbers.'''
##    inf = codecs.open(inf, 'r', 'utf-8')
##    outf = codecs.open(outf, 'w', 'utf-8')
##    for line in inf:
##        word, count = line.split()
##        outf.write(word + '\n')
##
##def filt4(inf, outf):
##    '''Just get rid of the numbers.'''
##    inf = codecs.open(inf, 'r', 'utf-8')
##    outf = codecs.open(outf, 'w', 'utf-8')
##    elim = 0
##    for line in inf:
##        word = line.strip()
##        if len(word) <= 11:
##            outf.write(word + '\n')
##        else:
##            elim += 1
##    print "Eliminated", elim
##    inf.close()
##    outf.close()

##def romanize_words(inpath, outpath):
##    infile = open(inpath)
##    outfile = open(outpath, 'w')
##    for line in infile:
##        ln = line.split()
##        ti = ln[1].strip()
##        rom = eth2sera(ETH_SERA['ti'][0], ti, lang='ti')
##        outfile.write(rom + '\n')
##        
##    infile.close()
##    outfile.close()

def get_words(inpath, outpath=None):
    infile = open(inpath)
    outfile = open(outpath, 'w')
    n = 0
    for line in infile:
        # Just write the first string in the line
        outfile.write(line.split()[0] + '\n')
        n += 1
        if n % 1000 == 0:
            print n, 'words checked'

    infile.close()
    outfile.close()

def scramble_words(inpath, outpath=None):
    infile = open(inpath)
    outfile = open(outpath if outpath else inpath[:-4] + '_out.txt', 'w')
    words = [w.strip() for w in infile]
    random.shuffle(words)
    for w in words:
        outfile.write(w + '\n')
    infile.close()
    outfile.close()

def n_words(inpath, outpath=None, n=1000):
    infile = open(inpath)
    outfile = open(outpath if outpath else inpath[:-4] + str(n) + '.txt', 'w')
    for line in infile.readlines()[:n]:
        outfile.write(line)
    infile.close()
    outfile.close()


