# filter out C V V
# leaving CW a
# except for w|y o|u a

-> start

start -> start   [V;/]

start -> X       [X-y,w]
X -> X           [_;X-y,w]

X -> start       [/]

# These can't be followed by another vowel
X -> XV          [a;e;E;i;I;o;u]

XV -> X          [X-y,w]
XV -> start      [/]
X -> Y            [y;w]
XV -> Y           [y;w]

# Accept o|u after y|w, but insert '
start -> Y       [y;w]
Y -> Y           [/;_;y;w]
Y -> YU          [o;u]
Y -> start       [V-o,u]
Y -> X           [X]
YU -> YU'        [':]
YU' -> start     [a]
YU -> start      [X;V-a;/;_]

# final states
start ->
X ->
XV ->
Y ->
YU ->
