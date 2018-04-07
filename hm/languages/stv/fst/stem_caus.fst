# Change e to E following at (vc=cs)

-> start

start -> start  [X;M;V;%]  [vc=smp];[vc=ps];[vc=tr]

start -> C      [X]        [vc=cs]
C -> C          [M]
# Insert E when there isn't long vowel, but don't do this for
# reduplicated forms
# C -> VV         [E:;E;O;a] [as=smp];[as=rc]
C -> VV         [E:]       [as=smp];[as=rc]
# already a long vowel
C -> VV         [E;O;a]
VV -> VV        [M]
VV -> end       [X]

# Also try inserting E after second consonant (atmiseekkara)
# (only for redup or CCCC verbs)
C -> CC         [X]
CC -> VV        [E:a]      [as=it]
CC -> VV        [a]        [as=smp];[as=rc]
CC -> VV        [E:]

end -> end      [X;M;V;%]

start ->
end ->
