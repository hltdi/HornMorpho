-> start

start -> start   [RR;V]

start -> LY      [LL;YY]
# delete _ after L and Y
LY -> start      [RR;V;:_]
LY -> LY         [LL;YY]

start -> _       [_]
# delete second and third _: 'den_n_o -. 'den___o
_ -> start       [RR;V]
_ -> LY          [LL;YY]
_ -> _           [:_]

start ->
_ ->
LY ->