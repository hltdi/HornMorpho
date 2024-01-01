-> start

start -> c1		[^N]

# 2nd segment may be geminated
c1 -> c1_		[/]
c1_ -> c2		[^N]

c1 -> c2		[^x]
c1 -> c2		[{q2Q}]	[+K2]
c1 -> c2		[^k]		[-K2]

# 3rd segment may be geminated
c2 -> c2_		[/]
c2_ -> c3		[^N]

c2 -> c3		[^x]
c2 -> c3		[{q2Q}]	[+K3]
c2 -> c3		[^k]		[-K3]

c3 -> c4		[^x]
c3 -> c4		[{q2Q}]	[+K4]
c3 -> c4		[^k]		[-K4]

c4 -> c5		[^x]
c4 -> c5		[{q2Q}]	[+K5]
c4 -> c5		[^k]		[-K5]

c5 -> c6		[^x]
c5 -> c6		[{q2Q}]	[+K6]
c5 -> c6		[^k]		[-K6]

c2 ->
c3 ->
c4 ->
c5 ->
c6 ->
