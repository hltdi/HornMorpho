-> start

## PREPOSITIONS
start -> stem_bound    [:]      [prep=None,-gen]
start -> stem_bound     >>n_prep<<
start -> stem_bound     <ye:>    [+gen,prep=None]

## BOUNDARY BETWEEN PREFIXES AND STEM
stem_bound -> stem     [$:]      [pos=nm]

## STEM
stem -> stemC1       [XX]
stemC1 -> stemV1     [VV]
stemC1 -> stemC      [XX]
stemL1 -> stemV1     [VV]
stemL1 -> stemC      [XX]
stemV1 -> stemC      [XX]

stemC -> stemV       [VV]
stemC -> stemC       [XX]
stemL -> stemV       [VV]
stemL -> stemC       [XX]
stemV -> stemC       [XX]
stemV -> acc         [:]
stemC -> acc         [:]

## ACCUSATIVE
acc -> cnj        [:]      [-acc]
acc -> cnj        [n:]     [+acc,prep=None]

## CONJUNCTIVE SUFFIXES
cnj -> end        [:]      [cnj=None]
cnj -> end        [m:]     [cnj=m]
cnj -> end        <s_:>    [cnj=s]
cnj -> end        <n_a:>   [cnj=na]

end ->
