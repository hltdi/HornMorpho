-> start

start -> start	[:-;**v;/]

start -> C		[*]
C ->  start		[**v;:-;/]
C -> C			[*-ይ]

## prefix changes

# ዚሰ/ብር
C -> C2i		[{I2i}]
start -> C2i	[{I2i}]
C2i -> C2i		[:-]
C2i -> start	[:ይ]

## stem-prefix boundary

# ዘስበረ; ተስ/ብር
C -> C2e		[{I2e}]
start -> C2e	[{I2e}]
C2e -> C2e		[:-]
C2e -> C2e+		[:<]
C2e+ -> stem0	[:ኣ]

# ዘሎ ከሎ etc.
C2e+  -> C2alle	[:-]	 [root=ህልው]
C2alle -> stem	[:ኣ]

C -> .Ia		[:እ]
start -> .Ia	[:እ]
.Ia -> .Ia		[:-]
.Ia -> I.a		[:<]
I.a -> stem0	[ኣ]

C -> stem+			[:<]
start -> stem+		[:<]
# stem starting with anything other than ኣ
stem+ -> stem0 		[^A;/]

start -> nopre		[:-]
nopre -> nopre		[:-]
nopre -> nopre+		[:<]
nopre+ -> stem0		[ኣ]

stem0 -> stem0		[^N;/]

# First base stem consonant
stem+ -> stem1		[:-]
stem0 -> stem1		[:-]

# k-K, q-Q when preceded by vowel
stem1 -> stem		[^x;/]		
stem1 -> stem		[{q2Q}]	[+K1]
stem1 -> stem		[^k]		[-K1]

stem -> stem		[^N;/]

# stem ending in vowel
stem -> stemV.+		[*v]
stemV.+ -> stemV+	[:>]
stemV+ -> suff		[ኻ:ካ;ኺ:ኪ;ኹ:ኩ;ኽ:ክ;^^q;:አ;:-]

# stem ending a consonant
stem -> stemC.+		[*]
stemC.+ -> stemC+	[:>]
# no changes before suffixes beginning with vowels
stemC+ -> suff		[^A;:-]
# ኢ -> እ before other suffixes; object, negative (but not conjunctions like ዶ)
stemC+ -> suff		[:ኢ]	[+O];[+neg,+mc,t=i]

## jussive 3 objects; geminate stem-final consonant (except laryngeals)
stem -> j3		[/:]
# add vowel suffix to stem-final consonant
j3 -> j3o1		[{^I2o}]
j3o1 -> j3o2	[:>]
j3o2 -> j3o2	[:-]
j3o2 -> j3o3	[:_]
j3o3 -> suff	[:ኦ]

j3 -> j3e1		[{I2e}]
j3e1 -> j3e2	[:>]
j3e2 -> j3e2	[:-]
j3e2 -> j3e3	[:_]
j3e3 -> suff	[:አ]

j3 -> j3a1		[{I2a}]
j3a1 -> j3a2	[:>]
j3a2 -> j3a2	[:-]
j3a2 -> j3a3	[:_]
j3a3 -> suff	[:ኣ]

# laryngeals are not geminated
stem -> j3o1	[{LI2o}]
stem -> j3e1	[{LI2e};{LI2a};{LI2E}]
stem -> j3a1	[{LI2a}]

# stem-final laryngeals + /e/ have three possible realizations
# stem can end in ኤ for verbs like ረአየ
stem -> stem_e		[{I2e};{LI2a};{LI2E};አ:እ;ኤ]
stem -> stem_a		[{I2a};ላ:ለ]
stem -> stem_o		[{I2o}]
stem -> stem_u		[{I2u};ቑ;ኹ;ጉ]
stem -> stem_i		[{I2i}]
stem -> stem_E		[{I2e};አ:እ]

# these may have no subject suffix and go straight to a 3p object suffix
# or delete the perf 3sm አ suffix before 3p objects

stem_e -> stem_e+	[:>]
stem_e+ -> stem_e+	[:-;:አ]
stem_e+ -> suff		[:አ]

stem_a -> stem_a+	[:>]
stem_a+ -> stem_a+	[:-;:አ]
stem_a+ -> suff		[:ኣ]

stem_o -> stem_o+	[:>]
stem_o+ -> stem_o+	[:-;:አ]
stem_o+ -> suff		[:ኦ]

# these can only be subject suffixes
stem_u -> stem_u+	[:>]
stem_u+ -> suff		[:ኡ]

stem_i -> stem_i+	[:>]
# has to be final; others converted to እ
stem_i+ -> suffi	[:ኢ]
suffi -> suffi		[:-]

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

## 3sf subjects, 3 object; perfective and converb
# geminate t
suff -> a.t			[/:]
a.t -> ato			[ቶ:ት]
ato -> ato+			[:-]
ato+ -> suff		[:ኦ]
a.t -> ata			[ታ:ት]
ata -> ata+			[:-]
ata+ -> suff		[:ኣ]
a.t -> ate			[ተ:ት]
ate -> ate+			[:-]
ate+ -> suff		[:አ]

# object suffixes without vowel infixes
suff -> suff+			[:-]
suff+ -> suff+			[/]
# are k,q possible?
suff+ -> suff			[ኒ;ን;ና;ካ;ኪ;ኩ;ክ;ዎ;ዋ;ወ;ዮ;ያ;የ;ል;ለ;ሉ;ላ;ሎ;ኻ;ኺ;ኹ;ኽ]

suff -> suff			[^N;/]

suff -> neg			[:-]
suff+ -> neg		[:-]
neg -> neg			[^N;:-]

suff+ ->
suff ->
suffi ->
neg ->
