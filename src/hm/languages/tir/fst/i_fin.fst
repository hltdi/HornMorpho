# CC# -> CCi#
# I# -> i#

-> start
start -> start   [V-I]

start -> C       [X]
C -> start       [V-I]
C -> CC          [_;X]
# There could still be three consonants if the last is y
CC -> CC         [_;X]
CC -> CCi        [i:]
CC -> start      [V-I]

start -> Ii      [i:I]
start -> I       [I]
C -> Ii          [i:I]
C -> I           [I]
CC -> Ii         [i:I]
CC -> I          [I]
I -> C           [X]
I -> start       [V-I]

start ->
CCi ->
C ->
Ii ->
