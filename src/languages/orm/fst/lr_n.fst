# n->l following l, n->r following r

-> start

start -> start    [$;!-l,r]

# Environment: l, r
start -> l        [l]
start -> r        [r]

# n->l
l -> start        [l:n]
# n->r
r -> start        [r:n]

# Consonants other than n
l -> start        [$;!-n]
r -> start        [$;!-n]

start ->
