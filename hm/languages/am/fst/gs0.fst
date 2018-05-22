# Insert glottal stop at the beginning of a word beginning with a vowel
# or after a space (realized here as //

-> start

# insert the glottal stop
start -> gs   [':]
gs -> middle     [V]
# end -> end    [X;V;%]

# fail if it's not inserted before an initial vowel
start -> V    [V]

# succeed if the word starts with a C, including
# a glottal stop which is already there
start -> middle  [X]

middle -> middle [X;V;%-/]

middle -> / [/]
# single / is possible
/ -> middle [X]
# two /s also possible
/ -> //     [/]
// -> middle [X]
// -> gs     [':]

middle ->

#end ->
