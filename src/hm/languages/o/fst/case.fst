### realize case suffixes

-> start

## stem  + def
start -> C		[!!]
start -> V		[$$1]
start -> VV		[$$2]

C -> CC	 		[!!]
C -> V			[$$1]
C -> VV			[$$2]

V -> C			[!!1]
V -> CC			[!!2]

VV -> C			[!!1]
VV -> CC		[!!2]

CC -> V			[$$1]
CC -> VV		[$$2]

## changes before the case boundary
C -> Vx			[:a;:e;:i;:o;:u]
# not sure what to do in the case of vowels other than a
CC -> CCVx		[i:a;e;i;o;u]
# lengthen short vowel (or use L)
C -> VL			[{V2VV}]
CC -> VL		[{V2VV}]

## case
C -> Cc			[:-]
# (actually this is not possible)
CC -> Cc		[:-]
V -> Vc			[:-]
VV -> VVc		[:-]

Vx -> Vxc		[:-]
CCVx -> CCVxc	[:-]
VL -> VLc		[:-]

# no case marker (base)
Cc -> end		[-]
Vc -> end		[-]
VVc -> end		[-]

# subject
Cc -> case		[:S]
CCVxc -> case	[:S]
Vxc -> case		<ni:S>
Vxc -> case		<ti:S>		[+fem]
VVc -> case		[n:S]

# genitive, dative, instrumental, ablative
VLc -> case		[:D;:A]
VLc -> gen		[:G]
VVc -> gen		[:G]
Cc -> gen		[ii:G]
gen -> case		[:]
gen -> case		<tii:D>
gen -> case		<tii:A>
gen -> case		[f:D]
gen -> case		<tiin:I>

# dative and ablative
VLc -> case		[f:D]
VVc -> case		<dhaaf:D>
VVc -> case		<dhaa:D>
VVc -> case		<dhaa:A>
VVc -> case		[f:D]
Cc -> case		[ii:D;ii:A]

# instrumental
VLc -> case		[n:I]
VVc -> case		<dhaan:D>
VVc -> case		[n:I]
CC -> case		<iin:I>

# locative
Vc ->	case	<tti:X>
VVc -> 	case	<tti:X>
Cc -> case		<itti:X>

case -> end		[-]

end -> end		[!;$;-;L;N]

end ->