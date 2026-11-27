;; Durative model of the robomimic ToolHang task (PDDL 2.1).
;; Predicates are LAMP's learned relational regions (union of the listed regions).
;; Durations (seconds) and condition tolerances are learned from 180 training demos.
(define (domain toolhang-durative)
  (:requirements :typing :durative-actions :negative-preconditions)
  (:types gripper frame stand tool)
  (:predicates
    (holding-frame ?g - gripper ?f - frame)   ; gripper holds the frame := gripper_frame_1
    (frame-above-stand ?f - frame ?s - stand)   ; frame above the stand, before insertion := frame_stand_1 or frame_stand_3
    (frame-in-stand ?f - frame ?s - stand)   ; frame inserted in the stand := frame_stand_2
    (at-tool-grasp ?g - gripper ?t - tool)   ; gripper at tool grasp pose, open := gripper_tool_1
    (holding-tool ?g - gripper ?t - tool)   ; gripper holds the tool := gripper_tool_2
    (tool-at-hook ?f - frame ?t - tool)   ; tool lined up at hook height := frame_tool_2
    (tool-on-hook ?f - frame ?t - tool)   ; tool hanging on the hook (NOT LEARNED) := no LAMP region
  )

  ;; relevant relations in this stage: gripper-frame (all others ignored)
  (:durative-action approach-frame
    :parameters (?g - gripper ?f - frame)
    :duration (and (>= ?duration 0.8) (<= ?duration 8.1))
    :condition (and
      (over all (not (holding-frame ?g ?f)))   ; flicker tolerance 0% of stage
    )
    :effect (and )
  )

  ;; relevant relations in this stage: frame-stand, gripper-frame (all others ignored)
  (:durative-action move-frame-to-stand
    :parameters (?g - gripper ?f - frame ?s - stand)
    :duration (and (>= ?duration 1.4) (<= ?duration 22.2))
    :condition (and
      (at start (holding-frame ?g ?f))   ; within 20 frames
      (over all (holding-frame ?g ?f))   ; flicker tolerance 100% of stage
      (at end (frame-above-stand ?f ?s))   ; within 1 frames
    )
    :effect (and (at end (frame-above-stand ?f ?s)))
  )

  ;; relevant relations in this stage: frame-stand, gripper-frame (all others ignored)
  (:durative-action insert-frame
    :parameters (?g - gripper ?f - frame ?s - stand)
    :duration (and (>= ?duration 0.2) (<= ?duration 21.9))
    :condition (and
      (at start (frame-above-stand ?f ?s))   ; within 0 frames
      (over all (holding-frame ?g ?f))   ; flicker tolerance 100% of stage
      (at end (frame-in-stand ?f ?s))   ; within 20 frames
    )
    :effect (and (at end (frame-in-stand ?f ?s)))
  )

  ;; relevant relations in this stage: frame-stand, gripper-tool (all others ignored)
  (:durative-action approach-tool
    :parameters (?g - gripper ?t - tool ?f - frame ?s - stand)
    :duration (and (>= ?duration 1.1) (<= ?duration 11.1))
    :condition (and
      (over all (frame-in-stand ?f ?s))   ; flicker tolerance 100% of stage
      (at end (at-tool-grasp ?g ?t))   ; within 20 frames
    )
    :effect (and (at end (at-tool-grasp ?g ?t)))
  )

  ;; relevant relations in this stage: frame-stand, frame-tool, gripper-tool (all others ignored)
  (:durative-action move-tool-to-hook
    :parameters (?g - gripper ?t - tool ?f - frame ?s - stand)
    :duration (and (>= ?duration 1.4) (<= ?duration 35.1))
    :condition (and
      (at start (holding-tool ?g ?t))   ; within 20 frames
      (over all (holding-tool ?g ?t))   ; flicker tolerance 100% of stage
      (over all (frame-in-stand ?f ?s))   ; flicker tolerance 68% of stage
      (at end (tool-at-hook ?f ?t))   ; within 20 frames
    )
    :effect (and (at end (tool-at-hook ?f ?t)))
  )

  ;; relevant relations in this stage: frame-stand, frame-tool (all others ignored)
  (:durative-action hang-tool-and-retreat
    :parameters (?g - gripper ?t - tool ?f - frame ?s - stand)
    :duration (and (>= ?duration 0.2) (<= ?duration 9.8))
    :condition (and
      (over all (frame-in-stand ?f ?s))   ; flicker tolerance 100% of stage
      (at end (tool-on-hook ?f ?t))   ; NOT CHECKABLE: LAMP learned no region for this relation
    )
    :effect (and (at end (tool-on-hook ?f ?t)))
  )
)
