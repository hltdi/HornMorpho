-> start

start -> nolab  []    [-W]
nolab -> nolab  [X;C]

## classes A, B, C, E, s=0

start -> lab3   []    [c3=B|K,s=0,+W]
start -> lab12  []    [c3=T|R|N,s=0,+W]
lab12 -> lab2   []    [c2=B|K]
lab12 -> lab1   []    [c1=B|K,c2=T|R|N]
lab12 -> nolab   []    [c1=T|R|N|a,c2=T|R|N]

# labialization of final segment
lab3 -> lab3.0    [X;C]    [c=E];[c=A|B|C,s=0,as=it]
lab3.0 -> lab3.1  [X;C]    [c=E,-d];[as=it]
lab3.0 -> lab3.1  [{labB.Ie};{labG.Ie}]
lab3 -> lab3.1    [X;C]
lab3.1 -> lab3.2  [X;C]    [-d];[c=E]
lab3.1 -> lab3.2  [{labB.Ie};{labG.Ie}]
lab3.2 -> end     [{labB.I}]

# labialization of 2nd to last segment
lab2 -> lab2.0    [X;C]    [c=E,-d];[c=A|B|C,s=0,as=it]
lab2 -> lab2.0    [{labB.Ie};{labG.Ie}]    [c=E,+d]
lab2.0 -> lab2.1  [X;C]    [c=E]
lab2.0 -> lab2.1  [{labB.a};{labG.a}]      [as=it]
lab2 -> lab2.1    [X;C]
lab2.1 -> lab2.2  [{labB.Ie};{labG.Ie}]
lab2.2 -> end     [X;C]

# labialization of 3rd to last segment
lab1 -> lab1.0    [X;C]    [c=E]
lab1 -> lab1.0    [{labB.I};{labG.I}]       [c=A|B|C,s=0,as=it]
lab1.0 -> lab1.1  [X;C]
# also labG.E (or would this always be palatalized in class B?)
lab1 -> lab1.1    [{labB.Ie};{labG.Ie};{labB.E}]
lab1.1 -> lab1.2  [X;C]
lab1.2 -> end     [X;C]

## class A,B a3

start -> lab2a3   []   [s=a3,c2=B|K,+W]
start -> lab01a3  []    [s=a3,c2=T|R|N,+W]
lab01a3 -> lab1a3 []    [s=a3,c1=B|K]
lab01a3 -> nolab  []    [s=a3,c1=T|R|N]

# labialization of first segment
lab1a3 -> lab1a3.0   [{labB.I}{labG.I}]    [as=it]
lab1a3 -> lab1a3.1   [{labB.e}{labG.e};{labB.E}]
lab1a3.0 -> lab1a3.1 [X;C]
lab1a3.1 -> end     [X;C]

# labialization of final segment
lab2a3 -> lab2a3.0  [X;C]   [as=it]
lab2a3.0 -> lab2a3.1 [{labB.a};{labG.a}]
lab2a3 -> lab2a3.1  [X;C]
lab2a3.1 -> end     [{labB.a};{labG.a}]         [-Y]
lab2a3.1 -> end     [{labB.a2e};{labG.a2e}]     [+Y]

## class A,B,E e3

# ዝነጘ
start -> lab2e3  []   [s=e3,c2=C,+W]
# ጨ<ኘ>; any other possibilities for c2? (what about 3p prf?)
start -> lab01e3 []   [s=e3,c2=J,+W]
lab01e3 -> lab1e3 []  [s=e3,c1=B|K]
# <ጨ>ኘ
lab01e3 -> nolab  []  [s=e3,c1=J|N]

# labialization of first segment (second in class E)
lab1e3 -> lab1e3.0    [X;C]   [c=E]
lab1e3.0 -> lab1e3.1  [{labB.e};{labG.e}]
lab1e3 -> lab1e3.1    [{labB.e};{labG.e}]   [c=A|B]
lab1e3.1 -> end       [X;C]

# labiabization of last segment
lab2e3 -> lab2e3.0   [X;C]   [c=E]
lab2e3.0 -> lab2e3.1 [X;C]
lab2e3 -> lab2e3.1   [X;C]    [c=A|B]
lab2e3.1 -> end      [{labC.Ie}]

nolab ->
end ->
