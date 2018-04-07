###
### This file is part of AmMorpho.
###
###    AmMorpho is free software: you can redistribute it and/or modify
###    it under the terms of the GNU General Public License as published by
###    the Free Software Foundation, either version 3 of the License, or
###    (at your option) any later version.
###
###    AmMorpho is distributed in the hope that it will be useful,
###    but WITHOUT ANY WARRANTY; without even the implied warranty of
###    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
###    GNU General Public License for more details.
###
###    You should have received a copy of the GNU General Public License
###    along with AmMorpho.  If not, see <http://www.gnu.org/licenses/>.
###
###  Author: Michael Gasser <gasser@cs.indiana.edu>
### -----------------------------------------------------------------------------------
### FST which covers details of the Amharic verb stem.
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

-> start

#### PREFIXES

## Transitive a-
start -> a          [a:]      [vc=tr]
## Passive te- (perfective, gerundive, imperative)
start -> te         <te:>     [vc=ps,tm=prf];[vc=ps,tm=ger];[tm=j_i,vc=ps,sb=[+p2],-neg]
## Causative as-
start -> as         <as:>
# for C1=L verbs, +iterative
as -> ast           [t:]      [vc=tr]
## Passive in imperfective, jussive is special because te- is replaced by ...
# ... tt for verbs with C1=L: yIttawweqal, yIttewawweqal
start -> tt         <t_:>     [vc=ps,tm=imf];[vc=ps,tm=j_i,sb=[-p2]];[vc=ps,tm=j_i,sb=[+p2],+neg]
start -> ij_ps      [:]       [tm=imf,vc=ps];[tm=j_i,vc=ps,sb=[-p2]];[tm=j_i,vc=ps,sb=[+p2],+neg]
# ... gemination of the following consonant (C1!=L): yImmerreTal, yImmerarreTal
ij_ps -> i/         [/:]
# ... 0 when the root begins with C|: yInsaffefal, yICberebberal
ij_ps -> i|         [:]

## Combine causative, passive, and transitive prefixes, along with
## no prefix in one state (simp) because they are common to most roots
# Causative
as -> simp          [:]       [vc=cs]
# Passive (perfective, gerundive, imperative)
te -> simp          [:]
# Prevent reciprocal and iterative aspect (which need a/)
a -> simp           [:]       [as=smp]
# Simplex voice: no stem prefix
start -> simp       [:]       [vc=smp]

# Transitive and passive before C| verbs is special
a -> a_te           [:]       
te -> a_te          [:]

# Transitive iterative, reciprocal: geminate C1 after the prefix
a -> a/             [/:]      

#### END
### State names with "-" represent positions starting from the right:
###   -1 is right before the last consonant
###  -2V is right before the vowel following the second to last consonant

## Final consonant
-1 -> end           [X/L]

## Final vowels for most situations
# e: perfect; imperfect and jussive/imperative passive
#    (also for jussive/imperative simplex with CCC verbs but that's handled separately below)
-2V -> -1           [e:]      [tm=imf,vc=ps];[tm=j_i,vc=ps];[tm=prf]
# no vowel in other cases
-2V -> -1           [:]       [tm=imf,vc=smp];[tm=imf,vc=cs];[tm=imf,vc=tr]; [tm=j_i,vc=cs];[tm=j_i,vc=tr];[tm=j_i,vc=smp]; [tm=ger]

