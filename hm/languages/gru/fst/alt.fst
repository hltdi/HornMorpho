## optional alternate vowels at the beginning of words
# yC -> yi
# yE -> ye
# r -> er
## anywhere
# go -> gWe, ko -> kWe, qo -> qWe
# we -> wo

-> start
start -> end    [X;V;_]

# erox_o, eraben_t
start -> e.r    [e:]
e.r -> end      [r]

start -> w1     [w]
end -> w        [w]
w -> w          [_]
w -> end        [o:e]
w1 -> end       [o:e]
w1 -> w1.C      [u:]
w1.C -> end     [X]

start -> y      [y]
y -> yi         [i:]
yi -> end       [X]
y -> end        [e:E]

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

start -> g.o    [gW:g]
end -> g.o      [gW:g]
g.o -> g.o      [_]
g.o -> end      [e:o]

start -> gW.e   [g:gW]
end -> gW.e     [g:gW]
gW.e -> gW.e    [_]
gW.e -> end     [o:e]

start -> k.o    [kW:k]
end -> k.o      [kW:k]
k.o -> k.o      [_]
k.o -> end      [e:o]

start -> kW.e   [k:kW]
end -> kW.e     [k:kW]
kW.e -> kW.e    [_]
kW.e -> end     [o:e]

start -> q.o    [qW:q]
end -> q.o      [qW:q]
q.o -> q.o      [_]
q.o -> end      [e:o]

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

##start -> lW.e   [l:lW]
##end -> lW.e     [l:lW]
##lW.e -> lW.e    [_]
##lW.e -> end     [o:e]
##
##start -> sW.e   [s:sW]
##end -> sW.e     [s:sW]
##sW.e -> sW.e    [_]
##sW.e -> end     [o:e]
##
##start -> TW.e   [T:TW]
##end -> TW.e     [T:TW]
##TW.e -> TW.e    [_]
##TW.e -> end     [o:e]
##
##start -> CW.e   [C:CW]
##end -> CW.e     [C:CW]
##CW.e -> CW.e    [_]
##CW.e -> end     [o:e]
##
##start -> xW.e   [x:xW]
##end -> xW.e     [x:xW]
##xW.e -> xW.e    [_]
##xW.e -> end     [o:e]
##
##start -> l.uC   [l:lW]
##end   -> l.uC   [l:lW]
##l.uC -> l.uC    [_]
##l.uC -> lu.C    [u:]
##lu.C -> end     [X]
##
##start -> s.uC   [s:sW]
##end   -> s.uC   [s:sW]
##s.uC -> s.uC    [_]
##s.uC -> su.C    [u:]
##su.C -> end     [X]
##
##start -> x.uC   [x:xW]
##end   -> x.uC   [x:xW]
##x.uC -> x.uC    [_]
##x.uC -> xu.C    [u:]
##xu.C -> end     [X]
##
##start -> T.uC   [T:TW]
##end   -> T.uC   [T:TW]
##T.uC -> T.uC    [_]
##T.uC -> Tu.C    [u:]
##Tu.C -> end     [X]
##
##start -> C.uC   [C:CW]
##end   -> C.uC   [C:CW]
##C.uC -> C.uC    [_]
##C.uC -> Cu.C    [u:]
##Cu.C -> end     [X]

end -> end      [X;V;_]
end ->
