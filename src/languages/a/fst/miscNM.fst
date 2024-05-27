# optionally change i to I following palatal consonants
# optionally change GWe to Go and vice versa and GW to Gu and vice versa
# a->e following laryngeal
# delete gemination characters (change for phonetic FST)
# replace // with space

-> start

start -> start	[^^X;ሀ:ሃ;አ:ኣ;ሐ:ሓ;{i2I}]
start -> gkq	[ጐ:ጎ;ኰ:ኮ;ቈ:ቆ;ኈ:ሆ;ጎ:ጐ;ኮ:ኰ;ቆ:ቈ;ሆ:ኈ;ጉ:ጕ;ኩ:ኵ;ቁ:ቍ;ሁ:ኍ;ጕ:ጉ;ኵ:ኩ;ቍ:ቁ;ኍ:ሁ]
gkq -> start	[^^X;ሀ:ሃ;አ:ኣ;ሐ:ሓ;{i2I}]

start -> del/	[:/]
gkq -> del/		[:/]
del/ -> start	[^^X;ሀ:ሃ;አ:ኣ;ሐ:ሓ;{i2I}]
del/ -> gkq		[ጐ:ጎ;ኰ:ኮ;ቈ:ቆ;ኈ:ሆ;ጎ:ጐ;ኮ:ኰ;ቆ:ቈ;ሆ:ኈ;ጉ:ጕ;ኩ:ኵ;ቁ:ቍ;ሁ:ኍ;ጕ:ጉ;ኵ:ኩ;ቍ:ቁ;ኍ:ሁ]

start -> /		[ :/]
gkq -> / 		[ :/]
/ -> start		[:/]
/ -> gkq		[:/]

start ->

