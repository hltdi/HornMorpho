-> start

start -> V		[*v]
start -> C1		[*]

V -> V	 		[^Qv;{kV2KV}]
V -> C1	 		[^Q;{k2K}]

# 4 successive Cs; vowels after C1 and C3
C1 -> C2.4     	[^Q;{k2K}]
C2.4 -> C3.4	[*]
C3.4 -> C4		[^Q;{k2K}]

# 3 successive Cs; vowel after C2
C1 -> C2.3		[*]
C2.3 -> C3		[^Q;{k2K}]
C3 -> V			[*v]
C3 -> gem		[/]

# 2 successive Cs; vowel after C2 unless ተ-ሰብር- ይ-ሰብር-
C1 -> C2		[^Q;{k2K}]	 [c=C|E|F|G|H|I];[c=A,a=a|i]
C1 -> C2end		[*]			 [c=A,a=0,t=p,v=p];[c=A,a=0,t=i,v=0]
C2 -> V			[*v]
C2 -> gem		[/]

# 1 consonant
C1 -> V			[*v]
C1 -> gem		[/]

V -> gem		[/]

gem -> V		[*;*v]

V ->

C1 ->
C2 ->
C2end ->
C3 ->
C4 ->
