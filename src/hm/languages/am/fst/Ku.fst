# Cku+ -> CkW, etc.
# Vhu+ -> VhW

-> start

start -> start   [D]

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
h -> start       [X;V-u:D]
h -> hu          [u]
hu -> start      [X;V;_;D]

X -> K           [k;g;q]
K -> start       [X;_;V-u;D]
K -> Ku          [u]
Ku -> start      [X;V;_;D]

#start -> start   [X-h,k,g,q;V;_;D]
#start -> K.u     [hW:h;kW:k;gW:g;qW:q]
#K.u -> Ku.       [:u]

#start -> K       [h;k;g;q]
#K -> start       [X;_;V-u;D]
#K -> Ku          [u]
#Ku -> start      [X;V;_;D]

start ->
KW. ->
hW. ->
K ->
h ->
