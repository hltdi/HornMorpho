# Assimilation rules across stem(+def)-case boundary
# optional
# 1   l + n -> ll
# 2   r + n -> rr
# 3   t + n -> nn
# 4   s + n -> fn
# 5   s + t -> ft
# obligatory
# 6   dh + t -> t		;	fuudh-ti -> fuuti
# 7   dh + n -> nn		;	

-> start

start -> start	[!!-dh;$$]

# 1
start -> ln	[l]
ln -> start 	[l:n]

# 2
start -> rn	[r]
rn -> start 	[r:n]

# 3
start -> tn	[n:t]
tn -> start	[n]

# 4, 5
start -> sn	[f:s]
sn -> start	[n;t]

# 6
start -> dht	[:dh]
dht -> start	[t]

#7
start  -> dhn	[n:dh]
dhn -> start	[n]

# other dh, followed by vowel
start -> dh	[dh]
dh -> start	[$$]

start ->