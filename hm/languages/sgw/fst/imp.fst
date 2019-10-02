# impersonal palatalization and labialization; 3smO labialization

-> start

start -> start  [XX;^;@;/]    [sp=1|2|3,op=None];[sp=1|2|3,on=2];[sp=1|2|3,op=3,og=f];[sn=2];[sp=2,sn=1,sg=f]

start -> lab    [:]           [sp=None];[op=3,og=m,on=1,sn=1,sp=1|3];[op=3,og=m,on=1,sn=1,sp=2,sg=m]

lab -> pal      [:]           [sp=None]

# 3smO
lab -> labO     [:]           [op=3,og=m,on=1]
labO -> labO    [e;a;E;A]
labO -> lab1    [@:]
labO -> labOnP  [/;:]
labOnP -> lab2  [DD]

# do nothing if the final consonant or vowel is already palatalized or will be.
pal -> lab2            [PP;^;E]

# Condition A: final a is palatalized
pal -> pal_a          [A:a]
# also palatalize previous dental
pal_a -> pal_aP       [^:]
pal_aP -> pal_aP      [/]
pal_aP -> lab2        [TT]

# palatalize *Ca
pal_a -> lab_a        [@:]
lab_a -> lab_a        [/]
lab_a -> fin          [MM;KK]

# don't palatalize final non-dental
pal_a -> pal_aL       [/;:]
pal_aL -> lab2        [KK;MM;r]

# Condition 1: palatalize final dental
pal -> pal1           [^:]
pal1 -> lab2          [TT]

# labialize final consonant
pal -> lab1            [@:]
# mutation possible for *Ch + n
lab1 -> lab1           [/]
lab1 -> fin            [MM;KK]

# labialize C2
pal -> lab2            [r]
lab2 -> lab2           [a;e;o;E;A]
lab2 -> lab2l          [@:]
lab2l -> lab2l         [/]
lab2l -> fin           [KK;MM]
# already labialized or labialize C1
lab2 -> lab2nl         [/;:]
lab2nl -> fin          [UU]
lab2nl -> lab3         [DD]

# labialize C1
lab3 -> lab3           [a;e;o;E;A]
lab3 -> lab3l          [@:]
lab3l -> lab3l         [/]
lab3l -> fin           [KK;MM]
# already labialized
lab3 -> lab3nl         [/;:]
lab3nl -> fin          [UU;DD;PP]

fin -> fin             [RG;V;^;@;/]
fin ->
start ->
