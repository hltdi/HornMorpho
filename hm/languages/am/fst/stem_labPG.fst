# replace labialized consonant other than k, g, h, q,
# followed by e, I, or consonant
# by consonant followed by o or u (delabialize)
#
#   CWe -> Co, CW(I) -> Cu
#
# do the reverse (labialize) for k, g, h, q:
#   replace Co with CWe and Cu with CW (for k,g,h,q)

-> start
# All unlabialized consonants except g,h,k,q; gW,hW,kW,qW
start -> start   [~B-g,h,k,q;BB;V;_;/]

# labialize g,h,k,q before o or u
start -> *2W     [kW:k;gW:g;qW:q]
*2W -> *2W       [_]
*2W -> start     [e:o;:u]

# other instances of g,h,k,q
start -> 2W      [g;h;k;q]
2W -> 2W         [_]
2W -> start      [V-o,u;X;/]

# delabialize obligatorily for these consonants except before a
start -> BW      [B!]
BW -> BW         [_]
BW -> start      [a]       # fail if anything else comes next

# delabialize
# start -> CW      [g:gW;h:hW;k:kW;q:qW]
start -> CW      [b:bW;c:cW;C:CW;d:dW;f:fW]
start -> CW      [j:jW;l:lW;m:mW;n:nW;N:NW]
start -> CW      [r:rW;s:sW;S:SW]
start -> CW      [t:tW;T:TW;x:xW;z:zW;Z:ZW]

CW -> CW         [_]
CW -> start      [o:e;u:]
CW -> CW.C       [u:]
CW.C -> start    [X]       # fail if there's no consonant next
# CW.C -> CW       [g:gW;k:kW;q:qW]

start ->
# stem can end in g,k,q
2W ->
