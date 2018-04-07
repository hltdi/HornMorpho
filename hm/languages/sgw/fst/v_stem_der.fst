## Chaha root -> derivational stems
## Features:
## vc: [+-ps, +-tr]; as: smp, rc, it; tm: imf, prf, j_i, con1, con2, fut1, fut2
## Root types:
## Aqtl, Bqtl, Cqtl, DqWtl, (qll), Eqlmg, (qlql), (qltt), nqlmg, qlamg?
## Operates right-to-left over roots

-> start

###  get the class
start -> A   <:A|>
start -> B   <:B|>
start -> C|   <:C|>
start -> D|   <:D|>
start -> E|   <:E|>

A -> A.c          [RR]
A.c -> A.cv       [e:]   [tm=prf];[tm=imf,vc=[+ps]];[tm=j_i,vc=[+ps]];[tm=j_i,-tr]
A.c -> A.cv       [:]    [tm=imf,vc=[-ps]];[tm=j_i,vc=[-ps],+tr]
A.cv -> A.cvc1    [/:]   [tm=prf];[tm=imf,vc=[+ps]]
A.cv -> A.cvc1    [:]   [tm=imf,vc=[-ps]];[tm=j_i]
A.cvc1 -> A.cvc   [RR]
A.cvc -> A.cvcv   [:]    [tm=j_i]
A.cvc -> A.cvcv   [e:]    [tm=prf];[tm=imf]
A.cvcv -> end     [RR]

B -> B.c          [RR]
B.c -> B.cv       [e:]   [tm=prf];[tm=imf,vc=[+ps]];[tm=j_i,vc=[+ps]]
B.c -> B.cv       [:]    [tm=imf,vc=[-ps]];[tm=j_i,vc=[-ps]]
B.cv -> B.cv^     [^:]   [tm=imf];[tm=prf]
B.cv -> B.cv^     [:]    [tm=j_i]
B.cv^ -> B.cv/    [/:]
B.cv/ -> B.cvc    [RR:]
B.cvc -> B.cvc^   [^:]   [tm=imf];[tm=prf]
B.cvc -> B.cvc^   [:]    [tm=j_i]
B.cvc^ -> B.cvcv  [e:]
B.cvcv -> B.cvcv^ [^:]   [tm=imf];[tm=prf]
B.cvcv -> B.cvcv^ [:]    [tm=j_i]
B.cvcv^ -> end    [RR]

### Class A
## C1
#A| -> A|C          [RR]
## V1
#A|C -> A|CV        [e:]   [tm=prf];[tm=imf]
#A|C -> A|CV        [:]    [tm=j_i]
## C2
## for these verbs, never geminate
#A|CV -> A|CVC1     [:.]
#A|CV -> A|CVC1     [/:]   [tm=prf];[tm=imf,vc=[+ps]]
#A|CV -> A|CVC1     [:]    [tm=imf,vc=[-ps]];[tm=j_i]
#A|CVC1 -> A|CVC    [RR]
## V2
#A|CVC -> CVCV      [e:]   [tm=prf];[tm=imf,vc=[+ps]];[tm=j_i,vc=[+ps]];[tm=j_i,-tr]
#A|CVC -> CVCV      [:]    [tm=imf,vc=[-ps]];[tm=j_i,vc=[-ps],+tr]

## Class B
# palatalization except in jussive/imperative
B| -> B|1          [^:]   [tm=imf];[tm=prf]
B| -> B|1          [:]    [tm=j_i]
# C1
B|1 -> B|C         [RR]
# V1
B|C -> B|CV        [e:]
# C2 gemination (except for some jussive/imperatives)
B|CV -> B|CV/      [/:]
# C2
B|CV/ -> B|CVC     [RR]
# V2
B|CVC -> CVCV    [e:]   [tm=prf];[tm=imf,vc=[+ps]];[tm=j_i,vc=[+ps]]
B|CVC -> CVCV    [:]    [tm=imf,vc=[-ps]];[tm=j_i,vc=[-ps]]

## Class C
# C1
C| -> C|C          [RR]
# V1: always a
C|C -> C|CV        [a:]
# C2
C|CV -> C|CVC1     [/:]   [tm=prf];[tm=imf]
# also geminated for some verbs (C:zbt)
C|CV -> C|CVC1     [:]    [tm=j_i]
C|CVC1 -> C|CVC    [RR]
# V2
C|CVC -> CVCV    [e:]   [tm=prf];[tm=imf,vc=[+ps]];[tm=j_i,vc=[+ps]]
C|CVC -> CVCV    [:]    [tm=imf,vc=[-ps]];[tm=j_i,vc=[-ps]]

## Class D
# C1 (labialized)
D| -> D|C          [RR]
# V1
D|C -> D|CV        [e:]
# C2
D|CV -> D|CV/      [/:]   [tm=prf];[tm=imf]
D|CV/ -> D|CVC     [RR]
D|CV -> D|CVC      [RR]   [tm=j_i]
# V2
D|CVC -> CVCV      [e:]   [tm=prf];[tm=imf,vc=[+ps]];[tm=j_i,vc=[+ps]]
D|CVC -> CVCV      [:]    [tm=imf,vc=[-ps]];[tm=j_i,vc=[-ps]]

## Class E
# C1
E| -> E|C           [RR]
# V1
E|C -> E|CV         [e:]   [tm=j_i]
E|C -> E|CV         [:]    [tm=prf];[tm=imf]
# C2
E|CV -> E|CVC       [RR]
# V2
E|CVC -> E|CVCV     [e:]   [tm=prf];[tm=imf]
E|CVC -> E|CVCV     [:]    [tm=j_i]
# C3
E|CVCV -> E|CVCV/   [/:]   [tm=prf];[tm=imf]
E|CVCV/ -> E|CVCVC  [RR]
E|CVCV -> E|CVCVC   [RR]   [tm=j_i]
# V3
E|CVCVC -> CVCV     [e:]   [tm=prf]
E|CVCVC -> CVCV     [:]    [tm=imf];[tm=j_i]

# last C
CVCV -> end         [RR]

end ->
