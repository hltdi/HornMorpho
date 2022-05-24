-> start

start -> lab   [X;C]   [+W]
start -> pal   [X;C]   [+Y]
start -> nolabpal [X;C]   [-W,-Y]

nolabpal -> nolabpal [X;C]

lab -> lab     [X;C]
pal -> pal     [X;C]

# labialize final bilabial or velar [add -a]
lab -> lab1    [ᎃ:ም;ᎇ:ብ;ᎋ:ፍ;ቍ:ቅ;ኵ:ክ;:ሕ;ጕ:ግ]                  [w=1]
# also labialize already palatalized velars (only for Mesqan?)
# lab -> lab1P   [ቍ:ቕ;ኵ:ኽ;:ⷕ;ጕ:ጝ;ቈ:ቐ;ኰ:ኸ;:ⷐ;ጐ:ጘ]            [w=1]
# palatalize final dentals for both [+Y,+W] and [+Y,-W]
# t => c; ta -> ce
# r, n, and l not included
# OR already palatalized
pal -> pal1    [ች:ት;ሽ:ስ;ጅ:ድ;ዥ:ዝ;ጭ:ጥ;ቸ:ታ;ሸ:ሳ;ጀ:ዳ;ዠ:ዛ;ጨ:ጣ;ሽ;ች;ጅ;ዥ;ጭ]      [y=1]
# palatalize final velars (and vowels) only for [+Y,-W]
# also include r->y and l->y here
pal -> pal1Y   [ጝ:ግ;ኽ:ክ;ቕ:ቅ:ⷕ:ሕ;ጘ:ጋ;ቐ:ቃ;ⷐ:ሓ;ኸ:ካ;ይ:ር;ይ:ል;ቕ;ኽ;ⷕ;ጝ]      [y=1,-W]
# palatalize final -a following labials for +pal and ±lab
# (doesn't count as palatalization though)
pal -> pal1A    [በ:ባ;መ:ማ;ፈ:ፋ;ፐ:ፓ]

nolabpal ->
lab ->
lab1 ->
pal ->
pal1 ->
pal1Y ->
pal1A ->
