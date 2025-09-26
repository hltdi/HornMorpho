# optionally change i to I following palatal consonants
# optionally change GWe to Go and vice versa and GW to Gu and vice versa
# a->e following laryngeal
# delete gemination characters (change for phonetic FST)
# optionally drop final -ኢ after palatals
# verbs only: optionally change ሽ and ች to ሺ and ቺ before consonantal object suffix or finally
#   (but make it possible anywhere)

-> start

# optionally start with እ before initial ር; እርዳው
start -> Ir  	 [እ:]
Ir -> end	 	[ር]

start -> end	[]

end -> end	[^^X;:/;ሀ:ሃ;አ:ኣ;ሐ:ሓ]
# only if the final i is required as in ሺ
end -> end	[{i2I}]		[-Ci]
end -> gkq	[ጐ:ጎ;ኰ:ኮ;ቈ:ቆ;ጎ:ጐ;ኮ:ኰ;ቆ:ቈ;ሆ:ኈ;ጉ:ጕ;ኩ:ኵ;ቁ:ቍ;ሁ:ኍ;ጕ:ጉ;ኵ:ኩ;ቍ:ቁ;ኍ:ሁ]

gkq -> end	[^^X;:/;ሀ:ሃ;አ:ኣ;ሐ:ሓ;{i2I}]

# 2sf and 3sf perfective endings
end -> end	[ሺ:ሽ;ቺ:ች]

end ->
gkq ->

