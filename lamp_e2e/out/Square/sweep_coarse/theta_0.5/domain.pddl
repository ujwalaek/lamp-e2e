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
	(gripper_nut_2 ?x - gripper ?y - nut)
	(gripper_nut_3 ?x - gripper ?y - nut)
	(gripper_peg_0 ?x - gripper ?y - peg)
	(nut_peg_0 ?x - nut ?y - peg)
	(nut_peg_1 ?x - nut ?y - peg)
	(nut_peg_2 ?x - nut ?y - peg)
	(clear3_gripper_nut_1 ?x - gripper)
	(clear3_gripper_nut_2 ?x - gripper)
	(clear3_gripper_nut_3 ?x - gripper)
)

(:action a1 
:parameters ( ?nut_p1 - nut  ?gripper_p1 - gripper )
:precondition (and 
	(gripper_nut_2 ?gripper_p1 ?nut_p1)
	(clear3_gripper_nut_1 ?gripper_p1) 
	(clear3_gripper_nut_3 ?gripper_p1) 
) 
:effect (and 
 	(gripper_nut_3 ?gripper_p1 ?nut_p1) 
	(not (gripper_nut_0 ?gripper_p1 ?nut_p1))
	(not (gripper_nut_1 ?gripper_p1 ?nut_p1))
	(not (gripper_nut_2 ?gripper_p1 ?nut_p1))
	(clear3_gripper_nut_2 ?gripper_p1) 
	(not (clear3_gripper_nut_3 ?gripper_p1)) 
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
 	(nut_peg_0 ?nut_p1 ?peg_p1) 
	(not (nut_peg_1 ?nut_p1 ?peg_p1))
	(not (nut_peg_2 ?nut_p1 ?peg_p1))
 ) 
)

(:action a3 
:parameters ( ?nut_p1 - nut  ?gripper_p1 - gripper  ?peg_p1 - peg )
:precondition (and 
	(gripper_nut_1 ?gripper_p1 ?nut_p1)
	(gripper_peg_0 ?gripper_p1 ?peg_p1)
	(nut_peg_1 ?nut_p1 ?peg_p1)
	(clear3_gripper_nut_2 ?gripper_p1) 
	(clear3_gripper_nut_3 ?gripper_p1) 
) 
:effect (and 
 	(gripper_nut_0 ?gripper_p1 ?nut_p1) 
	(nut_peg_0 ?nut_p1 ?peg_p1) 
	(not (gripper_nut_1 ?gripper_p1 ?nut_p1))
	(not (gripper_nut_2 ?gripper_p1 ?nut_p1))
	(not (gripper_nut_3 ?gripper_p1 ?nut_p1))
	(not (nut_peg_1 ?nut_p1 ?peg_p1))
	(not (nut_peg_2 ?nut_p1 ?peg_p1))
	(clear3_gripper_nut_1 ?gripper_p1) 
 ) 
)

(:action a4 
:parameters ( ?nut_p1 - nut  ?gripper_p1 - gripper  ?peg_p1 - peg )
:precondition (and 
	(gripper_nut_2 ?gripper_p1 ?nut_p1)
	(gripper_peg_0 ?gripper_p1 ?peg_p1)
	(nut_peg_0 ?nut_p1 ?peg_p1)
	(clear3_gripper_nut_1 ?gripper_p1) 
	(clear3_gripper_nut_3 ?gripper_p1) 
) 
:effect (and 
 	(gripper_nut_3 ?gripper_p1 ?nut_p1) 
	(nut_peg_1 ?nut_p1 ?peg_p1) 
	(not (gripper_nut_0 ?gripper_p1 ?nut_p1))
	(not (gripper_nut_1 ?gripper_p1 ?nut_p1))
	(not (gripper_nut_2 ?gripper_p1 ?nut_p1))
	(not (nut_peg_0 ?nut_p1 ?peg_p1))
	(not (nut_peg_2 ?nut_p1 ?peg_p1))
	(clear3_gripper_nut_2 ?gripper_p1) 
	(not (clear3_gripper_nut_3 ?gripper_p1)) 
 ) 
)

