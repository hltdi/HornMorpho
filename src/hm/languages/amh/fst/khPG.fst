-> start
start -> start [%]

start -> V    [V]
start -> X    [X]

# Only h after vowels
V -> start    [h:7;hW:9]
V -> X        [X]
V -> V        [V]
V -> start    [%-7,9]

# k after consonants
X -> start    [k:7;kW:9]
X -> X        [X]
X -> V        [V]
X -> start    [%-7,9]

start ->
X ->
V ->
