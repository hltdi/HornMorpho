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
start -> .c        [t;d;T] [tm=imf|j_i,root=[cls=A]];[root=[cls=Ap|B|C|D|E|F]]
# need these for <wrd> => wende
start -> .T        [t;d;T] [tm=prf,root=[cls=A]]
start -> .h        [:h]
start -> .c        [:y]    [tm=prf,sp=3,sn=2];[tm=imf,sp=2|3,sn=2];[tm=j_i,sp=2|3,sn=2];[sp=None]
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
.cv -> E.CV        [:]    [root=[cls=E|F]]

.y -> A.y          [:]    [root=[cls=A]]
.y -> B.y          [:]    [root=[cls=B]]
.y -> C.y          [:]    [root=[cls=C]]
.y -> E.y          [:]    [root=[cls=E|F]]

### A class

## strong verbs
#{ these are needed to handle deletion of e in wendem
A.T -> A.T1       [/:]
A.Te -> A.Te1     [/:]
A.T1 -> A.cvc     [r]
A.Te1 -> A.cvc    [YY-r]
#}
# skip mutation
A.cv -> A.cvc1    [:.]
A.cv -> A.cvc1    [/:]   [tm=prf];[tm=imf,vc=[+ps]];[tm=imf,as=it]
A.cv -> A.cvc1    [:]    [tm=imf,vc=[-ps],as=None|rc];[tm=j_i]
# C2
A.cvc1 -> A.cvc   [YY]
# V1
A.cvc -> A.cvcv   [:]     [tm=j_i,vc=[-ps],as=None]
# assume both e and a are possible for frequentative (as=it)
A.cvc -> A.cvcv   [e:]    [tm=imf|prf,as=None];[tm=j_i,vc=[+ps],as=None];[as=it]
A.cvc -> A.cvcv   [a:]    [as=rc,vc=[+ps]];[as=rc,vc=[+cs]];[as=it]
# duplicated consonant in frequentative
A.cvcv -> A.cvcvD [D:]    [as=it]
A.cvcvD -> voice  [YY]
A.cvcv -> voice   [YY]    [as=None|rc]

## weak A verbs

# final y
# last vowel
# palatalize final e in tr j_i: sTe->sTE (what about passive j_i?); go to strong template
A.y -> A.cv       [E:]   [tm=j_i,root=[-tr]]
# palatalize elsewhere
A.y -> A.yv       [e:]   [tm=prf];[tm=imf|j_i,vc=[+ps]]
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
# palatalize the first vowel (except for qYeme)
A.yvc -> A.cvcv   [E:]   [tm=imf|prf]
# palatalize the first vowel (I); sif
A.yvc -> A.cvcv   [i:]  [tm=j_i]

# medial w
# o when the first consonant is not labializable
.c -> A.co        [o:w]  [root=[cls=A],as=None]
# first consonant: dental
A.co -> voice       [DD]
# e or I if the first consonant is labializable
.c -> A.cw        [e:w]  [tm=prf|imf]
.c -> A.cw        [:w]   [tm=j_i]
# labialize first consonant
A.cw -> A.cW      [@:]   [root=[cls=A],as=None]
A.cW -> voice       [LL]

# medial h
.c -> A.cvcv      [a:h]  [tm=prf|j_i,root=[cls=A],vc=[-cs]]
.c -> A.cvcv      [e:h]  [tm=imf,root=[cls=A]];[tm=prf|j_i,root=[cls=A],vc=[+cs]]

# medial y
.c -> A.cy        [e:y]  [tm=imf|prf,root=[cls=A]]
.c -> A.cy        [:y]   [tm=j_i,root=[cls=A]]
A.cy -> A.c^      [^:]
# seems only velars can be palatalized
A.c^ -> voice       [KK]
.c -> A.cE        [E:y]  [root=[cls=A]]
# probably lots of these are not possible
A.cE -> voice     [AA-KK]

# initial w
A.cvcv -> voice   [w]    [tm=imf|prf];[tm=j_i,root=[+tr]];[tm=j_i,root=[-tr],sp=2]
A.cvcv -> voice   [:w]   [tm=j_i,root=[-tr],sp=1|3]

