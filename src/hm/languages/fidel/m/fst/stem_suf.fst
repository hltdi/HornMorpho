-> start

start -> start    [u;o;V;/]


=e -> start       [:=አ]
=u -> start       [:=ኡ]
=i -> start       [:=ኢ]
# =a -> start       [:=ኣ]

# 0+e => e
start -> =e        [{I2e}]
# 0+u => u, e+u => o
start -> =u        [{I2u};{e2o}]
# 0+i => i
start -> =i        [{I2i}]
# start -> =a       [ያ:የ;ባ:በ;ታ:ተ]
start -> a        [a]
start -> iE       [i;E]
start -> e        [e]

# a+i => ay ? (E?); a+u => aw (o?)
a -> start        [ው:=ኡ;:=አ;ይ:=ኢ;u;o;/]
a -> a            [a]
a -> e            [e]
a -> =e           [{I2e}]
                        
a -> =u           [{I2u};{e2o}]
a -> =i           [{I2i}]
a -> C            [C;e]
a -> iE           [i;E]

# e+e => e
e -> start        [:=አ;u;o;/]
e -> a            [a]
e -> iE           [i;E]

start -> C        [C;e]
C -> start        [u;o;/]
C -> C            [C;e]
C -> a            [a]
C -> e            [e]
C -> iE           [i;E]
C -> =e           [{I2e}]
C -> =u            [{I2u};{e2o}]
C -> =i            [{I2i}]

# iu => iw; Eu => Ew; ii => i; Ei => E; ie => i; Ee => E
iE -> start       [ው:=ኡ;:=ኢ;:=አ;XX;/]
iE -> iE          [i;E]
iE -> a           [a]
iE -> C           [C;e]
iE -> e           [e]
iE -> =e          [{I2e}]
iE -> =u          [{I2u};{e2o}]
iE -> =i          [{I2i}]

start ->
C ->
a ->
iE ->
