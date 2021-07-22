## Realize 1 as impersonal palatalization
## Realize 2 as 2sf subject palatalization

-> start

start -> start    [X;V;*;=;^;@;4]

#### 2sf palatalization

## last vowel and consonant
start -> pal2_     [:2]
pal2_ -> pal2      [=]

pal2 -> pal2V      [e:a;E:e]
pal2 -> start      [E]
pal2V -> pal2VP    [^:]
pal2VP -> start    [DD;GG;l]
pal2V -> start     [^;PP]
pal2V -> pal2C     [BB;n]

pal2 -> start      [^;PP]
pal2 -> pal2P      [^:]
pal2P -> start     [DD;GG;l]
pal2 -> pal2C      [BB;n]

## vowel before last consonant
# palatalize (tket<i>f) ...
pal2C -> pal2Ci    [E:e;i:;E;A:a]
# ... following dental or labial (tke<t>if) or already palatalized cons (tCEn)
pal2Ci -> start    [DD;BB;n;^]
# otherwise leave vowel unchanged if there is one ...
pal2C -> pal2CV    [V;:]
# ... and palatalize preceding velar
pal2CV -> pal2C^   [^:]
pal2C^ -> start    [GG]
# beginning of stem
pal2C -> start     [=]
pal2CV -> start    [=]

## if 2nd to last consonant is labial(?), r, or n, alternative is ...
pal2CV -> pal2CC   [BB;r;n]
pal2CC -> pal2CCV  [V;:]
# ... palatalizing a preceding velar
pal2CCV -> pal2CC^ [^:]
pal2CC^ -> start   [GG]

#### impersonal palatalization

start -> pal0      [:1]
# ignore labializer
pal0 -> pal0       [4]
pal0 -> pal        [=]

### final vowel
## imp: palatalize final -a; delete final e
pal -> palV        [e:a;:e]
# final vowel already palatalized (how can this happen?)
pal -> start        [E]
palV -> palVP      [^:]
# palatalize dental preceding final vowel
palVP -> start       [TT]

## consonant preceding final vowel not palatalized
palV -> start        [BB;GG;r;n]

### final consonant
## already palatalized
pal -> start        [^;PP]

## palatalize final coronal (excluding r and n)
pal -> palCP          [^:]
palCP -> start        [TT]

## final labial or velar (including labialized ones), r, n: no palatalization
pal -> start         [BB;GG;r;n]

start ->
