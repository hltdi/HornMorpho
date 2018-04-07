### Filter out impossible roots with repeated consonants
### X(a,0)X

-> start

end ->

start -> C.  [X]
C. -> C|.    [|]
C|. -> mid   [X]
C. -> mid    [a;:]

# CCC, CaCC, CC_C verbs
mid -> .C     [X]
.C -> .C      [_]
.C -> end     [X/B]

# C|CCCC, C|CCaCC, CCCC, CCaCC verbs (C2!=C3)
mid -> b      [b]
b -> b_mid    [a;:]
b_mid -> .C   [X-b]

mid -> bW     [bW]
bW -> bW_mid  [a;:]
bW_mid -> .C  [X-bW]

mid   -> c   [c]
c -> c_mid   [a;:]
c_mid -> .C  [X-c]

mid   -> cW  [cW]
cW -> cW_mid [a;:]
cW_mid -> .C [X-cW]

mid   -> C   [C]
C -> C_mid   [a;:]
C_mid -> .C  [X-C]

mid   -> CW  [CW]
CW -> CW_mid [a;:]
CW_mid -> .C [X-CW]

mid   -> d   [d]
d -> d_mid   [a;:]
d_mid -> .C  [X-d]

mid   -> f   [f]
f -> f_mid   [a;:]
f_mid -> .C  [X-f]

mid   -> fW  [fW]
fW -> fW_mid [a;:]
fW_mid -> .C [X-fW]

mid   -> g   [g]
g -> g_mid   [a;:]
g_mid -> .C  [X-g]

mid   -> gW  [gW]
gW -> gW_mid [a;:]
gW_mid -> .C [X-gW]

mid   -> j   [j]
j -> j_mid   [a;:]
j_mid -> .C  [X-j]

mid   -> k   [k]
k -> k_mid   [a;:]
k_mid -> .C  [X-k]

mid   -> kW  [kW]
kW -> kW_mid [a;:]
kW_mid -> .C [X-kW]

mid   -> l   [l]
l -> l_mid   [a;:]
l_mid -> .C  [X-l]

mid   -> m   [m]
m -> m_mid   [a;:]
m_mid -> .C  [X-m]

mid   -> mW  [mW]
mW -> mW_mid [a;:]
mW_mid -> .C [X-mW]

mid   -> n   [n]
n -> n_mid   [a;:]
n_mid -> .C  [X-n]

mid   -> q   [q]
q -> q_mid   [a;:]
q_mid -> .C  [X-q]

mid   -> qW  [qW]
qW -> qW_mid [a;:]
qW_mid -> .C [X-qW]

mid   -> r   [r]
r -> r_mid   [a;:]
r_mid -> .C  [X-r]

mid   -> s   [s;sW]
s -> s_mid   [a;:]
s_mid -> .C  [X-s,sW]

mid   -> S   [S;SW]
S -> S_mid   [a;:]
S_mid -> .C  [X-S,SW]

mid   -> t   [t]
t -> t_mid   [a;:]
t_mid -> .C  [X-t]

mid   -> tW  [tW]
tW -> tW_mid [a;:]
tW_mid -> .C [X-tW]

mid   -> T   [T]
T -> T_mid   [a;:]
T_mid -> .C  [X-T]

mid   -> TW  [TW]
TW -> TW_mid [a;:]
TW_mid -> .C [X-TW]

mid   -> w   [w]
w -> w_mid   [a;:]
w_mid -> .C  [X-w]

mid   -> x   [x]
x -> x_mid   [a;:]
x_mid -> .C  [X-x]

mid   -> xW  [xW]
xW -> xW_mid [a;:]
xW_mid -> .C [X-xW]

mid   -> z   [z]
z -> z_mid   [a;:]
z_mid -> .C  [X-z]

mid   -> zW  [zW]
zW -> zW_mid [a;:]
zW_mid -> .C [X-zW]

mid   -> Z   [Z]
Z -> Z_mid   [a;:]
Z_mid -> .C  [X-Z]

mid   -> ZW  [ZW]
ZW -> ZW_mid [a;:]
ZW_mid -> .C [X-ZW]

mid   -> h   [h]
h -> h_mid   [a;:]
h_mid -> .C  [X-h]

mid   -> hW  [hW]
hW -> hW_mid [a;:]
hW_mid -> .C [X-hW]

mid   -> H   [H]
H -> H_mid   [a;:]
H_mid -> .C  [X-H]

mid   -> HW  [HW]
HW -> HW_mid [a;:]
HW_mid -> .C [X-HW]
