### definiteness
# delete stem boundary > and realize plural D

-> start

## stem
start -> C		[!!]
start -> V		[$$]
C -> C	 		[!!]
V -> C			[!!]
C -> V			[$$]

C -> V2i		[{v2i};i]

## definiteness
C ->  C+			[:>]
V -> V+			[:>]
V2i -> V2i+		[:>]

# no determiner
C+   -> end		[-]
V+   -> end		[-]

# determiner options
# D...
C+ -> C+D		[i:D]
V2i+ -> V+D		[:D]

C+D -> C+D		[!;$]
V+D -> V+D		[!;$]

C+D -> end		[-]
V+D -> end		[-]

# D
#C+ ->

## other suffixes
end -> end		[!;$;-;%]

end ->
