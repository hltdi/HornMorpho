## Chaha root -> derivational stems for infinitive: j_i, 3sm form
## Features:
## vc: [+-ps, +-cs]; as: smp, rc, it; tp: we, ot
## Root types:
## Aqtl, Bqtl, Cqtl, DqWtl, (qll), Eqlmg, (qlql), (qltt), nqlmg, qlamg?
## Weak roots: h**, *h*, **h; *y*, **y; w**, *w*
## Operates right-to-left over roots

-> start

### final consonant

start -> .c        [ZZ]
start -> .h        [:h]
# for -o, -ema, and impersonal, don't palatalize these verbs (Kry, etc.)
start -> .c        [:y]    [tp=ot]
start -> .y        [:y]    [tp=we]

.h -> .cv          [a:]
.c -> .cv          [e:]   [vc=[+ps,-cs]];[vc=[-cs],root=[-tr]]
.c -> .cv          [:]    [vc=[-ps],root=[+tr]];[vc=[+cs]]

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
A.cv -> A.cvc1    [:]
# C2
A.cvc1 -> A.cvc   [YY]
# V1
A.cvc -> A.cvcv   [:]     [vc=[-ps],as=None]
# assume both e and a are possible for frequentative (as=it)
A.cvc -> A.cvcv   [e:]    [vc=[+ps],as=None];[as=it]
A.cvc -> A.cvcv   [a:]    [as=rc,vc=[+ps]];[as=rc,vc=[+cs]];[as=it]
# duplicated consonant in frequentative
A.cvcv -> A.cvcvD [D:]    [as=it]
A.cvcvD -> pre_n  [YY]
A.cvcv -> pre_n   [AA]    [as=None|rc]

## weak A verbs

# final y
# last vowel
# palatalize final e in -tr j_i: sTe->sTey (what about passive j_i?); go to strong template
A.y -> A.cv       <ye:>   [root=[-tr]]
# palatalize elsewhere
A.y -> A.yv       [e:]   [vc=[+ps]]
A.y -> A.yv       [:]    [vc=[-ps],root=[+tr]]
# palatalize the final consonant
A.yv -> A.yv^     [^:]
A.yv^ -> A.yv^1   [:]
# palatalizable final consonants
A.yv^1 -> A.cvc   [KK;DD]
# path for non-palatalizable final consonant
A.yv -> A.yv1     [:]
# non-palatalizable final consonants
A.yv1 -> A.yvc    [MM]
# **U verbs in Banksira
A.yv1 -> A.yvW    [UU]
# palatalize the first vowel (except for qYeme)
A.yvc -> A.yvcE   [i:]   [as=None]
# first consonant is not labialized
A.yvcE -> pre_n   [ZZ;PP]
A.yvc -> A.yvcv   [:]   [as=None]
# first consonant is labialized (Banksira **U)
A.yvcv -> pre_n   [UU]
A.yvW -> A.cvcv   [:]    [as=None]

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
.c -> A.cw        [:w]
# labialize first consonant
A.cw -> A.cW      [@:]   [root=[cls=A]]
A.cW -> pre_n     [LL]   [as=None]
A.cW -> A.cWD     [LL]   [as=it]
A.cWD -> A.cWDV   [e:]
# copy first consonant for freq
A.cWDV -> pre_n   [D:]

# medial h
.c -> A.cvhv      [a:h]  [root=[cls=A],vc=[-cs],as=None]
.c -> A.cvhv      [e:h]  [as=None,root=[cls=A],vc=[+cs]]
A.cvhv -> pre_n   [YY;w]

# medial y
# %% what about as=it?
.c -> A.cy        [:y]   [root=[cls=A],as=None]
A.cy -> A.c^      [^:]
# seems only velars can be palatalized
A.c^ -> pre_n     [KK]
.c -> A.cE        [E:y]  [root=[cls=A],as=None]
# probably lots of these are not possible
A.cE -> pre_n     [AA-KK]

