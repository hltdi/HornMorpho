-> start

# start -> start  [X;C]

# unlabialized labializable consonants
start -> nolab   [B;K;k]
nolab -> nolab   [B;K;T;R;N;Y]
# final unlabialized labializable or unlabializable consonant
nolab -> nolab0  [B;K;T;R;N;Y]         [-W]

# labialized consonants
nolab -> lab     [W]
# any characters after this
lab -> lab       [X;C]

# other characters; either not labializable or already labialized
start -> start   [T;R;N;W;J]

start ->
nolab0 ->
lab ->
