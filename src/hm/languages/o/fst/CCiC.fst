# epenthetic i: CCC -> CCiC

-> start

start -> start    [$;-;>;~]

start -> C		[!-~]

C -> CC	 		[!-~]

C -> start		[$;-;>;~]

CC -> start		[$]

# 3 consonants can't occur together (across morpheme boundary)
CC -> CC+		[-;>]

CC+ -> start	[$]

CC -> CCi		[i:]

# only occurs at morpheme boundaries
# delete it because there won't be any more changes
CCi -> CCi+		[:-;:>]

CCi+ -> start	[!-~]

start ->
C ->
