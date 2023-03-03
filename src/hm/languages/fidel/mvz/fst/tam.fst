-> start

start -> pn0   []         [tm=p,+neg]
start -> p0    []         [tm=p,-neg]
start -> i0    []           [tm=i]
start -> j0    []           [tm=j]

# changes to prf -neg for vc=ps|a
# %% handle A,E, as=at here instead of in depal.fst
# vc=0, cc=4 verbs and cc=3 verbs that are not hollow
p0 -> end         []           [vc=0|ps];[c=B|C|D|E|F|K];[c=A,-hol];[c=A,+hol,2=e|o]
# ሳመ
p0 -> end         [{a2e}]   [c=A,2=a,vc=a|at]

pn0 -> pn1         [{I2e}] [c=E]
pn0 -> pn1         [C]          [c=F]
pn0 -> pn1         []            [c=A|B|C|D]
pn1 -> end         [{e2I}] [c=E];[c=A,vc=a]
pn1 -> end          [X]        [c=A,vc=0|ps|at];[c=B|C|D]

# deficient A and B verbs
# no changes for V2 and V3 except
i0 -> end            [X]          [c=A,2=o|e];[c=A|B,3=a|e]
# for 2=a: ይሰም
i0 -> end            [{a2e}]   [2=a]
i0 -> i1              [C]          [c=E|F]
i0 -> i1              []             [c=A|B|C|D]
i1 -> i2              [X]           [c=B|C|D|E|F|K];[c=A,rc=3];[c=A,1=a]
i2 -> end            [X]          [vc=ps]
i2 -> end            [{e2I}] [vc=0|a|at]

j0 -> end          [X]            [c=A,2=o,1=J];[c=A,2=a]
j0 -> j1            [{I2e}]   [c=E]
j0 -> j1            [C]            [c=F]
j0 -> j1            []              [c=A|B|C|D]
j1 -> j2            [{e2I}]   [c=E];[c=A,2=B|K|T|J,vc=0|a]
j1 -> end          [{o2u}]   [c=A,2=o,1=B|K|T,vc=0|a]
j1 -> j2            [አ:ኣ]        [c=A,1=a,vc=0|at]
j1 -> j2            [X]            [c=B|C|D|F];[c=A,vc=ps|at]
j2 -> end          [X]            [vc=ps];[c=A,-tr,vc=0]
# there seem to be anomalous A verbs here: አልፍ(-tr), አሰር(+tr)
j2 -> end          [{e2I}]   [c=B|C|D|E|F,vc=0];[vc=a|at];[c=A,+tr,vc=0]
# no C3
j2 -> end          []              [3=a|e]

end -> end       [%X]
end ->

