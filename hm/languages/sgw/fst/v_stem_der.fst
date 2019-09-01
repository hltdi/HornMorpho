## Chaha root -> derivational stems
## Features:
## vc: [+-ps, +-tr]; as: smp, rc, it; tm: imf, prf, j_i, con1, con2, fut1, fut2
## Root types:
## Aqtl, Bqtl, Cqtl, DqWtl, (qll), Eqlmg, (qlql), (qltt), nqlmg, qlamg?
## Weak roots: h**, *h*, **h; *y*, **y; w**, *w*
## Operates right-to-left over roots

-> start

###  get the class
start -> A   [:]   [root=[cls=A]]
start -> B   [:]   [root=[cls=B]]
start -> C   [:]   [root=[cls=C]]
start -> D   [:]   [root=[cls=D]]
start -> E   [:]   [root=[cls=E]];[root=[cls=F]]

### A class
## strong verbs
# final consonant
A -> A.c          [ZZ]
A.c -> A.cv       [e:]   [tm=prf];[tm=imf,vc=[+ps]];[tm=j_i,vc=[+ps]];[tm=j_i,root=[-tr]]
A.c -> A.cv       [:]    [tm=imf,vc=[-ps]];[tm=j_i,vc=[-ps],root=[+tr]]
A.cv -> A.cvc1    [/:]   [tm=prf];[tm=imf,vc=[+ps]]
A.cv -> A.cvc1    [:]    [tm=imf,vc=[-ps]];[tm=j_i]
A.cvc1 -> A.cvc   [YY]
A.cvc -> A.cvcv   [:]     [tm=j_i]
A.cvc -> A.cvcv   [e:]    [tm=prf];[tm=imf]
A.cvcv -> end     [YY]

## weak A verbs

# final 'h'
A -> A.h          [:h]
# stem always ends in a (potentially modified by palatalization later); otherwise same as strong
A.h -> A.cv       [a:]

# final 'y'
A -> A.y          [:y]
A.y -> A.yv       [e:]   [tm=prf];[tm=imf,vc=[+ps]];[tm=j_i,vc=[+ps]];[tm=j_i,root=[-tr]]
A.y -> A.yv       [:]    [tm=imf,vc=[-ps]];[tm=j_i,vc=[-ps],root=[+tr]]
# palatalize the final consonant, unless the subject is 3p prf, 2/3p imf, or 2/p j_i
A.yv -> A.yv^     [^:]   [tm=prf,sn=1];[tm=prf,sp=1,sn=2];[tm=prf,sp=2,sn=2];[tm=imf,sn=1];[tm=imf,sp=1,sn=2];[tm=j_i,sn=1];[tm=j_i,sp=1,sn=2]
A.yv -> A.yv^     [:]    [sp=None];[tm=prf,sp=3,sn=2];[tm=imf,sp=3,sn=2];[tm=imf,sp=2,sn=2];[tm=j_i,sp=3,sn=2];[tm=j_i,sp=2,sn=2]
A.yv^ -> A.yv^1   [/:]   [tm=prf];[tm=imf,vc=[+ps]]
A.yv^ -> A.yv^1   [:]    [tm=imf,vc=[-ps]];[tm=j_i]
A.yv^1 -> A.cvc   [KK;DD]
A.yv -> A.yv1     [/:]   [tm=prf];[tm=imf,vc=[+ps]]
A.yv -> A.yv1     [:]    [tm=imf,vc=[-ps]];[tm=j_i]
A.yv1 -> A.yvc    [MM]
# palatalize the first vowel
A.yvc -> A.cvc    [^:]

### B class
B -> B.c          [ZZ;:y]
B.c -> B.cv       [e:]   [tm=prf];[tm=imf,vc=[+ps]];[tm=j_i,vc=[+ps]]
B.c -> B.cv       [:]    [tm=imf,vc=[-ps]];[tm=j_i,vc=[-ps]]
# palatalize 2nd (velar) consonant
B.cv -> B.cv^     [^:]   [tm=prf];[tm=imf]
B.cv -> B.cv^     [:]    [tm=j_i]
B.cv^ -> B.cv^/   [/:]
B.cv^/ -> B.cvG   [KK]
B.cvG -> B.cvGv   [e:]
B.cvGv -> end     [MM;r]
# palatalize 1st consonant (velar or coronal obstruent)
B.cv -> B.cv/     [/:]
B.cv/ -> B.cvc    [YY]
B.cvc -> B.cvcv   [e:]
B.cvcv -> B.cvcv^ [^:]   [tm=prf];[tm=imf]
B.cvcv -> B.cvcv^ [:]    [tm=j_i]
B.cvcv^ -> end    [KK;TT]
# palatalize first vowel
B.cv/ -> B.cvX    [DD;MM]
B.cvX -> B.cvX^   [^:]   [tm=prf];[tm=imf]
B.cvX -> B.cvX^   [:]    [tm=j_i]
B.cvX^ -> B.cvX^v [e:]
B.cvX^v -> end    [MM;r]

