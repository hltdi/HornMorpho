-> particle

particle -> particle    [^N]
particle -> particle/  [/]
particle/ -> particle  [^N]
# There can be more than one particle
particle/ -> particle   [/]
particle/ -> first		[/]
first -> start			[*v;*]
first -> first		  	[:-;:<]
first -> CV			[]

start -> start   [*v;*;/]
start -> CV		[]

CV -> .a        	[{I2a};{e2a};*a]
.a -> .a		[:-;:<;:>]
.a -> start		[:ኣ]
# ፈለግ>-አ-ኣት
.a -> a.e		[:አ]
a.e -> a.e		[:-]
a.e -> start	[:ኣ]
# ፈልግ>-ኣ--ኣለች
.a -> a.a		[:ኣ]
a.a -> a.a		[:-]
a.a -> start	[:ኣ]

CV -> .e		[{I2e};*a;*e]
.e -> .e		[:-;:<;:>]
.e -> start		[:አ]

CV -> .-u		[{I2u};{a2u};{e2u}]
.-u -> -.u		[:-;:<;:>]
-.u -> -.u		[:-;:<;:>]
-.u -> start	[:ኡ]
-.u -> ou		[:ኡ]

CV -> ou		[*u]

CV -> .-o		[{I2o}]
.-o -> -.o		[:-;:<;:>]
-.o -> -.o		[:-;:<;:>]
-.o -> start	[:ኦ]
-.o -> ou		[:ኦ]
ou -> oua.-		[ዋ:]
oua.- -> oua-.	[:-]
oua-. -> oua-.	[:-]
oua-. -> start	[:ኣ]

# 2sf t=i|j suffix
# * - ኢ -> *i
CV -> .-i		[{^I2i};{^a2i}]
.-i -> -.i		[:<;:>]
-.i -> start	[:ኢ]
-.i -> i		[:ኢ]
CV -> .-E        	[{^I2E}]
.-E -> -.E		[:<;:>]
-.E -> start	[:ኤ]
-.E -> i		[:ኤ]
# *ኢ|*ኤ - ኣ -> ያ
i -> ya.-		[ያ:]
ya.- -> ya-.	[:-]
ya-.-> ya-.		[:-]
ya-. -> start	[:ኣ]

# delete -, <, and > when followed by a consonant
start -> -.X	[:-;:<;:>]
-.X -> -.X		[:-;:<;:>]
# delete እ following other segments
-.X -> start	[**;**v;/;:እ]
-.X -> CV		[]

start ->
-.X ->
