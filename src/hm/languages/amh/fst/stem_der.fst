## Amharic root -> derivational stems
## Features:
##   der: ps, tr, cs, rc, it
## Root types:
##   sbr, sb_r, sabr, sbsb, sbasb, sbrbr, sbrabr
##   qr*, slc*

-> start0

start0 -> 0           [:]   [as=smp,vc=smp]
start0 -> te_       [:]   [as=smp,vc=ps]
start0 -> a_         [:]   [as=smp,vc=tr]
start0 -> as_       [:]    [as=smp,vc=cs]
start0 -> te_a     [:]   [as=rc,vc=ps]
start0 -> a_a       [:]   [as=rc,vc=tr]
start0 -> R           [:]     [as=it,vc=smp]
start0 -> te_R     [:]   [as=it,vc=ps]
start0 -> a_R       [:]   [as=it,vc=tr]
start0 -> as_R      [:]   [as=it,vc=cs]


0 -> start                [:]         [bs=0]
te_ -> start            [:]         [bs=te_];[bs=0];[bs=a_]
a_  -> start             [:]         [bs=a_];[bs=0];[bs=te_]
as_ -> start           [:]          [bs=as_];[bs=0];[bs=te_];[bs=a_]
te_a -> start         [:]          [bs=te_a];bs=0]
a_a -> start            [:]         [bs=te_a];[bs=0]
R -> start                [:]         [bs=0]
te_R -> start          [:]         [bs=te_R];[bs=0];[bs=te_];[bs=a_];[bs=te_a]
a_R -> start            [:]         [bs=te_R];[bs=0];[bs=te_];[bs=a_];[bs=te_a]
as_R -> start         [:]          [bs=te_R];[bs=0];[bs=te_];[bs=a_];[bs=te_a]

#start0 -> start [:] [vc=ps,+ps];[vc=tr,+tr];[vc=cs,+cs];[vc=smp,+smp];[pos=n_dv,v=man]

## CCC
start -> 1a.3 [X/L]
start -> 1L.3 [L]     [as=it];[as=smp]
1a.3 -> 1b.3  [:]     [as=it];[as=smp]
1b.3 -> 1c.3  [:]
1b.3 -> 1a_c.3  [a]     # C verbs

# C2 = y, w, ', `; no gemination of w, y
# redup
1a.3 -> 1Dw.3 <wD:>    [as=it]
1Dw.3 -> 2c.3 [w]
1a.3 -> 1D.3  [D:]     [as=it]
1D.3 -> 2c.3  [L;y]    [cls=A]
# not redup
1a.3 -> 2c.3  [L;w;y]  [as=smp]

# recip
1a.3 -> 1c.3   [a:]     [vc=ps,as=rc];[vc=tr,as=rc]
1a.3 -> 1wR.3  [a:]     [as=rc]
# not possible with C2=L
1wR.3 -> 2c.3  [w;y]

# after L, y and w are possible (and treated normally)
1L.3 -> 2a.3   [X/L]

1a_c.3 -> 2a.3 [X/L]    # C verbs
1c.3 -> 2a.3   [X!]
# non-duplicated CC(_)C
2a.3 -> 2b.3   [:]     [as=smp];[as=rc]
2b.3 -> 2c.3   [_;:]
# these must be geminated
1c.3 -> 2aw.3  [w;y]
2aw.3 -> 2bw.3 [D:]   [as=it]
2aw.3 -> 2bw.3 [:]    [as=smp];[as=rc]
2bw.3 -> 2c.3  [_]

# C2 dup
2a.3 -> 2b.3  [D:]    [as=it]

2c.3 -> end   [X]

## CCCC
start -> 1.4  [X]
1.4 -> 2a.4   [X]
2a.4 -> 2b.4  [:]     [as=smp];[as=it]
2a.4 -> 2b.4  [a:]    [vc=ps,as=rc];[vc=tr,as=rc]
2a.4 -> 2b.4  [a]     [as=smp];[as=it]

2b.4 -> 3a.4  [X]
# C3 dup
3a.4 -> 3b.4  [D:]    [as=it]
3a.4 -> 3b.4  [:]     [as=rc];[as=smp]

3b.4 -> end   [X]

## CCCCC, C|CCCC
start -> 1.5  [X]
# C|...
1.5 -> |.5    [|]
# CC...
1.5 -> 1.4    [X]
# C|C...
|.5 -> |2.5   [X]
# C|CC...
|2.5 -> 2a.4  [X]
# C|Ca...
|2.5 -> 2b.4  [a]     [as=smp];[as=it]

end ->
