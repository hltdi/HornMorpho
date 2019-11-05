# convert sequences of vowels and consonants across stem-suffix boundaries and within suffixes

-> start

start -> Csuf       [X]
# delete the boundary
Csuf -> C=          [:=]
C= -> stem        [X;V]
# not at boundary yet
Csuf -> start       [:]

# only perfective (-e, -ec)
start -> del_e   [:e]      [sn=1]
start -> e       [e]
e -> start       [:]
e -> e=          [:=]
e= -> stem        [X;V-a,e]
del_e -> del_e=  [:=]
del_e= -> stem    [a;e]
# benemam; impf, j_i also sp=2
e= -> stem        [:a]      [sn=2,sp=3,sg=f]

# seTebemam
e -> eb          [b:]      [sn=2,sp=3,sg=f]
eb -> eb=        [:=]
eb= -> stem       [e]
eb= -> eb=e      [:e]
# srabemam; only prf
eb=e -> stem      [a]

start -> o       [o]
o -> start       [:]
o -> ob          [b:]
ob -> ob=        [:=]
# seTebom
ob= -> stem       [e]
ob= -> ob=e      [:e]
# srabom; only prf
ob=e -> stem      [a]
o -> o=          [:=]
o= -> stem        [X;V-a,e]
# benom
o= -> stem        [:a]
# [sn=2,sp=3,sg=m]

start -> V       [V-e,o,i]
V -> V=          [:=]
V= -> stem        [X;V]
V -> start       [:]

# ai -> A within suffix ema+i, Kma+i
start -> a.i     [A:i]
a.i -> start     [:a]
# other i
start -> i       [i]
# vowel other than a possible?
i -> start       [:]
i -> i=          [:=]
i= -> stem        [X;V]

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

pre -> pre      [X;V]
=r2n ->
=C ->
=V ->
pre ->
end ->

#stem -> stem       [X;V;=]
#stem ->