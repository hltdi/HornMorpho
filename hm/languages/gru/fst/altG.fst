## optional alternate vowels at the beginning of words
# yC -> yi
# yE -> ye
# we -> wo
# r -> er
## anywhere
# go -> gWe, ko -> kWe, qo -> qWe
# bwa -> bWa, gwa -> gWa, etc.

-> start
start -> end    [X-r,kW,gW,qW;V;_]

## erox_o, eraben_t
## Make this obligatory for generation because it seems to be for some verbs (ኧሮሾ፟)
start -> e.r    [e:]
e.r -> end      [r]

# should be obligatory
#start -> y      [y]
#y -> yi         [i:]
#yi -> end       [X]

## exclude for generation

#start -> w1     [w]
#end -> w        [w]
#w -> w          [_]
#w -> end        [o:e]
#w1 -> end       [o:e]
#w1 -> w1.C      [u:]
#w1.C -> end     [X]

#y -> end        [e:E]

# b(_)wa -> bW(_)a
start -> b.wa   [bW:b]
end   -> b.wa   [bW:b]
b.wa -> b.wa    [_]
b.wa -> bw.a    [:w]
bw.a -> end     [a]

# g(_)wa -> gW(_)a
start -> g.wa   [gW:g]
end   -> g.wa   [gW:g]
g.wa -> g.wa    [_]
g.wa -> gw.a    [:w]
gw.a -> end     [a]

# k(_)wa -> kW(_)a
start -> k.wa   [kW:k]
end   -> k.wa   [kW:k]
k.wa -> k.wa    [_]
k.wa -> kw.a    [:w]
kw.a -> end     [a]

# m(_)wa -> mW(_)a
start -> m.wa   [mW:m]
end   -> m.wa   [mW:m]
m.wa -> m.wa    [_]
m.wa -> mw.a    [:w]
mw.a -> end     [a]

# q(_)wa -> qW(_)a
start -> q.wa   [qW:q]
end   -> q.wa   [qW:q]
q.wa -> q.wa    [_]
q.wa -> qw.a    [:w]
qw.a -> end     [a]

#start -> g.o    [gW:g]
#end -> g.o      [gW:g]
#g.o -> g.o      [_]
#g.o -> end      [e:o]

start -> gW.e   [g:gW]
end -> gW.e     [g:gW]
gW.e -> gW.e    [_]
gW.e -> end     [o:e]

#start -> k.o    [kW:k]
#end -> k.o      [kW:k]
#k.o -> k.o      [_]
#k.o -> end      [e:o]

start -> kW.e   [k:kW]
end -> kW.e     [k:kW]
kW.e -> kW.e    [_]
kW.e -> end     [o:e]

start -> kW     [kW]
end -> kW       [kW]
kW -> end       [V-e;X;_]

start -> gW     [gW]
end -> gW       [gW]
gW -> end       [V-e;X;_]

start -> qW     [qW]
end -> qW       [qW]
qW -> end       [V-e;X;_]

#start -> q.o    [qW:q]
#end -> q.o      [qW:q]
#q.o -> q.o      [_]
#q.o -> end      [e:o]

start -> qW.e   [q:qW]
end -> qW.e     [q:qW]
qW.e -> qW.e    [_]
qW.e -> end     [o:e]

start -> g.uC   [g:gW]
end   -> g.uC   [g:gW]
g.uC -> g.uC    [_]
g.uC -> gu.C    [u:]
gu.C -> end     [X]

start -> k.uC   [k:kW]
end   -> k.uC   [k:kW]
k.uC -> k.uC    [_]
k.uC -> ku.C    [u:]
ku.C -> end     [X]

start -> q.uC   [q:qW]
end   -> q.uC   [q:qW]
q.uC -> q.uC    [_]
q.uC -> qu.C    [u:]
qu.C -> end     [X]

start -> b.uC   [b:bW]
end   -> b.uC   [b:bW]
b.uC -> b.uC    [_]
b.uC -> bu.C    [u:]
bu.C -> end     [X]

start -> m.uC   [m:mW]
end   -> m.uC   [m:mW]
m.uC -> m.uC    [_]
m.uC -> mu.C    [u:]
mu.C -> end     [X]

start -> bW.e   [b:bW]
end -> bW.e     [b:bW]
bW.e -> bW.e    [_]
bW.e -> end     [o:e]

start -> mW.e   [m:mW]
end -> mW.e     [m:mW]
mW.e -> mW.e    [_]
mW.e -> end     [o:e]

end -> end      [X-kW,gW,qW;V;_]
end ->
