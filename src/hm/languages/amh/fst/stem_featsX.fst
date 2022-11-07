### Generate stem features

-> start

# Imperfective, perfective, gerundive, jussive-imperative
start -> voice    <:($aspect=imp>   [tm=imf]
start -> voice    <:($aspect=perf>     [tm=prf]
start -> voice    <:($verbform=conv>     [tm=ger]
start -> voice    <:($mood=jus> [tm=j_i]

# Morphological voice
voice -> end           [:)]   [as=smp,vc=smp]
voice -> end       <:,voice=pass)>   [as=smp,vc=ps]
voice -> end        <:,voice=trans)>   [as=smp,vc=tr]
voice -> end       <:,voice=cau)>    [as=smp,vc=cs]
voice -> end      <:,voice=rcp)>   [as=rc,vc=ps]
# this should be trans *and* rcp
voice -> end       <:,voice=trans)>   [as=rc,vc=tr]
# this should be aspect=iter *but* aspect already has a value
voice -> end           [:)]    [as=it,vc=smp]
# the same as te_a; could also be aspect=iter
voice -> end     <:,voice=rcp)>   [as=it,vc=ps]
# this should be trans *and* rcp (or iter)
voice -> end       <:,voice=trans)>   [as=it,vc=tr]
# this should be cau *and* rcp (or iter)
voice -> end       <:,voice=cau)>   [as=it,vc=cs]

## Use the following for syntactic/semantic voice

#voice -> 0           [:]   [as=smp,vc=smp]
#voice -> te_       <:,ውልድ=te_>   [as=smp,vc=ps]
#voice -> a_         <:,ውልድ=a_>   [as=smp,vc=tr]
#voice -> as_       <:,ውልድ=as_>    [as=smp,vc=cs]
#voice -> te_a     <:,ውልድ=te_a>   [as=rc,vc=ps]
#voice -> a_a       <:,ውልድ=a_a>   [as=rc,vc=tr]
#voice -> R           <:,ውልድ=R>     [as=it,vc=smp]
#voice -> te_R     <:,ውልድ=te_R>   [as=it,vc=ps]
#voice -> a_R       <:,ውልድ=a_R>   [as=it,vc=tr]
#voice -> as_R       <:,ውልድ=as_R>   [as=it,vc=cs]

#0 -> end                <:)>                                [bs=0]
#te_ -> end            <:)>                               [bs=te_]
#te_ -> end            <:,voice=pass)>         [bs=0];[bs=a_]
#a_  -> end             <:)>                                [bs=a_]
#a_  -> end             <:,voice=trans)>      [bs=0];[bs=te_]
#as_ -> end           <:)>                                 [bs=as_]
#as_ -> end           <:,voice=cau)>          [bs=0];[bs=te_];[bs=a_]
#te_a -> end         <:)>                                 [bs=te_a]
#te_a -> end          <:,voice=rcp)>             [bs=0]
#a_a -> end            <:,voice=trans)>        [bs=te_a]
#a_a -> end            <:,voice=rcp,voice=trans)>   [bs=0]
## Is this always iterative?
#R -> end                <:,aspect=iter)>         [bs=0]
#te_R -> end          <:)>                                 [bs=te_R]
#te_R -> end          <:,voice=rcp)>             [bs=0];[bs=te_];[bs=a_];[bs=te_a]
## What about causative iterative for this case?
#a_R -> end            <:,voice=trans)>          [bs=te_R]
#a_R -> end            <:,voice=rcp,voice=cau)>   [bs=0];[bs=te_];[bs=a_];[bs=te_a]
## For now treat this as identical to a_R?
#as_R -> end         <:,voice=caus)>             [bs=te_R]
#as_R -> end         <:,voice=rcp,voice=cau)>    [bs=0];[bs=te_];[bs=a_];[bs=te_a]

end ->