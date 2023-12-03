-> start

start -> start	[:-]

## prefix changes

start -> V		[*v]
start -> firstC	[*]

V -> V			[:-;*v]
firstC -> firstC	[:-;/]
firstC -> C2	[*]
firstC -> V		[*v]
C2 -> C2  		[:-]
C -> C			[:-;*]
V -> C			[*-ይ;/]

V -> y			[ይ]
y -> V			[*v]
y -> y.			[:-]
y. -> C			[*-ይ]
y. -> V			[*v]
y. -> stem		[<]

# it seems that both ኣ/ይኸውን and ኣይከውን are possible with the latter more common
V -> y.y		[/:ይ;:ይ]
y.y -> yy.		[:-]
yy. -> C		[ይ]

#C2 -> C			[*-እ;:እ]
C2 -> C				[*]
C2 -> V			[*v]
C -> V			[*v]

start -> C2e	[{I2e}]
C2e -> C2e		[:-]
C2e -> V		[:ኣ]
C2e -> C2e+		[<]
C2e+ -> stem	[:ኣ]
start -> C2i	[{I2i}]
C2i -> C2i		[:-]
C2i -> V		[:ይ]

firstC -> C2e	[{I2e}]
firstC -> C2i	[{I2i}]

V -> C2e	[{I2e}]
V -> C2i	[{I2i}]

C -> C2e	[{I2e}]
C -> C2i	[{I2i}]

#C2 -> C2e	[{I2e}]
#C2 -> C2i	[{I2i}]

## stem changes

C -> stem [<]
C2 -> stem [<]
V -> stem [<]
firstC -> stem [<]

# no segments before stem
start -> stem		[<]

stem -> stem 		[^N;/;:-]

stem -> stemC+		[:>]
# ኢ -> እ before other suffixes
stemC+ -> suff		[^A;:-;:ኢ]

## final stem consonants

stem -> stem_e		[{I2e};ኤ]
stem -> stem_a		[{I2a}]
stem -> stem_o		[{I2o}]
stem -> stem_u		[{I2u}]
stem -> stem_i		[{I2i}]
stem -> stem_E		[{I2e}]

# these may have no subject suffix and go straight to a 3p object suffix
# or delete the perf 3sm አ suffix before 3p objects

stem_e -> stem_e+	[:>]
stem_e+ -> stem_e+	[:-;_;:አ]
stem_e+ -> suff		[:አ]

stem_a -> stem_a+	[:>]
stem_a+ -> stem_a+	[:-;_;:አ]
stem_a+ -> suff		[:ኣ]

stem_o -> stem_o+	[:>]
stem_o+ -> stem_o+	[:-;_;:አ]
stem_o+ -> suff		[:ኦ]

# these can only be subject suffixes
stem_u -> stem_u+	[:>]
stem_u+ -> suff		[:ኡ]

stem_i -> stem_i+	[:>]
# has to be final; others converted to እ
stem_i+ -> suffi	[:ኢ]
suffi -> suffi		[:-]

# -ኢ -> እ before other suffixes
#stem_I -> stem_I+	[:>]
#stem_I+ -> stem_Ii	[:ኢ]
#stem_Ii -> stem_Ii.[:-]
#stem_Ii. -> stem	[^N]

stem_E -> stem_E+	[:>]
stem_E+ -> suff		[:ኤ]

## objects
# 3 objects with 2|3pf subjects
# optionally skip ኣ suffix
stemC+ -> suff3pfA		[:ኣ]
suff3pfA ->	suff3pfA+	[:-]
suff3pfA+ -> suff		[:እ]
suff -> suff3pfA+		[:-] 			

# 23pm subjects with infixed ኡ
suff -> suff_mu			[ሙ:ም]
suff_mu -> suff_mu+	[:-]
suff_mu+ -> suff		[:ኡ]
# 23pf subjects with infixed ኣ
suff -> suff_na			[ና:ን]
suff_na -> suff_na+	[:-]
suff_na+ -> suff		[:ኣ]

# 3sf subjects, perfective and converb
suff -> suff_to			[ቶ:ት]
suff_to -> suff_to+	[:-]
suff_to+ -> suff_to+	[/;_]
suff_to+ -> suff		[:ኦ]
suff -> suff_ta			[ታ:ት]
suff_ta -> suff_ta+	[:-]
suff_ta+ -> suff_ta+	[/;_]
suff_ta+ -> suff		[:ኣ]
suff -> suff_te			[ተ:ት]
suff_te -> suff_te+	[:-]
suff_te+ -> suff_te+	[/;_]
suff_te+ -> suff		[:አ]

# object suffixes without vowel infixes
suff -> suff+			[:-]
#suff+ -> suff			[ኒ;ና;ኻ:ካ;ኺ:ኪ;ኹ:ኩ;ኽ:ክ;ዎ;ዋ;ወ;ዮ;ያ;የ;ል;ለ;ሉ;ላ;ሎ]
suff+ -> suff+			[/]
suff+ -> suff			[ኒ;ና;ካ;ኪ;ኩ;ክ;ዎ;ዋ;ወ;ዮ;ያ;የ;ል;ለ;ሉ;ላ;ሎ]

#suff+ -> suff+/			[/]
#suff+/ -> suff			[ኒ;ና;ካ;ኪ;ኩ;ክ;ዎ;ዋ;ወ;ዮ;ያ;የ;ለ;ሉ;ላ;ሎ]

suff -> suff			[^N;/]

suff -> neg			[:-]
suff+ -> neg		[:-]
neg -> neg			[^N;:-]

suff+ ->
suff ->
suffi ->
neg ->
