# delete or convert to e the vowel in passive prefix t*
# convert * before the stem prefix n to I when it's word initial

-> start

start -> start  [X;V-*;%]

# * -> e when there's no prefix; te...
start -> e      [e:*]
e -> te         [t]
# * -> I when there's no prefix; In...
start -> I      [I:*]
I -> end        [=]
te -> end       [=]

# * -> 0 when there's a prefix (or causative a)
start -> 0      [:*]
0 -> t          [t]
# *n
0 -> pre        [=]
# t* could precede *n, in which case it's =ten...
0 -> e          [e:*]
# ... or x=tn... ?
0 -> 0          [:*]
t -> pre        [=]
# a or maybe e if the = has been deleted
t -> start      [V]
pre -> start    [X;V]

end ->
start ->