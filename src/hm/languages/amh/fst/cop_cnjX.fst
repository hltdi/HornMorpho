-> start

# These can't appear with non-subordinate negative
start -> end  <m:-m(@cconj,*ም,~cc)>               [cj2=m,-neg];[cj2=m,+sub]
start -> end  <m_a:-m_a(@cconj,*ማ,~cc )>            [cj2=ma,-neg];[cj2=ma,+sub]
start -> end  <s_:-s(@cconj,*ስ,~cc)>              [cj2=s,-neg];[cj2=s,+sub]
start -> end  <s_a:-s_a(@cconj,*ሳ,~cc)>            [cj2=sa,-neg];[cj2=sa,+sub]

# Make the negative suffix -m optional for negative copula
# % features copies from the TB
start -> end <m:-m(@part,ncm,$polarity=neg,*ም,~discourse)> [cj2=None,+neg]

# No constraints on appearance
start -> end  <n_a:-n_a(@cconj,*ና,~cc)>            [cj2=na]
start -> end  <nji:-nji(@cconj,*ንጂ,~cc)>           [cj2=Inji]   # only jussive/imperative?

# Interrogative suffixes
# start -> end  <nI:>             [tm=imf,cj2=nI,-sub];[tm=prf,cj2=nI,-sub]
# start -> end  <ndE:>          [tm=imf,cj2=IndE,-sub];[tm=prf,cj2=IndE,-sub]

end ->
