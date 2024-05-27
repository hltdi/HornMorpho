### V + w/y
### Iy -> i; Iw -> u / # > | >C
### ey -> e; ew -> o / # > | >C
### iy -> i; iw -> i / # > | >C
### iw -> y # >V

-> stem

stem -> stemV		[]		[-cons]
stem -> stemC		[]		[+cons]

# No changes for stem V
stemV -> stemV		[^N;/]

stemC -> stemC		[*a;*o;*E;*u;/]

stemC -> stemC_e	[*e]
stemC_e -> stemC_e	[*e;/]
stemC_e -> stemC_I	[*-ይ,ው]
stemC_e -> stemC_i	[*i]
stemC_e -> stemC	[*a;*o;*E;*u]

stemC -> stemC_I	[*]
#stemC_I -> stemC_I	[*-ይ,ው;/]
stemC_I -> stemC_I	[*;/]
stemC_I -> stemC_e	[*e]
stemC_I -> stemC_i	[*i]
stemC_I -> stemC	[*a;*o;*E;*u]

stemC -> stemC_i	[*i]
stemC_i -> stemC_I	[*-ይ,ው;/]

# y,w maintained other than in final position
stemC_e -> wy		[ይ;ው]
stemC_I -> wy		[ይ;ው]
# iy should change to Iy here; a separate rule?
wy -> stemC_e		[*e]
wy -> stemC_I		[*-ይ,ው;/]
wy -> stemC_i		[*i]
wy -> stemC			[*a;*o;*E;*u]
wy -> Iy2i			[{I2i}]
wy -> Iw2u			[{I2u}]
wy -> ew2o			[{e2o}]

# iw should change to Iy here; a separate rule?
stemC_i -> w2y		[ይ:ው]

# ey -> e ; iy -> i ; iw -> i before >C or >#
stemC_i -> e2v	        [:ይ;:ው]
stemC_e -> e2v		[:ይ]

# ew -> o before >C or >#
stemC -> ew2o		[{e2o}]
stemC_I -> ew2o		[{e2o}]
stemC_e -> ew2o		[{e2o}]
stemC_i -> ew2o		[{e2o}]
ew2o -> e2v			[:ው]

# Iy -> i | Iw -> u  before C or >#
stemC -> Iy2i        	[{I2i}]
stemC_I -> Iy2i		[{I2i}]
stemC_e -> Iy2i		[{I2i}]
stemC_i -> Iy2i		[{I2i}]
stemC -> Iw2u        	[{I2u}]
stemC_I -> Iw2u		[{I2u}]
stemC_e -> Iw2u		[{I2u}]
stemC_i -> Iw2y		[{I2u}]
Iy2i -> I2v			[:ይ]
Iw2u -> I2v			[:ው]

# iy -> Iy; converb for final -y and final -w; this maybe should be obligatory?
#stemC -> iy.Iy		     [{^i2I}]
stemC_e -> iy.Iy	     [{^i2I}]
stemV -> iy.Iy	     	     [{^i2I}]
iy.Iy -> iyIy.	     	     [ይ;ይ:ው]

# ረኤ, ርኤ (possibly only this verb); ረኣ, ርኣ
stemC_I -> a.y		[ኤ:ኣ;ሔ:ሓ;ዔ:ዓ;ኣ;ሓ;ዓ;ሃ]
stemC_e -> a.y		[ኤ:ኣ;ሔ:ሓ;ዔ:ዓ;ኣ;ሓ;ዓ;ሃ]
stemV -> a.y		[ኤ:ኣ;ሔ:ሓ;ዔ:ዓ]
a.y -> ay.			[:ይ]
# ረኣ+ኻ (alternate to ረኤ+ኻ)
#stemC_e -> a.y		[ኣ;ሓ;ዓ;ሃ]

end -> end			[^N;/;-]

stemV ->
stemC_e ->
stemC_I ->
stemC   ->

e2v ->
I2v ->
w2y ->

iyIy. ->

ay. ->
