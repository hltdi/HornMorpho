# Convert vowel representations
# e -> a
# a -> aa
# I -> i
# i -> ii
# @ -> e
# E -> ee
# O -> oo
# U -> uu
# o, u unchanged

-> start

start -> start    [X;_;u;o]

# short vowels
start -> start    [a:e;i:I;e:@]

# long vowels
start -> a        [a]
a -> start        [a:]
start -> i        [i]
i -> start        [i:]
start -> o        [o:O]
o -> start        [o:]
start -> u        [u:U]
u -> start        [u:]
start -> e        [e:E]
e -> start        [e:]

start ->
