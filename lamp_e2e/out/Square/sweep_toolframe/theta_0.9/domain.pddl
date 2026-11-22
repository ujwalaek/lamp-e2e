(define (domain Square)
(:requirements :strips :typing :equality :conditional-effects :existential-preconditions :universal-preconditions)
(:types 
	nut
	gripper
	peg
)

(:constants 
)

(:predicates 
	(gripper_nut_0 ?x - gripper ?y - nut)
	(gripper_peg_0 ?x - gripper ?y - peg)
	(nut_peg_0 ?x - nut ?y - peg)
	(nut_peg_1 ?x - nut ?y - peg)
	(nut_peg_2 ?x - nut ?y - peg)
)

(:action a1 
:parameters ( ?nut_p1 - nut  ?gripper_extra_p1 - gripper  ?peg_p1 - peg )
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

(:action a2 
:parameters ( ?nut_p1 - nut  ?gripper_extra_p1 - gripper  ?peg_p1 - peg )
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

(:action a3 
:parameters ( ?nut_p1 - nut  ?gripper_extra_p1 - gripper  ?peg_p1 - peg )
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

(:action a4 
:parameters ( ?nut_p1 - nut  ?gripper_extra_p1 - gripper  ?peg_p1 - peg )
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

(:action a5 
:parameters ( ?nut_p1 - nut  ?gripper_extra_p1 - gripper  ?peg_p1 - peg )
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


)