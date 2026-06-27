# ሲመጣ እንዲመጡ የሚያመጣ, etc.
-> start

start -> start	[*v;/;ይ]
start -> C		[*-ይ]
C -> start		[*v]
C -> C			[*-ይ;/]
C -> y			[ይ]

# only certain consonants are possible (ስ ብ ል ድ ክ ም)
start -> Ci		[{*I2i}]       [sp=3,sn=1,sg=m,t=i,+sub];[sp=3,sn=2,t=i,+sub]
C -> Ci	 		[{*I2i}]       [sp=3,sn=1,sg=m,t=i,+sub];[sp=3,sn=2,t=i,+sub]
Ci -> start		[:ይ;ያ]

y -> C			[^N;/]		[sp=1|2];[t=j|c|p];[sp=3,sn=1,sg=f];[-sub]

start ->
C ->
y ->

