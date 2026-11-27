;; LEARNED durative model of robomimic ToolHang (nothing task-specific written by hand).
;; Predicates = LAMP's learned regions; stages = robot grasp events; conditions kept if they held in
;; >= 98% of training demos; durations learned.
(define (domain toolhang-learned)
  (:requirements :durative-actions :negative-preconditions)
  (:predicates (frame_stand_1) (frame_stand_1|frame_stand_2) (frame_stand_2) (frame_tool_1) (frame_tool_1|frame_tool_2) (frame_tool_1|frame_tool_2|frame_tool_3) (frame_tool_1|frame_tool_3) (frame_tool_2) (frame_tool_2|frame_tool_3) (frame_tool_3) (gripper_frame_1) (gripper_frame_1|gripper_frame_2) (gripper_frame_1|gripper_frame_2|gripper_frame_3) (gripper_frame_1|gripper_frame_2|gripper_frame_3|gripper_frame_4) (gripper_frame_1|gripper_frame_2|gripper_frame_4) (gripper_frame_1|gripper_frame_3) (gripper_frame_1|gripper_frame_3|gripper_frame_4) (gripper_frame_1|gripper_frame_4) (gripper_frame_2) (gripper_frame_2|gripper_frame_3) (gripper_frame_2|gripper_frame_3|gripper_frame_4) (gripper_frame_2|gripper_frame_4) (gripper_frame_3) (gripper_frame_3|gripper_frame_4) (gripper_frame_4) (gripper_stand_1) (gripper_stand_1|gripper_stand_2) (gripper_stand_1|gripper_stand_2|gripper_stand_3) (gripper_stand_1|gripper_stand_3) (gripper_stand_2) (gripper_stand_2|gripper_stand_3) (gripper_stand_3) (gripper_tool_1) (gripper_tool_1|gripper_tool_2) (gripper_tool_1|gripper_tool_2|gripper_tool_3) (gripper_tool_1|gripper_tool_2|gripper_tool_3|gripper_tool_4) (gripper_tool_1|gripper_tool_2|gripper_tool_4) (gripper_tool_1|gripper_tool_3) (gripper_tool_1|gripper_tool_3|gripper_tool_4) (gripper_tool_1|gripper_tool_4) (gripper_tool_2) (gripper_tool_2|gripper_tool_3) (gripper_tool_2|gripper_tool_3|gripper_tool_4) (gripper_tool_2|gripper_tool_4) (gripper_tool_3) (gripper_tool_3|gripper_tool_4) (gripper_tool_4) (stand_tool_1) (stand_tool_1|stand_tool_2) (stand_tool_1|stand_tool_2|stand_tool_3) (stand_tool_1|stand_tool_3) (stand_tool_2) (stand_tool_2|stand_tool_3) (stand_tool_3))
  (:durative-action free0
    :duration (<= ?duration 8.1)
    :condition (and
      (over all (not (frame_stand_2)))   ; held in 178/178 training demos
      (over all (not (frame_tool_1|frame_tool_3)))   ; held in 178/178 training demos
      (at end (gripper_frame_1))   ; held in 179/180 training demos
      (over all (not (gripper_frame_1|gripper_frame_2|gripper_frame_3)))   ; held in 178/178 training demos
      (over all (not (gripper_stand_1|gripper_stand_2|gripper_stand_3)))   ; held in 178/178 training demos
      (over all (not (gripper_tool_1|gripper_tool_2|gripper_tool_3|gripper_tool_4)))   ; held in 178/178 training demos
      (over all (not (stand_tool_2|stand_tool_3)))   ; held in 178/178 training demos
    ))
  (:durative-action carry1-frame
    :duration (<= ?duration 29.4)
    :condition (and
      (over all (not (frame_stand_1)))   ; held in 178/178 training demos
      (at end (frame_stand_2))   ; held in 178/180 training demos
      (over all (not (frame_tool_1|frame_tool_2)))   ; held in 178/178 training demos
      (at end (frame_tool_3))   ; held in 177/180 training demos
      (at start (gripper_frame_1))   ; held in 179/180 training demos
      (over all (not (gripper_frame_2|gripper_frame_3|gripper_frame_4)))   ; held in 178/178 training demos
      (over all (not (gripper_stand_1|gripper_stand_2|gripper_stand_3)))   ; held in 178/178 training demos
      (over all (not (gripper_tool_1|gripper_tool_2|gripper_tool_3|gripper_tool_4)))   ; held in 178/178 training demos
      (over all (not (stand_tool_2|stand_tool_3)))   ; held in 178/178 training demos
    ))
  (:durative-action free1
    :duration (<= ?duration 22.6)
    :condition (and
      (over all (not (frame_stand_1)))   ; held in 179/179 training demos
      (over all (frame_stand_2))   ; held in 177/179 training demos
      (over all (not (frame_tool_1|frame_tool_2)))   ; held in 179/179 training demos
      (at start (frame_tool_3))   ; held in 177/180 training demos
      (over all (not (gripper_frame_1|gripper_frame_2|gripper_frame_3|gripper_frame_4)))   ; held in 177/179 training demos
      (over all (not (gripper_stand_1|gripper_stand_2|gripper_stand_3)))   ; held in 179/179 training demos
      (over all (not (gripper_tool_1|gripper_tool_2|gripper_tool_3|gripper_tool_4)))   ; held in 179/179 training demos
      (over all (not (stand_tool_2|stand_tool_3)))   ; held in 179/179 training demos
    ))
  (:durative-action carry2-tool
    :duration (<= ?duration 35.1)
    :condition (and
      (over all (not (frame_stand_1)))   ; held in 179/179 training demos
      (at start (frame_stand_2))   ; held in 180/180 training demos
      (at end (frame_stand_2))   ; held in 180/180 training demos
      (over all (not (frame_tool_2|frame_tool_3)))   ; held in 178/179 training demos
      (over all (not (gripper_frame_1|gripper_frame_3|gripper_frame_4)))   ; held in 179/179 training demos
      (over all (not (gripper_stand_1|gripper_stand_2|gripper_stand_3)))   ; held in 179/179 training demos
      (over all (not (gripper_tool_1|gripper_tool_2|gripper_tool_3)))   ; held in 179/179 training demos
      (at start (gripper_tool_1|gripper_tool_4))   ; held in 177/180 training demos
      (over all (not (stand_tool_1|stand_tool_3)))   ; held in 178/179 training demos
    ))
  (:durative-action free2
    :duration (<= ?duration 15.8)
    :condition (and
      (over all (not (frame_stand_1)))   ; held in 180/180 training demos
      (at start (frame_stand_2))   ; held in 180/180 training demos
      (at end (frame_stand_2))   ; held in 179/180 training demos
      (over all (not (frame_tool_2|frame_tool_3)))   ; held in 180/180 training demos
      (over all (not (gripper_frame_1|gripper_frame_3|gripper_frame_4)))   ; held in 180/180 training demos
      (over all (not (gripper_stand_1|gripper_stand_2|gripper_stand_3)))   ; held in 180/180 training demos
      (over all (not (gripper_tool_2|gripper_tool_3|gripper_tool_4)))   ; held in 180/180 training demos
      (over all (not (stand_tool_1|stand_tool_3)))   ; held in 180/180 training demos
    ))
)
