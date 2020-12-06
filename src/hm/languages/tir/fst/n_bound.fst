# handle characters at the boundary between stem and add_suffixes

-> start

# wait for the boundary character
start -> C     [X]
start -> V     [V]
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
