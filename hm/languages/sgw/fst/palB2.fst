-> start

start -> pal       [:8]
start -> start     [RG;^;V]

pal -> pal2        [^:]
pal2 -> pal2c      [GG]
pal2c -> pal2cv    [V;:]
pal2cv -> pal2cv^  [^]
pal2cv^ -> end     [BB;DD]

pal -> nopal.c         [RG-GG]
nopal.c -> nopal.cv    [V;:]
nopal.cv -> nopal.cv^  [^]
nopal.cv^ -> end       [RR]

pal -> nopal.g         [GG]
nopal.g -> nopal.gv    [V;:]
nopal.gv -> nopal.gv^  [^]
nopal.gv^ -> end       [RR-BB,DD]

start ->
end ->
