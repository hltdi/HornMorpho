# For WG, palatalize and labialize for +Y and +W

-> start

start -> lab   [X;C]   [+W]
start -> pal   [X;C]   [+Y]
# For NG, don't labialize or palatalize (for now)
start -> nolabpal [X;C]   [-W,-Y];[tl=M];[tl=k]

nolabpal -> nolabpal [X;C]

lab -> lab     [X;C]
pal -> pal     [X;C]

# delabialize final bilabial or velar [add -a]
lab -> lab1    [ም:ᎃ;ብ:ᎇ;ፍ:ᎋ;ፕ:ᎏ;ቅ:ቍ;ክ:ኵ;ሕ:;ግ:ጕ]            [w=1]
# depalatalize final dentals for both [+Y,+W] and [+Y,-W]
# t => c; ta -> ce
# r, n, and l not included
# OR already palatalized
pal -> pal1    [ት:ች;ስ:ሽ;ድ:ጅ;ዝ:ዥ;ጥ:ጭ;ታ:ቸ;ሳ:ሸ;ዳ:ጀ;ዛ:ዠ;ጣ:ጨ;ሽ;ች;ጅ;ዥ;ጭ]   [y=1]
# depalatalize final velars (and vowels) only for [+Y,-W]
# also include r->y and l->y here
pal -> pal1Y   [ግ:ጝ;ክ:ኽ;ቅ:ቕ:ሕ:ⷕ;ጋ:ጘ;ቃ:ቐ;ሓ:ⷐ;ካ:ኸ;ር:ይ;ል:ይ;ቕ;ኽ;ⷕ;ጝ]      [y=1,-W]
# depalatalize final -a following labials for +pal and ±lab
# (doesn't count as palatalization though)
pal -> pal1A    [ባ:በ;ማ:መ;ፋ:ፈ;ፓ:ፐ]

nolabpal ->
lab ->
lab1 ->
pal ->
pal1 ->
pal1Y ->
pal1A ->
