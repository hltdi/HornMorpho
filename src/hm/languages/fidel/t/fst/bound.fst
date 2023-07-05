-> start

start -> start	[:-]

## prefix changes

start -> V		[*v]
start -> firstC	[*]

V -> V			[:-;*v]
firstC -> firstC	[:-]
firstC -> C2	[*-እ;:እ]
firstC -> V		[*v]
C2 -> C2  		[:-]
C -> C			[:-;*-እ;:እ]
V -> C			[*]
C2 -> C			[*-እ;:እ]
C2 -> V			[*v]
C -> V			[*v]

start -> C2e	[{I2e}]
C2e -> C2e		[:-]
C2e -> V		[:ኣ]
start -> C2i	[{I2i}]
C2i -> C2i		[:-]
C2i -> V		[:ይ]

firstC -> C2e	[{I2e}]
firstC -> C2i	[{I2i}]

V -> C2e	[{I2e}]
V -> C2i	[{I2i}]

## stem changes

firstC -> kqchange+	[:<]
C2 -> kqchange+			[:<]
C -> kqchange+			[:<]
V -> kqchange+			[:<]

## don't change initial k,q
C -> stem			[:<]
# no segments before stem
start -> stem		[:<]

# change initial k, q
kqchange+ -> stem		[^Qv;{kV2KV};^Q;{k2K}]

stem -> stem 		[^N;/]

stem -> stemC+		[:>]
stemC+ -> suff		[^A;:-]

## final stem consonants

stem -> stem_e		[{I2e}]
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
stem_i+ -> suff		[:ኢ]

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

# 3sf subjects, perfective
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
suff+ -> suff			[ኒ;ና;ኻ:ካ;ኺ:ኪ;ኹ:ኩ;ኽ:ክ;ዎ;ዋ;ወ;ዮ;ያ;የ]

suff+ -> suff+/			[/]
suff+/ -> suff			[ኒ;ና;ካ;ኪ;ኩ;ክ;ዎ;ዋ;ወ;ዮ;ያ;የ]

suff -> suff			[^N;/;']

suff -> neg			[:-]
suff+ -> neg		[:-]
neg -> neg			[^N]

suff+ ->
suff ->
neg ->
