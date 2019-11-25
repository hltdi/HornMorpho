# Delete initial glottal stop, ignoring any initial digits and punctuation

-> start

# digits at the beginning don't count
start -> start  [D]

start -> end    [X-';V;_]

start -> end    [:']

end -> end      [X;V;_;D]

end ->
