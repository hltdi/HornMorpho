# handle characters at the boundary between stem and suffixes

-> start

# adposition; no negation
start -> adpV	[*v]
start -> adpC	[*]
adpV -> adpV	[*v]
adpC ->	adpV	[*v]
adpC -> adpC	[/;*]
adpV -> adpC	[/;*]
# ምስ ከም
adpV -> adpCa	[{I2a};*e]
adpC -> adpCa	[{I2a};*e]
adpC -> preC	[:-]
adpV -> preV	[:-]
adpC -> preV	[:-]
adpCa -> preCa	[:-]
# ኣብ + ኣየናይ -> ኣበየናይ
adpV -> adpCe	[{I2e}]
adpC -> adpCe	[{I2e}]
start -> adpCe	[{I2e}]
adpCe -> preCe	[:-]
# መእንትኡ
adpC -> adpA	[{A2I}]
adpA -> preA	[:-]
# ምእንታኻ (ምእንታ + ኣኻ)
adpC -> adpAA 	[*a]
adpAA -> preAA	[:-]
preAA -> aastem	[:<]
aastem -> stemV	[:ኣ]	[pos=PRON,-dem,-neg]
# ን-<እቲ> -> ነቲ
start -> nbdet1		[ነ:ን;በ:ብ]	[adp=ን|ብ]
nbdet1 -> nbdet2	[:-]
nbdet2 -> nbdet3	[:<]
nbdet3 -> stemV		[:እ]	[pos=PRON|DET,+dem,-neg]

# no adposition
start -> neg0	[:-]
# negation
neg0 -> neg1	<ኣይ>
neg0 -> neg1	<ዘይ>

# stem
neg1 -> stem0	[:<]
neg0 -> stem0	[:<]

preV -> Vstem	[:<]
preC -> Cstem	[:<]
preV -> NAstem	[:<]	[pos=N|ADJ|PROPN|ADV]
preC -> NAstem	[:<]	[pos=N|ADJ|PROPN|ADV]
preCa -> Castem	[:<]
preCe -> Cestem	[:<]
preA -> Astem	[:<]

# k->K, q->Q for nouns and adjectives with prepositions
NAstem -> stem0	[^^K;{q2Q}]

# what to do with prepositions before pronouns
Vstem -> stemC	[*-እ;:እ]       [pos=PRON|DET]
Cstem -> stemC	[*-እ;:እ]	[pos=PRON|DET,+dem]
Cstem -> stemC	[*]			[pos=PRON,-dem]
Cstem -> stemV	[*v]		[pos=PRON]
Vstem -> stemV	[*v]		[pos=PRON]
Castem -> stemV	[:ኣ]		[pos=PRON,-dem]
Cestem -> stemV	[:ኣ]		[pos=PRON|DET,-pers]
# ምእንትኡ
Astem -> stemV	[ኡ;ኣ;ኦ;ኤ]	[pos=PRON,-dem]

stem0 -> stemC	[*;/]
stem0 -> stemV	[*v]

stemC -> stemC	[*;/]
stemC -> stemV	[*v]

stemV -> stemC	[*;/]
stemV -> stemV	[*v]

# C -> Cu, etc.
stemV -> stemu	[{I2u}]
stemC -> stemu	[{I2u}]
stemV -> stema	[{I2a}]
stemC -> stema	[{I2a}]
stemV -> stemo	[{I2o}]
stemC -> stemo	[{I2o}]
stemV -> steme	[{I2e}]
stemC -> steme	[{I2e}]
stemV -> stemE	[{I2e}]
stemC -> stemE	[{I2e}]
# ምውድኡ alongside ምውዳኡ
stemC -> stemAI	[{a2I}]	# [d=inf]
stemAI -> stemAIu	[ኡ:እ;ዑ:ዕ;ሑ:ሕ;ሁ:ህ]
stemAI -> stemAIa	[ኣ:እ;ዓ:ዕ;ሓ:ሕ;ሃ:ህ]
stemAI -> stemAIE	[አ:እ;ዓ:ዕ;ሐ:ሕ;ሀ:ህ]
stemAI -> stemAIe	[አ:እ;ዓ:ዕ;ሐ:ሕ;ሀ:ህ]
stemAI -> stemAIo	[ኦ:እ;ዖ:ዕ;ሖ:ሕ;ሆ:ህ]
stemAIu -> usuff	[:>]
stemAIa -> asuff	[:>]
stemAIe -> esuff	[:>]
stemAIo -> osuff	[:>]
stemAIE -> Esuff	[:>]

