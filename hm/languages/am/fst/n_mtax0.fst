-> start

## PREPOSITIONS
start -> stem_bound    [:]      [-dis,pp=None,-gen,rl=[-p,-gen]]
# The glottal stop appears only when its word-initial
start -> stem_bound  <'y_e:>    [+dis,+def,pp=None,-gen,rl=[-p,-gen]]
start -> distrib     >>n_prep<<
start -> distrib     <ye:>      [+gen,pp=None,rl=[-p,+gen]]

## DISTRIBUTIVE
distrib -> stem_bound  [:]      [-dis]
# No initial glottal stop following other prefix
distrib -> stem_bound  <y_e:>   [+dis,+def]

## BOUNDARY BETWEEN PREFIXES AND STEM
stem_bound -> stem     [$:]

## STEM
# Verbal nouns
stem -> plr_oc     >>vnoun0<<   
# Other nouns
stem -> stemC1       [X/L]      [v=None]
stem -> stemL1       [L]        [v=None]
stemC1 -> stemV1     [VV]
stemC1 -> stemC      [X/L]
stemC1 -> stemL      [L]
stemL1 -> stemV1     [VV]
stemL1 -> stemC      [X/L]
stemV1 -> stemC      [X/L]
stemV1 -> stemL      [L]

stemC -> stemV       [VV]
stemC -> stemC       [X/L]
stemC -> stemL       [L]
stemL -> stemV       [VV]
stemL -> stemC       [X/L]
stemV -> stemC       [X/L]
stemV -> stemL       [L]
stemV -> plr_oc      [:]
stemC -> plr_oc      [:]

## PLURAL
plr_an -> poss    <an:>    [+plr]
plr_oc -> poss    <oc_:>   [+plr,v=None];[+plr,v=ins];[+plr,v=agt];[+plr,v=man]
plr_an -> poss     [:]     [-plr]
plr_oc -> poss     [:]     [-plr]

## POSSESSIVE, DEFINITE
# Noun could be +def without a suffix
poss -> acc       [:]      [poss=[-expl],-def]
poss -> acc       [E:]     [+def,poss=[+p1,-p2,-plr,+expl]]
poss -> acc       [h:]     [+def,poss=[-p1,+p2,-plr,-fem,+expl]]
poss -> acc       [x:]     [+def,poss=[-p1,+p2,-plr,+fem,+expl]]
poss -> acc       [u:]     [+def,poss=[-p1,-p2,-plr,-fem,+expl]];[+def,poss=[-expl],-fem]
poss -> acc      <itu:>    [poss=[-expl],+fem,+def,-plr]
poss -> acc      <wa:>     [+def,poss=[-p1,-p2,-plr,+fem,+expl],-itu];[+def,-prp,poss=[-expl],+fem,-plr,-itu,v=None];[+def,-prp,poss=[-expl],+fem,-plr,-itu,v=agt]
poss -> acc     <ac_n:>    [+def,poss=[+p1,-p2,+plr,+expl]]
poss -> acc     <ac_hu:>   [+def,poss=[-p1,+p2,+plr,+expl]]
poss -> acc     <ac_ew:>   [+def,poss=[-p1,-p2,+plr,+expl]]
poss -> acc     <wo(t):>    [+def,poss=[-p1,+p2,-plr,+frm,+expl]]

## ACCUSATIVE
acc -> cnj        [:]      [-acc,rl=[-acc]]
acc -> cnj        [n:]     [+acc,pp=None,rl=[-p,+acc]]

## CONJUNCTIVE SUFFIXES
cnj -> end        [:]      [cnj=None,pos=n]
cnj -> end        [m:]     [cnj=m,pos=n]
cnj -> end        <s_:>    [cnj=s,pos=n]
cnj -> end        <n_a:>   [cnj=na,pos=n]

end ->
