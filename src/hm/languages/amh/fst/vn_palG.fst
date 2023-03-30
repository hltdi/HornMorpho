# palatalizable -> palatal / _i

-> start

start -> start [X-JJ;V;_;/]

# already palatalized
start -> PP    [JJ]
PP -> PP       [JJ;_;/]
PP -> start    [X-JJ;V-i]

start -> P     [c:t;j:d;C:T;x:s;C:S;Z:z;y:l;N:n]
PP -> P        [c:t;j:d;C:T;x:s;C:S;Z:z;y:l;N:n]

P -> P         [_]            # actually only one _ possible
# after palatalized C, i possible before C (or final, but not for GENERATION)
P -> Pi        [i]
Pi -> start    [X]
# after palatalized C, delete the i before a vowel
P -> Pxi       [:i]
Pxi -> start   [V]       # only a possible?

# already palatalized; drop i after these before a vowel
start -> P     [J]
start -> !P    [J]
!P -> !P       [_]
!P -> start    [X;V-i,E;/]

start ->
PP ->
# Final i after palatal (geZi, gedayi); EXCLUDE FOR GENERATION
# Pi ->
# No final i after palatal  (geZ, geday)
Pxi ->
!P ->
