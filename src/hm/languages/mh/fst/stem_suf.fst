-> start

start -> start    [u;o;V;/]


=e -> start       [:=አ]
=u -> start       [:=ኡ]
=i -> start       [:=ኢ]
# =a -> start       [:=ኣ]

# 0+e => e
start -> =e       [ለ:ል;ሐ:ሕ;መ:ም;ረ:ር;ሰ:ስ;ሸ:ሽ;ቀ:ቅ;በ:ብ;ተ:ት;ቸ:ች;ነ:ን;ኘ:ኝ;አ:እ;ከ:ክ;ወ:ው;ዘ:ዝ;ዠ:ዥ;የ:ይ;ደ:ድ;ጀ:ጅ;ገ:ግ;ጠ:ጥ;ጨ:ጭ;ፈ:ፍ;ⷐ:ⷕ;ቐ:ቕ;ኸ:ኽ;ጘ:ጝ;ቈ:ቍ;ጐ:ጕ;:;ኰ:ኵ;ᎀ:ᎃ;ᎄ:ᎇ;ᎈ:ᎋ;ᎌ:ᎏ]
# 0+u => u, e+u => o
start -> =u       [ሉ:ል;ሑ:ሕ;ሙ:ም;ሩ:ር;ሱ:ስ;ሹ:ሽ;ቁ:ቅ;ቡ:ብ;ቱ:ት;ቹ:ች;ኑ:ን;ኙ:ኝ;ኡ:እ;ኩ:ክ;ዉ:ው;ዙ:ዝ;ዡ:ዥ;ዩ:ይ;ዱ:ድ;ጁ:ጅ;ጉ:ግ;ጡ:ጥ;ጩ:ጭ;ፉ:ፍ;ⷑ:ⷕ;ቑ:ቕ;ኹ:ኽ;ጙ:ጝ;ሎ:ለ;ሖ:ሐ;ሞ:መ;ሮ:ረ;ሶ:ሰ;ሾ:ሸ;ቆ:ቀ;ቦ:በ;ቶ:ተ;ቾ:ቸ;ኖ:ነ;ኞ:ኘ;ኦ:አ;ኮ:ከ;ዎ:ወ;ዞ:ዘ;ዦ:ዠ;ዮ:የ;ዶ:ደ;ጆ:ጀ;ጎ:ገ;ጦ:ጠ;ጮ:ጨ;ፎ:ፈ;ⷖ:ⷐ;ቖ:ቐ;ኾ:ኸ;ጞ:ጘ]
# 0+i => i
start -> =i       [ሊ:ል;ሒ:ሕ;ሚ:ም;ሪ:ር;ሲ:ስ;ሺ:ሽ;ቂ:ቅ;ቢ:ብ;ቲ:ት;ቺ:ች;ኒ:ን;ኚ:ኝ;ኢ:እ;ኪ:ክ;ዊ:ው;ዚ:ዝ;ዢ:ዥ;ዪ:ይ;ዲ:ድ;ጂ:ጅ;ጊ:ግ;ጢ:ጥ;ጪ:ጭ;ፊ:ፍ;ⷒ:ⷕ;ቒ:ቕ;ኺ:ኽ;ጚ:ጝ;ቊ:ቍ;ጒ:ጕ;:;ኲ:ኵ;ᎁ:ᎃ;ᎅ:ᎇ;ᎉ:ᎋ;ᎍ:ᎏ]
# start -> =a       [ያ:የ;ባ:በ;ታ:ተ]
start -> a        [a]
start -> iE       [i;E]
start -> e        [e]

