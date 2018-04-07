-> start

start -> start     [RG;V]

## Palatalize 2nd consonant
start -> pal2      [^]
pal2 -> pal2c      [GG]
# don't palatalize the vowel
pal2c -> pal2^     [:^]
pal2^ -> pal2v     [e]
# first consonant must be labial (not palatalized) or velar (palatalized)
pal2v -> pal2vB    [:^]
pal2vB -> end      [BB]
pal2v -> pal2vD    [^]
pal2v^ -> end      [DD]

## Palatalize only 1st consonant because 2nd consonant is not velar
start -> pal1      [:^]
pal1 -> pal1c      [RG-GG]
pal1c -> pal1c^    [:^]
pal1c^ -> pal1cv   [e]
pal1cv -> pal1cv^  [^]
pal1cv^ -> end     [DD;GG]

## Palatalize only 1st consonant because 1nd consonant is not coronal
start -> pal1      [:^]
pal1 -> pal1G      [GG]
pal1G -> pal1G^    [:^]
pal1G^ -> pal1Gv   [e]
pal1Gv -> pal1Gv^  [^]
pal1Gv^ -> end     [GG]

## Palatalize first vowel because neither 1st nor 2nd consonant is palatalizable
pal1c^ -> pal1cE   [E:e]
pal1cE -> pal1cE^  [:^]
pal1cE^ -> end     [RG-DD,GG]

## Palatalize first vowel because neither 1st nor 2nd consonant is palatalizable
pal1G -> pal1GE    [E:e]
pal1GE -> pal1GE^  [:^]
pal1GE^ -> end     [RG-GG]

start ->
end ->
