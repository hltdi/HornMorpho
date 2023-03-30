# convert sequences of vowels and consonants across stem-suffix boundaries
# and within suffixes, for perfective verbs; remember: this is reversed!

-> start

# N, L, R at stem-suffix boundary (but for prf, only -n can start suffix)
start -> Csuf       [X-n]
# R=N -> N_; R=R -> L_; L=N -> N_; L=R -> L_
start -> nsuf     [n]
start -> ndel     [_:n]
# only perfective (-e, -ec)
start -> del_e   [:e]      [sn=1]
start -> e       [e]
start -> o       [o]
start -> aE.     [A:E]
start -> E       [E]
start -> Vsuf     [V-e,o,i,E]
# ai -> A within suffix ema+i (only possibility?
start -> a.i     [A:i]
# other i
start -> i       [i]
start -> ai.     [E:i]

# delete the boundary
Csuf -> C=          [:=]
C= -> stem          [X;V]
# not at boundary yet
Csuf -> Csuf       [X-n]
# R=N -> N_; R=R -> L_; L=N -> N_; L=R -> L_
Csuf -> nsuf     [n]
Csuf -> ndel     [_:n]
# only perfective (-e, -ec)
Csuf -> del_e   [:e]      [sn=1]
Csuf -> e       [e]
Csuf -> o       [o]
Csuf -> aE.     [A:E]
Csuf -> E       [E]
Csuf -> Vsuf     [V-e,o,i,E]
# ai -> A within suffix ema+i (only possibility?
Csuf -> a.i     [A:i]
# other i
Csuf -> i       [i]
Csuf -> ai.     [E:i]

ndel -> n=.r      [:=]
n=.r -> stem      [n;l;n:r]
nsuf -> n=        [:=]
n= -> stem        [X-r,n,l;V]

# nsuf back to start
nsuf -> Csuf       [X-n]
nsuf -> del_e   [:e]      [sn=1]
nsuf -> e       [e]
nsuf -> o       [o]
nsuf -> aE.     [A:E]
nsuf -> E       [E]
nsuf -> Vsuf     [V-e,o,i,E]
nsuf -> a.i     [A:i]
# other i
nsuf -> i       [i]
nsuf -> ai.     [E:i]

e -> e=          [:=]
e= -> stem        [X;V-a,e]
del_e -> del_e=  [:=]
del_e= -> stem    [a;e]

# e back to start
e -> Csuf       [X-n]
e -> nsuf     [n]
e -> ndel     [_:n]

# benemam; seTemam; SKIP FOR GENERATION
e= -> stem        [:a;:e]  [sn=2,sp=3,sg=f]

# o back to start
o -> Csuf       [X-n]
o -> nsuf     [n]
o -> ndel     [_:n]

o -> o=          [:=]
o= -> stem        [X;V-a,e]
# benom; seTom
o= -> stem        [:a;:e]

# E back to start
E -> Csuf       [X-n]
E -> nsuf     [n]
E -> ndel     [_:n]

E -> E=          [:=]
E= -> stem        [X;:e]
aE. -> a.E        [:=]
a.E -> stem       [:a]

E -> Csuf         [:e]
E -> yE           [y:]
yE -> a           [a]
yE -> o           [o]
yE -> E           [E]
# WHAT ABOUT u IN SUFFIXES?
yE -> start       [u]
yE -> iyE         [i]
iyE -> start      [X]
E -> iE           [y:i]
iE -> o           [o]

Vsuf -> V=        [:=]
V= -> stem        [X;V]

# Vsuf back to start
Vsuf -> Csuf       [X-n]
Vsuf -> nsuf     [n]
Vsuf -> ndel     [_:n]

a.i -> start     [:a]
# vowel other than a possible?

# i back to start
i -> Csuf       [X-n]
i -> nsuf     [n]
i -> ndel     [_:n]

i -> i=          [:=]
i= -> stem        [X;V-e]
ai. -> a.i       [:=]
a.i -> stem       [:e]

## stem and prefix

stem -> C        [X-r]
C -> =C          [:=]
=C -> pre       [X;V]

C -> V          [V]
C -> C          [X-r]
C -> r          [r]
C -> r2n        [n:r]

# word initial r -> n
stem -> r      [r]
r -> V          [V]
r -> C          [X]
# r->n in first position or following n in prefix
r2n -> end      [:=]
r2n -> =r2n     [:=]
# prefix ending in -n, deleted before stem-initial r->n (or copy for geminated nn)
=r2n -> pre     [:n]
r -> =r         [:=]
=r -> pre       [X-n;V]

# n=w -> mbW (optional); ኣምᎄጣ / ኣንወጣ
V -> wbW       [bW:w]
wbW -> wbW:     [:=]
wbW: -> pre     [m:n]

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

pre -> pre      [X;V]
=C ->
=V ->
pre ->
end ->
