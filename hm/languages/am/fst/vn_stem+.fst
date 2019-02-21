#### Amharic infinitive, agent, instrumental, manner noun
### AGENT
## sebari:     1esa3i
### INSTRUMENTAL
## mesberiya:  me12e3iya
### MANNER
## as_ebaber:  a1_e2a2e3
###
### Template features:
### pre:    {te, a, as, aste, me, ma, mas, maste, teste, meste, None}
### c1:     {1, 2, None}
### c2:     {2, None}
### c3:     {3, None}
### c4:     {4, None}
### c_1:    {c, t, None}
### c_2:    {1, 2, 3, 4, None}
### c1gem:  {True, False}
### c_2gem: {True, False}
### v1:     {e, a, Wa, i, None}
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
start -> tmp       [:]

tmp -> stem       <me:>     [v=inf];[v=ins]
tmp -> stem       [:]       [v=agt]
tmp -> man0       [a:]      [v=man,vc=smp,as=smp,tmp=[pre=a]]
man0 -> man        [/:]     [tmp=[+c1gem]]

stem -> a0         [:]        [v=inf,vc=tr,tmp=[pre=ma]];[v=agt,vc=tr,tmp=[pre=a]];[v=ins,vc=tr,tmp=[pre=ma]]
a0 -> a            [a:]       [tmp=[-c1gem]]
a0 -> a/           <a/:>      [as=rc,tmp=[+c1gem]];[as=it,tmp=[+c1gem]]
stem -> te         <te:>      [vc=ps,v=agt,tmp=[pre=te,-c1gem]]
stem -> /C         [/:]       [vc=ps,v=inf,tmp=[pre=me,+c1gem]];[vc=ps,v=ins,tmp=[pre=me,+c1gem]]
stem -> |          [X/L]      [vc=ps,v=inf,tmp=[pre=me,-c1gem]];[vc=ps,v=ins,tmp=[pre=me,-c1gem]]
te -> |            [X/L]      
a -> |             [X/L]      [tmp=[-c1gem]]
man0 -> |          [X/L]      [tmp=[-c1gem]]
stem -> tt         <t_:>      [vc=ps,v=inf,tmp=[pre=met,-c1gem]];[vc=ps,v=ins,tmp=[pre=met,-c1gem]]

stem -> as         <as:>      [tmp=[-c1gem]]
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
# ... sbr[as=it]: mesebab<e>r, megelb<e>T
-2V -> -1           [e:]      [v=man,tmp=[v_1=e]];[v=inf,tmp=[v_1=e]];[v=ins,tmp=[v_1=e]]
-2V -> -1           [a:]      [v=agt,tmp=[v_1=a]]

