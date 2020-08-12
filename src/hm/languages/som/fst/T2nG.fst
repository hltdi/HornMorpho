# tn -> nn; dn -> nn
# ex: barbaanne, binne, namoonni
# obligatory for generation (optional for analysis)

-> start

start -> start    [$;!-t,d]

# Change t or d to n
start -> T2n      [n:t;n:d]
# ... before
T2n -> start      [n]

# Preserve t or d
start -> T        [t;d]
# ... before a vowel or any consonant but n
T -> start        [$;!-n]

start ->
T ->
