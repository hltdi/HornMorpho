# imperfect and jussive/imperative 2 person singular feminine suffix's effect on the verb stem

-> start

# doesn't apply
start -> start        [XX;^;/;@] [sp=1];[sp=3];[sp=None];[sg=m];[sp=2,sn=2,sg=f];[tm=prf]

# does apply
start -> pal          [:]     [sp=2,sn=1,sg=f,tm=imf];[sp=2,sn=1,sg=f,tm=j_i]

# do nothing if the final consonant or vowel is already palatalized or will be.
pal -> fin            [PP;^;E]

# Condition A: final a is palatalized without affecting further palatalization (but has to be treated separately)
pal -> pal_a          [e:a]
# palatalize final consonant (before -a)
pal_a -> pal_aP       [^:]
pal_aP -> pal_aP/     [/]
pal_aP/ ->  fin       [TT;GG]
# non-mutated r can be palatalized, but not mutated r (n)
pal_aP -> fin         [DD;GG]

pal_a -> pal_a/       [/]
pal_a/ -> pal_aC      [BB;r]
pal_a -> pal_aC       [BB]
pal_aC -> pal_aCV     [V;:]
# -2 (C*h) consonant is velar, palatalizable
pal_aCV -> pal_aCVP   [^:]
pal_aCVP -> fin       [GG]

# -2 (C*h) consonant is dental or labial
# palatalize vowel *V*h
pal_aC -> pal_aCi    [E:e;:i]
pal_aCi -> pal_aCi   [/]
pal_aCi -> fin       [DD;BB]

## -2 (C*h) consonant is r or labial
#pal_aCV -> pal_aCVC   [r;BB]
## -3 (C**h) consonant (quadrilateral with -h) is velar, palatalizable
#pal_aCVC -> pal_aCVCP [^:]
#pal_aCVCP -> fin      [GG]
## -2 consonant is dental; stop looking
#pal_aCV -> fin        [DD]

# Condition 1: palatalize final coronal (including r but not n) or velar
pal -> pal1           [^:]
pal1 -> fin           [DD;GG]

# Condition 2: palatalize last velar that's not palatalized unless there's an intervening coronal
# last consonant can't be palatalized
pal -> pal2           [BB;n]
pal2 -> pal2v         [V;:]
# palatalize a velar in position -2
pal2v -> pal2v^       [^:]
pal2v^ -> pal2v^      [/]
pal2v^ -> fin         [GG]

# or if it's a labial(?) or r, look in position -3
pal2v -> pal2v/       [/;:]
pal2v/ -> pal2vc      [r;BB]
pal2vc -> pal2vcv     [V;:]
pal2vcv -> pal2vcvP   [^:]
# palatalize a velar in position -3
pal2vcvP -> fin       [GG]

# Condition 3: palatalize vowel after the second-to-last consonant, when nothing can be palatalized
# TEn, tCEn <Tny>
pal -> pal/           [/]
pal -> pal3           [BB]
# final mutated r -> n; don't palatalize
pal/ -> pal3          [r;BB]
# vowel palatalization (vowel may already be palatalized, at least E)
pal3 -> pal3_i        [E:e;A:a;i:;E]
# C2 could be palatalized: tCEn
pal3_i -> pal3_i      [^;/]
# dental, possibly palatalized in position 2, blocks further palatalization
pal3_i -> fin         [DD]

fin -> fin            [RG;V;^;@;/]
fin ->
start ->
