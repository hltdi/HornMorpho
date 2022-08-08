### Generate stem features

-> start

# Imperfective, perfective, gerundive, jussive-imperative
start -> tam    <:(imprf>   [tm=imf]
start -> tam    <:(prf>     [tm=prf]
start -> tam    <:(ger>     [tm=ger]
start -> tam    <:(jusimpv> [tm=j_i]

# Iterative, reciprocal
tam -> asp      [:]         [as=smp]
tam -> asp      <:,iter>    [as=it]
tam -> asp      <:,recip>   [as=rc]

# Passive, transitive, causative
asp -> end      <:)>        [vc=smp]
asp -> end      <:,pas)>    [vc=ps]
asp -> end      <:,trans)>  [vc=tr]
asp -> end      <:,caus)>   [vc=cs]

end ->