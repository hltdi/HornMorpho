-> start

start -> mid    [^X;አ:=ኣ]

mid -> mid	     [^X]

=a -> mid       [:=ኣ]
=e -> mid       [:=አ]
=o -> mid       [:=ኦ]
=u -> mid       [:=ኡ]
=a -> ^e     	[:=ኣ]
=e -> ^e	[:=አ]
=o -> ^e	[:=ኦ]
=u -> ^e       	[:=ኡ]

# *=e=a -> *a
=a -> =e.a	[:=አ]
=e.a -> mid	[:=ኣ]

mid -> =e       [{I2e};*a]
mid -> =a       [{I2a};*a;{YiE2a};{u2Wa}]
mid -> =o       [{I2o}]
mid -> =u       [{I2u};{a2u}]
# *=u=a	-> *Wa; *=o=a -> *Wa
mid -> =uo.a	[{I2Wa}]
=uo.a -> =a	[:=ኡ;:=ኦ]

mid -> ^e       [{~YI2e};*i;^Y;*u;*o;*a;*e]
^e -> mid       [:^አ]

mid -> iE	[~Yi;~YE]
iE -> =a	[ያ:]

mid ->

