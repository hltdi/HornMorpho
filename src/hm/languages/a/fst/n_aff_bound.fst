-> start

start -> pre1	[^N;/;_]
pre1 -> pre1	[^N;/;_]

# prefix boundaries

# prep before stem-initial ኣ: ላልማዝ
start -> e2a		[{e2a}]
pre1 -> e2a		[{e2a}]
e2a -> e2a		[:-]
e2a -> e2a+		[:<]
# noun stems normally begin with አ
# +- init feature can prevent this
e2a+ -> stem  	      	[:ኣ;:አ]		[+delinit]

# but also allow ለአልማዝ
start -> ea		[*e]
ea -> ea 		[:-]
ea -> ea+		[:<]
ea+ -> stem		[ኣ;አ]

# prep before እየ እነ or stem-initial እ
# ለየቤቱ ለነሱ
start -> eI		[*e]
pre1 -> eI		[*e]
eI -> eI2 		[:-]
eI2 -> eI2+		[:<]
eI2 -> pre2		[:እ;እ]
eI2+ -> stem		[:እ]	    [+delinit]

# prep before stem-initial consonant or ኢ ኤ ኦ ኡ or አ (optionally)
pre1 -> pre2C	[:-]
pre2C -> pre2C+	[:<]
pre2C+ -> stem	[**v;*;ኢ;ኤ;ኦ;ኡ;አ;/]

# no prep, start with pre2
start -> pre2	[:-]
pre2 -> pre2	[^N;/]
# allow no change before all stem-initial segments
pre2 -> stem	[:<]
#pre2 -> pre2C	[:>]
#pre2C ->  stem	 [^N]
#pre2C -> stem	[**v;*;ኢ;ኤ;ኦ;ኡ]

# እያባቱ
pre2 -> pre2V	[{e2a}]
pre2V -> pre2V+	[:<]
pre2V+ -> stem	[:ኣ;:አ]

# prefix
start -> nopre	[:-]
nopre -> nopre	[:-]
nopre -> stem	[:<]

# suffix boundaries

stem -> stem	[^N;/;_;:-]

## agent and manner verbal nouns
## ሰባሪ መላሽ
#stem -> iya		[*i;{^i2I}]
#iya -> iya		[:-;:>]
#iya -> plposs	[ያ:ኣ]

# plurals
# ቤቶች; a2o and i2o cover some plurals, like ጌቶች, ጓደኞች, ነጆች
stem -> plur	[{I2o};{a2o};{i2o}]
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

# ኢትዮጵያዊያን
stem -> plurIA		[ዊ;ው:ዊ]
plurIA -> plurIA	[:>]
plurIA -> plposs	[ያ:ኣ]

# human suffix
stem -> a2I		[{a2I};*;*v]
# stem and plural boundaries
a2I -> a2I		[:>;:-]
a2I -> human	[:እ]
human -> human	[/;የ;ዮ;ዬ]
human -> end	[:-]
human -> humposs	[:-]
humposs -> end	[ው:ኡ]

# possessives
# ቤቷ
stem -> Wa		[{I2Wa}]
plposs -> Wa		[{I2Wa}]
Wa -> Wa 		[:-;:>]
Wa -> end		[:ዋ]

# ቤቴ
stem -> I2E		[{I2E}]
plposs -> I2E		[{I2E}]
I2E -> I2E		[:-;:>]
I2E -> end		[:ኤ]

# መሪዬ መሪያቸው
stem -> VyE		[*v]
plposs -> VyE		[*v]
VyE -> VyE		[:-;:>]
VyE -> end		[ዬ:ኤ;ያ:ኣ]

stem -> I2u		[{I2u}]
plposs -> I2u	[{I2u}]
I2u -> I2u		[:-;:>]
I2u -> end		[:ኡ]

stem -> Vwu		[*v]
plposs -> I2u	[{I2u}]
Vwu -> Vwu		[:-;:>]
Vwu -> end		[ው:ኡ]

stem -> Ca		[{I2a};^a]
plposs -> Ca	[{I2a};^a]
Ca -> Ca		[:-;:>]
Ca -> end		[:ኣ]

# -ኢቱ
stem -> Ci		[{I2i}]
plposs -> Ci	[{I2i}]
Ci -> Ci		[:-;:>]
Ci -> end		[:ኢ]

stem -> Csuf	[:>]
Csuf -> Csuf	[:-]
Csuf -> end		[**v;*;/;_]

plposs -> end	[ች;ን]

Csuf ->

end -> end		[:-;^N;/;_]

end ->