# initial h
A.cvc -> voice    [a:h]  [tm=prf,vc=[-cs]];[tm=imf,vc=[-cs]]
A.cvc -> voice    [e:h]  [tm=j_i,vc=[-cs]]
A.cvc -> voice    <ey:h> [tm=prf,vc=[+cs]];[tm=imf,vc=[+cs]];[tm=j_i,vc=[+cs]]

### B class
# Needed to be consistent with final y in other classes
B.y -> B.cv       [e:]   [tm=prf];[tm=imf|j_i,vc=[+ps]]
B.y -> B.cv       [:]    [tm=imf|j_i,vc=[-ps]]

# palatalize 2nd (velar) consonant
B.cv -> B.cv^     [^:]   [tm=prf|imf];[tm=j_i,as=it]
B.cv -> B.cv^     [:]    [tm=j_i,as=None|rc]
B.cv^ -> B.cv^/   [/:]
B.cv^ -> B.cv^/   [:.]
# C2
B.cv^/ -> B.cvG   [KK]
B.cvG -> B.cvGv.D [a:;e:] [as=it]
B.cvGv.D -> B.cvGv <^D:>
B.cvG -> B.cvGv   [e:]   [as=None]
B.cvG -> B.cvGv   [a:]   [as=rc,vc=[+ps]];[as=rc,vc=[+cs]]
B.cvGv -> voice   [MM;r]

# palatalize 1st consonant (velar or coronal obstruent)
B.cv -> B.cv/     [/:]
B.cv -> B.cv/     [:.]
# C2
B.cv/ -> B.cvc    [YY]
B.cvc -> B.cvcV.D [a:;e:] [as=it]
B.cvcV.D -> B.cvcv [D:]
B.cvc -> B.cvcv   [e:]   [as=None]
B.cvc -> B.cvcv   [a:]   [as=rc,vc=[+ps]];[as=rc,vc=[+cs]]
B.cvcv -> B.cvcv^ [^:]   [tm=prf|imf];[tm=j_i,as=it]
B.cvcv -> B.cvcv^ [:]    [tm=j_i,as=None|rc]
B.cvcvD -> voice  [KK]   [root=[cls=Ap],vc=[+cs,+ps]];[root=[cls=B]]
B.cvcvD -> voice  [TT]   [root=[cls=B]]
# for A->B causative, don't palatalize coronals
B.cvcv^ -> voice  [KK]   [root=[cls=Ap],vc=[+cs,+ps]];[root=[cls=B]]
B.cvcv^ -> voice  [TT]   [root=[cls=B]]

# palatalize first vowel
# C2
B.cv/ -> B.cvX    [DD;MM]
B.cvX -> B.cvXV.D [a:;e:] [as=it]
B.cvXV.D -> B.cvX [D:]
B.cvX -> B.cvXv   [E:]   [tm=prf|imf,as=None]
B.cvX -> AB.cvXv  <ey:>  [tm=prf|imf,as=None]
B.cvX -> B.cvXv   [e:]   [tm=j_i,as=None|rc]
B.cvX -> B.cvXv   [a:]   [as=rc,vc=[+ps]];[as=rc,vc=[+cs]]
B.cvX -> B.cvXv   [:]    [as=it]
AB.cvXv -> voice  [MM;r;TT]  [root=[cls=Ap],vc=[+cs,+ps]]
B.cvXv -> voice   [MM;r]  [root=[cls=B]]

# medial w
# o when the first consonant is not labializable
.c -> B.co        [o:w]  [root=[cls=B],as=None]
# first consonant: dental
B.co -> B.co^     [^:]   [tm=prf|imf];[tm=j_i,as=it]
B.co -> B.co^     [:]    [tm=j_i,as=None|rc]
B.co^ -> voice    [DD]
# e or I if the first consonant is labializable
.c -> B.cw        [e:w]  [tm=prf|imf]
.c -> B.cw        [:w]   [tm=j_i]
# labialize first consonant
B.cw -> B.cW      [@:]   [root=[cls=B],as=None]
B.cW -> voice     [LL]

