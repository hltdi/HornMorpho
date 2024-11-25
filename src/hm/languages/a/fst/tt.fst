-> start

start -> start	[^N]

start -> /		[/]

/ -> start		[^N]

# optionally delete ጥ and ት before final converb ት
# መጥቶ -> መቶ; ተፈትቶ -> ተፈቶ
# but not in the 1s case where the final consonant is geminated
# መጥ/ቼ
# or when the ት or ጥ is preceded by a vowel as in ኣድራጊ converb
start -> t0   	[]   		[t=c,v=0|p|as];[t=c,a=a|i,v=a]
t0 -> t1		[/:ጥ;/:ት]	[sp=2|3];[sn=2]

t1 -> t2 		[ት]

start ->

t2 ->