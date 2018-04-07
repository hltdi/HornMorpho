# yI prefix
# CIy(I) -> Ci (-> CI)
# CIye -> Ce

-> start

## The first character doesn't matter
start -> C      [X;_]
C -> C          [X-y;_]
C -> V          [V-I]
start -> V      [V]
V -> C          [X]

## delete I
C -> I-         [:I]
# ... before y(I)C or ye
I- -> y-        [:y]
I- -> y>i       [i:y]
I- -> y>I       [I:y]
## keep I
C -> I          [I]
# ... before a consonant other than y
I -> C          [X-y]
# ... or before geminated y
I -> Iy         [y]
Iy -> C         [_]
# ... or y followed by a vowel other than e or I
Iy -> V         [V-e,I]

## y -> i/I
# Keep these states separate because only i can end a word
C   -> y>i      [i:y]
C   -> y>I      [I:y]
# ... before (I)C
y>i -> C        [X]
y>I -> C        [X]
y>i -> y>iI     [:I]
y>I -> y>iI     [:I]
y>iI -> C       [X]
## delete y
C  -> y-        [:y]
# ... before e
y- -> y-e       [e]
y-e -> C        [X]
## keep y
C  -> y         [y]
# ... when it's followed by a vowel other than e or I
y -> V          [V-e,I]
# ... or by a consonant, or when it's geminated
y -> C          [X;_]

C ->
V ->
y ->
y>i ->
y-e ->
