#### Amharic infinitive, agent, instrumental, manner noun
### INFINITIVE
## mesber:        me12e3        [tmp=[n=3,c1=1,c2=2,  c3=3?,  c4=None, c_1=c,  c_2=2, -c_2gem, -c_1gem, -c1gem, v_1=e, v1=None, v2=e, v3=None, v4=None, pre=me, suff=None]]
## meTey_eq       meTey_eq      [tmp=[n=3,c1=1,c2=
## megabez
## mecal
## meCoh
## mader
## maCet
## megbat
## meqeb_at
## mesTet
## meselcet
## mefendat
## megelbeT
## meCberber
## mew_exenegager
### AGENT
## sebari:     1esa3i
### INSTRUMENTAL
## mesberiya:  me12e3iya
### MANNER
## as_ebaber:  a1_e2a2e3
###
### Example templates
###  teCberebber-e:    te12e3e4_e5,   [tmp=[n=5,c1=1,c2=2,   c3=None,c4=None, c_1=c,   c_2=c, +c_2gem, -c1gem, v_1=e, v1=e, v2=e,   v3=None,v4=None,pre=te  ]]
###  gelebabbeT-e:     1e2e3a3_e4,    [tmp=[n=4,c1=1,c2=2,   c3=3,   c4=None, c_1=c,   c_2=3, +c_2gem, -c1gem, v_1=e, v1=e, v2=e,   v3=a,   v4=None,pre=None]]
###  y-nkWakW_-al:     12a2_a,        [tmp=[n=5,c1=1,c2=None,c3=None,c4=None, c_1=None,c_2=2, +c_2gem, -c1gem, v_1=a, v1=a, v2=None,v3=None,v4=None,pre=None]] 
###  awwexenegagger-e: a1_e2e3e4a4_e5 [tmp=[n=5,c1=1,c2=2,   c3=3,   c4=4,    c_1=c,   c_2=4, +c_2gem, +c1gem, v_1=e, v1=e, v2=e,   v3=e,   v4=a,  ,pre=a   ]]
###  babba:            1a2_a          [tmp=[n=4,c1=1,c2=None,c3=None,c4=None, c_1=None,c_2=2, +c_2gem, -c1gem, v_1=a, v1=a, v2=None,v3=None,v4=None,pre=None]]
###  sebabber-e:       1e2a2_e3       [tmp=[n=3,c1=1,c2=2,   c3=None,c4=None, c_1=c,   c_2=2, +c_2gem, -c1gem, v_1=e, v1=e, v2=a,   v3=None,v4=None,pre=None]]
### Template features:
### pre:    {te, a, as, aste, me, ma, mas, maste, teste, meste, None}
### c1:     {1, None}
### c2:     {2, None}
### c3:     {3, None}
### c4:     {4, None}
### c_1:    {c, t, None}
### c_2:    {1, 2, 3, 4, None}
### c1gem:  {True, False}
### c_2gem: {True, False}
### v1:     {e, a, Wa, I, None}
### v2:     {e, a, None}
### v3:     {e, a, None}
### v4:     {a, None}
### v_1:    {e, a, o, i, E, None}
### suff:   {i, iya, None}
### n:      {3, 4, 5}

-> start

### PREFIXES

# Temporary template

# handled: pre, suff, c1gem, c1
start -> tmp       [:]       [tmp=[c3=None,c4=None,c_2=None,v2=None,v3=None,v4=None,n=3]]

tmp -> stem       <aleme:>  [v=inf,+neg]

tmp -> stem       <me:>     [v=inf,-neg];[v=ins]

tmp -> stem       [:]       [v=agt]

tmp -> man0      [a:]       [v=man,vc=smp,as=smp,tmp=[pre=a]]
man0 -> man        [/:]     [tmp=[+c1gem]]

