# Handle cases where stem-final ' is followed by different segments
#
# ' is dropped before -t, -n, or -s, and
# if not preceded by a long vowel and not already long, the last vowel
# of the stem is lengthened
# 
# ' is maintained before -V, or replaced by h, w, or y

-> start

## start: initial consonant
start -> start       [!;L]

## 1: any vowel
start -> 1           [$]
# Stay in 1 for any C(CC)V sequence
1 -> 1loopa          [!;L]
# Second consonant
1loopa -> 1loopb     [!]
# Third consonant
1loopb -> 1loopc     [!]
1loopa -> 1          [$]
1loopb -> 1          [$]
1loopc -> 1          [$]

## 2: long V + C
start -> 2a          [$2]
2a -> 2b             [!;L]
2b -> 2              [:;!]
# Stay in 2 for any C(C) sequence
2 -> 2loopa          [$2]
2loopa -> 2loopb     [!;L]
2loopb -> 2          [:;!]

## 3: short V + C
start -> 3a          [$1]
3a -> 3b             [!;L]
3b -> 3              [:;!]
# Stay in 3 for any C(C) sequence
3 -> 3loopa          [$1]
3loopa -> 3loopb     [!;L]
3loopb -> 3          [:;!]

## 4: vowel lengthening
## 2 + V; 3 + VV:V; start + VV:V
2 -> 4               [$]
3 -> 3v              [$1]
3v -> 4              [L:]
start -> startv      [$1]
startv -> 4          [L:]

## 5: end state
# Stay in 5 for any C, V, or special suffix characters
5 -> 5               [!;$;%]

## Move between 2 and 3 with sequences of long/short V+(C)C
2 -> 2>3a            [$1]
2>3a -> 2>3b         [!;L]
2>3b -> 2>3          [:;!]

3 -> 3>2a            [$2]
3>2a -> 3>2b         [!;L]
3>2b -> 2            [:;!]

## Get to 5
# Anything but -'+
1 -> 1>5a            [!-';L]
1>5a -> 1>5b         [:;!]
# Keep the + if there is one
1>5b -> 5            [+;:]

# analysis: -'+V: preserve ' or replace with h, y, or w
# !! generation: only '
1 -> 1>5'            [';y:';w:';h:']
# Delete the +
1>5' -> 1>5'+        [:+]
# Vowel follows
1>5'+ -> 5           [$]

# '+C
# Delete the '
4 -> 4>5a            [:']
# Delete the + before t or n
4>5a -> 4>5b         [:+]
4>5b -> 5            [t;n]
# Find the + after s
4>5a -> 4>5c         [s]
4>5c -> 5            [:+]

5 ->