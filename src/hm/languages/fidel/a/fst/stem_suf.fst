-> start

start -> =         [አ:=አ;ኣ:=ኣ]
= -> start          [*;*v]

start -> start    [*v]

start -> =e       [{I2e}]
start -> =a       [{I2a}]
start -> =u       [{I2u}]

=e -> start       [:=አ]
=u -> start       [:=ኡ]
=a -> start       [:=ኣ]

start -> I          [*]
I -> start          [*v;-]
I -> I                   [*]
I -> =e                 [{I2e}]
I -> =a                 [{I2a}]
I -> =u                 [{I2u}]

start ->
I ->
