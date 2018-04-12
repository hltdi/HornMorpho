## Segmentation morphotactics for Amharic nouns.
-> start

## PREPOSITIONS
# no prepositions
start -> distrib    [:]              [pp=None,-gen,rl=[-p,-gen]]
start -> distrib   >>n_prep+<<
start -> distrib    <ye:ye(gen)->    [+gen,pp=None,rl=[-p,+gen]]

## DISTRIBUTIVE
distrib -> stem     [:]              [-dis]
#% Deverbal nouns can't be distributive
distrib -> stem     <'y_e:'ye(distrib)->          [+dis,+def,v=None]

## STEM
# Mark off stem
stem -> stem0     [:{]
# Irregular prepositional forms: Izzih, Izziya, etc.; can't be distributive
stem0 -> acc0      +prep_n+      [-plr,v=None,-dis,-p1,-p2,poss=[-expl],+def,-itu,-prp]
# Personal pronouns: plurality specified, no possessor, not distributive
stem0 -> acc0      +ppron+       [v=None,poss=[-expl],-dis,+def,-itu,-prp]
acc0 -> acc       [:}]

# Non-deverbal common nouns
stem0 -> plr_oc0   +n_stem+      [v=None,-prp]
plr_oc0 -> plr_oc       [:}]
# Place names; not necessarily -prp
stem0 ->  place0   +n_place+     [v=None]
place0 -> acc       [:}]        [+def,+prp,-itu,poss=[-expl]]
# Proper nouns (possessive is possible); always 3rd person singular
stem0 -> name0     +n_name+      [v=None,-p1,-p2,+def,+prp,-plr,-itu]
name0 -> acc       [:}]
stem0 -> plr_an0   +n_stem_an+   [v=None,-prp]
plr_an0 -> plr_an   [:}]         
# Deverbal nouns: v=agt | ins | man | inf
stem0 -> plr_oc0    >>vnoun<<    [-p1,-p2,-prp,pos=n_dv]
stem0 -> plr_oc0   +irr_vnoun+   [-p1,-p2,-prp,pos=n_dv]
# Irregular plurals
stem0 -> plr_irr0  +irr_plrS+   [v=None,-prp]
plr_irr0 -> plr_irr       [:}-(plr)]
stem0 -> plr_at0  +plr_at+      [v=None,-prp]
plr_at0 -> plr_at       [:}]
# Irregular -oc plurals
stem0 -> plr_oc10  +plr_oc+      [v=None,-prp]
plr_oc10 -> plr_oc1       [:}]
# Irregular definite (only sewy_ew?)
stem0 -> stemdef   +irr_n+        [v=None,poss=[-expl],-prp]
stemdef -> acc    <:}-u(def)>

## PLURAL
plr_an -> poss    <an:-an(plr)>    [+plr]
#% Infinitives can't be plural
plr_oc -> poss    <oc_:-oc(plr)>   [+plr,v=None];[+plr,v=ins];[+plr,v=agt];[+plr,v=man]
plr_irr -> poss    <:-X(plr)>    []
plr_at -> poss     <:-at(plr)>   []
plr_oc1 -> poss    <:-oc(plr)>   []
plr_an -> poss     [:]           [-plr]
plr_oc -> poss     [:]           [-plr]

## POSSESSIVE, DEFINITE
# Actually noun could be +def without a suffix
poss -> acc       [:]      [poss=[-expl],-prp,-itu,-def]
poss -> acc       <E:-E(poss=1s)>     [+def,poss=[+p1,-p2,-plr,+expl],-itu]
poss -> acc       <h:-h(poss=2sm)>     [+def,poss=[-p1,+p2,-plr,-fem,+expl],-itu]
poss -> acc       <x:-x(poss=2sf)>     [+def,poss=[-p1,+p2,-plr,+fem,+expl],-itu]
poss -> acc       <u:-u(def,mas/poss=3sm)>     [+def,-fem,-itu]
poss -> acc      <itu:-itu(def,fem)>    [+def,poss=[-expl],+fem,-plr,+itu,-prp]
#% the only deverbal nouns that can be feminine are agents
poss -> acc      <wa:-wa(def,fem/poss=3sf)>   [+def,-prp,poss=[-expl],+fem,-plr,-itu,v=None]
poss -> acc     <ac_n:-ac_n(poss=1p)>    [+def,poss=[+p1,-p2,+plr,+expl],-itu]
poss -> acc     <ac_hu:-ac_hu(poss=2p)>   [+def,poss=[-p1,+p2,+plr,+expl],-itu]
poss -> acc     <ac_ew:-ac_ew(poss=3p)>   [+def,poss=[-p1,-p2,+plr,+expl],-itu]
poss -> acc    <wo(t):-wo(poss=2F)>    [+def,poss=[-p1,+p2,-plr,+frm,+expl],-itu]

## ACCUSATIVE
acc -> cnj        [:]      [-acc,rl=[-acc]]
acc -> cnj        <n:-n(acc)>     [+acc,pp=None,rl=[-p,+acc]]

## CONJUNCTIVE SUFFIXES
cnj -> end        [:]      [cnj=None]
cnj -> end        <m:-m(cnj)>     [cnj=m]
cnj -> end        <s_:-s(cnj)>    [cnj=s]
cnj -> end        <n_a:-n_a(cnj)>   [cnj=na]

end ->
