# Fix final CC

-> start

start -> V      [V]
V -> wy         [w;y]
V -> C          [X-w,y]

# digits
start -> D      [D]
D -> D          [D]
D -> V          [V]
D -> C          [X-w,y]
D -> wy         [w;y]
V -> D          [D]
C -> D          [D]
wy -> D         [D]
CC -> D         [D]
CIC -> D        [D]

start -> C      [X-w,y]
start -> wy     [w;y]
# Can be followed by anything
wy -> CC        [X;_]

C -> V          [V]
wy -> V         [V]

C -> CC         [X-R;_]
# Can't be followed by final R
C -> CR         [R]
# There can't be any sequences of 3 consonants
CC -> V         [V]
CR -> V         [V]

C -> CI         [I:]
CI -> CIC       [R]

CIC ->
V ->
C ->
CC ->
wy ->
D ->
