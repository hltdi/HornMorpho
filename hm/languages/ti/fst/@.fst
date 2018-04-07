# @ -> e following non-L
# @ -> E optionally following L

-> start
start -> start [V]

# non-laryngeal consonant
start -> C    [X/L;_]
# followed by any vowel but @, back to start
C -> start    [V-@]
C -> C        [X/L;_]
C -> L        [L]
# followed by @, change it to e
C -> start    [e:@]

start -> L    [L]
# followed by any vowel, back to start
L -> start    [V]
L -> C        [X/L;_]
L -> L        [L]
# followed by @, optionally change to E
L -> start    [E:@]

start ->
C ->
L ->
