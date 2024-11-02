-> first

# a word can start with a series of border characters followed by any letter.
first -> start	[*v;*]
first -> first	[:-;:<]
first -> CV		[]

start -> start   [*v;*;/]
start -> CV		[]

CV -> .a        	[{I2a};{e2a};*a]
# :እ for የም-እ<ኣ-ደርግ>
.a -> .a		[:-;:<;:>;:እ]
.a -> start		[:ኣ]
# ፈለግ>-አ-ኣት
.a -> a.e		[:አ]
a.e -> a.e		[:-]
a.e -> start	[:ኣ]
# ፈልግ>-ኣ--ኣለች
.a -> a.a		[:ኣ]
a.a -> a.a		[:-]
a.a -> start	[:ኣ]

# Final adverbial ኣ
CV -> .A		[{I2a};{e2a}]
.A -> .A		[:-;:>]
.A -> A.		[:=ኣ]
.A -> .Ae		[:አ]
.Ae -> .Ae		[:-]
.Ae -> A.		[:=ኣ]

CV -> .e		[{I2e};*a;*e]
.e -> .e		[:-;:>]
.e -> start		[:አ]

CV -> .-u		[{I2u};{a2u};{e2u}]
.-u -> -.u		[:-;:>]
-.u -> -.u		[:-;:>]
-.u -> start	[:ኡ]
-.u -> ou		[:ኡ]

CV -> ou		[*u]

CV -> .-o		[{I2o}]
.-o -> -.o		[:-;:>]
-.o -> -.o		[:-;:>]
-.o -> start	[:ኦ]
-.o -> ou		[:ኦ]
# the usual rule ሰምቶኣል -> ሰምቶዋል -> ሰምቷል
ou -> oua.-		[ዋ:]
oua.- -> oua-.	[:-]
oua-. -> oua-.	[:-]
oua-. -> start	[:ኣ;:=ኣ]
# the other possibility; no change
ou -> oua.		[:-]
oua. -> oua.	[:-]
oua. -> start	[ኣ]

# 2sf t=i|j suffix
# * - ኢ -> *i
CV -> .-i		[{^I2i};{^a2i}]
.-i -> -.i		[:>]
-.i -> start	[:ኢ]
-.i -> i		[:ኢ]
CV -> /-E		[/:]
/-E -> .-E        	[{^I2E}]
.-E -> -.E		[:>]
-.E -> start	[:ኤ]
-.E -> i		[:ኤ]

# *ኢ|*ኤ - ኣ -> ያ
i -> ya.-		[ያ:]
ya.- -> ya-.	[:-]
ya-.-> ya-.		[:-]
ya-. -> start	[:ኣ;:=ኣ]

# delete -, <, and > when followed by a consonant
start -> -.X	[:-;:<;:>]
-.X -> -.X		[:-;:<;:>]
# delete እ following other segments
-.X -> start	[**;**v;/;:እ]
-.X -> CV		[]

start ->
-.X ->
A. ->