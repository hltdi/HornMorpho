-> start

start -> C      [X-H]
start -> V      [V]
V -> C          [X-H;/]
V -> V          [V]
C -> C          [X-H;_;/]
C -> V          [V]

# assumes this can only occur once in a word
C -> CH         [:H]
CH -> end       [kW:w]
CH -> CHk       [k:]
CHk -> end      [X;V;_]
V -> VH         [:H]
VH -> end       [hW:w]
VH -> VHh       [h:]
VHh -> end      [X;V;_]

end -> end      [X;V;/;_]
start ->
end ->
CHk ->
VHh ->
V ->
C ->