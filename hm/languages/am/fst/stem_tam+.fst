###
### This file is part of HornMorpho.
###
###    HornMorpho is free software: you can redistribute it and/or modify
###    it under the terms of the GNU General Public License as published by
###    the Free Software Foundation, either version 3 of the License, or
###    (at your option) any later version.
###
###    HornMorpho is distributed in the hope that it will be useful,
###    but WITHOUT ANY WARRANTY; without even the implied warranty of
###    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
###    GNU General Public License for more details.
###
###    You should have received a copy of the GNU General Public License
###    along with HornMorpho.  If not, see <http://www.gnu.org/licenses/>.
###
###  Author: Michael Gasser <gasser@cs.indiana.edu>
### -----------------------------------------------------------------------------------
### FST which covers details of the Amharic verb stem.
### Segmentation version.
### The prefixes a-, as-, te-, as well as the gemination of the stem initial consonsant
### that indicates passive voice for imperfective and jussive, are treated with separate
### states.
### Root/stem categories treated more or less separately in this FST:
### "A" roots: CCC, including those with initial laryngeal (addere), final laryngeal (bella),
###    and original final "y" (mexxe)
### special "A" roots, with C2=w|y|', behaving in many ways like 2-consonant verbs
### "B" roots: CC_C (fellege)
### 4-consonant and 5-consonant roots: CCCC (kelekkele), CCCCC (wexeneggere),
###    C|CCCC (teCberebbere)
### Stems with "a" before second-to-last consonants, including
###    "C" roots: CaCC (bakkene)
###    CCaCC roots: (tekenawwene)
###    C|CaCC roots: (tensaffefe)
###    C|CCaCC roots (tenSebarreqe)
###    iterative stem of "A" and "B" roots: CCaCC (sebabbere)
###    iterative stem of CCCC roots: (genefaffele)
###
### All occurrences of "o" and "u" in stems are treated as originating from labialized
### consonants in the root. For example,
### qureT <- qWIreT <- qWrT (an ordinary 3-consonant root)
### doleddome <- dWeledW_eme <- dWldWl (an ordinary 4-consonant root)
###
### Template features:
### pre, c_1, v_1, c1, c_2gem, c_2, c1gem
### Example templates
###  teCberebber-e:    te12e3e4_e5,   [tmp=[n=5,c1=12,c2=3,   c3=None,c4=None, c_1=c,   c_2=c, +c_2gem, -c1gem, v_1=e, v1=e, v2=e,   v3=None,v4=None,pre=te  ]]
###  gelebabbeT-e:     1e2e3a3_e4,    [tmp=[n=4,c1=1, c2=2,   c3=3,   c4=None, c_1=c,   c_2=3, +c_2gem, -c1gem, v_1=e, v1=e, v2=e,   v3=a,   v4=None,pre=None]]
###  y-nkWakW_-al:     12a2_a,        [tmp=[n=5,c1=12,c2=None,c3=None,c4=None, c_1=None,c_2=2, +c_2gem, -c1gem, v_1=a, v1=a, v2=None,v3=None,v4=None,pre=None]] 
###  awwexenegagger-e: a1_e2e3e4a4_e5 [tmp=[n=5,c1=1, c2=2,   c3=3,   c4=4,    c_1=c,   c_2=4, +c_2gem, +c1gem, v_1=e, v1=e, v2=e,   v3=e,   v4=a,  ,pre=a   ]]
###  babba:            1a2_a          [tmp=[n=4,c1=1, c2=None,c3=None,c4=None, c_1=None,c_2=2, +c_2gem, -c1gem, v_1=a, v1=a, v2=None,v3=None,v4=None,pre=None]]
###  sebabber-e:       1e2a2_e3       [tmp=[n=3,c1=1, c2=2,   c3=None,c4=None, c_1=c,   c_2=2, +c_2gem, -c1gem, v_1=e, v1=e, v2=a,   v3=None,v4=None,pre=None]]
### pre:    {te, a, as, aste, tt, None}
### c1:     {1, 12, None}
### c2:     {2, None}
### c3:     {3, None}
### c4:     {4, None}
### c_1:    {C, t, None}
### c_2:    {1, 2, 3, 4, None}
### c1gem:  {True, False}
### c_2gem: {True, False}
### v1:     {e, a, Wa, I, None}
### v2:     {e, a, None}
### v3:     {e, a, None}
### v4:     {a, None}
### v_1:    {e, a, o, i, E, u, Wa, W, None}
### n:      {3, 4, 5}

-> start

#### PREFIXES

