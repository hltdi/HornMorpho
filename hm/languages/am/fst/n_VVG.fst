# ea -> a
# aa -> a

-> start
# delete $ not following e
start -> start   [X;_;/;V-e,a]

# obligatory (for generation): ye(')alga -> yalga
start -> e.      [:e]
# Delete glottal stop between e and a
e. -> e'         [:';:]
e' -> start      [a]

# obligatory (for generation): delete ' after e and before a consonant
start -> e       [e]
e -> e0'         [:']
e0' -> start     [X;/]

# keep the glottal stop before another vowel (except I and a)
# delete I
start -> e       [e]
e -> e'.         [']
e'. -> start     [V-I,a;:I]

e -> start       [X-';/;V-a]

# obligatory; algac_ew (never a glottal stop in between?)
start -> a       [a]
a -> start       [:a;X;/;V-a]

start ->
e ->
a ->