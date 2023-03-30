-> start

## PREPOSITIONS
start -> stem_bound    [:]      [prep=None,-gen]
start -> stem_bound     >>n_prep<<
start -> stem_bound     <ye:>    [+gen,prep=None]

## BOUNDARY BETWEEN PREFIXES AND STEM
stem_bound -> stem     [$:]

## STEM
# Place names; not necessarily -prp
stem -> acc     +nm_place+     [pos=nm_pl,tp=pl]
# Proper nouns (possessive is possible); always 3rd person singular
stem -> acc     +nm_name+     [pos=nm_prs,tp=prs]

## ACCUSATIVE
acc -> cnj        [:]      [-acc]
acc -> cnj        [n:]     [+acc,prep=None]

## CONJUNCTIVE SUFFIXES
cnj -> end        [:]      [cnj=None]
cnj -> end        [m:]     [cnj=m]
cnj -> end        <s_:>    [cnj=s]
cnj -> end        <n_a:>   [cnj=na]

end ->
