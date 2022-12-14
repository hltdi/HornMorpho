-> start

## Suppletive verbs
start -> obj  <na:{mT'++na}($mood=jus,gender=masc,number=sing,person=2)>  [cls=A,bs=0,tm=j_i,vc=smp,as=smp,-neg,sb=[-p1,+p2,-fem,-plr,-frm],cj1=None,cj2=None,pp=None,ax=None,-rel,-sub,-acc,root=መጣ,lemma=መጣ,pos=v,ob=[+prp]]
start -> obj  <ney:{mT'++ney}($mood=jus,gender=fem,number=sing,person=2)>  [cls=A,bs=0,tm=j_i,vc=smp,as=smp,-neg,sb=[-p1,+p2,+fem,-plr,-frm],cj1=None,cj2=None,pp=None,ax=None,-rel,-sub,-acc,root=መጣ,lemma=መጣ,pos=v,ob=[+prp]]
start -> obj  <nu:{mT'++nu}($mood=jus,number=plur,person=2)>  [cls=A,bs=0,tm=j_i,vc=smp,as=smp,-neg,sb=[-p1,+p2,+plr,-frm],cj1=None,cj2=None,pp=None,ax=None,-rel,-sub,-acc,root=መጣ,lemma=መጣ,pos=v,ob=[+prp]]

## Set the part of speecn
start -> light   [:]     [pos=v]

## Light verbs (later leave these out for 1-word FSTs)
light -> light1         [:{]   [+lt]
light1 -> light_gap     +v_light+
light_gap -> pos         <//:}->
light -> pos  [:]

# No conjunction or preposition
pos   -> neg   [:]     [cj1=None,pp=None,-rel,-sub,-def,-ye]

## CONJUNCTIONS (+sub is redundant)
pos   -> neg    >>cnj1X<<
# salle, etc.
pos   -> obj  >>irr_conjX<<

## PREPOSITIONS (+sub is redundant)
# Needed because rel prefix is different in Am imperf following prep
pos   -> rel1  >>prepX<<
# Relative with no preposition
pos   -> rel   [:]      [pp=None,+sub,+rel]

## RELATIVE PREFIX (+sub is redundant)
# % 'mark' is from the TB; probably should be something else
rel -> rel1    <ye:ye(@part,rlp,*የ,~mark)->   [+rel,pp=None,+sub,+ye]
# alternate prefix when nothing precedes
rel -> rel1    [':]    [tm=imf,+rel,pp=None,+sub,-ye]
# second prefix for imperfective
# % 'mark' if from the TB; probably should be something else
rel1 -> neg    <m_I:'m_(@part,irlp,*እም,~mark)->  [tm=imf]
rel1 -> neg     [:]      [tm=prf];[tm=prs]

## NEGATIVE PREFIX
neg -> neg_a      <a:'A>    [+neg,ax=None]
neg_a -> sbjp     [:]     [tm=imf];[tm=j_i]
neg_a -> sbjp     <l:l(@part,$polarity=neg,*ኣል,~advmod)->    [tm=prf]
# Affirmative
neg ->  sbjp      [:]     [-neg]
# alle affirmative and negative, present
neg -> obj     >>alleX<<

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
# % Should the lemma be "I"?
sbjp1 -> stem     <l:l(@pron,$number=sing,person=1,*ል,~nsubj)->   [tm=j_i,sb=[+p1,-plr],ob=[-p1],-neg]
sbjp1 -> stem     <l:l(@part,$polarity=neg,number=sing,person=1,*ኣል,~advmod)->   [tm=imf,sb=[+p1,-plr],ob=[-p1],+neg]
# y: 3sm and 3p
sbjp1 -> stem     <y:y(@pron,$person=3,*ይ,~nsubj)->   [sb=[-p1,-p2,+plr],-neg]; [sb=[-p1,-p2,-plr,-fem],-neg]
sbjp1 -> stem     <y:y(@part,$polarity=neg,person=3,*ኣል,~advmod)->   [sb=[-p1,-p2,+plr],+neg]; [sb=[-p1,-p2,-plr,-fem],+neg]
# Unless at the beginning of the word or negative, there is no overt 1s prefix, except in jussive
sbjp1 -> stem     <:'(@pron,$number=sing,person=1,*እ,~nsubj)->    [tm=imf,sb=[+p1,-plr],ob=[-p1],-neg]
# t, n: 1p, 2, 3sf
sbjp1 -> stem     <t:t(@pron,$person=2,*ት,~nsubj)->   [sb=[+p2,-p1],ob=[-p2],-neg]
sbjp1 -> stem     <t:t(@pron,$gender=fem,number=sing,person=3,*ት,~nsubj)->   [sb=[-plr,-p1,-p2,+fem],-neg]
sbjp1 -> stem     <t:t(@part,$polarity=neg,person=2,*ኣል,~advmod)->   [sb=[+p2,-p1],ob=[-p2],+neg]
sbjp1 -> stem     <t:t(@part,$polarity=neg,gender=fem,number=sing,person=3,*ኣል,~advmod)->  [sb=[-plr,-p1,-p2,+fem],+neg]
sbjp1 -> stem     <n:'n(@pron,$number=plur,person=1,*እን,~nsubj)->           [sb=[+plr,+p1,-p2],ob=[-p1],-neg]
sbjp1 -> stem     <n:n(@part,$polarity=neg,number=plur,person=1,*ኣል,~nsubj)->      [sb=[+plr,+p1,-p2],ob=[-p1],+neg]

## STEM

# Irregular
stem -> stem0     [:{]
stem0 -> tmp_end      +irr_stemX+

# Regular stem
stem0 -> tmp    >>v_stemX<<

# Template
tmp -> tmp_end     >>tmp<<

tmp_end -> stem_feats   [:}]

# End of stem+template
stem_feats -> sbjs  >>stem_featsX<<

### SUBJECT SUFFIXES AND OBJECT INFIXES
sbjs -> sbjs_i        [:]    [tm=imf];[tm=j_i]
sbjs -> sbjs_p        [:]    [tm=prf];[tm=ger]

## IMPERFECTIVE, JUSSIVE/IMPERATIVE
# 2/3 plural; go directly to obj
# % 2/3 should be converted to 2,3
sbjs_i -> obj        <u:-u(@pron,subj,$number=plur,person=2/3,*ኡ,~nsubj)>   [sb=[-p1,+plr],ob=[+expl]];[sb=[-p1,+plr],ob=[-expl],ax=None]
#;[sb=[-p1,+plr],+def]
# 2sf; go directly to obj; palatalize previous consonant; don't show the palatalization character
sbjs_i -> obj        <8i:-i(@pron,subj,$gender=fem,number=sing,person=2,*ኢ,~nsubj)>   [sb=[+p2,-p1,+fem,-plr,-frm]]
# No suffix: 1s, 2sm, 3s, 1p; 23p when there is no obj and aux
sbjs_i -> sbjs_i0     [:]    [sb=[+p2,-p1,-plr,-fem,-frm]];[sb=[+p1,-p2,-plr]];[sb=[-p1,-p2,-plr]];[sb=[+p1,-p2,+plr]];[sb=[-p1,+plr],tm=imf,ax=al,ob=[-expl],-def]
# Infixes for objects when there is no sbj suffix; -e- for 1s/p, 3sm, 2s frm; -0- for 2p, 3p, prp, 3sf, 2s frm, no obj; -I- for 2s
# -e- for -n, -N, -w, optionally for -wo(t)
#sbjs_i0 -> obj        <e:-e(infix)>   [ob=[+p1,-p2,-prp,+expl]];[ob=[-p1,-p2,-plr,-fem,-prp,+expl]];[ob=[-p1,+p2,-plr,+frm,+expl]]
sbjs_i0 -> obj        <e:-e->   [ob=[+p1,-p2,-prp,+expl]];[ob=[-p1,-p2,-plr,-fem,-prp,+expl]];[ob=[-p1,+p2,-plr,+frm,+expl]]
#;[+def,ob=[-expl]]
# -I- for -h, -x, optionally for -wo(t)
sbjs_i0 -> obj        [I:]   [ob=[+p2,+expl,-plr,-prp]]
# No infix for -at, -ac_ew, -ac_hu
sbjs_i0 -> obj        [:]    [ob=[-expl],-def];[ob=[-p1,+plr,+expl]];[ob=[+prp,+expl]];[ob=[+p2,+expl,+plr,]];[ob=[-p1,-p2,-plr,+fem,+expl]]

## PERFECTIVE
# 3sm
sbjs_p -> obj         <e:-e(@pron,subj,$gender=masc,number=sing,person=3,*ኧ,~nsubj)>   [tm=prf,sb=[-p1,-p2,-plr,-fem]]
# 1s, 2sm: Ck, Vh; represent as 'h' in output
sbjs_p -> sbjs_pk     <7:-h>   [tm=prf,sb=[-plr]]
# 1s
sbjs_pk -> sbjs_pk1   <u:u(@pron,subj,$number=sing,person=1,*ኩ,~nsubj)>   [sb=[+p1,-p2],ob=[-p1]]
# kuNN possible when there's no object
sbjs_pk1 -> negs_aux  <N_>
sbjs_pk1 -> obj       [:]
# 2sm: infix for objects other than prep and for definite suffix
sbjs_pk -> obj        <e:(@pron,subj,$gender=masc,number=sing,person=2,*ክ,~nsubj)-e->   [sb=[-p1,+p2,-fem],ob=[-prp,-p2,+expl]]
#sbjs_pk -> obj        <e:(@pron,subj,$gender=masc,number=sing,person=2)-e(inf)>   [sb=[-p1,+p2,-fem],ob=[-prp,-p2,+expl]]
#;[sb=[-p1,+p2,-fem],ob=[-expl],+def,+rel,+sub]
sbjs_pk -> obj        <:(@pron,subj,$gender=masc,number=sing,person=2,*ክ,~nsubj)>    [sb=[-p1,+p2,-fem,-frm],ob=[-expl]];[sb=[-p1,+p2,-fem,-frm],ob=[-p2,+prp,+expl]]
# 2sf, no infix
sbjs_p -> obj         <x:-x(@pron,subj,$gender=fem,number=sing,person=2,*ሽ,~nsubj)>   [tm=prf,sb=[-p1,+p2,-plr,+fem,-frm],ob=[-p2]]
# 3sf, no infix
sbjs_p -> obj        <ec_:-ec_(@pron,subj,$gender=fem,number=sing,person=3,*ኧች,~nsubj)>  [tm=prf,sb=[-p1,-p2,-plr,+fem]]
# 1p, infix for 3sm obj and 2s frm, and +def
sbjs_p -> sbjs_pn     <n:-n(@pron,subj,$number=plur,person=1,*ን,~nsubj)>   [tm=prf,sb=[+p1,+plr],ob=[-p1]]
#sbjs_pn -> obj        <e:-e(infix)>   [ob=[-prp,-p1,-p2,-plr,+expl]];[ob=[-p1,+p2,-plr,+frm,-prp,+expl]]
sbjs_pn -> obj        <e:-e->   [ob=[-prp,-p1,-p2,-plr,+expl]];[ob=[-p1,+p2,-plr,+frm,-prp,+expl]]
#;[ob=[-expl],+def,+rel,+sub]
sbjs_pn -> obj        [:]      [ob=[-expl],-def];[ob=[+prp,+expl]];[ob=[+plr,-prp,+expl]];[ob=[+p2,-plr,-prp,-frm,+expl]];[ob=[-p2,-plr,-prp,+fem,+expl]]
# 2p: prf or ger
sbjs_p -> obj      <ac_hu:-Ac_hu(@pron,subj,$number=plur,person=2,*ኣችሁ,~nsubj)>  [sb=[+p2,-p1,+plr],ob=[-p2]]
# 3p
sbjs_p -> obj         <u:-u(@pron,subj,$number=plur,person=3,*ኡ,~nsubj)>   [tm=prf,sb=[-p1,-p2,+plr]]

# GERUNDIVE
# 1; geminate and palatalize previous consonant; don't show the palatalization character
sbjs_p -> obj         <_8E:-_E(@pron,subj,$number=sing,person=1,*ኤ,~nsubj)> [tm=ger,sb=[+p1,-p2,-plr],ob=[-p1]]
sbjs_p -> sbj_g1p     <en:-en(@pron,subj,$number=plur,person=1,*ኧን,~nsubj)>  [tm=ger,sb=[+p1,-p2,+plr],ob=[-p1]]
# 1p: infix for 2frm (handle later as prefix before -wo(t)?); 3sm
#sbj_g1p -> obj        <e:-e(infix)>   [ob=[-prp,-p1,+expl]];[ob=[-p1,+p2,-plr,+frm,-prp,+expl]]
sbj_g1p -> obj        <e:-e->   [ob=[-prp,-p1,+expl]];[ob=[-p1,+p2,-plr,+frm,-prp,+expl]]
sbj_g1p -> obj        [:]    [ob=[-expl],-def];[ob=[+expl,-p2,+fem,-plr,-prp]];[ob=[+plr,-prp,+expl]];[ob=[+expl,+p2,-frm,-prp]];[ob=[+expl,+prp]]
# 2s (plural same as perfective)
sbjs_p -> sbj_g2m     <eh:-eh(@pron,subj,$gender=masc,number=sing,person=2,*ኧህ,~nsubj)>  [tm=ger,sb=[+p2,-p1,-plr,-fem,-frm],ob=[-p2]]
# 2sm: infix for 1 objects, non-prep
sbj_g2m -> obj        <e:-e->   [ob=[-prp,+p1,+expl]]
#sbj_g2m -> obj        <e:-e(infix)>   [ob=[-prp,+p1,+expl]]
sbj_g2m -> obj        [:]    [ob=[-expl]];[ob=[-p2,+prp,+expl]];[ob=[-prp,-p1,-p2,+expl]]
sbjs_p -> obj         <ex:-ex(@pron,subj,$gender=fem,number=sing,person=2,*ኧሽ,~nsubj)>  [tm=ger,sb=[+p2,-p1,-plr,+fem,-frm],ob=[-p2]]
# 3
sbjs_p -> obj         <o:-o(@pron,subj,$gender=masc,number=sing,person=3,*ኦ,~nsubj)>   [tm=ger,sb=[-p2,-p1,-plr,-fem]]
sbjs_p -> obj         <a:-A(@pron,subj,$gender=fem,number=sing,person=3,*ኣ,~nsubj)>   [tm=ger,sb=[-p2,-p1,-plr,+fem]]
sbjs_p -> obj        <ew:-ew(@pron,subj,$number=plur,person=3,*ኧው,~nsubj)>  [tm=ger,sb=[-p2,-p1,+plr]]

### OBJECT SUFFIXES
# No object; not definite
obj -> negs_aux          [:]    [ob=[-expl]]
#obj -> negs_aux          [:]    [ob=[-expl],-def]
# 3sm suffix doubles as definite marker for relative clauses
#obj -> def3sm0           [:]    [ob=[-expl],+def,+rel,+sub]
# Explicit objects, also definite if relative
#obj -> obj0            [:]    [ob=[+expl],-def,-rel]
obj -> obj0            [:]    [ob=[+expl]]
# ;[ob=[+expl],+def,+rel]
# Prepositional
# Ambiguous: usually ben in TB, but sometimes loc
obj0 -> objs1       <b_:-b_(@adp,$case=mal,*ብ,~case)>  [ob=[+prp,+b,-l]]
# Ambiguous, but always ben in TB
obj0 -> objs1       <l_:-l_(@adp,$case=ben,*ል,~case)>  [ob=[+prp,+l,-b]]
# Non-prepositional
obj0 -> objs1          [:]    [ob=[-prp]]
# Pronouns
objs1  -> negs_aux     <N_:-N_(@pron,objc,$number=sing,person=1,*ኝ,~obj)>  [ob=[+p1,-p2,-plr,-prp]]
objs1  -> negs_aux     <h:-h(@pron,objc,$gender=masc,number=sing,person=2,*ህ,~obj)>   [ob=[-p1,+p2,-plr,-fem,-frm,-prp]]
objs1  -> negs_aux     <x:-x(@pron,objc,$gender=fem,number=sing,person=2,*ሽ,~obj)>   [ob=[-p1,+p2,-plr,+fem,-frm,-prp]]
objs1  -> negs_aux     <N_:-N_(@pron,objc,$number=sing,person=1,*ኝ,~expl)>  [ob=[+p1,-p2,-plr,+prp]]
objs1  -> negs_aux     <h:-h(@pron,objc,$gender=masc,number=sing,person=2,*ህ,~expl)>   [ob=[-p1,+p2,-plr,-fem,-frm,+prp]]
objs1  -> negs_aux     <x:-x(@pron,objc,$gender=fem,number=sing,person=2,*ሽ,~expl)>   [ob=[-p1,+p2,-plr,+fem,-frm,+prp]]
# lemma could also be ው (generic 3sm object)
objs1  -> negs_aux    <et:-et(@pron,objc,$gender=masc,number=sing,person=3,*ኧት,~expl)>     [ob=[-p1,-p2,-plr,-fem,+prp]]
# 3sm allomorphs: w, ew, t
objs1  ->  def3sm0    [:]        [ob=[-p1,-p2,-plr,-fem,-prp]]
objs1  -> negs_aux    <at:-At(@pron,objc,$gender=fem,number=sing,person=3,*ኣት,~obj)>   [ob=[-p1,-p2,-plr,+fem,-prp]]
objs1  -> negs_aux     <n:-n(@pron,objc,$number=plur,person=1,*ን,~obj)>    [ob=[+p1,-p2,+plr,-prp]]
objs1  -> negs_aux   <ac_hu:-Ac_hu(@pron,objc,$number=plur,person=2,*ኣችሁ,~obj)> [ob=[-p1,+p2,+plr,-frm,-prp]]
objs1  -> negs_aux   <ac_ew:-Ac_ew(@pron,objc,$number=plur,person=3,*ኣቸው,~obj)> [ob=[-p1,-p2,+plr,-prp]]
objs1  -> objs_2frm    <wo:-wo(@pron,objc,$person=2,polite=form,*ዎ,~obj)>  [ob=[-p1,+p2,-plr,+frm,-prp]]
objs1  -> negs_aux    <at:-At(@pron,objc,$gender=fem,number=sing,person=3,*ኣት,~expl)>   [ob=[-p1,-p2,-plr,+fem,+prp]]
objs1  -> negs_aux     <n:-n(@pron,objc,$number=plur,person=1,*ን,~expl)>    [ob=[+p1,-p2,+plr,+prp]]
objs1  -> negs_aux   <ac_hu:-Ac_hu(@pron,objc,$number=plur,person=2,*ኣችሁ,~expl)> [ob=[-p1,+p2,+plr,-frm,+prp]]
objs1  -> negs_aux   <ac_ew:-Ac_ew(@pron,objc,$number=plur,person=3,*ኣቸው,~expl)> [ob=[-p1,-p2,+plr,+prp]]
objs1  -> objs_2frm    <wo:-wo(@pron,objc,$person=2,polite=form,*ዎ,~expl)>  [ob=[-p1,+p2,-plr,+frm,+prp]]
objs_2frm -> negs_aux  [:;t:]
## def, 3sm_obj
# 3sm and 1s subjects
def3sm0 -> def3sm_3sm    [:]     [sb=[-p1,-p2,-fem,-plr]]
def3sm0 -> def3sm_1s     [:]     [sb=[+p1,-p2,-plr]]
def3sm_3sm -> def3sm_w   [:]     [tm=prf];[tm=imf];[tm=j_i]
def3sm_3sm -> def3sm_t   [:]     [tm=ger]
def3sm_1s -> def3sm_w    [:]     [tm=imf];[tm=j_i];[tm=ger]
def3sm_1s -> def3sm_t    [:]     [tm=prf]
# other subjects
def3sm0 -> def3sm_w      [:]     [sb=[+p2,-p1,-plr]];[sb=[-p1,-p2,+fem,-plr]];[sb=[+p1,-p2,+plr]]
def3sm0 -> def3sm_t      [:]     [sb=[+p2,-p1,+plr]];[sb=[-p1,-p2,+plr]]
def3sm_w -> negs_aux    <3:-w(@pron,objc,$gender=masc,number=sing,person=3,*ው,~obj)>
def3sm_t -> negs_aux    <3:-t(@pron,objc,$gender=masc,number=sing,person=3,*ው,~obj)>

# AUX; can't cooccur with +neg or +sub
# % maybe the lemma should really be ኣለ
negs_aux -> aux1  <al:-Al(@aux,*ኣል,~aux)>   [tm=imf,-sub,-neg,ax=al];[tm=ger,ax=al]
# ysebral, ysebrutal, sebrehal, sebrexal, sebrenal, sebracchWal, sebrewal
aux1  -> cj2      [:]        [sb=[-p1,-p2,-fem,-plr]];[sb=[-p1,-p2,+plr],ob=[+expl]];[tm=ger,sb=[+plr]];[tm=ger,sb=[+p2]]
# dropping the initial -e in the lemma for 1s,2sm,2sf,1p
aux1  -> cj2      <_ehu:-ehu(@pron,subjc,$number=sing,person=1,*ሁ,~nsubj)>     [sb=[+p1,-p2,-plr]]
aux1  -> cj2      <_eh:-eh(@pron,subjc,$gender=masc,number=sing,person=2,*ህ,~nsubj)>      [tm=imf,sb=[+p2,-p1,-plr,-fem,-frm]]
aux1  -> cj2      <_ex:-ex(@pron,subjc,$gender=fem,number=sing,person=2,*ሽ,~nsubj)>      [tm=imf,sb=[+p2,-p1,-plr,+fem,-frm]]
aux1  -> cj2      <_ec_:-ec(@pron,subjc,$gender=fem,number=sing,person=3,*ኧች,~nsubj)>     [sb=[-p2,-p1,-plr,+fem]]
aux1  -> cj2      <_en:-en(@pron,subjc,$number=plur,person=1,*ን,~nsubj)>      [tm=imf,sb=[+p1,-p2,+plr]]
aux1  -> cj2      <_ac_hu:-Achu(@pron,subjc,$number=plur,person=2,*ኣችሁ,~nsubj)>   [tm=imf,sb=[-p1,+p2,+plr]]
aux1  -> cj2      <_u:-u(@pron,subjc,$number=plur,person=3,*ኡ,~nsubj)>       [tm=imf,sb=[-p1,-p2,+plr],ob=[-expl]]
negs_aux -> noaux  [:]       [ax=None]

# NEGATIVE
# % @ncm and 'discourse' are from the TB; no features in TB (except in a few cases)
noaux -> cj2  <Im:-m(@part,ncm,$polarity=neg,*ም,~discourse)>         [+neg,-sub,tm=prf];[+neg,-sub,tm=imf];[+neg,-sub,tm=prs]
# ACCUSATIVE
# % no features in TB
noaux -> cj2  <In:-n(@part,acc,*ን,~case)>        [+rel,+acc,pp=None]
# No negs_aux: juss_imp; imprf, prs, or prf: -neg,-ax,-acc; +neg,-ax,+sub,-acc
noaux -> cj2  [:]            [tm=j_i]; [tm=ger]; [tm=imf,-neg,-acc]; [tm=imf,+neg,+sub,-acc]; [tm=prs,-neg,-acc]; [tm=prs,+neg,+sub,-acc]; [tm=prf,-neg,-acc]; [tm=prf,+neg,+sub,-acc]

## CONJUNCTIVE SUFFIXES
cj2 -> end     >>cnj2X<<
cj2 -> end  [:]               [cj2=None]

end ->
