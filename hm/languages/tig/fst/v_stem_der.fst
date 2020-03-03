## Tigre root -> derivational stems
## Features:
##   der: ps, tr, cs, rc, it
## Root types:

-> start

## derivational prefixes
# causative
start -> pre_cs      <'e:>   [vc=[+cs]]
pre_cs -> stem        [t:]   [vc=[+ps]]
pre_cs -> stem        [:]    [vc=[-ps]]
# non_causative
start -> pre_nocs     [:]    [vc=[-cs]]
pre_nocs -> stem      <tA:>  [vc=[+ps]]
pre_nocs -> stem      [:]    [vc=[-ps]]

#### A verbs
### strong
# 'etteqtele
stem -> A0          <_e:>   [vc=[+ps,+cs]]
stem -> A0           [:]    [vc=[-ps]];[vc=[-cs]]
A0 -> A1             [RR]   [cls=A]
A1 -> A1v            [e:]   [tm=imf,as=None,vc=[-cs]];[tm=imf,as=None,vc=[-ps]];[tm=j_i,as=None,vc=[+ps]];[tm=prf,as=None,vc=[-cs]];[as=it]
A1 -> A1v            [:]    [tm=j_i,vc=[-ps],as=None];[tm=prf,as=None,vc=[+cs]];[tm=imf,as=None,vc=[+cs,+ps]]
A1 -> A1v            [a:]   [as=rc]
A1v -> A2            [RR]
A2 -> A2it           [:]    [as=rc|None]
A2 -> A2it           [D:]   [as=it]
# separate t- from 0-, e-, ette-
A2it -> A2_          [_:]   [vc=[+ps,-cs],as=None|rc]
# never geminate in these cases
A2it -> A2_          [:]    [vc=[+cs]];[as=it];[tm=j_i|prf,vc=[-ps]]
# imperfective is complex...
A2it -> A2i          [:]    [tm=imf,vc=[-ps],as=None|rc]
# ... gemination when there are no subject suffixes (1, 2sm, 3s) and no 1 or 2 object suffixes; always geminate in imp with 3 obj, unless 2|3pf
A2i -> A2_           [_:]   [sp=1,op=None|3];[sp=2,sn=1,sg=m,op=None|3];[sp=3,sn=1,op=None|3];[op=3,sp=2|3,sn=2,sg=m];[op=3,sp=2,sn=1,sg=f];[vc=[+ps]]
# ... unless there is 3 obj with anything but 2|3pf, don't geminate before other objects, in 2sf, or 2,3p
A2i -> A2_           [:]     [op=1|2];[sp=2,sn=1,sg=f,op=None];[sp=2|3,sn=2,op=None];[sp=2|3,sn=2,sg=f,op=3]
# perfective: V2 - C3
# e dropped in prf,-ps with -V suffix
A2_ -> A2_p          [:]    [tm=prf]
A2_p -> A2p0         [:]    [sp=3,vc=[-ps]]
# den_e
A2p0 -> A2v          [:]    [-dup]
A2p0 -> end          [_:RR] [+dup]
A2_p -> A2v          [e:]   [sp=1|2];[vc=[+ps]];[vc=[+cs]]
# imperfective and jussive: V2 - C3
# V2: e (E, o)
A2_ -> A2v           [*:]   [tm=j_i,vc=[-cs]];[tm=imf,vc=[+ps,-cs]]
# V2: 0 (i, u)
A2_ -> A2i0          [:]    [tm=imf,vc=[-ps]];[tm=imf,vc=[+cs]];[tm=j_i,vc=[+cs]]
# -dup case and +dup with no subject suffix and no object or with vowel change and 3s objects
A2i0 -> A2v          [!:]   [-dup];[+dup,sp=1,op=None];[+dup,sp=3,sn=1,op=None];[+dup,sp=2,sn=1,sg=m,op=None];[+dup,sp=2|3,sn=2,sg=m,op=3];[+dup,sp=2,sn=1,sg=f,op=3]
# +dup case: geminate if there is a subject suffix and no object suffix; and with all objects unless the vowel changes (0->i (2sf), 0->u (23pm))
A2i0 -> end          [_:RR] [+dup,sp=2,sn=1,sg=f,op=None];[+dup,sp=2|3,sn=2,op=None];[+dup,op=1|2];[+dup,sp=1,op=3];[+dup,sp=3,sn=1,op=3];[+dup,sp=2|3,sn=2,sg=f,op=3];[+dup,sp=2,sn=1,sg=m,op=3]
A2v -> end           [RR]   
### weak
## L**
# only et- and t- possible; (no e- or ette_)
stem -> A1L          [LL]   [cls=A,vc=[-ps,-cs]];[cls=A,vc=[+cs,+ps]];[cls=A,vc=[+ps,-cs]]
A1L -> A1v           [e:]   [tm=prf,as=None|it];[tm=imf,as=None|it];[tm=j_i,vc=[+ps]]
A1L -> A1v           [:]    [tm=j_i,as=None|it,vc=[-ps],sp=2];[tm=j_i,as=None|it,vc=[-ps],sp=3];[tm=j_i,as=None|it,vc=[-ps],sp=1,sn=2]
# HiSeb
A1L -> A1v           [i:]   [tm=j_i,as=None|it,vc=[-ps],sp=1,sn=1]
## w/y**
stem -> A1Yip        [w;y]   [cls=A,tm=prf|imf];[cls=A,tm=j_i,vc=[+ps]];[cls=A,tm=j_i,vc=[+cs]]
stem -> A1Yj         [:w;:y] [cls=A,tm=j_i,vc=[-ps,-cs]]
A1Yj -> A1v          [i:]
A1Yip -> A1v         [e:]   [tm=imf,as=None,vc=[-cs]];[tm=imf,as=None,vc=[-ps]];[tm=j_i,vc=[+ps]];[tm=prf,vc=[-cs]]
A1Yip -> A1v         [:]    [as=it];[tm=prf,vc=[+cs]];[tm=imf,vc=[+cs,+ps]]
## *L*
# we`ele; wL* doesn't behave like other w**
stem -> A1L          [RR;w] [cls=A]
A1L -> A1v.L         [e:]   [tm=prf,as=None];[tm=j_i,as=None,sp=2]
A1L -> A1v.L         [:]    [tm=imf,as=None];[tm=j_i,as=None,sp=1|3]
A1v.L -> A2L         [LL]
A2L -> A2v           [*:]   [tm=prf];[tm=j_i]
A2L -> A2v           [!:]   [tm=imf]
# *LY: r'y (handle as irregular)
#A2L -> A2LvY         [e:]    [tm=j_i,vc=[-cs]];[tm=imf,vc=[+ps,-cs]];[tm=prf,vc=[+ps]];[tm=prf,vc=[+cs]];[tm=prf,vc=[-ps,-cs],sp=1|2];[tm=prf,vc=[-ps,-cs],sp=3,sn=1,sg=f]
#A2L -> A2LvY         [:]     [tm=prf,vc=[-ps,-cs],sp=3,sn=1,sg=m];[tm=prf,vc=[-ps,-cs],sp=3,sn=2];[tm=imf,vc=[-ps]];[tm=imf,vc=[+cs]];[tm=j_i,vc=[+cs]]
## prf
#A2LvY -> A2LYp       [:]    [tm=prf]
#A2LYp -> end         [Y:y]  [sp=1|2];[sp=3,sn=1,sg=f]
#A2LYp -> end         [:y]   [sp=3,sn=2];[sp=3,sn=1,sg=m]
## imf/jus
#A2LvY -> A2LYi       [:]    [tm=imf|j_i]
#A2LYi -> end         [Y:y]  [op=None|1|2];[sp=1,op=3];[sp=2,sn=1,sg=m,op=3];[sp=2|3,sn=2,sg=f,op=3];[sp=3,sn=1,op=3]
#A2LYi -> end         [i:y]  [sp=2,sn=1,sg=f,op=3]
#A2LYi -> end         [w:y]  [sp=2|3,sn=2,sg=m,op=3]
## *w*, *y*
# (still need to handle as=it)
stem -> A1.Y         [RR;LL]  [cls=A]
# prf
# gEde, dore, HExe, erEme
A1.Y -> A2Yv.        [:w;:y]    [tm=prf,sp=1|2,as=None,vc=[-ps]]
A1.Y -> A2Yv.        [o:w;E:y]  [tm=prf,sp=3,as=None,vc=[-ps]]
# jus
A1.Y -> A2Yv.        [u:w;i:y]  [tm=j_i,as=None,vc=[-ps]]
# +cs,+ps (ette-)
A1.Y -> A2Y.et       [YY]       [vc=[+ps,+cs],as=None]
A2Y.et -> A2Yv.      [e:]       [tm=prf]
A2Y.et -> A2Yv.      [:]        [tm=imf|j_i]
# impf and +ps
A1.Y -> A1v.Y        [e:]    [tm=imf,as=None];[tm=prf,vc=[+ps,-cs]];[tm=j_i,as=None,vc=[+ps,-cs]]
# never geminate Y
A1v.Y -> A2Y.        [YY]
A2Y. -> A2Yv.        [e:]    [vc=[+ps]]
A2Y. -> A2Yv.        [:]     [vc=[-ps]]
A2Yv. -> end         [RR]
# special case of *YL: ba'a, qaHa; lbey', lbye'
A1.Y -> A2vY.L       [e:YY]  [tm=prf]
A1.Y -> A2v.YLi      [e:]    [tm=imf]
A2v.YLi -> A2vY.L    [y:YY]
# jussive: also an alternative without explicit y
A1.Y -> A2v.YLj      [y:YY]  [tm=j_i]
A2v.YLj -> A2vY.L    [e:]
A2vY.L -> A3L        [LL]
## **L
# geminate all imperfective forms, except causative
A2it -> A2_L         [_:]   [tm=imf,vc=[-cs]];[tm=imf,vc=[+cs,-ps]];[tm=prf,vc=[+ps,-cs]];[tm=j_i,vc=[+ps,-cs]]
A2it -> A2_L         [:]    [tm=prf,vc=[-ps]];[tm=prf,vc=[+cs]];[tm=imf,vc=[+cs,+ps]];[tm=j_i,vc=[-ps]];[tm=j_i,vc=[+cs]]
# V2=0 in perfective for all persons
# unlike **C, stem vowels don't change for 2sf and 23pm to i/u, E/o
A2_L -> A2vL         [e:]   [tm=imf|j_i,vc=[+ps,-cs]];[tm=j_i,sp=1,vc=[-cs],op=None];[tm=j_i,sp=2,sn=1,sg=m,vc=[-cs],op=None];[tm=j_i,sp=3,sn=1,vc=[-cs],op=None]
A2_L -> A2vL         [:]    [tm=prf];[tm=imf,vc=[-ps]];[tm=imf|j_i,vc=[+cs]];[tm=j_i,sp=2,sn=1,sg=f,vc=[-cs]];[tm=j_i,sp=2|3,sn=2,vc=[-cs]];[tm=j_i,op=1|2|3]
A2vL -> A3L          [LL]
A3L -> A3Lp          [:]    [tm=prf]
A3L -> A3Li          [:]    [tm=imf|j_i]
# sem`eko
A3Lp -> end          [e:]   [sp=1|2]
A3Lp -> end          [:]    [sp=3]
A3Li -> end          [:]    [sp=1];[sp=3,sn=1];[sp=2|3,sn=2,sg=f];[sp=2,sn=1,sg=m];[sp=2,sn=1,sg=f,op=None|1|2];[sp=2|3,sn=2,sg=m,op=None|1|2]
# need to explicitly add the subject suffixes for 3p obj and 2sf, 23pm subj
A3Li -> end          [i:]   [sp=2,sn=1,sg=f,op=3]
A3Li -> end          [w:]   [sp=2|3,sn=2,sg=m,op=3]
## **y
# geminate all imperfective except 23pf and causative
A2it -> A2_Y         [_:]   [tm=imf,vc=[-cs],sp=1];[tm=imf,vc=[-cs],sn=1];[tm=imf,vc=[-cs],sp=2|3,sn=2,sg=m];[tm=imf,vc=[-ps,+cs],sp=1];[tm=imf,vc=[-ps,+cs],sn=1];[tm=imf,vc=[-ps,+cs],sp=2|3,sn=2,sg=m];[tm=imf|prf|j_i,vc=[+ps,-cs]]
# unless there is 3 obj with anything but 2|3pf, don't geminate before other objects, in 2sf, or 2,3p
A2it -> A2_Y         [:]    [tm=j_i,vc=[-ps]];[tm=j_i,vc=[+cs]];[tm=prf,vc=[-ps]];[tm=prf,vc=[+cs]];[tm=imf,vc=[+cs,+ps]];[tm=imf,vc=[-cs],sp=2|3,sn=2,sg=f];[tm=imf,vc=[-ps,+cs],sp=2|3,sn=2,sg=f]
A2_Y -> A2vY         [e:]    [tm=j_i,vc=[-cs]];[tm=imf,vc=[+ps,-cs]];[tm=prf,vc=[+ps]];[tm=prf,vc=[+cs]];[tm=prf,vc=[-ps,-cs],sp=1|2];[tm=prf,vc=[-ps,-cs],sp=3,sn=1,sg=f]
A2_Y -> A2vY         [:]     [tm=prf,vc=[-ps,-cs],sp=3,sn=1,sg=m];[tm=prf,vc=[-ps,-cs],sp=3,sn=2];[tm=imf,vc=[-ps]];[tm=imf,vc=[+cs]];[tm=j_i,vc=[+cs]]
# perf final vowel
A2vY -> A2vYp        [:]    [tm=prf]
# delete the y; xeqe, xeqew, xeqeye
A2vYp -> end         [:y]   [sp=3,sn=2];[sp=3,sn=1,sg=m]
# realize the y as Y; xeqEt, xeqEko,
A2vYp -> end         [Y:y]  [sp=1|2];[sp=3,sn=1,sg=f]
# imperf/juss final vowel
A2vY -> A2vYi        [:]    [tm=imf|j_i]
# realize the y as Y; lxeqqE, txeqqi, txeqqu, txeqye, xqE, xqey, xqew, xqeye; how this is actually realized is in Y.fst
A2vYi -> end         [Y:y]  [op=None|1|2];[sp=1,op=3];[sp=2,sn=1,sg=m,op=3];[sp=2|3,sn=2,sg=f,op=3];[sp=3,sn=1,op=3]
# special 3 obj cases: 2sf, 23pm, because the suffix is internal for weak roots
A2vYi -> end         [i:y]  [sp=2,sn=1,sg=f,op=3]
A2vYi -> end         [w:y]  [sp=2|3,sn=2,sg=m,op=3]

