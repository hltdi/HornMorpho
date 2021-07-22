# labialization and palatalization due to
#   imperfect and jussive/imperative 2 person singular feminine
#   impersonal
#   3sm object suffix, singular subjects except 2sf

-> start

## doesn't apply
# subject: 1 or 3; object: none or plural or 1, 2 sing or 3sf or 3smM
start -> sp13       [XX;^;@;=]     [sp=1|3,sn=1,fut=None];[sp=1|3,sn=1,fut=def]
sp13 -> start       [:]            [op=None];[on=2];[op=1];[op=2];[op=3,og=f];[op=3,og=m,on=1,ot=m]
# subject: 2sm, object: none or plural or 3sf or 3smM
start -> sp2s       [XX;^;@;=]     [sp=2,sn=1]
sp2s -> start       [:]            [op=None];[on=2];[op=1];[op=3,og=f];[op=3,og=m,on=1,ot=m]
# subject: 2sf, tm: perfective; or any plural subject
start -> start      [XX;^;@;=]     [sn=2]

## applies
# 3sm object
start -> lab0       [:]    [op=3,og=m,on=1,ot=a,sn=1,sp=1|3];[op=3,og=m,on=1,ot=a,sn=1,sp=2,sg=m];[op=3,og=m,on=1,ot=b,sn=1,sp=1|3];[op=3,og=m,on=1,ot=b,sn=1,sp=2,sg=m]
# 2sf
# start -> pal0       [:]    [sp=2,sn=1,sg=f]
# impersonal
start -> imp        [:]    [sp=None]

# impersonal
imp -> imp          [X;V]
imp -> labI         [=]
labI -> labI^       [^]
labI^ -> labI       [X]
labI -> labI        [PP;DD;n;V]
labI -> labI1       [@:]
labI1 -> fin        [MM;KK]
labI -> fin         [UU;=]

pal0 -> pal0        [XX]
pal0 -> pal         [=]
### final vowel
## 2sf/imp: palatalize final -a
pal -> palV        [e:a]
# impersonal has -wi for this case
pal -> palV        [e]        [sp=2,sn=1,sg=f]
# final vowel already palatalized
pal -> fin         [E]
palV -> palVP      [^:]
# palatalize final dental (done for 2sf, continue for impers)
palVP -> fin       [TT]      [sp=2,sn=1,sg=f]
# palatalize final velar for 2sf (but non impers)
palVP -> fin       [GG]       [sp=2,sn=1,sg=f]
# final non-mutated r can be palatalized for 2sf (but not impers)
palVP -> fin       [r]        [sp=2,sn=1,sg=f]
## consonant preceding -a
# not palatalized
palV -> palVnP      [:]
palVnP -> palVC     [BB;n]    [sp=2,sn=1,sg=f]
palVC -> palVCV     [V;:]
# 2sf: palatalize previous consonant
palVCV -> palVCVP   [^:]
palVCVP -> fin      [GG]
# 2sf: palatalize previous vowel
palVC -> palVCi     [E:e;:i]
palVCi -> fin       [DD;BB]

### final consonant
## already palatalized
pal -> pal^        [^]
# 2sf: we're done
pal^ -> fin        [GG;DD]    [sp=2,sn=1,sg=f]
pal -> fin         [PP]      [sp=2,sn=1,sg=f]

## palatalize final coronal (including r but not n) or velar
pal -> palCP          [^:]
palCP -> fin          [DD;GG]    [sp=2,sn=1,sg=f]
# look elsewhere for palatalization for 2sf
pal -> pal2           [BB;n]     [sp=2,sn=1,sg=f]

### palatalize last velar that's not palatalized unless there's an intervening coronal
# last consonant can't be palatalized
pal2 -> pal2v         [V;:]
# palatalize a velar in position -2
pal2v -> pal2v^       [^:]
pal2v^ -> fin         [GG]

# or if it's a labial(?) or r/n, look in position -3
pal2v -> pal2vc       [r;n;BB]
pal2vc -> pal2vcv     [V;:]
pal2vcv -> pal2vcvP   [^:]
# palatalize a velar in position -3
pal2vcvP -> fin       [GG]

### palatalize vowel after the second-to-last consonant, when nothing can be palatalized
## TEn, tCEn <Tny>
pal -> pal3           [n;BB]    [sp=2,sn=1,sg=f]
# vowel palatalization (vowel may already be palatalized, at least E)
pal3 -> pal3_i        [E:e;A:a;i:;E]
# C2 could be palatalized: tCEn
pal3_i -> pal3_i      [^]
# dental, possibly palatalized in position 2, blocks further palatalization
pal3_i -> fin         [DD;n]

# find the end of the stem
lab0 -> lab0        [XX]
lab0 -> lab         [=]

## 3smO; don't palatalize final dental
lab -> lab          [e;a;E;A]
lab -> labC         [DD;n]
# final stem consonant is palatalized before 3smO
lab -> lab^         [^]
lab^ -> labC        [X]
# 3sm0
lab -> lab1         [@:]
lab1 -> fin         [MM;KK]

labV -> fin        [BB;GG]

### labialize C2
labC -> labC           [a;e;o;E;A]
labC -> labC=          [=]
labC -> labCl          [@:]
labCl -> fin           [KK;MM]
# already labialized or labialize C1
labC -> labCnl         [:]
labCnl -> fin          [UU]
labCnl -> labCC        [DD;n]
labCC -> labCC=        [=]
# already palatalized C1/2
labC -> fin            [^]

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
# y=uj=i
labC= -> labC=        [X;V]
labC= ->
# y=coc=i
labCC= -> labCC=      [X;V]
labCC= ->
