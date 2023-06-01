-> start

start -> start  [^N;/;+;-]     [t=p|c]
start -> suf      []		[t=i|j,sp=2|3,sn=2,+suf];[t=i|j,sp=2,sn=1,sg=f,+suf];[t=i|j,op=1|2|3,+suf]
suf -> suf           [^N;/;+;-]
start -> nosuf   []		[t=i|j,sp=1,op=0,-suf];[t=i|j,sp=2,sn=1,sg=m,op=0,-suf];[t=i|j,sp=3,sn=1,op=0,-suf]
nosuf -> nosuf   [^N;/;+;-]

start ->
suf ->
nosuf ->