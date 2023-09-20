# handle vowel combination across boundaries
# and initial ኣ-> አ

-> first

start -> e2a	[ያ:የ;ዳ:ደ;ላ:ለ;ና:ነ;ኛ:ኝ;ኋ:ሁ;ሻ:ሽ;ዋ:ው;ሃ:ህ]
first -> e2a	[ያ:የ;ዳ:ደ;ላ:ለ;ና:ነ;ኛ:ኝ;ኋ:ሁ;ሻ:ሽ;ዋ:ው;ሃ:ህ]

e2a -> e2a		[:-;:>]

e2a -> start	[:ኣ]

start -> e2u	[ሉ:ለ]
first -> e2u	[ሉ:ለ]

e2u -> e2u+		[:-;:>]

e2u+ -> start	[:ኡ]

start -> e+e	[ለ]
e+e -> e+e>		[:>]
e+e> -> start	[:አ]

# vowel characters not possible after first character.
start -> start	[**v;**;/;:-;:>;:<]

first -> first	[:-;:<]

# first character can be ኣ -> አ or any other non-vowel character
first -> start	[**v;**;አ:ኣ]

start ->