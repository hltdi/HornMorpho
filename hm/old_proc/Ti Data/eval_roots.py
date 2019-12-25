import numpy

def eval_root(root, lists):
    return root, [numpy.std(l) for l in lists]

def eval_roots(filename):
    evals = {}
    inf = open(filename)
    for line in inf:
        root, lists = eval(line)
        evals[root] = lists
    return evals