(:action a5 
:parameters ( ?nut_p1 - nut  ?gripper_extra_p1 - gripper  ?peg_p1 - peg )
:precondition (and 
	(gripper_peg_0 ?gripper_extra_p1 ?peg_p1)
	(nut_peg_1 ?nut_p1 ?peg_p1)
) 
:effect (and 
 	(nut_peg_2 ?nut_p1 ?peg_p1) 
	(not (nut_peg_0 ?nut_p1 ?peg_p1))
	(not (nut_peg_1 ?nut_p1 ?peg_p1))
 ) 
)

(:action a6 
:parameters ( ?nut_p1 - nut  ?gripper_p1 - gripper  ?peg_p1 - peg )
:precondition (and 
	(gripper_nut_3 ?gripper_p1 ?nut_p1)
	(gripper_peg_0 ?gripper_p1 ?peg_p1)
	(nut_peg_1 ?nut_p1 ?peg_p1)
	(clear3_gripper_nut_1 ?gripper_p1) 
	(clear3_gripper_nut_2 ?gripper_p1) 
) 
:effect (and 
 	(gripper_nut_0 ?gripper_p1 ?nut_p1) 
	(nut_peg_0 ?nut_p1 ?peg_p1) 
	(not (gripper_nut_1 ?gripper_p1 ?nut_p1))
	(not (gripper_nut_2 ?gripper_p1 ?nut_p1))
	(not (gripper_nut_3 ?gripper_p1 ?nut_p1))
	(not (nut_peg_1 ?nut_p1 ?peg_p1))
	(not (nut_peg_2 ?nut_p1 ?peg_p1))
	(clear3_gripper_nut_3 ?gripper_p1) 
 ) 
)

(:action a7 
:parameters ( ?nut_p1 - nut  ?gripper_p1 - gripper  ?peg_p1 - peg )
:precondition (and 
	(gripper_nut_1 ?gripper_p1 ?nut_p1)
	(gripper_peg_0 ?gripper_p1 ?peg_p1)
	(nut_peg_2 ?nut_p1 ?peg_p1)
	(clear3_gripper_nut_2 ?gripper_p1) 
	(clear3_gripper_nut_3 ?gripper_p1) 
) 
:effect (and 
 	(gripper_nut_0 ?gripper_p1 ?nut_p1) 
	(nut_peg_1 ?nut_p1 ?peg_p1) 
	(not (gripper_nut_1 ?gripper_p1 ?nut_p1))
	(not (gripper_nut_2 ?gripper_p1 ?nut_p1))
	(not (gripper_nut_3 ?gripper_p1 ?nut_p1))
	(not (nut_peg_0 ?nut_p1 ?peg_p1))
	(not (nut_peg_2 ?nut_p1 ?peg_p1))
	(clear3_gripper_nut_1 ?gripper_p1) 
 ) 
)

(:action a8 
:parameters ( ?nut_p1 - nut  ?gripper_p1 - gripper )
:precondition (and 
	(gripper_nut_0 ?gripper_p1 ?nut_p1)
	(clear3_gripper_nut_1 ?gripper_p1) 
	(clear3_gripper_nut_2 ?gripper_p1) 
	(clear3_gripper_nut_3 ?gripper_p1) 
) 
:effect (and 
 	(gripper_nut_3 ?gripper_p1 ?nut_p1) 
	(not (gripper_nut_0 ?gripper_p1 ?nut_p1))
	(not (gripper_nut_1 ?gripper_p1 ?nut_p1))
	(not (gripper_nut_2 ?gripper_p1 ?nut_p1))
	(not (clear3_gripper_nut_3 ?gripper_p1)) 
 ) 
)

(:action a9 
:parameters ( ?nut_p1 - nut  ?gripper_p1 - gripper )
:precondition (and 
	(gripper_nut_3 ?gripper_p1 ?nut_p1)
	(clear3_gripper_nut_1 ?gripper_p1) 
	(clear3_gripper_nut_2 ?gripper_p1) 
) 
:effect (and 
 	(gripper_nut_0 ?gripper_p1 ?nut_p1) 
	(not (gripper_nut_1 ?gripper_p1 ?nut_p1))
	(not (gripper_nut_2 ?gripper_p1 ?nut_p1))
	(not (gripper_nut_3 ?gripper_p1 ?nut_p1))
	(clear3_gripper_nut_3 ?gripper_p1) 
 ) 
)

