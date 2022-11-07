-> start

# % Case feature is  missing for most of these in the TB, could leave it out since most are ambiguous
start -> end   <I:'(@adp,$case=loc,*እ,~case)->        [prep=I,-acc]
# ambiguous between Dat and Ben, so leave out case
start -> end   <le:le(@adp,*ለ,~case)->      [prep=le,-acc]
# ambiguous between Ins and Loc, so leave out case
start -> end   <be:be(@adp,*በ,~case)->      [prep=be,-acc]
start -> end   <ke:ke(@adp,$case=loc,*ከ,~case)->      [prep=ke,-acc]
start -> end   <wede:wede(@adp,$case=loc,*ወደ,~case)->  [prep=wede,-acc]
start -> end   <'nde:'nde(@adp,*እንደ,~case)->  [prep=Inde,-acc]
start -> end   <sIle:sle(@adp,*ስለ,~case)->   [prep=sIle,-acc]
start -> end   <'ske:'ske(@adp,*እስከ,~case)->  [prep=Iske,-acc]

#start -> end   <I:'(@adp,$case=loc,*እ,~case)->        [prep=I,-acc]
#start -> end   <le:le(@adp,$case=dat,*ለ,~case)->      [prep=le,-acc]
#start -> end   <be:be(@adp,$case=ins,*በ,~case)->      [prep=be,-acc]
#start -> end   <ke:ke(@adp,$case=ela,*ከ,~case)->      [prep=ke,-acc]
#start -> end   <wede:wede(@adp,$case=lat,*ወደ,~case)->  [prep=wede,-acc]
#start -> end   <'nde:'nde(@adp,$case=equ,*እንደ,~case)->  [prep=Inde,-acc]
#start -> end   <sIle:sle(@adp,$case=cau,*ስለ,~case)->   [prep=sIle,-acc]
#start -> end   <'ske:'ske(@adp,$case=ter,*እስከ,~case)->  [prep=Iske,-acc]

end ->
