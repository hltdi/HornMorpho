# labialization of last labializable consonant; impersonal and 3sm light object suffix

-> start

start -> start  [X;V;^;@;/]    [sp=1|2|3,op=None];[sp=1|2|3,on=2];[sp=1|2|3,op=3,og=f];[sn=2];[sp=2,sn=1,sg=f]

start -> lab    [:]            [sp=None];[op=3,og=m,on=1,sn=1,sp=1|3];[op=3,og=m,on=1,sn=1,sp=2,sg=m]

lab -> lab      [^;/;a;e]

# labialize last consonant
lab -> lab1     [@:]
lab1 -> end     [KK;MM]

lab -> lab2     [TT]
lab2 -> lab2    [^;/;a;e;o]
lab2 -> lab2l   [@:]
lab2l -> end    [KK;MM]

lab2 -> lab3    [TT]
lab3 -> lab3    [^;/;a;e;o]
lab3 -> lab3l   [@:]
lab3l -> end    [KK;MM]

lab3 -> end     [TT]

start ->
end ->
end -> end    [X;V;^;@;/]