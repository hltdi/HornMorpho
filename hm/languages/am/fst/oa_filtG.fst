# filter out C V V
# leaving CW a
# except for w|y o|u a

-> start

start -> start   [V;/]

start -> X       [X]
X -> X           [_;X]

X -> start       [/]

# These can't be followed by another vowel
X -> XV          [a;e;E;i;I;o;u]

XV -> X          [X]
XV -> start      [/]

# Accept o|u after y|w, but insert '
start -> Y       [y;w]
Y -> Y           [/;_]
Y -> YU          [o;u]
YU -> YU'        [':]
YU' -> start     [a]

# final states
start ->
X ->
XV ->
Y ->
YU ->
