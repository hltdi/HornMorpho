-> start

start -> start  [X;V;_;/]

start -> stem   [=]

stem -> C       [X;/]
stem -> V       [V]
C -> C          [X;_]
C -> V          [V]
V -> V          [V]
V -> C          [X;/]

V -> Vsuf       [=]
C -> Csuf       [=]

Vsuf -> Vsuf    [V]
Vsuf -> Csuf    [X;/]
Csuf -> Vsuf    [V]
Csuf -> Csuf    [X;_]

# V=@... => V=n_...
Vsuf -> Vsuf1   [n:@]
Vsuf1 -> end    [_:]

# C=@... -> C=_...
Csuf -> end     [_:@]

end -> end      [X;V;_;/]

end ->
Vsuf ->
Csuf ->