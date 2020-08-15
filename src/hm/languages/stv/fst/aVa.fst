# a I/e/a -> a
# e/I a -> a
# au -> u
# ai -> i
# upward: generates way too many forms

-> start
start -> start   [X;_;V-aa,a,i]

# Delete vowel before a, i, or u
start -> v.V     [:a;:i;:aa]       # any others?
v.V -> vV        [aa;ii;u]
vV -> start      [X;aa]            # only insert V before VC or Va or V#

# Delete e,I after a
start -> a       [aa]
a -> av          [:a;:i]
av -> start      [X]        # only insert V before C or #
a -> start       [X]        # any others?

start -> v.V*    [a;i]
v.V* -> vV*      [aa;ii;u]        # fail
v.V* -> start    [X]              # other vowels?
a -> aV          [a;i;aa;ii;u]    # fail (because a_ not deleted or _V not deleted)

start ->
a ->
vV ->
v.V* ->
av ->
