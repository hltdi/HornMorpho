### Generate infinitive features

-> start

## Syntactic/semantic voice

start -> 0           [:]   [as=smp,vc=smp]
start -> te_       <:,$ውልድ=te_>   [as=smp,vc=ps]
start -> a_         <:,$ውልድ=a_>   [as=smp,vc=tr]
start -> as_       <:,$ውልድ=as_>    [as=smp,vc=cs]
start -> te_a     <:,$ውልድ=te_a>   [as=rc,vc=ps]
start -> a_a       <:,$ውልድ=a_a>   [as=rc,vc=tr]
start -> R           <:,$ውልድ=R>     [as=it,vc=smp]
start -> te_R     <:,$ውልድ=te_R>   [as=it,vc=ps]
start -> a_R       <:,$ውልድ=a_R>   [as=it,vc=tr]
start -> as_R       <:,$ውልድ=as_R>   [as=it,vc=cs]

0 -> end                <:)>                                [bs=0]
te_ -> end            <:)>                               [bs=te_]
te_ -> end            <:,voice=pass)>         [bs=0];[bs=a_]
a_  -> end             <:)>                                [bs=a_]
a_  -> end             <:,voice=trans)>      [bs=0];[bs=te_]
as_ -> end           <:)>                                 [bs=as_]
as_ -> end           <:,voice=cau)>          [bs=0];[bs=te_];[bs=a_]
te_a -> end         <:)>                                 [bs=te_a]
te_a -> end          <:,voice=rcp)>             [bs=0]
a_a -> end            <:,voice=trans)>        [bs=te_a]
a_a -> end            <:,voice=rcp,voice=trans)>   [bs=0]
# Is this always iterative?
R -> end                <:,aspect=iter)>         [bs=0]
te_R -> end          <:)>                                 [bs=te_R]
te_R -> end          <:,voice=rcp)>             [bs=0];[bs=te_];[bs=a_];[bs=te_a]
# What about causative iterative for this case?
a_R -> end            <:,voice=trans)>          [bs=te_R]
a_R -> end            <:,voice=rcp,voice=cau)>   [bs=0];[bs=te_];[bs=a_];[bs=te_a]
# For now treat this as identical to a_R?
as_R -> end         <:,voice=cau)>             [bs=te_R]
as_R -> end         <:,voice=rcp,voice=cau)>    [bs=0];[bs=te_];[bs=a_];[bs=te_a]

end ->