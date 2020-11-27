### C2 = w/y verbs: all obligatory
### (These rules are very elaborate, and this is certainly not the best way to
### handle them. Also there is only one possibility in each case; Leslau gives several
### alternatives for most cases.)
###
### Exceptions to all rules when C3=y (gWeyeye, deweye)
## simplex cases
# perfective:   ewe -> o,     eye -> e
# imperfective: ewC -> oC,    eyC -> eC
# jussive:     CweC -> CuC,   CyeC -> CiC
# gerundive:   ewiC -> oyC,   eyiC -> eyC
## transitive cases
# perfective:   Cwe -> Co ,   Cye -> Ce
# imprf/juss:   CwC -> CuC,   CyC -> CiC
# gerundive:    Cwi -> Coy,   Cyi -> Ci

-> start
# wait for the boundary character
start -> start    [X;V;_;/]

# delete the boundary character
start -> bound    [:!]

# C1 (possibly followed by |)
bound -> C1       [X]
# C1 -> C1          [|]
# as long as there's no w, y, or e, go to the end state
#C1 -> end         [X-w,y;V-e]
# but there could be a sequence of consonants at the beginning (te-KWzeyzey-e)
C1 -> C1          [X-w,y]
C1 -> end         [V-e]
# once we're past C1, e, w, y, finish with anything
end -> end        [X;V;_;/]

# C1 palatal
bound -> P1       [PP]
# C1 non-palatal
bound -> ~P1      [X-PP]

## jussive simpl, trans: C1{w|y}eC3 aC1{w|y}C3; trans ger (y), imprf
C1 -> u=w        [u:w]
# second possibility is trans imprf (amut)
u=w -> end       [:e;X-y]
C1 -> i=y        [i:y]
# jussive smpl: yKid
i=y -> end       [:e]      [tm=j_i]
# 1: trans ger (axiT)
# 2: transitive imperfective
i=y -> end       [:i;X-y]

## transitive gerundive (w), transitive perfective
# wiC -> oyC [Leslau: also unchanged]
# CweC -> CoC
C1 -> o=w        [o:w]
o=w -> end       [y:i]
o=w -> o=we      [:e]
o=we -> end      [X-y]
# CyeC -> CeC but only for C1 palatal
P1 -> Pe=y       [e:y]
Pe=y -> Pe=ye    [:e]
Pe=ye -> end     [X-y]

## perfective, imperfective, gerundive simplex
# delete V1=e
C1   -> e.       [:e]
# ew->o
e. -> eo=w       [o:w]
# ey->e
e. -> ee=y       [e:y]
# xeTe
P1 -> Pe.        [:e]
Pe. -> Pey.      [e:y]
Pey. -> end      [:e]
# after ew->o, i->y in gerundive (moyt); C follows in imperfective (mot)
eo=w -> end      [y:i;/]
eo=w -> eo=wC    [X]
# for E verbs in prf with C2=2, ew-o is possible: `oSeSe
eo=wC -> end     [e]
# after ey->e, OK if there's a following C in imperfective (xeT)
ee=y -> end      [X-y;/]
# ew->o, if there's another e (perfective), we have to check C3
#ee=y -> eV=Ce    [:e]
eo=w -> eV=Ce    [:e]
# finished if C3!=y
eV=Ce -> end     [X-y]
# alternative for ~PyX in prf: zym, Tys: eye -> E; TEse, tezEme
~P1 -> ~Pe.      [:e]
~Pe. -> ~Pey.    [E:y]
~Pey. -> end     [:e]
# a-zEm-e
~P1 -> ~Py.      [E:y]
~Py. -> ~Pye.    [:e]
~Pye. -> end     [X]

## paths with no changes
# w, y following no V2 (jussive/imperative, transitive; C|wCCC all forms)
C1 -> w         [w]
C1 -> y         [y]
~P1 -> ~Py      [y]
# preserve if geminated or followed by y
# ye also survives for prf;tr following non-pal: asyeme, but not for j_i: sim
#w -> end        [_;y;e]
w -> end        [_;y;e]
y -> end         [_;y]
~Py -> end        [e]     [tm=prf]
# ye also survives if C3=y (trans perf)
y -> yV         [e]
yV -> end       [y]
# situations in which we keep V2=e
C1 -> e         [e]
# e OK if C2 is not w or y
e -> end        [X-w,y;/]
# situations in which to preserve ew, ey
e -> ew         [w]
e -> ey         [y]
# preserve ey, ew if C is geminated
# qey_er, qey_r, qey_ir, dew_el, dew_l, dew_il
# seyem
# preserve ey, ew if followed by y (dewy, gWeyy)
# preserve ey, ew if followed by a (in as=it: -mewawet-, xeyayeT-)
# alternately also if followed by e or laryngeal (newHE)
ew -> end       [_;y;a;e]
ey -> end       [_;y;a;e]
# eyiC -> eyC for gerundive (keyd); ew handled above (ewi -> oy)
ey -> eyi       [:i]
eyi -> end      [X]
# eyey for perfective with Cyy verbs (gWeyey)
ey -> eYe.y     [e]
eYe.y -> end    [y]
# ewey for perfective with Cwy verbs (dewey)
ew -> eYe.y     [e]
# ewCeC for CwCC verbs
ew -> ewC.C     [X]
ewC.C -> ewC.C  [V]
#ewC.c -> e      [e]
ewC.C -> end    [X]
# eyCeC for CyCC verbs
ey -> ewC.C     [X]
# eyL (te-rey`-e); only for following L??
# ewL (newH-e)
ey -> end       [L]
ew -> end       [L]

end ->
eo=wC ->
# te-KWzeyzey-e
ey ->
ew ->
C1 ->
