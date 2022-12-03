-> start
# % the boundary should probably be after the 'e' in ነኝ and in አይደለሁም, not as here (copied from the TB)
start -> end       <neN:{n++ne}($tense=pres,*ነ) -N(@pron,subc,$number=sing,person=1,*ኝ,~nsubj)>    [tm=prs,pos=aux,-neg,-rel,-sub,sb=[+p1,-p2,-plr],ob=[-expl]]
start -> end        <neh:{n++ne}($tense=pres,*ነ) -h(@pron,subc,$gender=masc,number=sing,person=2,*ህ,~nsubj)>   [tm=prs,pos=aux,-neg,-rel,-sub,sb=[-p1,+p2,-fem,-plr,-frm],ob=[-expl]]
start -> end        <nex:{n++ne}($tense=pres,*ነ) -x(@pron,subc,$gender=fem,number=sing,person=2,*ሽ,~nsubj)>   [tm=prs,pos=aux,-neg,-rel,-sub,sb=[-p1,+p2,+fem,-plr,-frm],ob=[-expl]]
start -> end        <new:{n++ne}($tense=pres,*ነ) -w(@pron,subc,$gender=masc,number=sing,person=3,*ው,~nsubj)>   [tm=prs,pos=aux,-neg,-rel,-sub,sb=[-p1,-p2,-fem,-plr],ob=[-expl]]
start -> end       <nec_:{n++ne}($tense=pres,*ነ) -ec_(@pron,subc,$gender=fem,number=sing,person=3,*ኧች,~nsubj)>   [tm=prs,pos=aux,-neg,-rel,-sub,sb=[-p1,-p2,+fem,-plr],ob=[-expl]]
start -> end        <nat:{n++ne}($tense=pres,*ነ) -at(@pron,subc,$gender=fem,number=sing,person=3,*ኧች,~nsubj)>   [tm=prs,pos=aux,-neg,-rel,-sub,sb=[-p1,-p2,+fem,-plr],ob=[-expl]]
start -> end        <nen:{n++ne}($tense=pres,*ነ) -n(@pron,subc,$number=plur,person=1,*ን,~nsubj)>   [tm=prs,pos=aux,-neg,-rel,-sub,sb=[+p1,-p2,+plr],ob=[-expl]]
start -> end      <nac_hu:{n++ne}($tense=pres,*ነ) -Ac_hu(@pron,subc,$number=plur,person=2,*ኣችሁ,~nsubj)>   [tm=prs,pos=aux,-neg,-rel,-sub,sb=[-p1,+p2,+plr,-frm],ob=[-expl]]
start -> end      <nac_ew:{n++ne}($tense=pres,*ነ) -Ac_ew(@pron,subc,$number=plur,person=3,*ኣቸው,~nsubj)>   [tm=prs,pos=aux,-neg,-rel,-sub,sb=[-p1,-p2,+plr],ob=[-expl]]
start -> end       <newot:{n++ne}($tense=pres,*ነ) -wot(@pron,subc,$person=2,polite=form,*ዎት,~nsubj)>   [tm=prs,pos=aux,-neg,-rel,-sub,sb=[-p1,+p2,-fem,-plr,+frm],ob=[-expl]]
start -> end    <'aydel_ehu:{n++'aydel_e}($tense=pres,polarity=neg,*ኣይደል) -hu(@pron,subc,$number=sing,person=1,*ሁ,~nsubj)> [tm=prs,pos=aux,+neg,-rel,-sub,sb=[+p1,-p2,-plr],ob=[-expl]]
start -> end    <'aydel_eh:{n++'aydel_e}($tense=pres,polarity=neg,*ኣይደል) -h(@pron,subc,$gender=masc,number=sing,person=2,*ህ,~nsubj)> [tm=prs,pos=aux,+neg,-rel,-sub,sb=[-p1,+p2,-fem,-plr,-frm],ob=[-expl]]
start -> end    <'aydel_ex:{n++'aydel_e}($tense=pres,polarity=neg,*ኣይደል) -x(@pron,subc,$gender=fem,number=sing,person=2,*ሽ,~nsubj)> [tm=prs,pos=aux,+neg,-rel,-sub,sb=[-p1,+p2,+fem,-plr,-frm],ob=[-expl]]
# this permits አይደለ,which probably can't occur
start -> end     <'aydel_e:{n++'aydel_e}($tense=pres,polarity=neg,*ኣይደል) -e(@pron,subc,$gender=masc,number=sing,person=3,*ኧ,~nsubj)> [tm=prs,pos=aux,+neg,-rel,-sub,sb=[-p1,-p2,-fem,-plr],ob=[-expl]]
start -> end    <'aydel_ec_:{n++'aydel_e}($tense=pres,polarity=neg,*ኣይደል) -ec_(@pron,subc,$gender=fem,number=sing,person=3,*ኧች,~nsubj)> [tm=prs,pos=aux,+neg,-rel,-sub,sb=[-p1,-p2,+fem,-plr],ob=[-expl]]
start -> end    <'aydel_en:{n++'aydel_e}($tense=pres,polarity=neg,*ኣይደል) -n(@pron,subc,$number=plur,person=1,*ን,~nsubj)> [tm=prs,pos=aux,+neg,-rel,-sub,sb=[+p1,-p2,+plr],ob=[-expl]]
start -> end   <'aydel_ac_hu:{n++'aydel_e}($tense=pres,polarity=neg,*ኣይደል) -Ac_hu(@pron,subc,$number=plur,person=2,*ኣችሁ,~nsubj)> [tm=prs,pos=aux,+neg,-rel,-sub,sb=[-p1,+p2,+plr],ob=[-expl]]
start -> end     <'aydel_u:{n++'aydel_e}($tense=pres,polarity=neg,*ኣይደል) -u(@pron,subc,$number=plur,person=3,*ኡ,~nsubj)>  [tm=prs,pos=aux,+neg,-rel,-sub,sb=[-p1,-p2,+plr],ob=[-expl]]

end ->
