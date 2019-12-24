# sem_ea => sem_a
# sem_ee => sem_e
-> start

start -> start  [X;V-e;_;/]

start -> e      [e]
e -> start      [X;/]
start -> e.V    [:e]
e.V -> start    [V]

start ->
e ->