(:action a10 
:parameters ( ?nut_p1 - nut  ?gripper_p1 - gripper )
:precondition (and 
	(gripper_nut_1 ?gripper_p1 ?nut_p1)
	(clear3_gripper_nut_2 ?gripper_p1) 
	(clear3_gripper_nut_3 ?gripper_p1) 
) 
:effect (and 
 	(gripper_nut_0 ?gripper_p1 ?nut_p1) 
	(not (gripper_nut_1 ?gripper_p1 ?nut_p1))
	(not (gripper_nut_2 ?gripper_p1 ?nut_p1))
	(not (gripper_nut_3 ?gripper_p1 ?nut_p1))
	(clear3_gripper_nut_1 ?gripper_p1) 
 ) 
)

(:action a11 
:parameters ( ?nut_p1 - nut  ?gripper_extra_p1 - gripper  ?peg_p1 - peg )
:precondition (and 
	(gripper_peg_0 ?gripper_extra_p1 ?peg_p1)
	(nut_peg_1 ?nut_p1 ?peg_p1)
) 
:effect (and 
 	(nut_peg_2 ?nut_p1 ?peg_p1) 
	(not (nut_peg_0 ?nut_p1 ?peg_p1))
	(not (nut_peg_1 ?nut_p1 ?peg_p1))
 ) 
)

(:action a12 
:parameters ( ?nut_p1 - nut  ?peg_extra_p1 - peg  ?gripper_p1 - gripper )
:precondition (and 
	(gripper_nut_0 ?gripper_p1 ?nut_p1)
	(nut_peg_0 ?nut_p1 ?peg_extra_p1)
	(clear3_gripper_nut_1 ?gripper_p1) 
	(clear3_gripper_nut_2 ?gripper_p1) 
	(clear3_gripper_nut_3 ?gripper_p1) 
) 
:effect (and 
 	(gripper_nut_1 ?gripper_p1 ?nut_p1) 
	(not (gripper_nut_0 ?gripper_p1 ?nut_p1))
	(not (gripper_nut_2 ?gripper_p1 ?nut_p1))
	(not (gripper_nut_3 ?gripper_p1 ?nut_p1))
	(not (clear3_gripper_nut_1 ?gripper_p1)) 
 ) 
)

(:action a13 
:parameters ( ?nut_p1 - nut  ?peg_extra_p1 - peg  ?gripper_p1 - gripper )
:precondition (and 
	(gripper_nut_0 ?gripper_p1 ?nut_p1)
	(nut_peg_0 ?nut_p1 ?peg_extra_p1)
	(clear3_gripper_nut_1 ?gripper_p1) 
	(clear3_gripper_nut_2 ?gripper_p1) 
	(clear3_gripper_nut_3 ?gripper_p1) 
) 
:effect (and 
 	(gripper_nut_2 ?gripper_p1 ?nut_p1) 
	(not (gripper_nut_0 ?gripper_p1 ?nut_p1))
	(not (gripper_nut_1 ?gripper_p1 ?nut_p1))
	(not (gripper_nut_3 ?gripper_p1 ?nut_p1))
	(not (clear3_gripper_nut_2 ?gripper_p1)) 
 ) 
)

(:action a14 
:parameters ( ?nut_p1 - nut  ?gripper_p1 - gripper )
:precondition (and 
	(gripper_nut_2 ?gripper_p1 ?nut_p1)
	(clear3_gripper_nut_1 ?gripper_p1) 
	(clear3_gripper_nut_3 ?gripper_p1) 
) 
:effect (and 
 	(gripper_nut_0 ?gripper_p1 ?nut_p1) 
	(not (gripper_nut_1 ?gripper_p1 ?nut_p1))
	(not (gripper_nut_2 ?gripper_p1 ?nut_p1))
	(not (gripper_nut_3 ?gripper_p1 ?nut_p1))
	(clear3_gripper_nut_2 ?gripper_p1) 
 ) 
)

