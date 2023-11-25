-> start

start -> start	[^^K;:/;';:_;-]

# preserve ኸ ቐ characters
start -> KQ		[^K]
KQ -> start		[^^K;:/;']
KQ -> K2k		[{K2k}]
KQ -> KQ		[^K]

# despirantize ኸ ቐ characters
start -> K2k	[{K2k}]
K2k -> start	[:_]

start ->
KQ ->
