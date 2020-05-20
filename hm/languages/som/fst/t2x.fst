# t->x following q or x

-> start

start -> start    [$;!-q]

# Environment: q_ or x_
start -> q        [q;x]

# t->x
q -> start        [x:t]

# Consonants other than t
q -> start        [$;!-t]

start ->
