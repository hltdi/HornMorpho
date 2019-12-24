# eu -> o
# Eu -> Ew
# iu -> iw

-> start

start -> start [X;:=;_;/;V-e,E,i,a]

start ->  e.u  [o:e]
e.u -> e.u     [:=]
e.u -> start   [:u]

start -> e     [e]
e -> start     [X;_;/;V-u]
e -> e=.C      [:=]
e=.C -> start  [X;/]
# delete e before vowels on other side of boundary

start -> e.=V  [:e]
e.=V -> e=.V   [:=]
# e=e, e=a, e=i, e=I, e=o
e=.V -> start  [I;o]
e=.V -> E      [E]
e=.V -> a      [a]
e=.V -> i      [i]
start -> e.E   [:e]
e.E -> E       [E]
e=.V -> e      [e]
e=.V -> e=e.u  [o:e]
e=e.u -> start [:u]

start -> E     [E]
E -> E         [:=]
E -> start     [:e;w:u;X;_;/;V-u,e]

start -> i     [i]
i -> start     [w:u;X;:=;_;/;V-u]

start -> a     [a]
a -> a=.       [:=]
a=. -> start   [X;/]
a=. -> a=.e    [:e]
a=.e -> start  [w:u;X;V-u]
a -> start     [X;_;/;V-i]
a -> a.i       [y:]
a.i -> start   [i]

start ->
a=. ->
a=.e ->
i ->
e ->
E ->
a ->