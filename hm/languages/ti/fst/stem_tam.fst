-> start

### PREFIXES

start -> a          [A:]      [vc=tr]
# Perfective, gerundive, imperative
start -> te         <te!:>    [vc=ps,tm=prf];[vc=ps,tm=ger];[tm=j_i,vc=ps,sb=[+p2],-neg]
# ! is needed here are elsewhere to mark the end of stem prefixes;
# For cases where imperfective passive has no prefix (CCC, CC_C, CCCC)
start -> ip         [!:]       [tm=imf,vc=ps]

# imperfective passive with gemination, jussive passive
start -> ij_ps      [:]       [tm=imf,vc=ps];[tm=j_i,vc=ps,sb=[-p2]];[tm=j_i,vc=ps,sb=[+p2],+neg]
ij_ps -> i/         </!:>
ij_ps -> i|         [!:]

te -> simp          [:]
# transitive a- precedes ungeminated consonant in simplex aspect
a -> simp           [!:]      [as=smp]
# transitive a- precedes geminated consonant in reciprocal and iterative aspects
a -> simp           </!:>     [as=it];[as=rc]
start -> simp       [!:]      [vc=smp]

a -> a_te           [!:]
te -> a_te          [:]

# For passive iterative CCC verbs with C1=L in imperfective and jussive
start -> tt         <t_e!:>    [vc=ps,as=it,tm=imf];[vc=ps,as=it,tm=j_i,sb=[-p2]];[vc=ps,tm=j_i,sb=[+p2],+neg]
# For transitive iterative CCC verbs with C1=L
a -> tt             <t_e!:>    [as=it]

### END

-1 -> end           [X/L]
-1L -> end          [L]
-1X -> end          [X]

# Final vowels for most situations
-2V -> -1           [e:]      [tm=prf];[tm=imf,vc=ps];[tm=j_i,vc=ps]
-2V -> -1           [:]       [tm=imf,vc=smp];[tm=imf,vc=tr];[tm=j_i,vc=tr];[tm=j_i,vc=smp]
-2V -> -1X          [i:]      [tm=ger]
# Final vowels following ...aC.C
# Distinguished because of the I in imf and j_i smp/smp
-2aV -> -1          [e:]      [tm=prf];[tm=imf,vc=ps];[tm=j_i,vc=ps]
-2aV -> -1          [I:]      [tm=imf,vc=smp];[tm=imf,vc=tr];[tm=j_i,vc=tr];[tm=j_i,vc=smp]
-2aV -> -1X         [i:]      [tm=ger]
-2aV -> -1L         [a:]      [tm=imf,vc=ps];[tm=j_i,vc=ps];[tm=prf,sb=[+p1]];[tm=prf,sb=[+p2]]
# Perfect: 3 person (all voices? aspects?); imperfect not passive
-2aV -> -1L         [I:]      [tm=prf,sb=[-p1,-p2]];[tm=imf,vc=smp];[tm=imf,vc=tr];[tm=j_i,vc=tr];[tm=j_i,vc=smp]
#-2aV -> -1L         [i:]      [tm=ger]

# Final L
# Imperfect and jussive-imperative passive, perfect: 1,2 person (all voices? aspects?)
-2V -> -1L          [a:]     [tm=imf,vc=ps];[tm=j_i,vc=ps];[tm=prf,sb=[+p1]];[tm=prf,sb=[+p2]]
# Perfect: 3 person (all voices? aspects?); imperfect not passive
-2V -> -1L          [:]      [tm=prf,sb=[-p1,-p2]];[tm=imf,vc=smp];[tm=imf,vc=tr];[tm=j_i,vc=tr];[tm=j_i,vc=smp]
#-2V -> -1L          [i:]     [tm=ger]

### A (CCC)

