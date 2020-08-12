# realize vowels in prefixes before laryngeals
# and -o suffix (as -u) 23pm imperf/juss after root-final laryngeal or y

-> pre

pre -> pre      [X;V;_;/]

# 'n(e) -> n
pre -> @del     [:@]
@del -> @deln   [n]
@deln -> @delnA [A]
@delnA -> @delstem [=]
@delstem -> stem [LL]
#'
#@del -> @delstem [=]
@del -> @delA     [:A]
@delA -> @delstem [=]

pre -> @        [':@]
@ -> @n         [n]
@n -> @nA       [:A]
@nA -> @stem    [=]
@stem -> stem   [RR;YY]

#'
@ -> @A         [A]
@A -> @stem     [=]

pre -> stem     [=]

stem -> stem    [RR;YY-Y;V;o:O;/;_;=]

# stem-final Y
stem -> stemY   [Y]
stemY -> stem   [RR;YY-Y;V;_;/]
stemY -> sufL   [=]

# stem-final L
stem -> stemL   [LL]
stemL -> stem   [RR;YY-Y;V;_;/]
stemL -> stemY  [Y]
stemL -> sufL   [=]

sufL -> sufL    [u:O;X;V;_]

sufL ->
stem ->