### Generate stem features

-> start

# Imperfective, perfective, gerundive, jussive-imperative
start -> tam    <:($aspect=imp>   [tm=imf]
start -> tam    <:($aspect=perf>     [tm=prf]
start -> tam    <:($verbform=conv>     [tm=ger]
start -> tam    <:($mood=jus> [tm=j_i]

# Iterative, reciprocal
tam -> asp      [:]         [as=smp]
tam -> asp      <:,aspect=iter>    [as=it]
tam -> asp      <:,voice=rcp>   [as=rc]

# Passive, transitive, causative
asp -> end      <:)>        [vc=smp]
asp -> end      <:,voice=pas)>    [vc=ps]
asp -> end      <:,voice=trans)>  [vc=tr]
asp -> end      <:,voice=cau)>   [vc=cs]

end ->