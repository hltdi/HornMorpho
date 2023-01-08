-> start

start -> sb_pre []  [pos=v]

#$ conj_prep_pre
#  ዘ   [cpp=z]
#  -- [cpp=None]

#$ neg
## These could be preceded by conjunctions
# ኢ       [+neg]
#  --   [-neg]

sb_pre -> stem  <ይ:ይ->  [tm=i|j,sp=3,sn=2,-neg];[tm=i|j,sp=3,sn=1,sg=m,-neg]
sb_pre -> stem  <ት:ት->   [tm=i,sp=2];[tm=i|j,sp=3,sn=1,sg=f];[tm=j,sp=2,+neg]
sb_pre -> stem  <እ:እ->   [tm=i|j,sp=1,sn=1]
sb_pre -> stem  <ን:ን->   [tm=i|j,sp=1,sn=2]
sb_pre -> stem  []    [tm=p|g];[tm=j,sp=2,-neg]

#$ voice
#  ተ   [tm=p,vc=ps,cpp=None];[tm=j,sp=2,vc=ps]
#  ት    [tm=i,vc=ps];[tm=j,sp=1|3,vc=ps];[tm=p,vc=ps,cpp=የ]
#  =ኣ  [vc=a]
#  =ኣት [vc=at]
#  --  [vc=0]

stem -> sb_suf   >>v_stemX<<

sb_suf -> ob_suf  <ኩ:-ኩ>   [tm=p,sp=1,sn=1]
sb_suf -> ob_suf  <ከ:-ከ>    [tm=p,sp=2,sn=1,sg=m]
sb_suf -> ob_suf  <ኪ:-ኪ>    [tm=p,sp=2,sn=1,sg=f]
sb_suf -> ob_suf  <=ኢ:-ኢ>  [tm=i|j,sp=2,sn=1,sg=f]
sb_suf -> ob_suf  <=አ:-አ>   [tm=p,sp=3,sn=1,sg=m]
sb_suf -> ob_suf  <=አት:-አት>   [tm=p,sp=3,sn=1,sg=f]
sb_suf -> ob_suf  <ነ:-ነ>     [tm=p,sp=1,sn=2]
sb_suf -> ob_suf  <ክሙ:-ክሙ>  [tm=p,sp=2,sn=2,sg=m]
sb_suf -> ob_suf  <ክን:-ክን>   [tm=p,sp=2,sn=2,sg=f]
sb_suf -> ob_suf  <=ኡ:-ኡ>    [sp=3,sn=2,sg=m];[tm=j|i,sp=2,sn=2,sg=m]
sb_suf -> ob_suf  <=ኣ:-ኣ>   [sp=3,sn=2,sg=f];[tm=j|i,sp=2,sn=2,sg=f]
sb_suf -> ob_suf  []   [tm=i|j,sp=2,sn=1,sg=m];[tm=i|j,sp=1];[tm=i|j,sp=3,sn=1]

ob_suf -> end   []  [op=0]

#$ end
#  --   [tm=j];[tm=i,-prog];[tm=p,-cvb]

end ->
