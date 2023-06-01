-> start

## A: strong
start -> sbr1 [s]     [c=A,1=ስ,2=ብ,3=ር,j=t,p=t]
#sbr1 -> sbr1  [ባ]
sbr1 -> sbr2   [b] 
sbr2 -> end     [r] 

start -> lbs1 [l]     [c=A,1=ል,2=ብ,3=ስ,j=i,p=i]
#lbs1 -> lbs1  [ባ]
lbs1 -> lbs2   [b] 
lbs2 -> end     [s]

start -> qrb1 [q]     [c=A,1=ቅ,2=ር,3=ብ,j=i]
qrb1 -> qrb2   [r] 
qrb2 -> end      [b]

## A: weak

# 1=w
start -> wrd1  [ወ;]	[c=A,1=ው,2=ር,3=ድ,j=i,p=t]
wrd1 -> wrd2     [r]
wrd2 -> end       [d]

# 2=w
start -> mwt1  [m]  [c=A,1=ም,2=ው,3=ት]
mwt1 -> mwt2     [;ው;ዊ;ወ]
mwt2 -> end       [t]

## B
start -> qds1   [q]   [c=B,1=ቅ,2=ድ,3=ስ]
#qds1 -> qds1     [ዳ]
qds1 -> qds2      [d]
qds2 -> end        [s]

## C
start -> brk1	  [b]	[c=C,1=ብ,2=ር,3=ክ]
brk1 -> brk2	  [r]
brk2 -> end		[k]

## E
start -> fdfd1	   [f]	[c=E,1=ፍ,2=ድ,3=ፍ,4=ድ]
fdfd1 -> fdfd2	   [d]
fdfd2 -> fdfd3	   [f]
fdfd3 -> end	   [d]

end ->