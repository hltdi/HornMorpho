# realize vowel A in prefixes before laryngeals and *Y*

-> pre

pre -> stem             [V]
pre -> stem1            [=]

pre -> preC             [X]
# realize A as e if it's not preceded by another prefix
preC -> preCA.L         [e:A]       [vc=[-cs]]
preCA.L -> pre.L        [=]
# ... and the first stem consonant is L
pre.L -> preL.          [LL]
# ... and there is some vowel other than i, u as stem V1 (i, u happen in jussive *Y*)
preL. -> stem           [V-i,u]

# delete A
# always for +cs, and delete initial '
preC -> pre_cs          [:]           [vc=[+cs]]
pre_cs -> pre_cs        [X;V-A;:A]
pre_cs -> stem_cs       [=]
stem_cs -> stem         [:']

# other cases
preC -> pre0A.          [:A]       [vc=[-cs]]
pre0A. -> pre0AC.       [X]
# ...if there's a second prefix
pre0AC. -> stem         [:A]
pre0A. -> pre0A=.C      [=]
# ...or if C1 is laryngeal
pre0A=.C -> pre0A=L.    [LL]
# ... and there's no following vowel or the following vowel is i, u
pre0A=L. -> stem        [X;i;u]
# ... or if C1 is not laryngeal
pre0A=.C -> stem        [RR;YY;V]

# realize A as i (jus *Y*)
preC -> preiA.          [i:A]     [vc=[-cs]]
preiA. -> preiA=.       [=]
# ... when stem C1 is not L or Y
preiA=. -> preiA=C.     [RR]
# ... and stem V1 is i or u; or C2 is y (with no V1)
preiA=C. -> stem        [i;u;y]

# no A after first vowel; go straight to stem and finish
preC -> stem            [X;V-A;=]

# +ps tA -> te when no other prefix and C1 is L; otherwise tA -> t
stem1 -> stemT.         [t]
# delete A
stemT. -> stemTA0.      [:A]
# ... if root begins with C that is not L
stemTA0. -> stem        [RR;YY]
# realize A as e
stemT. -> stemTAe.      [e:A]
# if root C1 is L (and this is not transitive/causative)
stemTAe. -> stem        [LL]         [vc=[-cs]]
stem1 -> stem           [X-t;V]
# if stem-initial t is not followed by A, finish
stemT. -> stem          [X;V-A]

stem -> stem            [X;V-A;:A;_;/;=]

stem ->