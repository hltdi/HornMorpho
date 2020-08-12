## Silt'e root -> derivational stems
## Features:
##   der: ps, tr, cs, rc, it
## Root types:
##   sbr, sb_r, sabr, sbsb, sbs_b, sbasb, sb|sbr, sbrbr, sbrabr
##   qrY, slcY
##   _O..., _o..., _E...

-> start

## CCC
# initial C other than '
start -> 1a.3      [X/L]
1a.3 -> 1b.3       [:]     [as=it];[as=smp]
1a.3 -> 1b.3       [a]     [as=it];[as=smp]  # C verbs
1b.3 -> 1c.3       [M]
# can't be followed by w (that's handled below)
1b.3 -> 2a.3       [X/L]
1c.3 -> 2a.3       [X/L]
# initial '
start -> 1L.3      [L]     [as=it];[as=smp]
1L.3 -> 1b.3       [:;O;E]
# 1Lb.3 -> 1Lc.3   [M]
# can be followed  by w, which can be reduplicated
# 1Lc.3 -> 2a.3    [X/L]
# 1Lb.3 -> 2.3     [X/L]

# long vowel after C1; D following C1; C2 can't be ' or w; no recip
# not reduplicated
1a.3 -> 1Vb.3      [O;E] [as=smp]
1Vb.3 -> 1Vc.3     [M]
# skip the D following C2
1Vc.3 -> 2b.3      [X/L]
1Vb.3 -> 2b.3      [X/L]
# reduplicated
1a.3 -> 1VD.3      [D:]  [as=it]
1VD.3 -> 1Vb.3     [O;E]

# C2 = '; D following C1; C2 can't be '
# reduplicated
1a.3 -> 1D.3      [D:]    [as=it]
1D.3 -> 2c.3      [']
# not reduplicated
1a.3 -> 2c.3      [']     [as=smp]

# recip, not possible with C1=' or C2='
1a.3 -> 1b.3      [a:]    [vc=ps,as=rc];[vc=tr,as=rc];[vc=cs,as=rc]

2a.3 -> 2b.3      [:]     [as=smp];[as=rc]
2b.3 -> 2c.3      [_;:]

# C2 dup
2a.3 -> 2b.3      [D:]    [as=it]

2c.3 -> end       [X]

## CCCC
# This can be '
start -> 1.4      [X]
# M probably only possible with C1='
1.4 -> 1.4n       [M]
1.4n -> 2a.4      [X]
1.4 -> 2a.4       [X]
2a.4 -> 2b.4      [:]     [as=smp]
# C2 dup
2a.4 -> 2bD.4     [D:]    [as=it]
# Follow D with another a, unless this is an -a- verb
# E, O also possible with initial '
2bD.4 -> 2b.4     [a:;a;E;O]
# Recip
2a.4 -> 2b.4      [a:]    [vc=ps,as=rc];[vc=tr,as=rc];[vc=cs,as=rc]
# Lexical long vowels (probably only possible with C1=')
2a.4 -> 2b.4      [a;O;E] [as=smp]

2b.4 -> 3a.4      [X]
3a.4 -> 3b.4      [:;_] 

3b.4 -> end       [X]

end ->
