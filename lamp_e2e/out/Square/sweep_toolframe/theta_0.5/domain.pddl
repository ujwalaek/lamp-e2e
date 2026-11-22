(define (domain Square)
(:requirements :strips :typing :equality :conditional-effects :existential-preconditions :universal-preconditions)
(:types 
	gripper
	nut
	peg
)

(:constants 
)

(:predicates 
	(gripper_nut_0 ?x - gripper ?y - nut)
	(gripper_nut_1 ?x - gripper ?y - nut)
	(gripper_peg_0 ?x - gripper ?y - peg)
	(nut_peg_0 ?x - nut ?y - peg)
	(nut_peg_1 ?x - nut ?y - peg)
	(nut_peg_2 ?x - nut ?y - peg)
	(clear3_gripper_nut_1 ?x - gripper)
)

(:action a1 
:parameters ( ?gripper_extra_p1 - gripper  ?peg_p1 - peg  ?nut_p1 - nut )
:precondition (and 
	(gripper_nut_0 ?gripper_extra_p1 ?nut_p1)
	(gripper_peg_0 ?gripper_extra_p1 ?peg_p1)
	(nut_peg_1 ?nut_p1 ?peg_p1)
) 
:effect (and 
 	(nut_peg_2 ?nut_p1 ?peg_p1) 
	(not (nut_peg_0 ?nut_p1 ?peg_p1))
	(not (nut_peg_1 ?nut_p1 ?peg_p1))
 ) 
)

(:action a2 
:parameters ( ?gripper_extra_p1 - gripper  ?peg_p1 - peg  ?nut_p1 - nut )
:precondition (and 
	(gripper_nut_0 ?gripper_extra_p1 ?nut_p1)
	(gripper_peg_0 ?gripper_extra_p1 ?peg_p1)
	(nut_peg_0 ?nut_p1 ?peg_p1)
) 
:effect (and 
 	(nut_peg_1 ?nut_p1 ?peg_p1) 
	(not (nut_peg_0 ?nut_p1 ?peg_p1))
	(not (nut_peg_2 ?nut_p1 ?peg_p1))
 ) 
)

(:action a3 
:parameters ( ?nut_p1 - nut  ?gripper_p1 - gripper )
:precondition (and 
	(gripper_nut_0 ?gripper_p1 ?nut_p1)
	(clear3_gripper_nut_1 ?gripper_p1) 
) 
:effect (and 
 	(gripper_nut_1 ?gripper_p1 ?nut_p1) 
	(not (gripper_nut_0 ?gripper_p1 ?nut_p1))
	(not (clear3_gripper_nut_1 ?gripper_p1)) 
 ) 
)

(:action a4 
:parameters ( ?gripper_extra_p1 - gripper  ?peg_p1 - peg  ?nut_p1 - nut )
:precondition (and 
	(gripper_nut_0 ?gripper_extra_p1 ?nut_p1)
	(gripper_peg_0 ?gripper_extra_p1 ?peg_p1)
	(nut_peg_1 ?nut_p1 ?peg_p1)
) 
:effect (and 
 	(nut_peg_0 ?nut_p1 ?peg_p1) 
	(not (nut_peg_1 ?nut_p1 ?peg_p1))
	(not (nut_peg_2 ?nut_p1 ?peg_p1))
 ) 
)

(:action a5 
:parameters ( ?gripper_extra_p1 - gripper  ?peg_p1 - peg  ?nut_p1 - nut )
:precondition (and 
	(gripper_nut_0 ?gripper_extra_p1 ?nut_p1)
	(gripper_peg_0 ?gripper_extra_p1 ?peg_p1)
	(nut_peg_2 ?nut_p1 ?peg_p1)
) 
:effect (and 
 	(nut_peg_0 ?nut_p1 ?peg_p1) 
	(not (nut_peg_1 ?nut_p1 ?peg_p1))
	(not (nut_peg_2 ?nut_p1 ?peg_p1))
 ) 
)

(:action a6 
:parameters ( ?gripper_extra_p1 - gripper  ?peg_p1 - peg  ?nut_p1 - nut )
:precondition (and 
	(gripper_nut_0 ?gripper_extra_p1 ?nut_p1)
	(gripper_peg_0 ?gripper_extra_p1 ?peg_p1)
	(nut_peg_2 ?nut_p1 ?peg_p1)
) 
:effect (and 
 	(nut_peg_1 ?nut_p1 ?peg_p1) 
	(not (nut_peg_0 ?nut_p1 ?peg_p1))
	(not (nut_peg_2 ?nut_p1 ?peg_p1))
 ) 
)

(:action a7 
:parameters ( ?nut_p1 - nut  ?gripper_p1 - gripper )
:precondition (and 
	(gripper_nut_1 ?gripper_p1 ?nut_p1)
) 
:effect (and 
 	(gripper_nut_0 ?gripper_p1 ?nut_p1) 
	(not (gripper_nut_1 ?gripper_p1 ?nut_p1))
	(clear3_gripper_nut_1 ?gripper_p1) 
 ) 
)

(:action a8 
:parameters ( ?gripper_extra_p1 - gripper  ?peg_p1 - peg  ?nut_p1 - nut )
:precondition (and 
	(gripper_nut_0 ?gripper_extra_p1 ?nut_p1)
	(gripper_peg_0 ?gripper_extra_p1 ?peg_p1)
	(nut_peg_0 ?nut_p1 ?peg_p1)
) 
:effect (and 
 	(nut_peg_2 ?nut_p1 ?peg_p1) 
	(not (nut_peg_0 ?nut_p1 ?peg_p1))
	(not (nut_peg_1 ?nut_p1 ?peg_p1))
 ) 
)

(:action a9 
:parameters ( ?gripper_p1 - gripper  ?peg_p1 - peg  ?nut_p1 - nut )
:precondition (and 
	(gripper_nut_1 ?gripper_p1 ?nut_p1)
	(gripper_peg_0 ?gripper_p1 ?peg_p1)
	(nut_peg_2 ?nut_p1 ?peg_p1)
) 
:effect (and 
 	(gripper_nut_0 ?gripper_p1 ?nut_p1) 
	(nut_peg_0 ?nut_p1 ?peg_p1) 
	(not (gripper_nut_1 ?gripper_p1 ?nut_p1))
	(not (nut_peg_1 ?nut_p1 ?peg_p1))
	(not (nut_peg_2 ?nut_p1 ?peg_p1))
	(clear3_gripper_nut_1 ?gripper_p1) 
 ) 
)


)