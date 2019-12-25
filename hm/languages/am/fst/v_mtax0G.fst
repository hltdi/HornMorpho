-> start

## Set the part of speecn
start -> pos   [:]     [pos=v]

# No conjunction or preposition
pos   -> neg   [:]     [cj1=None,pp=None,-rel,-sub,-def,rl=[-p,-acc]]

## CONJUNCTIONS (+sub is redundant)
pos   -> neg    >>cnj1<<

## PREPOSITIONS (+sub is redundant)
# Needed because rel prefix is different in Am imperf following prep
pos   -> rel1  >>prep<<
# Relative with no preposition
pos   -> rel   [:]      [pp=None,+sub,+rel,rl=[-p]]

## RELATIVE PREFIX (+sub is redundant)
rel -> rel1    <ye:>   [+rel,pp=None,+sub,rl=[-p]]
# alternate prefix when nothing precedes; leave out for generation
# rel -> rel1    [':]    [tm=imf,+rel,pp=None,+sub,rl=[-p]]
# second prefix for imperfective
rel1 -> neg    <m_I:>  [tm=imf]
rel1 -> neg    [:]     [tm=prf]

## NEGATIVE PREFIX
neg -> neg_a      [a:]    [+neg,ax=None]
neg_a -> sbjp     [:]     [tm=imf];[tm=j_i]
neg_a -> sbjp     [l:]    [tm=prf]
# Affirmative
neg ->  sbjp      [:]     [-neg]

