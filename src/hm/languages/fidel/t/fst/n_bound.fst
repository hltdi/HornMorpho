# handle characters at the boundary between stem and suffixes

-> start

# up to pre-stem boundary
start -> prep  [X]  # currently only b and n
prep -> prep=  [:=]
# spirantize velars
prep= -> C     [X-k,q,kW,qW;K:k;Q:q;KW:kW;QW:qW]
#prep= -> V     [V]  # not actually possible

start -> bound [:=]

# wait for the boundary character
bound -> C     [X]
#start -> V     [V]  # not possible
C -> V         [V]
C -> CC        [X;_]
CC -> CC       [X;_]
V -> C         [X]
CC -> V        [V]

# boundary
C -> C=        [:=]
CC -> CC=      [:=]
V -> V=        [:=]

# insert word-final i following CC or C_
CC= -> CC=i    [i:]

# following CC, k->K
CC= -> end     [X-k,';:';K:k;V]

# following vowel,
#   delete e of ey
#   k->K
V= -> end      [:e;X-k;K:k]

C= -> end      [V;X-';:']

CC=i ->
V= ->
C= ->

end -> end     [X;V;_]
end ->
