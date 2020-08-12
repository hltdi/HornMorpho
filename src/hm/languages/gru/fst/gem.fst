# clean up various geminated related things
# /C -> C_
# __ -> _

-> start

start -> start   [X;V]
# move / to after following C
start -> /       [:/]
/ -> /C          [X]
/C -> start      [_:]

start -> _       [_]
# delete second _
_ -> start       [X;V;:_]

start ->
_ ->