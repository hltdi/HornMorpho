-> start

start -> start  [X;V;%]     [tm=j_i];[tm=imf];[root=[cls=Ap|B|C|D|E|F]]

start -> stem   [=]         [tm=prf,root=[cls=A]]
stem -> stem    [^]
stem -> end     [X-d,t,T;V;%-^]

# delete e between n and dental
stem -> DD      [d;t;T]
DD -> DDe0      [:e]
DDe0 -> end     [n]

# no e to delete
DD -> end       [V-e;%]
# don't delete e after any other consonant
DD -> DDe       [e]
DDe -> end      [X-n]

start ->

end ->

end -> end      [X;V;%]
