-> start

start -> start	[*v]
start -> C		[*]
C -> start		[*v]
C -> C			[*-ይ]
C -> y			[ይ]

# only certain consonants are actually possible (ስ ብ ል ድ ክ ም), so this is too general.
start -> Ci		[{I2i}]
Ci -> start		[:ይ;ያ]

start ->
C ->
y ->
