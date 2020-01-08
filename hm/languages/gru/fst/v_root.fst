## roots for Ks verb guesser FST

-> start

start -> A1  [CC-y]  [cls=A];[cls=Aw];[cls=AW]
#A1 -> A2     [RR]    [cls=A];[cls=Aw];[cls=AW]
A1 -> A2     [ZZ]    [cls=AW];[cls=A]
A1 -> A2     [PP]    [cls=Aw];[cls=A]
A1 -> A2     [UU]    [cls=A]
A2 -> end    [CC]

start -> B1  [CC-y]   [cls=B]
B1 -> B2     [RR-h]
B2 -> end    [CC]

start -> C1  [RR-y]   [cls=C]
C1 -> C2     [RR-h,y]
C2 -> end    [CC]

start -> E0  [n;:]    [cls=E];[cls=F]
E0 ->  E1    [RR-y]
E1 ->  E2W   [UU]
E2W -> E3    [RR]
E3 -> end    [CC]

E1 -> E2h    [h]
E2h -> E3    [RR]

E1 -> E2b    [b]
E2b -> E3    [RR-b]

E1 -> E2c    [c]
E2c -> E3    [RR-c]

E1 -> E2C    [C]
E2C -> E3    [RR-C]

E1 -> E2d    [d]
E2d -> E3    [RR-d]

E1 -> E2f    [f]
E2f -> E3    [RR-f]

E1 -> E2g    [g]
E2g -> E3    [RR-g]

E1 -> E2j    [j]
E2j -> E3    [RR-j]

E1 -> E2k    [k]
E2k -> E3    [RR-k]

E1 -> E2l    [l]
E2l -> E3    [RR-l]

E1 -> E2m    [m]
E2m -> E3    [RR-m]

E1 -> E2n    [n]
E2n -> E3    [RR-n]

E1 -> E2q    [q]
E2q -> E3    [RR-q]

E1 -> E2r    [r]
E2r -> E3    [RR-r]

E1 -> E2s    [s]
E2s -> E3    [RR-s]

E1 -> E2x    [x]
E2x -> E3    [RR-x]

E1 -> E2S    [S]
E2S -> E3    [RR-S]

E1 -> E2t    [t]
E2t -> E3    [RR-t]

E1 -> E2T    [T]
E2T -> E3    [RR-T]

E1 -> E2z    [z]
E2z -> E3    [RR-z]

E1 -> E2Z    [Z]
E2Z -> E3    [RR-Z]

end ->