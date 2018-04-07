# Assimilate g, q to following k
# Assimilate T to following t

-> start

start -> start  [X-g,q,T;V;%]

start -> G.k    [/:g;/:q]
G.k -> start    [k]

start -> T.t    [/:T]
T.t -> start    [t]

start -> gq     [g;q]
gq -> start     [X-k;V;%]

start -> T      [T]
T -> start      [X-t;V;%]

start ->
gq ->