## Final vowel and consonant for final L, *
# a for final L except in gerundive
-2V -> end          [a:']     [tm=prf];[tm=imf];[tm=j_i]
# t for final L and * in gerundive
-2V -> end          [t:';t:*] [tm=ger]
# e for final * in perfective
-2V -> end          [e:*]     [tm=prf]
# no vowel for final * in imperfective and jussive/imperative
-2V -> end          [:*]      [tm=imf];[tm=j_i]

#### "A" verbs (CCC, C2 cannot be L, w, or y; these cases are handled below)

## Following C2
# geminate C2 in perfective, causative, imperfective passive
-2A_ -> -2V         [_:]      [tm=prf];[vc=cs];[tm=imf,vc=ps]
# no gemination in other cases
-2A_ -> -2V         [:]       [tm=imf,vc=smp];[tm=imf,vc=tr]; [tm=j_i,vc=tr]; [tm=ger,vc=smp];[tm=ger,vc=tr];[tm=ger,vc=ps]
# Final vowel: e for passive and simplex in jussive/imperative (simplex only for CCC)
-2A_ -> -1          [e:]      [tm=j_i,vc=ps];[tm=j_i,vc=smp]
# Final ', * for passive and simplex in jussive/imperative (a or 0, skipping to end)
-2A_ -> end         [a:']     [tm=j_i,vc=ps];[tm=j_i,vc=smp]
-2A_ -> end         [:*]      [tm=j_i,vc=ps];[tm=j_i,vc=smp]
# C2 (except after L): all root consonants except ', w, y (treated separately below)
-2A -> -2A_         [X!]
# following C1=L, y and w are also possible for C2
-2AL -> -2A_        [X/L]
# first stem vowel: e for perfective, imperfective, gerundive except transitive, jussive/imperative passive or causative
-3V -> -2A          [e:]      [tm=prf];[tm=ger,vc=smp];[tm=ger,vc=ps];[tm=ger,vc=cs];[tm=imf];[tm=j_i,vc=ps];[tm=j_i,vc=cs]
# no first stem vowel in other cases: gerundive transitive, jussive/imperative simplex or transitive
-3V -> -2A          [:]       [tm=j_i,vc=smp];[tm=j_i,vc=tr];[tm=ger,vc=tr]
# C1: all root consonants except L (treated separately below)
-3 -> -3V           [X/L]
# C1=L ('); no transitive voice possible
# C1 and V1 are a for perfective, imperfective, gerundive; jussive/imperative except simplex
-3L -> -3LV         [:']     [vc=smp];[vc=ps];[vc=cs]
-3LV -> -2AL        [a:]       [tm=prf];[tm=ger];[tm=imf];[tm=j_i,vc=ps];[tm=j_i,vc=cs]
# C1 and V1 are I in other case: jussive/imperative simplex
-3LV -> -2AL        [I:]       [tm=j_i,vc=smp]

## Transitive, passive, and causative prefixes (as well as no prefix) can precede CCC
simp -> -3          [:]
simp -> -3L         [:]
## Initial geminated consonant for imperfective and jussive passive
i/ -> -3            [:]

## C1=L in CCCC (e.g., aneTTese) apparently behaves like CCC in passive and causative (it has not transitive)
## ... the initial ' is dropped
as -> -3            [:']      [vc=cs]
te -> -3            [:']
# Initial geminated consonant for imperfective and jussive passive
i/ -> -3            [:']

#### Special "A" verbs (CXC, imperfective with w, y, ' as C2; reduplicated: CaCXC)
#### the same pattern of vowels works with all reduplicated forms in this category
#### State names contain .2 (because these behave like 2-consonant verbs)

## for C2=', the same vowel pattern applies to reduplicated and non-reduplicated forms, except for jussive
# C2=' surfaces as a for perfective, imperfective passive, jussive/imperative passive and simplex (simplex aspect)
# ... same, yIssam, sasame, yIssasam
-3V.2 -> -1          [a:']    [tm=prf];[tm=imf,vc=ps];[tm=j_i,vc=ps];[tm=j_i,vc=smp,as=smp]
# C2=' surfaces as 0 in other cases: imperfective except passive, gerundive, jussive/imperative except simple (simplex aspect)
# ... yIsImal, yIsasIm, assasIm
-3V.2 -> -1          [:']     [tm=imf,vc=smp];[tm=imf,vc=tr];[tm=imf,vc=cs];[tm=ger]
-3V.2 -> -1          [:']     [tm=j_i,as=it,vc=smp];[tm=j_i,as=rc,vc=smp];[tm=j_i,vc=tr];[tm=j_i,vc=cs]

# C2=w surfaces as o for perfective, imperfective and gerundive simplex (optionally); jussive/imperative passive
# ... mote, moto (also muto) (CHANGE FOR GENERATION)
-3V.2 -> -1          [o:w]    [tm=prf,as=smp];[tm=imf,as=smp];[tm=ger,as=smp];[tm=j_i,vc=ps]
# C2=w surfaces as u for jussive/imperative simplex aspect except passive, gerundive simplex aspect (optionally)
# ... yImut (but yImmot), muto (also moto)
-3V.2 -> -1          [u:w]    [tm=j_i,as=smp,vc=smp];[tm=j_i,as=smp,vc=tr];[tm=j_i,as=smp,vc=cs];[tm=ger,as=smp]
# C2=w surfaces as a for iterative aspect in perfective and imperfective+jussive/imperative passive
# ... mWamWate, yImWmWamWat
-3V.2 -> -1          [a:w]    [tm=prf,as=it];[tm=imf,vc=ps,as=it];[tm=j_i,vc=ps,as=it]
# C2=w surfaces as 0 for iterative aspect in other cases
# ... yImWamWIt (-> yImWamut)
-3V.2 -> -1          [:w]     [tm=imf,as=it,vc=smp];[tm=imf,as=it,vc=tr];[tm=imf,as=it,vc=cs]
-3V.2 -> -1          [:w]     [tm=j_i,as=it,vc=smp];[tm=j_i,as=it,vc=tr];[tm=j_i,as=it,vc=cs];[tm=ger,as=it]
# C1 before special C2: any root consonant other than L (')
-3.2 -> -3V.2        [X/L]

## Two classes of CCC verbs with C2=y
# C1 is palatal (cere, xeTe, etc.)
-3.2 -> -3PV.2       [J]
# C1 is not palatal (hEde, gETe, etc.)
-3.2 -> -3~PV.2      [~J]

# following palatal C1, y surfaces as e in simplex aspect (passive for jussive/imperative)
# optionally for gerundive (CHANGE FOR GENERATION)
# ... xeTe
-3PV.2 -> -1         [e:y]    [tm=prf,as=smp];[tm=imf,as=smp];[tm=ger,as=smp];[tm=j_i,vc=ps,as=smp]
# following palatal C1, y surfaces as a in iterative aspect: perfective, imperfective+jussive/imperative passive
# ... xaxaTe
-3PV.2 -> -1         [a:y]    [tm=prf,as=it];[tm=imf,vc=ps,as=it];[tm=j_i,vc=ps,as=it]
# following palatal C1, y surfaces as 0 in gerundive (optionally for simplex),
# imperfective+jussive/imperative except passive
# ... yIxIT, xITo
-3PV.2 -> -1         [:y]     [tm=j_i,vc=smp];[tm=j_i,vc=tr];[tm=j_i,vc=cs];[tm=ger]
# ... xaxITo, yIxaxIT
-3PV.2 -> -1         [:y]     [tm=imf,as=it,vc=smp];[tm=imf,as=it,vc=tr];[tm=imf,as=it,vc=cs]

# following non-palatal C1, y surfaces as E in perfective, imperfective simplex and passive iterative,
# gerundive simplex (optionally) and jussive/imperative passive (CHANGE FOR GENERATION)
# ... hEde, hEdo, fafEze, yIffafEz, fEzo
-3~PV.2 -> -1        [E:y]    [tm=prf];[tm=imf,as=smp];[tm=ger,as=smp];[tm=j_i,vc=ps];[tm=imf,vc=ps,as=it]
# following non-palatal C1, in other cases y surfaces as i
# ... yIhid, hido
-3~PV.2 -> -1        [i:y]    [tm=j_i,vc=smp];[tm=j_i,vc=tr];[tm=j_i,vc=cs];[tm=ger]
# ... yIfafiz, yafafiz
-3~PV.2 -> -1        [i:y]    [tm=imf,as=it,vc=smp];[tm=imf,as=it,vc=tr];[tm=imf,as=it,vc=cs]

## reduplicated (iterative) cases of CXC: precede by Ca
-4.2 -> -4V.2        [X]
-4V.2 -> -3.2        [a]

## Special CXC cases can preceded by normal voice prefixes and passive gemination of C1
i/ -> -3.2           [:]
simp -> -3.2         [:]

# reduplicated cases for exceptional CCC
i/ -> -4.2           [:]       [as=it]    # imf, jus passive iterative
te -> -4.2           [:]       [as=it]    # prf, ger, impv passive iterative
a/ -> -4.2           [:]       [as=it]    # transitive iterative
simp -> -4.2         [:]       [as=it]    # simple iterative

#### "B" verbs: CC_C, C2 cannot be ', since it can't be geminated
#### State names contain B

# Geminate C2 in all cases except jussive passive (optionally in imperative passive) (CHANGE FOR GENERATION)
-2B_ -> -2V         [_]        [tm=prf];[tm=imf];[tm=ger];[tm=j_i,vc=smp];[tm=j_i,vc=tr];[tm=j_i,vc=cs];[tm=j_i,vc=ps,sb=[+p2],-neg]
# No C2 gemination in jussive passive, optionally in the imperative
-2B_ -> -2V         [:_]       [tm=j_i,vc=ps]
# C2 can be y or w: qeyyere, lewweTe
-2B -> -2B_         [X/L]
-3V -> -2B          [e:]
# C1=L: realize as a; no transitive voice possible (as with CCC)
-3L -> -3LVB        [:']     [vc=smp];[vc=ps];[vc=cs]
-3LVB -> -2B        [a:]

#### 4-consonant and 5-consonant verbs without a before C-2 (CCCC, CCCCC, C|CCCC)
#### State names contain .4

# C-2 gemination, degemination
# no gemination of C-2 for gerundive and jussive/imperative
-2.4_ -> -2V        [:]     [tm=ger];[tm=j_i]
# gemination of C3 in other cases: perfective, imperative
-2.4_ -> -2V        [_:]    [tm=prf];[tm=imf]
# lexical gemination in the case of CC_C verb: ger; prf; imf; j_i smp, cs, tr smp
-2.4_ -> -2V        [_]     [tm=ger];[tm=prf];[tm=imf];[tm=j_i,vc=smp];[tm=j_i,vc=cs];[tm=j_i,vc=tr,as=smp]
# delete lexical gemination in jussive rc, it, and ps
-2.4_ -> -2V        [:_]    [tm=j_i,vc=ps];[tm=j_i,as=rc];[tm=j_i,as=it]

# C-2: any root consonant
-2.4 -> -2.4_       [X]
# vowel following C-3: 0 for gerundive and jussive/imperative
-3.4V -> -2.4       [:]       [tm=ger];[tm=j_i]
# vowel following C-3: e for perfective and imperfective
-3.4V -> -2.4       [e:]      [tm=prf];[tm=imf]
# C-3: any root consonant except ' (C-3=' handled below)
-3.4 -> -3.4V       [X/L]
# vowel after C-2: always e
-4.4V -> -3.4       [e:]

# C-3=' (babba, etc.): realized as a
-4.4V -> -2.4       [a:']

# C-4: any consonant except ' (C1=' handled below)
-4.4 -> -4.4V       [X/L]
# C-4=' (aneTTese, etc.): realized as a
-4.4L -> -3.4       [a:']
# vowel following first consonant of 5-consonant verbs (wexeneggere, etc.)
-5.5V -> -4.5       [e:]
# C1 for 5-consonant verbs: any root consonant
-5.5 -> -5.5V       [X]
-4.5 -> -4.5V       [X/L]    
-4.5V -> -3.5       [e:]     
-3.5 -> -3.5V       [X/L]    
-3.5V -> -2.4       [e:]     [tm=prf];[tm=imf]
-3.5V -> -2.4       [:]      [tm=ger];[tm=j_i]

## 4- and 5-consonant roots can be preceded by passive, transitive, causative
## prefixes and by no prefix
simp -> -4.4        [:]
simp -> -5.5        [:]
## also by initial gemination in passive imperfective and jussive
i/ -> -4.4          [:]
i/ -> -5.5          [:]

## causative and passive of CCC verbs with C1=L connect here
# ... astawweqe
ast -> -2.4         [a:']
# ... yIttewawweqe
tt -> -2.4          [a:']

## 4-consonant roots with C1=': no voice prefixes possible
## other cases are handled under CCC above (because they
## are apparently indistinguishable from them)
start -> -4.4L      [:]       [vc=smp]

#### ...aCC: "C" verbs (CaCC), CCaCC, C|CaCC, C|CCaCC
#### including iterative (reduplicative) versions of nearly all classes
#### State names contain a

# C-4: s.ebabbere
-4a -> -4aV         [X/L]
# vowel after C-4: se.babbere
-4aV -> -3a         [e:]
# be. in belexaxxe; CaCC, CCaCC iterative verbs
-4aV -> -3a         [e:a]     [as=it]
# C-3: seb.abbere
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
-4aL -> -4aLV       [:']      [vc=smp]
-4aL -> -4aLV       [:']     [vc=cs]
-4aLV -> -3a        [a:]
# passive: tewawweqe
-4aL -> -3a         [:']     [vc=ps]

## Special case of iterative passive or transitive CC' verbs with no vowel after C1
## ... tegfaffa, agfaffa
## We need to specify the whole path from here to the end.
# C1: (a)g.
-4a.L -> -4a.LV     [X/L]
# no vowel after C1: ag..
-4a.LV -> -3a.L     [:]       [as=it,vc=ps];[as=it,vc=tr]
# C2: agf.
-3a.L -> -3aV.L     [X]
# a after C2: agfa.
-3aV.L -> -2.L.4    [a]
# reduplicated C2: agfaf.
-2.L.4 -> -2.L.4_   [X]
# no gemination for gerundive and jussive/imperative: agfafto, agfafa
-2.L.4_ -> -2.LV    [:]       [tm=ger];[tm=j_i]
# gemination for perfective and imperfective: agfaffa, yagfaffal
-2.L.4_ -> -2.LV    [_:]      [tm=prf];[tm=imf]
# last segment: a for all but gerundive: agfaffa., yagfaffa.
-2.LV -> end        [a:']     [tm=prf];[tm=imf];[tm=j_i]
# last segment: t for gerundive: agfaft.o
-2.LV -> end        [t:']     [tm=ger]

## Transitive iterative: a preceding geminated C1
# CaCC
a/ -> -3a           [:]
# CCaCC
a/ -> -4a           [:]
# special iterative of CC': ag/faffa (realized as agfaffa)
a/ -> -4a.L         [:]
# CCCaCC: aggenefaffele
a/ -> -5a           [:]

## imperfective, jussive passive with geminated C1
i/ -> -3a           [:]
i/ -> -4a           [:]
i/ -> -5a           [:]
# special iterative of CC': /gfaffa (realized as gfaffa)
i/ -> -4a.L         [:]

## Consonant preceding | and following a- or te-
i| -> |             [X]
a_te -> |           [X]
# |: before CaCC (tensaffefe)
| -> -3a            [:|]
# |: before CCaCC (texqedaddeme)
| -> -4a            [:|]
# |: before CCCC (teCberebbere)
| -> -4.4           [:|]
# |: before CCCaCC (teCberebabbere)
| -> -5a            [:|]
# |: before CCCaCC (teCberebabbere)
| -> -6a|           [:|]
-6a| -> -5aV        [X/L]

## Transitive, causative, passive prefixes and no prefix before
## CaCC, CCaCC, CCCaCC
simp -> -3a         [:]
simp -> -4a         [:]
simp -> -5a         [:]
# Passive prefix before special CC' passive (tegfaffa)
te -> -4a.L         [:]

## Iterative of CCCCC verbs (maybe never happens?)
simp -> -6a         [:]       [as=it]
i/ -> -6a           [:]       [as=it]
# CCCCaCC: awwexenebabbere
a/ -> -6a           [:]       [as=it]

## CCC with C1=L: iterative
# causative: asawawweqe
as -> -4aL          [:]       [vc=cs]
# passive: tewawweqe
te -> -4aL          [:]
# simplex voice: awawweqe
start -> -4aL       [:]       [vc=smp]

## CCCC with C1=': iterative
# aneTaTTese
start -> -4a        [a:']     [vc=smp]
# anneTaTTese
a/ -> -4a           [:']
# asneTaTTese
as -> -4a           [:']      [vc=cs]
# yInneTaTTesal
i/ -> -4a           [:']
# teneTaTTese
te -> -4a           [:']

# Iterative transitive CCC with C1=L: astewawweqe
ast -> -3a          [e:']
# Iterative passive imperfective, jussive CCC with C1=L: yIttewawweqal
tt -> -3a           [e:']

end ->
