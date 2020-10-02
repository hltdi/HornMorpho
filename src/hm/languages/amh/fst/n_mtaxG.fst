-> start

## PREPOSITIONS
start -> distrib    [:]        [prep=None,-gen]
start -> distrib   >>n_prep<<
start -> distrib    <ye:>      [+gen,prep=None]

## DISTRIBUTIVE
distrib -> stem     [:]        [-dis]
distrib -> stem     <'y_e:>    [+dis,+def]

## STEM
# Irregular prepositional forms: Izzih, Izziya, etc.
stem -> poss     +prep_n+      [-plr,v=None,-dis,-p1,-p2,poss=[-expl],+def,-itu,-prp]
# Personal pronouns: plurality specified, no possessor, not distributive
stem -> acc      +ppronG+      [v=None,poss=[-expl],-dis,+def,-itu,-prp]
# People's names: for generation skip the possibility of proper nouns with possessives
stem -> acc      +n_name+     [v=None,-p1,-p2,+def,+prp,poss=[-expl],-itu]
# Place names; not necessarily +prp because they can take -awi
stem ->  place   +n_place+    [v=None]
# place -> plr_an   <awi:>       [der=[+ass],-prp]
place -> acc      [:]          [+def,+prp,-itu,poss=[-expl]]
# Non-deverbal common nouns: v=None
stem -> plr_oc    +n_stem+     [v=None,-prp]
stem -> plr_an    +n_stem_an+  [v=None,-prp]
# Deverbal nouns: v=agt | ins | man | inf
stem -> plr_oc    >>vnounG<<   [-p1,-p2,-prp]
stem -> plr_oc   +irr_vnoun+   [-p1,-p2,-prp]
stem -> poss     +irr_plr+     [v=None,-prp]

## PLURAL
plr_an -> poss    <an:>    [+plr]
plr_oc -> poss    <oc_:>   [+plr,v=None];[+plr,v=ins];[+plr,v=agt];[+plr,v=man]
plr_an -> poss     [:]     [-plr]
plr_oc -> poss     [:]     [-plr]

## POSSESSIVE, DEFINITE
# Noun could be +def without a suffix; don't bother to generate proper nouns
# with possessives
poss -> acc       [:]      [poss=[-expl],-def,-prp,-itu];[poss=[-expl],+def,+prp,-itu]
poss -> acc       [E:]     [+def,poss=[+p1,-p2,-plr,+expl]]
poss -> acc       [h:]     [+def,poss=[-p1,+p2,-plr,-fem,+expl]]
poss -> acc       [x:]     [+def,poss=[-p1,+p2,-plr,+fem,+expl]]
poss -> acc       [u:]     [+def,poss=[-p1,-p2,-plr,-fem,+expl]];[+def,-prp,poss=[-expl],-fem]
# Leave out this option for generation
# poss -> acc      <itu:>    [poss=[-expl],+fem,+def]
poss -> acc      <wa:>     [+def,poss=[-p1,-p2,-plr,+fem,+expl],-itu];[+def,-prp,poss=[-expl],+fem,-plr,-itu,v=None];[+def,-prp,poss=[-expl],+fem,-plr,-itu,v=agt]
poss -> acc     <ac_n:>    [+def,poss=[+p1,-p2,+plr,+expl]]
poss -> acc     <ac_hu:>   [+def,poss=[-p1,+p2,+plr,+expl]]
poss -> acc     <ac_ew:>   [+def,poss=[-p1,-p2,+plr,+expl]]
poss -> acc       <wo:>    [+def,poss=[-p1,+p2,-plr,+frm,+expl]]

## ACCUSATIVE
acc -> cnj        [:]      [-acc]
acc -> cnj        [n:]     [+acc,prep=None]

## CONJUNCTIVE SUFFIXES
cnj -> end        [:]      [cnj=None]
cnj -> end        [m:]     [cnj=m]
cnj -> end        <s_:>    [cnj=s]
cnj -> end        <n_a:>   [cnj=na]

end ->
