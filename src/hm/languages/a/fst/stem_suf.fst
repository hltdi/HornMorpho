-> start

start -> start    [X;V]

=a -> start       [:=ኣ]
=e -> start       [:=አ]
=o -> start       [:=ኦ]
=u -> start       [:=ኡ]

start -> =a       [ባ:ብ;ራ:ር;ሳ:ስ]
start -> =e       [በ:ብ;ረ:ር;ሰ:ስ]
start -> =u       [ቡ:ብ;ሩ:ር;ሱ:ስ]

start -> C        [ህ;ል;ሕ;ም;ር;ስ;ሽ;ቅ;ብ;ቭ;ት;ች;ን;ኝ;ክ;ኽ;ው;ዝ;ዥ;ይ;ድ;ጅ;ግ;ጥ;ጭ;ጵ;ጽ;ፍ;ፕ;ኵ;ዅ;ኍ;ቍ;ጕ;እ;ዕ]
C -> start        [X]
C -> C            [ህ;ል;ሕ;ም;ር;ስ;ሽ;ቅ;ብ;ቭ;ት;ች;ን;ኝ;ክ;ኽ;ው;ዝ;ዥ;ይ;ድ;ጅ;ግ;ጥ;ጭ;ጵ;ጽ;ፍ;ፕ;ኵ;ዅ;ኍ;ቍ;ጕ;እ;ዕ]
C -> =a           [ባ:ብ;ራ:ር;ሳ:ስ]
C -> =e           [በ:ብ;ረ:ር;ሰ:ስ]
C -> =u           [ቡ:ብ;ሩ:ር;ሱ:ስ]

#start -> b=       [:ብ=]
#b= -> start       [በ:=አ;ቡ:=ኡ;ቢ:=ኢ;ባ:=ኣ;ቤ:=ኤ;ቦ:=ኦ]
#b= -> b=b         [ብ:]
#b=b -> start      [X;C]

#start -> r=       [:ር=]
#r= -> start       [ረ:=አ;ሩ:=ኡ;ሪ:=ኢ;ራ:=ኣ;ሬ:=ኤ;ሮ:=ኦ]
#r= -> r=r         [ር:]
#r=r -> start      [X;C]

#start -> s=       [:ስ=]
#s= -> start       [ሰ:=አ;ሱ:=ኡ;ሲ:=ኢ;ሳ:=ኣ;ሴ:=ኤ;ሶ:=ኦ]
#s= -> s=s         [ስ:]
#s=s -> start      [X;C]

start ->
C ->
#b=b ->
#r=r ->
#s=s ->