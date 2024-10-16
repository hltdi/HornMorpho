-> start

start -> pre1	[^N;/;_]
pre1 -> pre1	[^N;/;_]

# prefix boundaries

# prep before stem-initial ኣ: ላልማዝ
start -> e2a	[{e2a}]
pre1 -> e2a		[{e2a}]
e2a -> e2a		[:-]
#e2a -> e2a+		[:<]
# noun stems normally begin with አ
e2a -> prestem  	[:ኣ;:አ]

# but also allow ለአልማዝ
start -> ea		[*e]
ea -> ea 		[:-]
#ea -> ea+		[:<]
ea -> prestem	[ኣ;አ]

# prep before እየ እነ or stem-initial እ
# ለየቤቱ ለነሱ
start -> eI		[*e]
pre1 -> eI		[*e]
eI -> eI2 		[:-]
eI2 -> pre2		[:እ]

# prep before stem-initial consonant or ኢ ኤ ኦ ኡ
pre1 -> pre2C	[:-]
pre2C -> pre2C	[:-]
#pre2C -> pre2C+	[:<]
pre2C -> prestem	[**v;*;ኢ;ኤ;ኦ;ኡ]

# no prep, start with pre2
start -> pre2	[:-]
pre2 -> pre2	[^N;/;:-]
# allow no change before all stem-initial segments
pre2 -> stem	[:<]
#pre2 -> pre2C	[:>]
#pre2C ->  stem	 [^N]
#pre2C -> stem	[**v;*;ኢ;ኤ;ኦ;ኡ]

# እያባቱ
pre2 -> pre2V	[{e2a}]
#pre2V -> pre2V+	[:<]
pre2V -> pre2V+		[:-]
pre2V+ -> prestem	[:ኣ;:አ]

prestem -> prestem 	[^N;/;:-]

prestem -> stem		[:<]

# prefix
start -> nopre	[:-]
nopre -> nopre	[:-;^N;/]
nopre -> stem	[:<]

# suffix boundaries

stem -> stem	[^N;/;_;:-]

stem -> iya		[*i;{^i2I}]
iya -> iya		[:-;:>]
iya -> plposs	[ያ:ኣ]

# plurals
# ቤቶች; a2o covers some plurals, like ጌቶች
stem -> plur	[{I2o};{a2o}]
plur -> plur	[:>]
plur -> plposs1	[:ኦ]
plposs1 -> plposs	[/]

# ገላዎች
stem -> plurV	[*v]
plurV -> plurV	[:>]
plurV -> plposs1 [ዎ:ኦ]

# ክቡራን
stem -> plurA		[{I2a}]
plurA -> plurA		[:>]
plurA -> plposs		[:ኣ]

# possessives
# ቤቷ
stem -> Wa		[{I2Wa}]
plposs -> Wa	[{I2Wa}]
Wa -> Wa 		[:-;:>]
Wa -> end		[:ዋ]

#stem -> Vwo		[*v]
#plposs -> Vwo	[*v]
#Vwo -> Vwo		[:-;:>]
#Vwo -> end		[ዎ:ኦ]

stem -> I2E		[{I2E}]
plposs -> I2E		[{I2E}]
I2E -> I2E		[:-;:>]
I2E -> end		[:ኤ]

stem -> VyE		[*v]
plposs -> VyE		[*v]
VyE -> VyE		[:-;:>]
VyE -> end		[ዬ:ኤ]

stem -> I2u		[{I2u}]
plposs -> I2u	[{I2u}]
I2u -> I2u		[:-;:>]
I2u -> end		[:ኡ]

stem -> Vwu		[*v]
plposs -> I2u	[{I2u}]
Vwu -> Vwu		[:-;:>]
Vwu -> end		[ው:ኡ]

stem -> Ca		[{I2a}]
plposs -> Ca	[{I2a}]
Ca -> Ca		[:-;:>]
Ca -> end		[:ኣ]

stem -> Csuf	[:>]
Csuf -> Csuf	[:-]
Csuf -> end		[**v;*;/;_]

#start ->
plposs -> end	[ች;ን]

Csuf ->

end -> end		[:-;^N;/;_]

end ->
