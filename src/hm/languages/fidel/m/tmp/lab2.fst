-> start

start -> start [X;C]

start -> lab   []     [+W]
start -> pal   []     [+Y]
# start -> labpal []    [+Y,+W]

lab -> lab   [X;C]
lab -> lab2   [ᎃ:ም;ᎇ:ብ;ᎋ:ፍ;ᎏ:ፕ;ኵ:ክ;ቍ:ቅ;ጕ:ግ;ᎀ:መ;ᎄ:በ;ᎈ:ፈ;ᎌ:ፐ;ቈ:ቀ;ኰ:ከ;ጐ:ገ]     [w=2]
# class C1C2C2 verbs: duplicate final labialization
lab -> lab2d   [ᎀ:መ;ᎄ:በ;ᎈ:ፈ;ᎌ:ፐ;ᎃ:ም;ᎇ:ብ;ᎋ:ፍ;ᎏ:ፕ;ቈ:ቀ;ኰ:ከ;:ሐ;ጐ:ገ;ቍ:ቕ;ኵ:ኽ;:ⷕ;ጕ:ጝ]  [w=1,+d,c=A]
lab2d -> lab2_ [X;C]
lab2 -> lab2_  [X;C]

pal -> pal   [X;C]
# vowel change following dental or labial (or r, n, l)
# (add palatalized consonants, and e->E)
# palatalization of velar
pal -> pal2  [ሊ:ል;ሌ:ለ;ሚ:ም;ሜ:መ;ሪ:ር;ሬ:ረ;ሲ:ስ;ሴ:ሰ;ሺ:ሽ;ሼ:ሸ;ቢ:ብ;ቤ:በ;ቲ:ት;ቴ:ተ;ቺ:ች;ቼ:ቸ;ኒ:ን;ኔ:ነ;ዚ:ዝ;ዜ:ዘ;ዢ:ዥ;ዤ:ዠ;ዲ:ድ;ዴ:ደ;ጂ:ጅ;ጄ:ጀ;ጢ:ጥ;ጤ:ጠ;ጪ:ጭ;ጬ:ጨ;ፊ:ፍ;ፌ:ፈ;ፒ:ፕ;ፔ:ፐ;ቐ:ቀ;ⷐ:ሐ;ኸ:ከ;ጘ:ገ;ⷕ:ሕ;ቕ:ቅ;ኽ:ክ;ጝ:ግ]   [y=2,-W]
# class A C1C2C2 verbs: duplicate final palatalization
pal -> pal2d  [ሸ:ሰ;ቸ:ተ;ጀ:ደ;ዠ:ዘ;ጨ:ጠ;ሽ:ስ;ቕ:ቅ;ች:ት;ጅ:ድ;ዥ:ዝ;ጭ:ጥ]   [y=1,+d,c=A]
pal -> pal2d  [ቐ:ቀ;ጘ:ገ;ኸ:ከ;ⷐ:ሐ;ቕ:ቅ;ጝ:ግ;ኽ:ክ;ⷕ:ሕ]  [y=1,c=A,+d,-W]
pal2 -> pal2_  [B;W;N]
pal2d -> pal2_  [X;C]

start ->

lab2_ ->
lab ->
pal ->
pal2_ ->
