-> start

## Set the part of speech
start -> light   [:]     [pos=v]

## Light verbs
light -> light_gap  +v_light+  [+lt]
light_gap -> pos         <//: >
light -> pos  [:]

# No conjunction or preposition
pos   -> neg   [:]     [cj1=None,pp=None,-rel,-sub,-def,-ye]

## CONJUNCTIONS (+sub is redundant)
pos   -> neg    >>cnj1<<
# salle, etc.
pos   -> obj  +irr_conj+

## PREPOSITIONS (+sub is redundant)
# Needed because rel prefix is different in Am imperf following prep
pos   -> rel1  >>prep<<
# Relative with no preposition
pos   -> rel   [:]      [pp=None,+sub,+rel]

## RELATIVE PREFIX (+sub is redundant)
rel -> rel1    <ye:>   [+rel,pp=None,+sub,+ye]
# alternate prefix when nothing precedes
rel -> rel1    [':]    [tm=imf,+rel,pp=None,+sub,-ye]
# second prefix for imperfective
rel1 -> neg    <m_I:>  [tm=imf]
rel1 -> neg    [:]     [tm=prf];[tm=prs]

## NEGATIVE PREFIX
neg -> neg_a      [a:]    [+neg,ax=None]
neg_a -> sbjp     [:]     [tm=imf];[tm=j_i]
neg_a -> sbjp     [l:]    [tm=prf]
# Affirmative
neg ->  sbjp      [:]     [-neg]
# alle affirmative and negative, present
neg -> obj     +alle+

## SUBJECT PREFIX
# Prefix only for imperfective and jussive
sbjp -> stem      [:]    [tm=prf];[tm=ger];[tm=j_i,sp=2,-neg]
sbjp -> sbjp*     [:]    [tm=imf];[tm=j_i,sp=1|3];[tm=j_i,+neg]
# When nothing precedes the subject prefix
sbjp* -> sbjp0    [:]    [-sub,-neg]
# 'sebr, 'nsebr
sbjp0 -> sbjp1    [':]   [tm=imf,sp=1,op=2|3];[tm=j_i,sp=1,sn=2,op=2|3]
sbjp0 -> sbjp1    [:]    [tm=j_i,sp=2|3];[tm=j_i,sp=1,sn=1];[tm=imf,sp=2|3]
# Another prefix precedes the subject prefix
sbjp* -> sbjp1    [:]    [+sub];[+neg]
# 1s l: jussive and imperf neg
sbjp1 -> stem     [l:]   [tm=j_i,sp=1,sn=1,op=2|3];[tm=imf,sp=1,sn=1,op=2|3,+neg]
# y: 3sm and 3p
sbjp1 -> stem     [y:]   [sp=3,sn=2]; [sp=3,sn=1,sg=m]
# Unless at the beginning of the word or negative, there is no 1s prefix, except in jussive
sbjp1 -> stem     [:]    [tm=imf,sp=1,sn=1,op=2|3,-neg]
# Treat t- and n- specially because they can be geminated
sbjp1 -> sbjp_t   [t:]   [sp=2,op=1|3];[sp=3,sn=1,sg=f]
sbjp_t -> stem    [!:]   [+sub,+rel];[+neg]
sbjp_t -> stem    [:]    [-sub,-neg];[+sub,-rel]
sbjp1 -> sbjp_n   [n:]   [sp=1,sn=2,op=2|3]
sbjp_n -> stem    [!:]

## STEM
# Irregular
stem -> sbjs    +irr_stem+
# Regular
stem -> sbjs    >>v_stemS<<

### SUBJECT SUFFIXES AND OBJECT INFIXES
sbjs -> sbjs_i        [:]    [tm=imf];[tm=j_i]
sbjs -> sbjs_p        [:]    [tm=prf];[tm=ger]

## IMPERFECTIVE, JUSSIVE/IMPERATIVE
# 2/3 plural; go directly to obj
sbjs_i -> obj         [u:]   [sp=2|3,sn=2,op=1|2|3];[sp=2|3,sn=2,+def];[sp=2|3,sn=2,op=None,ax=None]
# 2sf; go directly to obj; palatalize previous consonant
sbjs_i -> obj        <8i:>   [sp=2,sg=f,sn=1,-sf]
# No suffix: 1s, 2sm, 3s, 1p; 23p when there is no obj and aux
sbjs_i -> sbjs_i0     [:]    [sp=2,sn=1,sg=m,-sf];[sp=1,sn=1];[sp=3,sn=1];[sp=1,sn=2];[sp=2|3,sn=2,tm=imf,ax=al,op=None,-def]
# Infixes for objects when there is no sbj suffix; -e- for 1s/p, 3sm, 2s frm; -0- for 2p, 3p, prp, 3sf, 2s frm, no obj; -I- for 2s
# -e- for -n, -N, -w, optionally for -wo(t)
sbjs_i0 -> obj        [e:]   [op=1,ot=a];[op=3,on=1,og=m,ot=a];[op=2,on=1,+of];[+def,op=None,ot=a]
# -I- for -h, -x, optionally for -wo(t)
sbjs_i0 -> obj        [I:]   [op=2,on=1,ot=a]
# No infix for -at, -ac_ew, -ac_hu
sbjs_i0 -> obj        [:]    [op=None,-def];[op=2|3,on=2];[ot=b|m];[op=2,on=2];[op=3,on=1,og=f]

## PERFECTIVE
# 3sm
sbjs_p -> obj         [e:]   [tm=prf,sp=3,sn=1,sg=m]
# 1s, 2sm: Ck, Vh
sbjs_p -> sbjs_pk     [7:]   [tm=prf,sn=1]
# 1s
sbjs_pk -> sbjs_pk1   [u:]   [sp=1,op=2|3]
# kuNN possible when there's no object
sbjs_pk1 -> negs_aux  <N_:>
sbjs_pk1 -> obj       [:]
# 2sm: infix for objects other than prep and for definite suffix
sbjs_pk -> obj        [e:]   [sp=2,sg=m,op=1|3,ot=a];[sp=2,sg=m,op=None,+def,+rel,+sub]
sbjs_pk -> obj        [:]    [sp=2,sg=m,-sf,op=None];[sp=2,sg=m,-sf,op=1|3,ot=b|m]
# 2sf, no infix
sbjs_p -> obj         [x:]   [tm=prf,sp=2,sn=1,sg=f,-sf,op=1|3]
# 3sf, no infix
sbjs_p -> obj        <ec_:>  [tm=prf,sp=3,sn=1,sg=f]
# 1p, infix for 3sm obj and 2s frm, and +def
sbjs_p -> sbjs_pn     [n:]   [tm=prf,sp=1,sn=2,op=2|3]
sbjs_pn -> obj        [e:]   [op=3,on=1,ot=a];[op=2,on=1,ot=a,+of];[op=None,+def,+rel,+sub]
sbjs_pn -> obj        [:]    [op=None,-def];[ot=b|m];[on=2,ot=a];[op=2,on=1,-of,ot=a];[op=3,on=1,ot=b|m,og=f]
# 2p: prf or ger
sbjs_p -> obj      <ac_hu:>  [sp=2,sn=2,op=1|3]
# 3p
sbjs_p -> obj         [u:]   [tm=prf,sp=3,sn=2]

# GERUNDIVE
# 1; geminate and palatalize previous consonant
sbjs_p -> obj         <_8E:> [tm=ger,sp=1,sn=1,op=2|3]
sbjs_p -> sbj_g1p     <en:>  [tm=ger,sp=1,sn=2,op=2|3]
# 1p: infix for 2frm (handle later as prefix before -wo(t)?); 3sm
sbj_g1p -> obj        [e:]   [ot=a];[op=2,on=1,ot=a,+of]
sbj_g1p -> obj        [:]    [op=None,-def];[op=3,og=f,on=1,ot=a];[on=2,ot=a];[op=2,ot=a,-of];[ot=b|m]
# 2s (plural same as perfective)
sbjs_p -> sbj_g2m     <eh:>  [tm=ger,sp=2,sn=1,sg=m,-sf,op=1|3]
# 2sm: infix for 1 objects, non-prep
sbj_g2m -> obj        [e:]   [op=1,ot=a]
sbj_g2m -> obj        [:]    [op=None];[op=1|3,ot=b|m];[op=3,ot=a]
sbjs_p -> obj         <ex:>  [tm=ger,sp=2,sn=1,sg=f,-sf,op=1|3]
# 3
sbjs_p -> obj         [o:]   [tm=ger,sp=3,sn=1,sg=m]
sbjs_p -> obj         [a:]   [tm=ger,sp=3,sn=1,sg=f]
sbjs_p -> obj         <ew:>  [tm=ger,sp=3,sn=2]

### OBJECT SUFFIXES
# No object; not definite
obj -> negs_aux        [:]    [op=None,ot=a,-def]
# 3sm suffix doubles as definite marker for relative clauses
obj -> negs_aux        [3:]   [op=None,ot=a,+def,+rel,+sub]
# Explicit objects, also definite if relative
obj -> obj0            [:]    [op=1|2|3,+def,+rel];[op=1|2|3,-def,-rel]
# Prepositional
obj0 -> objs1          <b_:>  [ot=m]
obj0 -> objs1          <l_:>  [ot=b]
# Non-prepositional
obj0 -> objs1          [:]    [ot=a]
# Pronouns
objs1  -> negs_aux     <N_:>  [op=1,on=1]
objs1  -> negs_aux     [h:]   [op=2,on=1,og=m,-of]
objs1  -> negs_aux     [x:]   [op=2,on=1,og=f,-of]
objs1  -> negs_aux    <et:>   [op=3,on=1,og=m,ot=b|m]
# 3sm allomorphs: w, ew, t
objs1  -> negs_aux     [3:]   [op=3,on=1,og=m,ot=a]
objs1  -> negs_aux    <at:>   [op=3,on=1,og=f]
objs1  -> negs_aux     [n:]   [op=1,on=2]
objs1  -> negs_aux   <ac_hu:> [op=2,on=2]
objs1  -> negs_aux   <ac_ew:> [op=3,on=2]
objs1  -> objs_2frm    <wo:>  [op=2,on=1,+of]
objs_2frm -> negs_aux  [:;t:]

## NEGATIVE SUFFIX (required if verb is independent) or AUXILIARY VERB or ACCUSATIVE
# AUX; can't cooccur with +neg or +sub
negs_aux -> aux1  <al:>       [tm=imf,-sub,-neg,ax=al];[tm=ger,ax=al]
# ysebral, ysebrutal, sebrehal, sebrexal, sebrenal, sebracchWal, sebrewal
aux1  -> cj2      [:]         [sp=3,sn=1,sg=m];[sp=3,sn=2,op=1|2|3];[tm=ger,sn=2];[tm=ger,sp=2]
aux1  -> cj2      <_ehu:>     [sp=1,sn=1]
aux1  -> cj2      <_eh:>      [tm=imf,sp=2,sn=1,sg=m,-sf]
aux1  -> cj2      <_ex:>      [tm=imf,sp=2,sn=1,sg=f,-sf]
aux1  -> cj2      <_ec_:>     [sp=3,sn=1,sg=f]
aux1  -> cj2      <_en:>      [tm=imf,sp=1,sn=2]
aux1  -> cj2      <_ac_hu:>   [tm=imf,sp=2,sn=2]
aux1  -> cj2      <_u:>       [tm=imf,sp=3,sn=2,op=None]
negs_aux -> noaux  [:]        [ax=None]
# NEGATIVE
noaux -> cj2  <Im:>      [+neg,-sub,tm=prf];[+neg,-sub,tm=imf];[+neg,-sub,tm=prs]
# ACCUSATIVE
noaux -> cj2  <In:>     [+rel,+acc,pp=None]
# No negs_aux: juss_imp; imprf, prs, or prf: -neg,-ax,-acc; +neg,-ax,+sub,-acc
noaux -> cj2  [:]       [tm=j_i]; [tm=ger]; [tm=imf,-neg,-acc]; [tm=imf,+neg,+sub,-acc]; [tm=prs,-neg,-acc]; [tm=prs,+neg,+sub,-acc]; [tm=prf,-neg,-acc]; [tm=prf,+neg,+sub,-acc]

## CONJUNCTIVE SUFFIXES
cj2 -> end     >>cnj2<<
cj2 -> end  [:]               [cj2=None]

end ->
