-> start

start -> start [X;C]

start -> lab   []     [+W]
start -> pal   []     [+Y]
# start -> labpal []    [+Y,+W]

lab -> lab   [X;C]
lab -> lab2   [ᎃ:ም;ᎇ:ብ;ᎋ:ፍ;ኵ:ክ;ቍ:ቅ;ጕ:ግ;ᎀ:መ;ᎄ:በ;ᎈ:ፈ;ቈ:ቀ;ኰ:ከ;ጐ:ገ]     [w=2]
# class C1C2C2 verbs: duplicate final labialization
lab -> lab2d   [ᎀ:መ;ᎄ:በ;ᎈ:ፈ;ᎃ:ም;ᎇ:ብ;ᎋ:ፍ;ቈ:ቀ;ኰ:ከ;:ሐ;ጐ:ገ;ቍ:ቕ;ኵ:ኽ;:ⷕ;ጕ:ጝ]  [w=1,+d,c=A]
lab2d -> lab2_ [X;C]
lab2 -> lab2_  [X;C]

pal -> pal   [X;C]
# vowel change following dental or labial (or r, n, l)
# palatalization of velar
pal -> pal2  [ቲ:ት;ሲ:ስ;ዲ:ድ;ዚ:ዝ;ጢ:ጥ;ኸ:ከ;ኽ:ክ]   [y=2,-W]
# class A C1C2C2 verbs: duplicate final palatalization
pal -> pal2d  [ሸ:ሰ;ቸ:ተ;ጀ:ደ;ዠ:ዘ;ጨ:ጠ;ሽ:ስ;ቕ:ቅ;ች:ት;ጅ:ድ;ዥ:ዝ;ጭ:ጥ]   [y=1,+d,c=A]
pal -> pal2d  [ቐ:ቀ;ጘ:ገ;ኸ:ከ;ⷐ:ሐ;ቕ:ቅ;ጝ:ግ;ኽ:ክ;ⷕ:ሕ]  [y=1,c=A,+d,-W]
pal2 -> pal2_  [X;C]
pal2d -> pal2_  [X;C]

start ->

lab2_ ->
lab ->
pal ->
pal2_ ->
