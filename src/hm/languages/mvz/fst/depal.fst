-> start

start -> nodepal   []       [-depal]

start -> depal []     [+depal]

#start -> end   []       [c=B,tm=i];[c=B,tm=p,-neg];[c=A|C|D|E|F]
## these conditions are required to prevent non-palatalized  at- forms for classes A and E
## [c=A|E,vc=at,tm=j];[c=A|E,vc=0|ps|a];[c=A|E,vc=at,tm=p,+neg]

# PRF NEG and JUS for class B
#start -> B       []        [c=B,tm=j];[c=B,tm=p,+neg]
# PRF NEG and JUS for class A:1=J,2=o
#start -> AJo   []        [c=A,1=J,2=o,tm=j];[c=A,1=J,2=o,tm=p,+neg]
# What about C?
nodepal -> at     []        [c=A|E,vc=at]
# add features to prevent non-palatalized at- forms in A and E
nodepal -> end    []
# [c=B|C|D|F|K];[vc=0|a|ps]

# these allow for ሸከተ ጘጘተ ቄለበ
# ኣንሰከተ, የሰክት; ኣናሰብ, ኣንበተን; የቶት 
depal -> depal2    [{depal};{E2e};{depal.o}]
# depalatalize second B root consonant
depal2 -> end        [{depalG.e};{depalG.I};%C;%e]

# include palatalized at- forms of classes A and E alongside non-palatalized forms (maybe this is lexical)
# skip C0 for E
at -> at1         [%X]                                    [c=E]
at -> at1         []                                        [c=A]
# palatalize C1
at1 -> end       [{pal}]

end -> end       [%X]
end ->

