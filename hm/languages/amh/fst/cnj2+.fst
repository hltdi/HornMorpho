-> start

# These can't appear with non-subordinate negative
start -> end  <Im:-m(cnj2)>           [cj2=m,-neg];[cj2=m,+sub]
start -> end  <m_a:-m_a(cnj2)>        [cj2=ma,-neg];[cj2=ma,+sub]
start -> end  <s_:-s(cnj2)>           [cj2=s,-neg];[cj2=s,+sub]
start -> end  <s_a:-s_a(cnj2)>        [cj2=sa,-neg];[cj2=sa,+sub]

# No constraints on appearance
start -> end  <n_a:-n_a(cnj2)>        [cj2=na]
start -> end  <nji:-nji(cnj2)>        [cj2=Inji]   # only jussive/imperative?

# Interrogative suffixes
# (this just causes problems, so leave it out for now)
# start -> end  <nI:-nI(cnj2)>        [tm=imf,cj2=nI,-sub];[tm=prf,cj2=nI,-sub]

end ->
