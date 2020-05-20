# metathesis
# arg + te -> agarte
# kolf + te -> kofalte
# r/l + C1 t/n -> C1 a r/l t/n

-> start

# This is an optional rule, so let everything pass
start -> start    [!;$]

start -> r.       [:r]
r. -> rC.         [!]     # any constraints on which consonants?
rC. -> rCa.       [a:]
rCa. -> RCaR.     [r:]
RCaR. -> start    [t;n]
start -> l.       [:l]
l. -> lC.         [!]
lC. -> lCa.       [a:]
lCa. -> RCaR.     [l:]

start ->
