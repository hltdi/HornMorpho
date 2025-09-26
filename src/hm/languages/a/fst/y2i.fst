# ሲመጣ እንዲመጡ የሚያመጣ, etc.
-> start

start -> start	[*v;/;ይ]
start -> C		[*-ይ]
C -> start		[*v]
C -> C			[*-ይ;/]
C -> y			[ይ]

# only certain consonants are actually possible (ስ ብ ል ድ ክ ም), so this is too general.
start -> Ci		[{*I2i}]
C -> Ci	 		[{*I2i}]
Ci -> start		[:ይ;ያ]

start ->
C ->
y ->

