### Generate template

-> start

start -> bound  [:+]

bound -> pre    [:]       [tmp=[pre=None]]
bound -> pre    <:as>     [tmp=[pre=as]]
bound -> pre    <:tt>     [tmp=[pre=tt]]
bound -> pre    [:a]      [tmp=[pre=a]]
# End in vowels that get deleted before a c1=None stem
bound -> pre    [:t]      [tmp=[pre=te,c1=None,v1=a]]
bound -> pre    <:te>     [tmp=[pre=te,c1=1]];[tmp=[pre=te,c1=12]];[tmp=[pre=te,c1=None,v1=None]]
bound -> pre    <:ast>    [tmp=[pre=aste,c1=None,v1=a]]
bound -> pre   <:aste>    [tmp=[pre=aste,c1=1]];[tmp=[pre=aste,c1=12]];[tmp=[pre=aste,c1=None,v1=None]]

pre -> c1       [:]       [tmp=[c1=None]]
pre -> c1       <:12>     [tmp=[c1=12]]
pre -> c1_      [:1]      [tmp=[c1=1]]

c1_ -> c1       [:]       [tmp=[-c1gem]]
c1_ -> c1       [:_]      [tmp=[+c1gem]]

c1 -> v1        [:]       [tmp=[v1=None]]
c1 -> v1        [:e]      [tmp=[v1=e]]
c1 -> v1        [:a]      [tmp=[v1=a]]
c1 -> v1        [:I]      [tmp=[v1=I]]
c1 -> v1        <:Wa>     [tmp=[v1=Wa]]

v1 -> c2        [:]       [tmp=[c2=None]]
v1 -> c2        [:2]      [tmp=[c2=2]]

c2 -> v2        [:]       [tmp=[v2=None]]
c2 -> v2        [:e]      [tmp=[v2=e]]
c2 -> v2        [:a]      [tmp=[v2=a]]

v2 -> c3        [:]       [tmp=[c3=None]]
v2 -> c3        [:3]      [tmp=[c3=3]]

c3 -> v3        [:]       [tmp=[v3=None]]
c3 -> v3        [:e]       [tmp=[v3=e]]
c3 -> v3        [:a]       [tmp=[v3=a]]

v3 -> c4        [:]       [tmp=[c4=None]]
v3 -> c4        [:4]      [tmp=[c4=4]]

c4 -> v4        [:]       [tmp=[v4=None]]
c4 -> v4        [:e]      [tmp=[v4=e]]
c4 -> v4        [:a]      [tmp=[v4=a]]

v4 -> c_2       [:]       [tmp=[c_2=None]]
v4 -> c_2       [:1]      [tmp=[c_2=1]]
v4 -> c_2       [:2]      [tmp=[c_2=2]]
v4 -> c_2       [:3]      [tmp=[c_2=3]]
v4 -> c_2       [:4]      [tmp=[c_2=4]]

c_2 -> c_2_     [:]       [tmp=[-c_2gem]]
c_2 -> c_2_     [:_]      [tmp=[+c_2gem]]

c_2_ -> v_1     [:]       [tmp=[v_1=None]]
c_2_ -> v_1     [:e]      [tmp=[v_1=e]]
c_2_ -> v_1     [:E]      [tmp=[v_1=E]]
c_2_ -> v_1     [:i]      [tmp=[v_1=i]]
c_2_ -> v_1     [:a]      [tmp=[v_1=a]]
c_2_ -> v_1     [:o]      [tmp=[v_1=o]]
c_2_ -> v_1     [:u]      [tmp=[v_1=u]]
c_2_ -> v_1     [:Wa]     [tmp=[v_1=Wa]]
# or [:u]
c_2_ -> v_1     [:W]      [tmp=[v_1=W]]

v_1 -> c_1      [:]       [tmp=[c_1=None]]
v_1 -> c_1      [:t]      [tmp=[c_1=t]]
v_1 -> c_1      [:3]      [tmp=[c_1=c,n=3]]
v_1 -> c_1      [:4]      [tmp=[c_1=c,n=4]]
v_1 -> c_1      [:5]      [tmp=[c_1=c,n=5]]

c_1 -> end      [:]

end ->