-> start

## PREPOSITIONS
start -> distrib    [:]        [pp=None,-gen,rl=[-p,-gen]]
start -> distrib   >>n_prep<<
start -> pp_stem   >>n_prep<<
start -> distrib    <ye:>      [+gen,pp=None,rl=[-p,+gen]]
start -> pp_stem    <ye:>      [+gen,pp=None,rl=[-p,+gen]]

## DISTRIBUTIVE
distrib -> stem     [:]        [-dis]
distrib -> stem     <'y_e:>    [+dis,+def]

## STEM
# Irregular prepositional forms: Izzih, Izziya, etc.
pp_stem -> poss  +prep_n+      [-plr,v=None,+def,-prp]
# Non-deverbal nouns: v=None
stem -> plr_oc    +n_stemG+     [v=None,-prp]
# Place names; not necessarily +prp because they can take -awi
stem ->  place   +n_placeG+     [v=None]
# place -> plr_an   <awi:>       [der=[+ass],-prp]
place -> acc      [:]          [+def,+prp,-itu,poss=[-expl]]
# People's names
stem -> acc      +n_nameG+     [v=None,+def,+prp,-p1,-p2,-plr,poss=[-expl],-itu]
stem -> plr_an    +n_stem_an+  [v=None,-prp]
# Deverbal nouns: v=agt | ins | man | inf
stem -> plr_oc    >>vnounG<<   [-prp]
stem -> plr_oc   +irr_vnoun+   [-prp]
stem -> poss     +irr_plr+     [v=None,-prp]

## PLURAL
plr_an -> poss    <an:>    [+plr]
plr_oc -> poss    <oc_:>   [+plr,v=None];[+plr,v=ins];[+plr,v=agt];[+plr,v=man]
plr_an -> poss     [:]     [-plr]
plr_oc -> poss     [:]     [-plr]

## POSSESSIVE, DEFINITE
# Noun could be +def without a suffix
poss -> acc       [:]      [poss=[-expl],-def,-prp];[poss=[-expl],+def,+prp]
poss -> acc       [E:]     [+def,poss=[+p1,-p2,-plr,+expl]]
poss -> acc       [h:]     [+def,poss=[-p1,+p2,-plr,-fem,+expl]]
poss -> acc       [x:]     [+def,poss=[-p1,+p2,-plr,+fem,+expl]]
poss -> acc       [u:]     [+def,poss=[-p1,-p2,-plr,-fem,+expl]];[+def,poss=[-expl],-fem,-prp]
# Leave out this option for generation
poss -> acc      <itu:>    [+def,poss=[-expl],+fem,+itu,-prp]
poss -> acc      <wa:>     [+def,poss=[-p1,-p2,-plr,+fem,+expl],-itu];[+def,-prp,poss=[-expl],+fem,-plr,-itu,v=None];[+def,-prp,poss=[-expl],+fem,-plr,-itu,v=agt]
poss -> acc     <ac_n:>    [+def,poss=[+p1,-p2,+plr,+expl]]
poss -> acc     <ac_hu:>   [+def,poss=[-p1,+p2,+plr,+expl]]
poss -> acc     <ac_ew:>   [+def,poss=[-p1,-p2,+plr,+expl]]
poss -> acc       <wo:>    [+def,poss=[-p1,+p2,-plr,+frm,+expl]]

## ACCUSATIVE
acc -> cnj        [:]      [-acc,rl=[-acc]]
acc -> cnj        [n:]     [+acc,pp=None,rl=[-p,+acc]]

## CONJUNCTIVE SUFFIXES
cnj -> end        [:]      [cnj=None,pos=n]
cnj -> end        [m:]     [cnj=m,pos=n]
cnj -> end        <s_:>    [cnj=s,pos=n]
cnj -> end        <n_a:>   [cnj=na,pos=n]

end ->
