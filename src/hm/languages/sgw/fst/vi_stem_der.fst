## Chaha root -> derivational stems
## Features:
## vc: [+-ps, +-cs]; as: smp, rc, it; tm: imf, j_i, con1, con2, fut1, fut2
## Root types:
## Aqtl, Bqtl, Cqtl, DqWtl, (qll), Eqlmg, (qlql), (qltt), nqlmg, qlamg?
## Weak roots: h**, *h*, **h; *y*, **y; w**, *w*
## Operates right-to-left over roots

-> start

### final consonant

start -> .c        [ZZ]
start -> .h        [:h]
# for -o, -ema, and impersonal, don't palatalize these verbs (Kry, etc.)
start -> .c        [:y]    [sp=2|3,sn=2];[sp=None]
start -> .y        [:y]    [sp=1];[sn=1]

.h -> .cv          [a:]
.c -> .cv          [e:]   [vc=[+ps,-cs]]
.c -> .cv          [:]    [vc=[-ps]];[vc=[+cs]]

## get the class
.cv -> A.cv        [:]    [root=[cls=A]];[root=[cls=Ap],vc=[-ps]];[root=[cls=Ap],vc=[-cs]]
.cv -> B.cv        [:]    [root=[cls=B]];[root=[cls=Ap],vc=[+ps,+cs]]
.cv -> C.cv        [:]    [root=[cls=C],as=None|it]
.cv -> D.CV        [:]    [root=[cls=D]]
.cv -> E.CV        [:]    [root=[cls=E|F],as=None]

.y -> A.y          [:]    [root=[cls=A]]
.y -> B.y          [:]    [root=[cls=B]]
.y -> C.y          [:]    [root=[cls=C],as=None|it]
.y -> E.y          [:]    [root=[cls=E|F],as=None]

### A class

## strong verbs
# skip mutation
A.cv -> A.cvc1    [:.]
A.cv -> A.cvc1    [/:]   [vc=[+ps]];[as=it]
A.cv -> A.cvc1    [:]    [vc=[-ps],as=None|rc]
# C2
A.cvc1 -> A.cvc   [YY]
# V1
# assume both e and a are possible for frequentative (as=it)
A.cvc -> A.cvcv   [e:]    [as=None];[as=it]
A.cvc -> A.cvcv   [a:]    [as=rc,vc=[+ps]];[as=rc,vc=[+cs]];[as=it]
# duplicated consonant in frequentative
A.cvcv -> A.cvcvD [D:]    [as=it]
A.cvcvD -> pre_n  [YY]
A.cvcv -> pre_n   [YY]    [as=None|rc]

## weak A verbs

# final y
# palatalize last vowel
A.y -> A.yv       [e:]   [vc=[+ps]]
A.y -> A.yv       [:]    [vc=[-ps]]
# palatalize the final consonant
A.yv -> A.yv^     [^:]
A.yv^ -> A.yv^1   [/:]   [vc=[+ps]]
A.yv^ -> A.yv^1   [:]    [vc=[-ps]]
# palatalizable final consonants
A.yv^1 -> A.cvc   [KK;DD]
# path for non-palatalizable final consonant
A.yv -> A.yv1     [/:]   [vc=[+ps]]
A.yv -> A.yv1     [:]    [vc=[-ps]]
# non-palatalizable final consonants
A.yv1 -> A.yvc    [MM]
# **U verbs in Banksira
A.yv1 -> A.yvW    [UU]
# palatalize the first vowel (except for qYeme)
A.yvc -> A.yvcE   [E:]   [as=None]
# first consonant is not labialized
A.yvcE -> pre_n   [ZZ;PP]
A.yvc -> A.yvcv   [e:]   [as=None]
# first consonant is labialized (Banksira **U)
A.yvcv -> pre_n   [UU]
A.yvW -> A.cvcv   [e:]   [as=None]

# medial w
# o when the first consonant is not labializable
.c -> A.co        [o:w]  [root=[cls=A]]
# first consonant: dental
A.co -> pre_n       [DD] [as=None]
A.co -> A.coD     [DD]   [as=it]
A.coD -> A.coDV   [e:]
# copy first consonant for freq
A.coDV -> pre_n   [D:]
# e or I if the first consonant is labializable
.c -> A.cw        [e:w]
# labialize first consonant
A.cw -> A.cW      [@:]   [root=[cls=A]]
A.cW -> pre_n     [LL]   [as=None]
A.cW -> A.cWD     [LL]   [as=it]
A.cWD -> A.cWDV   [e:]
# copy first consonant for freq
A.cWDV -> pre_n   [D:]

# medial h
.c -> A.cvhv      [e:h]  [as=None,root=[cls=A]]
# duplicated consonant in frequentative; ** check to make sure this works for *h*
#A.cvhv -> A.cvhvD [D:]   [as=it]
#A.cvhvD -> pre_n  [YY;w]
A.cvhv -> pre_n   [YY;w]

# medial y
# %% what about as=it?
.c -> A.cy        [e:y]  [root=[cls=A],as=None]
A.cy -> A.c^      [^:]
# seems only velars can be palatalized
A.c^ -> pre_n     [KK]
.c -> A.cE        [E:y]  [root=[cls=A],as=None]
# probably lots of these are not possible
A.cE -> pre_n     [AA-KK]

# initial w
A.cvcv -> pre_n   [w]

# initial h
A.cvc -> pre_n    [a:h]  [vc=[-cs],as=None]
A.cvc -> pre_n    <ey:h> [vc=[+cs],as=None]