# a+i => ay ? (E?); a+u => aw (o?)
a -> start        [ው:=ኡ;:=አ;ይ:=ኢ;u;o;/]
a -> a            [a]
a -> e            [e]
a -> =e           [ለ:ል;ሐ:ሕ;መ:ም;ረ:ር;ሰ:ስ;ሸ:ሽ;ቀ:ቅ;በ:ብ;ተ:ት;ቸ:ች;ነ:ን;ኘ:ኝ;አ:እ;ከ:ክ;ወ:ው;ዘ:ዝ;ዠ:ዥ;የ:ይ;ደ:ድ;ጀ:ጅ;ገ:ግ;ጠ:ጥ;ጨ:ጭ;ፈ:ፍ;ⷐ:ⷕ;ቐ:ቕ;ኸ:ኽ;ጘ:ጝ;ቈ:ቍ;ጐ:ጕ;:;ኰ:ኵ;ᎀ:ᎃ;ᎄ:ᎇ;ᎈ:ᎋ;ᎌ:ᎏ]
a -> =u           [ሉ:ል;ሑ:ሕ;ሙ:ም;ሩ:ር;ሱ:ስ;ሹ:ሽ;ቁ:ቅ;ቡ:ብ;ቱ:ት;ቹ:ች;ኑ:ን;ኙ:ኝ;ኡ:እ;ኩ:ክ;ዉ:ው;ዙ:ዝ;ዡ:ዥ;ዩ:ይ;ዱ:ድ;ጁ:ጅ;ጉ:ግ;ጡ:ጥ;ጩ:ጭ;ፉ:ፍ;ⷑ:ⷕ;ቑ:ቕ;ኹ:ኽ;ጙ:ጝ;ሎ:ለ;ሖ:ሐ;ሞ:መ;ሮ:ረ;ሶ:ሰ;ሾ:ሸ;ቆ:ቀ;ቦ:በ;ቶ:ተ;ቾ:ቸ;ኖ:ነ;ኞ:ኘ;ኦ:አ;ኮ:ከ;ዎ:ወ;ዞ:ዘ;ዦ:ዠ;ዮ:የ;ዶ:ደ;ጆ:ጀ;ጎ:ገ;ጦ:ጠ;ጮ:ጨ;ፎ:ፈ;ⷖ:ⷐ;ቖ:ቐ;ኾ:ኸ;ጞ:ጘ]
a -> =i           [ሊ:ል;ሒ:ሕ;ሚ:ም;ሪ:ር;ሲ:ስ;ሺ:ሽ;ቂ:ቅ;ቢ:ብ;ቲ:ት;ቺ:ች;ኒ:ን;ኚ:ኝ;ኢ:እ;ኪ:ክ;ዊ:ው;ዚ:ዝ;ዢ:ዥ;ዪ:ይ;ዲ:ድ;ጂ:ጅ;ጊ:ግ;ጢ:ጥ;ጪ:ጭ;ፊ:ፍ;ⷒ:ⷕ;ቒ:ቕ;ኺ:ኽ;ጚ:ጝ;ቊ:ቍ;ጒ:ጕ;:;ኲ:ኵ;ᎁ:ᎃ;ᎅ:ᎇ;ᎉ:ᎋ;ᎍ:ᎏ]
a -> C            [C;e]
a -> iE           [i;E]

# e+e => e
e -> start        [:=አ;u;o;/]
e -> a            [a]
e -> iE           [i;E]

start -> C        [C;e]
C -> start        [u;o;/]
C -> C            [C;e]
C -> a            [a]
C -> e            [e]
C -> iE           [i;E]
C -> =e           [ለ:ል;ሐ:ሕ;መ:ም;ረ:ር;ሰ:ስ;ሸ:ሽ;ቀ:ቅ;በ:ብ;ተ:ት;ቸ:ች;ነ:ን;ኘ:ኝ;አ:እ;ከ:ክ;ወ:ው;ዘ:ዝ;ዠ:ዥ;የ:ይ;ደ:ድ;ጀ:ጅ;ገ:ግ;ጠ:ጥ;ጨ:ጭ;ፈ:ፍ;ⷐ:ⷕ;ቐ:ቕ;ኸ:ኽ;ጘ:ጝ;ቈ:ቍ;ጐ:ጕ;:;ኰ:ኵ;ᎀ:ᎃ;ᎄ:ᎇ;ᎈ:ᎋ;ᎌ:ᎏ]
C -> =u           [ሉ:ል;ሑ:ሕ;ሙ:ም;ሩ:ር;ሱ:ስ;ሹ:ሽ;ቁ:ቅ;ቡ:ብ;ቱ:ት;ቹ:ች;ኑ:ን;ኙ:ኝ;ኡ:እ;ኩ:ክ;ዉ:ው;ዙ:ዝ;ዡ:ዥ;ዩ:ይ;ዱ:ድ;ጁ:ጅ;ጉ:ግ;ጡ:ጥ;ጩ:ጭ;ፉ:ፍ;ⷑ:ⷕ;ቑ:ቕ;ኹ:ኽ;ጙ:ጝ;ሎ:ለ;ሖ:ሐ;ሞ:መ;ሮ:ረ;ሶ:ሰ;ሾ:ሸ;ቆ:ቀ;ቦ:በ;ቶ:ተ;ቾ:ቸ;ኖ:ነ;ኞ:ኘ;ኦ:አ;ኮ:ከ;ዎ:ወ;ዞ:ዘ;ዦ:ዠ;ዮ:የ;ዶ:ደ;ጆ:ጀ;ጎ:ገ;ጦ:ጠ;ጮ:ጨ;ፎ:ፈ;ⷖ:ⷐ;ቖ:ቐ;ኾ:ኸ;ጞ:ጘ]
C -> =i           [ሊ:ል;ሒ:ሕ;ሚ:ም;ሪ:ር;ሲ:ስ;ሺ:ሽ;ቂ:ቅ;ቢ:ብ;ቲ:ት;ቺ:ች;ኒ:ን;ኚ:ኝ;ኢ:እ;ኪ:ክ;ዊ:ው;ዚ:ዝ;ዢ:ዥ;ዪ:ይ;ዲ:ድ;ጂ:ጅ;ጊ:ግ;ጢ:ጥ;ጪ:ጭ;ፊ:ፍ;ⷒ:ⷕ;ቒ:ቕ;ኺ:ኽ;ጚ:ጝ;ቊ:ቍ;ጒ:ጕ;:;ኲ:ኵ;ᎁ:ᎃ;ᎅ:ᎇ;ᎉ:ᎋ;ᎍ:ᎏ]

