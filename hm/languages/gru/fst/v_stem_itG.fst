# CaC reduplication for Kistane
# Assumes it can only happen once in a word
# For generation, assume only CaC, not Cec

-> start

start -> start  [X;V;/;_]

start -> b   [b]
b -> ba      [a:D;i:Y]
ba -> end    [b:]

start -> c   [c]
c -> ca      [a:D;i:Y]
ca -> end    [c:]

start -> C   [C]
C -> Ca      [a:D;i:Y]
Ca -> end  [C:]

start -> d   [d]
d -> da      [a:D;i:Y]
da -> end  [d:]

start -> f   [f]
f -> fa      [a:D;i:Y]
fa -> end  [f:]

start -> g   [g]
g -> ga      [a:D;i:Y]
ga -> end  [g:]

start -> gW  [gW]
gW -> gWa    [a:D]
gWa -> end [gW:]

start -> j   [j]
j -> ja      [a:D;i:Y]
ja -> end  [j:]

start -> k   [k]
k -> ka      [a:D;i:Y]
ka -> end  [k:]

start -> kW  [kW]
kW -> kWa    [a:D]
kWa -> end [kW:]

start -> l   [l]
l -> la      [a:D;i:Y]
la -> end  [l:]

start -> m   [m]
m -> ma      [a:D;i:Y]
ma -> end  [m:]

start -> n   [n]
n -> na      [a:D;i:Y]
na -> end  [n:]

start -> N   [N]
N -> Na      [a:D;i:Y]
Na -> end  [N:]

start -> q   [q]
q -> qa      [a:D;i:Y]
qa -> end  [q:]

start -> qW  [qW]
qW -> qWa    [a:D]
qWa -> end [qW:]

start -> r   [r]
r -> ra      [a:D;i:Y]
ra -> end  [r:]

start -> s   [s]
s -> sa      [a:D;i:Y]
sa -> end  [s:]

start -> S   [S]
S -> Sa      [a:D;i:Y]
Sa -> end  [S:]

start -> t   [t]
t -> ta      [a:D;i:Y]
ta -> end  [t:]

start -> T   [T]
T -> Ta      [a:D;i:Y]
Ta -> end  [T:]

start -> w   [w]
w -> wa      [a:D;i:Y]
wa -> end  [w:]

start -> x   [x]
x -> xa      [a:D;i:Y]
xa -> end  [x:]

start -> y   [y]
y -> ya      [a:D;i:Y]
ya -> end  [y:]

start -> z   [z]
z -> za      [a:D;i:Y]
za -> end  [z:]

start -> Z   [Z]
Z -> Za      [a:D;i:Y]
Za -> end  [Z:]

start -> hW  [hW]
hW -> hWa    [a:D]
hWa -> end   [hW:]

end -> end  [X;V;_;/]

start ->
end ->
