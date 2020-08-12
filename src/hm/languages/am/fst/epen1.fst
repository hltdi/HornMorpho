-> start

start -> V      [V]

# the #CC case (#CIC epenthesis)
start -> C1     [X]
C1 -> C1I       [I:]
C1I -> C        [X]
C1 -> V         [V]

V -> C          [X]         # no consecutive vowels possible at this level
C -> V          [V]

# the CCC or C_C case (CCIC epenthesis)
C -> CC         [X;_]
CC -> CCI       [I:]
CC -> V         [V]         # escape back to V
CCI -> C        [X]         # escape back to C

# the CC_ case (CICC epenthesis)
C -> CI         [I:]
CI -> CIC       [X]
CIC -> CC       [_]         # can be followed by CCIC

V ->
C ->
# Fix these in epen2
CC ->
