-> start

start -> end   []       [as=0];[c=C|D|F]

start -> a       []       [as=a,vc=ps|at]

start -> it     []       [as=it,vc=0|ps|at]

a -> a0              [C]         [c=E]
a -> a0              []           [c=A|B]
a0 -> end          [{e2a}]  

# V1: e->0
it -> it1          [{e2I};C]
it1 -> it2b       [ባ:]
it2b -> end       [በ;ብ]
it1 -> it2m       [ማ:]
it2m -> end       [መ;ም]

end -> end       [X;C]
end ->

