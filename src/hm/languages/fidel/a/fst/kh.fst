-> start

start -> start 	[*;*v;-;/]
start -> stem	[<]

stem -> V		[*v]
stem -> C		[*]
V -> C			[*;/]
C -> V			[*v]
C -> C			[*;/]
V -> V			[*v]

V -> V+			[>]
V+ -> end		[ህ:ክ;ሁ:ኩ;-;አ;ኣ;ኦ;ኡ;ኤ;ኢ;ሽ;ን]
C -> end		[>]

# ሰ/ረቅኩ -> ሰ/ረ/ኩ
V -> kgq		[/:ክ;/:ቅ;/:ግ]
C -> kgq		[/:ክ;/:ቅ;/:ግ]
kgq -> kgq+		[>]
kgq+ -> end		[ክ;ኩ]

end -> end		[*v;*;-;/]

end ->

