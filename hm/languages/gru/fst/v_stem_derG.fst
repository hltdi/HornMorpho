## Kistane root -> derivational stems
## Features:
##   der: ps, tr, cs, rc, it
## Root types:
##   A: sbr, Aw: s[0]xy AW: s[o]br; B: sb_r, C: sabr, E: sbsb, F: sbasb, ?sbrbr, ?sbrabr

-> start

## derivational prefixes
start -> stem1       [:]    [vc=[-ps,-cs],as=None|it]
start -> stem1       [a:]   [vc=[-ps,+cs],as=None|it]
# te- only when there is no prefix (imperative or non-relative, non-negative prf with no conjunctions)
start -> stem1       <t*:>  [vc=[+ps,-cs]]
# passive with prefix: gemination of following consonant
start -> stem1       <at:>  [vc=[+ps,+cs]]
# optional gemination of C1 (fails for h**)
#start -> stem1       <a/:>  [vc=[+ps,+cs]]

##
# Inkretteto
stem1 -> stem1n      [I:]   [vc=[-ps,-cs]]
# tenqleqqelo
stem1 -> stem1n      [:]    [vc=[+ps]];[vc=[+cs]]
stem1n -> stem       [n]
stem1 -> stem        [:]

### A verbs
## strong
stem -> A1           [RR-h] [cls=A,vc=[-cs]];[cls=A,vc=[-ps]];[cls=A,as=rc,vc=[+cs,+ps]]
stem -> A1w          [CC-h] [cls=AW];[cls=Aw]
A1w -> A1v           [o:]   [tm=prf|imf,as=None]
A1w -> A1v           [u:]   [tm=j_i,as=None];[as=it]
A1w -> A1v           <wa:>  [as=rc]
A1 -> A1v            [e:]   [tm=prf|imf,as=None];[tm=j_i,vc=[+ps]]
A1 -> A1v            [:]    [tm=j_i,vc=[-ps],as=None|it];[as=it]
A1 -> A1v            [a:]   [as=rc]
A1v -> A2            [YY]
# foyyo
A1v -> A2            [y]    [cls=Aw]
A2 -> A2it           [:]    [as=rc|None]
A2 -> A2it           [D:]   [as=it]
A2it -> A2_          [_:]   [tm=prf,-neg];[tm=imf,vc=[+ps]];[tm=prf,+neg,vc=[+ps]];[tm=imf,cls=Aw,vc=[-ps]]
# ** assumption is that gemination is only lost for -ps: alsebere, altseb_er
A2it -> A2_          [:]    [tm=prf,+neg,vc=[-ps]];[tm=imf,cls=A,vc=[-ps]];[tm=imf,cls=AW,vc=[-ps]];[tm=j_i]
# for jussive, ±je feature used to control appearance of V2=e
A2_ -> A2v           [e:]   [tm=prf];[tm=imf|j_i,vc=[+ps]];[tm=j_i,+je];[tm=j_i,sp=2,-je];[tm=j_i,sp=1,sn=2,-je];[tm=j_i,sp=3,sn=1,sg=f,-je];[tm=j_i,+neg,-je]
# we need the vowel for 2sf
A2_ -> A2v           [I:]   [tm=j_i,sp=1,sn=1,-neg,-je,vc=[-ps]];[tm=j_i,sp=3,sn=2,-neg,-je,vc=[-ps]];[tm=j_i,sp=3,sn=1,sg=m,-neg,-je,vc=[-ps]]
A2_ -> A2vi          [:]    [tm=imf,vc=[-ps]]
# ywed_, ywed_E, ywed_x
A2vi -> end          [_:FF] [+dup,op=None|1|2]
# ywedId_
A2vi -> end          [FF]   [-dup];[+dup,op=3]
A2v -> end           [FF]   
## weak
# h**
# ab_ero, tab_ero, [atib_ero], abab_ero, tebab_ero, at_bab_ero; yabr, yt_ab_er, [yatib_r], yababr, yt_bab_er, yat_bab_r
# ebr
stem -> A1h          [:h]   [cls=A,as=None,vc=[-ps]];[cls=A,as=None,vc=[-cs]];[cls=A,as=it]
A1h -> A1h_          [_:]   [tm=imf,vc=[-cs,+ps]];[as=it,vc=[+cs,+ps]];[tm=j_i,vc=[-cs,+ps],sp=0|1|3]
A1h -> A1h_          [:]    [tm=prf,as=None];[tm=prf,as=it,vc=[-cs]];[tm=imf,vc=[-cs,-ps]];[tm=j_i,as=None,sp=2];[tm=j_i,vc=[-ps],sp=0|1|3]
A1h -> A1h_          [t:]   [vc=[+cs,-ps]]
A1h_ -> A1v          [a:]   [tm=imf,as=None];[tm=prf,-neg,as=None];[as=it,vc=[-ps,-cs]];[tm=j_i,as=None,vc=[+ps]]
A1h_ -> A1v          [:]    [as=it,vc=[+ps]]
# alt to a- with iter; prf neg: e-
A1h_ -> A1v          [e:]   [tm=prf,+neg,as=None];[as=it,vc=[+cs,-ps]];[tm=j_i,as=None,vc=[-ps]];[as=it,vc=[-ps,-cs]]
# **h
A2_ -> end           [e:h]  [sp=3,sn=2];[sp=0,op=1|2];[sp=0,op=3,on=1,og=m]
A2_ -> end           [a:h]  [sp=1|2];[sp=3,sn=1]
A2_ -> end           [:h]   [sp=0,op=3,on=2];[sp=0,op=3,on=1,og=f]
# **y
A2_ -> end           [e:y]  [tm=prf]
A2_ -> end           [:y]   [tm=imf|j_i]
# *h*, *w*, *y* verbs don't behave like B verbs with at-
stem -> atA1hwy      [FF]   [cls=A,vc=[+cs,+ps]]
# *h*
A1 -> A2_hit         [:]    [as=None,cls=A]
A1 -> A2_hit         [D:]   [as=it,cls=A]
A2_hit -> A2v        [a:h]  [tm=prf|j_i,vc=[-cs]]
A2_hit -> A2v        [e:h]  [tm=imf];[tm=prf|j_i,vc=[+cs]]
atA1hwy -> A2_hit    [:]    [as=None,cls=A]
atA1hwy -> A2_hit    [D:]   [as=it,cls=A]
# *w*
A1 -> A2w.it         [w]    [as=it,cls=A]
A2w.it -> A2wit      [D:]
A2wit -> A2wit_      [_:]   [tm=prf,-neg];[tm=imf,vc=[+ps]];[tm=prf,+neg,vc=[+ps]]
Aw2it -> A2wit_      [:]    [tm=prf,+neg,vc=[-ps]];[tm=imf,vc=[-ps]];[tm=j_i]
A2wit_ -> A2v        [e:]   [tm=prf];[tm=imf|j_i,vc=[+ps]];[tm=j_i,+je];[tm=j_i,sp=2,-je];[tm=j_i,sp=1,sn=2,-je];[tm=j_i,sp=3,sn=1,sg=f,-je];[tm=j_i,+neg,-je]
# we need the vowel for 2sf
A2wit_ -> A2v        [I:]   [tm=j_i,sp=1,sn=1,-neg,-je,vc=[-ps]];[tm=j_i,sp=3,sn=2,-neg,-je,vc=[-ps]];[tm=j_i,sp=3,sn=1,sg=m,-neg,-je,vc=[-ps]]
A2wit_ -> A2v        [:]    [tm=imf,vc=[-ps]]
A1 -> A2v            [o:w]  [as=None,tm=imf|prf,cls=A]
A1 -> A2v            [u:w]  [as=None,tm=j_i,cls=A]
A1 -> A1wrc          [a:w]  [cls=A,as=rc,vc=[+ps]]
A1wrc -> A2          [w:]
atA1hwy -> A2v       [o:w]  [cls=A,tm=imf|prf]
atA1hwy -> A2v       [u:w]  [cls=A,tm=j_i]
# *y*
stem -> A1y          [X-h]  [cls=A]
A1y -> A2v           [i:y]  [as=None]
# iterative: qiqiTo
A1y -> A2y.it        [Y:]   [as=it]
A2y.it -> A2v        [i:y]
atA1hwy -> A2v       [i:y]  [as=None]

