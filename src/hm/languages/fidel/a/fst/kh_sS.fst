-> start

start -> start 	[*;*v;-;/]
start -> stem	[<]

stem -> V		[*v-ኣ]
stem -> C		[*;/]
V -> C			[*;/;-]
C -> V			[*v]
C -> C			[*;/;-]
V -> V			[*v]

## handle አስ+sibilant gemination
# doesn't apply
stem -> a		[ኣ]
a -> C 			[*-ስ;/;-]
a -> V			[*v]
a -> as			[ስ]
# አስተ-
as -> V			[ተ]
as -> as-		[-]
as- -> V		[^S]
# applies
stem -> a.sS	[ኣ]
a.sS -> as.S	[/:ስ]
as.S -> as.S-	[-]
as.S- -> V		[ሰ;ዘ;ሸ;ዠ;ጸ;ሳ;ዛ;ሻ;ዣ;ጻ]

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

