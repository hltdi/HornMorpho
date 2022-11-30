# Cku+ -> CkW, etc.
# Vhu+ -> VhW

-> start

start -> V       [V]
start -> X       [X]
V -> X           [X-h]
X -> V           [V]
X -> X           [X-k,g,q;_]

V -> h.W         [hW:h]
h.W -> hW.       [:u]
X -> K.W         [kW:k;gW:g;qW:q]
K.W -> KW.       [:u]

V -> h           [h]
h -> start       [X]
h -> hu          [u]
hu -> start      [X;V;_]

X -> K           [k;g;q]
K -> start       [X;_;V-u]
K -> Ku          [u]
Ku -> start      [X;V;_]

#start -> start   [X-h,k,g,q;V;_]
#start -> K.u     [hW:h;kW:k;gW:g;qW:q]
#K.u -> Ku.       [:u]

#start -> K       [h;k;g;q]
#K -> start       [X;_;V-u]
#K -> Ku          [u]
#Ku -> start      [X;V;_]

start ->
KW. ->
hW. ->
K ->
h ->
