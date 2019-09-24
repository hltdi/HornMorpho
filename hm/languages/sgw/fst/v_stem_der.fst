## Chaha root -> derivational stems
## Features:
## vc: [+-ps, +-cs]; as: smp, rc, it; tm: imf, prf, j_i, con1, con2, fut1, fut2
## Root types:
## Aqtl, Bqtl, Cqtl, DqWtl, (qll), Eqlmg, (qlql), (qltt), nqlmg, qlamg?
## Weak roots: h**, *h*, **h; *y*, **y; w**, *w*
## Operates right-to-left over roots

-> start

### final consonant

start -> .c        [ZZ-t,d,T]
start -> .c        [t;d;T] [tm=imf,root=[cls=A]];[tm=j_i,root=[cls=A]];[root=[cls=Ap]];[root=[cls=B]];[root=[cls=C]];[root=[cls=D]];[root=[cls=E]];[root=[cls=F]]
start -> .T        [t;d;T] [tm=prf,root=[cls=A]]
start -> .h        [:h]
start -> .c        [:y]    [tm=prf,sp=3,sn=2];[tm=imf,sp=2,sn=2];[tm=imf,sp=3,sn=2];[tm=j_i,sp=2,sn=2];[tm=j_i,sp=3,sn=2];[sp=None]
start -> .y        [:y]    [sp=1];[sn=1];[tm=prf,sp=2,sn=2]

.T -> A.T          [:]    
.T -> A.Te         [e:]
.h -> .cv          [a:]
.c -> .cv          [e:]   [tm=prf];[tm=imf,vc=[+ps,-cs]];[tm=j_i,vc=[+ps,-cs]];[tm=j_i,vc=[-cs],root=[-tr]]
.c -> .cv          [:]    [tm=imf,vc=[-ps]];[tm=imf,vc=[+cs]];[tm=j_i,vc=[-ps],root=[+tr]];[tm=j_i,vc=[+cs]]

## get the class
.cv -> A.cv        [:]    [root=[cls=A]];[root=[cls=Ap],vc=[-ps]];[root=[cls=Ap],vc=[-cs]]
.cv -> B.cv        [:]    [root=[cls=B]];[root=[cls=Ap],vc=[+ps,+cs]]
.cv -> C.cv        [:]    [root=[cls=C]]
.cv -> D.CV        [:]    [root=[cls=D]]
.cv -> E.CV        [:]    [root=[cls=E]];[root=[cls=F]]

.y -> A.y          [:]    [root=[cls=A]]
.y -> B.y          [:]    [root=[cls=B]]
.y -> C.y          [:]    [root=[cls=C]]
.y -> E.y          [:]    [root=[cls=E]];[root=[cls=F]]

### A class
## strong verbs
# 2nd to last consonant
# skip mutation
A.cv -> A.cvc1    [:.]
A.T -> A.T1       [/:]
A.Te -> A.Te1     [/:]
A.cv -> A.cvc1    [/:]   [tm=prf];[tm=imf,vc=[+ps]]
A.cv -> A.cvc1    [:]    [tm=imf,vc=[-ps]];[tm=j_i]
A.T1 -> A.cvc     [r]
A.Te1 -> A.cvc    [YY-r]
A.cvc1 -> A.cvc   [YY]
A.cvc -> A.cvcv   [:]     [tm=j_i,vc=[-ps]]
A.cvc -> A.cvcv   [e:]    [tm=prf];[tm=imf];[tm=j_i,vc=[+ps]]
A.cvcv -> voice   [YY]

## weak A verbs

