# convert sequences of vowels and consonants across stem-suffix boundaries and within stems

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
start -> Csuf       [X]
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
E -> Csuf        [X]
E -> E=          [:=]
E= -> stem        [X;:e]
aE. -> a.E       [:=]
a.E -> stem       [:a]
# delete e before final E
E -> start        [:e]
E -> yE           [y:]
yE -> start       [a;o;E;u]
yE -> iyE         [i]
iyE -> start      [X]
E -> iE           [y:i]
# ybroyE
iE -> start       [o]

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
i -> yi          [y:]
# y-ud-o-(y)-i
yi -> start      [o]
i -> start       [:]
i -> i=          [:=]
i= -> stem        [X;V-e]
start -> ai.     [E:i]
ai. -> a.i       [:=]
# ei -> E (ysemWE)
a.i -> stem       [:e]

stem -> stem       [X;V;=]
stem ->