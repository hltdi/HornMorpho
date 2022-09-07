### Filter out X*, where X is not palatal

-> start

start -> start   [|;a;_]
start -> nonpal  [~J;B]
start -> pal     [J]

pal -> end       [*]
# B: bejje
pal -> pal_     [_]
pal_ -> end      [*]
pal -> start     [|;a]
pal -> nonpal    [~J;B]
pal -> pal       [J]

nonpal -> pal    [J]
nonpal -> start  [|;a;_]
nonpal -> nonpal [~J;B]

pal ->
nonpal ->
end ->
