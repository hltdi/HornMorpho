### Amharic verb classes
### 2020.3.14: '|' eliminated from roots; introduced here and then deleted in stem_tam.fst
### 'a' and '_' also eliminated
### A: 123
### B: 12_3
### C: 1a2d
### E: 1234
### F: 12a34
### G: 1|2345
### H: 1|23a45
### I: 1|234
### J: 1|2a34
### K: 12345
### L: 12a345

-> start

start -> A1  [X]     [cls=A]
A1 -> A2     [X]
A2 -> end    [X]

start -> B1  [X]     [cls=B]
B1 -> B2     [X]
B2 -> B2_    [_:]
B2_ -> end   [X]

# C verbs can't start with '
start -> C1  [X/L]     [cls=C]
C1 -> C1a    [a:]
C1a -> C2    [X]
# C verbs can't end with ', y, or w, but they can end in * (ቃዠ)
C2 -> end    [X!]

start -> E1  [X]     [cls=E];[cls=F]
E1 -> E2L   [L]      [cls=E]
E1 -> E2     [X/L]
E2 -> Fa     [a:]    [cls=F]
Fa -> E3     [X]
E2 -> E3     [X]     [cls=E]
E2 -> E3Y   [J]      [cls=E]
E2L -> E3L [X]
E3 -> end    [X]
E3L -> end   [L]
E3Y -> end   [*]

start -> G0  [X]     [cls=G,-smp];[cls=H,-smp]
G0 -> G|     [|:]
G| -> G1     [X]
G1 -> G2     [X]
G2 -> Ha     [a:]    [cls=H]
Ha -> G3     [X]
G2 -> G3     [X]     [cls=G]
G3 -> end    [X]

start -> I0  [X]     [cls=I,-smp];[cls=J,-smp]
I0 -> I|     [|:]
I| -> I1     [X]
I1 -> Ja     [a:]    [cls=J]
Ja -> I2     [X]
I1 -> I2     [X]     [cls=I]
I2 -> end    [X]

# include for guesser
start -> K1  [X]     [cls=K];[cls=L]
K1 -> K2     [X]
K2 -> K3     [X]
K3 -> La     [a:]   [cls=L]
La -> K4     [X]
K3 -> K4      [X]     [cls=K]
K4 -> end    [X]

end ->
