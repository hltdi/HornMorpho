### Filter out impossible roots of the form
### X|X

-> start

start -> mid  [X;a;_]  # but not |

mid -> mid    [X;a;_]

mid ->

# No duplicates of the form X|X

start -> b   [b;bW]
b -> b|      [|]
b| -> mid    [X-b,bW]

start -> c   [c;cW]
c -> c|      [|]
c| -> mid    [X-c,cW]

start -> C   [C;CW]
C -> C|      [|]
C| -> mid    [X-C,CW]

start -> d   [d]
d -> d|      [|]
d| -> mid    [X-d,t,T,tW,TW]

start -> f   [f;fW]
f -> f|      [|]
f| -> mid    [X-f,fW]

start -> g   [g;gW]
g -> g|      [|]
g| -> mid    [X-g,gW,k,kW]

start -> j   [j]
j -> j|      [|]
j| -> mid    [X-j]

start -> k   [k;kW]
k -> k|      [|]
k| -> mid    [X-k,kW,g,gW]

start -> l   [l]
l -> l|      [|]
l| -> mid    [X-l]

start -> m   [m;mW]
m -> m|      [|]
m| -> mid    [X-m,mW]

start -> n   [n]
n -> n|      [|]
n| -> mid    [X-n]

start -> q   [q;qW]
q -> q|      [|]
q| -> mid    [X-q,qW,k,kW]

start -> r   [r]
r -> r|      [|]
r| -> mid    [X-r]

start -> s   [s;sW]
s -> s|      [|]
s| -> mid    [X-s,sW,z,Z,S,x]

start -> S   [S;SW]
S -> S|      [|]
S| -> mid    [X-S,SW,s,z,Z,x]

start -> t   [t;tW]
t -> t|      [|]
t| -> mid    [X-t,tW,d,T,TW]

start -> T   [T;TW]
T -> T|      [|]
T| -> mid    [X-T,TW,d,t,tW]

start -> w   [w]
w -> w|      [|]
w| -> mid    [X-w]

start -> x   [x;xW]
x -> x|      [|]
x| -> mid    [X-x,xW,s,z,Z,S]

start -> z   [z;zW]
z -> z|      [|]
z| -> mid    [X-z,zW,s,x,Z,S]

start -> Z   [Z;ZW]
Z -> Z|      [|]
Z| -> mid    [X-Z,ZW,s,x,z,S]
