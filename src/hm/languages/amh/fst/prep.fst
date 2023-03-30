-> start

start -> distrib   <le:>     [pp=le,+rel,+sub,-ye]
start -> distrib   <be:>     [pp=be,+rel,+sub,-ye]
start -> distrib   <ke:>     [pp=ke,+rel,+sub,-ye]
start -> distrib   <wede:>   [pp=wede,+rel,+sub,-ye]

# for verbs, have the distributive prefix only following prepositions,
# which is probably the only case
distrib -> end     [:]              [-dis]
distrib -> end     <y_e1:>     [+dis]

# These are not really relative and not really prepositions.
# 1 means possible e'a
start -> end   <'nde1:>  [pp=Inde,+rel,+sub,-ye]
start -> end   <sle1:>   [pp=sIle,+rel,+sub,-ye]
start -> end   <'ske1:>  [pp=Iske,+rel,+sub,-ye]
start -> end   <'y_e1:>  [pp=Iyye,+rel,+sub,tm=prf,-ye]

end ->
