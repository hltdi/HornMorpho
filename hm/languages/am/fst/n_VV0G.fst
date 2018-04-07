# e($)a -> a
# e$'I -> e'
# aa -> a
# $ -> 0

-> start
# delete $ not following e
start -> start   [X;_;/;V-e,a;:$]

# obligatory: ye(')alga -> yalga
start -> e.      [:e]
# delete the word boundary (there has to be one)
e. -> e$.        [:$]
# Delete glottal stop between vowels if there is one
e$. -> e$'       [:';:]
e$' -> start     [a]

start -> e       [e]
# delete the boundary character
e -> e$          [:$]
e$ -> start      [X-';/]

# keep the glottal stop before a consonant or another vowel (except I)
# delete I
e$ -> e'.        [']
e'. -> start     [X;/;V-I,a;:I]

e -> start       [X;/;V-a]

# obligatory; algac_ew (never a glottal stop in between?)
start -> a       [a]
a -> start       [:a;X;/;V-a]

start ->
e ->
a ->