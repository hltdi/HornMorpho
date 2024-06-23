## 1s_sbj: C-an, V-n
## (on nouns)
## Do before all other FSTs with special characters

-> start

start -> start	[<;-]

start -> C   [!]
C -> end   <an:N>
C -> C       [!;-;<;>;T;C]
C -> V       [$1;I;L]
C -> VV	   [$2]

start -> V   [$]
V -> C       [!;<;>;T;C]
VV -> C     [!;T;C;>;<]

V -> V       [$1;I;L;-]
VV -> VV    [$2;I;L;-]

V -> end    [n:N]
VV -> end   [n:N]

C -> VL	     [{V2VV}]
VL -> VL    [-]
VL -> end   [:Q]

#C -> end     [:Q]
#VV -> end   [:Q]

end ->
C ->
V ->
VV ->