#### B verbs
### weak
stem -> B1           [X]    [cls=B]
B1 -> B1v            [e:]   [as=None]
B1 -> B1v            [a:]   [as=rc]
B1v -> B2            [RR]
# according to Raz, there should be no iter forms with B
#B2 -> B2it           [D:]   [as=it]
#B2 -> B2it           [:]    [as=None|rc]
#B2it -> B2_          [:]    [as=it]
# geminate C2 except for imp/jus -ps with suffixes
B2 -> B2_            [_:]    [tm=prf];[vc=[+ps,-cs]]
B2 -> B2i            [:]     [tm=imf|j_i,vc=[-ps]];[tm=imf|j_i,vc=[+cs]]
# imp/jus: geminate if +ps, no suffix or 3p object with all but 23pf
B2i -> B2_           [_:]   [sp=1,op=None|3];[sp=2,sn=1,sg=m,op=None|3];[sp=3,sn=1,op=None|3];[op=3,sp=2|3,sn=1,sg=m];[op=3,sp=2,sn=1,sg=f]
B2i -> B2_           [:]    [op=1|2];[sp=2,sn=1,sg=f,op=None];[sp=2|3,sn=2,op=None];[sp=2|3,sn=2,sg=f,op=3]
# final vowel in imprf and jus depends on object suffix
B2_ -> B2v           [e:]   [tm=prf]
B2_ -> B2eij         [*:]   [tm=imf|j_i,vc=[+ps,-cs]]
B2_ -> B20ij         [!:]   [tm=imf|j_i,vc=[-ps]];[tm=imf|j_i,vc=[+cs]]
# in *CC verbs (+dup) gemination before objects: 'azzakkum
B2eij -> B2v         [:]
B20ij -> B2v         [:]    [-dup];[+dup,op=None]
B20ij -> end         [:RR]  [+dup,op=1|2|3]
B2v -> end           [RR]
### strong
# *w*, *y*
B1v -> B2Y           [YY]
B2Y -> B2Yit         [D:]   [as=it]
B2Y -> B2Yit         [:]    [as=None|rc]
# don't geminate w, y
B2Yit -> B2_         [:]
# **L
# beyond here, the same as for A
B2_ -> A2vL         [e:]    [tm=prf,sp=3];[tm=j_i,vc=[+ps,-cs]];[tm=imf,vc=[+ps,-cs]]
B2_ -> A2vL         [:]     [tm=prf,sp=1|2];[tm=imf|j_i,vc=[-ps]];[tm=imf|j_i,vc=[+cs]]
# **y
# beyond here the same as for A
B2_ -> A2vY          [e:]    [tm=imf|j_i,vc=[+ps,-cs]];[tm=prf,sn=1|2];[tm=prf,sp=3,sn=1,sg=f]
B2_ -> A2vY          [:]     [tm=imf|j_i,vc=[-ps]];[tm=imf|j_i,vc=[+cs]];[tm=prf,sp=3,sn=1,sg=m];[tm=prf,sp=3,sn=2]

