# convert sequences of vowels, often across affix-stem boundaries
# to single vowels

-> start

start -> start   [X;E;A;i;I;a;u;=]

# delete e after another vowel, including -e(c) suffix
start -> del_e   [:e]    [sn=1]
del_e -> del_e=  [=]
#del_e= -> del_e  [:e]
del_e= -> start  [a;e]
del_e -> start   [a;e]

start -> e       [e]
e -> e=          [=]
e= -> start      [X]
e -> start       [X]

e -> eb          [b:]    [sn=2,sp=3,sg=f]
eb -> eb=        [=]
# seTebo
eb= -> start     [e]

eb= -> eb=e      [:e]
# srabo
eb=e -> start    [a]

# benema
e= -> start      [:a]    [sn=2,sp=3,sg=f]

start -> o       [o]
o -> ob          [b:]
ob -> ob=        [=]
# setebema
ob= -> start     [e]

ob= -> ob=e      [:e]
# srabema
ob=e -> start    [a]

o -> o=          [=]
# beno
o= -> start      [:a;X]
o -> start       [X]

# delete stem-final vowel before -ema suffix
e= -> start      [:e;:a]   [sn=2]

start ->