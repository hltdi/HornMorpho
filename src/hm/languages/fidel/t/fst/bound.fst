-> start

start -> start	[:-]

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

firstC -> kqchange+	[:<]
C2 -> kqchange+			[:<]
V -> kqchange+			[:<]

## don't change initial k,q
C -> stem			[:<]
# no segments before stem
start -> stem		[:<]

# change initial k, q
kqchange+ -> stem		[^Qv;{kV2KV};^Q;{k2K}]

stem -> stem 		[^N;/]

stem -> stemC+		[:>]
stemC+ -> suff		[^A;-]

stem -> stem_e		[{I2e}]
stem -> stem_a		[{I2a}]
stem -> stem_o		[{I2o}]
stem -> stem_u		[{I2u}]
stem -> stem_i		[{I2i}]
stem -> stem_E		[{I2e}]

stem_e -> stem_e+	[:>]
stem_e+ -> suff		[:አ]
stem_a -> stem_a+	[:>]
stem_a+ -> suff		[:ኣ]
stem_o -> stem_o+	[:>]
stem_o+ -> suff		[:ኦ]
stem_u -> stem_u+	[:>]
stem_u+ -> suff		[:ኡ]
stem_i -> stem_i+	[:>]
stem_i+ -> suff		[:ኢ]
stem_E -> stem_E+	[:>]
stem_E+ -> suff		[:ኤ]

suff -> suff		[-;/;^N;_]

suff ->
