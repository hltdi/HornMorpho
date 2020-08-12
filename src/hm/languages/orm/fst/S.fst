## S: suffix suffix
## after consonant: 0
## after single vowel: replace vowel and add -ni
## after double vowel: -n

-> start

start -> start [%;$$]

## consonant
start -> C     [!!]
C -> CC        [!]
CC -> V        [$]
# after double consonants, suffix is only -i
CC -> CCV.S    [:a;:e;:i;:o;:u]
# no S suffix after C
C -> end       [:S]
# a special character
C -> V         [%-S]
# a vowel...
# keep it if it's long
C -> VV.S      [$2]
# delete it if it's short
C -> V.S       [:a;:e;:i;:o;:u]
# ... before anything but S
C -> V         [$]
C -> VV        [$2]

## vowel
# single vowel without S after it
V -> C         [!1]
V -> V         [%-S]
# ch, etc. count as double consonants
V -> CC        [!2]
# double vowel without S after it
VV -> C        [!1]
VV -> VV       [%-S]
VV -> CC       [!2]
## S suffixes following vowels
# -ni/-ti after deleted short vowel
V.S -> end     <ni:S>          [-fem]  # (or maybe no specified gender)
V.S -> end     <ti:S>          [+fem]
# -i after double consonant
CCV.S -> end   [i:S]
# -n after long vowel
VV.S -> end    [n:S]

end -> end     [$;!;%]

end ->
C ->
V ->
VV ->