## Transitive a-
start -> a          [a:]      [vc=tr,tmp=[pre=a]]
## Passive te- (perfective, gerundive, imperative)
start -> te         <te:>     [vc=ps,tm=prf,tmp=[pre=te,-c1gem]];[vc=ps,tm=ger,tmp=[pre=te,-c1gem]];[tm=j_i,vc=ps,sb=[+p2],-neg,tmp=[pre=te,-c1gem]]
## Causative as-
start -> as         <as:>     [tmp=[-c1gem]]
# for C1=L verbs, +iterative
as -> ast           [t:]      [vc=tr]
## Passive in imperfective, jussive is special because te- is replaced by ...
# ... tt for verbs with C1=L: yIttawweqal, yIttewawweqal
start -> tt0         <t_:>    [vc=ps,tm=imf];[vc=ps,tm=j_i,sb=[-p2]];[vc=ps,tm=j_i,sb=[+p2],+neg]
tt0 -> tt           [:]       [tmp=[pre=tt,-c1gem]]
start -> ij_ps      [:]       [tm=imf,vc=ps];[tm=j_i,vc=ps,sb=[-p2]];[tm=j_i,vc=ps,sb=[+p2],+neg]
# ... gemination of the following consonant (C1!=L): yImmerreTal, yImmerarreTal
ij_ps -> i/         [/:]      [tmp=[pre=None,+c1gem]]
# ... 0 when the root begins with C|: yInsaffefal, yICberebberal
ij_ps -> i|         [:]       [tmp=[pre=None,-c1gem,c1=1]]

## Combine causative, passive, and transitive prefixes, along with
## no prefix in one state (simp) because they are common to most roots
# Causative
as -> simp          [:]       [vc=cs,tmp=[pre=as]]
# Passive (perfective, gerundive, imperative)
te -> simp          [:]
# Prevent reciprocal and iterative aspect (which need a/)
a -> simp           [:]       [as=smp,tmp=[-c1gem]]
# Simplex voice: no stem prefix
start -> simp       [:]       [vc=smp,tmp=[pre=None,-c1gem]]

# Transitive and passive before C| verbs is special
a -> a_te           [:]       [tmp=[c1=1,-c1gem]]
te -> a_te          [:]       [tmp=[c1=1]]

# Transitive iterative, reciprocal: geminate C1 after the prefix
a -> a/             [/:]      [tmp=[+c1gem]]

#### END
### State names with "-" represent positions starting from the right:
###   -1 is right before the last consonant
###  -2V is right before the vowel following the second to last consonant

## Final consonant
-1 -> end           [X/L]     [tmp=[c_1=c]]

## Final vowels for most situations
# e: perfect; imperfect and jussive/imperative passive
#    (also for jussive/imperative simplex with CCC verbs but that's handled separately below)
-2V -> -1           [e:]      [tm=imf,vc=ps,tmp=[v_1=e]];[tm=j_i,vc=ps,tmp=[v_1=e]];[tm=prf,tmp=[v_1=e]]
# no vowel in other cases
-2V -> -2V0         [:]       [tm=imf,vc=smp];[tm=imf,vc=cs];[tm=imf,vc=tr];[tm=j_i,vc=cs];[tm=j_i,vc=tr];[tm=j_i,vc=smp];[tm=ger]
-2V0 -> -1          [:]       [tmp=[v_1=None]]

