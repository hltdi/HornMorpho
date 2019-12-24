## Kistane root -> derivational stems
## Features:
##   der: ps, tr, cs, rc, it
## Root types:
##   A: sbr, Aw: s[o]bf B: sb_r, C: sabr, E: sbsb, F: sbasb, ?sbrbr, ?sbrabr

-> start

## derivational prefixes
start -> stem1       [:]    [vc=[-ps,-cs],as=None|it]
start -> stem1       [a:]   [vc=[-ps,+cs],as=None|it]
# te- only when there is no prefix (imperative or non-relative, non-negative prf with no conjunctions)
start -> stem1       <t*:>  [vc=[+ps,-cs]]
# [vc=[+ps,-cs],tm=prf,-rel,cnj=None,-neg];[vc=[+ps,-cs],tm=j_i,sp=2,-neg]
#start -> stem1       [t:]   [vc=[+ps,-cs],tm=imf];[vc=[+ps,-cs],+neg];[vc=[+ps,-cs],tm=j_i,sp=1|3];[vc=[+ps,-cs],tm=prf,+rel];[vc=[+ps,-cs],tm=prf,cnj=b|t|sl|In]
# passive with prefix: gemination of following consonant
#start -> stem1       [/:]   [vc=[+ps,-cs],tm=imf];[vc=[+ps,-cs],+neg];[vc=[+ps,-cs],tm=j_i,sp=1|3];[vc=[+ps,-cs],tm=prf,+rel];[vc=[+ps,-cs],tm=prf,cnj=b|t|sl|In]
start -> stem1       <at:>  [vc=[+ps,+cs]]
# optional gemination of C1 (fails for h**)
start -> stem1       <a/:>  [vc=[+ps,+cs]]

##
# Inkretteto
stem1 -> stem1n      [I:]   [vc=[-ps,-cs]]
# tenqleqqelo
stem1 -> stem1n      [:]    [vc=[+ps]];[vc=[+cs]]
stem1n -> stem       [n]
stem1 -> stem        [:]