### Class C
# Final y; last vowel
C.y -> C.yv        [e:]   [tm=prf];[tm=imf|j_i,vc=[+ps]]
C.y -> C.yv        [:]    [tm=imf|j_i,vc=[-ps]]
# Seems that C2 is always palatalizable for **y C verbs.
C.yv -> C.cv       [^:]
# C2
C.cv -> C.cvc1     [/:]   [tm=prf|imf];[tm=j_i,vc=[+ps,+cs]]
# also geminated for some verbs (C:zbt)?
C.cv -> C.cvc1     [:]    [tm=j_i]
C.cvc1 -> C.cvc    [YY]
# V1, always a
C.cvc -> C.cvcv    [a:]
C.cvcv -> voice    [RR]

### Class D
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

### Class E, F
# still have to handle +ps? and h in second position (shsh)

# final y, last vowel
E.y -> E.yV         [e:]   [tm=prf]
E.y -> E.yV         [:]    [tm=imf|j_i]

# C3

#{ separate j_i, dup=2: special rules (yededg, yegekm)
E.CV -> E.CVj       [:]    [tm=j_i,dup=2]
E.CV -> E.CVn       [:]    [tm=prf|imf];[dup=None|1]

E.CVj -> E.CVjn     [:.]
E.CVj -> E.CVjg     [:]
E.CVjg -> E.CVjg1   [/:]

E.CVjg1 -> E.CVjgD   [TT]
E.CVjg -> E.CVjD     [TT]
E.CVjn -> E.CVjnD    [TT]
E.CVjnD -> E.CVCVC   [:k;:g;:K;:q;:m;:f;:b]
E.CVjgD -> E.CVCVC   [:k;:g;:K;:q;:m;:f;:b]
E.CVjnD -> E.CVCVC   [DD]
E.CVjD  -> E.CVCVC   [DD]
E.CVjD -> E.CVCVCV   [a:h]

E.CVjg1 -> E.CVjgB  [BB;GG;r]
E.CVjg -> E.CVjB    [BB;GG;r]
E.CVjn -> E.CVjnB   [BB;GG;r]
E.CVjnB -> E.CVCVC  [:m;:f;:b]
E.CVjgB -> E.CVCVC  [:m;:f;:b]
E.CVjnB -> E.CVCVC  [DD;GG]
E.CVjB -> E.CVCVC   [DD;GG]
E.CVjB -> E.CVCVCV  [a:h]
}# end of special rules for j_i, dup=2

# C3
E.CVn -> E.CV/       [:.]
E.CVn -> E.CV/       [/:]   [tm=prf|imf]
E.CVn -> E.CV/       [:]    [tm=j_i]
E.CV/ -> E.CVC       [AA]

# ***y
E.yV -> E.yv^       [^:]
E.yv^ -> E.yv/      [/:]   [tm=prf|imf]
# assumes all have a velar or coronal as C3
E.yv/ -> E.CVC      [KK;DD]
E.yv^ -> E.CVC      [KK;DD] [tm=j_i]

# V2: always a for class F, e or 0 for class E
E.CVC -> E.CVCV     [a:]   [root=[cls=F]]
E.CVC -> E.CVCV     [e:]   [tm=prf|imf,root=[cls=E]]
E.CVC -> E.CVCV     [:]    [tm=j_i,root=[cls=E]]
# *h**: C2+V2+V1 => a (shsh => sasa)
E.CVC -> E.CVCVCV   [a:h]

# C2
E.CVCV -> E.CVCVC   [AA]

# V1
E.CVCVC -> E.CVCVCV [e:]   [tm=j_i,root=[cls=E]]
E.CVCVC -> E.CVCVCV [:]    [root=[cls=F]];[tm=prf|imf]

# C1
E.CVCVCV -> voice   [AA]

voice -> end        [:]    [vc=[-ps,-cs]]
voice -> end        [a:]   [vc=[+cs,-ps]]
voice -> end        <*t:>  [vc=[+ps,-cs]]
voice -> end        <ta:>  [vc=[+ps,+cs]]

end ->
