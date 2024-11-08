-> first

# a word can start with a series of border characters followed by any letter.
first -> start	[*v;*]
first -> first	[-;:+]
first -> CV		[]

start -> start   [**v;**;-;:+]
start -> CV		[]

CV -> .-a        	[{I2a};{e2a};*a]
.-a -> -.a		[:-;:+]
-.a -> -.a		[:-;:+]
-.a -> start	[:ኣ]

CV -> .-e		[{I2e};*a;*e]
.-e -> -.e		[:-;:+]
-.e -> -.e		[:-;:+]
-.e -> start	[:አ]

CV -> .-u		[{I2u};{a2u}]
.-u -> -.u		[:-;:+]
-.u -> -.u		[:-;:+]
-.u -> start	[:ኡ]

CV -> .-o		[{I2o}]
.-o -> -.o		[:-;:+]
-.o -> -.o		[:-;:+]
-.o -> start	[:ኦ]

# 2sf t=i|j suffix
# * - ኢ -> *i
CV -> .-i		[{I2i}]
.-i -> -.i		[:+]
-.i -> start	[:ኢ]
-.i -> i		[:ኢ]
CV -> .-E        	[{I2E}]
.-E -> -.E		[:+]
-.E -> start	[:ኤ]
-.E -> i		[:ኤ]
# *ኢ|*ኤ - ኣ -> ያ
i -> ya.-		[ያ:]
ya.- -> ya-.	[:-]
ya-.-> ya-.		[:-]
ya-. -> start	[:ኣ]

# delete - and + when followed by a consonant
#start -> -.X	[:-;:+]
#-.X -> -.X		[:-;:+]
# delete እ following other segments
#-.X -> start	[**;**v;:እ]
#-.X -> CV		[]

start ->
#-.X ->
