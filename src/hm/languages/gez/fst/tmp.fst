-> start

### A

## strong

start -> A0   []           [c=A,a=0]
#start -> AB0I []          [c=A|B,a=i]

A0 -> A1         [e/w;y]    [t=p,-gem,v=0|p];[t=i,+gem];[t=c,v=0,-gem];[t=j,v=p,-gem]
A0 -> A1          [I/w]    [t=j,v=0|a,-gem];[t=p,-gem,v=a];[t=c,v=a,-gem]
# variation in t=p; e with "transitive" and "intransitive" 1,2p , I with "intransitive" 3p
A1 -> x2          [e/w]    [t=p,p=t,v=0];[t=p,v=a|p];[t=p,p=i,-vsuf];[t=j,j=i,v=0];[t=i|j,v=p]
A1 -> x2          [I/w]    [t=p,v=p];[t=p,p=i,+vsuf];[t=i,v=0|a];[t=j,j=t,v=0];[t=j,v=a]
A1 -> x2           [i/w]    [t=c]
# final laryngeal
A1 -> L2           [I/w]    [t=i,v=a|0];[t=p|j,+vsuf];[t=i,v=p,+vsuf]
A1 -> L2           [a/w]     [t=p|j,-vsuf];[t=i,v=p,-vsuf]
A1 -> L2            [i/w]    [t=c]

## weak

# 1=w
A0 -> A1          [ወ]    [t=p,-gem,v=0|p];[t=i,+gem];[t=c,v=0,-gem];[t=j,v=p,-gem]
A0 -> A1           [ው]   [t=j,v=0|a,-gem,j=t];[t=p,-gem,v=a];[t=c,v=a,-gem];[t=j,v=a,j=i,-gem]
A0 -> A1	   []      [t=j,v=0,-gem,j=i]

# 2=w (3=L is special: ሞአ)
# o for jussive only for certain roots, e.g., ሮጸ; I also possible in jussive for some verbs
A0 -> x2	 [o]      [t=p,v=0|a,2=ው]   # ;[t=j,v=0|a,2=ው]
A0 -> x2          [u]     [t=j,v=0|a,2=ው]
A0 -> A1w         [e/w]	  [t=i|c,2=ው];[t=p,v=p,2=ው];[t=j,v=p,2=ው]
A1w -> x2         [ወ]       [t=i|j,v=p]
A1w -> x2         [ው]      [t=i|j|p,v=0|a]
A1w -> x2         [ዊ]       [t=c]

### B

## strong

start -> B0   []          [c=B,+gem,a=0]

B0 -> B1          [e]    [t=p|j|c]
B0 -> B1           [E]    [t=i]

B1 -> x2          [I]	    [t=p|i|j,v=0|a]
B1 -> x2          [e]        [t=p|i|j,v=p]
B1 -> x2          [i]	    [t=c]


### C

start -> C0	[]	[c=C,a=0]

C0 -> C1 	[a]

C1 -> x2	[e]	[t=p,+gem];[t=i,v=p,+gem];[t=j,v=p,-gem]
C1 -> x2	[I]	[t=i,v=0|a,+gem];[t=j,v=0|a,-gem]
C1 -> x2	[i]	[t=c,-gem]


### E

start -> E0	[]	[c=E]

E0 -> E1 	[e/w]

E1 -> E2	[I/w]	[t=p|j|c,-gem]
E1 -> E2	[e/w]	[t=i,+gem]

E2 -> x2	[e/w]	[t=p];[t=i|j,v=p]
E2 -> x2	[I/w]	[t=i|j,v=0|a]
E2 -> x2	[i/w]	[t=c]

### strong stem final character
x2 -> end        [I/L]
### stem final laryngeal
L2 -> end         [LI]
       
end ->