### B class
# Needed to be consistent with final y in other classes
B.y -> B.cv       [e:]   [vc=[+ps]]
B.y -> B.cv       [:]    [vc=[-ps]]

# palatalize 2nd (velar) consonant
B.cv -> B.cv^     [^:]
B.cv^ -> B.cv^/   [/:]
B.cv^ -> B.cv^/   [:.]
# C2
B.cv^/ -> B.cvG   [KK]
B.cvG -> B.cvGv.D [a:;e:] [as=it]
B.cvGv.D -> B.cvGv <^D:>
B.cvG -> B.cvGv   [e:]   [as=None]
B.cvG -> B.cvGv   [a:]   [as=rc,vc=[+ps]];[as=rc,vc=[+cs]]
B.cvGv -> pre_n   [MM;r]

# palatalize 1st consonant (velar or coronal obstruent)
B.cv -> B.cv/     [/:]
B.cv -> B.cv/     [:.]
# C2
B.cv/ -> B.cvc    [YY]
B.cvc -> B.cvcV.D [a:;e:] [as=it]
B.cvcV.D -> B.cvcv [D:]
B.cvc -> B.cvcv   [e:]   [as=None]
B.cvc -> B.cvcv   [a:]   [as=rc,vc=[+ps]];[as=rc,vc=[+cs]]
B.cvcv -> B.cvcv^ [^:]
# C3
B.cvcvD -> pre_n  [KK]   [root=[cls=Ap],vc=[+cs,+ps]];[root=[cls=B]]
B.cvcvD -> pre_n  [TT]   [root=[cls=B]]
# for A->B causative, don't palatalize coronals
B.cvcv^ -> pre_n  [KK]   [root=[cls=Ap],vc=[+cs,+ps]];[root=[cls=B]]
B.cvcv^ -> pre_n  [TT]   [root=[cls=B]]

# palatalize first vowel
# C2
B.cv/ -> B.cvX    [DD;MM]
B.cvX -> B.cvXV.D [a:;e:] [as=it]
B.cvXV.D -> B.cvX [D:]
B.cvX -> B.cvXv   [E:]   [as=None]
B.cvX -> AB.cvXv  <ey:>  [as=None]
B.cvX -> B.cvXv   [a:]   [as=rc,vc=[+ps]];[as=rc,vc=[+cs]]
B.cvX -> B.cvXv   [:]    [as=it]
AB.cvXv -> pre_n  [MM;r;TT]  [root=[cls=Ap],vc=[+cs,+ps]]
B.cvXv -> pre_n   [MM;r]  [root=[cls=B]]

# medial w
# o when the first consonant is not labializable
.c -> B.co        [o:w]  [root=[cls=B],as=None]
# first consonant: dental
B.co -> B.co^     [^:]
B.co^ -> pre_n    [DD]
# e or I if the first consonant is labializable
.c -> B.cw        [e:w]
# labialize first consonant
B.cw -> B.cW      [@:]   [root=[cls=B],as=None]
B.cW -> pre_n     [LL]

### Class C
# Final y; last vowel
C.y -> C.yv        [e:]   [vc=[+ps]]
C.y -> C.yv        [:]    [vc=[-ps]]
# Seems that C2 is always palatalizable for **y C verbs.
C.yv -> C.cv       [^:]
# C2
C.cv -> C.cvc1     [/:]
C.cvc1 -> C.cvc    [YY]
# V1, always a
C.cvc -> C.cvcv    [a:]
C.cvcv -> pre_n    [RR]

### Class D
# C2 (always geminated)
D.CV -> D.CV/      [/:]
D.CV -> D.CV/      [:.]
D.CV/ -> D.CVC     [RR]
# V1 (e followed labialized, o following unlabialized consonants)
D.CVC -> D.CVCe    [e:]   [as=None]
D.CVCe -> D.CVCe@  [@:]
D.CVCe@ -> pre_n   [LL]
D.CVC -> D.CVCo    [o:]   [as=None]
D.CVCo -> pre_n    [CC-LL]

### Class E, F
# still have to handle +ps? and h in second position (shsh)

# final y, last vowel
E.y -> E.yV         [:]

# C3
# delete . indicating no gemination or introduce gemination character
E.CV -> E.CV/       [:.;/:]
E.CV/ -> E.CVC       [AA]
# *rhy (without palatalization)
# this eventually gets deleted (before plural or impersonal suffixes), but seems to be needed anyway
E.CV -> E.CVh       [e:h]
# C2 is always r
E.CVh -> E.CVCVC     [r]

# ***y
E.yV -> E.yv^       [^:]
E.yv^ -> E.yv/      [/:]
# assumes all have a velar or coronal as C3
E.yv/ -> E.CVC      [KK;DD]
# *rhy (the e was already inserted)
E.yV -> E.yVh       [e:h]
# palatalized r
E.yVh -> E.CVCVC    [y:r]

# V2: always a for class F, e or 0 for class E
E.CVC -> E.CVCV     [a:]   [root=[cls=F]]
E.CVC -> E.CVCV     [e:]   [root=[cls=E]]
# *h**: C2+V2(+V1) => a (shsh => sasa)
E.CVC -> E.CVCVC    [a:h]

# C2
E.CVCV -> E.CVCVC   [AA]

# C1
E.CVCVC -> pre_n   [AA]

pre_n -> pre_n1     [n]
pre_n1 -> voice     [:]
pre_n -> voice      [:]

voice -> end        [:]    [vc=[-ps,-cs]]
voice -> end        [a:]   [vc=[+cs,-ps]]
voice -> end        [t:]   [vc=[+ps,-cs]]
voice -> end        <ta:>  [vc=[+ps,+cs]]

end ->