(:action a15 
:parameters ( ?nut_p1 - nut  ?gripper_p1 - gripper  ?peg_p1 - peg )
:precondition (and 
	(gripper_nut_1 ?gripper_p1 ?nut_p1)
	(gripper_peg_0 ?gripper_p1 ?peg_p1)
	(nut_peg_0 ?nut_p1 ?peg_p1)
	(clear3_gripper_nut_2 ?gripper_p1) 
	(clear3_gripper_nut_3 ?gripper_p1) 
) 
:effect (and 
 	(gripper_nut_0 ?gripper_p1 ?nut_p1) 
	(nut_peg_1 ?nut_p1 ?peg_p1) 
	(not (gripper_nut_1 ?gripper_p1 ?nut_p1))
	(not (gripper_nut_2 ?gripper_p1 ?nut_p1))
	(not (gripper_nut_3 ?gripper_p1 ?nut_p1))
	(not (nut_peg_0 ?nut_p1 ?peg_p1))
	(not (nut_peg_2 ?nut_p1 ?peg_p1))
	(clear3_gripper_nut_1 ?gripper_p1) 
 ) 
)

(:action a16 
:parameters ( ?nut_p1 - nut  ?gripper_extra_p1 - gripper  ?peg_p1 - peg )
:precondition (and 
	(gripper_peg_0 ?gripper_extra_p1 ?peg_p1)
	(nut_peg_0 ?nut_p1 ?peg_p1)
) 
:effect (and 
 	(nut_peg_1 ?nut_p1 ?peg_p1) 
	(not (nut_peg_0 ?nut_p1 ?peg_p1))
	(not (nut_peg_2 ?nut_p1 ?peg_p1))
 ) 
)

(:action a17 
:parameters ( ?nut_p1 - nut  ?gripper_p1 - gripper  ?peg_p1 - peg )
:precondition (and 
	(gripper_nut_1 ?gripper_p1 ?nut_p1)
	(gripper_peg_0 ?gripper_p1 ?peg_p1)
	(nut_peg_2 ?nut_p1 ?peg_p1)
	(clear3_gripper_nut_2 ?gripper_p1) 
	(clear3_gripper_nut_3 ?gripper_p1) 
) 
:effect (and 
 	(gripper_nut_0 ?gripper_p1 ?nut_p1) 
	(nut_peg_0 ?nut_p1 ?peg_p1) 
	(not (gripper_nut_1 ?gripper_p1 ?nut_p1))
	(not (gripper_nut_2 ?gripper_p1 ?nut_p1))
	(not (gripper_nut_3 ?gripper_p1 ?nut_p1))
	(not (nut_peg_1 ?nut_p1 ?peg_p1))
	(not (nut_peg_2 ?nut_p1 ?peg_p1))
	(clear3_gripper_nut_1 ?gripper_p1) 
 ) 
)

(:action a18 
:parameters ( ?nut_p1 - nut  ?gripper_p1 - gripper  ?peg_p1 - peg )
:precondition (and 
	(gripper_nut_3 ?gripper_p1 ?nut_p1)
	(gripper_peg_0 ?gripper_p1 ?peg_p1)
	(nut_peg_1 ?nut_p1 ?peg_p1)
	(clear3_gripper_nut_1 ?gripper_p1) 
	(clear3_gripper_nut_2 ?gripper_p1) 
) 
:effect (and 
 	(gripper_nut_0 ?gripper_p1 ?nut_p1) 
	(nut_peg_2 ?nut_p1 ?peg_p1) 
	(not (gripper_nut_1 ?gripper_p1 ?nut_p1))
	(not (gripper_nut_2 ?gripper_p1 ?nut_p1))
	(not (gripper_nut_3 ?gripper_p1 ?nut_p1))
	(not (nut_peg_0 ?nut_p1 ?peg_p1))
	(not (nut_peg_1 ?nut_p1 ?peg_p1))
	(clear3_gripper_nut_3 ?gripper_p1) 
 ) 
)

(:action a19 
:parameters ( ?nut_p1 - nut  ?gripper_extra_p1 - gripper  ?peg_p1 - peg )
:precondition (and 
	(gripper_peg_0 ?gripper_extra_p1 ?peg_p1)
	(nut_peg_0 ?nut_p1 ?peg_p1)
) 
:effect (and 
 	(nut_peg_1 ?nut_p1 ?peg_p1) 
	(nut_peg_2 ?nut_p1 ?peg_p1) 
	(not (nut_peg_0 ?nut_p1 ?peg_p1))
	(not (nut_peg_1 ?nut_p1 ?peg_p1))
	(not (nut_peg_2 ?nut_p1 ?peg_p1))
 ) 
)

