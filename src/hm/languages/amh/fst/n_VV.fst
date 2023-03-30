# e(')a -> a (optionally)
# e(')I -> e (optionally)
# a|o|u i -> a|o|u y

-> start
# delete $ not following e
start -> start   [X;_;/;V-e,a,o,u]

# optional: yalga, ye'alga
start -> e.      [:e]
# Delete glottal stop between vowels if there is one
e. -> e'         [:';:]
e' -> start      [a]

# optional: delete ' after e and before a consonant
start -> e       [e]
e -> e''         [:']
e'' -> start     [X;/]
# keep the glottal stop before another vowel (except I)
# delete I
e -> e'.         [']
e'. -> start     [V-I;:I]
e -> start       [X;/]

start -> V       [a;u;o]
# Cereqaytu, Truytu
V -> start       [y:i]
V -> start       [X;/;V-i]

start ->
e ->
V ->
