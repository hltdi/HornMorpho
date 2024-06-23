# tn -> nn; dn -> nn
# ex: barbaanne, binne, namoonni
# optional (uncomment #! to make it obligatory)

-> start

#! start -> start    [$;!-t,d]
# delete remaining morpheme boundaries
start -> start    [$;!;:-;:>]

# Change t or d to n
start -> T2n      [n:t;n:d]
# word boundary
T2n -> T2n+		[:-;:>]
# ... before
T2n+ -> start      [n]

# Preserve t or d
#!start -> T        [t;d]
# ... before a vowel or any consonant but n
#!T -> start        [$;!-n]

start ->
#!T ->
