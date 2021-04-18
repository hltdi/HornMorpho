# Realize combinations of l, r, n

-> start

start -> start  [X-l,r,n;V]

# NN -> N_; RN -> N_; LN -> N_
start -> n      [n]
n -> start      [X-l,r,n;V]
start -> deln   [_:n]
# nn -> n only within word
deln -> nn      [n:r;n:n;n:l]
nn -> start     [X;V]

start -> r      [r]
r -> start      [X-l,r,n;V]
# nr unchanged at the beginning of a word
r -> n          [n]

start -> l      [l]
l -> start      [X-l,r,n;V;:r]

# RR -> L_, NR -> N_, LR -> L_
start -> delr   [_:r]
# nr -> n only within word
delr -> llnn    [l;n;l:r]
llnn -> start   [X;V]

start ->
n ->
