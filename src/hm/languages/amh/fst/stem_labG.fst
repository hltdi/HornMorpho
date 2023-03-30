# CWe -> Co, CWI -> Cu; obligatorily for all consonants for generation

-> start
start -> start   [~B;V;_;/]

# labialize optionally; NOT FOR GENERATION THOUGH
# start -> *2W     [kW:k;gW:g;qW:q]
# *2W -> *2W       [_]
# *2W -> start     [e:o;:u]

# delabialization obligatory for these consonants except before a
start -> BW      [B!;BB]
BW -> BW         [_]
BW -> start      [a]       # fail if anything else comes next

# delabialize
start -> CW      [g:gW;h:hW;k:kW;q:qW]
start -> CW      [b:bW;c:cW;C:CW;d:dW;f:fW]
start -> CW      [j:jW;l:lW;m:mW;n:nW;N:NW]
start -> CW      [r:rW;s:sW;S:SW]
start -> CW      [t:tW;T:TW;x:xW;z:zW;Z:ZW]

CW -> CW         [_]
CW -> start      [o:e]
CW -> CW.C       [u:]
CW.C -> start    [X]       # fail if there's no consonant next

start ->
