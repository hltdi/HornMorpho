# Has to happen before the Iw and Iy rules

-> start

start -> start  [_]

start -> V      [V]

# the #CC case (#CIC epenthesis)
start -> C1     [X]
C1 -> C1        [$]
C1 -> C1I       [I:]
C1I -> C        [X]
C -> C          [$]
C1 -> V         [V]

V -> C          [X]
V -> V          [V]         # consecutive vowels possible at this level

# the CC_ case (CICC, CIC# epenthesis)
C -> CI         [I:]
CI -> CIC       [X]
CIC -> CIC      [$]
CIC -> CC       [_]         # possibility of CCIC epenthesis
CIC -> CICC     [X;_]       # or finish with CICC epenthesis
CICC -> CICC    [$]
CICC -> V       [V]
C -> V          [V]

# the CCC or C_C case (CCIC epenthesis)
C -> CC         [_;X]
CC -> CC        [$]
CC -> CCI       [I:]
CC -> V         [V]         # escape back to start
CCI -> C        [X]

V ->
C ->
CIC ->
CCIC ->
