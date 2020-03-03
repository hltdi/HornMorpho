# realize Y
# with objects: ልሸቅ፟ዮ ሽቀዮ

-> pre

pre -> pre       [X;V;_;/]
pre -> stemC     [=]

# C can be followed by C, Y, _, or V
stemC -> stemV   [V-e]
stemC -> stem_e  [e]
stemC -> stem_e0 [:e]
stemC -> stemC   [X-Y;_]
stemC -> stemCE  [E:Y]
stemC -> stemCy  [y:Y]
stemC -> stemCY0 [:Y]
stemC -> suf     [=]

# V can be followed by C, or Y
stemV -> stemC     [X-Y;/]
stemV -> stemVE    [E:Y]
stemV -> suf       [=]

stem_e -> stemC    [X-Y]
stem_e -> stem_eY0 [:Y]
stem_e -> stem_e=  [=]
stem_e= -> suf     [X;V-e]
stem_e -> stem_eYy [y:Y]

stem_e0 -> stemVE  [E:Y]
# xeqEko, xeqEt
sufVE -> suf        [k;:e]
# xqE
stemVE -> sufVE     [=]
stem_eY0 -> suf_eY0 [=]
stem_eYy -> suf_eYy [=]
# xqey, xqew, xqeyo (f.), xqewo
suf_eY0 -> suf_eY0  [_]
suf_eY0 -> suf      [y:i;w:u;y]
# xqeye
suf_eYy -> suf_eYy  [_]
suf_eYy -> suf      [e;o]
# lxeqqE
stemCE -> sufCE     [=]
stemCy -> sufCy     [=]
# lxeqqyo, lxeqqyen
sufCy -> sufCy      [_]
sufCy -> suf        [o;e]
# txeqqi, txeqqu
stemCY0 -> sufCY0   [=]
sufCY0 -> suf       [i;u]

stem_e0 -> stem_e0= [=]
stem_e0= -> suf     [e]

suf -> suf       [X;V;_;/]

suf ->
sufVE ->
sufCE ->
stem_e= ->