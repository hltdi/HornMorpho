# ey(yI) -> E before a C optionally
# Iye -> E optionally

-> start
# optional so continue with anything
start -> start   [X;_;V]

start -> e.y     [E:e]
# ey -> E
e.y -> ey.       [:y]
ey. -> start     [X-y]
# eyy(I) -> E
ey. -> eyy.      [:y]
eyy. -> start    [X;:I]

start -> I.ye    [:I]
I.ye -> Iy.e     [E:y]
Iy.e -> start    [:e]

start ->

