-> rel0

# distinguish stems with final laryngeal or semivowel from others
rel0 -> rel		[]	[+finX,c=A|B|C,R3=X];[+finX,c=E|F,R4=X];[+finX,c=G|H|K,R5=X];[-finX,c=A|B|C,R3=L|W];[-finX,c=E|F,R4=L|W];[-finX,c=G|H|K,R5=L|W]

rel -> rel		[^N;/]

rel -> neg		[:-]

neg -> neg		[ኢ]

neg -> sb1		[:-]

sb1 -> sb1		[^N;/]

# C -> Ce before stem Le
sb1 -> sbe		[ለ:ል;ተ:ት;ነ:ን]
sbe -> sbeS		[:<]
sbeS -> stem	[ሀ;ሐ;አ;ዐ]

# C -> Ci before stem i
sb1 -> sbi		[ሊ:ል;ቲ:ት;ኒ:ን;ኢ:እ]
sbi -> sbiS		[:<]
sbiS ->	stem	[:ኢ]

## causative 'a
# C -> Ce before causative 'a
sb1 -> cs	 	 [ለ:ል;ተ:ት;ነ:ን;አ:እ]	[t=i|j]
cs -> csS	 [:<]
csS -> csS-	 [:አ]		[v=a|at]

csS- -> stemP  		[ት]
csS- -> stemP/		[/:ት]

csS- -> csS.te		[/]
csS.te -> stemP	[ተ]

csSt -> stem	[:-]
csS- -> stem	 [:-]
csSte. -> stem [:-]

stem ->	  stemA	 [አ]		[t=p]
stemA -> stem	 [:-]

## other causative
sb1 -> csP	[:<]
csP -> stemA	[አ]
csP -> stemP	[ት]
csP -> stemP/	[/:ት]
csP -> csS.te	[/]

## passive ት
stem -> stemP	[ት]
stemP -> stem	[:-]

# geminated dentals, etc.; not possible when there is no prefix
stem -> stemP/	     	[/:ት]	       [+pre];[+neg];[+rel]
stemP/ -> stemP/-	[:-]
stemP/- -> stem		[^S]

## causative አት, አ/ተ
stem -> stemA.T			[አ]
stemA.T -> stemAT		[ት]
stemA.T -> stemA.TE	[/]
stemA.TE -> stemAT		[ተ]
stemAT -> stem			[:-]

sb1 -> stem		[:<]

stem ->	stem	[^N;/;-]

## suffixes

# ትበ/ሊዕ
stem -> stem.Li			[{I2i}]	[sp=2,sn=1,sg=f,t=i|j]
stem.Li -> stemL.i		[እ;ዕ;ህ;ሕ]
stemL.i -> stemLi.		[:>]
stemLi. -> sb2			[:ኢ]

# ትበ/ሉዕ
stem -> stem.Li			[{I2u}]	[sn=2,sg=m,t=i|j]
stem.Li -> stemL.i		[እ;ዕ;ህ;ሕ]
stemL.i -> stemLi.		[:>]
stemLi. -> sb2			[:ኡ]

# ሰብረ ; ልሰብረ/ከ
stem -> stem_e	[{I2e}]
stem_e -> _e	[:>]
_e -> sb2	        [:አ]
_e -> e_ob		[:-]
e_ob -> ob		[:አ]

# ልሰብሮ ስበሮ ትሰብሮ
stem -> stem_o	[{I2o}]
stem_o -> _o	[:>]
_o -> sb2	        [:ኦ]		[sn=2,sg=m]

# ልበ/ልዑ
stem -> stem_u	[{I2u}]
stem_u -> _u	[:>]
_u -> sb2	        [:ኡ]		[sn=2,sg=m]

# ትሰብሪ
stem -> stem_i	[{I2i}]
stem_i -> _i	[:>]
_i -> sb2	        [:ኢ]		[sp=2,sn=1,sg=f]

# ትሸቂ 
stem -> stem.Ei	[{E2i}]	[t=i]
stem.Ei -> stemE.i	[:>]
stemE.i -> sb2	[:ኢ]

# ልሸቁ
stem -> stem.Eu	[{E2u}]	[t=i]
stem.Eu -> stemE.u	[:>]
stemE.u -> sb2	[:ኡ]

# ትሽቀይ ትሽቀው
stem -> stem.eIo		[*e]
stem.eIo -> steme.Io	[:>]
steme.Io -> sb2			[ይ:ኢ;ው:ኡ]

# ሸቄት
stem -> stemE			[*E]
stemE -> stemE.			[:>]
stemE. -> sb2			[:አ]

## objects

# ትሰ/ቢሮ ; (ት)ስቤሮ
stem -> stem_in_i			[{I2i};{e2E}]	[op=3,sp=2,sn=1,sg=f,t=i|j,+finX]
# prevent this from happening for root-final L
stem_in_i -> stem_in_iC	[{^I2o}]
stem_in_iC -> sb2f_o		[:>]
sb2f_o -> obo				[:=ኢ]
obo -> obo_					[:-]
obo_ -> ob					[:ኦ]

# ትሰ/ቡሮ ; ስቦሮ
stem -> stem_in_u			[{I2u};{e2o}]	[op=3,sn=2,sg=m,+finX]
# prevent this from happening for root-final L
stem_in_u -> stem_in_uC	[{^I2o}]
stem_in_uC -> sbmp_o		[:>]
sbmp_o -> obo				[:=ኡ]

## 2sf subj, 3 obj; stem-final L/W
#stem -> 

# ልስ/ብ_ሮ (no subj suffix)
_o -> obj_o		[:-]		[sn=1,op=3];[sp=1,sn=2,op=3]
obj_o -> obj_o	[_]
obj_o -> ob		[:ኦ]

# ቀትሌ/ኒ
stem -> stem_E	[{I2E}]	[op=1|2]
stem_E -> _E	[:>]
_E -> sb.ob_E	[:ኤ]
sb.ob_E -> ob	[:-]

# ልው/ድዮ
stem -> stemE2I		[{E2I}]	[op=3]
stemE2I -> stemE2I_	[:>]
stemE2I_ -> stemE2I.3	[:-]
stemE2I.3 -> ob			[ዮ:ኦ]

# consonant-initial subj suffix or no subj suffix
stem -> stemL	[^N]
stemL -> sbC	[:>]
sbC -> sb2		[*V;**]
sbC -> ob		[:-]

sb2 -> sb2		[^N;/]
# objects that don't merge with stem or subject suffixes
sb2 -> ob		[:-]

## subject suffixes + object suffixes
# ሰበርክነኒ
sb2 -> sb_e		[ነ:ን;ተ:ት]
sb_e -> sb_e.	[:-]
sb_e. -> ob		[:አ]

# ሰብረቶ ሰብረዎ ሰበርኩሞ
sb2 -> sb_oO	[ቶ:ት;ዎ:ው;ሞ:ም]
sb_oO -> sb_oO.	[:-]
sb_oO. -> ob	[:ኦ]

ob ->  ob		[^N;/]

ob ->
end ->
