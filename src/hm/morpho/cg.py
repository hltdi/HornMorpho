'''
Constraint grammar for HornMorpho.
'''

CG3 = '/usr/local/bin/vislcg3'

from subprocess import Popen, PIPE
import sys

def open_sentence_file(path):
    return Popen(['cat', path], stdout=PIPE)

def call_cg3(rules_path, sentence, trace=True):
    if type(sentence) is str:
        # path to sentence file
        sentence = open_sentence_file(sentence)
    args = [CG3, '-g', rules_path]
    if trace:
        args.append('-t')
    PO = Popen(args, stdout=PIPE, stdin=sentence.stdout)
    res, x = PO.communicate()
    res = res.decode(sys.stdout.encoding)
    return res

#def call_cg3():
#    vislcg3 = Popen(['/usr/local/bin/vislcg3', '--help'], stdout=PIPE)
#    return vislcg3

def anal2cg(analysis):
    '''
    Convert a HM analysis (one element in a Word list) to CG3 format.
    '''
    um = analysis.get('um', '')
    um = ' '.join([u.replace('*', '') for u in um.split(';')])
    pos = analysis.get('pos', '')
    lemma = analysis.get('lemma', analysis.get('token'))
    return '\t"{}" {} {}'.format(lemma, pos, um)

def word2cg(word):
    token = word.name
    result = ['"<{}>"'.format(token)]
    result.extend([anal2cg(analysis) for analysis in word])
    return "\n".join(result)

def sentence2cg(sentence, predelim='', postdelim='', write2=''):
    '''
    Convert an HM Sentence object to CG3 format.
    '''
    result = []
    if predelim:
        result.append(predelim)
    for word in sentence.words:
        result.append(word2cg(word))
    if postdelim:
        result.append(postdelim)
    result = '\n'.join(result)
    if write2:
        with open(write2, 'w', encoding='utf8') as file:
            print(result, file=file)
    else:
        return result
