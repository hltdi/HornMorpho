## Depalatalization for B and A ቾተ class verbs in perfect negative and jussive
## Gemination

-> start

start -> depal1    []  [tm=p,+neg];[tm=j]

start -> p      []     [tm=p,-neg,-depal]

start -> i      []      [tm=i,-depal]

depal1 -> depal2  []   [c=B,+depal,+gem];[c=A,2=o,1=J,+depal,-gem]
depal1 -> end         []    [c=A,rc=3,-depal,-gem];[c=A,rc=2,1=B|K|T,-depal,-gem];[c=C|D|E|F|K,-gem]

p -> end        []       [c=B|C|D|E|F,+gem];[c=A,rc=3,+gem];[c=A,rc=2,-gem]

i -> end         []       [c=B|C|D|E|F,+gem];[c=A,rc=3,+gem,vc=ps|at];[c=K,-gem];[c=A,vc=0|a,-gem];[c=A,rc=2,-gem]

depal2 -> depal2 [%X]
end -> end              [%X]

depal2 ->
end ->
