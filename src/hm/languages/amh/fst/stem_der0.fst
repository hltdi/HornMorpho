## Amharic root -> derivational stems
## Features:
##   der: ps, tr, cs, rc, it
## Root types:
##   sbr, sb_r, sabr, sbsb, sbs_b, sbasb, sb|sbr, sbrbr, sbrabr
##   qr*, slc*

-> start

## CCC
start -> 1a.3 [X3]
start -> 1L.3 [L]     [as=it];[as=smp]
1a.3 -> 1b.3  [:]     [as=it];[as=smp]
1b.3 -> 1c.3  [:]
1b.3 -> 1a_c.3  [a]     # C verbs

# C2 = y, w, ', `; no gemination of w, y
# redup
1a.3 -> 1Dw.3 <wD:>    [as=it]
1Dw.3 -> 2c.3 [w]
1a.3 -> 1D.3  [D:]     [as=it]
1D.3 -> 2c.3  [L;y]
# not redup
1a.3 -> 2c.3  [L;w;y]  [as=smp]

# recip
1a.3 -> 1c.3   [a:]     [vc=ps,as=rc];[vc=tr,as=rc]
1a.3 -> 1wR.3  [a:]     [as=rc,vc=ps];[as=rc,vc=tr]
# not possible with C2=L
1wR.3 -> 2c.3  [w;y]

# after L, y and w are possible (and treated normally)
1L.3 -> 2a.3   [X3]

1a_c.3 -> 2a.3 [X3]    # C verbs (w, y? possible)
1c.3 -> 2a.3   [X!]
# non-duplicated CC(_)C
2a.3 -> 2b.3   [:]     [as=smp];[as=rc,vc=ps];[as=rc,vc=tr]
2b.3 -> 2c.3   [_;:]
# these must be geminated
1c.3 -> 2aw.3  [w;y]
2aw.3 -> 2bw.3 [D:]   [as=it]
2aw.3 -> 2bw.3 [:]    [as=smp];[as=rc,vc=ps];[as=rc,vc=tr]
2bw.3 -> 2c.3  [_]

# C2 dup
2a.3 -> 2b.3  [D:]    [as=it]

2c.3 -> end   [X31]

## CCCC
start -> 1.4  [X41]
1.4 -> 2a.4   [X42]
2a.4 -> 2b.4  [:]     [as=smp];[as=it]
2a.4 -> 2b.4  [a:]    [vc=ps,as=rc];[vc=tr,as=rc]
2a.4 -> 2b.4  [a]     [as=smp];[as=it]
# J necessary for selecce category
2b.4 -> 3a.4  [X41;J]
# C3 dup
3a.4 -> 3b.4  [D:]    [as=it]
3a.4 -> 3b.4  [:]     [as=rc,vc=ps];[as=rc,vc=tr];[as=smp]

3b.4 -> end   [X44]

## CCCCC, C|CCCC
start -> 1.5  [X5]
# C|...
1.5 -> |.5    [|]
# CC...
1.5 -> 1.4    [X5]
# C|C...
|.5 -> |2.5   [X52]
# C|CC...
|2.5 -> 2a.4  [X5]
# C|Ca...
|2.5 -> 2b.4  [a]     [as=smp];[as=it]

end ->
