# t->d following voiced stop

-> start

start -> start    [$;!-b,g,d;-;>]

# Environment b, d or g
start -> BDG      [b;d;g]

# Happens before a morpheme boundary; delete?
BDG -> BDG+	 [:-;:>]

BDG -> BDG-	 [-;>]

# t->d
BDG+ -> start      [d:t]

# Consonants other than t
BDG -> start      [$;!-t]
BDG- -> start	 [$;!-t]

start ->
