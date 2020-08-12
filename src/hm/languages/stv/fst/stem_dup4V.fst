# Move D in Silt'e
# CCCDC -> CCDaCC
# CV:CD -> CDV:C
-> start

start -> start  [V;%]
start -> start  [L]

# move D
start -> x     [X/L]
x -> xD.VV     [D:]
xD.VV -> xDVV  [VV]
xDVV -> xDVV   [M]
xDVV -> xDVVX  [X/L]
xDVVX -> start [:D]

x -> xx        [X/L]
xx -> xxD      [D:]
xxD -> xxDa    [a:;a]    # insert a if it's not there
xxDa -> xxDaX  [X/L]
xxDaX -> start [:D]

# fail if D not moved
x -> xVV       [VV]
xVV -> xVVx    [X/L]
xVVx -> xVVx   [X]
xVVx -> start  [V;%-D]

x -> start     [L;~V;%]
xx -> start    [L;~V;%]

xx -> xxx      [X/L]
xx -> xxVV     [VV]
xxVV -> xxx    [X/L]
xxx -> start   [X;V;%-D]

start ->
x ->
xx ->
xxx ->
xVVx ->
