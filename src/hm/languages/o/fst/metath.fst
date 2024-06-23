# metathesis
# arg + te -> agarte
# kolf + te -> kofalte
# r/l + C1 t/n -> C1 a r/l t/n

-> start

# This is an optional rule, so let everything pass
start -> start    [!;$;-;>]

# agarC-
start -> r.		[:r]
r. -> rC	  	[!]     # any constraints on which consonants?
rC -> rCa       	[a:]
rCa -> RCaR		[r:]
# kofalC
start -> l.		[:l]
l. -> lC         	[!]
lC -> lCa     		[a:]
lCa -> RCaR		[l:]

RCaR -> RCaR+	[-;>]
RCaR+ -> start	[t;n;s]

start ->