# Final L
-2V -> -1C          [:']      [v=agt,tmp=[-c1gem,v_1=None,c_1=None]];[v=man,tmp=[v_1=None,c_1=None]];[v=ins,tmp=[-c1gem,v_1=None,c_1=None]]
-2V -> -2V.t        [a:']     [v=inf,tmp=[v_1=a]]
-2V.t -> end        [t:]      [tmp=[suff=None,c_1=t]]
# Final *
-2V -> -1C          [:*]      [v=agt,tmp=[v_1=None,c_1=None,-c_2gem]];[v=man,tmp=[v_1=None,c_1=None,-c_2gem]];[v=ins,tmp=[v_1=None,c_1=None,-c_2gem]]
# infinitive and alternate for -* manner noun
-2V -> -2V.t        [e:*]     [v=man,tmp=[v_1=e,-c_2gem]];[v=inf,tmp=[v_1=e]]

### A (CCC, C2 cannot be L, w, or y)

-2A -> -2A_         [X!]      [tmp=[n=3,c_2=None]];[tmp=[n=4,c_2=3]]
-2A_ -> -2V         [:]       [vc=smp,tmp=[-c_2gem]];[vc=tr,tmp=[-c_2gem]];[vc=ps,tmp=[-c_2gem]]
-2A_ -> -2V         [_:]      [vc=cs,tmp=[+c_2gem]]

simp -> -3          [:]       [tmp=[c2=2,n=3,v2=None,v3=None,v4=None,c3=None,c4=None]]
# Following L, y and w also possible
-3 -> -3V           [X/L]
-3V -> -2A          [e:]      [vc=ps,tmp=[v1=e]];[vc=cs,tmp=[v1=e]];[v=man,tmp=[v1=e]];[v=agt,vc=smp,tmp=[v1=e]];[tmp=[n=4,v2=e]]
# transitive agent is aC1C2aC3; n=4: manTes, masneTes, meneTes
-3V -> -2A          [:]       [vc=smp,v=inf,tmp=[v1=None]];[vc=tr,v=inf,tmp=[v1=None]];[vc=smp,v=ins,tmp=[v1=None]];[vc=tr,v=ins,tmp=[v1=None]];[vc=tr,v=agt,tmp=[v1=None]]

# C1=L; no vc=tr possible; c1=None
-3L -> -3LV         [:']      [tmp=[c1=None]]
-3LV -> -2AL        [a:]
-2AL -> -2A_        [X/L]     [tmp=[c_2=2]]

as -> L1.as         [:]       [vc=cs,v=agt,tmp=[pre=None]];[vc=cs,v=inf,tmp=[pre=mas]];[vc=cs,v=ins,tmp=[pre=mas]]
L1.as -> -3LV       [:']      [tmp=[c1=None,c2=None,n=3,v1=a,v2=None,v3=None,v4=None,c3=None,c4=None]]
stem -> L1          [:]       [v=inf,tmp=[pre=ma,v1=None]];[v=ins,tmp=[pre=ma,v1=None]];[v=agt,tmp=[pre=None,v1=a]]
L1 -> -3LV          [:']      [vc=smp,as=smp,tmp=[c1=None,c2=None,n=3,v2=None,v3=None,v4=None,c3=None,c4=None]];[vc=smp,as=it,tmp=[c1=None,c2=None,n=3,v2=None,v3=None,v4=None,c3=None,c4=None]]
te -> -3LV          [:']      [tmp=[c1=None,c2=None,n=3,v1=a,v2=None,v3=None,v4=None,c3=None,c4=None]]
tt -> -3LV          [:']      [tmp=[c1=None,c2=None,n=3,v1=a,v2=None,v3=None,v4=None,c3=None,c4=None]]

# C1=L in CCCC; apparently behaves like CCC in ps and cs (no tr); c1=None
as -> -3            [:']      [vc=cs,v=agt,tmp=[c1=None,pre=as,n=4,v1=None,v2=e,v3=None,v4=None,c2=2,c3=None,c4=None]];[vc=cs,v=inf,tmp=[c1=None,pre=mas,n=4,v1=None,v2=e,v3=None,v4=None,c2=2,c3=None,c4=None]];[vc=cs,v=ins,tmp=[c1=None,pre=mas,n=4,v1=None,v2=e,v3=None,v4=None,c2=2,c3=None,c4=None]]
te -> -3            [:']      [tmp=[c1=None,c2=2,n=4,v1=None,v2=e,v3=None,v4=None,c3=None,c4=None]]
/C -> -3            [:']      [tmp=[c1=2,+c1gem,v1=e,c2=None,n=4,v2=None,v3=None,v4=None,c3=None,c4=None]]
stem -> smp4L       [a:']     [v=inf,vc=smp,as=smp,tmp=[pre=ma,c1=None,c2=2,n=4,v1=None,v2=None,v3=None,v4=None,c3=None,c4=None]];[v=agt,vc=smp,as=smp,tmp=[pre=None,c1=None,c2=2,n=4,v1=a,v2=None,v3=None,v4=None,c3=None,c4=None]];[v=ins,vc=smp,as=smp,tmp=[pre=ma,c1=None,c2=2,n=4,v1=None,v2=None,v3=None,v4=None,c3=None,c4=None]]
smp4L -> -2A        [X/L]     

### A (C*C, imperfective with w, y, L as C2; reduplicated: CaC*C)
### the same pattern of vowels works with all reduplicated forms

-3.2 -> -3V.2        [X/L]     [as=smp,tmp=[-c_2gem]];[as=it,tmp=[c2=None,-c_2gem]];[v=man,tmp=[c2=None,-c_2gem]]
# C2=y; two categories (mecer, mefEz)
-3.2 -> -3PV.2       [J]       [tmp=[-c_2gem]]
-3.2 -> -3~PV.2      [~J]      [tmp=[-c_2gem]]

# mWac, zWari
-3.2 -> -3Vw.2       [gW:g;hW:h;kW:k;qW:q]         [v=agt]
-3.2 -> -3Vw.2       [bW:b;cW:c;CW:C;dW:d;fW:f]    [v=agt]
-3.2 -> -3Vw.2       [jW:j;lW:l;mW:m;nW:n]         [v=agt]
-3.2 -> -3Vw.2       [rW:r;sW:s;SW:S]              [v=agt]
-3.2 -> -3Vw.2       [tW:t;TW:T;xW:x;zW:z]         [v=agt]
-3Vw.2 -> -1         [a:w]                         [tmp=[-c_2gem,v_1=Wa,v1=None,c_2=None]]

# C2='
-3V.2 -> -1          [a:']     [as=smp,tmp=[v_1=a,v1=None,c_2=None]];[as=it,tmp=[v_1=a,v2=None,c_2=1]];[v=man,tmp=[v_1=a,v2=None,c_2=1]]

# memot
-3V.2 -> -1          [o:w]     [v=inf,as=smp,tmp=[v_1=o,v1=None,c_2=None]];[v=ins,as=smp,tmp=[v_1=o,v1=None,c_2=None]];[v=inf,as=rc,tmp=[v_1=o,v1=None,c_2=None]];[v=ins,as=rc,tmp=[v_1=o,v1=None,c_2=None]]

# memWamWat (labialization handled in stem_dup)
-3.2w -> -3V.2w      [X/L]     [as=smp,tmp=[-c_2gem]];[as=it,tmp=[c2=None,-c_2gem]];[v=man,tmp=[c2=None,-c_2gem]]
-3V.2w -> -1         [a:w]     [v=man,tmp=[c2=None,v_1=Wa,v2=None,c_2=1]];[v=agt,tmp=[v_1=Wa,v1=Wa,v2=None,c_2=1]];[v=inf,as=it,tmp=[v_1=Wa,v1=Wa,v2=None,c_2=1]];[v=ins,as=it,tmp=[v_1=Wa,v1=Wa,v2=None,c_2=1]]

# mexeT
-3PV.2 -> -1         [e:y]     [v=inf,as=smp,tmp=[v_1=e,v1=None,c_2=None]];[v=ins,as=smp,tmp=[v_1=e,v1=None,c_2=None]];[v=inf,as=rc,tmp=[v_1=e,v1=None,c_2=None]];[v=ins,as=rc,tmp=[v_1=e,v1=None,c_2=None]]
# mexaxaT
-3PV.2 -> -1         [a:y]     [v=man,tmp=[v_1=a,v2=None,c2=None,c_2=1]];[v=agt,as=it,tmp=[v_1=a,v2=None,c2=None,c_2=1]];[v=inf,as=it,tmp=[v_1=a,v2=None,c2=None,c_2=1]];[v=ins,as=it,tmp=[v_1=a,v2=None,c2=None,c_2=1]];[v=agt,as=smp,tmp=[v1=a,v_1=None,v2=None,c2=None,c_2=None]]

# mefEz
-3~PV.2 -> -1        [E:y]     [v=inf,as=smp,tmp=[v_1=E,v1=None,c_2=None]];[v=ins,as=smp,tmp=[v_1=E,v1=None,c_2=None]]
# mefafEz v1=a, v_1=E, v2|v3|v4=None; c1=1, c_1=3, c_2=1, c2|c3|c4=None;
-3~PV.2 -> -1        [E:y]     [v=man,tmp=[v_1=E,v2=None,c2=None,c_2=1]];[v=inf,as=it,tmp=[v_1=E,c_2=1]];[v=ins,as=it,tmp=[v_1=E,c_2=1]]
# both smp agent (fiyaZ) and it agent (fafiyaZ)
-3~PV.2 -> -1        <iya:y>   [v=agt,tmp=[v_1=a,v1=i,c_2=2]]

simp -> -3.2         [:]       [tmp=[c2=None,v2=None,v3=None,v4=None,n=3,c3=None,c4=None]]

# reduplicated cases
stem -> -4.2         [:]       [as=it,vc=smp,tmp=[c1=1,-c1gem,pre=me,n=3,c3=None,c4=None],v=inf];[as=it,vc=smp,tmp=[c1=1,-c1gem,pre=None,n=3,c3=None,c4=None],v=agt];[as=it,vc=smp,tmp=[c1=1,-c1gem,pre=me,n=3,c3=None,c4=None],v=ins]
/C -> -4.2           [:]       [as=it,tmp=[c1=1,n=3,c3=None,c4=None]]
te -> -4.2           [:]       [as=it,tmp=[c1=1,n=3,c3=None,c4=None]]
a/ -> -4.2           [:]       [as=it,tmp=[c1=1,n=3,c3=None,c4=None]]
man -> -4.2          [:]       [tmp=[c1=1,n=3,c2=None,c3=None,c4=None]]
-4.2 -> -4V.2        [X]
-4V.2 -> -3.2        [a]       [tmp=[v1=a,v3=None,v4=None]]
-4V.2 -> -3.2w       [a]       [tmp=[v1=Wa,v3=None,v4=None]]

### B (CC_C, C2 cannot be L)

-3V -> -2B          [e:]       [tmp=[v1=e]]
# can be y or w: qeyyere, lewweTe
-2B -> -2B_         [X/L]      [tmp=[c_2=None]]
-2B_ -> -2V         [_]        [vc=ps,v=agt,tmp=[+c_2gem]];[vc=smp,tmp=[+c_2gem]];[vc=cs,tmp=[+c_2gem]];[vc=tr,tmp=[+c_2gem]]
# Drop the gemination in passive infinitive and instrumental
-2B_ -> -2V         [:_]       [vc=ps,v=inf,tmp=[-c_2gem]];[vc=ps,v=ins,tmp=[-c_2gem]]

# initial L; no vc=tr; c1=None
#-3L -> -3LBV        [:']       [vc=smp];[vc=ps];[vc=cs]
#-3LBV -> -2B        [a:]       [tmp=[v1=a]]
-3LV -> -2BL         [a:]       #[tmp=[v1=a]]
-2BL -> -2B_         [X/L]      [tmp=[c_2=2]]

### Quad (CCCC, C|CCC)

-2.4 -> -2V         [X]
-3.4 -> -3.4V       [X/L]
-3.4V -> -2.4       [:]      [as=smp,tmp=[v2=None]];[as=smp,tmp=[v2=e,n=5]]
-3.4V -> -2.4       [a]      [as=rc,tmp=[n=4,v2=a]];[as=rc,tmp=[n=5,v2=e,v3=a,c3=3]]

simp -> -4.4        [:]      [tmp=[n=4,-c_2gem,c3=None,c4=None]]
-4.4 -> -4.4V       [X/L]    [tmp=[c_2=3,n=4,c3=None,c4=None,v3=None,v4=None]];[tmp=[c_2=4,n=5,c3=3,c4=None,v3=None,v4=None]]
-4.4V -> -3.4       [e:]     [tmp=[n=4,c2=2,v1=e]];[tmp=[n=5,v2=e]]

# C2=L: mebabat
-4.4V -> -2.4       [a:']    [tmp=[c2=None,v1=a,v2=None,c_2=3]]

#tt -> -2.4          [a:']    [tmp=[c3=None,c4=None]]

### 5-consonant roots
simp -> -5.5        [:]      [tmp=[n=5,c2=2,v1=e,v2=e,v3=None,v4=None,c_2=4,-c_2gem,c3=3,c4=None]]
-5.5 -> -5.5V       [X]      
# vowel following first consonant of 5-consonant verbs: mew<e>xenger
-5.5V -> -4.5       [e:]     
-4.5 -> -4.5V       [X/L]    
-4.5V -> -3.5       [e:]     
-3.5 -> -3.5V       [X/L]    
-3.5V -> -2.4       [:]      [as=smp,tmp=[v3=None,v4=None]]
-3.5V -> -2.4       [a]      [as=rc]

### ...aCC: "C" verbs (CaCC), CCaCC, C|CaCC, C|CCaCC
### including as=it versions of nearly all classes

# sbr[as=it]: meseb<a>ber; megel<a>meT
-3aV -> -3aV3       [:]       [tmp=[n=3]]
-3aV -> -3aV4       [:]       [tmp=[n=4]]
-3aV -> -3aV5       [:]       [tmp=[n=5]]
-3aV3 -> -2.4       [a]       [tmp=[v2=a,v3=None,v4=None]];[tmp=[v1=a,c_1=2,c_2=None]];[tmp=[c_1=c,c_2=None,v1=a,v2=None,v3=None,v4=None]]
-3aV4 -> -2.4       [a]       [as=it,tmp=[v2=e,v3=a,v4=None]];[v=man,tmp=[v2=e,v3=a,v4=None]];[as=smp,tmp=[v2=a,v3=None,v4=None]]
-3aV5 -> -2.4       [a]       [as=it,tmp=[v2=e,v3=e,v4=a]];[as=rc,tmp=[v2=e,v3=a,v4=None]];[v=man,tmp=[v2=e,v3=e,v4=a]];[as=smp,tmp=[v2=e,v3=a,v4=None]]
# sbr[as=it]: meseba<b>er; Ty_q[as=it]: meTeyay_eq
-2.4 -> -2.4_       [X]
-2.4_ -> -2V        [_]        [v=agt,tmp=[+c_2gem]];[v=inf,vc=tr,tmp=[+c_2gem]];[v=inf,vc=cs,tmp=[+c_2gem]];[v=inf,vc=smp,tmp=[+c_2gem]];[v=ins,vc=tr,tmp=[+c_2gem]];[v=ins,vc=cs,tmp=[+c_2gem]];[v=ins,vc=smp,tmp=[+c_2gem]]
-2.4_ -> -2V        [:_]       [tmp=[-c_2gem]]
-2.4_ -> -2V        [:]        [tmp=[-c_2gem]]

# tegbabi
te -> -4a.L         [:]   [tmp=[c1=1,v1=None,c2=2,c_2=2,-c_2gem,n=3,c3=None,c4=None]]
# agbab
man0 -> -4a.L       [:]   [tmp=[c1=1,c2=2,c_2=2,-c_2gem,n=3,c3=None,c4=None]]
# magbabat, magbabiya, agbabi
#a -> -4a.L          [:]   [tmp=[c1=1,c2=2,c_2=2,-c_2gem,n=3,c3=None,c4=None]]
# megbabat, megbabiya
stem -> -4a.L       [:]   [v=inf,vc=ps,tmp=[c1=1,v1=None,pre=me,-c1gem,-c_2gem,c2=2,c_2=2,n=3,c3=None,c4=None]];[v=ins,vc=ps,tmp=[c1=1,v1=None,pre=me,-c1gem,-c_2gem,c2=2,c_2=2,n=3,c3=None,c4=None]]
# meggebabat
/C -> -4a.L         [:]   [v=inf,vc=ps,tmp=[c1=1,pre=me,-c_2gem,c2=2,c_2=2,n=3,c3=None,c4=None]];[v=ins,vc=ps,tmp=[c1=1,pre=me,-c_2gem,c2=2,c_2=2,n=3,c3=None,c4=None]]
a0 -> -4a.L         [a:]  [v=inf,tmp=[c1=1,-c_2gem,c2=2,c_2=2,n=3,c3=None,c4=None]];[v=ins,tmp=[c1=1,-c_2gem,c2=2,c_2=2,n=3,c3=None,c4=None]];[v=agt,tmp=[c1=1,-c_2gem,c2=2,c_2=2,n=3,c3=None,c4=None]]
# tegfafi, megbabat (need to specify the whole path from here to end)
-4a.L -> -4a.LV     [X/L]
-4a.LV -> -3a.L     [:]       [as=it,vc=ps,tmp=[v1=None,-c1gem]];[v=man,tmp=[v1=None,-c1gem]];[as=it,vc=tr,tmp=[v1=None,-c1gem]]
-4a.LV -> -3a.L     [e:]      [v=man,tmp=[v1=e,+c1gem]];[as=it,vc=ps,tmp=[v1=e,+c1gem]];[as=it,vc=tr,tmp=[v1=e,+c1gem]];[as=it,vc=smp,tmp=[v1=e,-c1gem]]
-3a.L -> -3aV.L     [X]
-3aV.L -> -2.L.4    [a]       [tmp=[v2=a,v3=None,v4=None]]
-2.L.4 -> -2.L.4_   [X]
-2.L.4_ -> -2.LV    [:]
-2.LV -> -2i.LV     [i:']     [v=agt,tmp=[suff=i,v_1=None,c_1=None]];[v=ins,tmp=[suff=iya,v_1=None,c_1=None]]
-2i.LV -> end       [a:]      [v=ins]
-2i.LV -> end       [:]       [v=agt]
-2.LV -> -2a.LV     [a:]      [v=inf,tmp=[suff=None,v_1=a]]
-2a.LV -> end       [t:']     [tmp=[c_1=t]]
-2.LV -> end        [:']      [v=man,tmp=[suff=None,v_1=None,c_1=None]]

# most reduplicated cases
# sbr[as=it]: mese<b>aber
-3a -> -3aV         [X]      [tmp=[-c_2gem]]

# sbr[as=it]: me<s>ebaber, [v=man]: 'a<ss>ebaber
-4a -> -4aV         [X/L]
# sbr[as=it]: mes<e>baber; sbr[v=man]: ass<e>baber
-4aV -> -3a         [e:]     [as=it,tmp=[v1=e]];[tmp=[n=4,v1=e]];[tmp=[n=5,v2=e]];[v=man,tmp=[n=3,v1=e]]
-4aV -> -3a         [:]      [tmp=[v1=None,-c1gem]]
# mebel<e>xaxet; CCaCC; menker<e>tatet
-4aV -> -3a         [e:a]    [as=it,tmp=[n=3,v1=e]];[v=man,tmp=[n=3,v1=e]];[as=it,tmp=[n=4,v1=e,v2=e]];[v=man,tmp=[n=4,v1=e,v2=e]];[as=it,tmp=[n=5,v2=e,v3=e]];[v=man,tmp=[n=5,v2=e,v3=e]]
# L in position 1, +it (smp, ps, cs)
-4aL -> -4aLV       [:']     [vc=smp]
-4aLV -> -3a        [a:]     [tmp=[v2=a]]
-4aL -> -3a         [a:']    [vc=cs]
-4aL -> -3a         [:']     [as=it,vc=ps,tmp=[v1=None,c2=2,c_2=2]]
# 'abe<>bab
man -> mC.LCL       [X/L]    [tmp=[c1=1,-c_2gem,c2=None,n=4,c_2=3,c3=3,c4=None,v1=e,v2=None,v3=a,v4=None]]
mC.LCL -> mCL.CL    [e:]
mCL.CL -> mCL..CL   [:']
mCL..CL -> mCLC.L   [X/L]
mCLC.L -> -2.4      [a]

# megelebabeT; aggelebabeT
-5a -> -5aV         [X/L]
-5aV -> -4a         [e:]    [tmp=[n=5,v2=e,c3=3]];[as=it,tmp=[n=4,v2=e,c3=3]];[v=man,tmp=[n=4,v2=e,c3=3]] #;[v=man,tmp=[n=5,v2=e,c3=3]];[as=it,tmp=[n=5,v2=e,c3=3]]
# mewexenegager
-6a -> -6aV         [X/L]
-6aV -> -5a         [e:]    [as=it,tmp=[n=5,v2=e,c3=3]];[v=man,tmp=[n=5,v2=e,c3=3]]

aste -> -3a         [:]     [tmp=[c1=None,n=3,c3=None,c4=None,c2=2,c_2=2]]
asteM -> -3a        [:]     [tmp=[c1=None,n=3,c3=None,c4=None,c2=2,c_2=2]]

# mensafef
| -> -3a            [:|]   [tmp=[n=4,v1=None,c1=1,c2=2,c3=None,c4=None,c_2=3]]
# needed at least for as=rc
| -> -4a            [:|]   [tmp=[n=5,v1=None,c1=1,c2=2,c3=3,c4=None,c_2=4]]
| -> -4.4           [:|]   [tmp=[c1=1,c2=2,c_2=4,v1=None,-c_2gem,n=5]]
| -> -5a            [:|]   [as=it,tmp=[c1=1,c2=2,c3=3,c4=4,c_2=4,v1=None,-c_2gem,n=5]];[v=man,tmp=[c1=1,c2=2,c3=3,c4=4,c_2=4,v1=None,-c_2gem,n=5]]

# manner CCC -> CeCaCeC, CCCC -> CeCeCaCeC
man -> -4a          [:]   [tmp=[c1=1,-c_2gem,c2=2,n=3,c_2=2,c3=None,c4=None]]
# anneTaTes
man -> man4L        [:']  [tmp=[c1=2,-c_2gem,c2=None,n=4,c_2=3,c3=3,c4=None,v1=None,v2=e,v3=a]]
man4L -> man4L.     [X/L]
man4L. -> -3a       [e:]
man -> -5a          [:]   [tmp=[c1=1,-c_2gem,c2=2,n=4,c_2=3,c3=3,c4=None]]
man -> -6a          [:]   [tmp=[c1=1,-c_2gem,c2=2,n=5,c_2=4,c3=3,c4=4,v1=e]]

simp -> -3a         [:]   [tmp=[c2=2,n=3,v2=None,v3=None,v4=None,c3=None,c4=None]]
# most reduplication: sbr[as=it]: me.sebaber
simp -> -4a         [:]   [as=it,tmp=[c2=2,n=3,c_2=2,v2=a,v3=None,v4=None,c3=None,c4=None]];[as=smp,tmp=[c2=2,n=4,c_2=3,c3=None,c4=None]]

# CCCC iterative
simp -> -5a         [:]   [as=it,tmp=[c2=2,-c_2gem,c_2=3,n=4,c3=3,c4=None]]
# CCCCC iterative
simp -> -6a         [:]   [as=it,tmp=[c2=2,-c_2gem,c_2=4,n=5,c3=3,c4=4,v1=e]]

# C1=L, CCC, iterative passive
te -> -4aL          [:]       [tmp=[c1=None,n=3,c3=None,c4=None]]

## +it for CCCC with C1=L
#stem -> -4a         [a:']     [vc=smp,tmp=[c1=None,pre=None,n=4,c3=None,c4=None]]
#a/ -> -4a           [:']      [tmp=[c1=None,pre=a,n=4,c3=None,c4=None]]
#as -> -4a           [:']      [vc=cs,tmp=[c1=None,pre=as,n=4,c3=None,c4=None]]
#te -> -4a           [:']      [tmp=[c1=None,pre=te,n=4,c3=None,c4=None]]

tt -> -3a           [e:']      [tmp=[c1=None,v1=e,n=3,c2=2,c_2=2,c3=None,c4=None]]

end ->
