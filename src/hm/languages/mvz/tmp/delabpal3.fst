-> start

#start -> start [X;C]

start -> lab   []  [+W]
start -> pal   []  [+Y]
start -> nopal  []  [-Y]
start -> nolab  []  [-W]
nopal -> nopal  [X;C]
nolab -> nolab  [X;C]

lab -> lab   [X;C]
lab -> lab3   [ም:ᎃ;ብ:ᎇ;ፍ:ᎋ;ፕ:ᎏ;ክ:ኵ;ቅ:ቍ;ግ:ጕ;መ:ᎀ;በ:ᎄ;ፈ:ᎈ;ፐ:ᎌ;ቀ:ቈ;ከ:ኰ;ገ:ጐ] [w=3]
lab3 -> lab3_  [X;C]
lab3_ -> lab3__ [X;C]
# as=it (A,B,C): duplicate C2 labialization
lab -> lab3i   [መ:ᎀ;በ:ᎄ;ፈ:ᎈ;ፐ:ᎌ;ም:ᎃ;ብ:ᎇ;ፍ:ᎋ;ፕ:ᎏ;ቀ:ቈ;ከ:ኰ;ሐ:;ገ:ጐ;ማ:ሟ;ባ:ቧ;ፋ:ፏ;ፓ:ፗ;ቃ:ቋ;ካ:ኳ;ሓ:ሗ;ጋ:ጓ]  [w=2,as=it]
lab3i -> lab3_  [X;C]
lab3i_ -> lab3i__ [X;C]

pal -> pal    [X;C]
# in this position palatalize only velars? no vowel changes?
# vowel is -e, -a, or -o
pal -> pal3   [ሐ:ⷐ;ቀ:ቐ;ከ:ኸ;ገ:ጘ;ሓ:ⷓ;ቃ:ቓ;ካ:ኻ;ጋ:ጛ;ሖ:ⷖ;ቆ:ቖ;ኮ:ኾ;ጎ:ጞ]   [y=3]
pal3 -> pal3_   [X;C]
pal3_ -> pal3__ [X;C]
# as=it (A,B,C): duplicate C2 palatalization
pal -> pal3i  [ሐ:ⷐ;ቀ:ቐ;ከ:ኸ;ገ:ጘ;ሓ:ⷓ;ቃ:ቓ;ካ:ኻ;ጋ:ጛ]  [y=2,as=it]
pal3i -> pal3i_  [X;C]
pal3i_ -> pal3i__ [X;C]

nolab ->
nopal ->
lab ->
pal ->
lab3__ ->
pal3__ ->
lab3i__ ->
pal3i__ ->
