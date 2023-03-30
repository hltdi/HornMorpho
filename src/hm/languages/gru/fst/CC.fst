# consonant combinations across morpheme boundaries
# k=k => k_ (H, G)
# n=n => n_
# m=m => m_
# c=x => c_

-> start

start -> start   [X;V;/;_]
start -> stem    [=]
stem -> stem     [X-c,k,n,m;V;/;_]

stem -> k.=k     [:k]
k.=k -> k=.k     [=]
k=.k -> k=k.     [k;k:H;kW:G]
k=k. -> k=k_     [_:]
k=k_ -> end      [X;V]

stem -> k        [k]
k -> stem        [X-c,k,n,m;V;/;_]
k -> k           [k]
k -> k.=k        [:k]
k -> k=          [=]
k -> n           [n]
k -> m           [m]
k -> c           [c]
k= -> end        [X-H,G;V;/;_]
k= -> k=k._      [k]
k=k._ -> end     [_]

stem -> n        [n]
n -> stem        [X-c,k,n,m;V;/;_]
n -> k           [k]
n -> m           [m]
n -> c           [c]
n -> k.=k        [:k]
n -> n=          [=]
n -> n           [n]
n= -> end        [X-n;_:n;V;/;_]

stem -> m        [m]
m -> stem        [X-c,k,n,m;V;/;_]
m -> k           [k]
m -> n           [n]
m -> c           [c]
m -> k.=k        [:k]
m -> m=          [=]
m -> m           [m]
m= -> end        [X-m;_:m;V;/;_]

stem -> c        [c]
c -> stem        [X-k,n,m,c;V;/;_]
c -> k           [k]
c -> n           [n]
c -> k.=k        [:k]
c -> c=          [=]
c -> c           [c]
c= -> end        [X-x;_:x;V;/;_]

stem -> end      [=]

end -> end       [X;V;/;_]
end ->
k= ->
n= ->
m= ->
c= ->
k=k_ ->
