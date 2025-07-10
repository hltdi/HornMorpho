-> stem

# no changes for stems that are not deverbal
stem -> end		[]			[d=0]

stem -> neg0	[ኣ]			[d=inf,+neg]
neg0 -> neg1	[ለ]
stem -> istem	[]			[d=inf,-neg];[d=ins]
neg1 -> istem	[:-]		

# infinitive and instrument
istem -> ME		[መ]		[d=ins|inf]
ME -> ME-		[:-]
ME -> AS		[ስ]
ME- -> end		[]			[d=inf]
ME- -> stemsuf	[]			[d=ins]
istem -> ME2A	[ማ:መ]
ME2A -> ME2A-	[:-]
ME2A- -> end	[:ኣ]		[d=inf]
ME2A- -> stemsuf	[:ኣ]		[d=ins]

ME -> ME/		[/]
ME/ -> end		[:-]		[d=inf]
ME/ -> stemsuf	[:-]		[d=ins]

ME/ -> TA		[ታ:ተ]
TA -> TA-		[:-]
TA- -> end		[:ኣ]		[d=inf]
TA- -> stemsuf	[:ኣ]		[d=ins|a]

#ME/ -> METE		[ተ]
#METE -> METE-	[:-]
#METE- -> end		[^N-ኣ]		[d=inf]
#METE- -> stemsuf	[^N-ኣ]		[d=ins]

istem -> MA		[ማ]			[d=ins|inf]
MA -> end		[:-]		[d=inf]
MA -> stemsuf	[:-]		[d=ins]
MA -> AS		[ስ]
MA -> MA/		[/]
MA/ -> end		[:-]		[d=inf]
MA/ -> stemsuf	[:-]		[d=ins]

AS -> AS-		[:-]
AS- -> end		[^S]		[d=inf]
AS- -> stemsuf	[^S]		[d=a|ins]
MA -> MAS.A		[ሳ:ስ]
MAS.A -> MASA-	[:-]
MASA- -> end	[:ኣ]		[d=inf]
MASA- -> stemsuf	[:ኣ]		[d=ins]

MA -> AS.S		[/:ስ]
AS.S -> AS.-S	[:-]
AS.-S -> end		[ሰ;ዘ;ሸ;ዠ;ጸ;ሳ;ዛ;ሻ;ዣ;ጻ]	[d=inf]
AS.-S -> stemsuf	[ሰ;ዘ;ሸ;ዠ;ጸ;ሳ;ዛ;ሻ;ዣ;ጻ]	[d=a|ins]
# needed for ማስ-ሻ-ኢያ: ማሻ
AS.-S -> pal		[{^S2i}]				[d=a|ins]

AS -> AST		[ተ]
AS -> ASTA		[ታ:ተ]
AST -> end		[:-]	[d=inf]
AST -> stemsuf	[:-]	[d=a|ins]
ASTA -> ASTA-	[:-]
ASTA- -> end	[:ኣ]	[d=inf]
ASTA- -> stemsuf	[:ኣ]	[d=a|ins]

ME/ -> M/T		[ተ]
MA/ -> M/T		[ተ]
M/T -> M/T-		[:-]
M/T- -> end		[^N-ኣ]	[d=inf]
M/T- -> stemsuf	[^N-ኣ]	[d=ins]

# manner
stem ->	man1	[ኣ]		[d=m]
man1 -> man2	[/]
# alternative for 1=እ: አተዳደር
man2 -> man2t	[ተ]
man2t -> end	[:-]
man2 -> end		[:-]
man1 -> man1S	[ስ]
man1S -> man1ST	[ተ]
man1ST -> end	[:-]

# agent
stem -> stemsuf	[^N]	[d=a,v=0]

stem -> T		[ተ]		[d=a,v=p];[d=a,v=ast,+pr]
T -> T-	 		[:-]
T- -> stemsuf	[^^N]
# ተስተ+
T -> AS			[ስ]

stem -> A		[ኣ]		[d=a,v=a|as]
A -> A			[/]
A -> stemsuf	[:-]
A -> AS			[ስ]
A -> AS.S		[/:ስ]

stem -> TA		[ታ:ተ]	[d=a,v=p]

stemsuf -> stemsuf	[^N;/]

# agent and manner suffix
stemsuf -> agtsuf	[{^I2i};{^I}]	[d=a,+pal]
agtsuf -> agtsuf-	[:-]
agtsuf- -> fin		[:ኢ]

stemsuf -> insnopal	[{~I2i}]	[d=ins]
insnopal -> insnopal-	[:-]
insnopal- -> insnopalya[:ኢ]
insnopalya -> fin		[ያ]

stemsuf -> inspal		[{^I2a}]	[d=ins]
inspal -> inspal-		[:-]
inspal- -> inspalya	[:ኢ]
inspalya -> fin			[:ያ]

end -> end		[^N;-;/]

end ->
fin ->
