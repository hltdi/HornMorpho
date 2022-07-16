-> start

start -> nolab  []    [-W]
nolab -> nolab  [X;C]

### classes A, B, C, E, s=0

## 3 is labializable
start -> lab3   []    [3=B,s=0,+W]
# but not if it's velar and Y is true
start -> lab12  []    [3=T|R|N,s=0,+W];[3=K,s=0,+Y,+W]
# labialize 2
lab12 -> lab2   []    [2=B|K]
# labialize 1
lab12 -> lab1   []    [1=B|K,2=T|R|N]
# 1 and 2 are not labializable
lab12 -> nolab   []    [1=T|R|N|a|w,2=T|R|N]

## labialization of final segment
# skip 0 for E and redup ABCD
lab3 -> lab3.0    [%X]    [c=E|F];[c=A|B|C|D,s=0,as=it]
# skip 1, unless E is +d
lab3.0 -> lab3.1  [%X]    [c=E|F,-d];[as=it]
# labialize 1 B or G, vowel I or e
lab3.0 -> lab3.1  [{lab.Ie}]
# skip 1 for ABC -it
lab3 -> lab3.1    [%X]       [c=A|B|C|D,as=0|a]
# skip 2 for ABC -d and 1 for E
lab3.1 -> lab3.2  [%X]    [-d];[c=E|F]
# labialize 2 for +d
lab3.1 -> lab3.2  [{lab.Ie}]   [+d]
# labialize 3
lab3.2 -> end     [{labB.I}]

## labialization of 2nd to last segment
# skip 0 for E and ABCD iter
lab2 -> lab2.0    [%X]    [c=E|F,-d];[c=A|B|C|D,s=0,as=it]
# labialize 0 for E|F redup
lab2 -> lab2.0    [{lab.Ie}]    [c=E|F,+d]
# labialize 1 for ABCD iter
lab2.0 -> lab2.1  [{lab.a}]      [as=it]
# skip 0 and 1 for ABCD -redup
lab2 -> lab2.1    [%X]      [c=A|B|C|D,as=0|a]    
# labialize 2
lab2.1 -> end     [{lab.Ie}]

## labialization of 3rd to last segment
lab1 -> lab1.0      [%X]    [c=E|F]
lab1.0 -> end     [{lab.Ie}]
lab1 -> end         [{lab.I}]       [c=A|B|C|D,s=0,as=it]
lab1 -> lab1.0.3    []                 [c=A|B|C|D,s=0,as=0|a]
# also labG.E (or would this always be palatalized in class B?)
lab1.0.3 -> end      [{lab.Ie};{labB.E}]

### class A,B a3

start -> lab2a3   []   [s=a3,2=B|K,+W]
start -> lab01a3  []    [s=a3,2=T|R|N,+W]
lab01a3 -> lab1a3 []    [s=a3,1=B|K]
lab01a3 -> nolab  []    [s=a3,1=T|R|N]

# labialization of first segment
lab1a3 -> lab1a3.0   [{lab.I}]    [as=it]
lab1a3 -> lab1a3.1   [{lab.e};{labB.E}]
lab1a3.0 -> lab1a3.1 [%X]
lab1a3.1 -> end            [%X]

# labialization of final segment
lab2a3 -> lab2a3.0  [%X]   [as=it]
lab2a3.0 -> lab2a3.1 [{lab.a}]
lab2a3 -> lab2a3.1  [%X]
lab2a3.1 -> end     [{lab.a}]         [-Y]
lab2a3.1 -> end     [{lab.a2e}]     [+Y]

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
lab1e3 -> lab1e3.0    [%X]   [c=E|F]
# Labialize C1 in E and F
lab1e3.0 -> lab1e3.1  [{lab.e};{lab.a}]
# Labialize C1 in A,B
lab1e3 -> lab1e3.1    [{lab.e}]   [c=A|B]
# C2
lab1e3.1 -> end       [%X]

## labiabization of last segment
# C0 in E
lab2e3 -> lab2e3.0   [%X]   [c=E|F]
# C1 in E
lab2e3.0 -> lab2e3.1 [%X]
# C1 in A,B
lab2e3 -> lab2e3.1   [%X]    [c=A|B]
# Labialize C2
lab2e3.1 -> end      [{lab.Ie}]

### still to do: class D (ቅየ), anomalous (ወረ, ባረ)

end -> end  [%X]
nolab ->
end ->
