# VE -> VyE
# Vo -> Vwo
# ia -> iya / Iya
# ua -> uwa, oa -> owa

-> start

start -> start  [X;_;/;$]

start -> V      [V]
# VyE
V -> Vy         [y:]
Vy -> start     [E]
# Vwo
V -> Vw         [w:]
Vw -> start     [o]

# iya
start -> i      [i]
i -> iy         [y:]
## or i->I
#start -> Ii     [I:i]
#Ii -> iy        [y:]
iy -> start     [a]       # only a possible?

# Eya
start -> E      [E]
E -> Ey         [y:]
Ey -> start     [a]       # only a possible?

# owa, uwa
start -> ou     [o;u]
ou -> ouw       [w:]
ouw -> start    [a]       # only a possible

start -> e      [e]
e -> V          [V-o]     # o also possible?
e -> start      [X;/;$]

i -> start      [X;/]
E -> start      [X;/]
ou -> start     [X;/]

V -> start      [X;/;$]
V -> i          [i]
# V -> E          [E]
V -> ou         [u]
V -> V          [V-E,o,a]

start ->
V ->
e ->
