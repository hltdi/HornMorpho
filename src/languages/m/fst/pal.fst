-> start

start -> nopal  []    [-Y];[3=J|GY,+Y];[3=e,2=J|GY,+Y]

### palatalize C3?
## 3 is palatalizable
start -> pal3   []    [3=T|K|N,s=0,+Y];[3=R,s=0,+Y,-W]
# palatalize C3
pal3 -> pal3.0   [C]         [c=E|F]
pal3 -> pal3.0   []           [c=A|B|C|D]
pal3.0 -> pal3.1  [%X]
pal3.1 -> pal3.2  [%X]
# r,l -> y; n -> N; or for C3 = {r,l}, change V2 (I->i, e->E)
pal3.2 -> end         [{pal.I}]

### 3 is not palatalizable
start -> pal12  []    [3=B,s=0,+Y];[3=R,s=0,+Y,+W]
pal12 -> pal12.0     [C]   [c=E|F]
pal12 -> pal12.0      []    [c=A|B|C|D]
# V1 may be palatalized for some words: tsEhi ትሴሒ (< ሰከረ) (Leslau)
# and velar C1 may optionally be palatalized (skipping palatalization of V2) in Chaha/Gumer;
# neither of these currently implemented
pal12.0 -> pal12.1  [%X]
# V2: I->i, e->E; another option, at least for Chaha/Gumer is palatalization of velar (not implemented)
pal12.1 -> end         [{e2E};{I2i}]

### 3=a: በዳ; ትበጀ (not sure about 2=N)
# C2 is palatalizable
start -> pal3a2  []   [3=a,2=T|K|N,+Y];[3=a,2=R,+Y,-W]
pal3a2 -> pal3a2.0   [C] [c=E|F]
pal3a2 -> pal3a2.0    []   [c=A|B|C|D]
pal3a2.0 -> pal3a2.1  [%X]
pal3a2.1 -> end           [{pal.a2e}]
# palatalization of C2 not possible
start -> pal3a1  []   [3=a,2=B,+Y];[3=a,2=R,+Y,+W]
pal3a1 -> pal3a1.0   [C] [c=E|F]
pal3a1 -> pal3a1.0    []  [c=A|B|C|D]
# V1: e->E (what about V1=a?)
pal3a1.0 -> pal3a1.1  [{e2E};{I2i}]
# V2: a->e
pal3a1.1  -> end            [{B.a2e};{R.a2e}]

nopal -> nopal  [%X]
end -> end    [%X]

nopal ->
end ->

