# yI prefix
# CIy(I) -> Ci
# CIye -> Ce

-> start

## The first character doesn't matter
start -> C      [X-y;_]
C -> C          [X-y;_]
C -> V          [V-I]
start -> V      [V]
V -> C          [X-y]

start -> y      [y]
V -> y          [y]
y -> V          [V-I]
y -> yI         [I]
yI -> C         [X-y]
y -> C          [X-y]
y -> y          [_]

## delete I
C -> I-         [:I]
# ... before y(I)C or ye
I- -> y-        [:y]
# for generation, only y->i
I- -> y>i       [i:y]
## keep I
C -> I          [I]
# ... before a consonant other than y
I -> C          [X-y]
# ... or before geminated y
I -> Iy         [y]
Iy -> C         [_]
# ... or y followed by a vowel other than e or I
Iy -> V         [V-e,I]

## y -> i (not I for generation)
C   -> y>i      [i:y]
# ... before (I)C
y>i -> C        [X]
y>i -> y>iI     [:I]
y>iI -> C       [X]
## delete y
C  -> y-        [:y]
# ... before e
y- -> y-e       [e]
y-e -> C        [X]
## keep y
C  -> Cy         [y]
# ... when it's followed by a vowel other than e or I
Cy -> V          [V-e,I]
# ... or by a consonant, or when it's geminated
Cy -> C          [X;_]

C ->
V ->
y ->
y>i ->
y-e ->
