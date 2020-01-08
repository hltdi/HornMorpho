-> start

start -> C      [X-H,G]
start -> V      [V]
V -> C          [X-H,G;/]
V -> V          [V]
C -> C          [X-H,G;_;/]
C -> V          [V]

# assumes this can only occur once in a word
C -> end         [k:H;kW:G]
V -> end         [h:H;hW:G]
#CH -> end       [X;V;_]
#CH -> CHk       [k:]
#CHk -> end      [X;V;_]
#VH -> end       [X;V;_]
#VH -> end       [hW:w]
#VH -> VHh       [h:]
#VHh -> end      [X;V;_]

end -> end      [X;V;/;_]
end ->
V ->
C ->
#CH ->
#VH ->
#start ->
