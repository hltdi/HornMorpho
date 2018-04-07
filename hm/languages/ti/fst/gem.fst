-> start

# Anything can go at the beginning
start -> mid    [X;V;_]

mid -> mid      [L;B;V;_]
# the X here prevents two geminations in succession
gem -> mid      [X;L;B;V]
nogem -> mid    [_]

mid ->
b ->
c ->
C ->
d ->
f ->
g ->
j ->
k ->
l ->
m ->
n ->
N ->
q ->
r ->
s ->
S ->
t ->
T ->
w ->
x ->
y ->
z ->
Z ->

mid -> b    [b]
b -> nogem  [b]
b -> gem    [_:b]
b -> mid    [X-b;V;_]

mid -> c    [c]
c -> nogem  [c]
c -> gem    [_:c]
c -> mid    [X-c;V;_]

mid -> C    [C]
C -> nogem  [C]
C -> gem    [_:C]
C -> mid    [X-C;V;_]

mid -> d    [d]
d -> nogem  [d]
d -> gem    [_:d]
d -> mid    [X-d;V;_]

mid -> f    [f]
f -> nogem  [f]
f -> gem    [_:f]
f -> mid    [X-f;V;_]

mid -> g    [g]
g -> nogem  [g]
g -> gem    [_:g]
g -> mid    [X-g;V;_]

mid -> j    [j]
j -> nogem  [j]
j -> gem    [_:j]
j -> mid    [X-j;V;_]

mid -> k    [k]
k -> nogem  [k]
k -> gem    [_:k]
k -> mid    [X-k;V;_]

mid -> l    [l]
l -> nogem  [l]
l -> gem    [_:l]
l -> mid    [X-l;V;_]

mid -> m    [m]
m -> nogem  [m]
m -> gem    [_:m]
m -> mid    [X-m;V;_]

mid -> n    [n]
n -> nogem  [n]
n -> gem    [_:n]
n -> mid    [X-n;V;_]

mid -> N    [N]
N -> nogem  [N]
N -> gem    [_:N]
N -> mid    [X-N;V;_]

mid -> q    [q]
q -> nogem  [q]
q -> gem    [_:q]
q -> mid    [X-q;V;_]

mid -> r    [r]
r -> nogem  [r]
r -> gem    [_:r]
r -> mid    [X-r;V;_]

mid -> s    [s]
s -> nogem  [s]
s -> gem    [_:s]
s -> mid    [X-s;V;_]

mid -> S    [S]
SS -> nogem [S]
S -> gem    [_:S]
S -> mid    [X-S;V;_]

mid -> t    [t]
t -> nogem  [t]
t -> gem    [_:t]
t -> mid    [X-t;V;_]

mid -> T    [T]
T -> nogem  [T]
T -> gem    [_:T]
T -> mid    [X-T;V;_]

mid -> w    [w]
w -> nogem  [w]
w -> gem    [_:w]
w -> mid    [X-w;V;_]

mid -> x    [x]
x -> nogem  [x]
x -> gem    [_:x]
x -> mid    [X-x;V;_]

mid -> y    [y]
y -> nogem  [y]
y -> gem    [_:y]
y -> mid    [X-y;V;_]

mid -> z    [z]
z -> nogem  [z]
z -> gem    [_:z]
z -> mid    [X-z;V;_]

mid -> Z    [Z]
Z -> nogem  [Z]
Z -> gem    [_:Z]
Z -> mid    [X-Z;V;_]
