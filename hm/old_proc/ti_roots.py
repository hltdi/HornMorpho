import sgt
from ngram import *
from nltk.probability import LidstoneProbDist
import os
import codecs
#from nltk.model import NgramModel
# import nltk

COUNTS = {}
FREQFREQ = {1:{}, 2:{}, 3:{}}
ROOTS = ['bSh', 'mS!', 'blSg', 'wrd', 'bark', 'n|Sbark', '`w_l']

ROOT_FILE = 'l3/FST/Ti/vb_root0.lex'
WORD_ANALS = {'known': 'l3/Data/Ti/root_k.txt',
              'novel': 'l3/Data/Ti/root_u.txt'}
ANAL_DIR = 'l3/Data/Ti/'

def make_root_text(rootfile=ROOT_FILE):
    rootin = open(ROOT_FILE)
    string = '#' + '#'.join([root.strip() for root in rootin]) + '#'
    string = string.replace("'", "!")
    return string

def segment(string):
    segs = []
    pos = 0
    while pos < len(string):
        char = string[pos]
        if pos < len(string) - 1:
            nextchar = string[pos+1]
            if nextchar in ['W', '|', '_']:
                if nextchar == 'W' and pos < len(string) - 2:
                    nextnextchar = string[pos+2]
                    if nextnextchar in ['_', '|']:
                        segs.append(string[pos:pos+3])
                        pos += 1
                    else:
                        segs.append(string[pos:pos+2])
                else:
                    segs.append(string[pos:pos+2])
                pos += 1
            else:
                segs.append(string[pos])
        else:
            segs.append(string[pos])
        pos += 1
    return segs

def get_counts(seq, n):
    counts = {}
    for start in range(len(seq)-n):
        subseq = seq[start:start+n]
        # Don't count sequences that have more than one boundary character at the end
        if subseq[1:].count('#') < 2 and subseq.count('#') < n:
            counts[subseq] = counts.get(subseq, 0) + 1
    return counts

ROOT_STRING = segment(make_root_text())

def make_trigram(string):
    estimator = lambda fdist, bins: LidstoneProbDist(fdist, 0.2)
    return NgramModel(3, string, estimator)

G3 = make_trigram(ROOT_STRING)

def root_prob(root, n=3):
    root = segment('##' + root + '#')
    prob = 0.0
    for start in range(len(root)-n+1):
        seq = root[start:start+n]
        try:
#            print 'Probability of', seq, G3.logprob(seq[-1], seq[:-1])
            prob += G3.logprob(seq[-1], seq[:-1])
        except RuntimeError:
            print 'No probability mass for', seq
            return 100.0
    return prob

def write_root_probs(root_type):
    infile = WORD_ANALS[root_type]
    infile = codecs.open(infile, 'r', 'utf8')
    outfile = open(os.path.join(ANAL_DIR, root_type + '_prob.txt'), 'w')
    for line in infile:
        if line[0] != ' ':
            # new root
#            root = line.split()[-1].replace('?', '')
            # Get rid of the colon
            root = line.strip()[:-1]
            outfile.write(root + ' ' + str(root_prob(root)) + '\n')
    infile.close()
    outfile.close()

#def make_ngram(string, n):
#    return nltk.model.NgramModel(n, string)

def count_n_grams1(word, n, counts=None):
    if counts == None:
        counts = {}
    affix = '#' * (n-1)
    word = affix + word + affix
    for start in range(len(word)-n):
        seq = word[start:start+n]
#        print('Checking', seq)
        counts[seq] = counts.get(seq, 0) + 1
        
def calc_freqfreq(counts, freqfreq=None, n=3):
    if freqfreq == None:
        freqfreq = dict([(x, {}) for x in range(1, n+1)])
    total = dict([(x, 0) for x in range(1, n+1)])
    for seq, count in counts.items():
        freqfreq[len(seq)][count] = freqfreq[len(seq)].get(count, 0) + 1
        total[len(seq)] += count
    adjusted = dict([(x, {}) for x in range(1, n+1)])
    for ln, freqs in freqfreq.items():
        adj = adjusted[ln]
        count1 = freqs.get(1, 0)
        count5 = freqs.get(5, 0)
        num_dec = float(count5 * 5) / count1
        den = 1.0 - num_dec
        for freq, count in freqs.items():
            pass
            
