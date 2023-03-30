-> start

# % in the TB, these are most often ~mark but sometimes ~case
# at least ከ and በ can also function as SCONJs
start -> distrib   <le:le(@adp,*ለ,~mark)->     [pp=le,+rel,+sub,-ye]
start -> distrib   <be:be(@adp,*በ,~mark)->     [pp=be,+rel,+sub,-ye]
start -> distrib   <ke:ke(@adp,*ከ,~mark)->     [pp=ke,+rel,+sub,-ye]
start -> distrib   <wede:wede(@adp,*ወደ,~mark)->   [pp=wede,+rel,+sub,-ye]

# for verbs, have the distributive prefix only following prepositions,
# which is probably the only case
distrib -> end     [:]              [-dis]
# % Not handled consistently in the TB
distrib -> end     <y_e1:'y_e(@det,$numtype=dist,*እየ,~det)->     [+dis]

# These are not really relative and not really prepositions.
# 1 means possible e'a
# % in the TB, these are ~mark, not sure this is right
start -> end   <'nde1:'nde(@sconj,*እንደ,~mark)->  [pp=Inde,+rel,+sub,-ye]
start -> end   <sle1:sle(@sconj,*ስለ,~mark)->   [pp=sIle,+rel,+sub,-ye]
start -> end   <'ske1:'ske(@sconj,*እስከ,~mark)->  [pp=Iske,+rel,+sub,-ye]
# % እየ has 3 different annotations in the TB, as ADP, SCONJ, and AUX; SCONJ seems right
start -> end   <'y_e1:'y_e(@sconj,*እየ,~mark)->  [pp=Iyye,+rel,+sub,tm=prf,-ye]

end ->
