# @ -> e following non-L

-> start
start -> start [L;V]

# non-laryngeal consonant
start -> C    [X/L;_]
# followed by any vowel but @, back to start
C -> start    [L;V-@]
C -> C        [X/L;_]
# followed by @, change it to e
C -> start    [e:@]

start ->
C ->

