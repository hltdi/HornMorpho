-> start

start -> start    [X]

start -> =e       [{I2e}]
start -> =a       [{I2a}]
start -> =u       [{I2u}]

=e -> start       [:=አ]
=u -> start       [:=ኡ]
=a -> start       [:=ኣ]

start -> I          [C]
I -> start          [X]
I -> I                   [C]
I -> =e                 [{I2e}]
I -> =a                 [{I2a}]
I -> =u                 [{I2u}]

start ->
I ->
