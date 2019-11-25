-> start

start -> start     [X;e;E;a;I;o;A;i;u;*;=]

start -> pal       [:^]

# also palatalize labialized consonsants
pal -> start       [c:t;C:T;j:d;x:s;Z:z;kY:k;gY:g;KY:K;qY:q;y:r;kY:kW;gY:gW;KY:KW;qY:qW]

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
b_w -> b_w=        [=]
b_w= -> start      [XX]
# b -> bW when it's word initial
lab -> b_bW        [bW:b]
b_bW -> end        [=]

# only vowel that can be labialized?
lab -> start       [O:a]

start ->

end ->
