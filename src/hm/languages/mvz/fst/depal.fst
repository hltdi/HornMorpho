-> start

start -> end   []       [c=B,tm=i];[c=B,tm=p,-neg];[c=D|E|F];[c=A|C,cs=2,tm=j];[c=A|C,cs=0|1];[c=A|C,cs=2,tm=p,+neg]

start -> B       []        [c=B,tm=j];[c=B,tm=p,+neg]
start -> at     []        [c=A|C,cs=2,tm=i];[c=A|C,cs=2,tm=p,-neg]

B -> B2             [{depal.e};{B.E2e}]      [s=0|P12]
B2 -> end         [{depal.e};{B.E2e}]      [s=P12|P2]
B2 -> end         [X;C]                                      [s=0]
at -> end         [{pal.e};{B.e2E}]

end -> end       [X;C]
end ->

