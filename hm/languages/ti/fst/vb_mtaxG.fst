### Verb morphotactics for generation
### (For more comments, see vb_mtax.fst)

-> start

# No conjunction or preposition
start -> neg   [:]     [cj1=None,pp=None,-rel,-sub]

## CONJUNCTIONS (+sub is redundant)
start -> neg    >>cnj1<<
# Irregular way of forming negative of m- (passes over neg)
start -> stem   <Aym:> [tm=prf,cj1=mI,pp=None,-rel,+neg,+sub]
# kello, etc.
start -> allo  +conj_alloG+

## PREPOSITIONS (+sub is redundant)
start -> rel  >>prep<<
start -> rel   [:]      [pp=None,+sub,+rel]

## RELATIVE PREFIX (+sub is redundant)
rel -> neg     [R:]     [+rel,tm=prf];[+rel,tm=imf];[+rel,tm=ger]
rel -> neg     [:]      [-rel]

## NEGATIVE PREFIX
neg -> sbjp      <Ay:>  [+neg]
neg -> sbjp      [:]    [-neg]
# allo, yellen, yeblon, etc. are irregular, can have object suffixes, also (regularly) (prep)zI-
neg -> allo      +alloG+
# (a)yebIllun irregular, object suffixes are included, compatible with (prep)zI-
neg -> negs     +yeblunG+

## ALLO OBJECT INFIXES
# no object
allo -> negs      [:]    [ob=[-xpl]]
# 1p, 2s: -y- before 3o
allo -> allo3o    [y:]   [sb=[+p1,-p2,+plr],ob=[+xpl,-p1,-p2,-prp]];[sb=[-p1,+p2,-plr],ob=[+xpl,-p1,-p2,-prp]]
allo -> obj       [:]    [sb=[-p1,+p2,-plr],ob=[+xpl,+p1,-p2,-prp]];[sb=[-p1,+p2,-plr],ob=[+xpl,+prp]];[sb=[+p1,-p2,+plr],ob=[+xpl,+prp]]
allo -> obj       [:]    [sb=[+p1,-p2,+plr],ob=[+xpl,-p1,+p2,-prp]];[sb=[-p1,+p2,-plr],ob=[+xpl,-p1,+p2,-prp]]
# 2pm; -u(w)-
allo -> obj_t3   <uw:>   [sb=[-p1,-p2,+plr,-fem],ob=[-p1,-p2,-prp,+xpl]]
allo -> obj       [u:]   [sb=[-p1,-p2,+plr,-fem],ob=[+p1,-prp,+xpl]];[sb=[-p1,-p2,+plr,-fem],ob=[+prp,+xpl]]
# 2pf, 3pf: -I'-, -a-
allo -> obj_t3   <I':>   [sb=[-p1,+plr,+fem],ob=[-p1,-p2,-prp,+xpl]]
allo -> obj       [a:]   [sb=[-p1,+plr,+fem],ob=[+p1,-prp,+xpl]];[sb=[-p1,+plr,+fem],ob=[+p2,-prp,+xpl]];[sb=[-p1,+plr,+fem],ob=[+prp,+xpl]]
# 3m (s and p), 1s: -w- before 3o
allo -> allo3o    [w:]   [sb=[-p1,-p2,-fem],ob=[+xpl,-p1,-p2,-prp]];[sb=[+p1,-p2,-plr],ob=[+xpl,-p1,-p2,-prp]]
allo3o -> obj_t3  [_:]   [sb=[-p1,-plr]];[sb=[+p1]]
allo3o -> obj_t3  [:]    [sb=[+p3,+plr]]
allo -> obj       [:]    [sb=[-p1,-p2,-fem],ob=[+xpl,+p1,-prp]];[sb=[-p1,-p2,-fem],ob=[+xpl,+p2,-prp]];[sb=[-p1,-p2,-fem],ob=[+xpl,+prp]]
allo -> obj       [:]    [sb=[+p1,-p2,-plr],ob=[+xpl,+p2,-prp]];[sb=[+p1,-p2,-plr],ob=[+xpl,+prp]]
# 3sf: -t(_/I)-
allo -> obj_t3   <t_:>   [sb=[-p1,-p2,-plr,+fem],ob=[-p1,-p2,-prp,+xpl]]
allo -> obj      <tI:>   [sb=[-p1,-p2,-plr,+fem],ob=[+p1,-prp,+xpl]];[sb=[-p1,-p2,-plr,+fem],ob=[+p2,-prp,+xpl]];[sb=[-p1,-p2,-plr,+fem],ob=[+prp,+xpl]]

