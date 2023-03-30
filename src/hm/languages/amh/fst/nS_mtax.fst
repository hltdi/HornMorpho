-> start

## PREPOSITIONS
# no prepositions
start -> distrib    [:]        [prep=None,-gen]
start -> distrib   >>n_prep<<
start -> distrib    <ye:>      [+gen,prep=None]

## DISTRIBUTIVE 'y_e
distrib -> stem     [:]        [-dis]
# Deverbal nouns can't be distributive
distrib -> stem     <'y_e:>    [+dis,+def,v=None]

## STEM
# Irregular prepositional forms: Izzih, Izziya, etc.; can't be distributive
stem -> acc      +prep_n+      [-plr,v=None,-dis,-p1,-p2,poss=[-expl],+def,-itu,-prp]
# Personal pronouns: plurality specified, no possessor, not distributive
stem -> poss      +ppronS+       [v=None,poss=[-expl],-dis,+def,-itu,-prp]
# Non-deverbal common nouns
stem -> plr_oc   +nS_stem+      [v=None,-prp]
# Place names; not necessarily -prp
#stem ->  place   +n_place+     [v=None]
#place -> acc      [:]          [+def,+prp,-itu,poss=[-expl]]
# Proper nouns (possessive is possible); always 3rd person singular
#stem -> poss     +n_name+      [v=None,-p1,-p2,+def,+prp,-plr,-itu]
stem -> plr_an   +n_stem_an+   [v=None,-prp]

# Deverbal nouns: v=agt | ins | man | inf
stem -> plr_oc     >>vnoun<<   [-p1,-p2,-prp,pos=v]
stem -> plr_oc   +irr_vnoun+   [-p1,-p2,-prp,pos=v]

# Irregular plurals
stem -> poss     +irr_plr+     [v=None,-prp,pos=n]
# Irregular nouns (only sewy_ew?)
stem -> acc      +irr_n+       [v=None,poss=[-expl],-prp]

## PLURAL
plr_an -> poss    <an:>    [+plr]
#% Infinitives can't be plural
plr_oc -> poss    <oc_:>   [+plr,v=None];[+plr,v=ins];[+plr,v=agt];[+plr,v=man]
plr_an -> poss     [:]     [-plr]
plr_oc -> poss     [:]     [-plr]

## POSSESSIVE, DEFINITE
# Noun could be +def without a suffix
poss -> acc       [:]      [poss=[-expl],-def,-prp,-itu];[poss=[-expl],+def,+prp,-itu]
poss -> acc       [E:]     [+def,poss=[+p1,-p2,-plr,+expl],-itu]
poss -> acc       [h:]     [+def,poss=[-p1,+p2,-plr,-fem,+expl],-itu]
poss -> acc       [x:]     [+def,poss=[-p1,+p2,-plr,+fem,+expl],-itu]
poss -> acc       [u:]     [+def,poss=[-p1,-p2,-plr,-fem,+expl],-itu];[+def,-fem,-prp,poss=[-expl],-itu]
poss -> acc      <itu:>    [+def,poss=[-expl],+fem,-plr,+itu,-prp]
#% the only deverbal nouns that can be feminine are agents
poss -> acc      <wa:>     [+def,poss=[-p1,-p2,-plr,+fem,+expl],-itu];[+def,-prp,poss=[-expl],+fem,-plr,-itu,v=None];[+def,-prp,poss=[-expl],+fem,-plr,-itu,v=agt]
poss -> acc     <ac_n:>    [+def,poss=[+p1,-p2,+plr,+expl],-itu]
poss -> acc     <ac_hu:>   [+def,poss=[-p1,+p2,+plr,+expl],-itu]
poss -> acc     <ac_ew:>   [+def,poss=[-p1,-p2,+plr,+expl],-itu]
poss -> acc     <wo:>      [+def,poss=[-p1,+p2,-plr,+frm,+expl],-itu]

## ACCUSATIVE
acc -> cnj        [:]      [-acc]
acc -> cnj        [n:]     [+acc,prep=None]

## CONJUNCTIVE SUFFIXES
cnj -> end        [:]      [cnj=None]
cnj -> end        [m:]     [cnj=m]
cnj -> end        <s_:>    [cnj=s]
cnj -> end        <n_a:>   [cnj=na]

end ->
