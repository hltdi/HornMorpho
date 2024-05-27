-> start

start -> start [X;C]

start -> lab   []  [+W]
start -> pal   []  [+Y]

lab -> lab   [X;C]
lab -> lab3   [ᎃ:ም;ᎇ:ብ;ᎋ:ፍ;ኵ:ክ;ቍ:ቅ;ጕ:ግ;ᎀ:መ;ᎄ:በ;ᎈ:ፈ;ቈ:ቀ;ኰ:ከ;ጐ:ገ;ᎂ:ሜ;ᎆ:ቤ;ᎊ:ፌ;ኴ:ኬ;ቌ:ቄ;ጔ:ጌ;:ሔ] [w=3]
lab3 -> lab3_  [X;C]
lab3_ -> lab3__ [X;C]
# as=it (A,B,C): duplicate C2 labialization
lab -> lab3i   [ᎀ:መ;ᎄ:በ;ᎈ:ፈ;ᎌ:ፐ;ᎃ:ም;ᎇ:ብ;ᎋ:ፍ;ᎏ:ፕ;ቈ:ቀ;ኰ:ከ;:ሐ;ጐ:ገ;ሟ:ማ;ቧ:ባ;ፏ:ፋ;ፗ:ፓ;ቋ:ቃ;ኳ:ካ;ሗ:ሓ;ጓ:ጋ]  [w=2,as=it]
lab3i -> lab3_  [X;C]
lab3i_ -> lab3i__ [X;C]

pal -> pal    [X;C]
# in this position palatalize only velars? no vowel changes?
# vowel is -e, -a, or -o
pal -> pal3   [ⷐ:ሐ;ቐ:ቀ;ኸ:ከ;ጘ:ገ;ⷓ:ሓ;ቓ:ቃ;ኻ:ካ;ጛ:ጋ;ⷖ:ሖ;ቖ:ቆ;ኾ:ኮ;ጞ:ጎ]
pal3 -> pal3_   [X;C]
pal3_ -> pal3__ [X;C]
# as=it (A,B,C): duplicate C2 palatalization
pal -> pal3i  [ⷐ:ሐ;ቐ:ቀ;ኸ:ከ;ጘ:ገ;ⷓ:ሓ;ቓ:ቃ;ኻ:ካ;ጛ:ጋ]  [y=2,as=it]
pal3i -> pal3i_  [X;C]
pal3i_ -> pal3i__ [X;C]

start ->
lab3__ ->
pal3__ ->
lab3i__ ->
pal3i__ ->
