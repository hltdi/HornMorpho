-> start

# % -m is usually ~cc but sometimes ~discourse in the TB; both may be right (i.e., it's ambiguous)
# These can't appear with non-subordinate negative
start -> end  <Im:-m(@cconj,*ም,~cc)>           [cj2=m,-neg];[cj2=m,+sub]
start -> end  <m_a:-m_a(@cconj,*ማ,~cc)>        [cj2=ma,-neg];[cj2=ma,+sub]
start -> end  <s_:-s(@cconj,*ስ,~cc)>           [cj2=s,-neg];[cj2=s,+sub]
start -> end  <s_a:-s_a(@cconj,*ሳ,~cc)>        [cj2=sa,-neg];[cj2=sa,+sub]

# No constraints on appearance
start -> end  <n_a:-n_a(@cconj,*ና,~cc)>        [cj2=na]
# Or is this an interjection?
start -> end  <nji:-nji(@cconj,*ንጂ,~cc)>        [cj2=Inji]   # only jussive/imperative?

# Interjection suffixes (for now call it cj2 in features)
start -> end <a:-A(@intj,*ኣ,~discourse)>    [cj2=a]

# Interrogative suffixes
# (this just causes problems, so leave it out for now)
# % this 
# start -> end  <nI:-nI(@cconj)>        [tm=imf,cj2=nI,-sub];[tm=prf,cj2=nI,-sub]

end ->