### B verbs
# A and C verbs with at- (vc=[+ps,+cs]) behave like B verbs
stem -> B1           [RR-h] [cls=B];[cls=A,vc=[+ps,+cs]];[cls=C,vc=[+ps,+cs],as=None|it]
B1 -> B1v            [i:]   [tm=prf,-neg,as=None];[tm=imf,as=None]
B1 -> B1v            [e:]   [tm=prf,+neg,as=None];[tm=j_i,as=None]
B1 -> B1v            [a:]   [as=rc]
B1 -> B1v            [:]    [as=it]
B1v -> B2            [YY;w]
# prevent this from happening for A verbs like nyd (no C verbs possible anyway)
B1v -> B2            [y]    [cls=B]
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
# optionally geminate the t of at- before root h
stem -> B1h          [:h]   [cls=B,as=None|it];[cls=A,vc=[+ps,+cs],as=None]
B1h -> B1h_          [_:]   [tm=imf,vc=[-cs,+ps]];[as=it,vc=[+cs,+ps]];[tm=j_i,vc=[-cs,+ps],sp=0|1|3]
B1h -> B1h_          [:]    [tm=prf,as=None];[tm=prf,as=it,vc=[-cs]];[tm=imf,vc=[-cs,-ps]];[tm=imf,as=None,vc=[+cs,+ps]];[tm=j_i,as=None,sp=2];[tm=j_i,vc=[-ps],sp=0|1|3]
B1h_ -> B1v          [i:]   [tm=prf,as=None,-neg];[tm=imf,as=None];[as=it,vc=[-ps,-cs]];[tm=j_i,as=None,vc=[+ps],sp=2]
B1h_ -> B1v          [a:]   [tm=prf,as=None,+neg];[as=it,vc=[-cs,-ps]];[tm=j_i,as=None,vc=[-ps]];[tm=j_i,as=None,vc=[-cs]]
# not sure about at_<e>bab_eTo
B1h_ -> B1v          [e:]   [as=it,vc=[+cs,-ps]];[tm=j_i,as=None,vc=[+cs,+ps]];[as=it,vc=[-ps,-cs]]
B1h_ -> B1v          [:]    [as=it,vc=[+ps]]
# **h
B2_ -> end           [e:h]  [sp=3,sn=2];[sp=0,op=1|2];[sp=0,op=3,on=1,og=m]
B2_ -> end           [a:h]  [sp=1|2];[sp=3,sn=1]
B2_ -> end           [:h]   [sp=0,op=3,on=2];[sp=0,op=3,on=1,og=f]
# **y
B2_ -> end           [e:y]  [tm=prf]
B2_ -> end           [:y]   [tm=imf|j_i]

