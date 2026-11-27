;; LEARNED durative model of robomimic Square (nothing task-specific written by hand).
;; Predicates = LAMP's learned regions; stages = robot grasp events; conditions kept if they held in
;; >= 80% of training demos; durations learned.
(define (domain square-learned)
  (:requirements :durative-actions :negative-preconditions)
  (:predicates (gripper_nut_1) (gripper_nut_1|gripper_nut_2) (gripper_nut_1|gripper_nut_2|gripper_nut_3) (gripper_nut_1|gripper_nut_2|gripper_nut_3|gripper_nut_4) (gripper_nut_1|gripper_nut_2|gripper_nut_3|gripper_nut_4|gripper_nut_5) (gripper_nut_1|gripper_nut_2|gripper_nut_3|gripper_nut_5) (gripper_nut_1|gripper_nut_2|gripper_nut_4) (gripper_nut_1|gripper_nut_2|gripper_nut_4|gripper_nut_5) (gripper_nut_1|gripper_nut_2|gripper_nut_5) (gripper_nut_1|gripper_nut_3) (gripper_nut_1|gripper_nut_3|gripper_nut_4) (gripper_nut_1|gripper_nut_3|gripper_nut_4|gripper_nut_5) (gripper_nut_1|gripper_nut_3|gripper_nut_5) (gripper_nut_1|gripper_nut_4) (gripper_nut_1|gripper_nut_4|gripper_nut_5) (gripper_nut_1|gripper_nut_5) (gripper_nut_2) (gripper_nut_2|gripper_nut_3) (gripper_nut_2|gripper_nut_3|gripper_nut_4) (gripper_nut_2|gripper_nut_3|gripper_nut_4|gripper_nut_5) (gripper_nut_2|gripper_nut_3|gripper_nut_5) (gripper_nut_2|gripper_nut_4) (gripper_nut_2|gripper_nut_4|gripper_nut_5) (gripper_nut_2|gripper_nut_5) (gripper_nut_3) (gripper_nut_3|gripper_nut_4) (gripper_nut_3|gripper_nut_4|gripper_nut_5) (gripper_nut_3|gripper_nut_5) (gripper_nut_4) (gripper_nut_4|gripper_nut_5) (gripper_nut_5) (gripper_peg_1) (gripper_peg_1|gripper_peg_2) (gripper_peg_1|gripper_peg_2|gripper_peg_3) (gripper_peg_1|gripper_peg_2|gripper_peg_3|gripper_peg_4) (gripper_peg_1|gripper_peg_2|gripper_peg_3|gripper_peg_4|gripper_peg_5) (gripper_peg_1|gripper_peg_2|gripper_peg_3|gripper_peg_5) (gripper_peg_1|gripper_peg_2|gripper_peg_4) (gripper_peg_1|gripper_peg_2|gripper_peg_4|gripper_peg_5) (gripper_peg_1|gripper_peg_2|gripper_peg_5) (gripper_peg_1|gripper_peg_3) (gripper_peg_1|gripper_peg_3|gripper_peg_4) (gripper_peg_1|gripper_peg_3|gripper_peg_4|gripper_peg_5) (gripper_peg_1|gripper_peg_3|gripper_peg_5) (gripper_peg_1|gripper_peg_4) (gripper_peg_1|gripper_peg_4|gripper_peg_5) (gripper_peg_1|gripper_peg_5) (gripper_peg_2) (gripper_peg_2|gripper_peg_3) (gripper_peg_2|gripper_peg_3|gripper_peg_4) (gripper_peg_2|gripper_peg_3|gripper_peg_4|gripper_peg_5) (gripper_peg_2|gripper_peg_3|gripper_peg_5) (gripper_peg_2|gripper_peg_4) (gripper_peg_2|gripper_peg_4|gripper_peg_5) (gripper_peg_2|gripper_peg_5) (gripper_peg_3) (gripper_peg_3|gripper_peg_4) (gripper_peg_3|gripper_peg_4|gripper_peg_5) (gripper_peg_3|gripper_peg_5) (gripper_peg_4) (gripper_peg_4|gripper_peg_5) (gripper_peg_5) (nut_peg_1))
  (:durative-action free0
    :duration (<= ?duration 8.0)
    :condition (and
      (at end (gripper_nut_1|gripper_nut_2))   ; held in 168/180 training demos
      (over all (not (gripper_nut_1|gripper_nut_2|gripper_nut_3|gripper_nut_5)))   ; held in 143/177 training demos
      (at end (gripper_nut_1|gripper_nut_4))   ; held in 171/180 training demos
      (over all (not (gripper_nut_2|gripper_nut_3|gripper_nut_4|gripper_nut_5)))   ; held in 146/177 training demos
      (at end (gripper_nut_2|gripper_nut_5))   ; held in 172/180 training demos
      (at end (gripper_nut_4|gripper_nut_5))   ; held in 175/180 training demos
      (over all (not (gripper_peg_1|gripper_peg_2|gripper_peg_3|gripper_peg_4|gripper_peg_5)))   ; held in 177/177 training demos
      (over all (not (nut_peg_1)))   ; held in 177/177 training demos
    ))
  (:durative-action carry1-nut
    :duration (<= ?duration 12.1)
    :condition (and
      (at start (gripper_nut_1|gripper_nut_2))   ; held in 168/180 training demos
      (at end (gripper_nut_1|gripper_nut_2))   ; held in 156/180 training demos
      (over all (not (gripper_nut_1|gripper_nut_3|gripper_nut_4)))   ; held in 177/177 training demos
      (at start (gripper_nut_1|gripper_nut_4))   ; held in 171/180 training demos
      (at end (gripper_nut_1|gripper_nut_4))   ; held in 158/180 training demos
      (over all (gripper_nut_2|gripper_nut_5))   ; held in 154/177 training demos
      (at start (gripper_nut_4|gripper_nut_5))   ; held in 175/180 training demos
      (at end (gripper_nut_4|gripper_nut_5))   ; held in 161/180 training demos
      (over all (not (gripper_peg_1|gripper_peg_2|gripper_peg_3|gripper_peg_4|gripper_peg_5)))   ; held in 176/177 training demos
      (at end (nut_peg_1))   ; held in 174/180 training demos
    ))
  (:durative-action free1
    :duration (<= ?duration 13.7)
    :condition (and
      (at start (gripper_nut_1|gripper_nut_2))   ; held in 156/180 training demos
      (at end (gripper_nut_1|gripper_nut_2))   ; held in 152/180 training demos
      (at start (gripper_nut_1|gripper_nut_4))   ; held in 158/180 training demos
      (at end (gripper_nut_1|gripper_nut_4))   ; held in 157/180 training demos
      (over all (not (gripper_nut_2|gripper_nut_3|gripper_nut_5)))   ; held in 180/180 training demos
      (at start (gripper_nut_2|gripper_nut_5))   ; held in 159/180 training demos
      (at start (gripper_nut_4|gripper_nut_5))   ; held in 161/180 training demos
      (over all (not (gripper_peg_1|gripper_peg_2|gripper_peg_3|gripper_peg_5)))   ; held in 180/180 training demos
      (at start (nut_peg_1))   ; held in 174/180 training demos
      (at end (nut_peg_1))   ; held in 174/180 training demos
    ))
)
