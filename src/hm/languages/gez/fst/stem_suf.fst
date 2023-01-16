-> start

start -> =         [አ:=አ;ኣ:=ኣ]
= -> start          [X;Xv]

start -> start    [Xv]

start -> =e       [{I2e}]
start -> =a       [{I2a}]
start -> =u       [{I2u}]

=e -> start       [:=አ]
=u -> start       [:=ኡ]
=a -> start       [:=ኣ]

start -> I          [X]
I -> start          [Xv;-]
I -> I                   [X]
I -> =e                 [{I2e}]
I -> =a                 [{I2a}]
I -> =u                 [{I2u}]

start ->
I ->