(:action a20 
:parameters ( ?nut_p1 - nut  ?gripper_p1 - gripper  ?peg_p1 - peg )
:precondition (and 
	(gripper_nut_1 ?gripper_p1 ?nut_p1)
	(gripper_peg_0 ?gripper_p1 ?peg_p1)
	(nut_peg_1 ?nut_p1 ?peg_p1)
	(clear3_gripper_nut_2 ?gripper_p1) 
	(clear3_gripper_nut_3 ?gripper_p1) 
) 
:effect (and 
 	(gripper_nut_0 ?gripper_p1 ?nut_p1) 
	(nut_peg_2 ?nut_p1 ?peg_p1) 
	(not (gripper_nut_1 ?gripper_p1 ?nut_p1))
	(not (gripper_nut_2 ?gripper_p1 ?nut_p1))
	(not (gripper_nut_3 ?gripper_p1 ?nut_p1))
	(not (nut_peg_0 ?nut_p1 ?peg_p1))
	(not (nut_peg_1 ?nut_p1 ?peg_p1))
	(clear3_gripper_nut_1 ?gripper_p1) 
 ) 
)

(:action a21 
:parameters ( ?nut_p1 - nut  ?gripper_p1 - gripper  ?peg_p1 - peg )
:precondition (and 
	(gripper_nut_3 ?gripper_p1 ?nut_p1)
	(gripper_peg_0 ?gripper_p1 ?peg_p1)
	(nut_peg_0 ?nut_p1 ?peg_p1)
	(clear3_gripper_nut_1 ?gripper_p1) 
	(clear3_gripper_nut_2 ?gripper_p1) 
) 
:effect (and 
 	(gripper_nut_0 ?gripper_p1 ?nut_p1) 
	(nut_peg_2 ?nut_p1 ?peg_p1) 
	(not (gripper_nut_1 ?gripper_p1 ?nut_p1))
	(not (gripper_nut_2 ?gripper_p1 ?nut_p1))
	(not (gripper_nut_3 ?gripper_p1 ?nut_p1))
	(not (nut_peg_0 ?nut_p1 ?peg_p1))
	(not (nut_peg_1 ?nut_p1 ?peg_p1))
	(clear3_gripper_nut_3 ?gripper_p1) 
 ) 
)

(:action a22 
:parameters ( ?nut_p1 - nut  ?gripper_extra_p1 - gripper  ?peg_p1 - peg )
:precondition (and 
	(gripper_peg_0 ?gripper_extra_p1 ?peg_p1)
	(nut_peg_1 ?nut_p1 ?peg_p1)
	(nut_peg_2 ?nut_p1 ?peg_p1)
) 
:effect (and 
 	(not (nut_peg_1 ?nut_p1 ?peg_p1))
 ) 
)

(:action a23 
:parameters ( ?nut_p1 - nut  ?gripper_extra_p1 - gripper  ?peg_p1 - peg )
:precondition (and 
	(gripper_nut_0 ?gripper_extra_p1 ?nut_p1)
	(gripper_peg_0 ?gripper_extra_p1 ?peg_p1)
	(nut_peg_1 ?nut_p1 ?peg_p1)
	(nut_peg_2 ?nut_p1 ?peg_p1)
) 
:effect (and 
 	(nut_peg_0 ?nut_p1 ?peg_p1) 
	(not (nut_peg_1 ?nut_p1 ?peg_p1))
	(not (nut_peg_2 ?nut_p1 ?peg_p1))
 ) 
)

