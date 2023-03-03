-> start

#start -> start        [X;C]

start -> lab   []     [+W]
start -> pal   []     [+Y]
start -> nolab []    [-W]
nolab -> nolab     [X;C]
start -> nopal []     [-Y]
nopal -> nopal     [X;C]

# start -> labpal []    [+Y,+W]

lab -> lab   [X;C]
lab -> lab2   [ም:ᎃ;ብ:ᎇ;ፍ:ᎋ;ፕ:ᎏ;ክ:ኵ;ቅ:ቍ;ግ:ጕ;መ:ᎀ;በ:ᎄ;ፈ:ᎈ;ፐ:ᎌ;ቀ:ቈ;ከ:ኰ;ገ:ጐ]     [w=2]
# class C1C2C2 verbs: duplicate final labialization
lab -> lab2d   [መ:ᎀ;በ:ᎄ;ፈ:ᎈ;ፐ:ᎌ;ም:ᎃ;ብ:ᎇ;ፍ:ᎋ;ፕ:ᎏ;ቀ:ቈ;ከ:ኰ;ሐ:;ገ:ጐ;ቕ:ቍ;ኽ:ኵ;ⷕ:;ጝ:ጕ]  [w=1,+d2,c=A]
lab2d -> lab2_ [X;C]
lab2 -> lab2_  [X;C]

pal -> pal   [X;C]
# vowel change following dental or labial (or r, n, l)
# (add palatalized consonants, and e->E)
# palatalization of velar
pal -> pal2  [ል:ሊ;ለ:ሌ;ም:ሚ;መ:ሜ;ር:ሪ;ረ:ሬ;ስ:ሲ;ሰ:ሴ;ሽ:ሺ;ሸ:ሼ;ብ:ቢ;ብ:ቤ;ት:ቲ;ተ:ቴ;ች:ቺ;ቸ:ቼ;ን:ኒ;ነ:ኔ;ዝ:ዚ;ዘ:ዜ;ዥ:ዢ;ዠ:ዤ;ድ:ዲ;ደ:ዴ;ጅ:ጂ;ጀ:ጄ;ጥ:ጢ;ጠ:ጤ;ጭ:ጪ;ጨ:ጬ;ፍ:ፊ;ፈ:ፌ;ፕ:ፒ;ፐ:ፔ;ቀ:ቐ;ሐ:ⷐ;ከ:ኸ;ገ:ጘ;ሕ:ⷕ;ቅ:ቕ;ክ:ኽ;ግ:ጝ]   [y=2,-W]
# class A C1C2C2 verbs: duplicate final palatalization
pal -> pal2d  [ሰ:ሸ;ተ:ቸ;ደ:ጀ;ዘ:ዠ;ጠ:ጨ;ስ:ሽ;ቅ:ቕ;ት:ች;ድ:ጅ;ዝ:ዥ;ጥ:ጭ]   [y=1,+d2,c=A]
pal -> pal2d  [ቀ:ቐ;ገ:ጘ;ከ:ኸ;ሐ:ⷐ;ቅ:ቕ;ግ:ጝ;ክ:ኽ;ሕ:ⷕ]  [y=1,c=A,+d2,-W]
pal2 -> pal2_  [B;W;N]
pal2d -> pal2_  [X;C]

#start ->
nolab ->
nopal ->
lab2_ ->
lab ->
pal ->
pal2_ ->
