-> start

start -> sb_pre []  [pos=v]

#$ conj_prep_pre
#  ዘ   [cpp=z]
#  -- [cpp=None]

#$ neg
## These could be preceded by conjunctions
# ኢ       [+neg]
#  --   [-neg]

sb_pre -> voice  <ይ:ይ->  [t=i|j,sp=3,sn=2,-neg];[t=i|j,sp=3,sn=1,sg=m,-neg]
sb_pre -> voice  <ት:ት->   [t=i,sp=2];[t=i|j,sp=3,sn=1,sg=f];[t=j,sp=2,+neg]
sb_pre -> voice  <እ:እ->   [t=i|j,sp=1,sn=1]
sb_pre -> voice  <ን:ን->   [t=i|j,sp=1,sn=2]
sb_pre -> voice  []    	 [t=p|g];[t=j,sp=2,-neg]

voice -> stem	 <ተ:ተ->	   [t=p,v=p];[t=j,sp=2,v=p];[t=c,v=p]
voice -> stem       <ት:ት->	   [t=i,v=p];[t=j,sp=1|3,v=p]
voice -> stem       <=ኣ:ኣ-> [v=a]
voice -> stem	  []	           [v=0]

stem -> sb_suf   >>v_stemX<<

# initial consonant suffixes
sb_suf -> ob_suf  <ኩ:-ኩ>   [t=p,sp=1,sn=1,-vsuf]
sb_suf -> ob_suf  <ከ:-ከ>    [t=p,sp=2,sn=1,sg=m,-vsuf]
sb_suf -> ob_suf  <ኪ:-ኪ>    [t=p,sp=2,sn=1,sg=f,-vsuf]
sb_suf -> ob_suf  <ነ:-ነ>     [t=p,sp=1,sn=2,-vsuf]
sb_suf -> ob_suf  <ክሙ:-ክሙ>  [t=p,sp=2,sn=2,sg=m,-vsuf]
sb_suf -> ob_suf  <ክን:-ክን>   [t=p,sp=2,sn=2,sg=f,-vsuf]
# initial vowel suffixes
sb_suf -> ob_suf  <=ኡ:-ኡ>    [sp=3,sn=2,sg=m,+vsuf];[t=j|i,sp=2,sn=2,sg=m,+vsuf]
sb_suf -> ob_suf  <=ኣ:-ኣ>   [sp=3,sn=2,sg=f,+vsuf];[t=j|i,sp=2,sn=2,sg=f,+vsuf]
sb_suf -> ob_suf  <=ኢ:-ኢ>  [t=i|j,sp=2,sn=1,sg=f,+vsuf]
sb_suf -> ob_suf  <=አ:-አ>   [t=p,sp=3,sn=1,sg=m,+vsuf]
sb_suf -> ob_suf  <=አት:-አት>   [t=p,sp=3,sn=1,sg=f,+vsuf]
# no suffixes
sb_suf -> ob_suf  []   [t=i|j,sp=2,sn=1,sg=m,-ssuf];[t=i|j,sp=1,-ssuf];[t=i|j,sp=3,sn=1,-ssuf]

ob_suf -> end   []  [op=0,t=p];[op=0,t=i|j,-ssuf,-vsuf];[op=0,t=i|j,+ssuf,+vsuf]

#$ end
#  --   [t=j];[t=i,-prog];[t=p,-cvb]

end ->