## Final vowel and consonant for final L, *
# a for final L except in gerundive
-2V -> -2V2         [a:']     [tm=prf];[tm=imf];[tm=j_i]
-2V2 -> end         [:]       [tmp=[v_1=a,c_1=None]]
# t for final L and * in gerundive
-2V -> end          [t:';t:*] [tm=ger,tmp=[v_1=None,c_1=t]]
# e for final * in perfective
-2V -> end          [e:*]     [tm=prf,tmp=[v_1=e,c_1=None]]
# no vowel for final * in imperfective and jussive/imperative
-2V -> end          [:*]      [tm=imf,tmp=[v_1=None,c_1=None]];[tm=j_i,tmp=[v_1=None,c_1=None]]

#### "A" verbs (CCC, C2 cannot be L, w, or y; these cases are handled below)

## Following C2
# geminate C2 in perfective, causative, imperfective passive
-2A_ -> -2V         [_:]      [tm=prf,tmp=[+c_2gem]];[vc=cs,tmp=[+c_2gem]];[tm=imf,vc=ps,tmp=[+c_2gem]]
# no gemination in other cases
-2A_ -> -2V1        [:]       [tm=imf,vc=smp];[tm=imf,vc=tr];[tm=j_i,vc=tr];[tm=ger,vc=smp];[tm=ger,vc=tr];[tm=ger,vc=ps]
-2V1 -> -2V         [:]       [tmp=[-c_2gem]]
# Final vowel: e for passive and simplex in jussive/imperative (simplex only for CCC)
-2A_ -> -1          [e:]      [tm=j_i,vc=ps,tmp=[v_1=e]];[tm=j_i,vc=smp,tmp=[v_1=e]]
# Final ', * for passive and simplex in jussive/imperative (a or 0, skipping to end)
-2A_ -> end         [a:']     [tm=j_i,vc=ps,tmp=[c_1=None,v_1=a]];[tm=j_i,vc=smp,tmp=[c_1=None,v_1=a]]
-2A_ -> end         [:*]      [tm=j_i,vc=ps,tmp=[c_1=None,v_1=None]];[tm=j_i,vc=smp,tmp=[c_1=None,v_1=None]]
# C2 (except after L): all root consonants except ', w, y (treated separately below)
-2A -> -2A_         [X!]      [tmp=[c_2=2]]
# following C1=L, y and w are also possible for C2
-2AL -> -2A_        [X/L]     [tmp=[c_2=2]]
# first stem vowel: e for perfective, imperfective, gerundive except transitive, jussive/imperative passive or causative
-3V -> -2A0         [e:]      [tm=prf];[tm=ger,vc=smp];[tm=ger,vc=ps];[tm=ger,vc=cs];[tm=imf];[tm=j_i,vc=ps];[tm=j_i,vc=cs]
-2A0 -> -2A         [:]       [tmp=[v1=e]]
# no first stem vowel in other cases: gerundive transitive, jussive/imperative simplex or transitive
-3V -> -2Aig         [:]      [tm=j_i,vc=smp];[tm=j_i,vc=tr];[tm=ger,vc=tr]
-2Aig -> -2A         [:]      [tmp=[v1=None,-c_2gem]]
# C1: all root consonants except L (treated separately below)
-3 -> -3V           [X/L]     [tmp=[c1=1]]
# C1=L ('); no transitive voice possible
# C1 and V1 are a for perfective, imperfective, gerundive; jussive/imperative except simplex
-3L -> -3LV         [:']    [vc=smp,tmp=[c1=None]];[vc=ps,tmp=[c1=None]];[vc=cs,tmp=[c1=None]]
-3LV -> -2AL        [a:]      [tm=prf,tmp=[v1=a]];[tm=ger,tmp=[v1=a]];[tm=imf,tmp=[v1=a]];[tm=j_i,vc=ps,tmp=[v1=a]];[tm=j_i,vc=cs,tmp=[v1=a]]
# C1 is 0 and V1 is I in other case: jussive/imperative simplex
-3LV -> -2AL        [I:]      [tm=j_i,vc=smp,tmp=[v1=I,-c_2gem]]

## Transitive, passive, and causative prefixes (as well as no prefix) can precede CCC
simp -> -3t         [:]       
simp -> -3L         [:]       [tmp=[n=3,c2=None,c3=None,c4=None,v2=None,v3=None,v4=None]]
## Initial geminated consonant for imperfective and jussive passive
i/ -> -3t           [:]
-3t -> -3           [:]       [tmp=[n=3,c2=None,c3=None,c4=None,v2=None,v3=None,v4=None]]

#### Special "A" verbs (CXC, imperfective with w, y, ' as C2; reduplicated: CaCXC)
#### the same pattern of vowels works with all reduplicated forms in this category
#### State names contain .2 (because these behave like 2-consonant verbs)

# C1 before special C2: any root consonant other than L (')
-3.2 -> -3V.2        [X/L]    [tmp=[c1=1]]

## for C2=', the same vowel pattern applies to reduplicated and non-reduplicated forms, except for jussive
# C2=' surfaces as a for perfective, imperfective passive, jussive/imperative passive and simplex (simplex aspect)
# ... same, yIssam, sasame, yIssasam
-3V.2 -> -3V.2a      [a:']    [tm=prf];[tm=imf,vc=ps];[tm=j_i,vc=ps];[tm=j_i,vc=smp,as=smp]
-3V.2a -> -1         [:]      [as=smp,tmp=[v_1=a,c_2=None,v1=None]];[as=rc,tmp=[v_1=a,c_2=None,v1=None]];[as=it,tmp=[v_1=a,c_2=1,v1=a]]
# C2=' surfaces as 0 in other cases: imperfective except passive, gerundive, jussive/imperative except simple (simplex aspect)
# ... yIsImal, yIsasIm, assasIm
-3V.2 -> -3V.2b      [:']     [tm=imf,vc=smp];[tm=imf,vc=tr];[tm=imf,vc=cs];[tm=ger]
-3V.2b -> -1         [:]      [as=smp,tmp=[v_1=None,c_2=None,v1=None]];[as=rc,tmp=[v_1=None,c_2=None,v1=None]]
-3V.2b -> -1         [:]      [as=it,tmp=[v_1=None,c_2=1,v1=a]]
-3V.2 -> -3V.2c      [:']     [tm=j_i,as=it,vc=smp];[tm=j_i,as=rc,vc=smp];[tm=j_i,vc=tr];[tm=j_i,vc=cs]
-3V.2c -> -1         [:]      [as=smp,tmp=[v_1=None,c_2=None,v1=None]];[as=rc,tmp=[v_1=None,c_2=None,v1=None]]
-3V.2c -> -1         [:]      [as=it,tmp=[v_1=None,c_2=1,v1=a]]

# C2=w surfaces as o for perfective, imperfective and gerundive simplex (optionally); jussive/imperative passive
# ... mote, moto (also muto) (CHANGE FOR GENERATION)
-3V.2 -> -3V.2d      [o:w]    [tm=prf,as=smp];[tm=imf,as=smp];[tm=ger,as=smp];[tm=j_i,vc=ps,as=rc];[tm=j_i,vc=ps,as=smp]
-3V.2d -> -1         [:]      [tmp=[v_1=o,c_2=None,v1=None]]
# C2=w surfaces as u for jussive/imperative simplex aspect except passive, gerundive simplex aspect (optionally)
# ... yImut (but yImmot), muto (also moto)
-3V.2 -> -3V.2e      [u:w]    [tm=j_i,as=smp,vc=smp];[tm=j_i,as=smp,vc=tr];[tm=j_i,as=smp,vc=cs];[tm=ger,as=smp]
-3V.2e -> -1         [:]      [tmp=[v_1=u,c_2=None,v1=None]]
# C2=w surfaces as a for iterative aspect in perfective and imperfective+jussive/imperative passive
# ... mWamWate, yImWmWamWat
-3V.2 -> -3V.2f      [a:w]    [tm=prf,as=it];[tm=imf,vc=ps,as=it];[tm=j_i,vc=ps,as=it]
-3V.2f -> -1         [:]      [tmp=[v_1=Wa,c_2=1,v1=Wa]]
# C2=w surfaces as 0 for iterative aspect in other cases
# ... yImWamWIt (-> yImWamut)
-3V.2 -> -3V.2g      [:w]     [tm=imf,as=it,vc=smp];[tm=imf,as=it,vc=tr];[tm=imf,as=it,vc=cs]
-3V.2 -> -3V.2g      [:w]     [tm=j_i,as=it,vc=smp];[tm=j_i,as=it,vc=tr];[tm=j_i,as=it,vc=cs];[tm=ger,as=it]
-3V.2g -> -1         [:]      [tmp=[v_1=W,c_2=1,v1=Wa]]

## Two classes of CCC verbs with C2=y
# C1 is palatal (cere, xeTe, etc.)
-3.2 -> -3PV.2       [J]      [tmp=[c1=1]]
# C1 is not palatal (hEde, gETe, etc.)
-3.2 -> -3~PV.2      [~J]     [tmp=[c1=1]]

# following palatal C1, y surfaces as e in simplex aspect (passive for jussive/imperative)
# optionally for gerundive (CHANGE FOR GENERATION)
# ... xeTe
-3PV.2 -> -3PV.2a    [e:y]    [tm=prf,as=smp];[tm=imf,as=smp];[tm=ger,as=smp];[tm=j_i,vc=ps,as=smp]
-3PV.2a -> -1        [:]      [tmp=[v1=None,v_1=e,c_2=None]]
# following palatal C1, y surfaces as a in iterative aspect: perfective, imperfective+jussive/imperative passive
# ... xaxaTe
-3PV.2 -> -3PV.2b    [a:y]    [tm=prf,as=it];[tm=imf,vc=ps,as=it];[tm=j_i,vc=ps,as=it]
-3PV.2b -> -1        [:]      [tmp=[v_1=a,c_2=1,v1=a]]
# following palatal C1, y surfaces as 0 in gerundive (optionally for simplex),
# imperfective+jussive/imperative except passive
# ... yIxIT, xITo, xaxITo, yIxaxIT
-3PV.2 -> -3PV.2c    [:y]     [tm=j_i,vc=smp];[tm=j_i,vc=tr];[tm=j_i,vc=cs];[tm=ger]
-3PV.2 -> -3PV.2c    [:y]     [tm=imf,as=it,vc=smp];[tm=imf,as=it,vc=tr];[tm=imf,as=it,vc=cs]
-3PV.2c -> -1        [:]      [as=it,tmp=[v_1=None,c_2=1,v1=a]];[as=smp,tmp=[v_1=None,c_2=None,v1=None]];[as=rc,tmp=[v_1=None,c_2=None,v1=None]]

# following non-palatal C1, y surfaces as E in perfective, imperfective simplex and passive iterative,
# gerundive simplex (optionally) and jussive/imperative passive (CHANGE FOR GENERATION)
# ... hEde, hEdo, fafEze, yIffafEz, fEzo
-3~PV.2 -> -3~PV.2a   [E:y]   [tm=prf];[tm=imf,as=smp];[tm=ger,as=smp];[tm=j_i,vc=ps];[tm=imf,vc=ps,as=it]
-3~PV.2a -> -1        [:]     [as=smp,tmp=[v1=None,v_1=E,c_2=None]];[as=it,tmp=[v1=a,v_1=E,c_2=1]]
# following non-palatal C1, in other cases y surfaces as i
# ... yIhid, hido
-3~PV.2 -> -3~PV.2c  [i:y]    [tm=j_i,vc=smp];[tm=j_i,vc=tr];[tm=j_i,vc=cs];[tm=ger]
-3~PV.2c -> -1       [:]      [as=smp,tmp=[v_1=i,c_2=None,v1=None]];[as=it,tmp=[v_1=i,c_2=1,v1=a]]
# ... yIfafiz, yafafiz
-3~PV.2 -> -3~PV.2b  [i:y]    [tm=imf,as=it,vc=smp];[tm=imf,as=it,vc=tr];[tm=imf,as=it,vc=cs]
-3~PV.2b -> -1       [:]      [tmp=[v_1=i,c_2=1,v1=a]]

## Special CXC cases can be preceded by normal voice prefixes and passive gemination of C1
i/ -> -3.2t          [:]      
simp -> -3.2t        [:]      
-3.2t -> -3.2        [:]      [tmp=[n=3,c2=None,c3=None,c4=None,v2=None,v3=None,v4=None,-c_2gem]]

# reduplicated cases for exceptional CCC
i/ -> -4.2           [:]       [as=it]    # imf, jus passive iterative
te -> -4.2           [:]       [as=it]    # prf, ger, impv passive iterative
a/ -> -4.2           [:]       [as=it]    # transitive iterative
simp -> -4.2         [:]       [as=it]    # simple iterative
-4.2 -> -4V.2        [X]       [tmp=[n=3,c1=1,c2=None,c3=None,c4=None,v2=None,v3=None,v4=None,-c_2gem]]
-4V.2 -> -3.2        [a]       

#### "B" verbs: CC_C, C2 cannot be ', since it can't be geminated
#### State names contain B

# Geminate C2 in all cases except jussive passive (optionally in imperative passive) (CHANGE FOR GENERATION)
-2B_ -> -2Va         [_]       [tm=prf];[tm=imf];[tm=ger];[tm=j_i,vc=smp];[tm=j_i,vc=tr];[tm=j_i,vc=cs];[tm=j_i,vc=ps,sb=[+p2],-neg]
-2Va -> -2V          [:]       [tmp=[+c_2gem]]
# No C2 gemination in jussive passive, optionally in the imperative
-2B_ -> -2Vb         [:_]      [tm=j_i,vc=ps]
-2Vb -> -2V          [:]       [tmp=[-c_2gem]]
# C2 can be y or w: qeyyere, lewweTe
-2B -> -2B_         [X/L]      [tmp=[c_2=2]]
-3V -> -2B          [e:]       [tmp=[v1=e]]
# C1=L: realize as a; no transitive voice possible (as with CCC)
-3L -> -3LVB        [:']     [vc=smp];[vc=ps];[vc=cs]
-3LVB -> -2B        [a:]       [tmp=[c1=None,v1=a]]

#### 4-consonant and 5-consonant verbs without a before C-2 (CCCC, CCCCC, C|CCCC)
#### State names contain .4

# C-2: any root consonant
-2.4 -> -2.4_       [X]
# C-2 gemination, degemination
# no gemination of C-2 for gerundive and jussive/imperative
-2.4_ -> -2.4t      [:]     [tm=ger];[tm=j_i]
# gemination of C3 in other cases: perfective, imperative
-2.4_ -> -2.4t_     [_:]    [tm=prf];[tm=imf]
# lexical gemination in the case of CC_C verb: ger; prf; imf; j_i smp, cs, tr smp
-2.4_ -> -2.4t_     [_]     [tm=ger];[tm=prf];[tm=imf];[tm=j_i,vc=smp];[tm=j_i,vc=cs];[tm=j_i,vc=tr,as=smp]
# delete lexical gemination in jussive rc, it, and ps
-2.4_ -> -2.4t      [:_]    [tm=j_i,vc=ps];[tm=j_i,as=rc];[tm=j_i,as=it]
# gemination of C-2 in template
-2.4t_ -> -2V       [:]     [tmp=[+c_2gem]]
# no gemination of C-2 in template
-2.4t  -> -2V       [:]     [tmp=[-c_2gem]]

# vowel following C-3: 0 for gerundive and jussive/imperative
-3.4V -> -2.4       [:]       [tm=ger,tmp=[v2=None]];[tm=j_i,tmp=[v2=None]]
# vowel following C-3: e for perfective and imperfective
-3.4V -> -2.4       [e:]      [tm=prf,tmp=[v2=e]];[tm=imf,tmp=[v2=e]]
# C-3: any root consonant except ' (C-3=' handled below)
-3.4 -> -3.4V       [X/L]     [tmp=[c2=2]]
# vowel after C-2: always e
-4.4V -> -3.4       [e:]      [tmp=[v1=e,c_2=3]]

# C-3=' (babba, etc.): realized as a
-4.4V -> -2.4       [a:']     [tmp=[c2=None,c_2=3,v1=a,v2=None]]

# C-4: any consonant except ' (C1=' handled below)
-4.4 -> -4.4V       [X/L]

# C1 for 5-consonant verbs: any root consonant
-5.5 -> -5.5V       [X]      [tmp=[c1=1]]
# vowel following first consonant of 5-consonant verbs (wexeneggere, etc.)
-5.5V -> -4.5       [e:]     [tmp=[v1=e]]
-4.5 -> -4.5V       [X/L]    [tmp=[c2=2]]
-4.5V -> -3.5       [e:]     [tmp=[v2=e]]
-3.5 -> -3.5V       [X/L]    [tmp=[c3=3,c_2=4]]
-3.5V -> -2.4       [e:]     [tm=prf,tmp=[v3=e]];[tm=imf,tmp=[v3=e]]
-3.5V -> -2.4       [:]      [tm=ger,tmp=[v3=None]];[tm=j_i,tmp=[v3=None]]

## 4- and 5-consonant roots can be preceded by passive, transitive, causative
## prefixes and by no prefix
simp -> -4.4        [:]      [tmp=[n=4,c1=1,c3=None,c4=None,v3=None,v4=None]]
simp -> -5.5        [:]      [tmp=[n=5,c4=None,v4=None]]
## also by initial gemination in passive imperfective and jussive
i/ -> -4.4          [:]      [tmp=[n=4,c1=1,c3=None,c4=None,v3=None,v4=None]]
i/ -> -5.5          [:]      [tmp=[n=5,c4=None,v4=None]]

### |: before CCCC (teCberebbere)
## Consonant preceding | and following a- or te-
i| -> |              [X]
a_te -> |            [X]
| -> -5.5|           [:|]    [tmp=[n=5,c2=2,c3=3,c4=None,v1=None,v4=None]]
-5.5| -> -4.5V       [X]

## causative and passive of CCC verbs with C1=L connect here
# ... astawweqe
ast -> -2.4         [a:']  [tmp=[n=3,pre=aste,c1=None,c2=None,c3=None,c4=None,v1=a,v2=None,v3=None,v4=None,c_2=2]]
# ... yIttaweq
tt -> -2.4          [a:']  [tmp=[n=3,c1=None,c2=None,c3=None,c4=None,v1=a,v2=None,v3=None,v4=None,c_2=2]]

## 4-consonant roots with C1=': no transitive prefix possible
## other cases are handled under CCC above (because they
## are apparently indistinguishable from them)
start -> -4.4L      [:]      [vc=smp,tmp=[pre=None,n=4,c1=None,c3=None,c4=None,v3=None,v4=None]]
-4.4L -> -3.4       [a:']    [tmp=[v1=a,c_2=3]]

## behaves like CCC in passive and causative
## ... the initial ' is dropped
as -> -3_4          [:']      [vc=cs,tmp=[pre=as]]
te -> -3_4          [:']
# Initial geminated consonant for imperfective and jussive passive
i/ -> -3_4          [:']
-3_4 -> -3_4V       [X/L]     [tmp=[n=4,c1=None,c2=2,c3=None,c4=None,v1=None,v3=None,v4=None]]
-3_4V -> -2.3_4     [e:]      [tmp=[v2=e]]
-2.3_4 -> -2A_      [X!]      [tmp=[c_2=3]]

#### ...aCC: "C" verbs (CaCC), CCaCC, C|CaCC, C|CCaCC
#### including iterative (reduplicative) versions of nearly all classes
#### State names contain a

# C-4: s.ebabbere
-4a -> -4aV         [X/L]
# vowel after C-4: se.babbere
-4aV -> -3a         [e:]
# be. in belexaxxe; CaCC, CCaCC iterative verbs
-4aV -> -3a         [e:a]     [as=it]
# C-3: T.affeTe, seb.abbere
-3a -> -3aV         [X]
# vowel after C-3: seba.bbere
-3aV -> -2.4        [a]

# C-5: g.enefaffele
-5a -> -5aV         [X/L]
# vowel after C-5: ge.nefaffele
-5aV -> -4a         [e:]

# C-6: wexenegaggere
-6a -> -6aV         [X/L]
# vowel after C-5: ge.nefaffele
-6aV -> -5a         [e:]

## C1=L of CCC verbs in iterative aspect: causative, passive, simplex
## (Note that astewawweqe is considered transitive iterative and handled elsewhere)
# causative and simplex voice: asawawweqe, awawweqe
-4aL -> -4aLV       [:']    [vc=smp,tmp=[n=3,c1=None,c2=2,c3=None,c4=None,c_1=c,c_2=2,v1=a,v2=a,v3=None,v4=None,pre=None]]
-4aL -> -4aLV       [:']    [vc=cs,tmp=[n=3,c1=None,c2=2,c3=None,c4=None,c_1=c,c_2=2,v1=a,v2=a,v3=None,v4=None,pre=as]]
-4aLV -> -3a        [a:]
# passive: tewawweqe
-4aL -> -3a         [:']    [vc=ps,tmp=[n=3,c1=None,c2=2,c3=None,c4=None,c_1=c,c_2=2,v1=None,v2=a,v3=None,v4=None,pre=te]]

## "C" verbs: CaCC, CCaCC, CCCaCC
simp -> -3a         [:]       [tmp=[n=3,c1=1,c2=None,c3=None,c4=None,c_2=2,v1=a,v2=None,v3=None,v4=None]]
simp -> -4a         [:]       [as=smp,tmp=[n=4,c1=1,c2=2,c3=None,c4=None,c_2=3,v1=e,v2=a,v3=None,v4=None]]
simp -> -5a         [:]       [as=smp,tmp=[n=5,c1=1,c2=2,c3=3,c4=None,c_2=4,v1=e,v2=e,v3=a,v4=None]]
## imperfective, jussive passive with geminated C1
i/ -> -3a           [:]       [tmp=[n=3,c1=1,c2=None,c3=None,c4=None,c_2=2,v1=a,v2=None,v3=None,v4=None]]
i/ -> -4a-it        [:]       [as=smp];[as=rc]
-4a-it -> -4a       [:]       [tmp=[n=4,c1=1,c2=2,c3=None,c4=None,c_2=3,v1=e,v2=a,v3=None,v4=None]]
i/ -> -5a-it        [:]       [as=smp];[as=rc]
-5a-it -> -5a       [:]       [tmp=[n=5,c1=1,c2=2,c3=3,c4=None,c_2=4,v1=e,v2=e,v3=a,v4=None]]

## C|C(eC)aCeC
## |: before CaCC (tensaffefe)
| -> -4a|           [:|]      [tmp=[n=4,c2=2,c3=None,c4=None,c_2=3,v1=None,v2=a,v3=None,v4=None]]
-4a| -> -3aV        [X/L]
# |: before CCaCC (texqedaddeme)
| -> -5a|           [:|]      [tmp=[n=5,c2=2,c3=3,c4=None,c_2=4,v1=None,v2=e,v3=a,v4=None]]
-5a| -> -4aV         [X/L]
# |: before CCCaCC (teCberebabbere)
| -> -6a|           [:|]      [tmp=[n=5,c1=1,c2=2,c3=3,c4=4,c_2=4,v1=None,v2=e,v3=e,v4=a]]
-6a| -> -5aV        [X/L]
# |: before C'C' (tenkWakWkWa)
| -> -5aL|          [:|]      [tmp=[n=5,c2=2,c3=None,c4=None,c_2=4,v1=None,v2=a,v3=None,v4=None]]
-5aL| -> -4aV|      [X/L]
-4aV| -> -2.4       [a:']


## Iterative of CCC verbs
simp -> -4a         [:]       [as=it,tmp=[n=3,c1=1,c2=2,c3=None,c4=None,c_2=2,v1=e,v2=a,v3=None,v4=None]]
i/ -> -4a           [:]       [as=it,tmp=[n=3,c1=1,c2=2,c3=None,c4=None,c_2=2,v1=e,v2=a,v3=None,v4=None]]

## Iterative of CCCC verbs
simp -> -5a         [:]       [as=it,tmp=[n=4,c1=1,c2=2,c3=3,c4=None,c_2=3,v1=e,v2=e,v3=a,v4=None]]
i/ -> -5a           [:]       [as=it,tmp=[n=4,c1=1,c2=2,c3=3,c4=None,c_2=3,v1=e,v2=e,v3=a,v4=None]]

## Iterative of CCCCC verbs (maybe never happens?)
simp -> -6a         [:]       [as=it,tmp=[n=5,c1=1,c2=2,c3=3,c4=4,c_2=4,v1=e,v2=e,v3=e,v4=a]]
i/ -> -6a           [:]       [as=it,tmp=[n=5,c1=1,c2=2,c3=3,c4=4,c_2=4,v1=e,v2=e,v3=e,v4=a]]

## Transitive iterative, reciprocal: a preceding geminated C1
# CaCC
a/ -> -3a           [:]       [as=rc,tmp=[n=3,c1=1,c2=None,c3=None,c4=None,c_2=2,v1=a,v2=None,v3=None,v4=None]]
a/ -> -4a-it        [:]       [as=rc]
a/ -> -5a-it        [:]       [as=rc]
# CCaCC
a/ -> -4a           [:]       [as=it,tmp=[n=3,c1=1,c2=2,c3=None,c4=None,c_2=2,v1=e,v2=a,v3=None,v4=None]]
# CCCaCC: aggenefaffele
a/ -> -5a           [:]       [as=it,tmp=[n=4,c1=1,c2=2,c3=3,c4=None,c_2=3,v1=e,v2=e,v3=a,v4=None]]
# CCCCaCC: awwexenebabbere
a/ -> -6a           [:]       [as=it,tmp=[n=5,c1=1,c2=2,c3=3,c4=4,c_2=4,v1=e,v2=e,v3=e,v4=a]]

### Special case of iterative passive or transitive CC' verbs with no vowel after C1
# ag/faffa (realized as agfaffa)
a -> -4a.L          [:]       [as=it,tmp=[n=3,-c1gem,c1=1,c2=2,c3=None,c4=None,c_2=2,v1=None,v2=a,v3=None,v4=None]]
# tegfaffa
te -> -4a.L         [:]       [as=it,tmp=[n=3,c1=1,c2=2,c3=None,c4=None,c_2=2,v1=None,v2=a,v3=None,v4=None]]
# /gfaffa (realized as gfaffa)
ij_ps -> -4a.L      [:]       [as=it,tmp=[n=3,pre=None,-c1gem,c1=1,c2=2,c3=None,c4=None,c_2=2,v1=None,v2=a,v3=None,v4=None]]
## ... tegfaffa, agfaffa
## We need to specify the whole path from here to the end.
# C1: (a)g.
-4a.L -> -4a.LV     [X/L]
# no vowel after C1: ag..
-4a.LV -> -3a.L     [:]       [vc=ps];[vc=tr]
# C2: agf.
-3a.L -> -3aV.L     [X]
# a after C2: agfa.
-3aV.L -> -2.L.4    [a]
# reduplicated C2: agfaf.
-2.L.4 -> -2.L.4_   [X]
# no gemination for gerundive and jussive/imperative: agfafto, agfafa
-2.L.4_ -> -2.LV    [:]       [tm=ger,tmp=[-c_2gem]];[tm=j_i,tmp=[-c_2gem]]
# gemination for perfective and imperfective: agfaffa, yagfaffal
-2.L.4_ -> -2.LV    [_:]      [tm=prf,tmp=[+c_2gem]];[tm=imf,tmp=[+c_2gem]]
# last segment: a for all but gerundive: agfaffa., yagfaffa.
-2.LV -> -2.LV-c    [a:']     [tm=prf];[tm=imf];[tm=j_i]
-2.LV-c -> end      [:]       [tmp=[v_1=a,c_1=None]]
# last segment: t for gerundive: agfaft.o
-2.LV -> end        [t:']     [tm=ger,tmp=[v_1=None,c_1=t]]

## CCC with C1=L: iterative
# causative: asawawweqe
as -> -4aL          [:]       [vc=cs]
# passive: tewawweqe
te -> -4aL          [:]
# simplex voice: awawweqe
start -> -4aL       [:]       [vc=smp]

### CCCC with C1=L (aneTTese)
## iterative
# aneTaTTese
start -> -4a0        [a:']     [vc=smp,tmp=[v1=a]]
# anneTaTTese
a/ -> -4a0           [:']      [tmp=[v1=None]]
# asneTaTTese; like CCC
as -> -4a0           [:']      [vc=cs,tmp=[v1=None]]
# yInneTaTTesal
i/ -> -4a0           [:']      [tmp=[v1=None]]
# teneTaTTese; like CCC
te -> -4a0           [:']      [tmp=[v1=None]]
-4a0 -> -4a          [:]       [tmp=[n=4,c1=None,+c_2gem]]

# Iterative transitive CCC with C1=L: astewawweqe
ast -> -3a        [e:']    [tmp=[n=3,pre=aste,c1=None,c2=2,c3=None,c4=None,v1=None,v2=a,v3=None,v4=None,c_2=2]]
# Iterative passive imperfective, jussive CCC with C1=L: yIttewawweqal
tt -> -3a         [e:']    [tmp=[n=3,v1=e,c1=None,c2=2,c3=None,c4=None,v2=a,v3=None,v4=None,c_2=2]]

end ->
