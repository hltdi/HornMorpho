## P: initial character in plural suffix
##    replace final vowel (short or long) in stem, do nothing after consonant

-> start

# special characters
start -> start [%;$$]

## consonant
start -> C     [!!]
# delete the P, expect vowel next
C -> end       [:P]
# another consonant or special character
C -> C         [!;%-P]
# a vowel...
# keep it
C -> V         [$]
# delete it
C -> V.P       [:a;:e;:i;:o;:u;:aa;:ee;:ii;:oo;:uu]

## vowel
# a consonant or special character
V -> C         [!;%-P]

# deleted vowel before P
# expect vowel next
V.P -> end     [:P]

end -> end     [$;!;%]

end ->
C ->
V ->