### A verbs
## strong
stem -> A1           [X-h]  [cls=A|Aw,vc=[-cs]];[cls=A|Aw,vc=[-ps]];[cls=A|Aw,as=rc,vc=[+cs,+ps]]
A1 -> A1v            [o:]   [cls=Aw,as=None]
A1 -> A1v            [e:]   [cls=A,tm=prf|imf,as=None];[cls=A,tm=j_i,vc=[+ps]]
A1 -> A1v            [:]    [cls=A,tm=j_i,vc=[-ps],as=None|it];[cls=A,as=it]
A1 -> A1v            [a:]   [cls=A,as=rc]
A1 -> A1v            <uwa:> [cls=Aw,as=rc]
A1v -> A2            [FF]
A2 -> A2it           [:]    [as=rc|None]
A2 -> A2it           [D:]   [as=it]
A2it -> A2_          [_:]   [tm=prf,-neg];[tm=imf,vc=[+ps]];[tm=prf,+neg,vc=[+ps]]
# ** assumption is that gemination is only lost for -ps: alsebere, altseb_er
A2it -> A2_          [:]    [tm=prf,+neg,vc=[-ps]];[tm=imf,vc=[-ps]];[tm=j_i]
# for jussive, ±je feature used to control appearance of V2=e
A2_ -> A2v           [e:]   [tm=prf];[tm=imf|j_i,vc=[+ps]];[tm=j_i,+je];[tm=j_i,sp=2,-je];[tm=j_i,sp=1,sn=2,-je];[tm=j_i,sp=3,sn=1,sg=f,-je];[tm=j_i,+neg,-je]
# we need the vowel for 2sf
A2_ -> A2v           [I:]   [tm=j_i,sp=1,sn=1,-neg,-je,vc=[-ps]];[tm=j_i,sp=3,sn=2,-neg,-je,vc=[-ps]];[tm=j_i,sp=3,sn=1,sg=m,-neg,-je,vc=[-ps]]
A2_ -> A2vi          [:]    [tm=imf,vc=[-ps]]
A2vi -> end          [_:FF] [+dup]
A2vi -> end          [FF]   [-dup]
A2v -> end           [FF]   
## weak
# h**
stem -> A1v          [a:h]  [cls=A,vc=[-cs],tm=imf];[cls=A,vc=[-ps],tm=imf];[cls=A,vc=[-cs],tm=prf,-neg];[cls=A,vc=[-ps],tm=prf,-neg];[cls=A,vc=[+ps],tm=j_i,sp=2]
stem -> A1v          [e:h]  [cls=A,vc=[-cs],tm=prf,+neg];[cls=A,vc=[-ps],tm=prf,+neg];[cls=A,vc=[-cs],tm=j_i];[cls=A,vc=[-ps],tm=j_i]
stem -> A1v          <_a:h> [cls=A,tm=imf,vc=[+ps,-cs]];[cls=A,tm=j_i,vc=[+ps,+cs],sp=1|3]
# **h
A2_ -> end           [e:h]  [sp=3,sn=2];[sp=0,op=1|2];[sp=0,op=3,on=1,og=m]
A2_ -> end           [a:h]  [sp=1|2];[sp=3,sn=1]
A2_ -> end           [:h]   [sp=0,op=3,on=2];[sp=0,op=3,on=1,og=f]
# **y
A2_ -> end           [e:y]  [tm=prf]
A2_ -> end           [:y]   [tm=imf|j_i]
# *h*, *w*, *y* verbs don't behave like B verbs with at-
stem -> atA1hwy      [FF]   [cls=A,vc=[+cs,+ps]];[cls=Aw,vc=[+cs,+ps]]
# *h*
A1 -> A2v            [a:h]  [tm=prf|j_i,vc=[-cs]]
A1 -> A2v            [e:h]  [tm=imf];[tm=prf|j_i,vc=[+cs]]
atA1hwy -> A2v       [e:h]
# *w*
A1 -> A2v            [o:w]  [tm=imf|prf]
A1 -> A2v            [u:w]  [tm=j_i]
atA1hwy -> A2v       [o:w]  [tm=imf|prf]
atA1hwy -> A2v       [u:w]  [tm=j_i]
# *y*
A1 -> A2v            [i:y]
atA1hwy -> A2v       [i:y]

### B verbs
# A and C verbs with at- (vc=[+ps,+cs]) behave like B verbs
stem -> B1           [X-h]  [cls=B];[cls=A,vc=[+ps,+cs]];[cls=Aw,vc=[+ps,+cs]];[cls=C,vc=[+ps,+cs]]
B1 -> B1v            [i:]   [tm=prf,-neg,as=None];[tm=imf,as=None]
B1 -> B1v            [e:]   [tm=prf,+neg,as=None];[tm=j_i,as=None]
B1 -> B1v            [a:]   [as=rc]
B1 -> B1v            [:]    [as=it]
B1v -> B2            [FF]
B2 -> B2it           [D:]   [as=it]
B2 -> B2it           [:]    [as=None|rc]
B2it -> B2_          [_:]   [tm=prf];[tm=imf];[tm=j_i]
# no C2 gemination in imperative (**not sure about negative imperative)
# B2it -> B2_          [:]    [tm=j_i,sp=2]
B2_ -> B2v           [e:]   [tm=prf];[tm=imf,vc=[+ps,-cs]];[tm=j_i,vc=[+ps,-cs]]
B2_ -> B2v           [I:]    [tm=imf|j_i,vc=[-ps]];[tm=imf|j_i,vc=[+cs]]
B2v -> end           [FF]
## weak
# h**
stem -> B1v          [i:h]  [cls=B,tm=prf,-neg];[cls=B,tm=imf,vc=[-ps]];[cls=A,vc=[+ps,+cs],tm=prf,-neg];[cls=A,vc=[+ps,+cs],tm=imf]
stem -> B1v          [a:h]  [cls=B,tm=j_i,vc=[-ps]];[cls=B,tm=prf,+neg];[cls=B,tm=j_i,vc=[+ps],sp=2]
stem -> B1v          <_a:h> [cls=B,tm=j_i,vc=[+ps],sp=1|3];[cls=B,tm=imf,vc=[+ps]]
stem -> B1v          [e:h]  [cls=A,tm=j_i,vc=[+ps,+cs]];[cls=B,tm=j_i,vc=[+ps,+cs]]
# **h
B2_ -> end           [e:h]  [sp=3,sn=2];[sp=0,op=1|2];[sp=0,op=3,on=1,og=m]
B2_ -> end           [a:h]  [sp=1|2];[sp=3,sn=1]
B2_ -> end           [:h]   [sp=0,op=3,on=2];[sp=0,op=3,on=1,og=f]
# **y
B2_ -> end           [e:y]  [tm=prf]
B2_ -> end           [:y]   [tm=imf|j_i]

