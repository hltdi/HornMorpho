-> start

start -> nolab  []    [-W]
nolab -> nolab  [X;C]

### classes A, B, C, E, s=0

## 3 is labializable
start -> lab3   []    [3=B,s=0,+W]
# but not if it's velar and Y is true
start -> lab12  []    [3=T|R|N,s=0,+W];[3=K,s=0,+Y,+W]
# labialize 2 only in case of redup
lab12 -> lab2   []    [2=B|K]
# labialize 1 only in case of redup
lab12 -> lab1   []    [1=B|K,2=T|R|N]
# 1 and 2 are not labializable
lab12 -> nolab   []    [1=T|R|N|a|w,2=T|R|N]

## labialization of final segment
# skip 0 for E and redup ABC
lab3 -> lab3.0    [X;C]    [c=E|F];[c=A|B|C,s=0,as=it]
# skip 1, unless E is +d
lab3.0 -> lab3.1  [X;C]    [c=E|F,-d];[as=it]
# labialize 1 B or G, vowel I or e
lab3.0 -> lab3.1  [{labB.Ie};{labG.Ie}]
# skip 1 for ABC -it
lab3 -> lab3.1    [X;C]
# skip 2 for ABC -d and 1 for E
lab3.1 -> lab3.2  [X;C]    [-d];[c=E|F]
# labialize 2
lab3.1 -> lab3.2  [{labB.Ie};{labG.Ie}]
# labialize 3
lab3.2 -> end     [{labB.I}]

## labialization of 2nd to last segment
lab2 -> lab2.0    [X;C]    [c=E|F,-d];[c=A|B|C,s=0,as=it]
lab2 -> lab2.0    [{labB.Ie};{labG.Ie}]    [c=E|F,+d]
lab2.0 -> lab2.1  [X;C]    [c=E|F]
lab2.0 -> lab2.1  [{labB.a};{labG.a}]      [as=it]
lab2 -> lab2.1    [X;C]
lab2.1 -> lab2.2  [{labB.Ie};{labG.Ie}]
lab2.2 -> end     [X;C]

## labialization of 3rd to last segment
lab1 -> lab1.0    [X;C]    [c=E|F]
lab1 -> lab1.0    [{labB.I};{labG.I}]       [c=A|B|C,s=0,as=it]
lab1.0 -> lab1.1  [X;C]
# also labG.E (or would this always be palatalized in class B?)
lab1 -> lab1.1    [{labB.Ie};{labG.Ie};{labB.E}]
lab1.1 -> lab1.2  [X;C]
lab1.2 -> end     [X;C]

### class A,B a3

start -> lab2a3   []   [s=a3,2=B|K,+W]
start -> lab01a3  []    [s=a3,2=T|R|N,+W]
lab01a3 -> lab1a3 []    [s=a3,1=B|K]
lab01a3 -> nolab  []    [s=a3,1=T|R|N]

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

### class A,B,E e3

## ዝነጘ
start -> lab2e3  []   [s=e3,2=C,+W]
# ጨ<ኘ>; any other possibilities for c2? (what about 3p prf?)
start -> lab01e3 []   [s=e3,2=J,+W]
lab01e3 -> lab1e3 []  [s=e3,1=B|K]
# <ጨ>ኘ
lab01e3 -> nolab  []  [s=e3,1=J|N]

## labialization of first segment (second in class E)
# C0 in E
lab1e3 -> lab1e3.0    [X;C]   [c=E|F]
# Labialize C1 in E and F
lab1e3.0 -> lab1e3.1  [{labB.e};{labG.e};{labB.a};{labG.a}]
# Labialize C1 in A,B
lab1e3 -> lab1e3.1    [{labB.e};{labG.e}]   [c=A|B]
# C2
lab1e3.1 -> end       [X;C]

## labiabization of last segment
# C0 in E
lab2e3 -> lab2e3.0   [X;C]   [c=E|F]
# C1 in E
lab2e3.0 -> lab2e3.1 [X;C]
# C1 in A,B
lab2e3 -> lab2e3.1   [X;C]    [c=A|B]
# Labialize C2
lab2e3.1 -> end      [{lab.Ie}]

### still to do: class D (ቅየ), anomalous (ወረ, ባረ)

nolab ->
end ->
