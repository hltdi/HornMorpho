# syllable types
# cvc; cv
# cv + cv; V -> V
# cv + c + cv; V -> C -> V

-> start

# first segment always has a vowel

start -> V		[^N]

# always spirantize following a vowel
V -> V	 		[^Qv;{kV2KV};:እ]
V -> C			[^Q-እ;{k2K}]

# geminated consonant has a vowel
V -> gem		[/]
C -> gem		[/]
gem -> V		[^N]

# coda -> onset + V
C -> V			[*-እ;:እ;*v]

V -> Vstem		[:<]
C -> stem		[:<]
start -> stem	[:<]

stem -> stemV	[*v]
stem -> stemC	[*]

Vstem -> stemV	[^Qv;{kV2KV}]
Vstem -> stemC   [^Q;{k2K}]

stemV -> stemV	[^Qv;{kV2KV}]
stemV -> stemC	[^Q-እ;{k2K}]
stemC -> stemV	[*v]
stemC -> stemC	[*]
stemV -> stemgem  [/]
stemC -> stemgem  [/]
Vstem -> stemgem  [/]
stem -> stemgem	  [/]
stemgem -> stemV  [^N]

stemC ->
stemV ->

#stem ->