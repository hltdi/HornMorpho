# replace labialized consonant followed by e, I, or consonant
#   by consonant followed by o or u (delabialize)
#
#   CWe -> Co, CW(I) -> Cu
#
# optionally do the reverse (labialize):
#   replace Co with CWe and Cu with CW (for k,g,h,q)

-> start
start -> start   [~B;kW;gW;hW;qW;V;_;/]

# labialize optionally
start -> *2W     [kW:k;gW:g;qW:q]
*2W -> *2W       [_]
*2W -> start     [e:o;:u]

# delabialize obligatorily for these consonants except before a
start -> BW      [B!]
BW -> BW         [_]
BW -> start      [a]       # fail if anything else comes next

# delabialize
start -> CW      [g:gW;h:hW;k:kW;q:qW]
start -> CW      [b:bW;c:cW;C:CW;d:dW;f:fW]
start -> CW      [j:jW;l:lW;m:mW;n:nW;N:NW]
start -> CW      [r:rW;s:sW;S:SW]
start -> CW      [t:tW;T:TW;x:xW;z:zW;Z:ZW]

CW -> CW         [_]
CW -> start      [o:e;u:]
CW -> CW.C       [u:]
CW.C -> start    [X]       # fail if there's no consonant next
CW.C -> CW       [g:gW;k:kW;q:qW]

start ->
