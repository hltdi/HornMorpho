# k -> K / V_~k
# q -> Q / V-~q
# has to follow (downward) gemination

-> start

start -> start [X;_]

start -> V     [V]
V -> start     [X-k,q,kW,qW]

V -> VK       [K:k;KW:kW;Q:q;QW:qW]
VK -> V       [V]
VK -> start   [X]         # but not _

V -> Vk       [k;kW;q;qW]
Vk -> start   [_]         # otherwise fail

start ->
V ->
VK ->
