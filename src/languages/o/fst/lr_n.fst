# n->l following l, n->r following r

-> start

start -> start    [$;!-l,r;-;>]

# Environment: l, r
start -> l        [l]
start -> r        [r]

# delete morpheme boundaries; no more changes
l -> l+	 	  [:-;:>]
r -> r+		  [:-;:>]

# n->l
l+ -> start        [l:n]
# n->r
r+ -> start        [r:n]

# keep the - otherwise
l ->  l++	   [-;>]
r -> r++	   [-;>]

# Consonants other than n
l++ -> start        [$;!-n]
r++ -> start        [$;!-n]

l -> start	    [$;!-n]
r -> start	    [$;!-n]

start ->