# iu => iw; Eu => Ew; ii => i; Ei => E; ie => i; Ee => E
iE -> start       [ው:=ኡ;:=ኢ;:=አ;XX;/]
iE -> iE          [i;E]
iE -> a           [a]
iE -> C           [C;e]
iE -> e           [e]
iE -> =e          [ለ:ል;ሐ:ሕ;መ:ም;ረ:ር;ሰ:ስ;ሸ:ሽ;ቀ:ቅ;በ:ብ;ተ:ት;ቸ:ች;ነ:ን;ኘ:ኝ;አ:እ;ከ:ክ;ወ:ው;ዘ:ዝ;ዠ:ዥ;የ:ይ;ደ:ድ;ጀ:ጅ;ገ:ግ;ጠ:ጥ;ጨ:ጭ;ፈ:ፍ;ⷐ:ⷕ;ቐ:ቕ;ኸ:ኽ;ጘ:ጝ;ቈ:ቍ;ጐ:ጕ;:;ኰ:ኵ;ᎀ:ᎃ;ᎄ:ᎇ;ᎈ:ᎋ;ᎌ:ᎏ]
iE -> =u          [ሉ:ል;ሑ:ሕ;ሙ:ም;ሩ:ር;ሱ:ስ;ሹ:ሽ;ቁ:ቅ;ቡ:ብ;ቱ:ት;ቹ:ች;ኑ:ን;ኙ:ኝ;ኡ:እ;ኩ:ክ;ዉ:ው;ዙ:ዝ;ዡ:ዥ;ዩ:ይ;ዱ:ድ;ጁ:ጅ;ጉ:ግ;ጡ:ጥ;ጩ:ጭ;ፉ:ፍ;ⷑ:ⷕ;ቑ:ቕ;ኹ:ኽ;ጙ:ጝ;ሎ:ለ;ሖ:ሐ;ሞ:መ;ሮ:ረ;ሶ:ሰ;ሾ:ሸ;ቆ:ቀ;ቦ:በ;ቶ:ተ;ቾ:ቸ;ኖ:ነ;ኞ:ኘ;ኦ:አ;ኮ:ከ;ዎ:ወ;ዞ:ዘ;ዦ:ዠ;ዮ:የ;ዶ:ደ;ጆ:ጀ;ጎ:ገ;ጦ:ጠ;ጮ:ጨ;ፎ:ፈ;ⷖ:ⷐ;ቖ:ቐ;ኾ:ኸ;ጞ:ጘ]
iE -> =i          [ሊ:ል;ሒ:ሕ;ሚ:ም;ሪ:ር;ሲ:ስ;ሺ:ሽ;ቂ:ቅ;ቢ:ብ;ቲ:ት;ቺ:ች;ኒ:ን;ኚ:ኝ;ኢ:እ;ኪ:ክ;ዊ:ው;ዚ:ዝ;ዢ:ዥ;ዪ:ይ;ዲ:ድ;ጂ:ጅ;ጊ:ግ;ጢ:ጥ;ጪ:ጭ;ፊ:ፍ;ⷒ:ⷕ;ቒ:ቕ;ኺ:ኽ;ጚ:ጝ;ቊ:ቍ;ጒ:ጕ;:;ኲ:ኵ;ᎁ:ᎃ;ᎅ:ᎇ;ᎉ:ᎋ;ᎍ:ᎏ]

start ->
C ->
a ->
iE ->