# Ci -> C* for epenthetic -i
stemC -> stemi_		[{i2I}]
stemC -> stemi2e	[{i2e}]
stemC -> stemi2u	[{i2u}]
stemC -> stemi2a	[{i2a}]
stemC -> stemi2o	[{i2o}]
stemC -> stemi2E	[{i2e}]

# changes to other stem-final vowels; all optional
# -i (not epenthetic)
stemV -> stemi2I   	[{i2I}]
# -a
stemV -> stemV2I	[{a2I}]
stemC -> stemV2I	[{a2I}]
# ለቕሓ + አይ -> ለቕሐይ
stemC -> stemLa2e	[ሐ:ሓ;ሀ:ሃ;ዓ:ዐ;ኣ:አ]
stemV -> stemLa2e	[ሐ:ሓ;ሀ:ሃ;ዓ:ዐ;ኣ:አ]
stemLa2e -> Vsuff	[:>]	[+sv]
# -e; and other vowels?
stemV -> stemV2I	[{e2I}]
stemC -> stemV2I	[{e2I}]
# -u
stemV -> stemV2I	[{u2I}]
stemC -> stemV2I	[{u2I}]
# -o
stemV -> stemV2I	[{o2u}]
stemC -> stemV2I	[{o2u}]

# unchanged stem final vowels and consonants
stemV -> Vsuff	[:>]   [+sv]
stemC -> Csuff	[:>]   [-sv]

# possessive suffixes beginning with vowels following stem C
stemu -> usuff	[:>]
usuff -> poss	[:ኡ]
stema -> asuff	[:>]
asuff -> poss	[:ኣ]
stemo -> osuff	[:>]
osuff -> poss	[:ኦ]
steme -> esuff	[:>]
esuff -> poss	[:አ]
stemE -> Esuff	[:>]
Esuff -> poss	[:ኤ]

# stem ending with epenthetic i
# 2nd person; 1p
stemi_ -> i_suff   [:>]
i_suff -> poss	   [ኻ:ካ;ኺ:ኪ;ኹ:ኩ;ኽ:ክ;ና]
# 1s
stemi2e -> i2e_suff	[:>]
i2e_suff -> poss	[:አ]
# 3p; vowel possessive suffixes
stemi2u -> i2u_suff    [:>]
stemi2a -> i2a_suff    [:>]
stemi2o -> i2o_suff    [:>]
stemi2E -> i2E_suff    [:>]
i2u_suff -> poss	[:ኡ]
i2a_suff -> poss	[:ኣ]
i2o_suff -> poss	[:ኦ]
i2E_suff -> poss	[:ኤ]
i_suff -> i_suff_	[:-]
i_suff_ -> neg2		[ን]
i_suff_ -> i_suff__	[:-]
i_suff__ -> cnj		[ኸ:ከ;ን;ስ;ሲ; ዶ;/]

stemV2I -> V2i_suff	[:>]
V2i_suff -> poss	[ኡ;ኦ;ኣ;ኤ]

# possessive suffixes following stem-final vowels
Vsuff -> poss	[ኻ:ካ;ኺ:ኪ;ኹ:ኩ;ኽ:ክ;ና;:አ;ኡ;ኣ;ኦ;ኤ]
Csuff -> poss	[ካ;ኪ;ኩ;ክ;ና]

poss -> poss	[^N]

# no possessive
Vsuff -> neg2	[:-]
Csuff -> neg2	[:-]
poss -> neg2	[:-]
stem_i -> i_neg2	[:-]

neg2 -> neg2	[ን]
i_neg2 -> neg2	[ን]
neg2 -> cnj		[:-]

cnj -> cnj		[^^Q]
# keep the k in ke
cnj -> cnj		[ከ]		[+neg];[-neg,p=s1];[-neg,p=pm2];[-neg,p=pf2];[-neg,p=pm3];[-neg,p=pf3];[-sv,-neg,p=0]
# ከ -> ኸ
cnj -> cnj		[ኸ:ከ]	[-neg,p=p1];[-neg,p=sm2];[-neg,p=sf2];[-neg,p=sm3];[-neg,p=sf3];[+sv,-neg,p=0]

cnj ->