# Final vowel dropped OPTIONALLY for passive perfect when vowel suffix (3 person subject) follows
-2A_ -> -1          [:]       [tm=prf,vc=ps,sb=[-p1,-p2]]
-2A_ -> -1L         [:]       [tm=prf,vc=ps,sb=[-p1,-p2]]
# e for ps and smp in jussive-imperative (a before L)
-2A_ -> -1          [e:]      [tm=j_i,vc=ps];[tm=j_i,vc=smp]
-2A_ -> -1L         [a:]      [tm=j_i,vc=ps];[tm=j_i,vc=smp]
-2A_ -> -2V         [_:]      [tm=imf,vc=ps]
-2A_ -> -2V         [:]       [tm=ger];[tm=j_i,vc=tr];[tm=prf]
## Imperfective simplex/transitive gemination of C2
# Geminate tr and smp imperf when there is no sb or ob suffix
-2A_ -> -2V         [_:]      [tm=imf,vc=smp,ob=[-xpl],sb=[+p1,+plr]];[tm=imf,vc=smp,ob=[-xpl],sb=[-p2,-plr]];[tm=imf,vc=smp,ob=[-xpl],sb=[-p1,+p2,-plr,-fem]]
-2A_ -> -2V         [_:]      [tm=imf,vc=tr,ob=[-xpl],sb=[+p1,+plr]];[tm=imf,vc=tr,ob=[-xpl],sb=[-p2,-plr]];[tm=imf,vc=tr,ob=[-xpl],sb=[-p1,+p2,-plr,-fem]]
# No gemination in imperf tr and smp if there is a sb or ob suffix
-2A_ -> -2V         [:]       [tm=imf,vc=smp,ob=[+xpl]];[tm=imf,vc=smp,sb=[+p2,+fem]];[tm=imf,vc=smp,sb=[-p1,+plr]]
-2A_ -> -2V         [:]       [tm=imf,vc=tr,ob=[+xpl]];[tm=imf,vc=tr,sb=[+p2,+fem]];[tm=imf,vc=tr,sb=[-p1,+plr]]

## C2
-2A -> -2A_         [X/L]

## V1
-3AV -> -2A         [e:]      [tm=prf,vc=smp];[tm=prf,vc=ps];[tm=imf,vc=smp]
-3AV -> -2A         [e:]      [tm=ger,vc=smp];[tm=ger,vc=ps];[tm=j_i,vc=ps]
# First vowel in CCC jussive/imperative non-passive and in imperfective passive/simple and perfective transitive an exception
-3AV -> -2A         [:]       [tm=imf,vc=ps];[tm=imf,vc=tr];[tm=prf,vc=tr];[tm=j_i,vc=smp];[tm=j_i,vc=tr];[tm=ger,vc=tr]

## C1
-3 -> -3AV          [X]

simp -> -3          [:]
ip -> -3            [:]
i/ -> -3            [:]       [tm=j_i]

### A (CLC)

## V2
# C1 != a
# C(e)LaC
-2LV -> -1          [a:]      [tm=prf];[tm=imf,vc=ps];[tm=j_i,vc=smp];[tm=j_i,vc=ps]
# C(e)LIC
-2LV -> -1          [I:]      [tm=imf,vc=smp];[tm=imf,vc=tr];[tm=j_i,vc=tr]
# C(e)LiC
-2LV -> -1          [i:]      [tm=ger]

# C1 = a
# CaLaC
-2LVa -> -1         [a:]      [tm=prf,vc=smp];[tm=prf,vc=ps];[tm=imf,vc=ps]
# CaLC
-2LVa -> -1         [:]       [tm=prf,vc=ps]
# CaLiC
-2LVa -> -1         [i:]      [tm=ger,vc=ps]

## CVL.VC
-2L -> -2LV         [L]
# V1=a
-2La -> -2LVa       [L]

## V1
# CL...
-3LV -> -2L         [:]       # possible with any form
# CaL...
-3LV -> -2La        [a:]      [vc=ps];[tm=prf,vc=smp]
# CeL...
-3LV -> -2L         [e:]      [tm=prf,vc=smp];[tm=prf,vc=ps];[tm=imf,vc=ps];[tm=j_i,vc=ps]

## C.VLVC
-3L -> -3LV         [X/L]

