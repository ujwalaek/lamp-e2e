;; LEARNED durative model of robomimic Square (nothing task-specific written by hand).
;; Predicates = LAMP's learned regions; stages = robot grasp events; conditions kept if they held in
;; >= 90% of training demos; durations learned.
(define (domain square-learned)
  (:requirements :durative-actions :negative-preconditions)
  (:predicates (gripper_nut_1) (gripper_nut_1|gripper_nut_2) (gripper_nut_1|gripper_nut_2|gripper_nut_3) (gripper_nut_1|gripper_nut_3) (gripper_nut_2) (gripper_nut_2|gripper_nut_3) (gripper_nut_3) (nut_peg_1) (nut_peg_1|nut_peg_2) (nut_peg_2))
  (:durative-action free0
    :duration (<= ?duration 8.0)
    :condition (and
      (at end (gripper_nut_1|gripper_nut_2))   ; held in 172/180 training demos
      (over all (not (gripper_nut_1|gripper_nut_2|gripper_nut_3)))   ; held in 160/177 training demos
      (at end (gripper_nut_1|gripper_nut_3))   ; held in 169/180 training demos
      (over all (not (nut_peg_1|nut_peg_2)))   ; held in 177/177 training demos
    ))
  (:durative-action carry1-nut
    :duration (<= ?duration 12.1)
    :condition (and
      (at start (gripper_nut_1|gripper_nut_2))   ; held in 172/180 training demos
      (at start (gripper_nut_1|gripper_nut_3))   ; held in 169/180 training demos
      (over all (not (gripper_nut_3)))   ; held in 177/177 training demos
      (over all (not (nut_peg_1|nut_peg_2)))   ; held in 172/177 training demos
    ))
  (:durative-action free1
    :duration (<= ?duration 13.7)
    :condition (and
      (over all (not (gripper_nut_1|gripper_nut_2)))   ; held in 180/180 training demos
    ))
)
