# Move pregem character / to postgem character _

-> start

start -> start  [X;V;_]

start -> /      [:/]
/ -> /C         [X/L]
# Don't geminate it if another consonant follows
/C ->  start    [X]
# ... but do if it precedes a vowel or is final
/C -> /C_       [_:]
/C_ -> start    [V]

start ->
/C_ ->