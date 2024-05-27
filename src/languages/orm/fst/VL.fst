# vowel lengthening

-> start

start -> start    [!;%;+]

start -> a.       [:a]
start -> e.       [:e]
start -> i.       [:i]
start -> o.       [:o]
start -> u.       [:u]
a. -> start       [aa:L]
e. -> start       [ee:L]
i. -> start       [ii:L]
o. -> start       [oo:L]
u. -> start       [uu:L]
# Don't lengthen already long vowels
start -> VV       [$2]
VV -> start       [!;%;+;:L]
start -> V        [$]
V -> start        [!;T;C;+]

start ->
V ->
