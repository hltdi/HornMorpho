-> start

#start -> KQ0	[t=i];[t=j,sp=1|3];[t=j,sp=2,v=p|a];[t=p,v=p|a];[t=p,v=0,
#start -> X0		[t=c];[t=j,sp=2,v=0]

start -> R1V	[*v]
start -> R1C	[*]

R1C -> gem		[/]
R1V -> gem		[/]

# C2 follows * and is not geminated
# c=E: spirantize
# c=A, v=0,t=j: don't spirantize
# c=A, v=a,t=i: don't spirantize
gem -> R2V	 	[^N]

R1C -> R1C_E	[]				[c=E]
R1C -> R1C_X	[]				[c=A|G|H|I|J]

R1C_X -> R2V	[*v]
R1C_E -> R2V	[^Qv;{kV2KV}]

R1C_X -> R2C	[*]
R1C_E -> R2C	[^Q;{k2K}]

R1V -> R2V		[^Qv;{kV2KV}]
R1V -> R2C		[^Q;{k2K}]

# R3 follows *
# c=E, v=0, don't spirantize
# c=A, v=0, following geminated C2, spirantize; otherwise don't
# c=B, spirantize (following geminated C2)
# c=C, spirantize
R2V -> R3V		[^Qv;{kV2KV}]
R2V -> R3C		[^Q;{k2K}]

R2C -> R2C_C	[]				[c=C]
R2C -> R2C_X	[]				[c=A|E]

R2C_X  -> R3V	[*v]
R2C_C  -> R3V	[^Qv;{kV2KV}]

R2C_X  -> R3C	[*]
R2C_C ->  R3C	[^Q;{k2K}]

# R4 follows 
R3V -> R4V		[^Qv;{kV2KV}]	[c=E|F|G|H|I|J];[a=i]
R3V -> R4C		[^Q;{k2K}]		[c=E|F|G|H|I|J];[a=i]

R3C -> R3C_E	[]				[c=E|F];[c=A|B|C,a=i]
R3C -> R3C_X	[]				[c=G|H|I|J]

R3C_X -> R4V	[*v]
R3C_E -> R4V	[^Qv;{kV2KV}]

R3C_X -> R4C	[*]
R3C_E -> R4C	[^Q;{k2K}]

R4C -> R5		[^Q;{k2K}]		[c=G|H];[a=i,c=E|F|I|J]
R4V -> R5		[^Q;{k2K}]		[c=G|H];[a=i,c=E|F|I|J]

R2V ->
R2C ->
R3V ->
R3C ->
R4V ->
R4C ->
R5 ->