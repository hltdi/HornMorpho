-> start

### adp
start -> prep	[^N]
prep -> prep	[^N]
prep -> rel	[:-]
start -> rel	[:-]

### conj1
rel -> rela	[ዝ;ክ]		[-neg]
rel -> rela	[ዚ:ዝ;ኪ:ክ]	[sg=m,sn=1,sp=3,t=i,-neg];[sp=3,sn=2,t=i,-neg]
rel -> rela	[ዘ:ዝ;ከ:ክ;ኸ:ኽ;ደ:ድ]	[+neg]
rel -> rel0	[^N]	[-rel]
rel0 -> rel0	[^N;/]
rel0 -> rela	[ተ:ት]	[+neg]
rel -> neg1	[:-]
rela -> neg1	[:-]
rel0 -> neg1	[:-]

rel -> alle1	[ዘ:ዝ;ከ:ክ;ኸ:ኽ;ደ:ድ]	[r=ህልው,-neg]
alle1 -> alle1	[:-;:<]
alle1 -> stem	[:አ]

rel -> .zeyelle.	[ዘ:ዝ]			[r=ህልው,+neg,+rel]
#.zeyelle -> ze.yelle	[:-]
#ze.yelle -> zeye.lle	[:ኣ]
#zeye.lle -> zeyelle.	[:ይ]
zeyelle. -> zeyelle.	[:-;:<]
zeyelle. -> stem	[የ]

### neg1
neg1 -> neg1a	[ኣ]	[conj1=0]
neg1 -> neg1a	[:ኣ]	[conj1=ክ|ዝ|እንተ];[adp=እንተ,conj1=0]
neg1a -> neg1b  [ይ]
neg1b -> conj2	[:-]
# affirmative
neg1 -> conj2	[:-]

### conj2
conj2 -> sbj1	[:<]
conj2 -> conj2a	[ክ;ም]
conj2a -> sbj1	[:<]

### sbj1
sbj1 -> sbj1a	[^N;/]	[t=j];[t=i,sn=2];[t=i,sp=2];[t=i,sg=f,sp=2|3]
#sbj1a -> sbj1b	[^N;/]
# delete the ipf 1s and 3sm subject prefix when there's a rel and/or neg prefix
sbj1 -> sbj1c 	[:ይ;:እ]
sbj1c -> voice	[:-]	[+neg,t=i|j,sg=m,sp=3];[+neg,t=i|j,sn=2,sp=3];[+neg,t=i|j,sp=1,sn=1];[+rel,t=i,sg=m,sp=3];[+rel,t=i,sn=2,sp=3];[+rel,t=i,sn=1,sp=1]
sbj1 -> sbj1d	[:እ]	[t=i|j,sp=1,sn=1,v=a]
sbj1d -> voice	[:-]
sbj1a -> voice	[:-]
#sbj1b -> voice	[:-]
# no sbj prefix
sbj1 -> voice	[:-]
# ይ->የ ት->ተ
sbj1 -> sbji23	[ተ:ት;የ:ይ]
sbji23 -> voicei23	[:-]

### voice prefix

voice -> voice	[አ;ተ;/]
voice -> stem0	[:-]
voicei23 -> voicei23a	[:አ]
voicei23a -> voicei23a	[ተ;/]
voicei23a -> stem0	[:-]

### stem proper and subject suffixes

# first stem consonant
stem0 -> stem		[^x]		
stem0 -> stem		[{q2Q}]	[+K1]
stem0 -> stem		[^k]		[-K1]

#stem0 -> stem		[^N]
stem -> stem		[^N;/;:-]

# stem ending in vowel
stem -> stemV.+		[*v]
# subject suffix boundary
stemV.+ -> stemV+	[:-]
stemV+ -> suff		[ኻ:ካ;ኺ:ኪ;ኹ:ኩ;ኽ:ክ;^^q;:አ;:-]
# optionally in ይ
stem -> stemy.+		[ይ]
# subject suffix boundary
stemy.+ -> stemy+	[:-]
stemy+ -> suff		[ኻ:ካ;ኺ:ኪ;ኹ:ኩ;ኽ:ክ]

## ይፍቶኪ ; I don't understand this!
#stem -> stemO		[*o]	[oinf=e,+O]
#stemO -> stemO+		[:_]
#stemO+ -> stemO+		[:-]
#stemO+ -> suffO		[:አ]
#suffO -> suffO1		[:/]
#suffO1 -> suff		[ኻ:ካ;ኺ:ኪ;ኹ:ኩ;ኽ:ክ;ኒ;ና]

