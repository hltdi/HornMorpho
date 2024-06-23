### plural
# delete stem boundary > and realize plural D and P

-> start

## stem
start -> C		[!!]
start -> V		[$]
C -> C	 		[!]
V -> C			[!]
C -> V			[$]

V -> V2i		[{v2i};i]

## plural
C ->  C+			[:>]
V -> V+			[:>]
V2i -> V2i+		[:>]

# no plural or determiner
C+   -> end		[-]
V+   -> end		[-]

# plural determiner options
# D...
C+ -> C+D		[i:D]
V2i+ -> V2iD	[:D]
C+ -> C+	 	[!;$]
V+ -> V+		[!;$]

C+D -> C+D		[!;$]
V2iD -> V2iD	[!;$]

C+D -> end		[-]
V2iD -> end		[-]

# D
#C+ ->

## other suffixes
end -> end		[!;$;-;%]

end ->
