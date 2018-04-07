# CWe -> Co, CWI -> Cu obligatorily

-> start
start -> start     [~B;V;_;/]

# delabialization obligatory for all labialized consonants except before a
# (for generation only true for KW)
start -> BW        [B]
BW -> BW           [_]
BW -> start        [a;i]      # fail if anything but a or i comes next

# delabialize
start -> C=CW      [g:gW;h:hW;H:HW;k:kW;q:qW]
start -> C=CW      [b:bW;c:cW;C:CW;d:dW;f:fW]
start -> C=CW      [j:jW;l:lW;m:mW;n:nW;N:NW]
start -> C=CW      [r:rW;s:sW;S:SW;t:tW;T:TW;x:xW;z:zW;Z:ZW]

C=CW -> C=CW       [_]
C=CW -> start      [o:e]
C=CW -> C=CW.C     [u:;u:I]
C=CW.C -> start    [X]       # fail if there's no consonant next

start ->
