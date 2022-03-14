-> start

start -> start    [XX;V;/]

=e -> start       [:=አ]
=u -> start       [:=ኡ]
=i -> start       [:=ኢ]

start -> =e       [a;e;በ:ብ;ረ:ር;ሰ:ስ]
start -> =u       [ቡ:ብ;ሩ:ር;ሱ:ስ]
start -> =i       [ቢ:ብ;ሪ:ር;ሲ:ስ]
start -> a        [a]
a -> start        [ው:ኡ;XX;/]
a -> a            [a]
a -> =e           [a;e;በ:ብ;ረ:ር;ሰ:ስ;]
a -> =u           [ቡ:ብ;ሩ:ር;ሱ:ስ]
a -> =i           [ቢ:ብ;ሪ:ር;ሲ:ስ]
a -> C            [C;e]

start -> C        [C;e]
C -> start        [XX;/]
C -> C            [C;e]
C -> a            [a]
C -> =e           [a;e;በ:ብ;ረ:ር;ሰ:ስ]
C -> =u           [ቡ:ብ;ሩ:ር;ሱ:ስ]
C -> =i           [ቢ:ብ;ሪ:ር;ሲ:ስ]

start ->
C ->
a ->
