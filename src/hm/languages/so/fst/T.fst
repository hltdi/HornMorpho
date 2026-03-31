# realize subject suffix (2, 3sf)
# T -> d ; {c,d,h,kh,q,w,x,y,'}_
# T -> dh ; dh _
# T -> sh ; l _
# T -> s ; [cls=2];[cls=3];[a=prg] _

-> stem0

# delete the stem start character
stem0 -> stem [:<]

# T -> t
stem -> stem     [b;f;g;j;k;m;n;p;r;s;sh;t;v;z;$;I;:>]
stem -> stem_   [:-]
stem_ -> suff	[t:T;$;I;!;:-]

# T -> d
stem -> .d       [c;d;h;kh;q;w;x;y;';:>]
.d -> stem       [b;f;g;j;k;m;n;p;r;s;sh;t;v;z;$;I;:>]
.d -> .d         [c;d;h;kh;q;w;x;y;';:>]
.d -> .dh        [dh]
.d -> l.	 [:l]
.d -> l		 [l]
.d -> .d_	 [:-]
.d_  -> suff	 [d:T;$;I;!;:-]

# T -> dh
stem -> .dh      [dh]
.dh -> stem      [b;f;g;j;k;m;n;p;r;s;sh;t;v;z;$;I;:>]
.dh -> .d        [c;d;h;kh;q;w;x;y;']
.dh -> l.	 [:l]
.dh -> l	 [l]
.dh -> .dh       [dh;:>]
.dh -> .dh_	 [:-]
# second dh can be deleted orthographically
.dh_ -> suff      [dh:T;:T;$;I;!;:-]

# lT -> sh (l deleted)
stem -> l.       [:l]
l. -> stem       [b;f;g;j;k;m;n;p;r;s;sh;t;v;z;$;I;:>]
l. -> .d         [c;d;h;kh;q;w;x;y;']
# probably not possible
l. -> l.         [:l;:>]
l. -> .dh        [dh]
l. -> l._	 [:-]
l._ -> suff    [sh:T]

# other l (not followed by T)
stem -> l	[l]
l -> stem	 [b;f;g;j;k;m;n;p;r;s;sh;t;v;z;$;I;:>]
l -> .d         [c;d;h;kh;q;w;x;y;']
l -> l          [l;:>]
l -> .dh        [dh]
l -> l_	 [:-]
l_ -> suff    [$;I;!;:-]

# environments for T -> s
# causative -i...

suff -> suff     [$;I;!;T;:-]

suff ->