## SUBJECT PREFIX
# Prefix only for imperfective and jussive
sbjp -> stem      [:]    [tm=prf];[tm=ger];[tm=j_i,sb=[+p2],-neg]
sbjp -> sbjp*     [:]    [tm=imf];[tm=j_i,sb=[-p2]];[tm=j_i,+neg]
# When nothing precedes the subject prefix; insert a glottal stop for 1s
sbjp* -> sbjp0    [:]    [-sub,-neg]
sbjp0 -> sbjp1    [':]   [sb=[+p1,-plr],ob=[-p1]]
sbjp0 -> sbjp1    [:]    [sb=[-p1]]; [sb=[+plr]]
# Another prefix precedes the subject prefix; no glottal stop necessary for 1s
sbjp* -> sbjp1    [:]    [+sub];[+neg]
sbjp1 -> stem     [y:]  [sb=[-p1,-p2,+plr]]; [sb=[-p1,-p2,-plr,-fem]]
# Unless at the beginning of the word there is no 1s prefix, except in jussive
sbjp1 -> stem     [:]    [tm=imf,sb=[+p1,-plr]];[tm=j_i,sb=[+p1,-plr]]
sbjp1 -> stem     [t:]  [sb=[+p2,-p1],ob=[-p2]];[sb=[-plr,-p1,-p2,+fem]]
sbjp1 -> stem     [n:]  [sb=[+plr,+p1,-p2],ob=[-p1]]

## STEM
stem -> stemend   +irr_stem+
stem -> stemend   >>vb_stemG<<
stemend -> sbjs   [$:]

### SUBJECT SUFFIXES AND OBJECT INFIXES
sbjs -> sbjs_i    [:]    [tm=imf];[tm=j_i]
sbjs -> sbjs_p    [:]    [tm=prf];[tm=ger]
## IMPERFECTIVE, JUSSIVE/IMPERATIVE
# 2/3 plural
sbjs_i -> sbjs_iu   [u:]   [sb=[-p1,+plr,-fem]]
sbjs_i -> sbjs_ia   [a:]   [sb=[-p1,+plr,+fem]]
sbjs_i -> sbjs_ia   [I:]   [sb=[-p1,+plr,+fem],ob=[-p1,-p2,-prp,+xpl]]
# 2sf, I->i only when final
sbjs_i -> sbjs_ii   [I:]   [sb=[-p1,+p2,+fem,-plr]]
# Infixes before 3p objects
sbjs_iu -> obj_t3   [w:]   [ob=[-p1,-p2,-prp,+xpl]]
sbjs_ia -> obj_t3   [':]   [ob=[-p1,-p2,-prp,+xpl]]
sbjs_ii -> obj_t3   <y_:>  [ob=[-p1,-p2,-prp,+xpl]]
sbjs_iu -> obj      [:]    [ob=[+p1,+xpl]];[ob=[+p2,+xpl]];[ob=[+prp,+xpl]];[ob=[-xpl]]
sbjs_ia -> obj      [:]    [ob=[+p1,+xpl]];[ob=[+p2,+xpl]];[ob=[+prp,+xpl]];[ob=[-xpl]]
sbjs_ii -> obj      [:]    [ob=[+p1,+xpl]];[ob=[+p2,+xpl]];[ob=[+prp,+xpl]];[ob=[-xpl]]
# No suffix
sbjs_i -> sbjs_i0   [:]    [sb=[+p2,-p1,-plr,-fem]];[sb=[+p1,-p2,-plr]];[sb=[-p1,-p2,-plr]];[sb=[+p1,-p2,+plr]]
# Infixes for objects when there is no sbj suffix
sbjs_i0 -> obj      [e:]   [ob=[+prp,+xpl]];[ob=[+p2,-p1,-prp,+xpl]];[ob=[+p1,-p2,-prp,+xpl]]
# Jussive/imperative with 3rd person (non-prepositional) objects: geminate stem-final consonant
sbjs_i0 -> obj      [_:]   [tm=j_i,ob=[-p1,-p2,+xpl,-prp]]
# Imperfective with 3rd person objects; no object
sbjs_i0 -> obj      [:]    [ob=[-xpl]];[tm=imf,ob=[-p1,-p2,-prp,+xpl]]
## PERFECTIVE
sbjs_p -> obj       [@:]   [tm=prf,sb=[-p1,-p2,-plr,-fem]]
sbjs_p -> sbjs_p1s  <ku:>  [tm=prf,sb=[+p1,-p2,-plr],ob=[-p1]]
sbjs_p1s -> obj_t3  <w_:>  [ob=[-p1,-p2,-prp,+xpl]]
sbjs_p1s -> obj     [:]    [ob=[+p1,+xpl]];[ob=[+p2,+xpl]];[ob=[+prp,+xpl]];[ob=[-xpl]]
# -na, -ka, -ki work for both perfect and gerund and share y_ before 3 object                   
sbjs_p -> sbjs_py   <na:>  [sb=[+p1,-p2,+plr],ob=[-p1]]
sbjs_p -> sbjs_py   <ka:>  [sb=[-p1,+p2,-plr,-fem],ob=[-p2]]
sbjs_p -> sbjs_py   <kI:>  [sb=[-p1,+p2,-plr,+fem],ob=[-p2]]
sbjs_py -> obj_t3   <y_:>  [ob=[-p1,-p2,-prp,+xpl]]
sbjs_py -> obj      [:]    [ob=[+p1,+xpl]];[ob=[+p2,+xpl]];[ob=[+prp,+xpl]];[ob=[-xpl]]
# -kum and -kIn work for both perfect and gerund
sbjs_p -> sbjs_p2pm <kum:> [sb=[+p2,-p1,+plr,-fem],ob=[-p2]]
sbjs_p2pm -> obj_t3 <uw:>  [ob=[-p1,-p2,-prp,+xpl]]
sbjs_p2pm -> obj    [u:]   [ob=[+p1,+xpl]];[ob=[+prp,+xpl]]
sbjs_p2pm -> negs   [:]    [ob=[-xpl]]
sbjs_p -> sbjs_p2pf <kIn:> [sb=[+p2,-p1,+plr,+fem],ob=[-p2]]
sbjs_p2pf -> obj_t3 <a':>  [tm=prf,ob=[-p1,-p2,-prp,+xpl]]
sbjs_p2pf -> obj_t3 <I':>  [ob=[-p1,-p2,-prp,+xpl]]
sbjs_p2pf -> obj    [a:]   [ob=[+p1,+xpl]];[ob=[+prp,+xpl]]
sbjs_p2pf -> negs   [:]    [ob=[-xpl]]
# -et, -u, -a: perfective only
sbjs_p -> sbjs_p3sf  <@t:> [tm=prf,sb=[-p1,-p2,-plr,+fem]]
sbjs_p3sf -> obj_t3 [_:]   [ob=[-p1,-p2,-prp,+xpl]]
sbjs_p3sf -> obj    [:]    [ob=[+p1,+xpl]];[ob=[+p2,+xpl]];[ob=[+prp,+xpl]];[ob=[-xpl]]
sbjs_p -> sbjs_p3pm [u:]   [tm=prf,sb=[-p1,-p2,+plr,-fem]]
sbjs_p3pm -> obj_t3 [w:]   [ob=[-p1,-p2,-prp,+xpl]]
sbjs_p3pm -> obj    [:]    [ob=[+p1,+xpl]];[ob=[+p2,+xpl]];[ob=[+prp,+xpl]];[ob=[-xpl]]
sbjs_p -> sbjs_p3pf [a:]   [tm=prf,sb=[-p1,-p2,+plr,+fem]]
sbjs_p -> sbjs_p3pf [I:]   [tm=prf,sb=[-p1,-p2,+plr,+fem],ob=[-p1,-p2,-prp,+xpl]]                 
sbjs_p3pf -> obj_t3 [':]   [ob=[-p1,-p2,-prp,+xpl]]
sbjs_p3pf -> obj    [:]    [ob=[+p1,+xpl]];[ob=[+p2,+xpl]];[ob=[+prp,+xpl]];[ob=[-xpl]]
## GERUNDIVE
sbjs_p -> sbjs_g1s  [@:]   [tm=ger,sb=[+p1,-p2,-plr],ob=[-p1]]
sbjs_g1s -> obj_t3  <y_:>  [ob=[-p1,-p2,-prp,+xpl]]
sbjs_g1s -> obj     [:]    [ob=[+p1,+xpl]];[ob=[+p2,+xpl]];[ob=[+prp,+xpl]];[ob=[-xpl]]
sbjs_p -> sbjs_g3sf [a:]   [tm=ger,sb=[-p1,-p2,-plr,+fem]]
sbjs_g3sf -> obj_t3 <t_:>  [ob=[-p1,-p2,-prp,+xpl]]
sbjs_g3sf -> obj    <tI:>  [ob=[+p1,+xpl]];[ob=[+p2,+xpl]];[ob=[+prp,+xpl]]
sbjs_g3sf -> negs    [:]   [ob=[-xpl]]
sbjs_p -> sbjs_g3sm [u:]   [tm=ger,sb=[-p1,-p2,-plr,-fem]]
sbjs_g3sm -> obj_t3 [w:]   [ob=[-p1,-p2,-prp,+xpl]]
sbjs_g3sm -> obj    [:]    [ob=[+p1,+xpl]];[ob=[+p2,+xpl]];[ob=[+prp,+xpl]];[ob=[-xpl]]
sbjs_p -> sbjs_g3pm <om:>  [tm=ger,sb=[-p1,-p2,+plr,-fem]]
sbjs_g3pm -> obj_t3 <uw:>  [ob=[-p1,-p2,-prp,+xpl]]
sbjs_g3pm -> obj    [u:]   [ob=[+p1,+xpl]];[ob=[+p2,+xpl]];[ob=[+prp,+xpl]]
sbjs_g3pm -> negs   [:]    [ob=[-xpl]]
sbjs_p -> sbjs_g3pf <@n:>  [tm=ger,sb=[-p1,-p2,+plr,+fem]]
sbjs_g3pf -> obj_t3 <I':>  [ob=[-p1,-p2,-prp,+xpl]]
sbjs_g3pf -> obj    [a:]   [ob=[+p1,+xpl]];[ob=[+p2,+xpl]];[ob=[+prp,+xpl]]
sbjs_g3pf -> negs   [:]    [ob=[-xpl]]

### OBJECT SUFFIXES
obj -> negs        [:]     [ob=[-xpl]]
obj -> obj_tp      [l:]    [ob=[+prp,+xpl]]
obj -> obj_t       [:]     [ob=[-prp,+xpl]]
# Gemination of prepositional l-: singular and 1p subjects, 3 or 1s objects
obj_tp -> obj_t    [_:]    [sb=[-plr],ob=[-p1,-p2]];[sb=[-plr],ob=[+p1,-p2,-plr]];[sb=[+p1,-p2,+plr],ob=[-p1,-p2]]
obj_tp -> obj_t    [:]     [sb=[+plr,-p1]];[ob=[+p2,-p1]];[ob=[+p1,-p2,+plr]]
obj_t -> obj_t3    [:]     [ob=[-p1,-p2]]
obj_t -> obj_t2,1  [k:]    [ob=[+p2,-p1],sb=[-p2]]
obj_t -> obj_t1,1  [n:]    [ob=[+p1,-p2],sb=[-p1]]
obj_t -> negs      <ey:>    [ob=[+p1,-p2,-plr,+prp],sb=[-p1]]
# Gemination of 1 and 2 person
obj_t2,1 -> obj_t2 [_:]    [sb=[+p1,-p2,+plr],ob=[-prp]];[sb=[-p1,-p2,-plr],ob=[-prp]];[tm=imf,sb=[+p1,-plr],ob=[-prp]];[tm=j_i,sb=[+p1,-plr],ob=[-prp]];[tm=ger,sb=[+p1,-plr],ob=[-prp]]
obj_t2,1 -> obj_t2 [:]     [sb=[-p1,+plr]];[tm=prf,sb=[+p1,-plr]];[ob=[+prp]]
obj_t1,1 -> obj_t1 [_:]    [sb=[-plr],ob=[-prp]]
obj_t1,1 -> obj_t1 [:]     [sb=[+plr]];[ob=[+prp]]
# Final segments
obj_t3 -> negs     [o:]    [ob=[-plr,-fem,-prp]]
obj_t3 -> negs     [u:]    [ob=[-plr,-fem,+prp]]
obj_t3 -> negs     [a:]    [ob=[-plr,+fem]]
obj_t3 -> negs     <om:>   [ob=[+plr,-fem]]
obj_t3 -> negs     <@n:>   [ob=[+plr,+fem]]
obj_t1 -> negs     [I:]    [ob=[-plr,-prp]]
obj_t1 -> negs     [a:]    [ob=[+plr]]
obj_t2 -> negs     [a:]    [ob=[-plr,-fem]]
obj_t2 -> negs     [I:]    [ob=[-plr,+fem]]
obj_t2 -> negs     <um:>   [ob=[+plr,-fem]]
obj_t2 -> negs     <In:>   [ob=[+plr,+fem]]

## NEGATIVE SUFFIX: required if verb is independent
negs -> cj2  [n:]         [+neg,-sub,tm=prf];[+neg,-sub,tm=imf];[+neg,-sub,tm=prs]
negs -> cj2  [:]          [-neg];[+neg,+sub];[tm=j_i]

## CONJUNCTIVE SUFFIXES
cj2 -> end     >>cnj2<<
cj2 -> end  [:]           [cj2=None,-yn,pos=v]

end ->
