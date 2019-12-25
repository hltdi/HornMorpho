## roots for Ks verb guesser FST

-> start

start -> A1  [CC]   [cls=A];[cls=Aw]
A1 -> A2     [CC]
A2 -> end    [CC]

start -> B1  [CC]   [cls=B]
B1 -> B2     [CC-h]
B2 -> end    [CC]

start -> C1  [CC]   [cls=C]
C1 -> C2     [CC-h]
C2 -> end    [CC]

start -> E1  [CC]   [cls=E];[cls=F]
E1 -> E2     [CC]
E2 -> E3     [CC]
E3 -> end    [CC]

end ->