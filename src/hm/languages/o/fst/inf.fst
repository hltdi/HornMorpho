# Infinitive suffix; -dh -> -chuu; otherwise + -uu
# < stem start and delete - before infinitive

-> start

start -> start  [$$;!!;%-C;:<;-]

## infinitive
# dh changes to ch before C (special character for infinitive)
start -> dh>ch      [ch:dh]
dh>ch -> dh>ch-	[:-]
dh>ch- -> end [:C]

# no changes for other consonants; delete C
start -> steminf	[!-dh]
steminf -> steminf-	[:-]
steminf- -> end		[:C]

# optional changes for ', w, y
start -> '		[w:';y:';h:';':w;':y;':h]
' ->  '-			[:-]
'- -> end		[:C]

start -> yw		[w:y;':y;y:w;':w]
yw -> yw-		[:-]
yw- -> end		[:C]

## no infinitive
start -> end	[>]

end -> end		[$;!;%;>;-]

end ->
