# CaC reduplication for Tigre
# Assumes it can only happen once in a word

-> start

start -> start  [X-D;V;/;_]

start -> b   [b]
b -> ba      [a:D]
ba -> end    [b:]

start -> c   [c]
c -> ca      [a:D]
ca -> end    [c:]

start -> C   [C]
C -> Ca      [a:D]
Ca -> end  [C:]

start -> d   [d]
d -> da      [a:D]
da -> end  [d:]

start -> f   [f]
f -> fa      [a:D]
fa -> end  [f:]

start -> g   [g]
g -> ga      [a:D]
ga -> end  [g:]

start -> j   [j]
j -> ja      [a:D]
ja -> end  [j:]

start -> k   [k]
k -> ka      [a:D]
ka -> end  [k:]

start -> l   [l]
l -> la      [a:D]
la -> end  [l:]

start -> m   [m]
m -> ma      [a:D]
ma -> end  [m:]

start -> n   [n]
n -> na      [a:D]
na -> end  [n:]

start -> N   [N]
N -> Na      [a:D]
Na -> end  [N:]

start -> q   [q]
q -> qa      [a:D]
qa -> end  [q:]

start -> r   [r]
r -> ra      [a:D]
ra -> end  [r:]

start -> s   [s]
s -> sa      [a:D]
sa -> end  [s:]

start -> S   [S]
S -> Sa      [a:D]
Sa -> end  [S:]

start -> t   [t]
t -> ta      [a:D]
ta -> end  [t:]

start -> T   [T]
T -> Ta      [a:D]
Ta -> end  [T:]

start -> w   [w]
w -> wa      [a:D]
wa -> end  [w:]

start -> x   [x]
x -> xa      [a:D]
xa -> end  [x:]

start -> y   [y]
y -> ya      [a:D]
ya -> end  [y:]

start -> z   [z]
z -> za      [a:D]
za -> end  [z:]

start -> Z   [Z]
Z -> Za      [a:D]
Za -> end  [Z:]

# not sure what happens with laryngeals

start -> h   [h]
h -> ha      [a:D]
ha -> end    [h:]

start -> H   [H]
H -> Ha      [a:D]
Ha -> end    [H:]

start -> `   [`]
` -> `a      [a:D]
`a -> end    [`:]

end -> end  [X;V;_;/]

start ->
end ->
