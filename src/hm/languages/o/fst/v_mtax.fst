-> start

### OPTIONAL NEGATIVE PREFIX
# Possible with all tenses except perfect
start -> stem     <hin:>    [+neg,t=sub];[+neg,t=prs];[+neg,t=pst];[+neg,t=imv];[+neg,t=contemp]
# Absence of hin- does not necessarily mean -neg
start -> stem     [:]

### STEM
# Irregular verbs go to different states
stem            +irr_stem+
stem -> der     +v_stems+
# To skip derivational suffixes...
# stem -> stem_end  +v_stems+

### DERIVATIONAL SUFFIXES
## Passive
# T- is needed to get -tam- with roots ending in dh-: nyaatam-, dubbatam-
der -> pass      <Tam:>    [+ps,-autoben]
pass -> stem_end  [:]      [-cs]
## Passive + causative (unfortunately not distinguished from causative + passive)
pass -> stem_end  <siis:>  [+cs]
## Causative
der -> caus       [s:]    [+cs,-ps,-autoben]
caus -> caus1     [i:;ii:]
caus1 -> stem_end [s:]
# exclude the possibility of -s only since it's not really productive
#caus -> stem_end  [:]
## Autobenefactive
der -> autoben1   [a:;aa:]
autoben1 -> stem_end [dh:] [+autoben,-ps,-cs]
## Causative + passive (not distinguished from passive + causative)
der -> stem_end  <fam:>    [+ps,+cs,-autoben]
## Autobenefactive + passive
der -> stem_end  <fadh:>   [+ps,-cs,+autoben]
## To morpheme boundary before suffixes
der -> stem_end   [:]      [-ps,-cs,-autoben]

### STEM-SUFFIX BOUNDARY
# Morpheme boundary separating stem and suffixes
stem_end -> sbj   [+:]     

### SUBJECT SUFFIXES: -t-, -n-, -T-, -0-
## Non-finite forms: bypass subject and TAM endings
sbj -> nonfin     [:]      [p=0,t=None]
## No subject suffixes for imperative; go straight to imv state
sbj -> imv        [:]      [t=imv]
## No subject suffixes for subordinate/contemporary negative
sbj -> main      <in:>     [t=sub,+neg];[t=contemp,+neg]
## Subject suffixes for other forms
sbj -> sbj1       [:]      [t=prs];[t=pst];[t=sub,-neg];[t=contemp,-neg];[t=prf]
# -t-: 2 or 3sf
sbj1 -> sbj_t     [t:]     [p=2];[p=3,n=1,g=f]
# -tu: 2p; -ta, -te
# all TAM for 2s; all but prs,-neg for 3sf; nothing for 2p
sbj_t -> tam      [:]      [p=2,n=2,t=prs,-neg];[p=2,n=1];[p=3,n=1,g=f]
# -tan(i): 2p; past, present, subordinate, contemporary, perfect
sbj_t -> sbj_tan <an:>     [p=2,n=2]
sbj_tan -> main   <(i):>   [t=pst,-neg];[t=prs];[t=sub,-neg]
sbj_tan -> end    [uu:]    [t=contemp,-neg]
sbj_tan -> prf    [ii:]    [t=prf]
# 3sf pres
sbj_t -> main     [i:]     [p=3,n=1,g=f,t=prs,-neg]
# -n-: 1p
sbj1 -> sbj_n     [n:]
sbj_n -> tam      [:]      [p=1,n=2]
# past negative for all subjects
sbj_n -> main     [e:]     [t=pst,+neg]
# -0-: 1s
sbj1 -> tam       [:]      [p=1,n=1]
# -T-: 3; only surfaces following -dh-
sbj1 -> sbj_3     [T:]     [p=3]
# 3sm, 3p
sbj_3 -> tam      [:]      [n=1,g=m];[n=2,t=prs,-neg]
# 3p: -an(i); past, present, subordinate, contemporary, perfect
sbj_3 -> sbj_an  <an:>     [n=2]
sbj_an -> main   <(i):>    [t=pst,-neg];[t=prs];[t=sub,-neg]
sbj_an -> prf    [ii:]     [t=prf]
sbj_an -> end    [uu:;ii:] [t=contemp,-neg]

### TAM endings
## Present and past
# Present 1s, 1p, 3sm, 2s
tam -> main       [a:]     [t=prs,-neg,p=1];[t=prs,-neg,p=3,n=1,g=m];[t=prs,-neg,p=2,n=1]
# Past 1s, 1p, 3sm, 3sf, 2s (not 2p, 3p)
tam -> main       [e:]     [t=pst,-neg]
## Perfect
tam -> prf        [ee:]    [t=prf]
## Subordinate; present 2, 3 plural
tam -> end        [u:]     [t=sub,-neg];[t=prs,+neg]
tam -> main       [u:]     [t=prs,n=2,p=2|3,-neg]
## Contemporary
tam -> end        [uu:]    [t=contemp,-neg]
## Imperative affirmative: singular and plural
imv -> main       [aa:]    [-inter,p=2,n=2,-neg]
imv -> main       [I:]     [-inter,p=2,n=1,-neg]
## Imperative negative: i/ii difference is dialectal? (C G-M)
# Ti(i)n(aa): (T only surfaces after -dh-)
imv -> imv_neg    [T:]     [+neg,-inter]
imv_neg -> imv_i  [i:;ii:]
imv_i -> imv_in   [n:]
# singular and plural
imv_in -> main    [:]      [p=2,n=1]
imv_in -> main    [aa:]    [p=2,n=2]
## Perfect: subject agreement is duplicated in the TAM suffix
# all begin with -r; -t also possible for 2s, 2p, and 3sf
prf -> prf1       [r:]
prf -> prf1       [t:]    [p=2];[p=3,n=1,g=f]
# 1s, 3sm
prf1 -> main      [a:]    [p=1,n=1];[p=3,n=1,g=m]
# 2s 
prf1 -> main      <ta:>   [p=2,n=1]
# 3sf
prf1 -> main      <ti:>   [p=3,n=1,g=f]
# 1p
prf1 -> main      <ra:>   [p=1,n=2]
# 2p
prf1 -> main      <tu:>   [p=2,n=2]
# 3p
prf1 -> main      [u:]    [p=3,n=2]