## prefixes
simp -> -3L         [:]
#a -> -3L            [:]
i/ -> -3L           [:]
#te -> -3L           [:]
#start -> -3L        [!:]       [vc=smp]

### B (CC_C)

-2B_ -> -2V         [_]

-2B -> -2B_         [X]
-3BV -> -2B         [e:]      [tm=prf];[tm=ger];[tm=imf,vc=tr];[tm=j_i]
-3BV -> -2B         [I:]      [tm=imf,vc=smp];[tm=imf,vc=ps]
-3B -> -3BV         [X]

## prefixes
simp -> -3B         [:]
ip -> -3B           [:]
i/ -> -3B           [:]       [tm=j_i]

### CCCC, C|CCC, CCCCC

## C3 (CCCC), C4 (CCCCC)
-2.4 -> -2V       [X]
# ...CaCC verbs
-2a.4 -> -2a.4V     [X]
# sebab.ere, feSaSS.eme, feSaS.eme
# how to prevent ba*kk*ene?
-2a.4V -> -2aV      [:;_;:_]

-3.4V -> -2.4       [:]

## C2 (CCCC), C3 (CCCCC)
-3.4 -> -3.4V       [X]
-3L.4 -> -3.4V      [L]

## V1 (CCCC), V2 (CCCCC)
# e in prf, ger, trans imprf, j_i
-4.4V -> -3.4       [e:]      [tm=prf];[tm=ger];[tm=imf,vc=tr];[tm=j_i]
# a also possible before laryngeal
-4.4V -> -3L.4      [a:]      [tm=prf];[tm=ger];[tm=imf,vc=tr]
# I otherwise
-4.4V -> -3.4       [I:]      [tm=imf,vc=smp];[tm=imf,vc=ps]

## C1 (CCCC)
-4.4 -> -4.4V       [X]
## C1 (CCCCC)
-5.4 -> -5.4V       [X]
## V1 (CCCCC)
-5.4V -> -4.4       [e:]

## prefixes
simp -> -4.4        [:]
ip -> -4.4          [:]
simp -> -5.4        [:]
ip -> -5.4          [:]
i/ -> -4.4          [:]       [tm=j_i]
i/ -> -5.4          [:]

### ...aCC: C (CaCC), CCaCC, C|CaCC, C|CCaCC

# CaCC and end of others
# seba.bere
-3aV -> -2a.4       [a]

# seb.abere
-3a -> -3aV         [X/L]
-3aL -> -3aV        [L]
-4aV -> -3a         [e:]
# iterative of CaCC, CCaCC verbs
-4aV -> -3a         [e:a]        [as=it]
-4aV -> -3aL        [I:;a:;e:]

# s.ebabere
-4a -> -4aV         [X/L]
# H.edadere
-4aL -> -4aV        [L]
-5aV -> -4a         [e:]
-5a -> -5aV         [X] 

# denegageSe (must be CCCC +it)
start -> -5a        [!:]       [as=it]

# imperfect passive iterative
i/ -> -3a           [:]
i/ -> -4a           [:]
# ynqTqeT
i/ -> -5a           [:]

# transitive iterative, reciprocal
a -> a/             </!:>      [as=it];[as=rc]

a/ -> -3a           [:]
a/ -> -4a           [:]
# addenegageSe
a/ -> -5a           [:]

| -> -3a            [:|]
| -> -4a            [:|]
| -> -4.4           [:|]
| -> -5a            [:|]

i| -> |             [X]
a_te -> |           [X]

simp -> -3a         [:]
simp -> -3aL        [:]
simp -> -4a         [:]
# tedenegageSe; no a- or 0- for CCCC iterative
te -> -5a           [:]

te -> -4aL          [:]
tt -> -4aL          [:]
# Alternative for +it+tr in imf and j_i
tt -> -4a           [:]      [vc=tr,as=it,tm=imf];[vc=tr,as=it,tm=j_i]
# Hadadere; is this always +it?
start -> -4aL       [!:]     [vc=smp]

end ->
