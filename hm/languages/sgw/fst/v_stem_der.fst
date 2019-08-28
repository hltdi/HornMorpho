## Chaha root -> derivational stems
## Features:
## vc: [+-ps, +-tr]; as: smp, rc, it; tm: imf, prf, j_i, con1, con2, fut1, fut2
## Root types:
## Aqtl, Bqtl, Cqtl, DqWtl, (qll), Eqlmg, (qlql), (qltt), nqlmg, qlamg?
## Weak root: h**, *h*, **h; *y*, **y; w**, *w*
## Operates right-to-left over roots

-> start

###  get the class
start -> A   [:]   [root=[cls=A]]
start -> B   [:]   [root=[cls=B]]
start -> C   [:]   [root=[cls=C]]
start -> D   [:]   [root=[cls=D]]
start -> E   [:]   [root=[cls=E]]

### A class
## strong verbs
# final consonant
A -> A.c          [RR]
A.c -> A.cv       [e:]   [tm=prf];[tm=imf,vc=[+ps]];[tm=j_i,vc=[+ps]];[tm=j_i,root=[-tr]]
A.c -> A.cv       [:]    [tm=imf,vc=[-ps]];[tm=j_i,vc=[-ps],root=[+tr]]
A.cv -> A.cvc1    [/:]   [tm=prf];[tm=imf,vc=[+ps]]
A.cv -> A.cvc1    [:]   [tm=imf,vc=[-ps]];[tm=j_i]
A.cvc1 -> A.cvc   [RR]
A.cvc -> A.cvcv   [:]    [tm=j_i]
A.cvc -> A.cvcv   [e:]    [tm=prf];[tm=imf]
A.cvcv -> end     [RR]

## weak A verbs

# final 'h'
A -> A.h          [:h]
# stem always ends in a (potentially modified by palatalization later); otherwise same as strong
A.h -> A.cv       [a:]

# final 'y'
A -> A.y          [:y]
A.y -> A.cv       [e:]   [tm=prf];[tm=imf,vc=[+ps]];[tm=j_i,vc=[+ps]];[tm=j_i,root=[-tr]]
A.y -> A.cv       [:]    [tm=imf,vc=[-ps]];[tm=j_i,vc=[-ps],root=[+tr]]

### B class
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

## weak B verbs

# final 'y'
B -> B.y          [:y]
B.y -> B.cv       [e:]   [tm=prf];[tm=imf,vc=[+ps]];[tm=j_i,vc=[+ps]]
B.y -> B.cv       [:]    [tm=imf,vc=[-ps]];[tm=j_i,vc=[-ps]]

## Class C
# C3
C -> C.c           [RR]
# V2
C.c -> C.cv        [e:]   [tm=prf];[tm=imf,vc=[+ps]];[tm=j_i,vc=[+ps]]
C.c -> C.cv        [:]    [tm=imf,vc=[-ps]];[tm=j_i,vc=[-ps]]
# C2
C.cv -> C.cvc1     [/:]   [tm=prf];[tm=imf]
# also geminated for some verbs (C:zbt)?
C.cv -> C.cvc1     [:]    [tm=j_i]
C.cvc1 -> C.cvc    [RR]
# V1, always a
C.cvc -> C.cvcv    [a:]
C.cvcv -> end      [RR]

## Class D
# C1 (labialized)
D -> D.C           [RR]
# V1
D.C -> D.CV        [e:]
# C2
D.CV -> D.CV/      [/:]   [tm=prf];[tm=imf]
D.CV/ -> D.CVC     [RR]
D.CV -> D.CVC      [RR]   [tm=j_i]
# V2
D.CVC -> CVCV      [e:]   [tm=prf];[tm=imf,vc=[+ps]];[tm=j_i,vc=[+ps]]
D.CVC -> CVCV      [:]    [tm=imf,vc=[-ps]];[tm=j_i,vc=[-ps]]

## Class E
# C1
E -> E.C            [RR]
# V1
E.C -> E.CV         [e:]   [tm=j_i]
E.C -> E.CV         [:]    [tm=prf];[tm=imf]
# C2
E.CV -> E.CVC       [RR]
# V2
E.CVC -> E.CVCV     [e:]   [tm=prf];[tm=imf]
E.CVC -> E.CVCV     [:]    [tm=j_i]
# C3
E.CVCV -> E.CVCV/   [/:]   [tm=prf];[tm=imf]
E.CVCV/ -> E.CVCVC  [RR]
E.CVCV -> E.CVCVC   [RR]   [tm=j_i]
# V3
E.CVCVC -> CVCV     [e:]   [tm=prf]
E.CVCVC -> CVCV     [:]    [tm=imf];[tm=j_i]

# last C
CVCV -> end         [RR]

end ->
