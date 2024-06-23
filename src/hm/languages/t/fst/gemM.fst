-> start

start -> start	[^N]

# Delete single /: gemination character
start -> del/	[:/]
del/ -> start	[^N]

# Keep //: space character
start -> /		[/]
/ -> start		[/]

start ->
