# labialization and palatalization due to
#   imperfect and jussive/imperative 2 person singular feminine
#   impersonal
#   3sm object suffix, singular subjects except 2sf

-> start

## doesn't apply
# subject: 1,3; object: none or plural or 1, 2 sing or 3sf or 3smM
start -> sp123      [XX;^;@;=]     [sp=1|3]
sp123 -> start      [:]            [op=None];[on=2];[op=1];[op=2];[op=3,og=f];[op=3,og=m,on=1,ot=m]
# subject: 2sm, object: none or plural or 1 or 3sf or 3smM
start -> sp2sm      [XX;^;@;=]     [sp=2,sn=1,sg=m]
sp2sm -> start      [:]            [op=None];[on=2];[op=1];[op=3,og=f];[op=3,og=m,on=1,ot=m]
# subject: 2sf or any plural subject
start -> start      [XX;^;@;=]     [sp=2,sn=1,sg=f];[sn=2]

## applies
# 3sm object
start -> lab0       [:]    [op=3,og=m,on=1,ot=a,sn=1,sp=1|3];[op=3,og=m,on=1,ot=a,sn=1,sp=2,sg=m];[op=3,og=m,on=1,ot=b,sn=1,sp=1|3];[op=3,og=m,on=1,ot=b,sn=1,sp=2,sg=m]
# impersonal
start -> imp        [:]    [sp=None]

# find the end of the stem
lab0 -> lab0        [XX]
lab0 -> lab         [=]

# impersonal
imp -> imp          [X;V-i]
imp -> imp_i        [i]
imp_i -> imp_wi     [w:]
imp_wi -> imp=wi    [=]
imp=wi= -> fin      [e]

imp_i -> pal        [=]

### final vowel
## imp: palatalize final -a
pal -> palV        [e:a]
# final vowel already palatalized
pal -> fin         [E]
palV -> palVP      [^:]
# palatalize final dental
palVP -> fin       [TT]

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

## 3smO; don't palatalize final dental
lab -> lab          [e;a;E;A]
lab -> labC         [DD;n]
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
labC -> labCl          [@:]
labCl -> fin           [KK;MM]
# already labialized or labialize C1
labC -> labCnl         [:]
labCnl -> fin          [UU]
labCnl -> labCC        [DD;n]

### labialize C1
labCC -> labCC           [a;e;o;E;A]
labCC -> labCCl          [@:]
labCCl -> fin            [KK;MM]
# already labialized or unlabializable
labCC -> labCCnl         [:]
labCCnl -> fin           [UU;DD;PP]

fin -> fin            [X;V;^;@;=]

fin ->
start ->
