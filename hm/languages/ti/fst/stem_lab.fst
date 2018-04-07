## delabialization
# CWe -> Co, CW(I) -> Cu; optionally for {g, k, q, h, H}, obligatorily for others
## labialization
# Co -> CWe, Cu -> CWI; optionally for {g, k, q, h, H}

-> start
start -> start     [~B;kW;gW;hW;HW;qW;V;_;/]

# labialize optionally
start -> KW=KO     [kW:k;gW:g;hW:h;HW:H;qW:q]
KW=KO -> KW=KO     [_]
KW=KO -> start     [e:o;:u]

# delabialization is obligatory for these consonants except before a and i
start -> BW        [B!]
BW -> BW           [_]
BW -> start        [a;i]       # fail if anything else comes next

# delabialize
start -> C=CW      [g:gW;h:hW;H:HW;k:kW;q:qW]

start -> C=CW      [b:bW;c:cW;C:CW;d:dW;f:fW]
start -> C=CW      [j:jW;l:lW;m:mW;n:nW;N:NW]
start -> C=CW      [r:rW;s:sW;S:SW;t:tW;T:TW;x:xW;z:zW;Z:ZW]

C=CW -> C=CW       [_]
C=CW -> start      [o:e]
C=CW -> C=CW.C     [u:;u:I]
C=CW.C -> start    [X]       # fail if there's no consonant next
C=CW.C -> C=CW     [g:gW;h:hW;H:HW;k:kW;q:qW]

start ->
