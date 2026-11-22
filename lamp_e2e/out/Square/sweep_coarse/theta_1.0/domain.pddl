(define (domain Square)
(:requirements :strips :typing :equality :conditional-effects :existential-preconditions :universal-preconditions)
(:types 
	peg
	gripper
	nut
)

(:constants 
)

(:predicates 
	(gripper_nut_0 ?x - gripper ?y - nut)
	(gripper_nut_1 ?x - gripper ?y - nut)
	(gripper_peg_0 ?x - gripper ?y - peg)
	(nut_peg_0 ?x - nut ?y - peg)
	(clear3_gripper_nut_1 ?x - gripper)
)

(:action a1 
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

(:action a2 
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


)