# a e/a -> a
# e a -> a
# a e a -> a
# e e a -> a
# e e -> e
# e u -> u
# a u -> u
# a (8) i -> i
# upward: generates way too many forms

-> start
start -> start   [X;_;/;8;V-a,e]

# Delete e/a before a, i, or u; delete e before e
start -> e.      [:e]
e. -> ee.        [:e]          # delete second e
ee. -> start     [a]           # ... before a
e. -> ee         [e]           # keep second e
ee -> start      [/;X;I]       # ... before C, I or #
e. -> vV         [a;i;u]
start -> a.      [:a]
a. -> vV         [a;i;u]
a. -> a8.        [8]           # in case this is 2sf imperfect or imperative
a8. -> vV        [i]
vV -> start      [/;X;a;I]     # only delete V before VC or Va or vI or V#

# Delete e after a
start -> a       [a]
a -> av          [:e]
av -> start      [/;X;I;:a]    # only delete V before C or # or I;
                               # but delete another a if it follows
a -> start       [/;X;I]       # any others?

start -> e       [e]
e -> start       [/;X;I]       # other vowels?

start ->
a ->
vV ->
e ->
ee ->
av ->
