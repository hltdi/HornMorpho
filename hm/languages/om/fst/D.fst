## D: initial vowel in definite suffix
##    replace final vowel (short or long) in stem with, add i after consonant

-> start

# special characters
start -> start [%;$$]

## consonant
start -> C     [!!]
# replace D with i, expect consonant next
C -> end       [i:D]
# another consonant or special character
C -> C         [!;%-D]
# a vowel...
# keep it
C -> V         [$]
# delete it
C -> V.D       [i:a;i:e;i;i:o;i:u;i:aa;i:ee;i:ii;i:oo;i:uu]

## vowel
# a consonant or special character
V -> C         [!;%-D]

# replaced vowel before D
# expect vowel next
V.D -> end     [:D]

end -> end     [$;!;%]

end ->
C ->
V ->