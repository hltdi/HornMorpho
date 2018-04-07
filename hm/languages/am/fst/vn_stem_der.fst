## Amharic root -> verbal noun derivational stems
## Identical to stem_der.fst, except for D: v: man
## Features:
##   der: ps, tr, cs, rc, it
## Root types:
##   sbr, sb_r, sabr, sbsb, sbs_b, sbasb, sb|sbr, sbrbr, sbrabr
##   qr*, slc*

-> start

## CCC
start -> 1a.3 [X/L]
start -> 1L.3 [L]     [as=it];[as=smp];[v=man,vc=smp,as=smp]
1a.3 -> 1b.3  [:]     [as=it];[as=smp];[v=man,vc=smp,as=smp]
1b.3 -> 1c.3  [:]
1b.3 -> 1c.3  [a]     # C verbs

# C2 = y, w, '; no gemination of w, y
# redup
1a.3 -> 1Dw.3 <wD:>    [as=it];[v=man,vc=smp,as=smp]
1Dw.3 -> 2c.3 [w]
1a.3 -> 1D.3  [D:]     [v=agt,as=it];[v=inf,as=it];[v=ins,as=it];[v=man,vc=smp,as=smp]
1D.3 -> 2c.3  [L;y]
# not redup
1a.3 -> 2c.3  [L;w;y]  [as=smp,v=agt];[as=smp,v=inf];[as=smp,v=ins]

# recip
1a.3 -> 1c.3  [a:]     [as=rc,v=agt];[as=rc,v=inf];[as=rc,v=ins]
1a.3 -> 1wR.3 [a:]     [as=rc,v=agt];[as=rc,v=inf];[as=rc,v=ins]
# not possible with C2=L
1wR.3 -> 2c.3 [w;y]

# after L, y and w are possible (and treated normally)
1L.3 -> 2a.3  [X/L]

1c.3 -> 2a.3  [X!]
2a.3 -> 2b.3  [:]     [as=smp,v=agt];[as=rc,v=agt];[as=smp,v=inf];[as=rc,v=inf];[as=smp,v=ins];[as=rc,v=ins]
2b.3 -> 2c.3  [_;:]
# these must be geminated
1c.3 -> 2aw.3  [w;y]
2aw.3 -> 2bw.3 [D:]   [v=agt,as=it];[v=inf,as=it];[v=ins,as=it];[v=man,vc=smp,as=smp]
2aw.3 -> 2bw.3 [:]    [as=smp,v=agt];[as=smp,v=inf];[as=smp,v=ins];[as=rc,v=agt];[as=rc,v=inf];[as=rc,v=ins]
2bw.3 -> 2c.3  [_]

# C2 dup
2a.3 -> 2b.3  [D:]    [v=agt,as=it];[v=inf,as=it];[v=ins,as=it];[v=man,vc=smp,as=smp]

2c.3 -> end   [X]

## CCCC
start -> 1.4  [X]
1.4 -> 2a.4   [X]
2a.4 -> 2b.4  [:]     [as=smp];[as=it];[v=man,as=smp,vc=smp]
2a.4 -> 2b.4  [a:]    [as=rc,v=agt];[as=rc,v=inf];[as=rc,v=ins]
2a.4 -> 2b.4  [a]     [as=smp];[as=it];[v=man,as=smp,vc=smp]

2b.4 -> 3a.4  [X]
# C3 dup
3a.4 -> 3b.4  [D:]    [v=agt,as=it];[v=inf,as=it];[v=ins,as=it];[v=man,vc=smp,as=smp]
3a.4 -> 3b.4  [:]     [as=smp,v=agt];[as=smp,v=inf];[as=smp,v=ins];[as=rc,v=agt];[as=rc,v=inf];[as=rc,v=ins]

3b.4 -> end   [X]

## CCCCC
start -> 1.5  [X]     
1.5 -> |.5    [|]
|.5 -> |2.5   [X]
|2.5 -> 2a.4  [X]
|2.5 -> 2b.4  [a]     [as=smp];[as=it];[v=man,vc=smp,as=smp]

end ->
