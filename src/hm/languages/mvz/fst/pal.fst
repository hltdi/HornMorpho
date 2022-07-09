-> start

start -> nopal  []    [-Y]

### palatalize C3
## 3 is palatalizable
start -> pal3   []    [3=T|K|N,s=0,+Y];[3=R,s=0,+Y,-W]
# palatalize C3
pal3 -> pal3.0   [C]         [c=E|F]
pal3 -> pal3.0   []           [c=A|B|C|D]
pal3.0 -> pal3.1  [X;C]
pal3.1 -> pal3.2  [X;C]
# r,l -> y; n -> N; or for C3 = {r,l}, change V2 (I->i, e->E)
pal3.2 -> end         [{palG.I};{palD.I};{palR.I}]

### 3=0: በዳ; ትበጀ (not sure about 2=N)
start -> pal2a2  []   [3=a,2=T|K|N,+Y];[3=a,2=R,+Y,-W]
pal2a2 -> pal2a2.0   [C] [c=E|F]
pal2a2 -> pal2a2.0    []   [c=A|B|C|D]
pal2a2.0 -> pal2a2.1  [X;C]
pal2a2.1 -> end           [{palG.a2e};{palD.a2e};{palR.a2e}]
# palatalization of C2 not possible
start -> pal2a1  []   [3=a,2=B,+Y];[3=a,2=R,+Y,+W]
pal2a1 -> pal2a1.0   [C] [c=E|F]
pal2a1 -> pal2a1.0    []  [c=A|B|C|D]
# V1: e->E (what about V1=a?)
pal2a1.0 -> pal2a1.1  [{e2E};{I2i}]
# V2: a->e
pal2a1.1  -> end            [{B.a2e};{R.a2e}]

## # 3 is not palatalizable
start -> pal12  []    [3=B,s=0,+Y];[3=R,s=0,+Y,+W]
pal12 -> pal12.0     [C]   [c=E|F]
pal12 -> pal12.0      []    [c=A|B|C|D]
# V1 may be palatalized for some words: tsEhi ትሴሒ (< ሰከረ) (Leslau)
# and velar C1 may optionally be palatalized (skipping palatalization of V2) in Chaha/Gumer;
# neither of these currently implemented
pal12.0 -> pal12.1  [X;C]
# V2: I->i, e->E; another option, at least for Chaha/Gumer is palatalization of velar
pal12.1 -> end           [{B.I2i};{B.e2E};{D.I2i};{D.e2E};{G.I2i};{G.e2E}]

nopal -> nopal  [X;C]
end -> end    [X;C]

nopal ->
end ->

