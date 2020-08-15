# Change a to ee following at (vc=cs)

-> start

start -> start  [X;M;V;%]  [vc=smp];[vc=ps];[vc=tr]

start -> C      [X]        [vc=cs]
C -> C          [M]
# Insert ee when there isn't long vowel, but don't do this for
# reduplicated forms
# C -> VV         [ee:;ee;oo;aa] [as=smp];[as=rc]
C -> VV         [ee:]       [as=smp];[as=rc]
# already a long vowel
C -> VV         [ee;oo;aa]
VV -> VV        [M]
VV -> end       [X]

# Also try inserting ee after second consonant (atmiseekkara)
# (only for redup or CCCC verbs)
C -> CC         [X]
CC -> VV        [ee:aa]      [as=it]
CC -> VV        [aa]        [as=smp];[as=rc]
CC -> VV        [ee:]

end -> end      [X;M;V;%]

start ->
end ->
