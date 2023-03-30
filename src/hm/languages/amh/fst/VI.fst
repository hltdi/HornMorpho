# VI -> V; IV -> V
# upward: generates way too many forms

-> start
start -> start   [X;_;/;8]

# delete I before any vowel
start -> I.V     [:I]
I.V -> start     [V]

# other instance of I
start -> I       [I]
I -> start       [X;/;8]

# delete I after any vowel
start -> V       [V-I]
V -> start       [X;/;8;V-I;:I]

start ->
V ->
I ->
