from cluster import KMeansClustering

def get_data(inf='ders1.txt', nclusters=3):
    dct = {}
    data = []
    infile = open(inf)
    for line in infile:
        root, vals = eval(line)
        dct[vals] = root
        data.append(vals)
    infile.close()
    cl = KMeansClustering(data)
    return cl.getclusters(nclusters), dct
