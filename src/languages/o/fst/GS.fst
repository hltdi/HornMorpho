-> start

start -> start	[!;-;L;>]

# short V
start -> V		[$]
V -> start		[!-';-;>]
V -> V			[L]
# ' in other environments
V -> V'			[']
V'-> start		[!;$]
V -> V>			[';w:';h:';y:']
# ' before -V
V> -> V'+		[:>;:-]
V'+ -> start	[$]

# ' before -C: lengthen first
V -> VV			[L:]
VV -> VV'		[:']
VV' -> VV'+		[:>;:-]
VV'+ -> start	[t;n;s]

start ->