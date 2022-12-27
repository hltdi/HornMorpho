-> start

start -> p   []            [tm=p]
start -> i       []        [tm=i]
start -> j       []        [tm=j]

p -> end          []           [c=B];[c=A,s=t];[c=A,s=i,sp=1|2]
p -> p1            [e]          [c=A,s=i,sp=3]
# but this is optional for some "intransitive" verbs, like ቀረበ
p1 -> end        [{e2i}]

i -> i1             [e]             [c=A]
i -> i1             [{e2E}]    [c=B]
i1 -> end         [{e2I}]   [c=A,s=t];[c=B]

j -> j1                [e]         [c=B]
j -> j1              [{e2I}]   [c=A]
j1 -> end          [{e2I}]   [c=B];[c=A,s=t]
j1 -> end          [e]           [c=A,s=i]

end -> end       [%X]
end ->

