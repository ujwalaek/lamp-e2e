;; LEARNED durative model of robomimic Square (nothing task-specific written by hand).
;; Predicates = LAMP's learned regions; stages = robot grasp events; conditions kept if they held in
;; >= 95% of training demos; durations learned.
(define (domain square-learned)
  (:requirements :durative-actions :negative-preconditions)
  (:predicates (nut_peg_1))
  (:durative-action free0
    :duration (<= ?duration 8.0)
    :condition (and
      (over all (not (nut_peg_1)))   ; held in 177/177 training demos
    ))
  (:durative-action carry1-nut
    :duration (<= ?duration 12.1)
    :condition (and
      (over all (not (nut_peg_1)))   ; held in 177/177 training demos
    ))
  (:durative-action free1
    :duration (<= ?duration 13.7)
    :condition (and
      (over all (not (nut_peg_1)))   ; held in 175/180 training demos
    ))
)
