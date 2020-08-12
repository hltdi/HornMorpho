# s->f before t or n

-> start

start -> start    [$;!-s]

# s changes to f before n or t
start -> s>f      [f:s]
s>f -> start      [t;n]

# s doesn't change in other environments
start -> s        [s]
# followed by vowel or consonant other than n or t (?)
s -> start        [$;!-t,n]

start ->
# s can also end a word
s ->
