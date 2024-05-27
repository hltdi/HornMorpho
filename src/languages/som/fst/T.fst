# realize subject suffix (2, 3sf)
# T -> d ; {c,d,h,kh,q,w,x,y,'}_
# T -> dh ; dh _
# T -> sh ; l _
# T -> s ; [cls=2];[cls=3];[a=prg] _

-> stem

# stem
stem -> =.       [=]
=. -> suff       [t:T;$;!]

# T -> d
stem -> .d       [c;d;h;kh;q;w;x;y;']
.d -> =.d        [=]
.d -> stem       [b;f;g;j;k;m;n;p;r;s;sh;t;v;z;$]
# can these consonants follow d?
.d -> .d         [c;d;h;kh;q;w;x;y;']
.d -> .dh        [dh]
.d -> l.         [l]
=.d -> suff      [d:T;$;!]

# T -> dh
stem -> .dh      [dh]
.dh -> =.dh      [=]
.dh -> stem      [b;f;g;j;k;m;n;p;r;s;sh;t;v;z;$]
# can these consonants follow dh?
.dh -> .d        [c;d;h;kh;q;w;x;y;']
.dh -> .dh       [dh]
.dh -> l.        [l]
=.dh -> suff     [dh:T;$;!]

# T -> sh
stem -> l.       [l]
l. -> l=.        [=]
l=. -> suff      [sh:T;$;!]
l. -> .d         [c;d;h;kh;q;w;x;y;']
l. -> l.         [l]
l. -> .dh        [dh]
l. -> suff       [b;f;g;j;k;m;n;p;r;s;sh;t;v;z;$]

# other consonants
stem -> stem     [b;f;g;j;k;m;n;p;r;s;sh;t;v;z;$]

# environments for T -> s
# causative -i...

suff -> suff     [$;!;T]
suff ->
# no suffix?
=. ->
