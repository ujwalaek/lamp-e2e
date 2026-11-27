;; Durative model of the robomimic Square task (PDDL 2.1).
;; Predicates are LAMP's learned relational regions (union of the listed regions).
;; Durations (seconds) and condition tolerances are learned from 180 training demos.
(define (domain square-durative)
  (:requirements :typing :durative-actions :negative-preconditions)
  (:types gripper nut peg)
  (:predicates
    (holding ?g - gripper ?n - nut)   ; gripper holds the nut := gripper_nut_1 or gripper_nut_2
    (at-grasp-pose ?g - gripper ?n - nut)   ; gripper at grasp pose, open := gripper_nut_3
    (nut-above-peg ?n - nut ?p - peg)   ; nut aligned above / sliding down peg := nut_peg_2
    (nut-on-peg ?n - nut ?p - peg)   ; nut seated on peg := nut_peg_1
    (nut-at-peg ?n - nut ?p - peg)   ; nut aligned with peg (above or seated) := nut_peg_1 or nut_peg_2
    (ready-to-grasp ?g - gripper ?n - nut)   ; gripper at grasp pose or already holding := gripper_nut_1 or gripper_nut_2 or gripper_nut_3
  )

  ;; relevant relations in this stage: gripper-nut (all others ignored)
  (:durative-action approach-nut
    :parameters (?g - gripper ?n - nut)
    :duration (and (>= ?duration 0.0) (<= ?duration 8.0))
    :condition (and
      (over all (not (holding ?g ?n)))   ; flicker tolerance 0% of stage
      (at end (ready-to-grasp ?g ?n))   ; within 20 frames
    )
    :effect (and (at end (ready-to-grasp ?g ?n)))
  )

  ;; relevant relations in this stage: gripper-nut, nut-peg (all others ignored)
  (:durative-action move-nut-to-peg
    :parameters (?g - gripper ?n - nut ?p - peg)
    :duration (and (>= ?duration 0.0) (<= ?duration 6.1))
    :condition (and
      (at start (holding ?g ?n))   ; within 20 frames
      (over all (holding ?g ?n))   ; flicker tolerance 0% of stage
      (at end (nut-at-peg ?n ?p))   ; within 20 frames
    )
    :effect (and (at end (nut-at-peg ?n ?p)))
  )

  ;; relevant relations in this stage: gripper-nut, nut-peg (all others ignored)
  (:durative-action insert-nut
    :parameters (?g - gripper ?n - nut ?p - peg)
    :duration (and (>= ?duration 0.0) (<= ?duration 8.5))
    :condition (and
      (at start (nut-at-peg ?n ?p))   ; within 20 frames
      (over all (holding ?g ?n))   ; flicker tolerance 50% of stage
      (at end (nut-at-peg ?n ?p))   ; within 20 frames
    )
    :effect (and (at end (nut-at-peg ?n ?p)))
  )

  ;; relevant relations in this stage: gripper-nut, nut-peg (all others ignored)
  (:durative-action release-and-retreat
    :parameters (?g - gripper ?n - nut ?p - peg)
    :duration (and (>= ?duration 0.1) (<= ?duration 13.7))
    :condition (and
      (at start (nut-at-peg ?n ?p))   ; within 20 frames
      (over all (nut-at-peg ?n ?p))   ; flicker tolerance 73% of stage
      (at end (nut-on-peg ?n ?p))   ; within 12 frames
      (at end (not (holding ?g ?n)))   ; within 0 frames
    )
    :effect (and (at end (nut-on-peg ?n ?p)) (at end (not (holding ?g ?n))))
  )
)
