# Realize coda r as n in certain j_i environments

-> start

# never happens with **h?
start -> fin      [a]

# (*)**y, -tr
start -> y       [y]
y -> e         [e]
start -> e       [e;E]
e -> Ce        [X-m]
# m in root prevents r->n
e -> fin       [m]
# we need V for qere and qeye
Ce -> fin      [X-r;n:r;V]

# **y, +tr
start -> ^       [^]
^ -> ^C        [KK;DD]
^C -> fin      [n:r;X-r;:]
# final palatal or labialized consonant (does mW prevent r->n?)
start -> labpal  [PP-y;UU]
labpal -> fin  [n:r;X-r;V;:]

# other than **y and **h
start -> X       [ZZ-m]
# m in root prevents r->n: ye=gerdm
start -> fin     [m]
# ye=nKb, ye=dengr
X -> XV        [V;:]
XV -> XVC      [X]
# penultimate coda
XVC -> fin     [X-r;V;:]
XVC -> XVCn    [n:r]
XVCn -> end    [:]
# must be a vowel or nothing for r to be coda, as in =d<e>ngr
XVCn -> fin    [V]
# r not a coda
XVC -> XVCr    [r]
XVCr -> fin    [X]

end ->
fin ->
# ye=ez=o
XV ->
Ce ->
fin -> fin      [X;V;^;@]
