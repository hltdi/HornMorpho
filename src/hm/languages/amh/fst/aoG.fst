# aoc -> oc obligatorily (for generation)
# aa -> a obligatorily

-> start

start -> start  [X;_;/;V-a]

start -> a0     [:a]
# a0 -> start     <oc:>
a0 -> a0o       [o]
a0o -> start    [c]

# Delete a before a
a0 -> start     [a]

start -> a      [a]
a -> start      [X;_;/;V-a,o]

start ->
a ->
