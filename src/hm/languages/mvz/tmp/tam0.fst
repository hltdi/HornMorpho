### Still need to handle negative, which has different templates and gemination patterns
### and vc=[+cs]
-> start

## affirmative perfective; no changes
start -> end []    [tm=p,+gem,-neg]
## imperfective, jussive (treat negative jussive separately (for B))?
start -> ij  []    [tm=i|j]
start -> end []   [c=A|C|D,tm=p,-gem,+neg]

## negative perfective
start -> pneg  []    [tm=p,+neg]
# A,C,D: no gemination
pneg -> end      []    [c=A|C|D,-gem]
# B: depalatalize C1
pneg -> pnegB2 [{depal.e};{B.E2e}]  [c=B,s=0|P12,+gem]
pneg -> pnegB2  [X] [c=B,s=P2,+gem]
pnegB2 -> end     [X] [s=0]
pnegB2 -> end     [{depal.e}]   [s=P2|P12]
# E: ኣንመስከረ; C1eC2C3eC4, no gemination
pneg -> Epn1 [{I2e}]   [c=E,-gem]
Epn1-> end    [{e2I}]

## E: C0, C1
# keep C0
ij -> Ei1  [C]     [c=E,tm=i,+gem]
# C0 jussive: I=>e <ም>ረመር => <መ>ርመር
ij -> Ej1  [{I2e}] [c=E,tm=j,-gem]
# keep C1
Ei1 -> C2  [X]
# C1 jussive: e=>I ም<ረ>መር => መ<ር>መር
Ej1 -> C2  [{e2I}]

# Keep C1e
ij -> C2   [X]     [c=C|D];[c=A|B,tm=i];[c=A,tm=j,vc=[+ps]];[c=B,s=P2,tm=j]
# A: jussive: C1 e=>I
ij -> C2   [{e2I}] [c=A,tm=j,vc=[-ps]]
# B : jussive: depalatalize
ij -> C2   [{depal.e};{B.E2e}]  [c=B,s=0|P12,tm=j]


## C2
# keep C2e: passive; A "intransitive" jussive C2e
C2 -> end  [X]   [c=A|C|D|E,vc=[+ps]];[c=A,tm=j,j=i,vc=[-ps]];[c=B,tm=i,vc=[+ps]];[c=B,tm=j,s=0,vc=[+ps]]
# non-passive C2e: e => I
C2 -> end  [{e2I}] [c=C|D,tm=i|j,+gem,vc=[-ps]];[c=A,tm=i,-gem,vc=[-ps]];[c=A,tm=j,j=t,vc=[-ps]];[c=B,+gem,tm=i];[c=B,+gem,s=0,tm=j]
# B jussive: depalatalize C2 (s=P2|P12)
C2-> end  [{depal.e2I}]   [c=B,tm=j,+gem,s=P2|P12,vc=[-ps]]
C2 -> end [{depal.e}]       [c=B,tm=j,+gem,s=P2|P12,vc=[+ps]]
 
end -> end       [X;C]
end ->

