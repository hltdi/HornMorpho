-> start

start -> bound1   [y:]    [sb=[-p1,-p2,+plr],tm=imf];[sb=[-p1,-p2,-fem,-plr],tm=imf]
start -> bound1   <ye:>   [sb=[-p1,-p2],tm=j_i]
start -> bound1   [t:]    [sb=[-p1,-p2,+fem,-plr],tm=imf];[sb=[-p1,+p2],tm=imf]
start -> bound1   [:]     [tm=prf]

bound1 -> stem    [=:]

stem -> bound2  >>v_stem<<

bound2 -> suff    [=:]

suff -> end       <ema:>  [sb=[-p1,+plr,+fem]]
suff -> end       [e:]    [sb=[-p1,-p2,-fem,-plr],tm=prf]
suff -> end       [o:]    [sb=[-p1,-p2,+plr,-fem]]
# wrong; has to also accommodate 3sf imf
suff -> end       [:]     [sb=[-plr]]

end ->
  