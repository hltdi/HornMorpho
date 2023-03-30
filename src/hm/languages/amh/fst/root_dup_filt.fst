### Filter out impossible roots with repeated consonants
### X(a,0)X

-> start

end ->

start -> C.  [X]
# needed for CCCCC
C. -> CC.    [X]
C. -> C|.    [|]
C|. -> mid   [X]
C. -> mid    [a;:]
CC. -> mid   [:]

# CCC, CaCC, CC_C verbs
mid -> .C     [X]
.C -> .C      [_]
.C -> end     [X/B]

# CCCCC, C|CCCC, C|CCaCC, CCCC, CCaCC verbs (C2!=C3)
mid -> b      [b;bW]
b -> b_mid    [a;:]
b_mid -> .C   [X-b,bW]

mid   -> c   [c;cW]
c -> c_mid   [a;:]
c_mid -> .C  [X-c,cW]

mid   -> C   [C;CW]
C -> C_mid   [a;:]
C_mid -> .C  [X-C,CW]

mid   -> d   [d]
d -> d_mid   [a;:]
d_mid -> .C  [X-d]

mid   -> f   [f;fW]
f -> f_mid   [a;:]
f_mid -> .C  [X-f,fW]

mid   -> g   [g;gW]
g -> g_mid   [a;:]
g_mid -> .C  [X-g,gW]

mid   -> j   [j]
j -> j_mid   [a;:]
j_mid -> .C  [X-j]

mid   -> k   [k;kW]
k -> k_mid   [a;:]
k_mid -> .C  [X-k,kW]

mid   -> l   [l]
l -> l_mid   [a;:]
l_mid -> .C  [X-l]

mid   -> m   [m;mW]
m -> m_mid   [a;:]
m_mid -> .C  [X-m,mW]

mid   -> n   [n]
n -> n_mid   [a;:]
n_mid -> .C  [X-n]

mid   -> N   [N]
N -> N_mid   [a;:]
N_mid -> .C  [X-N]

mid   -> q   [q;qW]
q -> q_mid   [a;:]
q_mid -> .C  [X-q,qW]

mid   -> r   [r]
r -> r_mid   [a;:]
r_mid -> .C  [X-r]

mid   -> s   [s;sW]
s -> s_mid   [a;:]
s_mid -> .C  [X-s,sW]

mid   -> S   [S;SW]
S -> S_mid   [a;:]
S_mid -> .C  [X-S,SW]

mid   -> t   [t;tW]
t -> t_mid   [a;:]
t_mid -> .C  [X-t,tW]

mid   -> T   [T;TW]
T -> T_mid   [a;:]
T_mid -> .C  [X-T,TW]

mid   -> w   [w]
w -> w_mid   [a;:]
w_mid -> .C  [X-w]

mid   -> x   [x;xW]
x -> x_mid   [a;:]
x_mid -> .C  [X-x,xW]

mid   -> z   [z;zW]
z -> z_mid   [a;:]
z_mid -> .C  [X-z,zW]

mid   -> Z   [Z;ZW]
Z -> Z_mid   [a;:]
Z_mid -> .C  [X-Z,ZW]
