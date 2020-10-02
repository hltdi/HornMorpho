# Realize combinations of l, r, n

-> start

start -> start  [X-l,r,n;V]

start -> n      [n]
n -> start      [X-l,r,n;V]
# nn -> n only within word
n -> nn         [:r;:n]
nn -> start     [X;V]

start -> r      [r]
r -> start      [X-l,r,n;V]
# nr unchanged at the beginning of a word
r -> n          [n]

start -> l      [l]
l -> start      [X-l,r,n;V;:r]

start -> delr   [:r]
# nr -> n only within word
delr -> nn      [l;n;n:r]

start ->
n ->
