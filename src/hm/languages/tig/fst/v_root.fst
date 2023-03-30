## roots for Tigre verb guesser FST

-> start

start -> A1  [X]     [cls=A]
A1 -> A2     [X]
A2 -> end    [X]

start -> B1  [X]     [cls=B]
B1 -> B2     [X]
B2 -> end    [X]

start -> C1  [X]     [cls=C]
C1 -> C2     [X]
C2 -> end    [X]

start -> E1  [X]     [cls=E];[cls=F];[cls=Ew]
E1 -> E2     [X]     [cls=E];[cls=F]
# only 3 explicit consonants for Ew (gorete)
E1 -> E3     [X]     [cls=Ew]
E2 -> E3     [X]
E3 -> end    [X]

start -> G0  [n;s]   [cls=G];[cls=H]
G0 -> G1     [X]
G1 -> G2     [X]
G2 -> G3     [X]
G3 -> end    [X]

end ->