# handle vowel combination across boundaries
# and initial ኣ-> አ

-> first

first -> first	[:<]
first -> start	[**v;**;አ:ኣ;እ]

# vowel characters not possible after first character.
start -> start	[**v;**;/;:-;:>;:<]

start -> e2a	[ያ:የ;ዳ:ደ;ላ:ለ]
first -> e2a	[ያ:የ;ዳ:ደ;ላ:ለ]

e2a -> e2a		[:<]
e2a -> start	[:ኣ]

start -> I2a	[ዋ:ው;ማ:ም;ኋ:ሁ;ኛ:ኝ;ና:ን;ሃ:ህ;ሻ:ሽ;ቻ:ች;ታ:ት]
I2a -> I2a		[:>]
I2a -> start	[:ኣ]

# first character can be ኣ -> አ or any other non-vowel character

start ->