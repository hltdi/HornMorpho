-> start

start -> start  [X;C]

#start -> lab2   [W]
#start -> pal2   [Y]
#start -> den2y  [ሲ;ቲ;ዲ;ዚ;ጢ]
#start -> den2   [T-ሲ,ቲ,ዲ,ዚ,ጢ]   [-Y]
#start -> vel2   [K]   [-Y,+W];[-Y,-W];[+Y,+W]
#start -> bil2   [B]   [-W]
#start -> rl2    [R]   [-Y,-W];[+Y,+W];[-Y,+W]
#start -> n2     [N]

# reduplicated non-palatalized
start -> pal2    [Y]     [+d,+Y]
pal2 -> pal2_    [Y]

# last segment; unpalatalized velar or dental, unlabialized bilabial
# provide some information
start -> lab   [W]
start -> pal   [Y]   [-Y];[+Y,-d]
start -> den   [T]   [-Y]
start -> vel   [K]   [-Y,-W]
start -> bil   [B]   [-W]
start -> rl    [R]   [-Y,-W];[+Y,+W];[-Y,+W]
start -> n     [N]

lab ->
pal ->
den ->
pal2_ ->
vel ->
bil ->
rl ->
n ->
