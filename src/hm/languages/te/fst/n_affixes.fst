-> start

start -> start	[^N;/;:-;:<]	[-obl]

## Prepositions + pronouns
start -> prep0	[^N]		[+obl]
prep0 -> prep0	[^N]
prep0 -> prep1	[:-]
start -> prep1	[:-]

prep1 -> prepC	[*;/]
prep1 -> prepV	[*v]
prepV -> prepC	[*;/]
prepV -> prepV	[*v]
prepC -> prepC	[*;/]
prepC -> prepV	[*v]

prepC -> prepCe	[{I2e}]
prepC -> prepCo	[{I2o}]
prepC -> prepCu	[{I2u}]
prepC -> prepCE/ [/:]
prepC -> prepCyE [*~P]
prepV -> prepCe	[{I2e}]
prepV -> prepCo	[{I2o}]
prepV -> prepCu	[{I2u}]
prepV -> prepCE/ [/:]
prepV -> prepCyE [*~P]
prepCE/ -> prepCE	[{I2^E}]

prepV -> prepV.	[:<]
prepC -> prepC.	[:<]

prepCe -> prepCe.	[:<]
prepCo -> prepCo.	[:<]
prepCu -> prepCu.	[:<]
prepCE -> prepCE.	[:<]
prepCyE -> prepCyE.	[:<]

prepV. -> pron	[ሁ:ኡ;ሆ:ኦ;ሀ:አ;ዬ;ነ;ከ;ኪ;ኩ]
prepC. -> pron	[ነ;ከ;ኪ;ኩ;ክ]
prepCu. -> pron	[:ኡ]
prepCo. -> pron	[:ኦ]
prepCe. -> pron	[:አ]
prepCE. -> pron	[:ዬ]
prepCyE. -> pron [ዬ]
pron -> pron	[^N]
pron -> suff	[:>]

## consonant-final stems
start -> stemu	  [{I2u}]
start -> stema	  [{I2e}]
start -> stemo	  [{I2o}]
start -> stem.PyE  [/:;/]
stem.PyE ->	stemP.yE  [{I2^E}]
start -> stem~P.yE	  [*~P]
start -> stemC	  [*]

start -> stemV	[*v]
# alternate (more common) variant for stem ending in -e: ህገ -> ህግሁ
start -> stemV	[{e2I}]

stemu -> stem.u	[:>]
stem.u -> suff	[:ኡ]

stema -> stem.a	[:>]
stem.a -> suff	[:አ]

stemo -> stem.o	[:>]
stem.o -> suff	[:ኦ]

stemP.yE -> stemPy.E	[:>]
stemPy.E -> suff	[:ዬ]
stem~P.yE -> stem~Py.E	[:>]
stem~Py.E -> suff	[ዬ]

stemC -> stemC.	[:>]
stemC. -> suff	[ኩ;ክ;ከ;ኪ;ነ]

stemV -> stemV.	[:>]
stemV. -> Vposs	[ሁ:ኡ;ሀ:አ;ሆ:ኦ;ኩ;ክ;ከ;ኪ;ነ;ዬ]
Vposs -> end	[^N;:;:-]

stemV. -> suff	[:-]
stemC. -> suff	[:-]

suff -> end	[^N;:;:-]

end ->
stemC. ->
stemV. ->