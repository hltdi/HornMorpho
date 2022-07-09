-> start

start -> pn0   []         [tm=p,+neg]
start -> end   []        [tm=p,-neg]
start -> i0   []           [tm=i]
start -> j0   []           [tm=j]

pn0 -> pn1         [{I2e}] [c=E]
pn0 -> pn1         [C]          [c=F]
pn0 -> pn1         []            [c=A|B|C|D]
pn1 -> end         [{e2I}] [c=E];[c=A,vc=a]
pn1 -> end          [X]        [c=A,vc=0|ps|at];[c=B|C|D]

i0 -> i1              [C]          [c=E|F]
i0 -> i1              []             [c=A|B|C|D]
i1 -> i2              [X]           
i2 -> end            [X]          [vc=ps]
i2 -> end            [{e2I}] [vc=0|a|at]

j0 -> j1            [{I2e}]   [c=E]
j0 -> j1            [C]            [c=F]
j0 -> j1            []              [c=A|B|C|D]
j1 -> j2            [{e2I}]   [c=E];[c=A,vc=0|a]
j1 -> j2            [X]            [c=B|C|D|F];[c=A,vc=ps|at]
j2 -> end          [X]            [vc=ps];[c=A,j=i,vc=0]
j2 -> end          [{e2I}]   [c=B|C|D|E|F,vc=0|a|at];[c=A,vc=a|at];[c=A,j=t,vc=0]

end -> end       [X;C]
end ->