(:action a24 
:parameters ( ?nut_p1 - nut  ?gripper_p1 - gripper  ?peg_p1 - peg )
:precondition (and 
	(gripper_nut_3 ?gripper_p1 ?nut_p1)
	(gripper_peg_0 ?gripper_p1 ?peg_p1)
	(nut_peg_1 ?nut_p1 ?peg_p1)
	(nut_peg_2 ?nut_p1 ?peg_p1)
	(clear3_gripper_nut_1 ?gripper_p1) 
	(clear3_gripper_nut_2 ?gripper_p1) 
) 
:effect (and 
 	(gripper_nut_0 ?gripper_p1 ?nut_p1) 
	(nut_peg_0 ?nut_p1 ?peg_p1) 
	(not (gripper_nut_1 ?gripper_p1 ?nut_p1))
	(not (gripper_nut_2 ?gripper_p1 ?nut_p1))
	(not (gripper_nut_3 ?gripper_p1 ?nut_p1))
	(not (nut_peg_1 ?nut_p1 ?peg_p1))
	(not (nut_peg_2 ?nut_p1 ?peg_p1))
	(clear3_gripper_nut_3 ?gripper_p1) 
 ) 
)

(:action a25 
:parameters ( ?nut_p1 - nut  ?gripper_p1 - gripper  ?peg_p1 - peg )
:precondition (and 
	(gripper_nut_0 ?gripper_p1 ?nut_p1)
	(gripper_peg_0 ?gripper_p1 ?peg_p1)
	(nut_peg_1 ?nut_p1 ?peg_p1)
	(clear3_gripper_nut_1 ?gripper_p1) 
	(clear3_gripper_nut_2 ?gripper_p1) 
	(clear3_gripper_nut_3 ?gripper_p1) 
) 
:effect (and 
 	(gripper_nut_1 ?gripper_p1 ?nut_p1) 
	(nut_peg_2 ?nut_p1 ?peg_p1) 
	(not (gripper_nut_0 ?gripper_p1 ?nut_p1))
	(not (gripper_nut_2 ?gripper_p1 ?nut_p1))
	(not (gripper_nut_3 ?gripper_p1 ?nut_p1))
	(not (nut_peg_0 ?nut_p1 ?peg_p1))
	(not (nut_peg_1 ?nut_p1 ?peg_p1))
	(not (clear3_gripper_nut_1 ?gripper_p1)) 
 ) 
)

(:action a26 
:parameters ( ?nut_p1 - nut  ?gripper_extra_p1 - gripper  ?peg_p1 - peg )
:precondition (and 
	(gripper_peg_0 ?gripper_extra_p1 ?peg_p1)
	(nut_peg_1 ?nut_p1 ?peg_p1)
) 
:effect (and 
 	(nut_peg_0 ?nut_p1 ?peg_p1) 
	(not (nut_peg_1 ?nut_p1 ?peg_p1))
	(not (nut_peg_2 ?nut_p1 ?peg_p1))
 ) 
)

(:action a27 
:parameters ( ?nut_p1 - nut  ?gripper_p1 - gripper  ?peg_p1 - peg )
:precondition (and 
	(gripper_nut_0 ?gripper_p1 ?nut_p1)
	(gripper_peg_0 ?gripper_p1 ?peg_p1)
	(nut_peg_1 ?nut_p1 ?peg_p1)
	(clear3_gripper_nut_1 ?gripper_p1) 
	(clear3_gripper_nut_2 ?gripper_p1) 
	(clear3_gripper_nut_3 ?gripper_p1) 
) 
:effect (and 
 	(gripper_nut_2 ?gripper_p1 ?nut_p1) 
	(nut_peg_0 ?nut_p1 ?peg_p1) 
	(not (gripper_nut_0 ?gripper_p1 ?nut_p1))
	(not (gripper_nut_1 ?gripper_p1 ?nut_p1))
	(not (gripper_nut_3 ?gripper_p1 ?nut_p1))
	(not (nut_peg_1 ?nut_p1 ?peg_p1))
	(not (nut_peg_2 ?nut_p1 ?peg_p1))
	(not (clear3_gripper_nut_2 ?gripper_p1)) 
 ) 
)

(:action a28 
:parameters ( ?nut_p1 - nut  ?gripper_extra_p1 - gripper  ?peg_p1 - peg )
:precondition (and 
	(gripper_peg_0 ?gripper_extra_p1 ?peg_p1)
	(nut_peg_0 ?nut_p1 ?peg_p1)
) 
:effect (and 
 	(nut_peg_2 ?nut_p1 ?peg_p1) 
	(not (nut_peg_0 ?nut_p1 ?peg_p1))
	(not (nut_peg_1 ?nut_p1 ?peg_p1))
 ) 
)