# initial h
A.cvc -> pre_n    [e:h]  [vc=[-cs],as=None]
A.cvc -> pre_n    <ey:h> [vc=[+cs],as=None]

### B class
# Needed to be consistent with final y in other classes
B.y -> B.cv       [e:]   [vc=[+ps]]
B.y -> B.cv       [:]    [vc=[-ps]]

# palatalize 2nd (velar) consonant
B.cv -> B.cv^     [^:]   [as=it]
B.cv -> B.cv^     [:]    [as=None|rc]
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
B.cvcv -> B.cvcv^ [^:]   [as=it]
B.cvcv -> B.cvcv^ [:]    [as=None|rc]
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
B.cvX -> B.cvXv   [e:]   [as=None|rc]
B.cvX -> B.cvXv   [a:]   [as=rc,vc=[+ps]];[as=rc,vc=[+cs]]
B.cvX -> B.cvXv   [:]    [as=it]
AB.cvXv -> pre_n  [MM;r;TT]  [root=[cls=Ap],vc=[+cs,+ps]]
B.cvXv -> pre_n   [MM;r]  [root=[cls=B]]

# medial w
# o when the first consonant is not labializable
.c -> B.co        [o:w]  [root=[cls=B],as=None]
# first consonant: dental
B.co -> B.co^     [^:]   [as=it]
B.co -> B.co^     [:]    [as=None|rc]
B.co^ -> pre_n    [DD]
# e or I if the first consonant is labializable
.c -> B.cw        [:w]
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
C.cv -> C.cvc1     [/:]   [vc=[+ps,+cs]]
# also geminated for some verbs (C:zbt)?
C.cv -> C.cvc1     [:]
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

#{ separate j_i, dup=2: special rules (yededg, yegekm)
E.CV -> E.CVj       [:]    [dup=2]
E.CV -> E.CVn       [:]    [dup=None|1]

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
E.CVn -> E.CV/       [:]
E.CV/ -> E.CVC       [AA]
# *rhy (without palatalization)
E.CVn -> E.CVh       [:h]
# this eventually gets deleted (before plural or impersonal suffixes), but seems to be needed anyway
# C2 is always r
E.CVh -> E.CVCVC     [r]

# ***y
E.yV -> E.yv^       [^:]
# assumes all have a velar or coronal as C3
E.yv/ -> E.CVC      [KK;DD]
E.yv^ -> E.CVC      [KK;DD]
# *rhy (the e was already inserted)
E.yV -> E.yVh       [e:h]
# palatalized r
E.yVh -> E.CVCVC    [y:r]

# V2: always a for class F, e or 0 for class E
E.CVC -> E.CVCV     [a:]   [root=[cls=F]]
E.CVC -> E.CVCV     [:]    [root=[cls=E]]
# *h**: C2+V2+V1 => a (shsh => sasa)
E.CVC -> E.CVCVCV   [a:h]

# C2
E.CVCV -> E.CVCVC   [AA]

# V1
E.CVCVC -> E.CVCVCV [e:]   [root=[cls=E]]
E.CVCVC -> E.CVCVCV [:]    [root=[cls=F]]

# C1
E.CVCVCV -> pre_n   [AA]

pre_n -> pre_n1     [n]
# if word-initial, insert I before n-***-ot
pre_n1 -> voice     [*:]   [tp=ot]
# no vowel before n-*** following we-
pre_n1 -> voice     [:]    [tp=we]
pre_n -> voice      [:]

voice -> end        [:]    [vc=[-ps,-cs]]
voice -> end        [a:]   [vc=[+cs,-ps]]
# passive is always t- following we-
voice -> end        [t:]   [vc=[+ps,-cs],tp=we]
# passive may be te- if word initial: te-***-ot
voice -> end        <*t:>  [vc=[+ps,-cs],tp=ot]
voice -> end        <ta:>  [vc=[+ps,+cs]]

end ->
