-> start
start -> start [%]

start -> V    [V]
start -> X    [X]

V -> start    [h:7]
V -> X        [X]
V -> V        [V;+]
V -> start    [%-7]

X -> start    [k:7]
X -> X        [X;W;+]
X -> V        [V]
X -> start    [%-7]

start ->
X ->
V ->
