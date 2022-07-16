### Basic prefixes and suffixes

-> start

## CONJUNCTIONS, PREPOSITIONS, RELATIVE
# none
start -> neg    [:]    [-cp,-sub]
start -> neg    [የ]     [cp=የ,+sub]
start -> neg    [በ]     [cp=በ,+sub]

## NEGATIVE PREFIX
neg -> spre      <ኣን>   [+neg,tm=prf]
neg -> spre      <ኣት>   [+neg,tm=imf|j_i,sp=2];[+neg,tm=imf|j_i,sp=3,sg=f,sn=1]
neg -> stem      [ኤ]    [+neg,tm=imf|j_i,sp=3,sg=m,sn=1];[+neg,tm=imf|j_i,sp=3,sn=2]
neg -> spre      [:]    [-neg]

## SUBJECT PREFIX
# Prefix only for imperfective and jussive
spre -> stem      [ይ]    [tm=imf,sp=3,sn=1,sg=m];[tm=imf,sp=0]
spre -> stem      [:]    [tm=prf];[tm=j_i,sp=2,-neg]

## STEM
stem -> ssuff   +v_stem+

## SUBJECT SUFFIXES
ssuff -> osuff    [=አ]    [tm=prf,sp=3,sn=1,sg=m]
ssuff -> osuff    [ነ]    [sp=1,sn=2]
ssuff -> osuff    [:]    [tm=imf,sp=3,sn=1,sg=m];[tm=imf,sp=2,sn=1,sg=m];[tm=imf,sp=1,sn=1]

## OBJECT SUFFIXES
osuff -> mvm     [:]    [op=None]

## MAIN VERB MARKER
# required for chh and muh
mvm -> end       [:ም]   [tm=prf]
mvm -> end       [=ኡ:]   [tm=imf,tl=M]
mvm -> end       [:]    [tm=imf,tl=c];[+neg];[tm=j_i];[+sub]

end ->
