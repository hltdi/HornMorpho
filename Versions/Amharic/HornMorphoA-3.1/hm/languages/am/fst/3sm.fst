-> start
start -> start [%]

# 3 -> t
start -> ou  [w;o;u]
ou -> ou     [w;o;u]
ou -> 3      [t:3]
ou -> V      [X-w;V-o,u]
ou -> start  [%-3]

# 3 -> w; after a,i,E,e,I; C other than w
start -> V   [X-w;V-o,u]
V -> V       [X-w;V-o,u;_]
V -> 3       [w:3]
V -> ou      [w;o;u]             
V -> start   [%-3]

3 -> start   [X;V;%]

start ->
ou ->
V ->
3 ->