#### C verbs (no as=rc option)
### weak
# +ps,+cs in B, but it seem atC1aC2_eC3- is also possible for C verbs with [vc=[+ps,+cs],as=None]
stem -> C1           [RR]   [cls=C]
C1 -> C1v            [a:]   [as=None]
C1 -> C1v            [e:]   [as=it]
C1v -> C2            [RR]
C2 -> C2it           [D:]   [as=it]
C2 -> C2it           [:]    [as=None]
C2it -> C2v          [e:]   [tm=prf]
C2it -> C2v          [*:]   [tm=imf,vc=[+ps,-cs]];[tm=j_i,vc=[+ps,-cs]]
C2it -> C20          [:]    [tm=imf|j_i,vc=[-ps]];[tm=imf|j_i,vc=[+cs]]
# final L is the same as for A
C2it -> A2_L         [:]
# included for completeness; there may not be any of these
C2it -> A2_Y         [:]
C20 -> C2v           [!:]   [-dup]
C20 -> end           [_:RR] [+dup]
C2v -> end           [RR]
### strong

### E/F verbs
# no iterative (so far)
# also 'enbete, wetwete
stem -> E1           [RR;LL;w] [cls=E,as=None|rc];[cls=F,as=None];[cls=Ew,as=None]
E1 -> E1v            [e:]   [cls=E|F]
# gEge
E1 -> E2v            [E:y]  [cls=E]
E1 -> E2v            [o:]   [cls=Ew]
# newne
E1v -> E2            [RR;w] [cls=E]
E1v -> E2L           [LL]
E2L -> E2v           [e:]   [cls=E,as=None]
E2 -> E2v            [:]    [cls=E,as=None]
E2 -> E2v            [a:]   [cls=F];[cls=E,as=rc]
# wetwete
E2v -> E3            [RR;w]
E3 -> E3v            [e:]  [tm=prf]
E3 -> E3v            [*:]  [tm=imf|j_i,vc=[+ps,-cs]]
E3 -> E3v            [!:]  [tm=imf|j_i,vc=[-ps]];[tm=imf|j_i,vc=[+cs]]
# ***L
E3 -> A2_L           [:]
# ***Y
E3 -> A2_Y           [:]
# no gemination of **CC?
#E30 -> E3v           [!:]  [-dup]
#E30 -> end           [_:RR] [+dup]
E3v -> end           [RR]
## strong
# L*** (like weak)
# *L** (almost like weak, see above)
# ***L (like A, see above)
# ***Y (like A, see above)

### G/H verbs, 5 stem consonants
# no iterative (so far)
stem -> Gpre1        <t_:>  [vc=[+cs,-ps]]
stem -> Gpre1        [:]    [vc=[-cs,-ps]]
Gpre1 -> G0          [e:]   [cls=G,as=None];[cls=H,as=None]
G0 -> G1             [n;s]
G1 -> G2             [RR]
G2 -> G2v            [e:]   
G2v -> G3            [RR]
G3 -> G3v            [:]    [cls=G]
G3 -> G3v            [a:]   [cls=H]
G3v -> G4            [RR]
G4 -> G4v            [e:]   [tm=prf]
#G4 -> G40            [:]    [tm=imf|j_i]
G4 -> G4v            [!:]    [tm=imf|j_i]
#G40 -> end           [_:RR] [+dup]
G4v -> end           [RR]
## weak
# ***y
# ***h

end ->
