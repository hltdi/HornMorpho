# convert sequences of vowels and consonants across stem-affix boundaries and within stems

## suffix and stem
-> start

# no suffixes
start -> stem   [:=]

start -> sufV    [V-e,a,u]
start -> sufC    [X]
sufC -> sufV     [V-e,a,u]
sufV -> sufC     [X]
sufC -> sufC     [X]
## e
start -> suf_e   [e]
sufC -> suf_e    [e]
suf_e -> sufC   [X]
suf_e -> C.=e    [:=]
# bEt-eta, aso-eta
C.=e -> stem     [X;o]
C.=e -> i.y=e    [y:]
# temariy-eta
i.y=e -> stem    [i]
sufC -> V=.e     [:e]
V=.e -> V.=e     [:=]
# T(I)weta
C.=e -> stem     [w:u]
# IKa-ta
V.=e -> stem     [V]
## a
start -> suf_a   [a]
sufC -> suf_a    [a]
suf_a -> sufC    [X]
suf_a -> C.=a    [:=]
# angaca-Ke, tk-aKe, aso-aKe
C.=a -> stem     [X;:a;:e;o]
C.=a -> i.y=a    [y:]
# temariy-aKe
i.y=a -> stem    [i]
# T(I)waKe
C.=a -> stem     [w:u]
## u
start -> suf_uw  [w:u]
sufC -> suf_uw   [w:u]
sufC -> suf_uo   [o:u]
start -> suf_uo  [o:u]
sufC -> suf_uO   [O:u]
start -> suf_uO  [O:u]
start -> suf_u   [u]
fin_uw -> sufC   [X]
sufC -> suf_u    [u]
suf_u -> sufC    [X]
suf_u -> .=u     [:=]
.=u -> stem      [X]
suf_uw -> sufV   [V]
suf_uw -> V.=u   [:=]
V.=u -> stem     [E;o]
suf_uo -> e.=u   [:=]
suf_uO -> a.=u   [:=]
e.=u -> stem     [:e]
a.=u -> stem     [:a]

sufC -> stem     [:=]
sufV -> stem     [:=]

stem -> stem    [X;V-I,a,e]

# delete stem-initial I after prefix
# keep stem-initial a and e after prefix (all prefixes end in e)
stem -> V=.Ia     [:I;a;e]
V=.Ia -> V.=Ia     [:=]
# delete prefix-final 
V.=Ia -> pre      [:e]

stem -> I       [I]
I -> stem       [X]
stem -> e       [e]
e -> stem       [X]
stem -> a       [a]
a -> stem       [X]
e -> preC       [:=]
a -> preC       [:=]
I -> preC       [:=]
preC -> pre     [X]

stem -> pre     [:=]

pre -> pre      [X;V]

pre ->
preC ->

# end ->