# optionally change i to I following palatal consonants
# optionally change GWe to Go and vice versa and GW to Gu and vice versa
# a->e following laryngeal
# delete gemination characters (change for phonetic FST)

-> start

start -> start	[^^X;:/;:_;ሀ:ሃ;አ:ኣ;ሐ:ሓ;{i2I}]
start -> gkq	[ጐ:ጎ;ኰ:ኮ;ቈ:ቆ;ጎ:ጐ;ኮ:ኰ;ቆ:ቈ;ሆ:ኈ;ጉ:ጕ;ኩ:ኵ;ቁ:ቍ;ሁ:ኍ;ጕ:ጉ;ኵ:ኩ;ቍ:ቁ;ኍ:ሁ]

gkq -> start	[^^X;:/;:_;ሀ:ሃ;አ:ኣ;ሐ:ሓ;{i2I}]

start ->