(:action a29 
:parameters ( ?nut_p1 - nut  ?gripper_p1 - gripper  ?peg_p1 - peg )
:precondition (and 
	(gripper_nut_3 ?gripper_p1 ?nut_p1)
	(gripper_peg_0 ?gripper_p1 ?peg_p1)
	(nut_peg_1 ?nut_p1 ?peg_p1)
	(clear3_gripper_nut_1 ?gripper_p1) 
	(clear3_gripper_nut_2 ?gripper_p1) 
) 
:effect (and 
 	(gripper_nut_0 ?gripper_p1 ?nut_p1) 
	(nut_peg_2 ?nut_p1 ?peg_p1) 
	(not (gripper_nut_1 ?gripper_p1 ?nut_p1))
	(not (gripper_nut_2 ?gripper_p1 ?nut_p1))
	(not (gripper_nut_3 ?gripper_p1 ?nut_p1))
	(not (nut_peg_0 ?nut_p1 ?peg_p1))
	(not (nut_peg_1 ?nut_p1 ?peg_p1))
	(clear3_gripper_nut_3 ?gripper_p1) 
 ) 
)

(:action a30 
:parameters ( ?nut_p1 - nut  ?gripper_p1 - gripper  ?peg_p1 - peg )
:precondition (and 
	(gripper_nut_1 ?gripper_p1 ?nut_p1)
	(gripper_peg_0 ?gripper_p1 ?peg_p1)
	(nut_peg_1 ?nut_p1 ?peg_p1)
	(nut_peg_2 ?nut_p1 ?peg_p1)
	(clear3_gripper_nut_2 ?gripper_p1) 
	(clear3_gripper_nut_3 ?gripper_p1) 
) 
:effect (and 
 	(gripper_nut_0 ?gripper_p1 ?nut_p1) 
	(not (gripper_nut_1 ?gripper_p1 ?nut_p1))
	(not (gripper_nut_2 ?gripper_p1 ?nut_p1))
	(not (gripper_nut_3 ?gripper_p1 ?nut_p1))
	(not (nut_peg_2 ?nut_p1 ?peg_p1))
	(clear3_gripper_nut_1 ?gripper_p1) 
 ) 
)

(:action a31 
:parameters ( ?nut_p1 - nut  ?gripper_p1 - gripper  ?peg_p1 - peg )
:precondition (and 
	(gripper_nut_0 ?gripper_p1 ?nut_p1)
	(gripper_peg_0 ?gripper_p1 ?peg_p1)
	(nut_peg_0 ?nut_p1 ?peg_p1)
	(clear3_gripper_nut_1 ?gripper_p1) 
	(clear3_gripper_nut_2 ?gripper_p1) 
	(clear3_gripper_nut_3 ?gripper_p1) 
) 
:effect (and 
 	(gripper_nut_1 ?gripper_p1 ?nut_p1) 
	(nut_peg_1 ?nut_p1 ?peg_p1) 
	(not (gripper_nut_0 ?gripper_p1 ?nut_p1))
	(not (gripper_nut_2 ?gripper_p1 ?nut_p1))
	(not (gripper_nut_3 ?gripper_p1 ?nut_p1))
	(not (nut_peg_0 ?nut_p1 ?peg_p1))
	(not (nut_peg_2 ?nut_p1 ?peg_p1))
	(not (clear3_gripper_nut_1 ?gripper_p1)) 
 ) 
)

