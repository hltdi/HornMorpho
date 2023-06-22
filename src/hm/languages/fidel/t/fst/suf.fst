-> start

start -> prf	[]		[t=p,+suf]
start -> cvb	[]		[t=c,+suf]
start -> ij		[]		[t=i|j]

prf -> C 		[]		[sp=1|2]
prf -> V		[]		[sp=3]

cvb -> C		[]		[sp=2];[sp=1,sn=2]
cvb -> V		[]		[sp=3];[sp=1,sn=1]

ij ->  V			[]		[sp=2|3,sn=2,+suf];[sp=2,sn=1,sg=f,+suf];[op=1|2|3,+suf]
ij ->  C			[]		[op=0,sp=1,-suf];[op=0,sp=2,sn=1,sg=m,-suf];[op=0,sp=3,sn=1,-suf]

C ->  C			[^N;/;<;>;-]	[+cons]
V ->  V			[^N;/;<;>;-]	[-cons]

C ->
V ->
