-> start

start -> nopal  []    [-Y]
nopal -> nopal  [X;C]

### classes A, B, C, E, s=0

## 3 is palatalizable
start -> pal3   []    [3=T|K,s=0,+Y];[3=R,s=0,+Y,-W]
## 3 is not palatalizable
start -> pal12  []    [3=B|N,s=0,+Y]
# palatalize 2
pal12 -> pal2   []    [2=K]
# palatalize 1
pal12 -> pal1   []    [1=K,2=B|T|R|N]
# 1 and 2 are not palatalizable
pal12 -> nopal   []   [1=B|T|R|N|a|w,2=B|T|R|N]

nopal ->
end ->

