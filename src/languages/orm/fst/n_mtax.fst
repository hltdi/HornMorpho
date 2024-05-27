### Oromo noun and adjective morphotactics
### Features
### case: {bs,sb,dat,ins,abl,loc} [voc missing]
### cnj: {s,f,simmoo,oo,woo,llee,mmoo,moo,tu,None}
### +-gen, +-fem, +-pl, +-def, +-1s_sbj

-> start

### STEM
# Irregular nouns may go to different states
# start            +irr_n_stem+
# start -> der       +n_stems+
# To skip derivational suffixes...
start -> defplr    +nouns+
start -> nf        +nouns_f+
nf -> defplr       [:]    [+fem]
start -> nm        +nouns_m+
nm -> defplr       [:]    [-fem]
start -> npl       +nouns_pl+
npl -> case        [:]    [+pl]

### DERIVATIONAL SUFFIXES

### DEFINITENESS, PLURAL (apparently both aren't possible)
# Replace the final vowel before -oota
defplr -> case    <Poota:> [+pl]
# Initial i- replaces any stem-final vowel
defplr -> def1    [D:]    [+def]
def1 -> case      <cha:>  [-fem]
def1 -> case      <ttii:> [+fem]
defplr -> case    [:]     [-def,-pl]

### CASE
## Cases: base (bs), subject (sb), genitive (gen), dative (dat), instrumental (ins),
## ablative (abl), locative (loc) [vocative (voc)]
## Genitive can co-occur with another case, so there are separate case and genitive features
# Base: no suffix
case -> conj     [:]      [case=bs,-gen]
# Subject: subject suffix depends on previous phonological context and on gender
case -> conj     [S:]     [case=sb,-gen]
# Genitive, dative, instrumental, ablative
# Lengthen final vowel or add -ii to n
case -> caseL    [L:]     
caseL -> conj    [:]      [case=abl,-gen];[case=dat,-gen];[case=bs,+gen]
caseL -> conj    [f:]     [case=dat,-gen]
caseL -> conj    [n:]     [case=ins,-gen]
caseL -> conj    <tii:>   [case=abl,+gen]
caseL -> conj    <tiin:>  [case=ins,+gen]
# is this possible?
caseL -> conj    <tiif:>  [case=dat,+gen]
# Optional -dhaa after long vowel, followed by 0, -f, -n
## Dative, instrumental, ablative
case -> dhaa    [H:]
dhaa -> conj    [:]      [case=dat,-gen];[case=ins,-gen];[case=abl,-gen]
dhaa -> conj    [f:]     [case=dat,-gen]
dhaa -> conj    [n:]     [case=ins,-gen]
## Locative
# doesn't require lengthened vowel
case -> conj     <tti:>   [case=loc]
## Not handled: Oromootitti

### CONJUNCTIONS; FOCUS (probably not complete)
## Assume all are compatible with all case, definiteness, plural suffixes
## (probably not true)
# -(V)s(i) and -Vf(i)
conj -> s     <(L)s:>      [cnj=s]
s -> end        [i:;:]     [-1s_sb]
s -> 1s_sb       [:]       [+1s_sb]
conj -> f     <Lf:>        [cnj=f]
f -> 1s_sb       [:]       [+1s_sb]
f -> end        [i:;:]     [-1s_sb]
conj -> 1s_sb   <simmoo:>  [cnj=simmoo]
conj -> 1s_sb   <oo:>      [cnj=oo]
conj -> 1s_sb   <woo:>     [cnj=woo]
conj -> 1s_sb   <llee:>    [cnj=llee]
conj -> 1s_sb   <mmoo:>    [cnj=mmoo]
conj -> 1s_sb   <moo:>     [cnj=moo]
# -tu is not really a conjunction, but seems not to co-occur with any of them
conj -> 1s_sb   <tu:>      [cnj=tu]
# No conjunction
conj -> 1s_sb   [:]        [cnj=None]

### 1S SUBJECT SUFFIX
# N is realized as -an following consonants, -n following vowels
# so we need a special character for it (realized in NN.fst)
# !!!
1s_sb -> end       [N:]      [+1s_sb]
1s_sb -> end       [:]       [-1s_sb]

end ->
