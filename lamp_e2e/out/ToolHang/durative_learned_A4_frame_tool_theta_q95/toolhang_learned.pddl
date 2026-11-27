;; LEARNED durative model of robomimic ToolHang (nothing task-specific written by hand).
;; Predicates = LAMP's learned regions; stages = robot grasp events; conditions kept if they held in
;; >= 95% of training demos; durations learned.
(define (domain toolhang-learned)
  (:requirements :durative-actions :negative-preconditions)
  (:predicates (frame_stand_1) (frame_stand_1|frame_stand_2) (frame_stand_1|frame_stand_2|frame_stand_3) (frame_stand_1|frame_stand_3) (frame_stand_2) (frame_stand_2|frame_stand_3) (frame_stand_3) (frame_tool_1) (frame_tool_1|frame_tool_2) (frame_tool_1|frame_tool_2|frame_tool_3) (frame_tool_1|frame_tool_3) (frame_tool_2) (frame_tool_2|frame_tool_3) (frame_tool_3) (gripper_frame_1) (gripper_tool_1) (gripper_tool_1|gripper_tool_2) (gripper_tool_2))
  (:durative-action free0
    :duration (<= ?duration 8.1)
    :condition (and
      (over all (not (frame_stand_1|frame_stand_2|frame_stand_3)))   ; held in 178/178 training demos
      (over all (not (frame_tool_1|frame_tool_3)))   ; held in 178/178 training demos
      (over all (not (gripper_frame_1)))   ; held in 178/178 training demos
      (over all (not (gripper_tool_1|gripper_tool_2)))   ; held in 178/178 training demos
    ))
  (:durative-action carry1-frame
    :duration (<= ?duration 29.4)
    :condition (and
      (at end (frame_stand_1))   ; held in 177/180 training demos
      (over all (not (frame_stand_1|frame_stand_2)))   ; held in 178/178 training demos
      (at end (frame_stand_2|frame_stand_3))   ; held in 173/180 training demos
      (over all (not (frame_tool_1|frame_tool_2)))   ; held in 178/178 training demos
      (at end (frame_tool_3))   ; held in 177/180 training demos
      (over all (not (gripper_tool_1|gripper_tool_2)))   ; held in 178/178 training demos
    ))
  (:durative-action free1
    :duration (<= ?duration 22.6)
    :condition (and
      (at start (frame_stand_1))   ; held in 177/180 training demos
      (at end (frame_stand_2))   ; held in 178/180 training demos
      (at start (frame_stand_2|frame_stand_3))   ; held in 174/180 training demos
      (over all (not (frame_stand_3)))   ; held in 179/179 training demos
      (over all (not (frame_tool_1|frame_tool_2)))   ; held in 179/179 training demos
      (at start (frame_tool_3))   ; held in 177/180 training demos
      (over all (not (gripper_frame_1)))   ; held in 179/179 training demos
      (over all (not (gripper_tool_1|gripper_tool_2)))   ; held in 179/179 training demos
    ))
  (:durative-action carry2-tool
    :duration (<= ?duration 35.1)
    :condition (and
      (over all (not (frame_stand_1|frame_stand_3)))   ; held in 179/179 training demos
      (over all (frame_stand_2))   ; held in 174/179 training demos
      (at end (frame_tool_1|frame_tool_2))   ; held in 171/180 training demos
      (at end (frame_tool_1|frame_tool_3))   ; held in 171/180 training demos
      (over all (not (frame_tool_2|frame_tool_3)))   ; held in 178/179 training demos
      (over all (not (gripper_frame_1)))   ; held in 179/179 training demos
      (over all (not (gripper_tool_2)))   ; held in 179/179 training demos
    ))
  (:durative-action free2
    :duration (<= ?duration 15.8)
    :condition (and
      (over all (not (frame_stand_1|frame_stand_3)))   ; held in 180/180 training demos
      (over all (frame_stand_2))   ; held in 175/180 training demos
      (at end (frame_tool_1))   ; held in 171/180 training demos
      (at start (frame_tool_1|frame_tool_2))   ; held in 171/180 training demos
      (at start (frame_tool_1|frame_tool_3))   ; held in 171/180 training demos
      (over all (not (frame_tool_2|frame_tool_3)))   ; held in 180/180 training demos
      (over all (not (gripper_frame_1)))   ; held in 180/180 training demos
      (over all (not (gripper_tool_1)))   ; held in 180/180 training demos
    ))
)
