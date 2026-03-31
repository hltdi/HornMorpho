-> conj

### subordinating conjunctions
conj -> conj	[X]
conj -> sb_pre	[:-]

### subject and negative prefixes
sb_pre -> sb_pre [X]
sb_pre -> stem1	 [<]

### STEM
stem1 -> stem 	 [X]
stem -> stem	 [X]

### subject suffixes

## c=C, c=A; V-initial subj suffix
stem -> stem._A		[{i2a};*a]
stem._A -> stem_.A 	[:>]
stem_.A -> ss	     	[:አ]
stem -> stem._U		[{a2u};{i2u}]
stem._U -> stem_.U 	[:>]
stem_.U -> ss	     	[:ኡ]
# impersonal -ኢ
stem -> stem._II	[{a2ii};{i2ii}]		[-pal]
stem._II -> stem_.II 	[:>]
stem_.II -> ss	     	[:ኢ]
# 2sf -ኢ
stem -> stem._^II	[{^a2ii};{^i2ii};ሊ:ለ;ሊ:ል]	[+pal]
stem._^II -> stem_.^II 	[:>]
stem_.^II -> ss	     	[:ኢ]
# c=A before t=p 1|2
stem -> stem._AA	[{a2aa}]
stem._AA -> stem_.AA 	[:>]
stem_.AA -> ss	     	[:ኣ]

## c=Y verbs
stem -> stem._E		[{i2e}]		[-rpal]
stem -> stem._E		[{^i2e}]	[+rpal]
stem._E -> stem_.E	[:>]
stem_.E -> ss		[:ኤ]
# palatalize final stem consonant in absence of subject suffix
stem -> stem._y		[{^i};~^*]	[+rpal]
stem._y -> stem_.y	[:>]
stem_.y -> ss		[:ይ]

## C subject suffixes
#stem ->	 stem_		[:>]
#stem_ -> ss		[CC-ይ,ነ]

# እበልነ
stem -> stem._ANe	[{a2i}]
stem._ANe -> stem_.ANe	[:>]
stem_.ANe -> ss		[ነ]		[t=i|j]

stem -> stemC		[*]
stemC -> stemC_		[:>]
stemC_ -> ss		[CC]

# C stem, no subject suffix
stemC_ -> os		[-]
# A stem, no subject suffix
stem -> stemA		[*a]
stemA -> stemA_		[:>]
stemA_ -> os		[-]

ss -> ss 		[X]
ss -> os 		[-]

## no subject suffix
#stem_ -> os		[-]

### object suffixes
os -> os [X]
os -> aux	 [-]

### auxiliary suffixes
aux -> aux    [X]

aux -> det    [-]

### definite determiner -ይ
det -> det    [X]

det ->