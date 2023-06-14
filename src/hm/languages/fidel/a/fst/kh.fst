-> start

start -> start 	[*;*v;-]
start -> stem	[<]

#start -> s.		[:ስ]
#s. -> s.+		[<]
#s.+ -> stem		[ሰ;ሳ;ሶ;ሱ;ዘ;ዛ;ዞ;ዝ;ዙ;ሸ;ሻ;ሾ;ሽ;ሹ;ዠ;ዣ;ዦ;ዡ;ዥ]

#start -> s		[ስ]
#s -> start		[*-ስ;*v;-]
#s -> s+			[<]
#s+ -> stem		[^S]

stem -> V		[*v]
stem -> C		[*]
V -> C			[*]
C -> V			[*v]
C -> C			[*]
V -> V			[*v]

V -> V+			[>]
V+ -> end		[ህ:ክ;ሁ:ኩ;-;አ;ኣ;ኦ;ኡ;ኤ;ኢ;ሽ;ን]
C -> end		[>]

end -> end		[*v;*;-]

end ->

