# e(')a -> a (optionally)
# e(')I -> e (optionally)
# aa -> a

-> start
# delete $ not following e
start -> start   [X;_;/;V-e,a]

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

# obligatory; algac_ew (never a glottal stop in between?)
start -> a       [a]
a -> start       [:a;X;/;V-a]

start ->
e ->
a ->