## weak B verbs

## Class C
# C3
C -> C.c           [ZZ]
C -> C.y           [:y]
# V2
C.c -> C.cv        [e:]   [tm=prf];[tm=imf,vc=[+ps]];[tm=j_i,vc=[+ps]]
C.c -> C.cv        [:]    [tm=imf,vc=[-ps]];[tm=j_i,vc=[-ps]]
C.y -> C.yv        [e:]   [tm=prf];[tm=imf,vc=[+ps]];[tm=j_i,vc=[+ps]]
C.y -> C.yv        [:]    [tm=imf,vc=[-ps]];[tm=j_i,vc=[-ps]]
# Seems that C2 is always palatalizable for **y C verbs.
C.yv -> C.cv       [^:]
# C2
C.cv -> C.cvc1     [/:]   [tm=prf];[tm=imf]
# also geminated for some verbs (C:zbt)?
C.cv -> C.cvc1     [:]    [tm=j_i]
C.cvc1 -> C.cvc    [YY]
# V1, always a
C.cvc -> C.cvcv    [a:]
C.cvcv -> end      [RR]

## Class D
# C3
D -> D.C           [ZZ]
# 
D.C -> D.CV        [e:]   [tm=prf];[tm=imf,vc=[+ps]];[tm=j_i,vc=[+ps]]
D.C -> D.CV        [:]    [tm=imf,vc=[-ps]];[tm=j_i,vc=[-ps]]
# C2 (always geminated)
D.CV -> D.CV/      [/:]   
D.CV/ -> D.CVC     [RR]
# V1 (e followed labialized, o following unlabialized consonants)
D.CVC -> D.CVCe    [e:]
D.CVCe -> D.CVCe@  [@:]
D.CVCe@ -> end     [LL]
D.CVC -> D.CVCo    [o:]
D.CVCo -> end      [CC-LL]

## Class E, F
# C4
E -> E.C            [ZZ]
# final y -> palatalization (under certain circumstances)
E -> E.y            [:y]   [tm=prf,sn=1];[tm=prf,sp=1,sn=2];[tm=prf,sp=2,sn=2];[tm=imf,sn=1];[tm=imf,sp=1,sn=2];[tm=j_i,sn=1];[tm=j_i,sp=1,sn=2]
E -> E.C            [:y]   [sp=None];[tm=prf,sp=3,sn=2];[tm=imf,sp=3,sn=2];[tm=imf,sp=2,sn=2];[tm=j_i,sp=3,sn=2];[tm=j_i,sp=2,sn=2]
# V3
E.C -> E.CV         [e:]   [tm=prf]
E.C -> E.CV         [:]    [tm=j_i];[tm=imf]
E.y -> E.yV         [e:]   [tm=prf]
E.y -> E.yV         [:]    [tm=j_i];[tm=imf]
# C3
E.CV -> E.CV/       [/:]   [tm=prf];[tm=imf]
E.CV/ -> E.CVC      [AA]
E.CV  -> E.CVC      [AA]   [tm=j_i]
E.yV -> E.yv^       [^:]
E.yv^ -> E.yv/      [/:]   [tm=prf];[tm=imf]
# assumes all ***y verbs have a velar or coronal as C3
E.yv/ -> E.CVC      [KK;DD]
E.yv^ -> E.CVC      [KK;DD] [tm=j_i]

# V2
E.CVC -> E.CVCV     [a:]   [root=[cls=F]]
E.CVC -> E.CVCV     [e:]   [tm=prf,root=[cls=E]];[tm=imf,root=[cls=E]]
E.CVC -> E.CVCV     [:]    [tm=j_i,root=[cls=E]]
# C2
E.CVCV -> E.CVCVC   [AA]
# V1
E.CVCVC -> E.CVCVCV [e:]   [tm=j_i,root=[cls=E]]
E.CVCVC -> E.CVCVCV [:]    [root=[cls=F]];[tm=imf];[tm=prf]
# C1
E.CVCVCV -> end     [AA]

end ->
