### realize conjunctions

-> start

## stem  + def + case
start -> C		[!!]
start -> V		[$$]

C -> V			[$$]
V -> C			[!!]
C -> C			[!!]

# lengthen short vowel; keep long vowel
C -> VL			[{V2VV};aa;ee;ii;oo;uu]

## conjunction

C -> Cc			[:-]
V -> Vc			[:-]
VL -> VLc		[:-]

# no conjunction
Cc -> end		[-]
Vc -> end		[-]

# -s and -f, lengthen vowel
VLc -> end		[:L]
# add i after consonant before mmoo, llee, ?moo, ?woo, ?simmoo
Cc ->  Cconj		[i:]
Cconj -> end	[m;l;w;s]
# nothing to do before other conjunctions (oo and tu after consonants, any,except oo after vowels)
Cc -> end    	       [o;t]
# exclude -oo here
Vc -> end	       [s;w;l;m;t]

end -> end		[!;$;-;L;N]

end ->