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
as -> C			[*;/]
# includes አስተ-
as -> V			[*v]
as -> as-		[-]
# optionally allow the full prefix before ሽ,ዝ,ዥ,ጽ,ፅ
as- -> V		[^S;ሸ;ሻ;ዘ;ዛ;ዠ;ዣ;ጸ;ጻ;ፀ;ፃ]
# applies
stem -> a.sS	[ኣ]
a.sS -> as.S	[/:ስ]
as.S -> as.S-	[-]
as.S- -> V		[ሰ;ዘ;ሸ;ዠ;ጸ;ፀ;ሳ;ዛ;ሻ;ዣ;ጻ;ፃ]

V -> end		[>]

# optional h->k following consonant-final root
C -> C+			[>]
C+ -> end		[ክ:ህ;ኩ:ሁ]
C -> end		[>]

# optional ሰ/ረቅኩ -> ሰ/ረ/ኩ
V -> kgq		[/:ክ;/:ቅ;/:ግ]
C -> kgq		[/:ክ;/:ቅ;/:ግ]
kgq -> kgq+		[>]
kgq+ -> end		[ክ;ኩ;ኩ:ሁ;ክ:ህ]

end -> end		[*v;*;-;/;=ኣ]

end ->
