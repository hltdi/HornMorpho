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
lab -> start       [pW:p;w:b;mW:m;fW:f;kW:k;gW:g;KW:K;qW:q]

# only vowel that can be palatalized?
lab -> start       [O:a]

start ->
