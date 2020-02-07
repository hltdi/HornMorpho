## Tigre root -> derivational stems
## Features:
##   der: ps, tr, cs, rc, it
## Root types:

-> start

## derivational prefixes
start -> stem       [:]    [vc=[-ps,-cs],as=None|it]
start -> stem       [a:]   [vc=[-ps,+cs],as=None|it]
start -> stem       [t:]    [vc=[+ps,-cs]]
start -> stem       <at:>  [vc=[+ps,+cs]]
start -> stem       [a:]   [vc=[-ps,+cs]]

### A verbs
## strong
stem -> A1           [RR]   [cls=A]
A1 -> A1v            [e:]   [tm=prf|imf,as=None];[tm=j_i,vc=[+ps]]
A1 -> A1v            [:]    [tm=j_i,vc=[-ps],as=None|it];[as=it]
A1v -> A2            [RR]
A2 -> A2it           [:]    [as=rc|None]
A2 -> A2it           [D:]   [as=it]
# imperfective: gemination when there are no subject suffixes (1, 2sm, 3s) and no 1 or 2 object suffixes; always geminate in imp with 3 obj, unless 2|3pf
A2it -> A2_          [_:]   [tm=imf,sp=1,op=None];[tm=imf,sp=2,sn=1,sg=m,op=None];[tm=imf,sp=3,sn=1,op=None];[tm=imf,op=3,sp=1];[tm=imf,op=3,sp=2,sg=m];[tm=imf,op=3,sp=2,sn=1,sg=f];[tm=imf,vc=[+ps]]
# unless there is 3 obj with anything but 2|3pf, don't geminate before other objects, in 2sf, or 2,3p
A2it -> A2_          [:]    [tm=prf];[tm=j_i];[tm=imf,op=1|2];[tm=imf,sp=2,sn=1,sg=f,op=None];[tm=imf,sp=2|3,sn=2,op=None];[tm=imf,sp=2|3,sn=2,sg=f,op=3]
# e dropped in prf,-ps with -V suffix
A2_ -> A2v           [:]    [tm=prf,sp=3,vc=[-ps]]
A2_ -> A2v           [e:]   [tm=prf,sp=1|2];[tm=prf,vc=[+ps]]
# separate out jussive and imperative because of all the vowel changes
A2_ -> A2_j          [:]    [tm=j_i];[tm=imf,vc=[+ps]]
A2_ -> A2_i          [:]    [tm=imf,vc=[-ps]]
# imperf -ps (unless there's an object triggered vowel change): no V2
A2_i -> A2vi         [:]    [op=None|1|2];[sp=1,op=3];[sp=2,sn=1,sg=m,op=3];[sp=3,sn=1,op=3];[sp=2|3,sn=2,sg=f,op=3]
# jussive and passive imperf (unless there's an object triggered vowel change)
A2_j -> A2v          [e:]   [op=None|1|2];[sp=1,op=3];[sp=2,sn=1,sg=m,op=3];[sp=3,sn=1,op=3];[sp=2,sn=2,sg=f,op=3]
# imperf -ps with object-triggered I->i: tqet_ilo
A2_i -> A2v          [i:]   [sp=2,sn=1,sg=f,op=3]
# imperf -ps with object-triggered I-> : tqet_ulo, lqet_ulo
A2_i -> A2v          [u:]   [sp=2|3,sn=2,sg=m,op=3]
# jussive and +ps imperf with object-triggered e->E: qtElo
A2_j -> A2v          [E:]  [sp=2,sn=1,sg=f,op=3]
# jussive and +ps imperf with object-triggered e->o: qtolo, lqtolo
A2_j -> A2v          [o:]   [sp=2|3,sn=2,sg=m,op=3]
## *CC (+dup) roots treated specially in imperfect, -passive: lden_
A2vi -> end          [_:RR] [+dup]
A2vi -> end          [RR]   [-dup]
A2v -> end           [RR]   
## weak
# h**
# w**
# y**
# *h*
# *w*
# *y*
# **h
# **w
# **y

### B verbs
stem -> B1           [RR]   [cls=B]
B1 -> B1v            [e:]   [as=None|it]
B1 -> B1v            [a:]   [as=rc]
B2 -> B2it           [D:]   [as=it]
B2 -> B2it           [:]    [as=None|rc]
B2it -> B2_          [_:]
B2_ -> B2v           [e:]   [tm=prf];[tm=imf,vc=[+ps,-cs]];[tm=j_i,vc=[+ps,-cs]]
B2_ -> B2v           [:]    [tm=j_i,vc=[-ps]];[tm=imf,vc=[-ps],-dup];[tm=imf,vc=[-ps],+dup,op=None]
# in *CC verbs (+dup) gemination before objects: 'azzakkum
B2_ -> B2vid         [:]    [+dup,op=1|2|3]
B2vid -> end         [:RR]
B2v -> end           [RR]
## weak
# h**
# w**
# y**
# *w*
# *y*
# **h
# **w
# **y

### C verbs (no as=rc option)
# +ps,+cs in B, but it seem atC1aC2_eC3- is also possible for C verbs with [vc=[+ps,+cs],as=None]
stem -> C1           [RR]   [cls=C]
C1 -> C1v            [a:]   [as=None]
C1 -> C1v            [e:]    [as=it]
C1v -> C2            [RR]
C2 -> C2it           [D:]   [as=it]
C2 -> C2it           [:]    [as=None]
# never geminate
C2it -> C2_          [:]    
C2_ -> C2v           [e:]   [tm=prf];[tm=imf,vc=[+ps,-cs]];[tm=j_i,vc=[+ps,-cs]]
C2_ -> C2v           [:]    [tm=imf|j_i,vc=[-ps]];[tm=imf|j_i,vc=[+cs]]
C2v -> end           [RR]
# **y
# **h

### E/F verbs
# no iterative (so far)
stem -> E1           [RR]   [cls=E,as=None|rc];[cls=F,as=None]
E1 -> E1v            [e:]   
E1v -> E2            [RR]
E2 -> E2v            [e:]   [cls=E,as=None,tm=prf|imf]
E2 -> E2v            [a:]   [cls=F];[cls=E,as=rc]
E2 -> E2v            [:]    [cls=E,tm=j_i,as=None]
E2v -> E3            [RR]
E3 -> E3v            [e:]  [tm=prf];[tm=imf,vc=[+ps,-cs]];[tm=j_i,vc=[+ps,-cs]]
E3 -> E3v            [:]   [tm=imf|j_i,vc=[-ps]];[tm=imf|j_i,vc=[+cs]]
E3v -> end           [RR]
## weak
# ***y
# ***h

### G verbs, 5 stem consonants

start -> 

end ->
