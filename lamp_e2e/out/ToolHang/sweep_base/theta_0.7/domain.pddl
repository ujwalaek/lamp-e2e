(define (domain ToolHang)
(:requirements :strips :typing :equality :conditional-effects :existential-preconditions :universal-preconditions)
(:types 
	frame
	gripper
	stand
	tool
)

(:constants 
)

(:predicates 
	(gripper_frame_0 ?x - gripper ?y - frame)
	(gripper_frame_1 ?x - gripper ?y - frame)
	(gripper_stand_0 ?x - gripper ?y - stand)
	(gripper_tool_0 ?x - gripper ?y - tool)
	(gripper_tool_1 ?x - gripper ?y - tool)
	(frame_stand_0 ?x - frame ?y - stand)
	(frame_stand_1 ?x - frame ?y - stand)
	(frame_tool_0 ?x - frame ?y - tool)
	(frame_tool_1 ?x - frame ?y - tool)
	(frame_tool_2 ?x - frame ?y - tool)
	(frame_tool_3 ?x - frame ?y - tool)
	(stand_tool_0 ?x - stand ?y - tool)
	(stand_tool_1 ?x - stand ?y - tool)
	(stand_tool_2 ?x - stand ?y - tool)
	(clear3_gripper_tool_1 ?x - gripper)
	(clear3_gripper_frame_1 ?x - gripper)
)

(:action a1 
:parameters ( ?stand_p1 - stand  ?gripper_extra_p1 - gripper  ?tool_p1 - tool )
:precondition (and 
	(gripper_stand_0 ?gripper_extra_p1 ?stand_p1)
	(stand_tool_0 ?stand_p1 ?tool_p1)
) 
:effect (and 
 	(stand_tool_1 ?stand_p1 ?tool_p1) 
	(not (stand_tool_0 ?stand_p1 ?tool_p1))
	(not (stand_tool_2 ?stand_p1 ?tool_p1))
 ) 
)

(:action a2 
:parameters ( ?frame_p1 - frame  ?stand_p1 - stand  ?gripper_extra_p1 - gripper  ?tool_p1 - tool )
:precondition (and 
	(frame_stand_0 ?frame_p1 ?stand_p1)
	(frame_tool_1 ?frame_p1 ?tool_p1)
	(gripper_frame_0 ?gripper_extra_p1 ?frame_p1)
	(gripper_stand_0 ?gripper_extra_p1 ?stand_p1)
	(gripper_tool_0 ?gripper_extra_p1 ?tool_p1)
) 
:effect (and 
 	(frame_stand_1 ?frame_p1 ?stand_p1) 
	(frame_tool_0 ?frame_p1 ?tool_p1) 
	(not (frame_stand_0 ?frame_p1 ?stand_p1))
	(not (frame_tool_1 ?frame_p1 ?tool_p1))
	(not (frame_tool_2 ?frame_p1 ?tool_p1))
	(not (frame_tool_3 ?frame_p1 ?tool_p1))
 ) 
)

(:action a3 
:parameters ( ?frame_p1 - frame  ?tool_p1 - tool  ?gripper_extra_p1 - gripper )
:precondition (and 
	(frame_tool_1 ?frame_p1 ?tool_p1)
	(gripper_frame_0 ?gripper_extra_p1 ?frame_p1)
) 
:effect (and 
 	(frame_tool_0 ?frame_p1 ?tool_p1) 
	(not (frame_tool_1 ?frame_p1 ?tool_p1))
	(not (frame_tool_2 ?frame_p1 ?tool_p1))
	(not (frame_tool_3 ?frame_p1 ?tool_p1))
 ) 
)

(:action a4 
:parameters ( ?frame_p1 - frame  ?stand_p1 - stand  ?gripper_extra_p1 - gripper  ?tool_p1 - tool )
:precondition (and 
	(frame_stand_1 ?frame_p1 ?stand_p1)
	(frame_tool_3 ?frame_p1 ?tool_p1)
	(gripper_frame_0 ?gripper_extra_p1 ?frame_p1)
	(gripper_stand_0 ?gripper_extra_p1 ?stand_p1)
	(gripper_tool_0 ?gripper_extra_p1 ?tool_p1)
	(stand_tool_1 ?stand_p1 ?tool_p1)
) 
:effect (and 
 	(frame_tool_0 ?frame_p1 ?tool_p1) 
	(stand_tool_0 ?stand_p1 ?tool_p1) 
	(not (frame_tool_1 ?frame_p1 ?tool_p1))
	(not (frame_tool_2 ?frame_p1 ?tool_p1))
	(not (frame_tool_3 ?frame_p1 ?tool_p1))
	(not (stand_tool_1 ?stand_p1 ?tool_p1))
	(not (stand_tool_2 ?stand_p1 ?tool_p1))
 ) 
)

(:action a5 
:parameters ( ?gripper_p1 - gripper  ?frame_p1 - frame )
:precondition (and 
	(gripper_frame_0 ?gripper_p1 ?frame_p1)
	(clear3_gripper_frame_1 ?gripper_p1) 
	(clear3_gripper_tool_1 ?gripper_p1) 
) 
:effect (and 
 	(gripper_frame_1 ?gripper_p1 ?frame_p1) 
	(not (gripper_frame_0 ?gripper_p1 ?frame_p1))
	(not (clear3_gripper_frame_1 ?gripper_p1)) 
 ) 
)

(:action a6 
:parameters ( ?frame_p1 - frame  ?stand_p1 - stand  ?tool_p1 - tool  ?gripper_extra_p1 - gripper )
:precondition (and 
	(frame_stand_1 ?frame_p1 ?stand_p1)
	(frame_tool_2 ?frame_p1 ?tool_p1)
	(gripper_stand_0 ?gripper_extra_p1 ?stand_p1)
	(gripper_tool_0 ?gripper_extra_p1 ?tool_p1)
) 
:effect (and 
 	(frame_stand_0 ?frame_p1 ?stand_p1) 
	(frame_tool_0 ?frame_p1 ?tool_p1) 
	(not (frame_stand_1 ?frame_p1 ?stand_p1))
	(not (frame_tool_1 ?frame_p1 ?tool_p1))
	(not (frame_tool_2 ?frame_p1 ?tool_p1))
	(not (frame_tool_3 ?frame_p1 ?tool_p1))
 ) 
)

(:action a7 
:parameters ( ?frame_p1 - frame  ?stand_p1 - stand  ?gripper_extra_p1 - gripper  ?tool_p1 - tool )
:precondition (and 
	(frame_stand_0 ?frame_p1 ?stand_p1)
	(frame_tool_2 ?frame_p1 ?tool_p1)
	(gripper_frame_0 ?gripper_extra_p1 ?frame_p1)
	(gripper_stand_0 ?gripper_extra_p1 ?stand_p1)
	(gripper_tool_0 ?gripper_extra_p1 ?tool_p1)
) 
:effect (and 
 	(frame_stand_1 ?frame_p1 ?stand_p1) 
	(frame_tool_0 ?frame_p1 ?tool_p1) 
	(not (frame_stand_0 ?frame_p1 ?stand_p1))
	(not (frame_tool_1 ?frame_p1 ?tool_p1))
	(not (frame_tool_2 ?frame_p1 ?tool_p1))
	(not (frame_tool_3 ?frame_p1 ?tool_p1))
 ) 
)

(:action a8 
:parameters ( ?frame_p1 - frame  ?stand_p1 - stand  ?gripper_extra_p1 - gripper  ?tool_p1 - tool )
:precondition (and 
	(frame_stand_0 ?frame_p1 ?stand_p1)
	(frame_tool_0 ?frame_p1 ?tool_p1)
	(gripper_frame_0 ?gripper_extra_p1 ?frame_p1)
	(gripper_stand_0 ?gripper_extra_p1 ?stand_p1)
	(gripper_tool_0 ?gripper_extra_p1 ?tool_p1)
) 
:effect (and 
 	(frame_stand_1 ?frame_p1 ?stand_p1) 
	(frame_tool_1 ?frame_p1 ?tool_p1) 
	(not (frame_stand_0 ?frame_p1 ?stand_p1))
	(not (frame_tool_0 ?frame_p1 ?tool_p1))
	(not (frame_tool_2 ?frame_p1 ?tool_p1))
	(not (frame_tool_3 ?frame_p1 ?tool_p1))
 ) 
)

(:action a9 
:parameters ( ?gripper_p1 - gripper  ?frame_p1 - frame  ?tool_p1 - tool )
:precondition (and 
	(frame_tool_0 ?frame_p1 ?tool_p1)
	(gripper_frame_0 ?gripper_p1 ?frame_p1)
	(gripper_tool_0 ?gripper_p1 ?tool_p1)
	(clear3_gripper_frame_1 ?gripper_p1) 
	(clear3_gripper_tool_1 ?gripper_p1) 
) 
:effect (and 
 	(frame_tool_2 ?frame_p1 ?tool_p1) 
	(gripper_frame_1 ?gripper_p1 ?frame_p1) 
	(not (frame_tool_0 ?frame_p1 ?tool_p1))
	(not (frame_tool_1 ?frame_p1 ?tool_p1))
	(not (frame_tool_3 ?frame_p1 ?tool_p1))
	(not (gripper_frame_0 ?gripper_p1 ?frame_p1))
	(not (clear3_gripper_frame_1 ?gripper_p1)) 
 ) 
)

(:action a10 
:parameters ( ?gripper_p1 - gripper  ?frame_p1 - frame  ?tool_p1 - tool )
:precondition (and 
	(frame_tool_0 ?frame_p1 ?tool_p1)
	(gripper_frame_0 ?gripper_p1 ?frame_p1)
	(gripper_tool_0 ?gripper_p1 ?tool_p1)
	(clear3_gripper_frame_1 ?gripper_p1) 
	(clear3_gripper_tool_1 ?gripper_p1) 
) 
:effect (and 
 	(frame_tool_1 ?frame_p1 ?tool_p1) 
	(gripper_tool_1 ?gripper_p1 ?tool_p1) 
	(not (frame_tool_0 ?frame_p1 ?tool_p1))
	(not (frame_tool_2 ?frame_p1 ?tool_p1))
	(not (frame_tool_3 ?frame_p1 ?tool_p1))
	(not (gripper_tool_0 ?gripper_p1 ?tool_p1))
	(not (clear3_gripper_tool_1 ?gripper_p1)) 
 ) 
)

(:action a11 
:parameters ( ?gripper_p1 - gripper  ?frame_p1 - frame )
:precondition (and 
	(gripper_frame_1 ?gripper_p1 ?frame_p1)
	(clear3_gripper_tool_1 ?gripper_p1) 
) 
:effect (and 
 	(gripper_frame_0 ?gripper_p1 ?frame_p1) 
	(not (gripper_frame_1 ?gripper_p1 ?frame_p1))
	(clear3_gripper_frame_1 ?gripper_p1) 
 ) 
)

(:action a12 
:parameters ( ?gripper_p1 - gripper  ?stand_p1 - stand  ?tool_p1 - tool )
:precondition (and 
	(gripper_stand_0 ?gripper_p1 ?stand_p1)
	(gripper_tool_0 ?gripper_p1 ?tool_p1)
	(stand_tool_0 ?stand_p1 ?tool_p1)
	(clear3_gripper_frame_1 ?gripper_p1) 
	(clear3_gripper_tool_1 ?gripper_p1) 
) 
:effect (and 
 	(gripper_tool_1 ?gripper_p1 ?tool_p1) 
	(stand_tool_1 ?stand_p1 ?tool_p1) 
	(not (gripper_tool_0 ?gripper_p1 ?tool_p1))
	(not (stand_tool_0 ?stand_p1 ?tool_p1))
	(not (stand_tool_2 ?stand_p1 ?tool_p1))
	(not (clear3_gripper_tool_1 ?gripper_p1)) 
 ) 
)

(:action a13 
:parameters ( ?frame_p1 - frame  ?stand_p1 - stand  ?gripper_extra_p1 - gripper )
:precondition (and 
	(frame_stand_0 ?frame_p1 ?stand_p1)
	(gripper_stand_0 ?gripper_extra_p1 ?stand_p1)
) 
:effect (and 
 	(frame_stand_1 ?frame_p1 ?stand_p1) 
	(not (frame_stand_0 ?frame_p1 ?stand_p1))
 ) 
)

(:action a14 
:parameters ( ?gripper_p1 - gripper  ?frame_p1 - frame  ?stand_p1 - stand )
:precondition (and 
	(frame_stand_1 ?frame_p1 ?stand_p1)
	(gripper_frame_1 ?gripper_p1 ?frame_p1)
	(gripper_stand_0 ?gripper_p1 ?stand_p1)
	(clear3_gripper_tool_1 ?gripper_p1) 
) 
:effect (and 
 	(frame_stand_0 ?frame_p1 ?stand_p1) 
	(gripper_frame_0 ?gripper_p1 ?frame_p1) 
	(not (frame_stand_1 ?frame_p1 ?stand_p1))
	(not (gripper_frame_1 ?gripper_p1 ?frame_p1))
	(clear3_gripper_frame_1 ?gripper_p1) 
 ) 
)

(:action a15 
:parameters ( ?gripper_p1 - gripper  ?frame_p1 - frame  ?tool_p1 - tool )
:precondition (and 
	(frame_tool_1 ?frame_p1 ?tool_p1)
	(gripper_frame_0 ?gripper_p1 ?frame_p1)
	(gripper_tool_1 ?gripper_p1 ?tool_p1)
	(clear3_gripper_frame_1 ?gripper_p1) 
) 
:effect (and 
 	(frame_tool_0 ?frame_p1 ?tool_p1) 
	(gripper_tool_0 ?gripper_p1 ?tool_p1) 
	(not (frame_tool_1 ?frame_p1 ?tool_p1))
	(not (frame_tool_2 ?frame_p1 ?tool_p1))
	(not (frame_tool_3 ?frame_p1 ?tool_p1))
	(not (gripper_tool_1 ?gripper_p1 ?tool_p1))
	(clear3_gripper_tool_1 ?gripper_p1) 
 ) 
)

(:action a16 
:parameters ( ?frame_p1 - frame  ?stand_p1 - stand  ?tool_p1 - tool  ?gripper_extra_p1 - gripper )
:precondition (and 
	(frame_tool_1 ?frame_p1 ?tool_p1)
	(gripper_frame_0 ?gripper_extra_p1 ?frame_p1)
	(gripper_stand_0 ?gripper_extra_p1 ?stand_p1)
	(stand_tool_0 ?stand_p1 ?tool_p1)
) 
:effect (and 
 	(frame_tool_0 ?frame_p1 ?tool_p1) 
	(stand_tool_1 ?stand_p1 ?tool_p1) 
	(not (frame_tool_1 ?frame_p1 ?tool_p1))
	(not (frame_tool_2 ?frame_p1 ?tool_p1))
	(not (frame_tool_3 ?frame_p1 ?tool_p1))
	(not (stand_tool_0 ?stand_p1 ?tool_p1))
	(not (stand_tool_2 ?stand_p1 ?tool_p1))
 ) 
)

(:action a17 
:parameters ( ?frame_p1 - frame  ?stand_p1 - stand  ?tool_p1 - tool  ?gripper_extra_p1 - gripper )
:precondition (and 
	(frame_stand_1 ?frame_p1 ?stand_p1)
	(gripper_frame_0 ?gripper_extra_p1 ?frame_p1)
	(gripper_stand_0 ?gripper_extra_p1 ?stand_p1)
	(stand_tool_0 ?stand_p1 ?tool_p1)
) 
:effect (and 
 	(frame_stand_0 ?frame_p1 ?stand_p1) 
	(stand_tool_1 ?stand_p1 ?tool_p1) 
	(not (frame_stand_1 ?frame_p1 ?stand_p1))
	(not (stand_tool_0 ?stand_p1 ?tool_p1))
	(not (stand_tool_2 ?stand_p1 ?tool_p1))
 ) 
)

(:action a18 
:parameters ( ?gripper_p1 - gripper  ?stand_p1 - stand  ?tool_p1 - tool )
:precondition (and 
	(gripper_stand_0 ?gripper_p1 ?stand_p1)
	(gripper_tool_0 ?gripper_p1 ?tool_p1)
	(stand_tool_2 ?stand_p1 ?tool_p1)
	(clear3_gripper_frame_1 ?gripper_p1) 
	(clear3_gripper_tool_1 ?gripper_p1) 
) 
:effect (and 
 	(gripper_tool_1 ?gripper_p1 ?tool_p1) 
	(stand_tool_0 ?stand_p1 ?tool_p1) 
	(not (gripper_tool_0 ?gripper_p1 ?tool_p1))
	(not (stand_tool_1 ?stand_p1 ?tool_p1))
	(not (stand_tool_2 ?stand_p1 ?tool_p1))
	(not (clear3_gripper_tool_1 ?gripper_p1)) 
 ) 
)

(:action a19 
:parameters ( ?frame_p1 - frame  ?gripper_extra_p1 - gripper  ?tool_p1 - tool )
:precondition (and 
	(frame_tool_3 ?frame_p1 ?tool_p1)
	(gripper_frame_0 ?gripper_extra_p1 ?frame_p1)
	(gripper_tool_0 ?gripper_extra_p1 ?tool_p1)
) 
:effect (and 
 	(frame_tool_0 ?frame_p1 ?tool_p1) 
	(not (frame_tool_1 ?frame_p1 ?tool_p1))
	(not (frame_tool_2 ?frame_p1 ?tool_p1))
	(not (frame_tool_3 ?frame_p1 ?tool_p1))
 ) 
)

(:action a20 
:parameters ( ?stand_p1 - stand  ?gripper_extra_p1 - gripper  ?tool_p1 - tool )
:precondition (and 
	(gripper_stand_0 ?gripper_extra_p1 ?stand_p1)
	(stand_tool_2 ?stand_p1 ?tool_p1)
) 
:effect (and 
 	(stand_tool_0 ?stand_p1 ?tool_p1) 
	(not (stand_tool_1 ?stand_p1 ?tool_p1))
	(not (stand_tool_2 ?stand_p1 ?tool_p1))
 ) 
)

(:action a21 
:parameters ( ?frame_p1 - frame  ?tool_p1 - tool  ?gripper_extra_p1 - gripper )
:precondition (and 
	(frame_tool_2 ?frame_p1 ?tool_p1)
	(gripper_tool_0 ?gripper_extra_p1 ?tool_p1)
) 
:effect (and 
 	(frame_tool_0 ?frame_p1 ?tool_p1) 
	(not (frame_tool_1 ?frame_p1 ?tool_p1))
	(not (frame_tool_2 ?frame_p1 ?tool_p1))
	(not (frame_tool_3 ?frame_p1 ?tool_p1))
 ) 
)

(:action a22 
:parameters ( ?frame_p1 - frame  ?stand_p1 - stand  ?gripper_extra_p1 - gripper  ?tool_p1 - tool )
:precondition (and 
	(frame_stand_0 ?frame_p1 ?stand_p1)
	(frame_tool_0 ?frame_p1 ?tool_p1)
	(gripper_frame_0 ?gripper_extra_p1 ?frame_p1)
	(gripper_stand_0 ?gripper_extra_p1 ?stand_p1)
	(gripper_tool_0 ?gripper_extra_p1 ?tool_p1)
	(stand_tool_1 ?stand_p1 ?tool_p1)
) 
:effect (and 
 	(frame_stand_1 ?frame_p1 ?stand_p1) 
	(frame_tool_3 ?frame_p1 ?tool_p1) 
	(stand_tool_0 ?stand_p1 ?tool_p1) 
	(not (frame_stand_0 ?frame_p1 ?stand_p1))
	(not (frame_tool_0 ?frame_p1 ?tool_p1))
	(not (frame_tool_1 ?frame_p1 ?tool_p1))
	(not (frame_tool_2 ?frame_p1 ?tool_p1))
	(not (stand_tool_1 ?stand_p1 ?tool_p1))
	(not (stand_tool_2 ?stand_p1 ?tool_p1))
 ) 
)

(:action a23 
:parameters ( ?frame_p1 - frame  ?stand_p1 - stand  ?gripper_extra_p1 - gripper )
:precondition (and 
	(frame_stand_1 ?frame_p1 ?stand_p1)
	(gripper_stand_0 ?gripper_extra_p1 ?stand_p1)
) 
:effect (and 
 	(frame_stand_0 ?frame_p1 ?stand_p1) 
	(not (frame_stand_1 ?frame_p1 ?stand_p1))
 ) 
)

(:action a24 
:parameters ( ?gripper_p1 - gripper  ?tool_p1 - tool )
:precondition (and 
	(gripper_tool_1 ?gripper_p1 ?tool_p1)
	(clear3_gripper_frame_1 ?gripper_p1) 
) 
:effect (and 
 	(gripper_tool_0 ?gripper_p1 ?tool_p1) 
	(not (gripper_tool_1 ?gripper_p1 ?tool_p1))
	(clear3_gripper_tool_1 ?gripper_p1) 
 ) 
)

(:action a25 
:parameters ( ?frame_p1 - frame  ?stand_p1 - stand  ?gripper_extra_p1 - gripper  ?tool_p1 - tool )
:precondition (and 
	(frame_stand_1 ?frame_p1 ?stand_p1)
	(frame_tool_1 ?frame_p1 ?tool_p1)
	(gripper_frame_0 ?gripper_extra_p1 ?frame_p1)
	(gripper_stand_0 ?gripper_extra_p1 ?stand_p1)
	(stand_tool_1 ?stand_p1 ?tool_p1)
) 
:effect (and 
 	(frame_stand_0 ?frame_p1 ?stand_p1) 
	(frame_tool_0 ?frame_p1 ?tool_p1) 
	(stand_tool_0 ?stand_p1 ?tool_p1) 
	(not (frame_stand_1 ?frame_p1 ?stand_p1))
	(not (frame_tool_1 ?frame_p1 ?tool_p1))
	(not (frame_tool_2 ?frame_p1 ?tool_p1))
	(not (frame_tool_3 ?frame_p1 ?tool_p1))
	(not (stand_tool_1 ?stand_p1 ?tool_p1))
	(not (stand_tool_2 ?stand_p1 ?tool_p1))
 ) 
)

(:action a26 
:parameters ( ?gripper_p1 - gripper  ?stand_p1 - stand  ?tool_p1 - tool )
:precondition (and 
	(gripper_stand_0 ?gripper_p1 ?stand_p1)
	(gripper_tool_1 ?gripper_p1 ?tool_p1)
	(stand_tool_1 ?stand_p1 ?tool_p1)
	(clear3_gripper_frame_1 ?gripper_p1) 
) 
:effect (and 
 	(gripper_tool_0 ?gripper_p1 ?tool_p1) 
	(stand_tool_0 ?stand_p1 ?tool_p1) 
	(not (gripper_tool_1 ?gripper_p1 ?tool_p1))
	(not (stand_tool_1 ?stand_p1 ?tool_p1))
	(not (stand_tool_2 ?stand_p1 ?tool_p1))
	(clear3_gripper_tool_1 ?gripper_p1) 
 ) 
)

(:action a27 
:parameters ( ?gripper_p1 - gripper  ?frame_p1 - frame  ?stand_p1 - stand )
:precondition (and 
	(frame_stand_0 ?frame_p1 ?stand_p1)
	(gripper_frame_0 ?gripper_p1 ?frame_p1)
	(gripper_stand_0 ?gripper_p1 ?stand_p1)
	(clear3_gripper_frame_1 ?gripper_p1) 
	(clear3_gripper_tool_1 ?gripper_p1) 
) 
:effect (and 
 	(frame_stand_1 ?frame_p1 ?stand_p1) 
	(gripper_frame_1 ?gripper_p1 ?frame_p1) 
	(not (frame_stand_0 ?frame_p1 ?stand_p1))
	(not (gripper_frame_0 ?gripper_p1 ?frame_p1))
	(not (clear3_gripper_frame_1 ?gripper_p1)) 
 ) 
)

(:action a28 
:parameters ( ?gripper_p1 - gripper  ?frame_p1 - frame  ?stand_p1 - stand  ?tool_p1 - tool )
:precondition (and 
	(frame_stand_0 ?frame_p1 ?stand_p1)
	(gripper_frame_0 ?gripper_p1 ?frame_p1)
	(gripper_stand_0 ?gripper_p1 ?stand_p1)
	(gripper_tool_1 ?gripper_p1 ?tool_p1)
	(stand_tool_1 ?stand_p1 ?tool_p1)
	(clear3_gripper_frame_1 ?gripper_p1) 
) 
:effect (and 
 	(frame_stand_1 ?frame_p1 ?stand_p1) 
	(gripper_tool_0 ?gripper_p1 ?tool_p1) 
	(not (frame_stand_0 ?frame_p1 ?stand_p1))
	(not (gripper_tool_1 ?gripper_p1 ?tool_p1))
	(clear3_gripper_tool_1 ?gripper_p1) 
 ) 
)

(:action a29 
:parameters ( ?frame_p1 - frame  ?gripper_extra_p1 - gripper  ?tool_p1 - tool )
:precondition (and 
	(frame_tool_0 ?frame_p1 ?tool_p1)
	(gripper_tool_0 ?gripper_extra_p1 ?tool_p1)
) 
:effect (and 
 	(frame_tool_2 ?frame_p1 ?tool_p1) 
	(not (frame_tool_0 ?frame_p1 ?tool_p1))
	(not (frame_tool_1 ?frame_p1 ?tool_p1))
	(not (frame_tool_3 ?frame_p1 ?tool_p1))
 ) 
)

(:action a30 
:parameters ( ?frame_p1 - frame  ?stand_p1 - stand  ?gripper_extra_p1 - gripper  ?tool_p1 - tool )
:precondition (and 
	(frame_tool_0 ?frame_p1 ?tool_p1)
	(gripper_frame_0 ?gripper_extra_p1 ?frame_p1)
	(gripper_stand_0 ?gripper_extra_p1 ?stand_p1)
	(gripper_tool_0 ?gripper_extra_p1 ?tool_p1)
	(stand_tool_1 ?stand_p1 ?tool_p1)
) 
:effect (and 
 	(frame_tool_1 ?frame_p1 ?tool_p1) 
	(stand_tool_0 ?stand_p1 ?tool_p1) 
	(not (frame_tool_0 ?frame_p1 ?tool_p1))
	(not (frame_tool_2 ?frame_p1 ?tool_p1))
	(not (frame_tool_3 ?frame_p1 ?tool_p1))
	(not (stand_tool_1 ?stand_p1 ?tool_p1))
	(not (stand_tool_2 ?stand_p1 ?tool_p1))
 ) 
)

(:action a31 
:parameters ( ?gripper_p1 - gripper  ?frame_p1 - frame  ?tool_p1 - tool )
:precondition (and 
	(frame_tool_2 ?frame_p1 ?tool_p1)
	(gripper_frame_1 ?gripper_p1 ?frame_p1)
	(gripper_tool_0 ?gripper_p1 ?tool_p1)
	(clear3_gripper_tool_1 ?gripper_p1) 
) 
:effect (and 
 	(frame_tool_0 ?frame_p1 ?tool_p1) 
	(gripper_frame_0 ?gripper_p1 ?frame_p1) 
	(not (frame_tool_1 ?frame_p1 ?tool_p1))
	(not (frame_tool_2 ?frame_p1 ?tool_p1))
	(not (frame_tool_3 ?frame_p1 ?tool_p1))
	(not (gripper_frame_1 ?gripper_p1 ?frame_p1))
	(clear3_gripper_frame_1 ?gripper_p1) 
 ) 
)

(:action a32 
:parameters ( ?frame_p1 - frame  ?stand_p1 - stand  ?gripper_extra_p1 - gripper  ?tool_p1 - tool )
:precondition (and 
	(frame_stand_0 ?frame_p1 ?stand_p1)
	(gripper_frame_0 ?gripper_extra_p1 ?frame_p1)
	(gripper_stand_0 ?gripper_extra_p1 ?stand_p1)
	(gripper_tool_0 ?gripper_extra_p1 ?tool_p1)
	(stand_tool_1 ?stand_p1 ?tool_p1)
) 
:effect (and 
 	(frame_stand_1 ?frame_p1 ?stand_p1) 
	(stand_tool_0 ?stand_p1 ?tool_p1) 
	(not (frame_stand_0 ?frame_p1 ?stand_p1))
	(not (stand_tool_1 ?stand_p1 ?tool_p1))
	(not (stand_tool_2 ?stand_p1 ?tool_p1))
 ) 
)

(:action a33 
:parameters ( ?gripper_p1 - gripper  ?frame_p1 - frame  ?stand_p1 - stand  ?tool_p1 - tool )
:precondition (and 
	(frame_stand_0 ?frame_p1 ?stand_p1)
	(frame_tool_2 ?frame_p1 ?tool_p1)
	(gripper_frame_1 ?gripper_p1 ?frame_p1)
	(gripper_stand_0 ?gripper_p1 ?stand_p1)
	(gripper_tool_0 ?gripper_p1 ?tool_p1)
	(stand_tool_0 ?stand_p1 ?tool_p1)
	(clear3_gripper_tool_1 ?gripper_p1) 
) 
:effect (and 
 	(frame_stand_1 ?frame_p1 ?stand_p1) 
	(frame_tool_0 ?frame_p1 ?tool_p1) 
	(gripper_frame_0 ?gripper_p1 ?frame_p1) 
	(not (frame_stand_0 ?frame_p1 ?stand_p1))
	(not (frame_tool_1 ?frame_p1 ?tool_p1))
	(not (frame_tool_2 ?frame_p1 ?tool_p1))
	(not (frame_tool_3 ?frame_p1 ?tool_p1))
	(not (gripper_frame_1 ?gripper_p1 ?frame_p1))
	(clear3_gripper_frame_1 ?gripper_p1) 
 ) 
)

(:action a34 
:parameters ( ?gripper_p1 - gripper  ?stand_p1 - stand  ?tool_p1 - tool )
:precondition (and 
	(gripper_stand_0 ?gripper_p1 ?stand_p1)
	(gripper_tool_1 ?gripper_p1 ?tool_p1)
	(stand_tool_0 ?stand_p1 ?tool_p1)
	(clear3_gripper_frame_1 ?gripper_p1) 
) 
:effect (and 
 	(gripper_tool_0 ?gripper_p1 ?tool_p1) 
	(stand_tool_1 ?stand_p1 ?tool_p1) 
	(not (gripper_tool_1 ?gripper_p1 ?tool_p1))
	(not (stand_tool_0 ?stand_p1 ?tool_p1))
	(not (stand_tool_2 ?stand_p1 ?tool_p1))
	(clear3_gripper_tool_1 ?gripper_p1) 
 ) 
)

(:action a35 
:parameters ( ?frame_p1 - frame  ?stand_p1 - stand  ?gripper_extra_p1 - gripper  ?tool_p1 - tool )
:precondition (and 
	(frame_tool_0 ?frame_p1 ?tool_p1)
	(gripper_frame_0 ?gripper_extra_p1 ?frame_p1)
	(gripper_stand_0 ?gripper_extra_p1 ?stand_p1)
	(stand_tool_0 ?stand_p1 ?tool_p1)
) 
:effect (and 
 	(frame_tool_1 ?frame_p1 ?tool_p1) 
	(stand_tool_1 ?stand_p1 ?tool_p1) 
	(not (frame_tool_0 ?frame_p1 ?tool_p1))
	(not (frame_tool_2 ?frame_p1 ?tool_p1))
	(not (frame_tool_3 ?frame_p1 ?tool_p1))
	(not (stand_tool_0 ?stand_p1 ?tool_p1))
	(not (stand_tool_2 ?stand_p1 ?tool_p1))
 ) 
)

(:action a36 
:parameters ( ?frame_p1 - frame  ?stand_p1 - stand  ?gripper_extra_p1 - gripper  ?tool_p1 - tool )
:precondition (and 
	(frame_stand_0 ?frame_p1 ?stand_p1)
	(frame_tool_0 ?frame_p1 ?tool_p1)
	(gripper_frame_0 ?gripper_extra_p1 ?frame_p1)
	(gripper_stand_0 ?gripper_extra_p1 ?stand_p1)
	(gripper_tool_0 ?gripper_extra_p1 ?tool_p1)
	(stand_tool_0 ?stand_p1 ?tool_p1)
) 
:effect (and 
 	(frame_stand_1 ?frame_p1 ?stand_p1) 
	(stand_tool_2 ?stand_p1 ?tool_p1) 
	(not (frame_stand_0 ?frame_p1 ?stand_p1))
	(not (stand_tool_0 ?stand_p1 ?tool_p1))
	(not (stand_tool_1 ?stand_p1 ?tool_p1))
 ) 
)

(:action a37 
:parameters ( ?frame_p1 - frame  ?stand_p1 - stand  ?gripper_extra_p1 - gripper  ?tool_p1 - tool )
:precondition (and 
	(frame_stand_1 ?frame_p1 ?stand_p1)
	(frame_tool_0 ?frame_p1 ?tool_p1)
	(gripper_frame_0 ?gripper_extra_p1 ?frame_p1)
	(gripper_stand_0 ?gripper_extra_p1 ?stand_p1)
	(gripper_tool_0 ?gripper_extra_p1 ?tool_p1)
) 
:effect (and 
 	(frame_stand_0 ?frame_p1 ?stand_p1) 
	(frame_tool_2 ?frame_p1 ?tool_p1) 
	(not (frame_stand_1 ?frame_p1 ?stand_p1))
	(not (frame_tool_0 ?frame_p1 ?tool_p1))
	(not (frame_tool_1 ?frame_p1 ?tool_p1))
	(not (frame_tool_3 ?frame_p1 ?tool_p1))
 ) 
)

(:action a38 
:parameters ( ?frame_p1 - frame  ?stand_p1 - stand  ?gripper_extra_p1 - gripper  ?tool_p1 - tool )
:precondition (and 
	(frame_stand_0 ?frame_p1 ?stand_p1)
	(frame_tool_0 ?frame_p1 ?tool_p1)
	(gripper_stand_0 ?gripper_extra_p1 ?stand_p1)
	(gripper_tool_0 ?gripper_extra_p1 ?tool_p1)
) 
:effect (and 
 	(frame_stand_1 ?frame_p1 ?stand_p1) 
	(frame_tool_2 ?frame_p1 ?tool_p1) 
	(not (frame_stand_0 ?frame_p1 ?stand_p1))
	(not (frame_tool_0 ?frame_p1 ?tool_p1))
	(not (frame_tool_1 ?frame_p1 ?tool_p1))
	(not (frame_tool_3 ?frame_p1 ?tool_p1))
 ) 
)

(:action a39 
:parameters ( ?gripper_p1 - gripper  ?frame_p1 - frame  ?tool_p1 - tool )
:precondition (and 
	(frame_tool_0 ?frame_p1 ?tool_p1)
	(gripper_frame_0 ?gripper_p1 ?frame_p1)
	(gripper_tool_1 ?gripper_p1 ?tool_p1)
	(clear3_gripper_frame_1 ?gripper_p1) 
) 
:effect (and 
 	(frame_tool_1 ?frame_p1 ?tool_p1) 
	(gripper_tool_0 ?gripper_p1 ?tool_p1) 
	(not (frame_tool_0 ?frame_p1 ?tool_p1))
	(not (frame_tool_2 ?frame_p1 ?tool_p1))
	(not (frame_tool_3 ?frame_p1 ?tool_p1))
	(not (gripper_tool_1 ?gripper_p1 ?tool_p1))
	(clear3_gripper_tool_1 ?gripper_p1) 
 ) 
)

(:action a40 
:parameters ( ?frame_p1 - frame  ?stand_p1 - stand  ?gripper_extra_p1 - gripper  ?tool_p1 - tool )
:precondition (and 
	(frame_stand_1 ?frame_p1 ?stand_p1)
	(gripper_frame_0 ?gripper_extra_p1 ?frame_p1)
	(gripper_stand_0 ?gripper_extra_p1 ?stand_p1)
	(gripper_tool_0 ?gripper_extra_p1 ?tool_p1)
	(stand_tool_1 ?stand_p1 ?tool_p1)
) 
:effect (and 
 	(frame_stand_0 ?frame_p1 ?stand_p1) 
	(stand_tool_0 ?stand_p1 ?tool_p1) 
	(not (frame_stand_1 ?frame_p1 ?stand_p1))
	(not (stand_tool_1 ?stand_p1 ?tool_p1))
	(not (stand_tool_2 ?stand_p1 ?tool_p1))
 ) 
)

(:action a41 
:parameters ( ?frame_p1 - frame  ?gripper_extra_p1 - gripper  ?tool_p1 - tool )
:precondition (and 
	(frame_tool_0 ?frame_p1 ?tool_p1)
	(gripper_frame_0 ?gripper_extra_p1 ?frame_p1)
) 
:effect (and 
 	(frame_tool_1 ?frame_p1 ?tool_p1) 
	(not (frame_tool_0 ?frame_p1 ?tool_p1))
	(not (frame_tool_2 ?frame_p1 ?tool_p1))
	(not (frame_tool_3 ?frame_p1 ?tool_p1))
 ) 
)

(:action a42 
:parameters ( ?frame_p1 - frame  ?stand_p1 - stand  ?gripper_extra_p1 - gripper  ?tool_p1 - tool )
:precondition (and 
	(frame_stand_1 ?frame_p1 ?stand_p1)
	(frame_tool_1 ?frame_p1 ?tool_p1)
	(gripper_frame_0 ?gripper_extra_p1 ?frame_p1)
	(gripper_stand_0 ?gripper_extra_p1 ?stand_p1)
	(gripper_tool_0 ?gripper_extra_p1 ?tool_p1)
) 
:effect (and 
 	(frame_stand_0 ?frame_p1 ?stand_p1) 
	(frame_tool_0 ?frame_p1 ?tool_p1) 
	(not (frame_stand_1 ?frame_p1 ?stand_p1))
	(not (frame_tool_1 ?frame_p1 ?tool_p1))
	(not (frame_tool_2 ?frame_p1 ?tool_p1))
	(not (frame_tool_3 ?frame_p1 ?tool_p1))
 ) 
)

(:action a43 
:parameters ( ?frame_p1 - frame  ?stand_p1 - stand  ?gripper_extra_p1 - gripper  ?tool_p1 - tool )
:precondition (and 
	(frame_stand_1 ?frame_p1 ?stand_p1)
	(frame_tool_3 ?frame_p1 ?tool_p1)
	(gripper_frame_0 ?gripper_extra_p1 ?frame_p1)
	(gripper_stand_0 ?gripper_extra_p1 ?stand_p1)
	(gripper_tool_0 ?gripper_extra_p1 ?tool_p1)
	(stand_tool_0 ?stand_p1 ?tool_p1)
) 
:effect (and 
 	(frame_stand_0 ?frame_p1 ?stand_p1) 
	(frame_tool_0 ?frame_p1 ?tool_p1) 
	(not (frame_stand_1 ?frame_p1 ?stand_p1))
	(not (frame_tool_1 ?frame_p1 ?tool_p1))
	(not (frame_tool_2 ?frame_p1 ?tool_p1))
	(not (frame_tool_3 ?frame_p1 ?tool_p1))
 ) 
)

(:action a44 
:parameters ( ?stand_p1 - stand  ?tool_p1 - tool  ?gripper_extra_p1 - gripper )
:precondition (and 
	(gripper_stand_0 ?gripper_extra_p1 ?stand_p1)
	(stand_tool_1 ?stand_p1 ?tool_p1)
) 
:effect (and 
 	(stand_tool_0 ?stand_p1 ?tool_p1) 
	(not (stand_tool_1 ?stand_p1 ?tool_p1))
	(not (stand_tool_2 ?stand_p1 ?tool_p1))
 ) 
)

(:action a45 
:parameters ( ?stand_p1 - stand  ?tool_p1 - tool  ?gripper_extra_p1 - gripper )
:precondition (and 
	(gripper_stand_0 ?gripper_extra_p1 ?stand_p1)
	(gripper_tool_0 ?gripper_extra_p1 ?tool_p1)
	(stand_tool_0 ?stand_p1 ?tool_p1)
) 
:effect (and 
 	(stand_tool_2 ?stand_p1 ?tool_p1) 
	(not (stand_tool_0 ?stand_p1 ?tool_p1))
	(not (stand_tool_1 ?stand_p1 ?tool_p1))
 ) 
)

(:action a46 
:parameters ( ?gripper_p1 - gripper  ?frame_p1 - frame  ?stand_p1 - stand )
:precondition (and 
	(frame_stand_1 ?frame_p1 ?stand_p1)
	(gripper_frame_0 ?gripper_p1 ?frame_p1)
	(gripper_stand_0 ?gripper_p1 ?stand_p1)
	(clear3_gripper_frame_1 ?gripper_p1) 
	(clear3_gripper_tool_1 ?gripper_p1) 
) 
:effect (and 
 	(frame_stand_0 ?frame_p1 ?stand_p1) 
	(gripper_frame_1 ?gripper_p1 ?frame_p1) 
	(not (frame_stand_1 ?frame_p1 ?stand_p1))
	(not (gripper_frame_0 ?gripper_p1 ?frame_p1))
	(not (clear3_gripper_frame_1 ?gripper_p1)) 
 ) 
)

(:action a47 
:parameters ( ?frame_p1 - frame  ?gripper_extra_p1 - gripper  ?tool_p1 - tool )
:precondition (and 
	(frame_tool_0 ?frame_p1 ?tool_p1)
	(gripper_frame_0 ?gripper_extra_p1 ?frame_p1)
	(gripper_tool_0 ?gripper_extra_p1 ?tool_p1)
) 
:effect (and 
 	(frame_tool_3 ?frame_p1 ?tool_p1) 
	(not (frame_tool_0 ?frame_p1 ?tool_p1))
	(not (frame_tool_1 ?frame_p1 ?tool_p1))
	(not (frame_tool_2 ?frame_p1 ?tool_p1))
 ) 
)

(:action a48 
:parameters ( ?gripper_p1 - gripper  ?tool_p1 - tool )
:precondition (and 
	(gripper_tool_0 ?gripper_p1 ?tool_p1)
	(clear3_gripper_frame_1 ?gripper_p1) 
	(clear3_gripper_tool_1 ?gripper_p1) 
) 
:effect (and 
 	(gripper_tool_1 ?gripper_p1 ?tool_p1) 
	(not (gripper_tool_0 ?gripper_p1 ?tool_p1))
	(not (clear3_gripper_tool_1 ?gripper_p1)) 
 ) 
)

(:action a49 
:parameters ( ?frame_p1 - frame  ?stand_p1 - stand  ?gripper_extra_p1 - gripper  ?tool_p1 - tool )
:precondition (and 
	(frame_stand_1 ?frame_p1 ?stand_p1)
	(frame_tool_0 ?frame_p1 ?tool_p1)
	(gripper_frame_0 ?gripper_extra_p1 ?frame_p1)
	(gripper_stand_0 ?gripper_extra_p1 ?stand_p1)
	(stand_tool_0 ?stand_p1 ?tool_p1)
) 
:effect (and 
 	(frame_stand_0 ?frame_p1 ?stand_p1) 
	(frame_tool_1 ?frame_p1 ?tool_p1) 
	(not (frame_stand_1 ?frame_p1 ?stand_p1))
	(not (frame_tool_0 ?frame_p1 ?tool_p1))
	(not (frame_tool_2 ?frame_p1 ?tool_p1))
	(not (frame_tool_3 ?frame_p1 ?tool_p1))
 ) 
)

(:action a50 
:parameters ( ?gripper_p1 - gripper  ?frame_p1 - frame  ?stand_p1 - stand  ?tool_p1 - tool )
:precondition (and 
	(frame_stand_0 ?frame_p1 ?stand_p1)
	(frame_tool_2 ?frame_p1 ?tool_p1)
	(gripper_frame_0 ?gripper_p1 ?frame_p1)
	(gripper_stand_0 ?gripper_p1 ?stand_p1)
	(gripper_tool_0 ?gripper_p1 ?tool_p1)
	(stand_tool_0 ?stand_p1 ?tool_p1)
	(clear3_gripper_frame_1 ?gripper_p1) 
	(clear3_gripper_tool_1 ?gripper_p1) 
) 
:effect (and 
 	(frame_stand_1 ?frame_p1 ?stand_p1) 
	(frame_tool_0 ?frame_p1 ?tool_p1) 
	(gripper_frame_1 ?gripper_p1 ?frame_p1) 
	(not (frame_stand_0 ?frame_p1 ?stand_p1))
	(not (frame_tool_1 ?frame_p1 ?tool_p1))
	(not (frame_tool_2 ?frame_p1 ?tool_p1))
	(not (frame_tool_3 ?frame_p1 ?tool_p1))
	(not (gripper_frame_0 ?gripper_p1 ?frame_p1))
	(not (clear3_gripper_frame_1 ?gripper_p1)) 
 ) 
)

(:action a51 
:parameters ( ?gripper_p1 - gripper  ?frame_p1 - frame  ?stand_p1 - stand )
:precondition (and 
	(frame_stand_0 ?frame_p1 ?stand_p1)
	(gripper_frame_1 ?gripper_p1 ?frame_p1)
	(gripper_stand_0 ?gripper_p1 ?stand_p1)
	(clear3_gripper_tool_1 ?gripper_p1) 
) 
:effect (and 
 	(frame_stand_1 ?frame_p1 ?stand_p1) 
	(gripper_frame_0 ?gripper_p1 ?frame_p1) 
	(not (frame_stand_0 ?frame_p1 ?stand_p1))
	(not (gripper_frame_1 ?gripper_p1 ?frame_p1))
	(clear3_gripper_frame_1 ?gripper_p1) 
 ) 
)

(:action a52 
:parameters ( ?gripper_p1 - gripper  ?frame_p1 - frame  ?stand_p1 - stand  ?tool_p1 - tool )
:precondition (and 
	(frame_stand_0 ?frame_p1 ?stand_p1)
	(frame_tool_1 ?frame_p1 ?tool_p1)
	(gripper_frame_0 ?gripper_p1 ?frame_p1)
	(gripper_stand_0 ?gripper_p1 ?stand_p1)
	(gripper_tool_1 ?gripper_p1 ?tool_p1)
	(stand_tool_1 ?stand_p1 ?tool_p1)
	(clear3_gripper_frame_1 ?gripper_p1) 
) 
:effect (and 
 	(frame_stand_1 ?frame_p1 ?stand_p1) 
	(frame_tool_0 ?frame_p1 ?tool_p1) 
	(gripper_tool_0 ?gripper_p1 ?tool_p1) 
	(not (frame_stand_0 ?frame_p1 ?stand_p1))
	(not (frame_tool_1 ?frame_p1 ?tool_p1))
	(not (frame_tool_2 ?frame_p1 ?tool_p1))
	(not (frame_tool_3 ?frame_p1 ?tool_p1))
	(not (gripper_tool_1 ?gripper_p1 ?tool_p1))
	(clear3_gripper_tool_1 ?gripper_p1) 
 ) 
)

(:action a53 
:parameters ( ?gripper_p1 - gripper  ?frame_p1 - frame  ?stand_extra_p1 - stand  ?tool_p1 - tool )
:precondition (and 
	(frame_stand_1 ?frame_p1 ?stand_extra_p1)
	(frame_tool_2 ?frame_p1 ?tool_p1)
	(gripper_frame_0 ?gripper_p1 ?frame_p1)
	(gripper_tool_0 ?gripper_p1 ?tool_p1)
	(stand_tool_2 ?stand_extra_p1 ?tool_p1)
	(clear3_gripper_frame_1 ?gripper_p1) 
	(clear3_gripper_tool_1 ?gripper_p1) 
) 
:effect (and 
 	(frame_tool_0 ?frame_p1 ?tool_p1) 
	(gripper_frame_1 ?gripper_p1 ?frame_p1) 
	(not (frame_tool_1 ?frame_p1 ?tool_p1))
	(not (frame_tool_2 ?frame_p1 ?tool_p1))
	(not (frame_tool_3 ?frame_p1 ?tool_p1))
	(not (gripper_frame_0 ?gripper_p1 ?frame_p1))
	(not (clear3_gripper_frame_1 ?gripper_p1)) 
 ) 
)

(:action a54 
:parameters ( ?gripper_p1 - gripper  ?frame_p1 - frame  ?stand_p1 - stand  ?tool_p1 - tool )
:precondition (and 
	(frame_stand_0 ?frame_p1 ?stand_p1)
	(frame_tool_0 ?frame_p1 ?tool_p1)
	(gripper_frame_1 ?gripper_p1 ?frame_p1)
	(gripper_stand_0 ?gripper_p1 ?stand_p1)
	(gripper_tool_0 ?gripper_p1 ?tool_p1)
	(stand_tool_2 ?stand_p1 ?tool_p1)
	(clear3_gripper_tool_1 ?gripper_p1) 
) 
:effect (and 
 	(frame_stand_1 ?frame_p1 ?stand_p1) 
	(frame_tool_2 ?frame_p1 ?tool_p1) 
	(gripper_frame_0 ?gripper_p1 ?frame_p1) 
	(not (frame_stand_0 ?frame_p1 ?stand_p1))
	(not (frame_tool_0 ?frame_p1 ?tool_p1))
	(not (frame_tool_1 ?frame_p1 ?tool_p1))
	(not (frame_tool_3 ?frame_p1 ?tool_p1))
	(not (gripper_frame_1 ?gripper_p1 ?frame_p1))
	(clear3_gripper_frame_1 ?gripper_p1) 
 ) 
)

(:action a55 
:parameters ( ?frame_p1 - frame  ?stand_p1 - stand  ?gripper_extra_p1 - gripper  ?tool_p1 - tool )
:precondition (and 
	(frame_stand_1 ?frame_p1 ?stand_p1)
	(frame_tool_1 ?frame_p1 ?tool_p1)
	(gripper_frame_0 ?gripper_extra_p1 ?frame_p1)
	(gripper_stand_0 ?gripper_extra_p1 ?stand_p1)
	(gripper_tool_0 ?gripper_extra_p1 ?tool_p1)
	(stand_tool_1 ?stand_p1 ?tool_p1)
) 
:effect (and 
 	(frame_tool_3 ?frame_p1 ?tool_p1) 
	(stand_tool_0 ?stand_p1 ?tool_p1) 
	(not (frame_tool_0 ?frame_p1 ?tool_p1))
	(not (frame_tool_1 ?frame_p1 ?tool_p1))
	(not (frame_tool_2 ?frame_p1 ?tool_p1))
	(not (stand_tool_1 ?stand_p1 ?tool_p1))
	(not (stand_tool_2 ?stand_p1 ?tool_p1))
 ) 
)

(:action a56 
:parameters ( ?frame_p1 - frame  ?stand_p1 - stand  ?gripper_extra_p1 - gripper  ?tool_p1 - tool )
:precondition (and 
	(frame_stand_0 ?frame_p1 ?stand_p1)
	(frame_tool_3 ?frame_p1 ?tool_p1)
	(gripper_frame_0 ?gripper_extra_p1 ?frame_p1)
	(gripper_stand_0 ?gripper_extra_p1 ?stand_p1)
	(gripper_tool_0 ?gripper_extra_p1 ?tool_p1)
	(stand_tool_0 ?stand_p1 ?tool_p1)
) 
:effect (and 
 	(frame_stand_1 ?frame_p1 ?stand_p1) 
	(frame_tool_0 ?frame_p1 ?tool_p1) 
	(not (frame_stand_0 ?frame_p1 ?stand_p1))
	(not (frame_tool_1 ?frame_p1 ?tool_p1))
	(not (frame_tool_2 ?frame_p1 ?tool_p1))
	(not (frame_tool_3 ?frame_p1 ?tool_p1))
 ) 
)

(:action a57 
:parameters ( ?gripper_p1 - gripper  ?frame_p1 - frame  ?stand_p1 - stand  ?tool_p1 - tool )
:precondition (and 
	(frame_stand_0 ?frame_p1 ?stand_p1)
	(frame_tool_1 ?frame_p1 ?tool_p1)
	(gripper_frame_0 ?gripper_p1 ?frame_p1)
	(gripper_stand_0 ?gripper_p1 ?stand_p1)
	(gripper_tool_1 ?gripper_p1 ?tool_p1)
	(stand_tool_0 ?stand_p1 ?tool_p1)
	(clear3_gripper_frame_1 ?gripper_p1) 
) 
:effect (and 
 	(frame_tool_0 ?frame_p1 ?tool_p1) 
	(gripper_tool_0 ?gripper_p1 ?tool_p1) 
	(stand_tool_1 ?stand_p1 ?tool_p1) 
	(not (frame_tool_1 ?frame_p1 ?tool_p1))
	(not (frame_tool_2 ?frame_p1 ?tool_p1))
	(not (frame_tool_3 ?frame_p1 ?tool_p1))
	(not (gripper_tool_1 ?gripper_p1 ?tool_p1))
	(not (stand_tool_0 ?stand_p1 ?tool_p1))
	(not (stand_tool_2 ?stand_p1 ?tool_p1))
	(clear3_gripper_tool_1 ?gripper_p1) 
 ) 
)

(:action a58 
:parameters ( ?frame_p1 - frame  ?stand_p1 - stand  ?tool_p1 - tool  ?gripper_extra_p1 - gripper )
:precondition (and 
	(frame_tool_1 ?frame_p1 ?tool_p1)
	(gripper_frame_0 ?gripper_extra_p1 ?frame_p1)
	(gripper_stand_0 ?gripper_extra_p1 ?stand_p1)
	(stand_tool_1 ?stand_p1 ?tool_p1)
) 
:effect (and 
 	(frame_tool_0 ?frame_p1 ?tool_p1) 
	(stand_tool_0 ?stand_p1 ?tool_p1) 
	(not (frame_tool_1 ?frame_p1 ?tool_p1))
	(not (frame_tool_2 ?frame_p1 ?tool_p1))
	(not (frame_tool_3 ?frame_p1 ?tool_p1))
	(not (stand_tool_1 ?stand_p1 ?tool_p1))
	(not (stand_tool_2 ?stand_p1 ?tool_p1))
 ) 
)

(:action a59 
:parameters ( ?gripper_p1 - gripper  ?frame_p1 - frame  ?stand_p1 - stand  ?tool_p1 - tool )
:precondition (and 
	(frame_stand_1 ?frame_p1 ?stand_p1)
	(frame_tool_2 ?frame_p1 ?tool_p1)
	(gripper_frame_1 ?gripper_p1 ?frame_p1)
	(gripper_stand_0 ?gripper_p1 ?stand_p1)
	(gripper_tool_0 ?gripper_p1 ?tool_p1)
	(clear3_gripper_tool_1 ?gripper_p1) 
) 
:effect (and 
 	(frame_stand_0 ?frame_p1 ?stand_p1) 
	(frame_tool_0 ?frame_p1 ?tool_p1) 
	(gripper_frame_0 ?gripper_p1 ?frame_p1) 
	(not (frame_stand_1 ?frame_p1 ?stand_p1))
	(not (frame_tool_1 ?frame_p1 ?tool_p1))
	(not (frame_tool_2 ?frame_p1 ?tool_p1))
	(not (frame_tool_3 ?frame_p1 ?tool_p1))
	(not (gripper_frame_1 ?gripper_p1 ?frame_p1))
	(clear3_gripper_frame_1 ?gripper_p1) 
 ) 
)

(:action a60 
:parameters ( ?gripper_p1 - gripper  ?frame_p1 - frame  ?tool_p1 - tool )
:precondition (and 
	(frame_tool_0 ?frame_p1 ?tool_p1)
	(gripper_frame_1 ?gripper_p1 ?frame_p1)
	(gripper_tool_0 ?gripper_p1 ?tool_p1)
	(clear3_gripper_tool_1 ?gripper_p1) 
) 
:effect (and 
 	(frame_tool_2 ?frame_p1 ?tool_p1) 
	(gripper_frame_0 ?gripper_p1 ?frame_p1) 
	(not (frame_tool_0 ?frame_p1 ?tool_p1))
	(not (frame_tool_1 ?frame_p1 ?tool_p1))
	(not (frame_tool_3 ?frame_p1 ?tool_p1))
	(not (gripper_frame_1 ?gripper_p1 ?frame_p1))
	(clear3_gripper_frame_1 ?gripper_p1) 
 ) 
)

(:action a61 
:parameters ( ?frame_p1 - frame  ?stand_p1 - stand  ?gripper_extra_p1 - gripper  ?tool_p1 - tool )
:precondition (and 
	(frame_stand_0 ?frame_p1 ?stand_p1)
	(frame_tool_1 ?frame_p1 ?tool_p1)
	(gripper_frame_0 ?gripper_extra_p1 ?frame_p1)
	(gripper_stand_0 ?gripper_extra_p1 ?stand_p1)
	(gripper_tool_0 ?gripper_extra_p1 ?tool_p1)
	(stand_tool_1 ?stand_p1 ?tool_p1)
) 
:effect (and 
 	(frame_stand_1 ?frame_p1 ?stand_p1) 
	(frame_tool_0 ?frame_p1 ?tool_p1) 
	(stand_tool_0 ?stand_p1 ?tool_p1) 
	(not (frame_stand_0 ?frame_p1 ?stand_p1))
	(not (frame_tool_1 ?frame_p1 ?tool_p1))
	(not (frame_tool_2 ?frame_p1 ?tool_p1))
	(not (frame_tool_3 ?frame_p1 ?tool_p1))
	(not (stand_tool_1 ?stand_p1 ?tool_p1))
	(not (stand_tool_2 ?stand_p1 ?tool_p1))
 ) 
)

(:action a62 
:parameters ( ?frame_p1 - frame  ?stand_p1 - stand  ?gripper_extra_p1 - gripper  ?tool_p1 - tool )
:precondition (and 
	(frame_stand_1 ?frame_p1 ?stand_p1)
	(frame_tool_0 ?frame_p1 ?tool_p1)
	(gripper_frame_0 ?gripper_extra_p1 ?frame_p1)
	(gripper_stand_0 ?gripper_extra_p1 ?stand_p1)
	(gripper_tool_0 ?gripper_extra_p1 ?tool_p1)
	(stand_tool_0 ?stand_p1 ?tool_p1)
) 
:effect (and 
 	(frame_tool_3 ?frame_p1 ?tool_p1) 
	(stand_tool_1 ?stand_p1 ?tool_p1) 
	(not (frame_tool_0 ?frame_p1 ?tool_p1))
	(not (frame_tool_1 ?frame_p1 ?tool_p1))
	(not (frame_tool_2 ?frame_p1 ?tool_p1))
	(not (stand_tool_0 ?stand_p1 ?tool_p1))
	(not (stand_tool_2 ?stand_p1 ?tool_p1))
 ) 
)

(:action a63 
:parameters ( ?gripper_p1 - gripper  ?frame_p1 - frame  ?stand_p1 - stand  ?tool_p1 - tool )
:precondition (and 
	(frame_stand_1 ?frame_p1 ?stand_p1)
	(frame_tool_0 ?frame_p1 ?tool_p1)
	(gripper_frame_0 ?gripper_p1 ?frame_p1)
	(gripper_stand_0 ?gripper_p1 ?stand_p1)
	(gripper_tool_1 ?gripper_p1 ?tool_p1)
	(stand_tool_0 ?stand_p1 ?tool_p1)
	(clear3_gripper_frame_1 ?gripper_p1) 
) 
:effect (and 
 	(frame_tool_1 ?frame_p1 ?tool_p1) 
	(gripper_tool_0 ?gripper_p1 ?tool_p1) 
	(stand_tool_1 ?stand_p1 ?tool_p1) 
	(not (frame_tool_0 ?frame_p1 ?tool_p1))
	(not (frame_tool_2 ?frame_p1 ?tool_p1))
	(not (frame_tool_3 ?frame_p1 ?tool_p1))
	(not (gripper_tool_1 ?gripper_p1 ?tool_p1))
	(not (stand_tool_0 ?stand_p1 ?tool_p1))
	(not (stand_tool_2 ?stand_p1 ?tool_p1))
	(clear3_gripper_tool_1 ?gripper_p1) 
 ) 
)

(:action a64 
:parameters ( ?frame_p1 - frame  ?stand_p1 - stand  ?gripper_extra_p1 - gripper  ?tool_p1 - tool )
:precondition (and 
	(frame_stand_0 ?frame_p1 ?stand_p1)
	(frame_tool_0 ?frame_p1 ?tool_p1)
	(gripper_frame_0 ?gripper_extra_p1 ?frame_p1)
	(gripper_stand_0 ?gripper_extra_p1 ?stand_p1)
	(gripper_tool_0 ?gripper_extra_p1 ?tool_p1)
	(stand_tool_0 ?stand_p1 ?tool_p1)
) 
:effect (and 
 	(frame_stand_1 ?frame_p1 ?stand_p1) 
	(stand_tool_1 ?stand_p1 ?tool_p1) 
	(not (frame_stand_0 ?frame_p1 ?stand_p1))
	(not (stand_tool_0 ?stand_p1 ?tool_p1))
	(not (stand_tool_2 ?stand_p1 ?tool_p1))
 ) 
)

(:action a65 
:parameters ( ?frame_p1 - frame  ?stand_p1 - stand  ?gripper_extra_p1 - gripper  ?tool_p1 - tool )
:precondition (and 
	(frame_stand_1 ?frame_p1 ?stand_p1)
	(frame_tool_0 ?frame_p1 ?tool_p1)
	(gripper_frame_0 ?gripper_extra_p1 ?frame_p1)
	(gripper_stand_0 ?gripper_extra_p1 ?stand_p1)
	(gripper_tool_0 ?gripper_extra_p1 ?tool_p1)
	(stand_tool_1 ?stand_p1 ?tool_p1)
) 
:effect (and 
 	(frame_tool_3 ?frame_p1 ?tool_p1) 
	(stand_tool_0 ?stand_p1 ?tool_p1) 
	(not (frame_tool_0 ?frame_p1 ?tool_p1))
	(not (frame_tool_1 ?frame_p1 ?tool_p1))
	(not (frame_tool_2 ?frame_p1 ?tool_p1))
	(not (stand_tool_1 ?stand_p1 ?tool_p1))
	(not (stand_tool_2 ?stand_p1 ?tool_p1))
 ) 
)

(:action a66 
:parameters ( ?frame_p1 - frame  ?gripper_extra_p1 - gripper  ?tool_p1 - tool )
:precondition (and 
	(frame_tool_1 ?frame_p1 ?tool_p1)
	(gripper_frame_0 ?gripper_extra_p1 ?frame_p1)
	(gripper_tool_0 ?gripper_extra_p1 ?tool_p1)
) 
:effect (and 
 	(frame_tool_3 ?frame_p1 ?tool_p1) 
	(not (frame_tool_0 ?frame_p1 ?tool_p1))
	(not (frame_tool_1 ?frame_p1 ?tool_p1))
	(not (frame_tool_2 ?frame_p1 ?tool_p1))
 ) 
)

(:action a67 
:parameters ( ?gripper_p1 - gripper  ?frame_p1 - frame  ?stand_p1 - stand  ?tool_p1 - tool )
:precondition (and 
	(frame_stand_1 ?frame_p1 ?stand_p1)
	(frame_tool_1 ?frame_p1 ?tool_p1)
	(gripper_frame_0 ?gripper_p1 ?frame_p1)
	(gripper_stand_0 ?gripper_p1 ?stand_p1)
	(gripper_tool_1 ?gripper_p1 ?tool_p1)
	(stand_tool_1 ?stand_p1 ?tool_p1)
	(clear3_gripper_frame_1 ?gripper_p1) 
) 
:effect (and 
 	(frame_tool_0 ?frame_p1 ?tool_p1) 
	(gripper_tool_0 ?gripper_p1 ?tool_p1) 
	(stand_tool_0 ?stand_p1 ?tool_p1) 
	(not (frame_tool_1 ?frame_p1 ?tool_p1))
	(not (frame_tool_2 ?frame_p1 ?tool_p1))
	(not (frame_tool_3 ?frame_p1 ?tool_p1))
	(not (gripper_tool_1 ?gripper_p1 ?tool_p1))
	(not (stand_tool_1 ?stand_p1 ?tool_p1))
	(not (stand_tool_2 ?stand_p1 ?tool_p1))
	(clear3_gripper_tool_1 ?gripper_p1) 
 ) 
)

(:action a68 
:parameters ( ?gripper_p1 - gripper  ?frame_p1 - frame  ?stand_extra_p1 - stand  ?tool_p1 - tool )
:precondition (and 
	(frame_stand_1 ?frame_p1 ?stand_extra_p1)
	(frame_tool_1 ?frame_p1 ?tool_p1)
	(gripper_frame_0 ?gripper_p1 ?frame_p1)
	(gripper_tool_0 ?gripper_p1 ?tool_p1)
	(clear3_gripper_frame_1 ?gripper_p1) 
	(clear3_gripper_tool_1 ?gripper_p1) 
) 
:effect (and 
 	(frame_tool_0 ?frame_p1 ?tool_p1) 
	(gripper_tool_1 ?gripper_p1 ?tool_p1) 
	(not (frame_tool_1 ?frame_p1 ?tool_p1))
	(not (frame_tool_2 ?frame_p1 ?tool_p1))
	(not (frame_tool_3 ?frame_p1 ?tool_p1))
	(not (gripper_tool_0 ?gripper_p1 ?tool_p1))
	(not (clear3_gripper_tool_1 ?gripper_p1)) 
 ) 
)

(:action a69 
:parameters ( ?gripper_p1 - gripper  ?frame_p1 - frame  ?stand_p1 - stand  ?tool_p1 - tool )
:precondition (and 
	(frame_stand_1 ?frame_p1 ?stand_p1)
	(frame_tool_1 ?frame_p1 ?tool_p1)
	(gripper_frame_0 ?gripper_p1 ?frame_p1)
	(gripper_stand_0 ?gripper_p1 ?stand_p1)
	(gripper_tool_1 ?gripper_p1 ?tool_p1)
	(stand_tool_0 ?stand_p1 ?tool_p1)
	(clear3_gripper_frame_1 ?gripper_p1) 
) 
:effect (and 
 	(frame_stand_0 ?frame_p1 ?stand_p1) 
	(gripper_tool_0 ?gripper_p1 ?tool_p1) 
	(stand_tool_1 ?stand_p1 ?tool_p1) 
	(not (frame_stand_1 ?frame_p1 ?stand_p1))
	(not (gripper_tool_1 ?gripper_p1 ?tool_p1))
	(not (stand_tool_0 ?stand_p1 ?tool_p1))
	(not (stand_tool_2 ?stand_p1 ?tool_p1))
	(clear3_gripper_tool_1 ?gripper_p1) 
 ) 
)

(:action a70 
:parameters ( ?gripper_p1 - gripper  ?frame_p1 - frame  ?stand_p1 - stand  ?tool_p1 - tool )
:precondition (and 
	(frame_stand_1 ?frame_p1 ?stand_p1)
	(frame_tool_0 ?frame_p1 ?tool_p1)
	(gripper_frame_0 ?gripper_p1 ?frame_p1)
	(gripper_stand_0 ?gripper_p1 ?stand_p1)
	(gripper_tool_0 ?gripper_p1 ?tool_p1)
	(stand_tool_0 ?stand_p1 ?tool_p1)
	(clear3_gripper_frame_1 ?gripper_p1) 
	(clear3_gripper_tool_1 ?gripper_p1) 
) 
:effect (and 
 	(frame_tool_1 ?frame_p1 ?tool_p1) 
	(gripper_tool_1 ?gripper_p1 ?tool_p1) 
	(stand_tool_1 ?stand_p1 ?tool_p1) 
	(not (frame_tool_0 ?frame_p1 ?tool_p1))
	(not (frame_tool_2 ?frame_p1 ?tool_p1))
	(not (frame_tool_3 ?frame_p1 ?tool_p1))
	(not (gripper_tool_0 ?gripper_p1 ?tool_p1))
	(not (stand_tool_0 ?stand_p1 ?tool_p1))
	(not (stand_tool_2 ?stand_p1 ?tool_p1))
	(not (clear3_gripper_tool_1 ?gripper_p1)) 
 ) 
)

(:action a71 
:parameters ( ?gripper_p1 - gripper  ?frame_p1 - frame  ?stand_p1 - stand  ?tool_p1 - tool )
:precondition (and 
	(frame_stand_0 ?frame_p1 ?stand_p1)
	(frame_tool_0 ?frame_p1 ?tool_p1)
	(gripper_frame_0 ?gripper_p1 ?frame_p1)
	(gripper_stand_0 ?gripper_p1 ?stand_p1)
	(gripper_tool_0 ?gripper_p1 ?tool_p1)
	(stand_tool_2 ?stand_p1 ?tool_p1)
	(clear3_gripper_frame_1 ?gripper_p1) 
	(clear3_gripper_tool_1 ?gripper_p1) 
) 
:effect (and 
 	(frame_stand_1 ?frame_p1 ?stand_p1) 
	(frame_tool_2 ?frame_p1 ?tool_p1) 
	(gripper_frame_1 ?gripper_p1 ?frame_p1) 
	(not (frame_stand_0 ?frame_p1 ?stand_p1))
	(not (frame_tool_0 ?frame_p1 ?tool_p1))
	(not (frame_tool_1 ?frame_p1 ?tool_p1))
	(not (frame_tool_3 ?frame_p1 ?tool_p1))
	(not (gripper_frame_0 ?gripper_p1 ?frame_p1))
	(not (clear3_gripper_frame_1 ?gripper_p1)) 
 ) 
)


)