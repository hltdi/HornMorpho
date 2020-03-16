# optionally insert gs between e and another vowel (indicated by 1)

-> start

start -> start [X;V;%-1]

start -> e     [e]

# delete 1 before anything
e -> del1      [:1]
# anything may follow
del1 -> start  [X;V;%]

# replace 1 with ' before a vowel
e -> 12GS      [':1]
12GS -> start  [V]

start ->
e ->
