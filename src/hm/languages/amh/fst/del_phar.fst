-> start

# Keep everything at the beginning
start -> end      [X;V;%]

end -> end        [X-`;V;%]

# Delete ` in the middle of the word
end -> del`       [:`]
# but only before vowels
del` -> end       [V]

#end -> end        [:`]

end ->
