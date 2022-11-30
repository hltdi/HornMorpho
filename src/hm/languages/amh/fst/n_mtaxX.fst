## Segmentation morphotactics for Amharic nouns.
-> start

## PREPOSITIONS
# no prepositions
start -> distrib    [:]              [prep=None,-gen]
start -> distrib   >>n_prepX<<
# % the TB has features for የ
#start -> distrib    <ye:ye(@adp,$case=gen,*የ,~case)->    [+gen,prep=None]
# special irregular form
#start -> cnj  <'ndih:'nd(@adp,$case=equ,*እንደ,~case) -{ih++yh}(*ይህ)> [prep=Inde,v=None,pos=n,-plr,-dis,-p1,-p2,poss=[-expl],-itu,-acc]

## DISTRIBUTIVE
distrib -> prestem     [:]              [-dis]
# % Not handled consistently in the TB
distrib -> prestem     <'y_e:'ye(@det,$numtype=dist,*እየ,~det)->     [+dis,+def,v=None]

## NEGATIVE (y)ale
prestem -> stem        [:]             [-neg]
prestem -> stem      <ale:ale(@part,$polarity=neg,*ኣለ,~advmod)->   [+neg]
# preposition not possible before yale?; use the same lemma?
prestem -> stem      <yale:yale(@part,$polarity=neg,*ኣለ,~advmod)-> [+neg,prep=None]

## STEM
# Mark off stem
stem -> stem0     [:{]
# Irregular prepositional forms: Izzih, Izziya, etc.; can't be distributive
stem0 -> acc0      +prep_n+      [-plr,v=None,-dis,-p1,-p2,poss=[-expl],+def,-itu,-prp]
# Personal pronouns: plurality specified, no possessor, not distributive
stem0 -> poss0      +ppron+       [v=None,poss=[-expl],-dis,+def,-itu,-prp]
acc0 -> acc       [:}]
poss0 -> poss     [:}]

## Non-deverbal common nouns, single words
stem0 -> plr_oc0   +n_stem1X+      [v=None,-prp]
#plr_oc0 -> plr_oc       [:}]
plr_oc0 -> plr_oc       [:]
## Place names; not necessarily -prp
stem0 ->  place0   +n_place1X+     [v=None]
place0 -> acc       [:}]        [+def,+prp,-itu,poss=[-expl]]
## Proper nouns (possessive is possible); always 3rd person singular
stem0 -> name0     +n_name+      [v=None,-p1,-p2,+def,+prp,-plr,-itu]
name0 -> acc       [:}]
stem0 -> plr_an0   +n_stem_an+   [v=None,-prp]
plr_an0 -> plr_an   [:]

## Deverbal nouns: v=agt | ins | man | inf
stem0 -> vnoun    >>vnoun+<<      [pos=n_dv,-p1,-p2,-prp]
stem0 -> vnoun_pos   +irr_vnounX+   [pos=n_dv,-p1,-p2,-prp]
vnoun -> vnoun_pos  >>tmp_n<<
# Ins, agt, and man don't need to have verbal XPOS
#vnoun_pos -> plr_oc0   [:]        [v=ins|agt|man]
# Set XPOS for infinitives, which can't be plural
vnoun_pos -> inf          [:}(inf]  [v=inf,-plr]
inf -> poss  >>inf_featsX<<
# Constrain features for other deverbal nouns (no verbal XPOS)
vnoun_pos -> agt_man_ins   [:]   [v=agt|ins|man]
agt_man_ins -> plr_oc0   >>ami_featsX<<

## Irregular plurals
stem0 -> plr_irr0  +irr_plrX+   [v=None,-prp]
stem0 -> plr_at0  +plr_at+      [v=None,-prp]
plr_at0 -> plr_at       [:]
# Irregular -oc plurals
stem0 -> plr_oc10  +plr_oc+      [v=None,-prp]
plr_oc10 -> plr_oc1       [:]
## Irregular definite (only sewy_ew?)
stem0 -> stemdef   +irr_n+        [v=None,poss=[-expl],-prp]
#stemdef -> acc    <:}-u(@det,$definite=def)>
stemdef -> acc    <:}-u(@det,*ኡ,~det)>

