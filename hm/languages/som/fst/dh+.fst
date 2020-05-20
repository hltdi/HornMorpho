# Handle cases where stem-final dh is followed by different segments,
# and delete the +

-> start

start -> start  [$;!-dh;L;+]

# Get rid of other instances of C and T; we won't need them
# for lower FSTs
# Realize I as i.
start -> start  [:T;:C;i:I]

start -> dh     [dh]
# delete the +
dh -> dh+       [:+]
# Singular imperative (I) is realized as u rather than i
dh+ -> start    [u:I]
# dh before a vowel is unchanged; other consonants not possible
dh+ -> start    [$]
dh -> start     [$]

# dh changes to t before t/T
start -> dh>t   [t:dh]
# this can also happen within the stem (before -Tam passive)
dh>t -> dh>t+   [:+;:]
# delete the T
dh>t+ -> start  [t;:T]

# dh changes to n before n
start -> dh>n   [n:dh]
dh>n -> dh>n+   [:+]
dh>n+ -> start  [n]

# dhs changes to ch
start -> dhs>ch [ch:dh]
dhs>ch -> start [:s]

# dh changes to ch before C (special character for infinitive)
start -> dh>ch  [ch:dh]
dh>ch -> dh>ch+ [:+]
dh>ch+ -> start [:C]

#(dh can't precede any other consonants)

start ->
