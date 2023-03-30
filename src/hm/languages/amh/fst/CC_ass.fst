# Assimilate g, q to following k optionally
# Assimilate T to following t optionally

-> start

start -> start  [X;V;%]

start -> G.k    [/:g;/:q]
G.k -> start    [k]

start -> T.t    [/:T]
T.t -> Tt.         [t]
# Another segment must follow, but not geminated character
Tt. -> start    [X;V;/;3]
#T.t -> start    [t]

start ->
