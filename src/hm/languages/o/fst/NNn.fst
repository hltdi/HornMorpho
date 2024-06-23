## 1s_sbj: C-an, V-n
## (on nouns)
## Do before all other FSTs with special characters

-> start

start -> C		[!!]
start -> V		[$$]

C -> C	 		[!!]
C -> V			[$$1]
C -> VV			[$$2]
V -> C			[!!]
VV -> C			[!!]

# in 1s n + cop suffix slot
C -> C+	 		[:-]
V -> V+			[:-]
VV -> VV+		[:-]

# 1s
V+ -> end		[n:N]
VV+ -> end		[n:N]
C+ -> end		<an:N>
# cop
VV+ -> end		<dha:dh>
C+  -> end		<i:dh>
V+ ->  end		<ti>
VV+ -> end		<ti>

V+ ->
VV+ ->
C+ ->
end ->
