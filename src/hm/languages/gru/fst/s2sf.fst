-> start

start -> end   [:]    [sp=0|1|3];[tm=prf];[sp=2,sn=2];[sp=2,sn=1,sg=m]

start -> pre   [:]    [sp=2,sn=1,sg=f,tm=imf|j_i]

pre -> pre     [X;V;/;_]
pre -> stem    [=]
stem -> stem   [/]
stem -> C1     [X]
C1 -> C1       [_]
C1 -> V1       [V-e]
# A: V1: e->E
# palatalize first vowel in class A imperfective
C1 -> V        [E:e]           [tm=imf]
# but not B imperative
C1 -> V        [e;:]           [tm=j_i]
# V1 -> C        [X]
V -> C         [X]
C -> C         [X;_]
C -> V         [V]
# palatalize last vowel in imperative
C -> V_1       [E:e;i:I;V-e,I] [tm=j_i]
C -> V_1       [V]             [tm=imf]
# palatalize last consonant
V -> C.=       [FF-YY;c:t;C:T;j:d;x:s;C:S;Z:z;N:n]
V_1 -> C.=     [FF-YY;c:t;C:T;j:d;x:s;C:S;Z:z;N:n]
C -> C.=       [FF-YY;c:t;C:T;j:d;x:s;C:S;Z:z;N:n]
C.= -> C.=     [_]
C.= -> suf     [=]
# -a=
C -> V.=       [i:a;E:e]
V.= -> suf     [=]
# V -> suf       [=]

end -> end     [X;V;/;_;=]
suf -> suf     [X;V;_]

end ->
suf ->