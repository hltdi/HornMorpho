# palatalizable -> palatal preceding 8i and 8E

-> start

start -> start [!J;J;V;_;/]

# this can only happen after !J (non-palatalizable consonants)
start -> 8     [:8]
8 -> start     [i;E]

# palatalizable not followed by 8
start -> PP    [JJ]
PP -> PP       [JJ;/;_]
PP -> start    [X-JJ;V;/]

# palatalize palatalizable consonant
start -> P     [c:t;j:d;C:T;x:s;C:S;Z:z;y:l;N:n]
PP -> P        [c:t;j:d;C:T;x:s;C:S;Z:z;y:l;N:n]
P -> P         [_]
P -> P8        [:8]
# keep the i or E before a consonant (or at the end)
P8 -> Pi       [i;E]
Pi -> start    [X]
# delete the i or E before a vowel
# (keep these separate because deleted i can end the word)
P8 -> P0i      [:i]
P8 -> P0E      [:E]
P0i -> start   [V]
P0E -> start   [V]

## consonant already palatalized; do the same things as after a palatalized C (before 8)
start -> P     [J]
## palatalized consonant not before 8
start -> !P    [J]
!P -> !P       [_]
!P -> P        [c:t;j:d;C:T;x:s;C:S;Z:z;y:l;N:n]
!P -> PP       [JJ]
!P -> start    [!J;J;V;_;/]

start ->
PP ->
Pi ->
P0i ->
!P ->
