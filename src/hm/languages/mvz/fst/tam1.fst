-> start

start -> pn0   []         [tm=p,+neg]
start -> end   []        [tm=p,-neg]
start -> i0   []           [tm=i]
start -> j0   []           [tm=j]
start -> j1   []            [tm=j,c=A|B|C|D|F]
start -> j1   [{I2e}] [tm=j,c=E]

pn0 -> pn1         [{I2e}] [c=E]
pn0 -> pn1         [C]          [c=F]
pn0 -> pn1         []            [c=A|B|C|D]
pn1 -> end         [{e2I}] [c=E];[c=A,cs=1]
pn1 -> end          [X]        [c=A,cs=0|2];[c=B|C|D]

i0 -> i1              [C]          [c=E]
i0 -> i1              []             [c=A|B|C|D]
i1 -> i2              [X]
i2 -> end            [X]          [+ps]
i2 -> end            [{e2I}] [-ps]

j0 -> j1            [{I2e}]   [c=E]
j0 -> j1            []              [c=A|B|C|D]
j1 -> j2            [{e2I}]   [c=A|E]
j1 -> j2            [X]            [c=B|C|D]
j2 -> end          [X]            [+ps];[c=A,j=i,-ps]
j2 -> end          [{e2I}]   [c=B|C|D|E,-ps];[c=A,j=t,-ps]

end -> end       [X;C]
end ->

