# labialization and palatalization due to
#   impersonal
#   3sm object suffix, singular subjects except 2sf

-> start

## doesn't apply
# in perfective we don't have to handle 1s, 2ms subjects because the subject suffixes are labialized: KW, KWe
# we also can avoid 3smO malefactive because the object suffix is labialized: we
# SO all plural subjects and
#    1s and 2s subjects and
#    3s subjects with 1, 2 or no objects and
#    3s subjects with 3s plural or fem objects and
#    3s subjects with 3sm malefactive objects
start -> start      [XX;^;@;=]     [sn=2];[sp=1,sn=1];[sp=2,sn=1];[sp=3,sn=1,op=1|2|None];[sp=3,sn=1,op=3,on=2];[sp=3,sn=1,op=3,og=f];[sp=3,sn=1,op=3,on=1,og=m,ot=m]

## applies
# 3sm object (accusative or benefactive) with 3s subjects
start -> lab0       [:]    [op=3,og=m,on=1,ot=a,sn=1,sp=3];[op=3,og=m,on=1,ot=b,sn=1,sp=3]
# impersonal
start -> imp        [:]    [sp=None]

# find the end of the stem
lab0 -> lab0        [XX]
lab0 -> lab         [=]

# impersonal
imp -> imp          [X;V]
# bekewim
imp -> imp_i         [i]
# benefactive, malefactive
imp_i -> imp        [p;n]

# optionally (obligatory in Gumer?? AND FOR GENERATION) insert w following -e of
# **y root; no more labialization necessary
imp_i -> imp_i=     [=]
imp_i= -> pal_w     [w:]
# bekewim
pal_w -> pal_we.C   [e]
pal_we.C -> fin     [X]
# srawim
pal_w -> pal_we.a   [:e]
pal_we.a -> fin     [a]
# no initial i suffix
imp -> pal          [=]
# initial i suffix but no stem-final e
imp_i= -> pal       [:]

### final vowel
## imp: palatalize final -a; delete final e
pal -> palV        [e:a;:e]
# final vowel already palatalized (how can this happen?); in any case this is wrong because labialization also needs to happen
pal -> fin         [E]
palV -> palVP      [^:]
# palatalize final dental; go on to labialize other
palVP -> labC      [TT]

## consonant preceding -a
# not palatalized
palV -> palVnP      [:]
# impers: don't palatalize GG or BB or r; labialize BB and GG
palV -> labV       [@:]      [sp=None]
labV -> fin        [BB;GG]
# -ra / -na: no palatalization in impers; look for labializable C elsewhere
palVnP -> labC      [r;n]   [sp=None]

### final consonant
## already palatalized
pal -> pal^        [^]
# impers: look for consonant to labialize starting with C-2
pal^ -> labC       [GG;TT]   [sp=None]
pal -> labC        [PP]      [sp=None]

## palatalize final coronal (including r but not n) or velar
pal -> palCP          [^:]
palCP -> labC         [TT]       [sp=None]

## 3smO; ignore final vowel
# don't palatalize final dental
lab -> lab          [e;a;E;A]
lab -> labC         [DD;n]
# pass over already palatalized consonant
lab -> lab^         [^]
lab^ -> labC        [MM;KK;DD;n]
## labialize final labial or velar
# impers
pal -> lab1         [@:]      [sp=None]
# 3sm0
lab -> lab1         [@:]
lab1 -> fin         [MM;KK]
# r/n: only case where final consonant is unaffected for impers;
# keep looking for labializable consonant
pal -> labC         [r;n]        [sp=None]

### labialize C2
labC -> labC           [a;e;o;E;A]
labC -> labC=          [=]
labC -> labCl          [@:]
labCl -> fin           [KK;MM]
# already labialized or labialize C1
labC -> labCnl         [:]
labCnl -> fin          [UU]
labCnl -> labCC        [DD;n]
# already palatalized C1/2
labC -> fin            [^]

### labialize C1
# no C1
labCC -> fin           [=]
# V1
labCC -> labCC         [a;e;o;E;A]
labCC -> labCCl        [@:]
labCCl -> fin          [KK;MM]
# already labialized or unlabializable
labCC -> labCCnl       [:]
labCCnl -> fin         [UU;DD;PP]

fin -> fin             [X;V;^;@;=]

fin ->
start ->
# ojim
labC= ->
