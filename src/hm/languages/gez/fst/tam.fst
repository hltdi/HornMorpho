-> start

start -> p   []            [tm=p]
start -> i       []        [tm=i]
start -> j       []        [tm=j]
start -> g       []         [tm=g]

p -> end          []           [c=B|E];[c=A,s=t|ti];[c=A,sp=1|2]
p -> p1            [e]          [c=A,s=i|ti,sp=3]
p1 -> end        [{e2I}]

i -> i0              [e]             [c=E]
i -> i0               []              [c=A|B]
i0 -> i1             [e]             [c=A]
i0 -> i1             [{e2E}]    [c=B]
i0 -> i1             [{I2e}]     [c=E]
i1 -> end         [{e2I}]   [c=A|B|E]

j -> j0               [e]           [c=E]
j -> j0                []             [c=A|B]
j0 -> j1                [e]         [c=B]
j0 -> j1              [{e2I}]   [c=A]
j1 -> j2             [I]            [c=E]
j1 -> end          [{e2I}]   [c=B];[c=A,s=t]
j1 -> end          [e]           [c=A,s=i]
j2 -> end          [{e2I}]   [c=E]

# g -> g0

end -> end       [%X]
end ->