(:action a32 
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

(:action a33 
:parameters ( ?nut_p1 - nut  ?gripper_p1 - gripper  ?peg_p1 - peg )
:precondition (and 
	(gripper_nut_3 ?gripper_p1 ?nut_p1)
	(gripper_peg_0 ?gripper_p1 ?peg_p1)
	(nut_peg_1 ?nut_p1 ?peg_p1)
	(nut_peg_2 ?nut_p1 ?peg_p1)
	(clear3_gripper_nut_1 ?gripper_p1) 
	(clear3_gripper_nut_2 ?gripper_p1) 
) 
:effect (and 
 	(gripper_nut_0 ?gripper_p1 ?nut_p1) 
	(not (gripper_nut_1 ?gripper_p1 ?nut_p1))
	(not (gripper_nut_2 ?gripper_p1 ?nut_p1))
	(not (gripper_nut_3 ?gripper_p1 ?nut_p1))
	(not (nut_peg_1 ?nut_p1 ?peg_p1))
	(clear3_gripper_nut_3 ?gripper_p1) 
 ) 
)

(:action a34 
:parameters ( ?nut_p1 - nut  ?gripper_p1 - gripper )
:precondition (and 
	(gripper_nut_3 ?gripper_p1 ?nut_p1)
	(clear3_gripper_nut_1 ?gripper_p1) 
	(clear3_gripper_nut_2 ?gripper_p1) 
) 
:effect (and 
 	(gripper_nut_2 ?gripper_p1 ?nut_p1) 
	(not (gripper_nut_0 ?gripper_p1 ?nut_p1))
	(not (gripper_nut_1 ?gripper_p1 ?nut_p1))
	(not (gripper_nut_3 ?gripper_p1 ?nut_p1))
	(clear3_gripper_nut_3 ?gripper_p1) 
	(not (clear3_gripper_nut_2 ?gripper_p1)) 
 ) 
)

(:action a35 
:parameters ( ?nut_p1 - nut  ?gripper_extra_p1 - gripper  ?peg_p1 - peg )
:precondition (and 
	(gripper_nut_0 ?gripper_extra_p1 ?nut_p1)
	(gripper_peg_0 ?gripper_extra_p1 ?peg_p1)
	(nut_peg_1 ?nut_p1 ?peg_p1)
	(nut_peg_2 ?nut_p1 ?peg_p1)
) 
:effect (and 
 	(not (nut_peg_2 ?nut_p1 ?peg_p1))
 ) 
)

(:action a36 
:parameters ( ?nut_p1 - nut  ?gripper_p1 - gripper  ?peg_p1 - peg )
:precondition (and 
	(gripper_nut_1 ?gripper_p1 ?nut_p1)
	(gripper_peg_0 ?gripper_p1 ?peg_p1)
	(nut_peg_1 ?nut_p1 ?peg_p1)
	(clear3_gripper_nut_2 ?gripper_p1) 
	(clear3_gripper_nut_3 ?gripper_p1) 
) 
:effect (and 
 	(gripper_nut_0 ?gripper_p1 ?nut_p1) 
	(nut_peg_2 ?nut_p1 ?peg_p1) 
	(not (gripper_nut_1 ?gripper_p1 ?nut_p1))
	(not (gripper_nut_2 ?gripper_p1 ?nut_p1))
	(not (gripper_nut_3 ?gripper_p1 ?nut_p1))
	(not (nut_peg_0 ?nut_p1 ?peg_p1))
	(not (nut_peg_1 ?nut_p1 ?peg_p1))
	(clear3_gripper_nut_1 ?gripper_p1) 
 ) 
)

(:action a37 
:parameters ( ?nut_p1 - nut  ?gripper_p1 - gripper  ?peg_p1 - peg )
:precondition (and 
	(gripper_nut_3 ?gripper_p1 ?nut_p1)
	(gripper_peg_0 ?gripper_p1 ?peg_p1)
	(nut_peg_0 ?nut_p1 ?peg_p1)
	(clear3_gripper_nut_1 ?gripper_p1) 
	(clear3_gripper_nut_2 ?gripper_p1) 
) 
:effect (and 
 	(gripper_nut_0 ?gripper_p1 ?nut_p1) 
	(nut_peg_1 ?nut_p1 ?peg_p1) 
	(nut_peg_2 ?nut_p1 ?peg_p1) 
	(not (gripper_nut_1 ?gripper_p1 ?nut_p1))
	(not (gripper_nut_2 ?gripper_p1 ?nut_p1))
	(not (gripper_nut_3 ?gripper_p1 ?nut_p1))
	(not (nut_peg_0 ?nut_p1 ?peg_p1))
	(not (nut_peg_1 ?nut_p1 ?peg_p1))
	(not (nut_peg_2 ?nut_p1 ?peg_p1))
	(clear3_gripper_nut_3 ?gripper_p1) 
 ) 
)


)