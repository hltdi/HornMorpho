# Instead of optionally inserting GS between e and another vowel, as in analysis,
# just delete the 1 that marks the possible boundary

-> start

start -> start   [X;V-e;%-1]

start -> e       [e]

# delete 1 before anything
e -> del1        [:1]
# anything may follow
del1 -> start    [X;V;%]
e -> start       [X;V-e;%-1]
e -> e           [e]

# replace 1 with ' before a vowel (NOT FOR GENERATION)
# e -> 12GS      [':1]
# 12GS -> start  [V]

start ->
e ->
