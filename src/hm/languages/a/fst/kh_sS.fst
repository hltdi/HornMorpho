-> start

start -> start 	[*;*v;-;/]
start -> stem	[<]

# optionally ..lr.. -> /r (አ/ረሳም)
start -> l.r	[/:ል]
# could be a boundary here
l.r -> l.r		[-]
l.r -> lr.		[<]
lr. -> V		[ረ;ራ;ሮ;ሯ]

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

V -> end		[>]

# optional h->k following consonant-final root
C -> C+			[>]
C+ -> end		[ክ:ህ;ኩ:ሁ]
C -> end		[>]

# optional ሰ/ረቅኩ -> ሰ/ረ/ኩ
V -> kgq		[/:ክ;/:ቅ;/:ግ]
C -> kgq		[/:ክ;/:ቅ;/:ግ]
kgq -> kgq+		[>]
kgq+ -> end		[ክ;ኩ]

end -> end		[*v;*;-;/]

end ->
