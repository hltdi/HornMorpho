-> start
# % the boundary should probably be after the 'e' in ነኝ and in አይደለሁም, not as here (copied from the TB)
start -> end       <neN:{n++n}($tense=pres,*ን) -eN(@pron,subc,$number=sing,person=1,*ኝ,~nsubj)>    [tm=prs,pos=aux,-neg,-rel,-sub,sb=[+p1,-p2,-plr],ob=[-expl]]
start -> end        <neh:{n++n}($tense=pres,*ን) -eh(@pron,subc,$gender=masc,number=sing,person=2,*ህ,~nsubj)>   [tm=prs,pos=aux,-neg,-rel,-sub,sb=[-p1,+p2,-fem,-plr,-frm],ob=[-expl]]
start -> end        <nex:{n++n}($tense=pres,*ን) -ex(@pron,subc,$gender=fem,number=sing,person=2,*ሽ,~nsubj)>   [tm=prs,pos=aux,-neg,-rel,-sub,sb=[-p1,+p2,+fem,-plr,-frm],ob=[-expl]]
start -> end        <new:{n++n}($tense=pres,*ን) -ew(@pron,subc,$gender=masc,number=sing,person=3,*ው,~nsubj)>   [tm=prs,pos=aux,-neg,-rel,-sub,sb=[-p1,-p2,-fem,-plr],ob=[-expl]]
start -> end       <nec_:{n++n}($tense=pres,*ን) -ec_(@pron,subc,$gender=fem,number=sing,person=3,*ኧች,~nsubj)>   [tm=prs,pos=aux,-neg,-rel,-sub,sb=[-p1,-p2,+fem,-plr],ob=[-expl]]
start -> end        <nat:{n++n}($tense=pres,*ን) -at(@pron,subc,$gender=fem,number=sing,person=3,*ኧች,~nsubj)>   [tm=prs,pos=aux,-neg,-rel,-sub,sb=[-p1,-p2,+fem,-plr],ob=[-expl]]
start -> end        <nen:{n++n}($tense=pres,*ን) -en(@pron,subc,$number=plur,person=1,*ን,~nsubj)>   [tm=prs,pos=aux,-neg,-rel,-sub,sb=[+p1,-p2,+plr],ob=[-expl]]
start -> end      <nac_hu:{n++n}($tense=pres,*ን) -Ac_hu(@pron,subc,$number=plur,person=2,*ኣችሁ,~nsubj)>   [tm=prs,pos=aux,-neg,-rel,-sub,sb=[-p1,+p2,+plr,-frm],ob=[-expl]]
start -> end      <nac_ew:{n++n}($tense=pres,*ን) -Ac_ew(@pron,subc,$number=plur,person=3,*ኣቸው,~nsubj)>   [tm=prs,pos=aux,-neg,-rel,-sub,sb=[-p1,-p2,+plr],ob=[-expl]]
start -> end       <newot:{n++n}($tense=pres,*ን) -ewot(@pron,subc,$person=2,polite=form,*ዎት,~nsubj)>   [tm=prs,pos=aux,-neg,-rel,-sub,sb=[-p1,+p2,-fem,-plr,+frm],ob=[-expl]]
start -> end    <'aydel_ehu:{n++'aydel_}($tense=pres,polarity=neg,*ኣይደል) -ehu(@pron,subc,$number=sing,person=1,*ሁ,~nsubj)> [tm=prs,pos=aux,+neg,-rel,-sub,sb=[+p1,-p2,-plr],ob=[-expl]]
start -> end    <'aydel_eh:{n++'aydel_}($tense=pres,polarity=neg,*ኣይደል) -eh(@pron,subc,$gender=masc,number=sing,person=2,*ህ,~nsubj)> [tm=prs,pos=aux,+neg,-rel,-sub,sb=[-p1,+p2,-fem,-plr,-frm],ob=[-expl]]
start -> end    <'aydel_ex:{n++'aydel_}($tense=pres,polarity=neg,*ኣይደል) -ex(@pron,subc,$gender=fem,number=sing,person=2,*ሽ,~nsubj)> [tm=prs,pos=aux,+neg,-rel,-sub,sb=[-p1,+p2,+fem,-plr,-frm],ob=[-expl]]
# this permits አይደለ,which probably can't occur
start -> end     <'aydel_e:{n++'aydel_}($tense=pres,polarity=neg,*ኣይደል) -e(@pron,subc,$gender=masc,number=sing,person=3,*ኧ,~nsubj)> [tm=prs,pos=aux,+neg,-rel,-sub,sb=[-p1,-p2,-fem,-plr],ob=[-expl]]
start -> end    <'aydel_ec_:{n++'aydel_}($tense=pres,polarity=neg,*ኣይደል) -ec_(@pron,subc,$gender=fem,number=sing,person=3,*ኧች,~nsubj)> [tm=prs,pos=aux,+neg,-rel,-sub,sb=[-p1,-p2,+fem,-plr],ob=[-expl]]
start -> end    <'aydel_en:{n++'aydel_}($tense=pres,polarity=neg,*ኣይደል) -en(@pron,subc,$number=plur,person=1,*ን,~nsubj)> [tm=prs,pos=aux,+neg,-rel,-sub,sb=[+p1,-p2,+plr],ob=[-expl]]
start -> end   <'aydel_ac_hu:{n++'aydel_}($tense=pres,polarity=neg,*ኣይደል) -Ac_hu(@pron,subc,$number=plur,person=2,*ኣችሁ,~nsubj)> [tm=prs,pos=aux,+neg,-rel,-sub,sb=[-p1,+p2,+plr],ob=[-expl]]
start -> end     <'aydel_u:{n++'aydel_}($tense=pres,polarity=neg,*ኣይደል) -u(@pron,subc,$number=plur,person=3,*ኡ,~nsubj)>  [tm=prs,pos=aux,+neg,-rel,-sub,sb=[-p1,-p2,+plr],ob=[-expl]]

end ->
