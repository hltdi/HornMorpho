-> start

start -> end   []       [c=B,tm=i];[c=B,tm=p,-neg];[c=A|C|D|E|F]
# these conditions are required to prevent non-palatalized  at- forms for classes A and E
# [c=A|E,vc=at,tm=j];[c=A|E,vc=0|ps|a];[c=A|E,vc=at,tm=p,+neg]

start -> B       []        [c=B,tm=j];[c=B,tm=p,+neg]
# What about C?
start -> at     []        [c=A|E,vc=at,tm=i];[c=A|E,vc=at,tm=p,-neg]

# these allow for ሸከተ ጘጘተ ቄለበ 
B -> B2             [{depal};Q]
B2 -> end         [{depalG.e};{depalG.I};CC;Q]

# include palatalized at- forms of classes A and E alongside non-palatalized forms (maybe this is lexical)
# skip C0 for E
at -> at1         [X;C]                                    [c=E]
at -> at1         []                                           [c=A]
# palatalize C1
at1 -> end       [{pal}]

end -> end       [X;C]
end ->

