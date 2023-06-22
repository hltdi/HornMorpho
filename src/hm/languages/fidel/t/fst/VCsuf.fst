-> start

start -> prf	[]		[t=p]
start -> cvb	[]		[t=c]
start -> ij		[]		[t=i|j]

prf -> C 		[]		[sp=1|2]
prf -> V		[]		[sp=3]

cvb -> C		[]		[sp=2];[sp=1,sn=2]
cvb -> V		[]		[sp=3];[sp=1,sn=1]

ij -> V			[]		[sp=2|3,sn=2];[sp=2,sn=1,sg=f];[op=1|2|3]
ij -> C			[]		[op=0,sp=1];[op=0,sp=2,sn=1,sg=m];[op=0,sp=1];[op=0,sp=3,sn=1]

C -> C			[^N;/]	[+cons]
V -> V			[^N;/]	[-cons]

C ->
V ->