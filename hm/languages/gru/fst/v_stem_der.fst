## Kistane root -> derivational stems
## Features:
##   der: ps, tr, cs, rc, it
## Root types:
##   A: sbr, B: sb_r, C: sabr, E: sbsb, F: sbasb, ?sbrbr, ?sbrabr

-> start

## derivational prefixes
start -> stem1       [:]    [vc=[-ps,-cs]]
start -> stem1       [a:]   [vc=[-ps,+cs]]
start -> stem1       <t*:>  [vc=[+ps,-cs]]
start -> stem1       <at:>  [vc=[+ps,+cs]]

##
stem1 -> stem1n      [I:]
stem1n -> stem       [n]
stem1 -> stem        [:]

# A verbs
stem -> A1           [X]    [cls=A]
A1 -> A1v            [e:]   [tm=prf|imf]
A1 -> A1v            [:]    [tm=j_i]
A1v -> A2            [X]
A2 -> A2_            [_:]   [tm=prf,-neg]
A2 -> A2_            [:]    [tm=prf,+neg];[tm=imf];[tm=j_i]
A2_ -> A2v           [e:]   [tm=prf];[tm=j_i,sp=2];[tm=j_i,sp=1,sn=2];[tm=j_i,sp=3,sn=1,sg=f];[tm=j_i,+neg]
A2_ -> A2v           [:]    [tm=imf];[tm=j_i,sp=1,sn=1,-neg];[tm=j_i,sp=3,sn=2,-neg];[tm=j_i,sp=3,sn=1,sg=m,-neg]
A2v -> end           [X]

# B verbs
stem -> B1           [X]    [cls=B]
B1 -> B1v            [i:]   [tm=prf,-neg];[tm=imf]
B1 -> B1v            [e:]   [tm=prf,+neg];[tm=j_i]
B1v -> B2            [X]
B2 -> B2_            [_:]
B2_ -> B2v           [e:]   [tm=prf]
B2_ -> B2v           [:]    [tm=imf|j_i]
B2v -> end           [X]

# C verbs
stem -> C1           [X]    [cls=C]
C1 -> C1v            [a:]
C1v -> C2            [X]
C2 -> C2_            [_:]   [tm=prf,-neg];[tm=imf]
C2 -> C2_            [:]    [tm=prf,+neg];[tm=j_i]
C2_ -> C2v           [e:]   [tm=prf]
C2_ -> C2v           [:]    [tm=imf|j_i]
C2v -> end           [X]

start -> 

end ->
