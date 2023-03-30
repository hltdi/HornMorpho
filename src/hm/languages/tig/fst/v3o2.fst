-> pre

pre -> pre [X;V;_]

pre -> stem [=]

stem -> stemC    [X]
stemC -> stemLY  [LL;YY]
stemC -> stemV   [V]
stemC -> stemC   [RR;_]
stemLY -> stemV  [V]
stemLY -> stemC  [RR]
stemLY -> stemLY [LL;YY;_]
stemV -> stemC   [RR]


stemC -> stemV  [V]
stemC -> stemC  [X;_]
stemV -> stemC  [X]

stemC -> sufC

start ->