reverse

# imperfect and jussive/imperative 2 person singular feminine suffix's effect on the verb stem
-> start

# doesn't apply
start -> start        [XX;^] [sp=1];[sp=3];[sp=None];[sg=m];[sp=2,sn=2,sg=f];[tm=prf]

# does apply
start -> pal          [:]     [sp=2,sn=1,sg=f,tm=imf];[sp=2,sn=1,sg=f,tm=j_i]

# do nothing if the final consonant is already palatalized
pal -> fin            [PP]

# Condition A: final a is palatalized without affecting further palatalization (but has to be treated separately)
pal -> pal_a          [^:]
pal_a -> pal_a.       [a]
pal_a. -> pal_aP      [^:]
pal_aP -> fin         [DD;GG]
# -1 (*Ch) consonant is not palatalizable
pal_a. -> pal_aC      [RG-DD,GG]
pal_aC -> pal_aCV     [V;:]
# -2 (C*h) consonant is velar, palatalizable
pal_aCV -> pal_aCVP   [^:]
pal_aCVP -> fin       [GG]
# -2 (C*h) consonant is r or labial
pal_aCV -> pal_aCVC   [r;RG-DD,GG]
# -3 (C**h) consonant (quadrilateral with -h) is velar, palatalizable
pal_aCVC -> pal_aCVCP [^:]
pal_aCVCP -> fin      [GG]
# -2 consonant is dental; stop looking
pal_aCV -> fin        [DD]

# Condition 1: palatalize final coronal (including r but not n) or velar
pal -> pal1           [^:]
pal1 -> fin           [DD;GG]

# Condition 2: palatalize last velar that's not palatalized unless there's an intervening coronal
# last consonant can't be palatalized
pal -> pal2           [RG-DD,GG]
pal2 -> pal2v         [V;:]
# palatalize a velar in position -2
pal2v -> pal2v^       [^:]
pal2v^ -> fin         [GG]
# or if it's a labial or r, look in position -3
pal2v -> pal2vc       [r;RG-DD,GG]
pal2vc -> pal2vcv     [V;:]
pal2vcv -> pal2vcvP   [^:]
# palatalize a velar in position -3
pal2vcvP -> fin       [GG]

# Condition 3: insert i after the last consonant, when nothing can be palatalized
pal2 -> pal3_i        [i:]
pal3_i -> pal3_iV     [V;:]
pal3_iV -> fin        [^]
# previous consonant not-palatalizable and not dental
pal3_iV -> pal3_iVC   [r;RG-DD,GG]
pal3_iVC -> pal3_iVCV [V;:]
pal3_iVCV -> fin      [^]
# consonant in -3 not velar, not palatalizable
pal3_iVCV -> fin      [RG-GG]
# -2 consonant is dental
pal3_iV -> pal3_iVD   [DD]
pal3_iVD -> pal3_iVDV [V;:]
pal3_iVDV -> fin      [^]
# -3 consonant can be anything
pal3_iVDV -> fin      [RG]

fin -> fin            [RG;V;^]
fin ->
start ->
