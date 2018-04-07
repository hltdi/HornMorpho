## 1s_sbj: C-an, V-n
## (on nouns)
## Do before all other FSTs with special characters

-> start

start -> C   [!!]
C -> end   <an:N>
C -> C       [!]
C -> V       [$]

start -> V   [$$]
V -> end    [n:N]
V -> C       [!]
V -> V       [$]

end ->
C ->
V ->