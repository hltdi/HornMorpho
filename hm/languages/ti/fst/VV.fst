# Delete I and e before any other vowel
# e/@ a -> a sebera
# e/@ o -> o sebero seberom
# e/@ e -> e seberen

-> start
start -> start   [V-I,e,@;X;_]

# delete I before any other vowel
start -> I.V     [:I]
I.V -> start     [V]

# delete e before any other vowel (or only e, o, a?)
start -> e.V     [:e;:@]
e.V -> start     [e;o;a]

# it has to happen
start -> I       [I]
I -> start       [X]       # only a consonant can follow I
start -> e       [e;@]
e -> start       [X]       # only a consonant can follow e
     
start ->
e ->
