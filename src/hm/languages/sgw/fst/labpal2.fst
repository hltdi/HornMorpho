## Actually palatalize consonants and vowels followed by ^
## and labialize consonants followed by @

-> start

start -> start     [X;V;*;=]

start -> pal       [:^]

# also palatalize labialized consonsants
pal -> start       [c:t;C:T;j:d;x:s;Z:z;kY:k;gY:g;KY:K;qY:q;y:r;y:l;kY:kW;gY:gW;KY:KW;qY:qW]

pal -> start       [i:I;E:e;A:a]
# n stays the same
pal -> start       [n]

start -> lab       [:@]

# don't labialize palatalized consonants
lab -> start       [pW:p;mW:m;fW:f;kW:k;gW:g;KW:K;qW:q]
## b -> w | bW
# b -> w except when word-initial
lab -> b_w         [w:b]
b_w -> start       [XX]
b_w -> pal         [:^]
b_w -> b_w=        [=]
b_w= -> start      [XX]
# b -> bW when it's word initial
lab -> b_bW        [bW:b]
b_bW -> end        [=]

# only vowel that can be labialized?
lab -> start       [O:a]

start ->

end ->
