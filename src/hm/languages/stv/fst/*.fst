# handle *t (passive-reflexive)
# *y (imprf prefix)
-> start

start -> post  [X;V]
start -> start [+]
post -> post   [X;V;_;/;%-*]

# * at the beginning of the word
start -> *0    [:*]
*0 -> *0t      [t]
*0t -> post    [a:]
*0 -> post     [i:y]

# * with preceding segments
post -> *1     [:*]
*1 -> post     [t;:y]
# Ilew_ before non-back V
*1 -> *1_      [_]
*1_ -> post    [ee;ii;i;e]
*1 -> *1x_     [:_]
*1x_ -> post   [X;V-ee,ii,i,e]

post ->
