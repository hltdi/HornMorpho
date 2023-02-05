-> start

start -> V		[*V]
start -> C		[*]

V -> end	 	 [ህ:=ክ;ሁ:=ኩ]
C -> end		 [ክ:=ክ;ኩ:=ኩ]

V -> C			 [*]
C -> V			 [*V]
C -> C			 [*]
V -> V			 [*V]

start -> start 	 [^v;^V]
C -> start		 [^v;^V]
V -> start		 [^v;^V]

end -> end		 [^X;^v;^V]

start ->
C ->
V ->
end ->

