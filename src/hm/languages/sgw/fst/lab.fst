# perfective: labialization due to
#   impersonal
#   3sm object suffix, singular subjects except 2sf

-> start

start -> start      [XX;*;=;^;@]

start -> lab0       [:4]
# V at least may intervene between stem and object suffix for 3smo
lab0 -> lab0        [XX]
lab0 -> lab         [=]

# stem consonant is palatal or palatalized (PP, ^X)
# or palatalizable but not palatalized (DD-r)
# or neither palatalizable or labializable (r,n)
lab -> lab^         [^]
lab^ -> lab        [X]
lab -> lab         [PP;DD;n;V]
# labialize final consonant
lab -> lab1         [@:]
lab1 -> fin         [MM;KK]
# final consonant already labialized or no more stem characters
lab -> fin          [UU;=]

fin -> fin          [X;V;^;@;=]

fin ->
start ->