# final y
# last vowel
# palatalize final e in tr j_i: sTe->sTE (what about passive j_i?); go to strong template
A.y -> A.cv       [E:]   [tm=j_i,root=[-tr]]
# palatalize elsewhere
A.y -> A.yv       [e:]   [tm=prf];[tm=imf,vc=[+ps]];[tm=j_i,vc=[+ps]]
A.y -> A.yv       [:]    [tm=imf,vc=[-ps]];[tm=j_i,vc=[-ps],root=[+tr]]
# palatalize the final consonant
A.yv -> A.yv^     [^:]
A.yv^ -> A.yv^1   [/:]   [tm=prf];[tm=imf,vc=[+ps]]
A.yv^ -> A.yv^1   [:]    [tm=imf,vc=[-ps]];[tm=j_i]
# palatalizable final consonants
A.yv^1 -> A.cvc   [KK;DD]
# path for non-palatalizable final consonant
A.yv -> A.yv1     [/:]   [tm=prf];[tm=imf,vc=[+ps]]
A.yv -> A.yv1     [:]    [tm=imf,vc=[-ps]];[tm=j_i]
# non-palatalizable final consonants
A.yv1 -> A.yvc    [MM]
# palatalize the first consonant
A.yvc -> A.cvc    [^:]   [tm=imf];[tm=prf]
# palatalize the first vowel (I); sif
A.yvc -> A.cvc    [i:]  [tm=j_i]

# medial w
# o when the first consonant is not labializable
.c -> A.co        [o:w]  [root=[cls=A]]
# first consonant: dental
A.co -> voice       [DD]
# e or I if the first consonant is labializable
.c -> A.cw        [e:w]  [tm=prf];[tm=imf]
.c -> A.cw        [:w]   [tm=j_i]
# labialize first consonant
A.cw -> A.cW      [@:]   [root=[cls=A]]
A.cW -> voice       [LL]

# medial h
.c -> A.cvcv      [a:h]  [tm=prf,root=[cls=A],vc=[-cs]];[tm=j_i,root=[cls=A],vc=[-cs]]
.c -> A.cvcv      [e:h]  [tm=imf,root=[cls=A]];[tm=prf,root=[cls=A],vc=[+cs]];[tm=j_i,root=[cls=A],vc=[+cs]]

# medial y
.c -> A.cy        [e:y]  [tm=prf,root=[cls=A]];[tm=imf,root=[cls=A]]
.c -> A.cy        [:y]   [tm=j_i,root=[cls=A]]
A.cy -> A.c^      [^:]
# seems only velars can be palatalized
A.c^ -> voice       [KK]
.c -> A.cE        [E:y]  [root=[cls=A]]
# probably lots of these are not possible
A.cE -> voice     [AA-KK]

# initial w
A.cvcv -> voice   [w]    [tm=prf];[tm=imf];[tm=j_i,root=[+tr]];[tm=j_i,root=[-tr],sp=2]
A.cvcv -> voice   [:w]   [tm=j_i,root=[-tr],sp=1];[tm=j_i,root=[-tr],sp=3]

# initial h
A.cvc -> voice    [a:h]  [tm=prf,vc=[-cs]];[tm=imf,vc=[-cs]]
A.cvc -> voice    [e:h]  [tm=j_i,vc=[-cs]]
A.cvc -> voice    <ey:h> [tm=prf,vc=[+cs]];[tm=imf,vc=[+cs]];[tm=j_i,vc=[+cs]]

