# convert sequences of vowels and consonants across stem-affix boundaries
# and within stems

## suffix and stem
-> start

# no suffixes
start -> nosuf   [:=]
# stem ending in y
nosuf -> C.y=    [i:y]
nosuf -> V.y=    [:y]
# stem ending in vowel or consonant other than y
nosuf -> stem    [X-y;V]
# go to stem consonant (this could be the only remaining segment in the stem,
# as in ye=Ki)
C.y= -> C         [X]
# stem ending in Vy; change vowel
V.y= -> V         [A:a;E:e]

# C in suffix
start -> Csuf     [X]
suf -> Csuf       [X]
# delete the boundary
Csuf -> C=        [:=]
C= -> stem        [X-y;V]
# del y at boundary after e and a
C= -> V.y=        [:y]
C= -> C.y=        [i:y]
# not at boundary yet
Csuf -> Csuf      [X]
Csuf -> e         [e]
Csuf -> i         [i]
Csuf -> E         [E]
Csuf -> o         [o]
Csuf -> u         [u]
# a (or I?) or in suffix
Csuf -> Vsuf      [V-u,e,o,i,E]

# V in suffix
start -> e        [e]
e -> Csuf         [X]
e -> e=           [:=]
e= -> stem        [X;V-a,e,E,i]
# y=berema, ye=sTE=ema -> ye=STema??
e= -> stem        [:a;:E;:i]   [sn=2,sg=f]

start -> o        [o]
o -> Csuf         [X]
o -> o=           [:=]
o= -> stem        [X;V-a,e,E,i;:a]
o -> oy           [y:]
oy -> oy=         [:=]
# ye=sTe=o -> ye=sTeyo?? ; ye=qi -> ye=qyo
oy= -> stem       [e;e:E;:i]

start -> aE.      [A:E]
start -> E        [E]
# delete e before final E
E -> Vsuf         [V-e;:e]
E -> Csuf         [X]
E -> E=           [:=]
E= -> stem        [X;:e]
aE. -> a.E        [:=]
a.E -> stem       [:a]
E -> yE           [y:]
yE -> a           [a]
yE -> o           [o]
yE -> E           [E]
yE -> i           [i]
yE -> CyE         [:i]
CyE -> Csuf       [X]
CyE -> CyE=       [:=]
CyE= -> C         [X]
# WHAT ABOUT u IN SUFFIXES?
yE -> u           [u]
E -> iE           [y:i]
# ybroyE
iE -> o           [o]

start -> Vsuf     [a;A]
Vsuf -> V=        [:=]
V= -> stem        [X;V]
Vsuf -> Csuf      [X]

start -> u        [u]
u -> Csuf         [X]
u -> u=           [:=]
u= -> C           [X]
start -> uw       [w:u]
uw -> E           [E]
uw -> o           [o]
uw ->  i          [i]
uw -> e           [e]
uw -> u           [u]
uw -> uw=         [:=]
uw= -> V          [V]

# i in suffix
# ai -> A within suffix ema+i (only possibility?
start -> a.i     [A:i]
a.i -> Vsuf      [:a]
start -> i       [i]
i -> Csuf        [X]
# i following stem boundary
i -> i=          [:=]
i= -> stem       [X;o;u;a;A]
# tsebi=i -> tsebiyi; qeyE=i -> qeyEyi (qeyeyi?)
i= -> iy=i       [y:]
iy=i -> stem     [i;E;e]
start -> ei.     [E:i]
ei. -> e.i       [:=]
# ei -> E (ysemWE)
e.i -> V         [:e]

## stem and prefix

stem -> C       [X-r]
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

# word initial r -> n (only for jussive)
stem -> r       [r]
r -> V          [V]
r -> C          [X]
# r->n in first position
r2n -> =r2n     [:=]
r -> =r         [:=]
=r -> pre       [X-y;V]
=r -> end       [y]
=r -> y2i       [i:y]

stem -> V       [V]
V -> C          [X-r]
V -> r          [r]
V -> r2n        [n:r]
V -> =V         [:=]
# delete e- before a stem-initial vowel
=V -> pre       [:e]
=V -> pre       [V-e;X-y]
=V -> a.y=      [:y]
=V -> end       [y]
=V -> .y=V      [y]
.y=V -> .iy=V   [i:]
.iy=V -> end    [t;b]

pre -> pre      [X;V]

=r2n ->
=C ->
=V ->
pre ->
end ->