### C verbs
stem -> C1           [X]    [cls=C,vc=[-cs]];[cls=C,vc=[-ps]]
C1 -> C1v            [a:]   [as=rc|None]
C1 -> C1v            [:]    [as=it]
C1v -> C2            [FF]
C2 -> C2it           [D:]   [as=it]
C2 -> C2it           [:]    [as=None|rc]
C2it -> C2_          [_:]   [tm=prf,-neg];[tm=imf]
C2it -> C2_          [:]    [tm=prf,+neg];[tm=j_i]
C2_ -> C2v           [e:]   [tm=prf];[tm=imf,vc=[+ps,-cs]];[tm=j_i,vc=[+ps,-cs]]
C2_ -> C2v           [I:]    [tm=imf|j_i,vc=[-ps]];[tm=imf|j_i,vc=[+cs]]
C2v -> end           [FF]
# **y
C2_ -> end           [e:y]  [tm=prf]
C2_ -> end           [:y]   [tm=imf|j_i]
# **h
C2_ -> end           [e:h]  [sp=3,sn=2];[sp=0,op=1|2];[sp=0,op=3,on=1,og=m]
C2_ -> end           [a:h]  [sp=1|2];[sp=3,sn=1]
C2_ -> end           [:h]   [sp=0,op=3,on=2];[sp=0,op=3,on=1,og=f]

### E/F verbs
# no iterative (so far)
stem -> E1           [X]    [cls=E];[cls=F]
E1 -> E1v            [:]    [tm=prf];[tm=imf];[tm=j_i,cls=F]
E1 -> E1v            [e:]   [tm=j_i,cls=E]
E1v -> E2            [FF]
E2 -> E2v            [e:]   [cls=E,as=None,tm=prf|imf]
E2 -> E2v            [a:]   [cls=F];[cls=E,as=rc]
E2 -> E2v            [:]    [cls=E,tm=j_i,as=None]
E2v -> E3            [FF]
E3 -> E3_            [_:]   [tm=prf,-neg];[tm=imf];[tm=prf,+neg,vc=[+ps]]
E3 -> E3_            [:]    [tm=prf,+neg,vc=[-ps]];[tm=j_i]
E3_ -> E3v           [e:]   [tm=prf];[tm=imf,vc=[+ps,-cs]];[tm=j_i,vc=[+ps,-cs]]
E3_ -> E3v           [I:]    [tm=imf|j_i,vc=[-ps]];[tm=imf|j_i,vc=[+cs]]
E3v -> end           [FF]
## weak
# ***y
# V1 is 0, unlike other j_i in class E
E1 -> E2_y           [FF]    [tm=j_i,cls=E]
E2_y -> E2v_y        [e:]
E2v_y -> E3_y        [PP]
E3_y -> end          [:y]   [tm=j_i]
E3_ -> end           [e:y]  [tm=prf]
E3_ -> end           [:y]   [tm=imf]
# ***h
E3_ -> end           [a:h]

start -> 

end ->