### C verbs (no as=rc option)
# +ps,+cs in B, but it seem atC1aC2_eC3- is also possible for C verbs with [vc=[+ps,+cs],as=None]
stem -> C1           [RR-h,y]    [cls=C]
C1 -> C1v            [a:]   [as=None]
C1 -> C1v            [:]    [as=it]
C1v -> C2            [RR-h,y]
C2 -> C2it           [D:]   [as=it]
C2 -> C2it           [:]    [as=None]
C2it -> C2_          [_:]   [tm=prf,-neg];[tm=imf]
C2it -> C2_          [:]    [tm=prf,+neg];[tm=j_i]
C2_ -> C2v           [e:]   [tm=prf];[tm=imf,vc=[+ps,-cs]];[tm=j_i,vc=[+ps,-cs]]
C2_ -> C2v           [I:]   [tm=imf|j_i,vc=[-ps]];[tm=imf|j_i,vc=[+cs]]
C2v -> end           [CC]
# **y
C2_ -> end           [e:y]  [tm=prf]
C2_ -> end           [:y]   [tm=imf|j_i]
# **h
C2_ -> end           [e:h]  [sp=3,sn=2];[sp=0,op=1|2];[sp=0,op=3,on=1,og=m]
C2_ -> end           [a:h]  [sp=1|2];[sp=3,sn=1]
C2_ -> end           [:h]   [sp=0,op=3,on=2];[sp=0,op=3,on=1,og=f]

### E/F verbs
# no iterative (so far)
stem -> E1           [RR]    [cls=E,as=None|rc];[cls=F,as=None]
E1 -> E1v            [:]    [tm=prf];[tm=imf];[tm=j_i,cls=F]
E1 -> E1v            [e:]   [tm=j_i,cls=E]
E1v -> E2            [YY]
# -lal(_)a-
E1 -> E2v            [a:h]  [cls=E]
E2 -> E2v            [e:]   [cls=E,as=None,tm=prf|imf]
E2 -> E2v            [a:]   [cls=F];[cls=E,as=rc]
E2 -> E2v            [:]    [cls=E,tm=j_i,as=None]
E2v -> E3            [RR]
E3 -> E3_            [_:]   [tm=prf,-neg];[tm=imf];[tm=prf,+neg,vc=[+ps]]
E3 -> E3_            [:]    [tm=prf,+neg,vc=[-ps]];[tm=j_i]
E3_ -> E3v           [e:]   [tm=prf];[tm=imf,vc=[+ps,-cs]];[tm=j_i,vc=[+ps,-cs]]
E3_ -> E3v           [I:]   [tm=imf|j_i,vc=[-ps]];[tm=imf|j_i,vc=[+cs]]
E3v -> end           [FF]
## weak
# ***y
# V1 is 0, unlike other j_i in class E
E1 -> E2_y           [FF]    [tm=j_i,cls=E]
E2_y -> E2v_y        [e:]
E2v_y -> E3_y        [PP]
E3_y -> end          [:y]
E3_ -> end           [e:y]  [tm=prf]
E3_ -> end           [:y]   [tm=imf]
# ***h
E3_ -> end           [e:h]  [sp=3,sn=2];[sp=0,op=1|2];[sp=0,op=3,on=1,og=m]
E3_ -> end           [a:h]  [sp=1|2];[sp=3,sn=1]
E3_ -> end           [:h]   [sp=0,op=3,on=2];[sp=0,op=3,on=1,og=f]

start -> 

end ->
