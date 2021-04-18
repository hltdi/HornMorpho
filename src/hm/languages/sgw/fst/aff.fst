# convert sequences of vowels and consonants across stem-suffix boundaries
# and within suffixes, for perfective verbs; remember: this is reversed!

-> start

# N, L, R at stem-suffix boundary (but for prf, only -n can start suffix)
start -> Csuf       [X-n]
# delete the boundary
Csuf -> C=          [:=]
C= -> stem          [X;V]
# not at boundary yet
Csuf -> start       [:]

# R=N -> N_; R=R -> L_; L=N -> N_; L=R -> L_
start -> nsuf     [n]
nsuf -> start     [:]
start -> ndel     [_:n]
ndel -> n=.r      [:=]
n=.r -> stem      [n;l;n:r]
nsuf -> n=        [:=]
n= -> stem        [X-r,n,l;V]

#start -> rsuf     [r]
#rsuf -> start     [:]
#start -> rdel     [:r]
#rdel -> r=.r      [:=]
#r=.r -> stem      [n;l;n:r]
#rsuf -> r=        [:=]
#r= -> stem        [X-r,n,l;V]

# only perfective (-e, -ec)
start -> del_e   [:e]      [sn=1]
start -> e       [e]
e -> start       [:]
e -> e=          [:=]
e= -> stem        [X;V-a,e]
del_e -> del_e=  [:=]
del_e= -> stem    [a;e]
# benemam; seTemam; SKIP FOR GENERATION
#e= -> stem        [:a;:e]  [sn=2,sp=3,sg=f]

e -> eb          [b:]      [sn=2,sp=3,sg=f]
eb -> eb=        [:=]
# seTebemam; weTebemam
eb= -> stem      [e;e:a]
eb= -> eb=e      [:e]
# srabemam
eb=e -> stem     [a]

start -> o       [o]
o -> start       [:]
o -> ob          [b:]      [sn=2,sp=3,sg=m]
ob -> ob=        [:=]
# seTebom; weTebom
ob= -> stem      [e;e:a]
ob= -> ob=e      [:e]
# srabom
ob=e -> stem      [a]
o -> o=          [:=]
o= -> stem        [X;V-a,e]
# benom; seTom
o= -> stem        [:a;:e]

start -> aE.     [A:E]
start -> E       [E]
E -> start       [:]
E -> E=          [:=]
#
E= -> stem        [X;:e]
aE. -> a.E        [:=]
a.E -> stem       [:a]

E -> Csuf         [:e]
E -> yE           [y:]
# yE -> start     [a;o;E]
yE -> a           [a]
yE -> o           [o]
yE -> E           [E]
# WHAT ABOUT u IN SUFFIXES?
yE -> start       [u]
yE -> iyE         [i]
iyE -> start      [X]
E -> iE           [y:i]
iE -> o           [o]

start -> Vsuf     [V-e,o,i,E]
Vsuf -> V=        [:=]
V= -> stem        [X;V]
Vsuf -> start     [:]

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
# ei -> E (semWE)
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
