-> start

start -> 1X		[^^X;^^y]		[tmp=[1=X],1=X]
# 1=L
#start -> 1X		[ሀ;ህ;ሃ]			[tmp=[1=L],1=ህ]
#start -> 1X		[አ;እ;ኣ]			[tmp=[1=L],1=እ]
#start -> 1X		[ዐ;ዕ;ዓ]			[tmp=[1=L],1=ዕ]
#start -> 1X		[ሐ;ሕ;ሓ]			[tmp=[1=L],1=ሕ]
start -> 1X		[^^L]			[tmp=[1=L],1=L]
# 1=ው
start -> 1X		[^^w]			[tmp=[1=ው],1=ው]
start -> 2X		[^^X]			[tmp=[1=ው,2=X],t=j,1=ው,a=0|a,2=X]

# 1=ይ, t=j
start -> 1X		[ኢ]				[tmp=[1=ይ],v=0,t=j,-imp]

# 2=ይ
start -> 2X		[*E;*;*i]		[tmp=[1=X,2=ይ],2=ይ,-dup23,-gem2,a=0|a]

# 2=ው
start -> 2X		[*o;*u;*]		[tmp=[1=X,2=ው],2=ው,-dup23,-gem2,a=0|a]

1X -> 1X/		[/]				[+gem2]

1X -> 2X 		[^^X]			[tmp=[2=X],-gem2,a=0|a,2=X]
1X -> 2X		[^^y]			[tmp=[2=ይ],2=ይ,-gem2,a=0|a]
1X -> 2X		[^^w]			[tmp=[2=ው],2=ው,-gem2,a=0|a]
1X/ -> 2X		[^^X]			[tmp=[2=X],a=0|a,2=X]

1X -> 2X		[^^L]			[tmp=[2=L],2=L,-gem2,-dup23]

# C2=C3; nothing to prevent ungeminated sequences, so orthographic አዝዝ will be ambiguous
1X/ -> 2Xdup	[^^X]			[tmp=[2=X,3=X],+dup23,a=0|a]

2X -> 3X		[^^X]			[tmp=[3=X],-dup23,3=X]
2X -> 3X		[^^L]			[tmp=[3=L],-dup23,3=L]
# 3=ው, 23fp, t=i|j
2X -> 3w		[ይ]				[tmp=[3=ው],t=i|j,sp=2|3,sn=2,sg=f,3=ው]

# only two explicit consonants
# 3=ው
2X -> 3w		[]				[tmp=[3=ው],-dup23,3=ው]

3X -> 4X		[^^X]			[tmp=[4=X],a=0|a,4=X]

3X -> 4w		[]				[tmp=[4=ው],4=ው]

4X -> 5X		[^^X]			[tmp=[5=X],a=0|a,5=X]

# reduplicated; nothing to prevent sequences of CaC from being class F stems

1X -> mR		[ማ]				[a=i,2=ም,tmp=[2=X]]
mR -> 2X		[ም;መ]
1X -> bR		[ባ]				[a=i,2=ብ,tmp=[2=X]]
bR -> 2X		[ብ;በ]

1X -> nR		[ና]				[a=i,2=ን,tmp=[2=X]]
nR -> 2X		[ን;ነ]
1X -> tR		[ታ]				[a=i,2=ት,tmp=[2=X]]
tR -> 2X		[ት;ተ]
1X -> dR		[ዳ]				[a=i,2=ድ,tmp=[2=X]]
dR -> 2X		[ድ;ደ]
1X -> TR		[ጣ]				[a=i,2=ጥ,tmp=[2=X]]
TR -> 2X		[ጥ;ጠ]
1X -> sR		[ሳ]				[a=i,2=ስ,tmp=[2=X]]
sR -> 2X		[ስ;ሰ]
1X -> zR		[ዛ]				[a=i,2=ዝ,tmp=[2=X]]
zR -> 2X		[ዝ;ዘ]
1X -> SR		[ጻ]				[a=i,2=ጽ,tmp=[2=X]]
SR -> 2X		[ጽ;ጸ]

1X -> kR		[ካ]				[a=i,2=ክ,tmp=[2=X]]
kR -> 2X		[ክ;ከ]
1X -> gR		[ጋ]				[a=i,2=ግ,tmp=[2=X]]
gR -> 2X		[ግ;ገ]
1X -> qR		[ቃ]				[a=i,2=ቅ,tmp=[2=X]]
qR -> 2X		[ቅ;ቀ]

1X -> 'R		[ኣ]				[a=i,2=እ,tmp=[2=L]]
'R -> 2X		[እ;አ]
1X -> `R		[ዓ]				[a=i,2=ዕ,tmp=[2=L]]
`R -> 2X		[ዕ;ዐ]
1X -> hR		[ሃ]				[a=i,2=ህ,tmp=[2=L]]
hR -> 2X		[ህ;ሀ]
1X -> HR		[ሓ]				[a=i,2=ሕ,tmp=[2=L]]
HR -> 2X		[ሕ;ሐ]

2Xdup ->
3X ->
3w ->
4w ->

4X ->
5X ->