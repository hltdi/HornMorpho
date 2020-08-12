-> start

## PREPOSITIONS
# no prepositions
start -> stem    [:]        [pp=None,-gen,rl=[-p,-gen],-dis]  #% stem
start -> stem   >>n_prep<<                                    #% stem
start -> stem    <ye:>      [+gen,pp=None,rl=[-p,+gen],-dis]  #% stem

#% DISTRIBUTIVE
#% distrib -> stem     [:]        [-dis]
#%distrib -> stem     <'y_e:>    [+dis,+def]

## STEM
#% Irregular prepositional forms: Izzih, Izziya, etc.; can't be distributive
#% stem -> acc      +prep_n+      [-plr,v=None,-dis,-p1,-p2,poss=[-expl],+def,-itu,-prp]
#% Personal pronouns: plurality specified, no possessor, not distributive
#% stem -> acc      +ppron+       [v=None,poss=[-expl],-dis,+def,-itu,-prp]
#% Non-deverbal common nouns
#% stem -> der      +n_stem+      [v=None,-prp]
#% stem -> plr_oc   +n_stem+      [v=None,-prp]
#% Place names; not necessarily -prp
#% stem ->  place   +n_place+     [v=None]
#% place -> plr_an   <awi:>       [der=[+ass],-prp]
#% place -> acc      [:]          [+def,+prp,-itu,poss=[-expl]]
#% Proper nouns (possessive is possible); always 3rd person singular
#% stem -> poss     +n_name+      [v=None,-p1,-p2,+def,+prp,-plr,-itu]
#% stem -> plr_an   +n_stem_an+   [v=None,-prp]
# Deverbal nouns: v=agt | ins | man | inf
stem -> plr_oc    >>vnoun<<    [-p1,-p2,-prp]
stem -> plr_oc   +irr_vnoun+   [-p1,-p2,-prp]
#% Irregular plurals
#% stem -> poss     +irr_plr+     [v=None,-prp]
#% Irregular nouns (only sewy_ew?)
#% stem -> acc      +irr_n+       [v=None,poss=[-expl],-prp]

## PLURAL
#% plr_an -> poss    <an:>    [+plr]

plr_oc -> poss    <oc_:>   [+plr,v=ins];[+plr,v=agt];[+plr,v=man]
#% plr_an -> poss     [:]     [-plr]
plr_oc -> poss     [:]     [-plr]

## POSSESSIVE, DEFINITE
# Noun could be +def without a suffix
poss -> acc       [:]      [poss=[-expl],-def,-prp,-itu];[poss=[-expl],+def,+prp,-itu]
poss -> acc       [E:]     [+def,poss=[+p1,-p2,-plr,+expl],-itu]
poss -> acc       [h:]     [+def,poss=[-p1,+p2,-plr,-fem,+expl],-itu]
poss -> acc       [x:]     [+def,poss=[-p1,+p2,-plr,+fem,+expl],-itu]
poss -> acc       [u:]     [+def,poss=[-p1,-p2,-plr,-fem,+expl],-itu];[+def,-prp,poss=[-expl],-fem,-itu]
poss -> acc      <itu:>    [+def,poss=[-expl],+fem,-plr,+itu,-prp]
#% Only the agent can be feminine
poss -> acc      <wa:>     [+def,poss=[-p1,-p2,-plr,+fem,+expl],-itu];[+def,-prp,poss=[-expl],+fem,-plr,-itu,v=agt]
poss -> acc     <ac_n:>    [+def,poss=[+p1,-p2,+plr,+expl],-itu]
poss -> acc     <ac_hu:>   [+def,poss=[-p1,+p2,+plr,+expl],-itu]
poss -> acc     <ac_ew:>   [+def,poss=[-p1,-p2,+plr,+expl],-itu]
poss -> acc    <wo(t):>    [+def,poss=[-p1,+p2,-plr,+frm,+expl],-itu]

## ACCUSATIVE
acc -> cnj        [:]      [-acc,rl=[-acc]]
acc -> cnj        [n:]     [+acc,pp=None,rl=[-p,+acc]]

## CONJUNCTIVE SUFFIXES
cnj -> end        [:]      [cnj=None,pos=n]
cnj -> end        [m:]     [cnj=m,pos=n]
cnj -> end        <s_:>    [cnj=s,pos=n]
cnj -> end        <n_a:>   [cnj=na,pos=n]

end ->
