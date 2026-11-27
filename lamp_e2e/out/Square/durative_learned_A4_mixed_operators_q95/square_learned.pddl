;; LEARNED durative model of robomimic Square (nothing task-specific written by hand).
;; Predicates = LAMP's learned regions; stages = robot grasp events; conditions kept if they held in
;; >= 95% of training demos; durations learned.
(define (domain square-learned)
  (:requirements :durative-actions :negative-preconditions)
  (:predicates (gripper_nut_1) (gripper_nut_1|gripper_nut_2) (gripper_nut_2) (nut_peg_1) (nut_peg_1|nut_peg_2) (nut_peg_2))
  (:durative-action free0
    :duration (<= ?duration 31.6)
    :condition (and
      (over all (not (gripper_nut_1)))   ; held in 301/301 training demos
      (over all (not (nut_peg_1|nut_peg_2)))   ; held in 301/301 training demos
    ))
  (:durative-action carry1-nut
    :duration (<= ?duration 52.5)
    :condition (and
      (over all (not (gripper_nut_2)))   ; held in 301/301 training demos
      (over all (not (nut_peg_1)))   ; held in 301/301 training demos
    ))
  (:durative-action free1
    :duration (<= ?duration 26.6)
    :condition (and
      (over all (not (gripper_nut_1)))   ; held in 304/304 training demos
      (at end (nut_peg_1|nut_peg_2))   ; held in 293/305 training demos
    ))
)
