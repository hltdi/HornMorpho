-> stem

stem -> C      [X-r]
C -> =C         [:=]
=C -> end       [y]
=C -> y2i       [i:y]
y2i -> pre      [X]
=C -> pre       [X-y;V]
# negative ay -> E
=C -> a.y=      [:y]
a.y= -> pre     [E:a]

C -> V          [V]
C -> C          [X-r]
C -> r          [r]
C -> r2n        [n:r]

# word initial r -> n
stem -> r      [r]
r -> V          [V]
r -> C          [X]
# r->n in first position or following n in prefix
r2n -> =r2n     [:=]
# prefix ending in -n, deleted before stem-initial r->n (or copy for geminated nn)
=r2n -> pre     [:n]
r -> =r         [:=]
=r -> pre       [X;V]

stem -> V      [V]
V -> C          [X-r]
V -> r          [r]
V -> r2n        [n:r]
V -> =V         [:=]
# delete e- before a stem-initial vowel
=V -> pre       [:e]
=V -> pre       [V-e;X-y]
=V -> a.y=      [:y]
=V -> end       [y]

#stem -> pre    [:=]

pre -> pre      [X;V]
=r2n ->
=C ->
=V ->
pre ->
end ->