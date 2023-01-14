-> start

start -> =         [አ:=አ;ኣ:=ኣ]
= -> start          [I;X]

start -> start    [X]

start -> =e       [{I2e}]
start -> =a       [{I2a}]
start -> =u       [{I2u}]

=e -> start       [:=አ]
=u -> start       [:=ኡ]
=a -> start       [:=ኣ]

start -> I          [I]
I -> start          [X;-]
I -> I                   [I]
I -> =e                 [{I2e}]
I -> =a                 [{I2a}]
I -> =u                 [{I2u}]

start ->
I ->
