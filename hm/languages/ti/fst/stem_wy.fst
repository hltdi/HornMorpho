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
C1 -> C1          [|]
# as long as there's no w, y, or e, go to the end state
C1 -> end         [X-w,y;V-e]
# once we're past C1, e, w, y, finish with anything
end -> end        [X;V;_;/]

## jussive simpl, trans: C1{w|y}eC3 aC1{w|y}C3; trans ger (y), imprf
C1 -> u=w        [u:w]
# second possibility is trans imprf (amut)
u=w -> end       [:e;X-y]
C1 -> i=y        [i:y]
# second possibility is trans ger (axiT)
# third is transitive imperfective
i=y -> end       [:e;:i;X-y]

## transitive gerundive (w), transitive perfective
# wiC -> oyC [Leslau: also unchanged]
# weC -> oC
C1 -> o=w        [o:w]
o=w -> end       [y:i]
o=w -> o=we      [:e]
o=we -> end      [X-y]
# yeC -> eC
C1 -> e=y        [e:y]
e=y -> e=ye      [:e]
e=ye -> end      [X-y]

## perfective, imperfective, gerundive simplex
# delete V1=e
C1   -> e.       [:e]
# ew->o
e. -> eo=w       [o:w]
# ey->e
e. -> ee=y       [e:y]
# after ew->o, i->y in gerundive (moyt); C follows in imperfective (mot)
eo=w -> end      [y:i;X;/]
# after ey->e, OK if there's a following C in imperfective (xeT)
ee=y -> end      [X-y;/]
# after ey->e, ew->o, if there's another e (perfective), we have to check C3
ee=y -> eV=Ce    [:e]
eo=w -> eV=Ce    [:e]
# finished if C3!=y
eV=Ce -> end     [X-y]

## paths with no changes
# w, y following no V2 (jussive/imperative, transitive)
C1 -> w         [w]
C1 -> y         [y]
# preserve if geminated or followed by y
w -> end        [_;y]
y -> end        [_;y]
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
ew -> end       [_]
ey -> end       [_]
# preserve ey, ew if followed by y (dewy, gWeyy)
ew -> end       [y]
ey -> end       [y]
# preserve ey, ew if followed by a (in as=it: -mewawet-, xeyayeT-
ew -> end       [a]
ey -> end       [a]
# eyiC -> eyC for gerundive (keyd); ew handled above (ewi -> oy)
ey -> eyi       [:i]
eyi -> end      [X]
# eyey for perfective with Cyy verbs (gWeyey)
ey -> eYe.y     [e]
eYe.y -> end    [y]
# ewey for perfective with Cwy verbs (dewey)
ew -> eYe.y     [e]

end ->
