# Handle cases where stem-final dh is followed by different segments,
# and delete the -

-> start

start -> start  [$;!-dh;L;-;:<;>]

# Get rid of other instances of T and C; we won't need them
# for lower FSTs
# Realize I as i
start -> start  [:T;:C;i:I]

start -> dh     [dh]
# delete the >
dh -> dh	[:-]
dh -> dh+       [:>]
# Singular imperative (I) is realized as u rather than i
dh+ -> start    [u:I]
# dh before a vowel is unchanged; other consonants not possible
dh+ -> start    [$;-]
dh -> start     [$;-]

# dh changes to t before T (passive)
start -> dh>t   [t:dh]
dh>t -> dh>t   [:-]
dh>t -> start	[:T]
# dh changes to t before T/t subject suffixes
#dh>t -> dh>t--  [:-]
dh>t ->	dh>t+ [:>]
# delete the 3sm, 3p T
dh>t+ -> start  [t;:T]

# dhdh for fedhe, fuudhe, godhe, jedhe

start -> dh.dh	  [:dh]
dh.dh -> dhdh.	  [dh]
dhdh. -> dhdh+	  [:>]
dhdh+ -> start	  [:T]

# dh changes to n before n
start -> dh>n   [n:dh]
dh>n -> dh>n	[:-]
dh>n -> dh>n+   [:>]
dh>n+ -> start  [n]

# dh-s(iis) changes to ch
start -> dhs>ch [ch:dh]
dhs>ch -> dhs>ch	[:-]
dhs>ch -> start [:s]

# dh changes to ch before C (special character for infinitive)
start -> dh>ch  [ch:dh]
dh>ch -> dh>ch	[:-]
dh>ch -> dh>ch+ [:>]
dh>ch+ -> start [:C]

#(dh can't precede any other consonants)

start ->
