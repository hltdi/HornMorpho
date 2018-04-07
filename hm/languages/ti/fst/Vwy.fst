## C3=w/y verbs
## changes across the boundary between stem and first suffix
## perfective; imperfective passive; jussive-imperative simple, passive
# ew$C -> oC, ey$C -> eC; ew/y$ can end word
# ey$e -> e optionally
## imperfective simple, transitive
# Iw$C -> u, Iy$C -> i; Iw/y$ can end word
## gerundive
# iw/y$V -> yV, iw/y$C -> iC

-> start
start -> start  [X;V-e,@,I,i;_;$]

## gerundive: i...
# iw/yC -> iC
start -> i      [i]
i -> iY.$C      [:y;:w]
# boundary
iY.$C -> iY$.C  [:$] 
iY$.C -> start  [X]

# iw/yV -> yV
start -> i.Y$V  [y:i]
i.Y$V -> iY.$V  [:y;:w]
iY.$V -> iY$.V  [:$]
iY$.V -> start  [V]

# escape: any other consonant following i
i -> start      [X-y,w]

## perfective, imperfective passive; juss-imperative simplex, passive: e...
# delete e
start -> e.Y$   [:e;:@]
e.Y$ -> Vw.$    [o:w]
Vw.$ -> Vw$.    [:$]
Vw$. -> start   [X-w]

e.Y$ -> Vy.$    [e:y;@:y]
Vy.$ -> Vy$.    [:$]
Vy$. -> start   [X-y]
Vy$. -> Vy$V.   [:e;:@;:I]
# With a 3 person object suffix, ey->y is not possible
Vy$V. -> start  [X]

## imperfective simplex, transitive
# delete I
start -> I.Y$    [:I]
# replace the consonant with a vowel (y->i,e, w->o,u)
I.Y$  -> Vw.$    [u:w]
I.Y$  -> Vy.$    [i:y]

# it has to happen
# e,I not deleted
start -> e      [e;@]
start -> I      [I]
e -> start      [X-w,y;V;/]
I -> start      [X-w,y;V;/]
e -> Vy         [y]
I -> Vy         [y]
# boundary character possible because rule is optional
Vy -> start     [X;V;_;/;$]
# fail if last
e -> Vw         [w]
I -> Vw         [w]
# boundary character possible because rule is optional
Vw -> start     [X;V;_;/;$]

start ->
Vy$. ->
Vy$V. ->
Vw$. ->
Vw ->
Vy ->
e ->
@ ->
i ->
# can end word because it hasn't been converted to i yet (in i_fin)
I ->
