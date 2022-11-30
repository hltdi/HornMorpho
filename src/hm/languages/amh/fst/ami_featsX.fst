### Constraint instrument, manner, agent features

-> start

## Syntactic/semantic voice

start -> 0           [:]   [as=smp,vc=smp]
start -> te_       [:]   [as=smp,vc=ps]
start -> a_         [:]   [as=smp,vc=tr]
start -> as_       [:]   [as=smp,vc=cs]
start -> te_a     [:]   [as=rc,vc=ps]
start -> a_a       [:]   [as=rc,vc=tr]
start -> R           [:]    [as=it,vc=smp]
start -> te_R     [:]   [as=it,vc=ps]
start -> a_R       [:]   [as=it,vc=tr]
start -> as_R      [:]   [as=it,vc=cs]

0 -> end                [:]                                [bs=0]
te_ -> end            [:]                              [bs=te_]
te_ -> end            [:]            [bs=0];[bs=a_]
a_  -> end             [:]                                [bs=a_]
a_  -> end             [:]      [bs=0];[bs=te_]
as_ -> end           [:]                                [bs=as_]
as_ -> end           [:]          [bs=0];[bs=te_];[bs=a_]
te_a -> end         [:]                                 [bs=te_a]
te_a -> end          [:]             [bs=0]
a_a -> end            [:]        [bs=te_a]
a_a -> end            [:]   [bs=0]
# Is this always iterative?
R -> end                [:]         [bs=0]
te_R -> end          [:]                                [bs=te_R]
te_R -> end          [:]             [bs=0];[bs=te_];[bs=a_];[bs=te_a]
# What about causative iterative for this case?
a_R -> end            [:]          [bs=te_R]
a_R -> end            [:]   [bs=0];[bs=te_];[bs=a_];[bs=te_a]
# For now treat this as identical to a_R?
as_R -> end         [:]             [bs=te_R]
as_R -> end         [:]    [bs=0];[bs=te_];[bs=a_];[bs=te_a]

end ->