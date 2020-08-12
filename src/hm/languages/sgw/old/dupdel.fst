# delete C2 in class E, dup=2, tm=j_i when
# C2 is labial or C1 is coronal and C2 is velar.

-> start

# doesn't apply
start -> start      [:]      [root=[cls=A|Ap|B|C|D|F]];[tm=imf|prf];[dup=1|None]

# C4 (C2)
# geminate C3 after C2 deletion
start -> gem        [ZZ-OO]  [root=[cls=E],dup=2,tm=j_i]
# don't geminate C3 after C2 deletion
start -> nogem      [OO]     [root=[cls=E],dup=2,tm=j_i]

gem -> gem/         [/:]
gem/ -> gemcor      [DD]
# delete velar before coronal degdg -> dedg
gemcor -> end       [:k;:K;:q;:g]
gem/ -> gemnocor    [ZZ-DD]
gemnocor -> end     [:b;:p;:f;:m]
gemnocor -> end     [ZZ-BB]
gemcor -> end       [ZZ-KK]

end -> end          [ZZ;V;%]
end ->
start ->