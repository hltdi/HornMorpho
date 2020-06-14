-> start

start -> C      [X-H,G]
start -> V      [V]
V -> C          [X-H,G;/]
V -> V          [V;_]
C -> C          [X-H,G;_;/]
# two consonants or geminated consonant followed by epenthetic vowel before H/G
C -> V          [V]

# assumes this can only occur once in a word
C -> end         [k:H;kW:G]
V -> end         [h:H;hW:G]

end -> end      [X;V;/;_]

end ->
V ->
C ->