## SUBJECT PREFIX
# Prefix only for imperfective and jussive
sbjp -> stem      [:]    [tm=prf];[tm=ger];[tm=j_i,sb=[+p2],-neg]
sbjp -> sbjp*     [:]    [tm=imf];[tm=j_i,sb=[-p2]];[tm=j_i,+neg]
# When nothing precedes the subject prefix
sbjp* -> sbjp0    [:]    [-sub,-neg]
# 'sebr, 'nsebr
sbjp0 -> sbjp1    [':]   [tm=imf,sb=[+p1],ob=[-p1]];[tm=j_i,sb=[+p1,+plr],ob=[-p1]]
sbjp0 -> sbjp1    [:]    [tm=j_i,sb=[-p1]];[tm=j_i,sb=[+p1,-plr]];[tm=imf,sb=[-p1]]
# Another prefix precedes the subject prefix
sbjp* -> sbjp1    [:]    [+sub];[+neg]
# 1s l: jussive and imperf neg 
sbjp1 -> stem     [l:]   [tm=j_i,sb=[+p1,-plr],ob=[-p1]];[tm=imf,sb=[+p1,-plr],ob=[-p1],+neg]
# y: 3sm and 3p
sbjp1 -> stem     [y:]   [sb=[-p1,-p2,+plr]]; [sb=[-p1,-p2,-plr,-fem]]
# Unless at the beginning of the word or negative, there is no 1s prefix, except in jussive
sbjp1 -> stem     [:]    [tm=imf,sb=[+p1,-plr],ob=[-p1],-neg]
# Treat t- and n- specially because they can be geminated
sbjp1 -> sbjp_t   [t:]   [sb=[+p2,-p1],ob=[-p2]];[sb=[-plr,-p1,-p2,+fem]]
sbjp_t -> stem    [!:]   [+sub];[+neg]
sbjp_t -> stem    [:]    [-sub,-neg]
sbjp1 -> sbjp_n   [n:]   [sb=[+plr,+p1,-p2],ob=[-p1]]
sbjp_n -> stem    [!:]

## STEM
# Irregular
# stem -> sbjs    +irr_stem+
# Regular
stem -> sbjs    >>vb_stem0G<<

### SUBJECT SUFFIXES AND OBJECT INFIXES
sbjs -> sbjs_i        [:]    [tm=imf];[tm=j_i]
sbjs -> sbjs_p        [:]    [tm=prf];[tm=ger]

## IMPERFECTIVE, JUSSIVE/IMPERATIVE
# 2/3 plural; go directly to obj
sbjs_i -> obj         [u:]   [sb=[-p1,+plr],ob=[+expl]];[sb=[-p1,+plr],+def];[sb=[-p1,+plr],ob=[-expl],ax=None]
# 2sf; go directly to obj; palatalize previous consonant
sbjs_i -> obj        <8i:>   [sb=[+p2,-p1,+fem,-plr,-frm]]
# No suffix: 1s, 2sm, 3s, 1p; 23p when there is no obj and aux
sbjs_i -> sbjs_i0     [:]    [sb=[+p2,-p1,-plr,-fem,-frm]];[sb=[+p1,-p2,-plr]];[sb=[-p1,-p2,-plr]];[sb=[+p1,-p2,+plr]];[sb=[-p1,+plr],tm=imf,ax=al,ob=[-expl],-def]
# Infixes for objects when there is no sbj suffix; -e- for 1s/p, 3sm, 2s frm; -0- for 2p, 3p, prp, 3sf, 2s frm, no obj; -I- for 2s
# -e- for -n, -N, -w, optionally for -wo(t)
sbjs_i0 -> obj        [e:]   [ob=[+p1,-p2,-prp,+expl]];[ob=[-p1,-p2,-plr,-fem,-prp,+expl]];[ob=[-p1,+p2,-plr,+frm,+expl]];[+def,ob=[-expl]]
# -I- for -h, -x, optionally for -wo(t)
sbjs_i0 -> obj        [I:]   [ob=[+p2,+expl,-plr,-prp]]
# No infix for -at, -ac_ew, -ac_hu
sbjs_i0 -> obj        [:]    [ob=[-expl],-def];[ob=[-p1,+plr,+expl]];[ob=[+prp,+expl]];[ob=[+p2,+expl,+plr,]];[ob=[-p1,-p2,-plr,+fem,+expl]]

## PERFECTIVE
# 3sm
sbjs_p -> obj         [e:]   [tm=prf,sb=[-p1,-p2,-plr,-fem]]
# 1s, 2sm: Ck, Vh
sbjs_p -> sbjs_pk     [7:]   [tm=prf,sb=[-plr]]
# 1s
sbjs_pk -> sbjs_pk1   [u:]   [sb=[+p1,-p2],ob=[-p1]]
# kuNN possible when there's no object
sbjs_pk1 -> negs_aux  <N_:>
sbjs_pk1 -> obj       [:]
# 2sm: infix for objects other than prep and for definite suffix
sbjs_pk -> obj        [e:]   [sb=[-p1,+p2,-fem],ob=[-prp,-p2,+expl]];[sb=[-p1,+p2,-fem],ob=[-expl],+def,+rel,+sub]
sbjs_pk -> obj        [:]    [sb=[-p1,+p2,-fem,-frm],ob=[-expl]];[sb=[-p1,+p2,-fem,-frm],ob=[-p2,+prp,+expl]]
# 2sf, no infix
sbjs_p -> obj         [x:]   [tm=prf,sb=[-p1,+p2,-plr,+fem,-frm],ob=[-p2]]
# 3sf, no infix
sbjs_p -> obj        <ec_:>  [tm=prf,sb=[-p1,-p2,-plr,+fem]]
# 1p, infix for 3sm obj and 2s frm and +def
sbjs_p -> sbjs_pn     [n:]   [tm=prf,sb=[+p1,+plr],ob=[-p1]]
sbjs_pn -> obj        [e:]   [ob=[-prp,-p1,-p2,-plr,+expl]];[ob=[-p1,+p2,-plr,+frm,-prp,+expl]];[ob=[-expl],+def,+rel,+sub]
sbjs_pn -> obj        [:]    [ob=[-expl],-def];[ob=[+prp,+expl]];[ob=[+plr,-prp,+expl]];[ob=[+p2,-plr,-prp,-frm,+expl]];[ob=[-p2,-plr,-prp,+fem,+expl]]
# 2p: prf or ger
sbjs_p -> obj      <ac_hu:>  [sb=[+p2,-p1,+plr],ob=[-p2]]
# 3p
sbjs_p -> obj         [u:]   [tm=prf,sb=[-p1,-p2,+plr]]

# GERUNDIVE
# 1; geminate and palatalize previous consonant
sbjs_p -> obj         <_8E:> [tm=ger,sb=[+p1,-p2,-plr],ob=[-p1]]
sbjs_p -> sbj_g1p     <en:>  [tm=ger,sb=[+p1,-p2,+plr],ob=[-p1]]
# 1p: infix for 2frm (handle later as prefix before -wo(t)?); 3sm
sbj_g1p -> obj        [e:]   [ob=[-prp,-p1,+expl]];[ob=[-p1,+p2,-plr,+frm,-prp,+expl]]
sbj_g1p -> obj        [:]    [ob=[-expl],-def];[ob=[+expl,-p2,+fem,-plr,-prp]];[ob=[+plr,-prp,+expl]];[ob=[+expl,+p2,-frm,-prp]];[ob=[+expl,+prp]]
# 2s (plural same as perfective)
sbjs_p -> sbj_g2m     <eh:>  [tm=ger,sb=[+p2,-p1,-plr,-fem,-frm],ob=[-p2]]
# 2sm: infix for 1 objects, non-prep
sbj_g2m -> obj        [e:]   [ob=[-prp,+p1,+expl]]
sbj_g2m -> obj        [:]    [ob=[-expl]];[ob=[-p2,+prp,+expl]];[ob=[-prp,-p1,-p2,+expl]]
sbjs_p -> obj         <ex:>  [tm=ger,sb=[+p2,-p1,-plr,+fem,-frm],ob=[-p2]]
# 3
sbjs_p -> obj         [o:]   [tm=ger,sb=[-p2,-p1,-plr,-fem]]
sbjs_p -> obj         [a:]   [tm=ger,sb=[-p2,-p1,-plr,+fem]]
sbjs_p -> obj         <ew:>  [tm=ger,sb=[-p2,-p1,+plr]]

### OBJECT SUFFIXES
# No object; not definite
obj -> negs_aux        [:]    [ob=[-expl],-def]
# 3sm suffix doubles as definite marker for relative clauses
obj -> negs_aux        [3:]   [ob=[-expl],+def,+rel,+sub]
# Explicit objects, also definite if relative
obj -> obj0            [:]    [ob=[+expl],+def,+rel];[ob=[+expl],-def,-rel]
# Prepositional
obj0 -> objs1          <b_:>  [ob=[+prp,+b,-l]]
obj0 -> objs1          <l_:>  [ob=[+prp,+l,-b]]
# Non-prepositional
obj0 -> objs1          [:]    [ob=[-prp]]
# No object; not definite
obj -> negs_aux        [:]    [ob=[-expl],-def]
# 3sm suffix doubles as definite marker for relative clauses
obj -> negs_aux        [3:]   [ob=[-expl],+def,+rel,+sub]
# Prepositional
obj -> objs1           <b_:>  [ob=[+prp,+b,-l,+expl]]
obj -> objs1           <l_:>  [ob=[+prp,+l,-b,+expl]]
# Non-prepositional
obj -> objs1           [:]    [ob=[-prp,+expl]]
# Pronouns
objs1  -> negs_aux     <N_:>  [ob=[+p1,-p2,-plr]]
objs1  -> negs_aux     [h:]   [ob=[-p1,+p2,-plr,-fem,-frm]]
objs1  -> negs_aux     [x:]   [ob=[-p1,+p2,-plr,+fem,-frm]]
objs1  -> negs_aux    <et:>   [ob=[-p1,-p2,-plr,-fem,+prp]]
# w, ew, t
objs1  -> negs_aux     [3:]   [ob=[-p1,-p2,-plr,-fem,-prp]]
objs1  -> negs_aux    <at:>   [ob=[-p1,-p2,-plr,+fem]]
objs1  -> negs_aux     [n:]   [ob=[+p1,-p2,+plr]]
objs1  -> negs_aux   <ac_hu:> [ob=[-p1,+p2,+plr,-frm]]
objs1  -> negs_aux   <ac_ew:> [ob=[-p1,-p2,+plr]]
objs1  -> negs_aux     <wo:>  [ob=[-p1,+p2,-plr,+frm]]

## NEGATIVE SUFFIX (required if verb is independent) or AUXILIARY VERB or ACCUSATIVE or NEGATIVE SUFFIX
# AUX; can't cooccur with +neg or +sub
negs_aux -> aux1  <al:>       [tm=imf,-sub,-neg,ax=al];[tm=ger,ax=al]
# ysebral, ysebrutal, sebrehal, sebrexal, sebrenal, sebracchWal, sebrewal
aux1  -> cj2      [:]         [sb=[-p1,-p2,-fem,-plr]];[sb=[-p1,-p2,+plr],ob=[+expl]];[tm=ger,sb=[+plr]];[tm=ger,sb=[+p2]]
aux1  -> cj2      <_ehu:>     [sb=[+p1,-p2,-plr]]
aux1  -> cj2      <_eh:>      [tm=imf,sb=[+p2,-p1,-plr,-fem,-frm]]
aux1  -> cj2      <_ex:>      [tm=imf,sb=[+p2,-p1,-plr,+fem,-frm]]
aux1  -> cj2      <_ec_:>     [sb=[-p2,-p1,-plr,+fem]]
aux1  -> cj2      <_en:>      [tm=imf,sb=[+p1,-p2,+plr]]
aux1  -> cj2      <_ac_hu:>   [tm=imf,sb=[-p1,+p2,+plr]]
aux1  -> cj2      <_u:>       [tm=imf,sb=[-p1,-p2,+plr],ob=[-expl]]
negs_aux -> noaux  [:]        [ax=None]
# NEGATIVE
negs_aux -> cj2  <Im:>        [+neg,-sub,tm=prf];[+neg,-sub,tm=imf]
# ACCUSATIVE
noaux -> cj2  <In:>     [+rel,+acc,pp=None,rl=[-p,+acc]]
# No negs_aux: juss_imp; imprf, prs, or prf: -neg,-ax,-acc; +neg,-ax,+sub,-acc
noaux -> cj2  [:]       [tm=j_i]; [tm=ger]; [tm=imf,-neg,-acc,rl=[-acc]]; [tm=imf,+neg,+sub,-acc,rl=[-acc]]; [tm=prs,-neg,-acc,rl=[-acc]]; [tm=prs,+neg,+sub,-acc,rl=[-acc]]; [tm=prf,-neg,-acc,rl=[-acc]]; [tm=prf,+neg,+sub,-acc,rl=[-acc]]

## CONJUNCTIVE SUFFIXES
cj2 -> end     >>cnj2<<
cj2 -> end  [:]               [cj2=None]

end ->
