# Handle cases where stem-final w or y is followed by different segments

-> start

# Ignore consonants
start -> start       [!;L;-;>]

# Worry about vowels in case they precede w
# Change vowel to o(o) before w>f-
start -> v>o         [{v2o};o;oo]
# w changes to f
v>o -> v>o.w>f       [f:w]
# Delete the - or >
v>o.w>f -> v>o.w>f-  [:-;:>]
# This happens only before t, n, and (usually) s suffixes
v>o.w>f- -> start    [n;t;s]

# Now the vowel before y (not clear which ones remain unchanged)
# dandeenya, dandeessa
start -> v>e	[{v2ee};ee;oo;uu]
# y goes away
v>e -> v>e.y         [:y]
# Delete the - or >
v>e.y -> v>e.y+      [:-;:>]
# s -> ss, t -> ss, n -> ny
v>e.y+ -> v>e.y+t    [s:t;s]
v>e.y+t -> start     [s:]
v>e.y+ -> start      [ny:n]

# Vowels in other situations
start -> v           [$]
# Any other following consonant
v -> start           [!-w,y;L;-;>]
# Followed by w or y, which can also be changed to ',h
# +++ Simplify for generation +++
v -> vw|y            [w;':w;y:w;h:w;w:y;':y;y;h:y]
# Delete following - or >
vw|y -> vw|y+        [:-;:>]
# ... and then a vowel
vw|y+ -> start       [$]
# vw|y not before -
vw|y -> start        [$]
# w or y after vowel in other cases
v -> wy              [w;y]
wy -> start          [$;!;-;>]

start ->
v ->
