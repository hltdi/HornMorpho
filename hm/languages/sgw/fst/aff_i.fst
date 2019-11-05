# convert sequences of vowels and consonants across stem-affix boundaries and within stems

## suffix and stem
-> start

# no suffixes
start -> nosuf   [:=]
# stem ending in y
nosuf -> C.y=    [i:y]
nosuf -> V.y=    [:y]
nosuf -> stem     [X-y;V]
C.y= -> stem      [X]
V.y= -> stem      [A:a;E:e]

# C in suffix
start -> Csuf       [X-r,n]
# delete the boundary
Csuf -> C=          [:=]
C= -> stem        [X-y;V]
# del y at boundary after e and a
C= -> V.y=       [:y]
V.y= -> stem      [A:a;E:e]
C= -> C.y=       [i:y]
C.y= -> stem      [X]
# not at boundary yet
Csuf -> start       [:]

start -> rnsuf      [r;n]
rnsuf -> start     [:]
start -> rndel      [:r;:n]
rndel -> rn=.rn    [:=]
# l=r|n -> ll ?
rn=.rn -> stem     [n;l;n:r]
rnsuf -> rn=       [:=]
rn= -> stem        [X-r,n,l;V]

# V in suffix
start -> e       [e]
e -> start       [:]
e -> e=          [:=]
e= -> stem        [X;V-a,e,E,i]
# y=berema, ye=sTE=ema -> ye=STema??
e= -> stem        [:a;:E;:i]   [sn=2,sg=f]

# y=seTebema
e -> eb          [b:]      [sn=2,sp=3,sg=f]
eb -> eb=        [:=]
eb= -> stem       [e]

start -> o       [o]
o -> start       [:]
o -> ob          [b:]
ob -> ob=        [:=]
# y=seTebo
ob= -> stem       [e]
o -> o=          [:=]
o= -> stem        [X;V-a,e,E,i]
# y=beno
o= -> stem        [:a]
o -> oy          [y:]
oy -> oy=        [:=]
# ye=sTe=o -> ye=sTeyo?? ; ye=qi -> ye=qyo
oy= -> stem       [e;e:E;:i]

start -> aE.     [A:E]
start -> E       [E]
E -> start       [:]
E -> E=          [:=]
E= -> stem        [X;:e]
aE. -> a.E       [:=]
a.E -> stem       [:a]

start -> Vsuf       [V-e,o,i,E]
Vsuf -> V=          [:=]
V= -> stem        [X;V]
Vsuf -> start       [:]

# ai -> A within suffix ema+i (only possibility?
start -> a.i     [A:i]
a.i -> start     [:a]
# other i
start -> i       [i]
# vowel other than a possible?
i -> start       [:]
i -> i=          [:=]
i= -> stem        [X;V-e]
start -> ai.     [E:i]
ai. -> a.i       [:=]
# ei -> E (ysemWE)
a.i -> stem       [:e]

#stem -> stem       [X;V;=]

## stem and prefix

stem -> C      [X-r]
C -> =C         [:=]
=C -> end       [y]
=C -> y2i       [i:y]
y2i -> pre      [X]
=C -> pre       [X-y;V]
# negative ay -> E
=C -> a.y=      [:y]
a.y= -> pre     [E:a]

C -> V          [V]
C -> C          [X-r]
C -> r          [r]
C -> r2n        [n:r]

# word initial r -> n
stem -> r      [r]
r -> V          [V]
r -> C          [X]
# r->n in first position or following n in prefix
r2n -> =r2n     [:=]
# prefix ending in -n, deleted before stem-initial r->n (or copy for geminated nn)
=r2n -> pre     [:n]
r -> =r         [:=]
=r -> pre       [X;V]

stem -> V      [V]
V -> C          [X-r]
V -> r          [r]
V -> r2n        [n:r]
V -> =V         [:=]
# delete e- before a stem-initial vowel
=V -> pre       [:e]
=V -> pre       [V-e;X-y]
=V -> a.y=      [:y]
=V -> end       [y]

#stem -> pre    [:=]

pre -> pre      [X;V]
=r2n ->
=C ->
=V ->
pre ->
end ->