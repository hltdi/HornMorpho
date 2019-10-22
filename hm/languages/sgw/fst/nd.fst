-> start

start -> start  [XX;^;@]   [root=[cls=B]];[root=[cls=D]];[root=[cls=D]];[root=[cls=E]];[root=[cls=F]];[tm=imf];[tm=j_i];[vc=[+ps]]

start -> X      [:]        [root=[cls=A],tm=prf,vc=[-ps]];[root=[cls=Ap],tm=prf,vc=[-ps]]

X -> T          [t;d;T]

# delete the e
T -> T_e        [:e]
T_e -> end      [n]

# don't do anything
X -> end        [X-t,d,T;^;V]
T -> end        [X;a;E;i;o;^;@]
T -> Te         [e]
Te -> end       [X-n;^;@]

start ->

end ->

end -> end      [XX;^;@]