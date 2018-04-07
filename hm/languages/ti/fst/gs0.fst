# Insert glottal stop at the beginning of a word beginning with a vowel

-> start

# insert the glottal stop
start -> gs   [':]
gs -> end     [V]
end -> end    [X;K;Q;KW;QW;V;_]

# succeed if the word starts with a C, including
# a glottal stop which is already there
start -> end  [X]

end ->
