### Tigrinya verb classes
### 2020.3.13: '|' eliminated from roots; introduced here and then deleted in stem_tam.fst
### A: 123
### B: 12_3
### C: 1a2d
### E: 1234
### F: 12a34
### G: 1|2345
### H: 1|23a45
### I: 1|234
### J: 1|2a34
### K: 12345  ?

-> start

start -> A1  [X]     [cls=A]
A1 -> A2     [X]
A2 -> end    [X]

start -> B1  [X]     [cls=B]
B1 -> B2     [X]
B2 -> B2_    [_:]
B2_ -> end   [X]

start -> C1  [X]     [cls=C]
C1 -> C1a    [a:]
C1a -> C2    [X]
C2 -> end    [X]

start -> E1  [X]     [cls=E];[cls=F]
E1 -> E2     [X]     
E2 -> Fa     [a:]    [cls=F]
Fa -> E3     [X]
E2 -> E3     [X]     [cls=E]
E3 -> end    [X]

start -> G0  [X]     [cls=G];[cls=H]
G0 -> G|     [|:]
G| -> G1     [X]
G1 -> G2     [X]
G2 -> Ha     [a:]    [cls=H]
Ha -> G3     [X]
G2 -> G3     [X]     [cls=G]
G3 -> end    [X]

start -> I0  [X]     [cls=I];[cls=J]
I0 -> I|     [|:]
I| -> I1     [X]
I1 -> Ja     [a:]    [cls=J]
Ja -> I2     [X]
I1 -> I2     [X]     [cls=I]
I2 -> end    [X]

end ->