### V + w/y
### Iy -> i; Iw -> u / # > | >C
### ey -> e; ew -> o / # > | >C
### iy -> i; iw -> i / # > | >C
### iw -> y # >V

-> start

# Go to stem
start -> start	[^N;/;-]

start -> stem	[<]

# y and w rules

stem -> stem		[*a;*o;*E;*u;/]

stem -> stem_e		[*e]
stem_e -> stem_e	[*e;/]
stem_e -> stem_I	[*-ይ,ው]
stem_e -> stem_i	[*i]
stem_e -> stem		[*a;*o;*E;*u]

stem -> stem_I		[*]
stem_I -> stem_I	[*-ይ,ው;/]
stem_I -> stem_e	[*e]
stem_I -> stem_i	[*i]
stem_I -> stem		[*a;*o;*E;*u]

stem -> stem_i		[*i]
stem_i -> stem_I	[*-ይ,ው;/]
stem_i -> stem_e	[*e]
stem_i -> stem_i	[*i]
stem_i -> stem		[*a;*o;*E;*u]

# y,w maintained
stem_e -> wy		[ይ;ው]
stem_I -> wy		[ይ;ው]
# iy should change to Iy here; a separate rule?
stem_i -> wy		[ይ]
wy -> stem_e		[*e]
wy -> stem_I		[*-ይ,ው;/]
wy -> stem_i		[*i]
wy -> stem			[*a;*o;*E;*u]
wy -> wy+			[>]
wy -> Iy2i			[{I2i}]
wy -> Iw2u			[{I2u}]
wy -> ew2o			[{e2o}]
wy+ -> end			[^V]

# iw should change to Iy here; a separate rule?
stem_i -> w2y		[ይ:ው]
w2y -> wy+			[>]
stem_i -> iw		[ው]
iw -> stem_e		[*e]
iw -> stem_I		[*-ይ,ው;/]
iw -> stem_i		[*i]
iw -> stem			[*a;*o;*E;*u]

stem_e -> end		[>]
stem_I -> end		[>]
stem_i -> end		[>]
stem   -> end		[>]

# ey -> e ; iy -> i ; iw -> i before >C or >#
stem_i -> e2v	        [:ይ;:ው]
stem_e -> e2v		[:ይ]
e2v -> e2v+			[>]
e2v+ -> end			[^C]

# ew -> o before >C or >#
stem_I -> ew2o		[{e2o}]
stem_e -> ew2o		[{e2o}]
stem_i -> ew2o		[{e2o}]
ew2o -> e2v			[:ው]

# Iy -> i | Iw -> u  before >C or >#
stem_I -> Iy2i		[{I2i}]
stem_e -> Iy2i		[{I2i}]
stem_i -> Iy2i		[{I2i}]
stem_I -> Iw2u		[{I2u}]
stem_e -> Iw2u		[{I2u}]
stem_i -> Iw2y		[{I2u}]
Iy2i -> I2v			[:ይ]
Iw2u -> I2v			[:ው]
I2v -> I2v+			[>]
I2v+ -> end			[^C]

end -> end			[^N;/;-]

end ->
e2v+ ->
I2v+ ->