# convert sequences of vowels and consonants across stem-affix boundaries and within stems

## prefix
-> start

## no prefix
start -> nopref   [:=]
# r becomes n word initially
nopref -> stem    [X-r;n:r]

## prefix-stem boundary
# only possible prefixes are ye-, be-, te-
start -> preC   [y;b;t]
# preserve e- before stem consonant
preC -> preV    [e]
preV -> e=.     [:=]
e=. -> stem     [X]

# delete e- before stem vowel
preC -> preXe   [:e]
preXe -> Xe=.   [:=]
# delete stem-initial I after prefix
Xe=. -> stem    [V-I;:I]

## stem
stem -> stemC    [X]
stem -> stemV    [V-a,e]
stem -> stemA    [a]
stem -> stemE    [e]
stemC -> stemA   [a]
stemC -> stemE   [e]
stemC -> stemXE  [:e]
stemC -> stemC   [X-r,n,l]
stemC -> stemR   [r;n;l]
stemR -> stemC   [X-r,n,l]
stemR -> stemR   [r;n;l]
stemC -> stemV   [V-a,e]
stemR -> stemV   [V-a,e]
stemR -> stemA   [a]
stemR -> stemE   [e]
stemR -> stemXE  [:e]
stemV -> stemC   [X-r,n,l]
stemV -> stemR   [r;n;l]
stemA -> stemC   [X-r,n,l]
stemA -> stemR   [r;n;l]
stemE -> stemC   [X-r,n,l]
stemE -> stemR   [r;n;l]
# delete r,l,n before -n... suffix
stemV -> stemXR  [:r;:n;:l]
stemA -> stemXR  [:r;:n;:l]
stemE -> stemXR  [:r;:n;:l]
stemC -> stemXR  [:r;:n;:l]
stemR -> stemXR  [:r;:n;:l]
# assuming sequences of vowels not possible

## stem-suffix boundary
stemC -> C.suf     [:=]
stemR -> R.suf     [:=]
stemV -> V.suf     [:=]
stemA -> A.suf     [:=]
stemE -> E.suf     [:=]
stemXE -> XE.suf   [:=]
stemXR -> XR.suf   [:=]

C.suf -> CsufV.    [V]
R.suf -> CsufV.    [V]
V.suf -> VsufV.    [w:u;a]
V.suf -> Vsuf.E    [y:]
Vsuf.E -> VsufV.   [E]
A.suf -> VsufV.    [w:u;:a]
A.suf -> Asuf.E    [y:]
Asuf.E -> VsufV.   [E]
XE.suf -> VsufV.   [o:u;a;E]
# actually a GEMINATED n or l
XR.suf -> suf      [n;l:r]
C.suf -> suf       [X]
R.suf -> suf       [X-n]
V.suf -> suf       [X]
A.suf -> suf       [X]
E.suf -> suf       [X]

CsufV. -> suf      [X;V;:]
VsufV. -> suf      [X;V;:]
suf -> suf         [X;V]

suf ->
A.suf ->
E.suf ->
V.suf ->
C.suf ->
R.suf ->