### MAIN CLAUSE VERB SUFFIXES
### (CONT) (CASE)
### (CONJ)
###
## Lengthen final vowel for "continuative": interrogative or past/imperative sequence
main -> main1      [L:]    [+cont,cnj=None]
main -> main1      [:]     [-cont,cnj=None]
# Past continuative can have 1s subject suffix in compound tenses (without conjunctions?)
main1 -> 1s_sb     [:]     [t=pst,+cont,-dat,-ins]
# Present can have 1s subject suffix in compound tenses (without conjunctions?)
main -> 1s_sb      [:]     [t=prs,-cont,-dat,-ins,cnj=None]
## Case suffixes
# 3 person dative; lengthen V and add -f(i)
main1 -> end     <Lf(i):>  [+dat,-ins,-1s_sb]
main1 -> end      [:]      [-dat,-ins,-1s_sb]
# 3 person instrumental; lengthen V and add -n(i)
main1 -> end     <Ln(i):>  [+ins,-dat,-1s_sb]
## Various conjunctive suffixes, apparently only possible with -cont.
## Assume they cannot follow +cont or case suffixes
## and that 1s_sb cannot follow (this is probably WRONG)
main -> main2     [:]      [-cont,-dat,-ins,-1s_sb]
main2 -> end      <Ltii:>  [cnj=ti,t=imv]
main2 -> end      <Lti:>   [cnj=ti,t=pst]
# The L seems not to be required with -s
main2 -> s1       <(L)s:>  [cnj=s]
s1 -> end         <(i):>
main2 -> end      <Lf(i):> [cnj=f]
main2 -> end      <dhaaf:> [cnj=f]
main2 -> end      <tti:>   [cnj=tti]
main2 -> end      <llee:>  [cnj=llee]
main2 -> end      <yyuu:>  [cnj=yyuu]
main2 -> end       [:]     [cnj=None]

###  SUFFIXES FOR NON-FINITE FORMS: INFINITIVE, PARTICIPLE, AGENT, GERUND
# Infinitive; a noun also can have noun suffixes
nonfin -> noun     <Cuu:>   [+inf,-prt,-ger,-agt]
# Participle; can have 1s subj -n in compound tenses
nonfin -> 1s_sb    [aa:]    [+prt,-inf,-agt,-ger]
# Agent; these are nouns so they can have noun suffixes
nonfin -> noun     [aa:]    [+agt,-fem,-inf,-prt,-ger]
nonfin -> noun     <tuu:>   [+agt,+fem,-inf,-prt,-ger]
# Gerund; can probably have 1s subj -n
nonfin -> 1s_sb    <naan:>  [+ger,-inf,-prt,-agt]

### NOUN SUFFIXES: FOR INFINITIVES AND AGENTS
## Cases: base (bs), subject (sb), genitive (gen), dative (dat), instrumental (ins),
# ablative (abl), locative (loc) [vocative (voc)]
# Base, genitive
# No suffix can mean genitive because vowel is already long (omit??)
noun -> n_conj     [:]      [case=bs];[case=gen]
# Subject
# -n works for -uu (infinitive, fem. agent) and -aa (masc. agent)
noun -> end        [n:]     [case=sb]
# Dative, instrumental, ablative
noun -> n_conj     [f:]     [case=dat]
noun -> n_dhaa    <dhaa:>
n_dhaa -> n_conj   [:]      [case=dat];[case=ins];[case=abl]
n_dhaa -> n_conj   [f:]     [case=dat]
noun -> n_conj     [n:]     [case=ins]
n_dhaa -> n_conj   [n:]     [case=ins]
# Locative
noun -> n_conj     <tti:>   [case=loc]

### NOUN CONJUNCTIONS; FOCUS (probably not complete)
# -(V)s(i) and -Vf(i)
n_conj -> n_s     <(L)s:>    [cnj=s]
n_s -> end        [i:;:]     [-1s_sb]
n_s -> 1s_sb       [:]       [+1s_sb]
n_conj -> n_f     <Lf:>      [cnj=f]
n_f -> 1s_sb       [:]       [+1s_sb]
n_f -> end        [i:;:]     [-1s_sb]
n_conj -> 1s_sb   <simmoo:>  [cnj=simmoo]
n_conj -> 1s_sb   <oo:>      [cnj=oo]
n_conj -> 1s_sb   <woo:>     [cnj=woo]
n_conj -> 1s_sb   <llee:>    [cnj=llee]
n_conj -> 1s_sb   <mmoo:>    [cnj=mmoo]
n_conj -> 1s_sb   <moo:>     [cnj=moo]
# -tu is not really a conjunction, but seems not to co-occur with any of them
n_conj -> 1s_sb   <tu:>      [cnj=tu]
# No conjunction
n_conj -> 1s_sb   [:]        [cnj=None]

### 1S SUBJECT SUFFIX
# N is realized as -an following consonants, -n following vowels
# so we need a special character for it (realized in NN.fst)
# !!!
1s_sb -> end       [N:]      [+1s_sb,p=1,n=1];[+1s_sb,p=0]
1s_sb -> end       [:]       [-1s_sb]

end ->
