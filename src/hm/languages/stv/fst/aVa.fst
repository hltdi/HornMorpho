# a I/e/a -> a
# e/I a -> a
# au -> u
# ai -> i
# upward: generates way too many forms

-> start
start -> start   [X;_;V-a,e,I]

# Delete vowel before a, i, or u
start -> v.V     [:e;:I;:a]       # any others?
v.V -> vV        [a;i;u]
vV -> start      [X;a]            # only insert V before VC or Va or V#

# Delete e,I after a
start -> a       [a]
a -> av          [:e;:I]
av -> start      [X]        # only insert V before C or #
a -> start       [X]        # any others?

start -> v.V*    [e;I]
v.V* -> vV*      [a;i;u]          # fail
v.V* -> start    [X]              # other vowels?
a -> aV          [e;I;a;i;u]      # fail (because a_ not deleted or _V not deleted)

start ->
a ->
vV ->
v.V* ->
av ->
