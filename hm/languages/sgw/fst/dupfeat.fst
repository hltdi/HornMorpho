-> suff

suff -> suff        [XX]
suff -> stem        [=]

stem -> dup         [:]          [dup=1|2];[as=it]
stem -> end         [:]          [dup=None];[as=rc|None]
# last consonant is palatalized
dup -> pal1        [^]
pal1 -> pal1C      [GG;DD]
# frequentative doesn't care about final palatalized consonant
pal1C -> dup2      [:]         [as=it]
pal1C -> pal1C     [V]         [dup=1|2]
# C3 is labialized; relevant only for dup=2
pal1C -> pal1CL    [@]         [dup=2]
# C3 is palatalized or neither
pal1C -> pal1Cn    [:;^]       [dup=2]
# palatalize C-1
pal1C -> end       [^:]        [dup=1]
pal1Cn -> pal1CC   [X]
pal1CC -> pal1CC   [V]
# palatalize C-2: X*P*XP
pal1CC -> end        [^:]
# LP*L*P
pal1CL -> pal1CLC    [KK;MM]
pal1CLC -> pal1CLC   [V]
# palatalize C2: L*P*LP
pal1CLC -> pal1CLCp  [^:]
pal1CLCp -> pal1CLCC [GG;DD]
pal1CLCC -> pal1CLCC [V]
# labialize C1: *L*PLP
pal1CLCC -> end      [@:]

# last consonant is labialized
dup -> lab1        [@]         [dup=1|2]
lab1 -> lab1C      [KK;MM]
# frequentative doesn't care about final labialized consonant
lab1C -> dup2      [:]         [as=it]
lab1C -> lab1C     [V]         [dup=1|2]
lab1C -> lab1C     [^;@]       [dup=2]
# labialize C-1
lab1C -> end       [@:]        [dup=1]
lab1C -> lab1CC    [X]         [dup=2]
lab1CC -> lab1CC   [V]
# labialize C-2
lab1CC -> end      [@:]

# last consonant is neither palatalized nor labialized
# for simple reduplication, stop here
dup -> end         [X]         [dup=1]

### check C-1 for frequentative and complex reduplication
dup -> dup2        [X]         [dup=2];[as=it]
dup2 -> dup2       [V]
# palatalized
dup2 -> pal2       [^]
pal2 -> pal2C      [GG;DD]
## palatalize C-2
pal2C -> pal2C     [V]
pal2C -> end       [^:]        [as=it]
# interim consonant could be palatalized or labialized
pal2C -> pal2C     [^;@]       [dup=2]
pal2C -> pal2CC    [X]         [dup=2]
pal2CC -> pal2CC   [V]
# palatalize C-3
pal2CC -> end      [^:]

# labialized
dup2 -> lab2       [@]
lab2 -> lab2C      [GG;BB]
## labialize C-2
lab2C -> lab2C     [V]
lab2C -> end       [@:]        [as=it]
# interim consonant could be palatalized or labialized
lab2C -> lab2C     [^;@]       [dup=2]
lab2C -> lab2CC    [X]         [dup=2]
lab2CC -> lab2CC   [V]
# labialize C-3
lab2CC -> end      [@:]

# C-1 is neither palatalized nor labialized
dup2 -> end        [X]

#start ->

end ->
end -> end         [XX;^;@;=]