# stem ending a consonant
stem -> stemC.+		[*]
# subject suffix boundary
stemC.+ -> stemC+	[:-]
# no changes before suffixes beginning with consonants or no suffix
stemC+ -> suff		[^A;:-]
# ኢ -> እ before other suffixes; object, negative (but not adverbs like ዶ)
stemC+ -> suff		[:ኢ]	[+O];[+neg,+mc,t=i]

### jussive 3 objects; geminate stem-final consonant (except laryngeals)
stem -> j3		[/:]
# add vowel suffix to stem-final consonant
j3 -> j3o1		[{^I2o}]
# subject suffix boundary
j3o1 -> j3o2	[:-]
# object suffix boundary
j3o2 -> j3o3	[:-]
j3o3 -> j3o4	[:_]
j3o4 -> suff	[:ኦ]

j3 -> j3e1		[{I2e}]
# subject suffix boundary
j3e1 -> j3e2	[:-]
j3e2 -> j3e3	[:-]
j3e3 -> j3e4	[:_]
j3e4 -> suff	[:አ]

j3 -> j3a1		[{I2a}]
# subject suffix boundary
j3a1 -> j3a2	[:-]
j3a2 -> j3a3	[:-]
j3a3 -> j3a4	[:_]
j3a4 -> suff	[:ኣ]

# laryngeals are not geminated
stem -> j3o1	[{LI2o};{La2o}]
stem -> j3e1	[{LI2e};{LI2a};{LI2E};{La2e};{La2E};ኣ;ዓ;ሓ;ሃ]
stem -> j3a1	[{LI2a};ኣ;ዓ;ሓ;ሃ]

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

# subject suffix boundary
stem_e -> stem_e+	[:-]
# object suffix boundary
stem_e+ -> stem_e+	[:-;:አ]
stem_e+ -> suff		[:አ]

# subject suffix boundary
stem_a -> stem_a+	[:-]
# object suffix boundary
stem_a+ -> stem_a+	[:-;:አ]
stem_a+ -> suff		[:ኣ]

# subject suffix boundary
stem_o -> stem_o+	[:-]
# object suffix boundary
stem_o+ -> stem_o+	[:-;:አ]
stem_o+ -> suff		[:ኦ]

# these can only be subject suffixes
# subject suffix boundary
stem_u -> stem_u+	[:-]
stem_u+ -> suff		[:ኡ]

# subject suffix boundary
stem_i -> stem_i+	[:-]
# has to be final; others converted to እ
stem_i+ -> suffi	[:ኢ]
suffi -> suffi		[:-]

# subject suffix boundary
stem_E -> stem_E+	[:-]
stem_E+ -> suff		[:ኤ]

### objects

## 3 objects with 2|3pf subjects
# optionally skip ኣ suffix
stemC+ -> suff3pfA		[:ኣ]
suff3pfA ->	suff3pfA+	[:-]
suff3pfA+ -> suff		[:እ]
suff -> suff3pfA+		[:-]

## 23pm subjects with infixed ኡ
suff -> suff_mu		[ሙ:ም]
suff_mu -> suff_mu+	[:-]
suff_mu+ -> suff		[:ኡ]

## 23pf subjects with infixed ኣ
suff -> suff_na		[ና:ን]
suff_na -> suff_na+	[:-]
suff_na+ -> suff		[:ኣ]

## 23pm subjects with 3 objects without ው
# ሰቢሮሞ ሰቢሮሞም ሰቢርኩሞ ሰቢርኩሞም
suff -> suff_mo	       	[ሞ:ም]
suff_mo -> suff_mo+	[:-]
suff_mo+ -> suff		[:ኦ]
# ሰቢሮማ ሰቢርኩማ
suff -> suff_ma		[ማ:ም]
suff_ma -> suff_ma+	[:-]
suff_ma+ -> suff		[:ኣ]
# ሰቢሮመን ሰቢርኩመን (not sure if this happens)
suff -> suff_me	    	 [መ:ም]
suff_me -> suff_me+	 [:-]
suff_me+ -> suff		 [:አ]

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

## object suffixes without vowel infixes
suff -> suff+			[:-]
suff+ -> suff+			[/]
# is k possible?
suff+ -> suff			[ኒ;ን;ና;ካ;ኪ;ኩ;ክ;ዎ;ዋ;ወ;ዮ;ያ;የ;ል;ለ;ሉ;ላ;ሎ;ኻ;ኺ;ኹ;ኽ]

suff -> suff			[^N;/]

### after object

suff -> neg			[:>]
suff+ -> neg			[:>]
neg -> neg			[^N;:-]

suff+ -> suffend		[:>]
suff -> suffend			[:>]
suffi -> suffend		[:>]

suffend -> end			[:-]

#suff+ ->
#suff ->
#suffi ->
end ->
neg ->