stem -> a0         [:]        [v=inf,tmp=[pre=ma]];[v=agt,tmp=[pre=a]];[v=ins,tmp=[pre=ma]]
a0 -> a            [a:]       [vc=tr,tmp=[-c1gem]]
a0 -> a/           <a/:>      [vc=tr,as=rc,tmp=[+c1gem]];[vc=tr,as=it,tmp=[+c1gem]]
stem -> te         <te:>      [vc=ps,v=agt,tmp=[pre=te,-c1gem]]
stem -> /C         [/:]       [vc=ps,v=inf,tmp=[pre=me,+c1gem]];[vc=ps,v=ins,tmp=[pre=me,+c1gem]]
stem -> |          [X/L]      [vc=ps,v=inf,tmp=[pre=me,-c1gem]];[vc=ps,v=ins,tmp=[pre=me,-c1gem]]
te -> |            [X/L]      
a -> |             [X/L]      [tmp=[-c1gem]]
man0 -> |          [X/L]      [tmp=[-c1gem]]
stem -> tt         <t_:>      [vc=ps,v=inf,tmp=[pre=met,-c1gem]];[vc=ps,v=ins,tmp=[pre=met,-c1gem]]

stem -> as         <as:>      [tmp=[-c1gem]]
#stem -> mas        <mas:>     [tmp=[-c1gem],v=inf];[tmp=[-c1gem],v=ins]
as ->  ast         [t:]       [vc=tr,v=agt,tmp=[pre=aste,c1=None]];[vc=tr,v=inf,tmp=[pre=maste,c1=None]];[vc=tr,v=ins,tmp=[pre=maste,c1=None]]
ast -> aste        [e:']      [tmp=[v1=None]]

tmp -> astM      <ast:>      [v=man,tmp=[pre=aste,-c1gem]]
astM -> asteM      [e:']      [tmp=[v1=None]]

as -> simp          [:]       [vc=cs,v=agt,tmp=[pre=as,c1=1]];[vc=cs,v=inf,tmp=[pre=mas,c1=1]];[vc=cs,v=imp,tmp=[pre=mas,c1=1]]
te -> simp          [:]       [tmp=[c1=1]]
a -> simp           [:]       [as=smp,tmp=[c1=1]]
stem -> simp0       [:]       [v=agt,tmp=[pre=None,-c1gem,c1=1]];[v=inf,tmp=[pre=me,-c1gem,c1=1]];[v=ins,tmp=[pre=me,-c1gem,c1=1]]
# ... sbr[as=it]: me.sebaber
simp0 -> simp       [:]       [vc=smp,as=smp];[vc=smp,as=it]
/C -> simp          [:]       [tmp=[c1=1]]
a/ -> simp          [:]       [tmp=[c1=1]]

### END

# ... sbr[as=it]: mesebabe<r>
-1 -> -1C           [X/L]     [tmp=[c_1=c]]
-1C -> end          [:]       [v=inf,tmp=[suff=None]];[v=man,tmp=[suff=None]]
-1C -> -1i          [i:]      [v=agt];[v=ins]
-1i -> end          [:]       [v=agt,tmp=[suff=i]]
-1i -> end          [a:]      [v=ins,tmp=[suff=iya]]

# Final vowels for most situations
# ... sbr[as=it]: mesebab<e>r
-2V -> -1           [e:]      [v=man,tmp=[v_1=e]];[v=inf,tmp=[v_1=e]];[v=ins,tmp=[v_1=e]]
-2V -> -1           [a:]      [v=agt,tmp=[v_1=a]]

# Final L
-2V -> -1C          [:']      [v=agt,tmp=[v_1=None,c_1=None]];[v=man,tmp=[v_1=None,c_1=None]];[v=ins,tmp=[v_1=None,c_1=None]]
-2V -> -2V.t        [a:']     [v=inf,tmp=[v_1=a]]
-2V.t -> end        [t:]      [tmp=[suff=None,c_1=t]]
# Final *
-2V -> -1C          [:*]      [v=agt,tmp=[v_1=None,c_1=None,-c_2gem]];[v=man,tmp=[v_1=None,c_1=None,-c_2gem]];[v=ins,tmp=[v_1=None,c_1=None,-c_2gem]]
# infinitive and alternate for -* manner noun
-2V -> -2V.t        [e:*]     [v=man,tmp=[v_1=e,-c_2gem]];[v=inf,tmp=[v_1=e,-c_2gem]]

### A (CCC, C2 cannot be L, w, or y)

-2A_ -> -2V         [:]       [vc=smp,tmp=[-c_2gem]];[vc=tr,tmp=[-c_2gem]];[vc=ps,tmp=[-c_2gem]]
-2A_ -> -2V         [_:]      [vc=cs,tmp=[+c_2gem]]
-2A -> -2A_         [X!]
# Following L, y and w also possible
-3 -> -3V           [X/L]
-3V -> -2A          [e:]      [vc=ps,tmp=[v1=e]];[vc=cs,tmp=[v1=e]];[v=man,tmp=[v1=e]];[v=agt,vc=smp,tmp=[v1=e]]
# transitive agent is aC1C2aC3
-3V -> -2A          [:]       [vc=smp,v=inf,tmp=[v1=None]];[vc=tr,v=inf,tmp=[v1=None]];[vc=smp,v=ins,tmp=[v1=None]];[vc=tr,v=ins,tmp=[v1=None]];[vc=tr,v=agt,tmp=[v1=None]]
-2AL -> -2A_        [X/L]

# initial L; no vc=tr possible; c1=None
-3L -> -3LV         [:']      [tmp=[c1=None,v1=a]]
-3LV -> -2AL        [a:]

simp -> -3          [:]       [tmp=[c2=2]]
as -> -3L           [:]       [vc=cs,tmp=[c1=None,pre=as,c2=2]]
#mas -> -3L          [:]       [vc=cs,tmp=[c1=None,pre=mas,c2=2]]
stem -> -3L         [:]       [vc=smp,as=smp,tmp=[c1=None,pre=None,c2=2]];[vc=smp,as=it,tmp=[c1=None,pre=None,c2=2]]
te -> -3L           [:]       [tmp=[c1=None,c2=2]]
tt -> -3L           [:]       [tmp=[c1=None,c2=2]]

# C1=L in CCCC; ?? apparently behaves like CCC in ps and cs (no tr); c1=None
as -> -3            [:']      [vc=cs,tmp=[c1=None,pre=as]]
te -> -3            [:']      [tmp=[c1=None]]
/C -> -3            [:']      [tmp=[c1=None]]

### A (C*C, imperfective with w, y, L as C2; reduplicated: CaC*C)
### the same pattern of vowels works with all reduplicated forms

-3.2 -> -3V.2        [X/L]     [tmp=[-c_2gem]]
-3.2 -> -3PV.2       [J]       [tmp=[-c_2gem]]
-3.2 -> -3~PV.2      [~J]      [tmp=[-c_2gem]]

# mWac, zWari
-3.2 -> -3Vw.2       [gW:g;hW:h;kW:k;qW:q]         [v=agt]
-3.2 -> -3Vw.2       [bW:b;cW:c;CW:C;dW:d;fW:f]    [v=agt]
-3.2 -> -3Vw.2       [jW:j;lW:l;mW:m;nW:n]         [v=agt]
-3.2 -> -3Vw.2       [rW:r;sW:s;SW:S]              [v=agt]
-3.2 -> -3Vw.2       [tW:t;TW:T;xW:x;zW:z]         [v=agt]
-3Vw.2 -> -1         [a:w]                         [tmp=[-c_2gem,v_1=Wa,v1=None]]

# C2='
-3V.2 -> -1          [a:']                         [tmp=[v_1=a,v1=None]]

# mote, moto (also muto)
-3V.2 -> -1          [o:w]     [v=inf,as=smp,tmp=[v_1=o,v1=None]];[v=ins,as=smp,tmp=[v_1=o,v1=None]];[v=inf,as=rc,tmp=[v_1=o,v1=None]];[v=ins,as=rc,tmp=[v_1=o,v1=None]]

# memWamWat (labialization handled in stem_dup)
-3V.2 -> -1          [a:w]     [v=man,tmp=[v_1=Wa,v1=Wa]];[v=inf,as=it,tmp=[v_1=Wa,v1=Wa]];[v=ins,as=it,tmp=[v_1=Wa,v1=Wa]]

# xeTe
-3PV.2 -> -1         [e:y]     [v=inf,as=smp,tmp=[v_1=e,v1=None]];[v=ins,as=smp,tmp=[v_1=e,v1=None]];[v=inf,as=rc,tmp=[v_1=e,v1=None]];[v=ins,as=rc,tmp=[v_1=e,v1=None]]
# xaxaTe
-3PV.2 -> -1         [a:y]     [v=man,tmp=[v_1=a,v1=None]];[v=agt,tmp=[v_1=a,v1=None]];[v=inf,as=it,tmp=[v_1=a,v1=None]];[v=ins,as=it,tmp=[v_1=a,v1=None]]

# hEde, hEdo, fafEze, yIffafEz, fEzo
-3~PV.2 -> -1        [E:y]     [v=inf,tmp=[v_1=E,v1=None]];[v=ins,tmp=[v_1=E,v1=None]];[v=agt,tmp=[v_1=E,v1=None]]
-3~PV.2 -> -1        [a:y]     [v=man,tmp=[v_1=a,v1=None]]

# reduplicated cases: precede by Ca
-4.2 -> -4V.2        [X]
-4V.2 -> -3.2        [a]       [tmp=[c2=2]]

simp -> -3.2         [:]       [tmp=[c2=None]]

# reduplicated cases
stem -> -4.2         [:]       [as=it,tmp=[c1=1,pre=me],v=inf];[as=it,tmp=[c1=1,pre=None],v=agt];[as=it,tmp=[c1=1,pre=me],v=ins]
/C -> -4.2           [:]       [as=it,tmp=[c1=1]]
te -> -4.2           [:]       [as=it,tmp=[c1=1]]
a/ -> -4.2           [:]       [as=it,tmp=[c1=1]]
man -> -4.2          [:]       [tmp=[c1=1]]

### B (CC_C, C2 cannot be L)

-3V -> -2B          [e:]       [tmp=[v1=e]]
# can be y or w: qeyyere, lewweTe
-2B -> -2B_         [X/L]
-2B_ -> -2V         [_]        [vc=ps,v=agt,tmp=[+c_2gem]];[vc=smp,tmp=[+c_2gem]];[vc=cs,tmp=[+c_2gem]];[vc=tr,tmp=[+c_2gem]]
# Drop the gemination in passive infinitive and instrumental
-2B_ -> -2V         [:_]       [vc=ps,v=inf,tmp=[-c_2gem]];[vc=ps,v=ins,tmp=[-c_2gem]]

# initial L; no vc=tr; c1=None
-3L -> -3LBV        [:']       [vc=smp];[vc=ps];[vc=cs]
-3LBV -> -2B        [a:]       [tmp=[v1=a]]

### Quad (CCCC, C|CCC)

-2.4 -> -2V         [X]

-3.4 -> -2.4        [X/L]
-4.4V -> -3.4       [e:]     [tmp=[c2=2]]

# C2=L: babba
-4.4V -> -2.4       [a:']    [tmp=[c2=None,-c_2gem,v1=a]]

-4.4 -> -4.4V       [X/L]
# C1=L: aneTTese; c1=None
-4.4L -> -3.4       [a:']    [tmp=[c1=None,v1=a]]
-5.4V -> -4.4       [e:]     [tmp=[v1=e]]
-5.4 -> -5.4V       [X]

simp -> -4.4        [:]     
simp -> -5.4        [:]

ast -> -2.4         [a:']
tt -> -2.4          [a:']

# C1=L; c1=None
tmp -> -4.4L      [:]       [vc=smp]

### ...aCC: C (CaCC), CCaCC, C|CaCC, C|CCaCC
### including as=it versions of nearly all classes

# sbr[as=it]: meseb<a>ber
-3aV -> -2.4        [a]
# sbr[as=it]: meseba<b>er; Ty_q[as=it]: meTeyay_eq
-2.4 -> -2.4_       [X]
-2.4_ -> -2V        [_]        [v=agt,tmp=[+c_2gem]];[v=inf,vc=tr,tmp=[+c_2gem]];[v=inf,vc=cs,tmp=[+c_2gem]];[v=inf,vc=smp,tmp=[+c_2gem]];[v=ins,vc=tr,tmp=[+c_2gem]];[v=ins,vc=cs,tmp=[+c_2gem]];[v=ins,vc=smp,tmp=[+c_2gem]]
-2.4_ -> -2V        [:_]       [v=man,tmp=[-c_2gem]];[v=inf,tmp=[-c_2gem]];[v=ins,tmp=[-c_2gem]]
-2.4_ -> -2V        [:]        [tmp=[-c_2gem]]

# sbr[as=it]: mese<b>aber
-3a -> -3aV         [X]        [tmp=[-c_2gem]]
# -3aV -> -3aV_       [_;:]
# most verbs; sbr[as=it]: mes<e>baber
-4aV -> -3a         [e:]      [tmp=[v1=e]]
# belexaxxe; CCaCC +it verbs
-4aV -> -3a         [e:a]     [as=it,tmp=[v1=e]];[v=man,tmp=[v1=e]]

# tegfafi (need to specify the whole path from here to end)
-4a.L -> -4a.LV     [X/L]
-4a.LV -> -3a.L     [:]       [as=it,vc=ps];[as=it,vc=tr];[v=man]
-3a.L -> -3aV.L     [X]
-3aV.L -> -2.L.4    [a]
-2.L.4 -> -2.L.4_   [X]
-2.L.4_ -> -2.LV    [:]
-2.LV -> end        [i:']     [v=agt,tmp=[suff=i,v_1=None,c_1=None]];[v=ins,tmp=[suff=iya,v_1=None,c_1=None]]
-2.LV -> -2a.LV     [a:]      [v=inf,tmp=[suff=None,v_1=a]]
-2a.LV -> end       [t:']     [tmp=[c_1=None]]
-2.LV -> end        [:']      [v=man,tmp=[suff=None,v_1=None,c_1=None]]

# most reduplicated cases; sbr[as=it]: me<s>ebaber
-4a -> -4aV         [X/L]
-5aV -> -4a         [e:]      [tmp=[v1=e]]
-5a -> -5aV         [X/L]
# L in position 1, +it (smp, ps, cs)
-4aL -> -4aLV       [:']      [vc=smp]
-4aLV -> -3a        [a:]
-4aL -> -3a         [a:']   [vc=cs]
-4aL -> -3a         [:']     [vc=ps]

aste -> -3a         [:]     [tmp=[c1=None]]
asteM -> -3a        [:]     [tmp=[c1=None]]

| -> -3a            [:|]
| -> -4a            [:|]
| -> -4.4           [:|]   [tmp=[c1=1,c2=2,-c_2gem,v1=None]]
| -> -5a            [:|]   [tmp=[c1=1,c2=2,-c_2gem,v1=None]]

# manner CCC -> CeCaCeC, CCCC -> CeCeCaCeC
man -> -4a          [:]   [tmp=[c1=1,-c_2gem,c2=2]]
man -> -5a          [:]   [tmp=[c1=1,-c_2gem,c2=2]]

simp -> -3a         [:]   [tmp=[c2=2]]
# most reduplication: sbr[as=it]: me.sebaber
simp -> -4a         [:]   [tmp=[c2=2]]
# tegbabi
te -> -4a.L         [:]   [tmp=[c1=1,c2=2,-c_2gem]]
# agbab
man0 -> -4a.L       [:]   [tmp=[c1=1,c2=2,-c1gem,-c_2gem]]
# magbabat, magbabiya, agbabi
a -> -4a.L          [:]   [tmp=[c1=1,c2=2,-c_2gem]]
# megbabat, megbabiya
stem -> -4a.L       [:]   [v=inf,vc=ps,tmp=[c1=1,pre=me,-c1gem,-c_2gem,c2=2]];[v=ins,vc=ps,tmp=[c1=1,pre=me,-c1gem,-c_2gem,c2=2]]
simp -> -5a         [:]   [tmp=[c2=2,-c_2gem]]

# C1=L, CCC, iterative passive
#as -> -4aL          [:]       [vc=cs,tmp=[c1=None]]
te -> -4aL          [:]       [tmp=[c1=None]]
#stem  -> -4aL       [:]       [vc=smp,tmp=[c1=None]]

# +it for CCCC with C1=L
stem -> -4a         [a:']     [vc=smp,tmp=[c1=None,pre=None]]
a/ -> -4a           [:']      [tmp=[c1=None,pre=a]]
as -> -4a           [:']      [vc=cs,tmp=[c1=None,pre=as]]
te -> -4a           [:']      [tmp=[c1=None,pre=te]]

ast -> -3a          [e:']      [tmp=[c1=None,v1=None]]
tt -> -3a           [e:']      [tmp=[c1=None,v1=None]]

end ->
