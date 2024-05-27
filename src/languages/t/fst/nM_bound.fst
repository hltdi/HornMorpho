# handle characters at the boundary between stem and suffixes

-> start

# adposition
start -> adp	[^N]
adp -> adp		[^N]
adp -> adp_stem	[:<]

start -> stem0	[:<]

stem0 -> stem0	[^N;/]

# k->K, q->Q for nouns and adjectives with prepositions
adp_stem -> stem0	[^^K;{q2Q}]

stem0 -> stemC	[*;/]
stem0 -> stemV	[*v]

stemC -> stemC	[*;/]
stemC -> stemV	[*v]

stemV -> stemC	[*;/]
stemV -> stemV	[*v]

stemV -> Vsuff	[:>]   [+sv]
stemC -> Csuff	[:>]   [-sv]

#stem0 -> poss	[:>]

Vsuff -> poss	[]
Csuff -> poss	[]

poss -> cnj		[:-]

cnj -> cnj		[^^Q]
## keep the k in ke
cnj -> cnj		[ከ]		[p=s1];[p=pm2];[p=pf2];[p=pm3];[p=pf3];[-sv,p=0]
## ከ -> ኸ
cnj -> cnj		[ኸ:ከ]	[p=p1];[p=sm2];[p=sf2];[p=sm3];[p=sf3];[+sv,p=0]

cnj ->

