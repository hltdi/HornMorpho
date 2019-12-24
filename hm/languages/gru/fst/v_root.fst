## roots for Ks verb guesser FST

-> start

start -> A1  [X]   [cls=A]
A1 -> A2     [X]
A2 -> end    [X]

start -> B1  [X]   [cls=B]
B1 -> B2     [X-h]
B2 -> end    [X]

start -> C1  [X]   [cls=C]
C1 -> C2     [X-h]
C2 -> end    [X]

start -> E1  [X]   [cls=E]
E1 -> E2     [X]
E2 -> E3     [X]
E3 -> end    [X]

end ->