# Insert glottal stop at the beginning of a word beginning with a vowel

-> start

# insert the glottal stop
start -> gs   [':]
gs -> end     [V]
end -> end    [X;V;%]

# fail if it's not inserted before an initial vowel
start -> V    [V]

# succeed if the word starts with a C, including
# a glottal stop which is already there
start -> end  [X]

end ->
