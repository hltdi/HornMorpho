reverse

# imperfect and jussive/imperative 2 person singular feminine suffix's effect on the verb stem
-> start

# doesn't apply
start -> start        [XX;^]  [sb=[-p2]];[sb=[-fem]];[sb=[+p2,+fem,+plr]];[tm=prf]

# does apply
start -> pal          [:]     [sb=[-p1,+p2,+fem,-plr],tm=imf];[sb=[-p1,+p2,+fem,-plr],tm=j_i]

# Condition 1: palatalize final coronal or velar
pal -> pal1           [^:]
pal1 -> fin           [DD;GG]

# Condition 2: palatalize last velar that's not palatalized unless there's an intervening coronal
# first consonant
pal -> pal2           [RG-DD,GG]
pal2 -> pal2v         [V;:]
pal2v -> pal2v^       [^:]
pal2v^ -> fin         [GG]
pal2v -> pal2         [RG-DD,GG]

# Condition 3: palatalize final vowel
# ...

fin -> fin            [RG;V;^]
fin ->
start ->
