## Realize 3 as b following stem-final -a and -e

-> start

# -eb is always optional
start -> start    [X;V;*;=;^;@;1;2;4;:3]

start -> 3        [:3]

3 -> 3            [1;4]

3 -> 3stem        [=]

3stem -> 3stem1   [b:]
3stem1 -> 3stem2  [e:]
# vowel precedes; precludes werebom, aderebom, etc.
3stem2 -> start   [:e;:a]

# srae+3o -> srabo
3stem1 -> 3stem3  [:e]
3stem3 -> start   [a]

start ->
