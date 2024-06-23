-> start

start -> start	[^N;/;:-;:<]

# consonant-final stems
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
Vposs -> end	[^N;:]

suff -> end	[^N;:]

end ->
stemC. ->
stemV. ->