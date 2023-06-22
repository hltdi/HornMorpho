-> start

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
R2C -> R3V		[*v]
R2C -> R3C		[*]

# R4 follows 
R3V -> R4		[^N]	[c=E|F|G|H|I|J];[a=i]
R3C -> R4		[^N]	[c=E|F|G|H|I|J];[a=i]

R4 -> R5		[^N]	[c=G|H];[a=i,c=E|F]

R2V ->
R2C ->
R3V ->
R3C ->
R4 ->
R5 ->