def count_n_grams(words, n, counts=None, freqfreq=None):
    return_counts = False
    if counts == None:
        return_counts = True
        counts = {}
    for word in words:
        for n1 in range(1, n+1):
            count_n_grams1(word, n1, counts=counts)
    calc_freqfreq(counts, freqfreq=freqfreq)
    if return_counts:
        return freqfreq, counts
        
def get_prob(seq, counts, totals):
    count_n = counts.get(seq, 0)
    count_nminus1 = counts.get(seq[:-1], 0)
    if count_n and count_nminus1:
        return logprob(float(count_n) / count_nminus1)
    else:
        print('Backing off')
        return 0.0
    
def logprob(prob):
    return math.log(prob, 2)
    
VOWELS = u'aeEiIou@AOU'
CONSONANTS = ["h", "l", "H", "m", "^s", "r", "s", "x", "q", "Q", "b", "t", "c",
              "^h", "n", "N", "!", "k", "K", "w", "`", "z", "Z", "y", "d", "j", "g",
              "T", "C", "P", "S", "^S", "f", "p", '|', '_']
## Geez consonants and vowels in traditional order
GEEZ_ALPHA_CONSONANTS = [u'h', u'l', u'H', u'm', u'^s', u'r', u's', u'x', u'q', u'Q', u'b',
                        u't', u'c', u'^h', u'n', u'N', u"!", u'k', u'K', u'w',
                        u"`", u'z', u'Z', u'y', u'd', u'j', u'g', u'T', u'C', u'P',
                        u'S', u'^S', u'f', u'p', '|', '_']
GEEZ_ALPHA_VOWELS = [u'e', u'@', u'u', u'i', u'a', u'E', u'I', u'o']

def geez_alpha(s1, s2, pos1 = 0, pos2 = 0):
    """Comparator function for two strings or lists using Geez order.
    (Need to fix _)
    """
    if s1 == s2:
        return 0
    elif pos1 >= len(s1):
        return -1
    elif pos2 >= len(s2):
        return 1
    else:
        seg1 = s1[pos1]
        seg2 = s2[pos2]
        if seg1 == seg2:
            return geez_alpha(s1, s2, pos1 + 1, pos2 + 1)
        elif seg1 in VOWELS and seg2 in VOWELS:
            if GEEZ_ALPHA_VOWELS.index(seg1) < GEEZ_ALPHA_VOWELS.index(seg2):
                return -1
            else:
                return 1
        elif seg1 == u'W':
            return 1
        elif seg2 == u'W':
            return -1
        elif seg1 in CONSONANTS and seg2 in CONSONANTS:
            if GEEZ_ALPHA_CONSONANTS.index(seg1) < GEEZ_ALPHA_CONSONANTS.index(seg2):
                return -1
            else:
                return 1
        # Otherwise one of the vowels is a missing 6th order vowel
        elif seg1 in CONSONANTS:
            if seg2 in VOWELS and 5 < GEEZ_ALPHA_VOWELS.index(seg2):
                return -1
            else:
                return 1
        elif seg2 in CONSONANTS:
            if seg1 in VOWELS:
                if GEEZ_ALPHA_VOWELS.index(seg1) < 5:
                    return -1
                else:
                    return 1
            else:
                return -1
        else:
            # Both are non-Ethiopic characters
            return cmp(s1[pos1:], s2[pos2:])

def sort_root_feats(flin, flout=None):
    flin = open(flin)
    root_feats = [eval(l) for l in flin]
    root_feats.sort(cmp=lambda rf1, rf2: geez_alpha(rf1[0], rf2[0]))
    flin.close()
    if flout:
        flout = open(flout, 'w')
        for root_feat in root_feats:
            flout.write(root_feat.__repr__() + '\n')
        flout.close()
    return root_feats
