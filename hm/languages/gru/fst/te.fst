# delete or convert to e the vowel in passive prefix t*
# convert * before the stem prefix n to I when it's word initial

-> start

# no prefix: t* -> te
start -> stem       [=]
# t must be first character after =
stem -> end         [X-t;V;/;_]
stem -> t           [t]
t -> t*.            [e:*]
t -> t*.V           [:*]
# delete second e: t*elal_efe
t*. -> end          [:_;X;V-e,a;/]
t*.V -> end         [a;e]
t -> end            [X;V;/;_]
stem -> end         [=]

# prefix: t* -> t | /
start -> pre        [X;V;/;_]
pre -> pre          [X;V;/;_]
pre -> prestem      [=]
prestem -> end      [X-t;V;/;_]
prestem -> pret     [t]
pret -> end         [:*;X;V;/;_]
prestem -> pret0    [/:t]
pret0 -> end        [:*]

end ->
end -> end          [X;V;/;_;=;@]

