-> stem

# no changes for stems that are not deverbal
stem -> end		[]			[d=0]

# infinitive and instrument
stem -> ME		[መ]		[d=ins|inf]
ME -> ME-		[:-]
ME -> AS		[ስ]
ME- -> end		[]			[d=inf]
ME- -> stemsuf	[]			[d=ins]
stem -> ME2A	[ማ:መ]
ME2A -> ME2A-	[:-]
ME2A- -> end	[:ኣ]		[d=inf]
ME2A- -> stemsuf	[:ኣ]		[d=ins]
ME -> ME/		[/]
ME/ -> end		[:-]		[d=inf]
ME/ -> stemsuf	[:-]		[d=ins]
ME/ -> TA		[ታ:ተ]
TA -> TA-		[:-]
TA- -> end		[:ኣ]

stem -> MA		[ማ]			[d=ins|inf]
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
MASA- -> stesuf	[:ኣ]		[d=ins]

MA -> AS.S		[/:ስ]
AS.S -> AS.-S	[:-]
AS.-S -> end		[ሰ;ዘ;ሸ;ዠ;ጸ;ሳ;ዛ;ሻ;ዣ;ጻ]	[d=inf]
AS.-S -> stemsuf	[ሰ;ዘ;ሸ;ዠ;ጸ;ሳ;ዛ;ሻ;ዣ;ጻ]	[d=a|ins]
# needed for ማስ-ሻ-ኢያ: ማሻ
AS.-S -> pal		[{^S2i}]				[d=a|ins]

AS -> AST		[ተ]
AST -> end		[:-]	[d=inf]
AST -> stemsuf	[:-]	[d=a|ins]

ME/ -> M/T		[ተ]
MA/ -> M/T		[ተ]
M/T -> end		[:-]	[d=inf]
M/T -> stemsuf	[:-]	[d=ins]

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
A -> stemsuf	[:-]
A -> AS			[ስ]
A -> AS.S		[/:ስ]

stem -> TA		[ታ:ተ]	[d=a,v=p]

stemsuf -> stemsuf	[^N;/]

# agent and manner suffix
stemsuf -> pal		[{^I2i}]
pal ->  pal-			[:-]
pal- -> end			[:ኢ]

end -> end		[^N;-;/]

end ->