### B class
# Needed to be consistent with final y in other classes
B.y -> B.cv       [e:]   [tm=prf];[tm=imf,vc=[+ps]];[tm=j_i,vc=[+ps]]
B.y -> B.cv       [:]    [tm=imf,vc=[-ps]];[tm=j_i,vc=[-ps]]
# palatalize 2nd (velar) consonant
B.cv -> B.cv^     [^:]   [tm=prf];[tm=imf]
B.cv -> B.cv^     [:]    [tm=j_i]
B.cv^ -> B.cv^/   [/:]
B.cv^ -> B.cv^/   [:.]
B.cv^/ -> B.cvG   [KK]
B.cvG -> B.cvGv   [e:]
B.cvGv -> voice   [MM;r]
# palatalize 1st consonant (velar or coronal obstruent)
B.cv -> B.cv/     [/:]
B.cv -> B.cv/     [:.] 
B.cv/ -> B.cvc    [YY]
B.cvc -> B.cvcv   [e:]
B.cvcv -> B.cvcv^ [^:]   [tm=prf];[tm=imf]
B.cvcv -> B.cvcv^ [:]    [tm=j_i]
# for A->B causative, don't palatalize coronals
B.cvcv^ -> voice  [KK]   [root=[cls=Ap],vc=[+cs,+ps]]
B.cvcv^ -> voice  [KK;TT] [root=[cls=B]]
# palatalize first vowel
B.cv/ -> B.cvX    [DD;MM]
B.cvX -> B.cvXv   [E:]   [tm=prf];[tm=imf]
B.cvX -> AB.cvXv  <ey:>  [tm=prf];[tm=imf]
B.cvX -> B.cvXv   [e:]   [tm=j_i]
AB.cvXv -> voice  [MM;r;TT]  [root=[cls=Ap],vc=[+cs,+ps]]
B.cvXv -> voice   [MM;r]  [root=[cls=B]]

# medial w
# o when the first consonant is not labializable
.c -> B.co        [o:w]  [root=[cls=B]]
# first consonant: dental
B.co -> B.co^     [^:]   [tm=prf];[tm=imf]
B.co -> B.co^     [:]    [tm=j_i]
B.co^ -> voice    [DD]
# e or I if the first consonant is labializable
.c -> B.cw        [e:w]  [tm=prf];[tm=imf]
.c -> B.cw        [:w]   [tm=j_i]
# labialize first consonant
B.cw -> B.cW      [@:]   [root=[cls=B]]
B.cW -> voice     [LL]

## Class C
# Final y; last vowel
C.y -> C.yv        [e:]   [tm=prf];[tm=imf,vc=[+ps]];[tm=j_i,vc=[+ps]]
C.y -> C.yv        [:]    [tm=imf,vc=[-ps]];[tm=j_i,vc=[-ps]]
# Seems that C2 is always palatalizable for **y C verbs.
C.yv -> C.cv       [^:]
# C2
C.cv -> C.cvc1     [/:]   [tm=prf];[tm=imf];[tm=j_i,vc=[+ps,+cs]]
# also geminated for some verbs (C:zbt)?
C.cv -> C.cvc1     [:]    [tm=j_i]
C.cvc1 -> C.cvc    [YY]
# V1, always a
C.cvc -> C.cvcv    [a:]
C.cvcv -> voice    [RR]

## Class D
# C2 (always geminated)
D.CV -> D.CV/      [/:]
D.CV -> D.CV/      [:.]
D.CV/ -> D.CVC     [RR]
# V1 (e followed labialized, o following unlabialized consonants)
D.CVC -> D.CVCe    [e:]
D.CVCe -> D.CVCe@  [@:]
D.CVCe@ -> voice   [LL]
D.CVC -> D.CVCo    [o:]
D.CVCo -> voice    [CC-LL]

## Class E, F
# final y, last vowel
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
# V2: always a for class F, e or 0 for class E
E.CVC -> E.CVCV     [a:]   [root=[cls=F]]
E.CVC -> E.CVCV     [e:]   [tm=prf,root=[cls=E]];[tm=imf,root=[cls=E]]
E.CVC -> E.CVCV     [:]    [tm=j_i,root=[cls=E]]
# C2
E.CVCV -> E.CVCVC   [AA]
# V1
E.CVCVC -> E.CVCVCV [e:]   [tm=j_i,root=[cls=E]]
E.CVCVC -> E.CVCVCV [:]    [root=[cls=F]];[tm=imf];[tm=prf]
# C1
E.CVCVCV -> voice   [AA]

voice -> end        [:]    [vc=[-ps,-cs]]
voice -> end        [a:]   [vc=[+cs,-ps]]
voice -> end        <*t:>  [vc=[+ps,-cs]]
voice -> end        <ta:>  [vc=[+ps,+cs]]

end ->
