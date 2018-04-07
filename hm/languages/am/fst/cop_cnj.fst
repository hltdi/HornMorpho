-> start

# These can't appear with non-subordinate negative
start -> end  [m:]              [cj2=m,-neg];[cj2=m,+sub]
start -> end  <m_a:>            [cj2=ma,-neg];[cj2=ma,+sub]
start -> end  <s_:>             [cj2=s,-neg];[cj2=s,+sub]
start -> end  <s_a:>            [cj2=sa,-neg];[cj2=sa,+sub]

# No constraints on appearance
start -> end  <n_a:>            [cj2=na]
start -> end  <nji:>            [cj2=Inji]   # only jussive/imperative?

# Interrogative suffixes
start -> end  <nI:>             [tm=imf,cj2=nI,-sub];[tm=prf,cj2=nI,-sub]
# start -> end  <ndE:>          [tm=imf,cj2=IndE,-sub];[tm=prf,cj2=IndE,-sub]

end ->