## PLURAL
plr_an -> poss    <an:@n}($number=plur)>    [+plr]
#% Infinitives can't be plural
#plr_oc -> poss    <oc_:-oc($number=plur)>   [+plr,v=None];[+plr,v=ins];[+plr,v=agt];[+plr,v=man]
plr_oc -> poss    <oc_:Oc}($number=plur)>   [+plr,v=None];[+plr,v=ins];[+plr,v=agt];[+plr,v=man]
# * here represents no clear suffix marking plural
#plr_irr0 -> poss    <:}-*($number=plur)>  []
plr_irr0 -> poss    <:}($number=plur)>  []
plr_at -> poss       <:at}($number=plur)>   []
plr_oc1 -> poss     <:Oc}($number=plur)>   []
plr_an -> poss     [:]           [-plr]
plr_oc -> poss     [:}]           [-plr]

## POSSESSIVE, DEFINITE
# Actually noun could be +def without a suffix
poss -> acc       [:]      [poss=[-expl],-prp,-itu,-def];[poss=[-expl],+def,pos=pron,-itu,v=None]
poss -> acc       <E:-E(@pron,posm,$number=sing,person=1,poss=yes,*ኤ,~nmod)>     [+def,poss=[+p1,-p2,-plr,+expl],-itu]
poss -> acc       <h:-h(@pron,posm,$gender=masc,number=sing,person=2,poss=yes,*ህ,~nmod)>     [+def,poss=[-p1,+p2,-plr,-fem,+expl],-itu]
poss -> acc       <x:-x(@pron,posm,$gender=fem,number=sing,person=2,poss=yes,*ሽ,~nmod)>     [+def,poss=[-p1,+p2,-plr,+fem,+expl],-itu]
# Combine the two interpretations of -u and -wa??
#poss -> acc       <u:-u(@det,$definite=def)>          [+def,poss=[-expl],-itu,-fem]
poss -> acc       <u:-u(@det,*ኡ,~det)>          [+def,poss=[-expl],-itu,-fem]
poss -> acc       <u:-u(@pron,posm,$gender=masc,number=sing,person=3,poss=yes,*ኡ,~nmod)>     [+def,poss=[-p1,-p2,-plr,-fem,+expl],-itu]
#poss -> acc      <itu:-itu(@det,$definite=def,gender=fem)>    [+def,poss=[-expl],+fem,-plr,+itu,-prp]
poss -> acc      <itu:-itu(@det,$gender=fem,*ኢቱ,~det)>    [+def,poss=[-expl],+fem,-plr,+itu,-prp]
# the only deverbal nouns that can be feminine are agents
#poss -> acc      <wa:-wa(@det,$definite=def,gender=fem)>    [+def,-prp,poss=[-expl],+fem,-plr,-itu,v=None];[+def,-prp,poss=[-expl],+fem,-plr,-itu,v=agt]
poss -> acc      <wa:-wa(@det,$gender=fem,*ዋ,~det)>    [+def,-prp,poss=[-expl],+fem,-plr,-itu,v=None];[+def,-prp,poss=[-expl],+fem,-plr,-itu,v=agt]
poss -> acc      <wa:-wa(@pron,posm,$gender=fem,number=sing,person=3,poss=yes,*ዋ,~nmod)>   [+def,-prp,poss=[-p1,-p2,-plr,+fem,+expl],-itu]
poss -> acc     <ac_n:-Ac_n(@pron,posm,$number=plur,person=1,poss=yes,*ኣችን,~nmod)>    [+def,poss=[+p1,-p2,+plr,+expl],-itu]
poss -> acc     <ac_hu:-Ac_hu(@pron,posm,$number=plur,person=2,poss=yes,*ኣችሁ,~nmod)>   [+def,poss=[-p1,+p2,+plr,+expl],-itu]
poss -> acc     <ac_ew:-Ac_ew(@pron,posm,$number=plur,person=3,poss=yes,*ኣቸው,~nmod)>   [+def,poss=[-p1,-p2,+plr,+expl],-itu]
poss -> acc     <wo:-wo(@pron,posm,$number=sing,person=2,polite=form,poss=yes,*ዎ,~nmod)>    [+def,poss=[-p1,+p2,-plr,+frm,+expl],-itu]

## ACCUSATIVE
acc -> cnj        [:]      [-acc]
# % not sure why the TB allots a special XPOS to accusative; they also include no features
acc -> cnj        <n:-n(@part,acc,$case=acc,*ን,~case)>     [+acc,prep=None]

## CONJUNCTIVE SUFFIXES
cnj -> end        [:]      [cnj=None]
cnj -> end        <m:-m(@cconj,*ም,~cc)>     [cnj=m]
cnj -> end        <s_:-s(@cconj,*ስ,~cc)>    [cnj=s]
cnj -> end        <n_a:-n_a(@cconj,*ና,~cc)>   [cnj=na]

end ->
