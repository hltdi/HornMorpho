### Still need to handle negative, which has different templates and gemination patterns
### and vc=[+cs]
-> start

## affirmative perfective; no changes
start -> end []    [tm=p,+gem,-neg]
## imperfective, jussive (treat negative jussive separately (for B))?
start -> ij  []    [tm=i|j]
## negative perfective
start -> pneg []   [tm=p,-gem,+neg]

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
ij -> C2   [X]     [c=B|C|D];[c=A,tm=i];[c=A,tm=j,vc=[+ps]]
# A: jussive: C1 e=>I
ij -> C2   [{e2I}] [c=A,tm=j,vc=[-ps]]

## C2
# keep C2e: passive; A "intransitive" jussive C2e
C2 -> end  [X]   [vc=[+ps]];[c=A,tm=j,j=i,vc=[-ps]]
# non-passive C2e: e => I
C2 -> end  [{e2I}] [c=B|C|D,tm=i,+gem,vc=[-ps]];[c=A,tm=i,-gem,vc=[-ps]];[c=A,tm=j,j=t,vc=[-ps]]

## negative perfective
 
end -> end       [X;C]
end ->

