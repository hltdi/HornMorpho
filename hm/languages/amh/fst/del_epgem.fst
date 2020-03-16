-> start

start -> V        [V-I]
start -> C        [X]
V -> C            [X]
C -> C            [X]
C -> V            [:I;V-I]

# delete first /
V -> /            [:/]
C -> /            [:/]
# single / followed by C (possible end state)
/ -> C            [X]
# C followed by _ (possible end state)
C -> _            [:_]
_ -> C            [X]
_ -> V            [:I;V-I]
# _ can also be followed by /
_ -> /            [:/]
# second /; convert to space; not end state, must be followed by C
/ -> /             [ :/]

V ->
C ->
_ ->
