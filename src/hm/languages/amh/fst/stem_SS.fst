# when a "sibilant" follows as-, replace sS with SS (geminated sibilant)
# sS -> SS; S: {s,z,S,x,Z}

-> start
start -> start    [X-s;V;_;/]

# replace s with pre-gemination character (/)
start -> s.S      [/:s]
s.S -> sS.        [s;z;Z;S;x]
sS. -> start      [X;V]

# other cases: s not followed by a sibilant
start -> s        [s]
s -> start        [X-9;V;_;/]
# or followed by a sibilant which is the last character: kess
s -> ss           [s;z;Z;S;x]

s ->
ss ->
start ->
