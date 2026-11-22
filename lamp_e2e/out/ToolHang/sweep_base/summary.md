| theta | RCRs per pair | actions | best predicate vs ground truth | flagged (transition check) | flagged (transition + goal) |
|---|---|---|---|---|---|
| 1.0 | frame_stand 3, frame_tool 3, gripper_frame 1, gripper_stand 0, gripper_tool 1, stand_tool 1 | 78 | frame_is_assembled: frame_stand_1 F1 0.91; holding: frame_stand_1 F1 0.40; tool_on_frame: frame_stand_1 F1 0.08 | nominal 95% / drop 65% / miss 65% | nominal 95% / drop 65% / miss 65% |
| 0.7 | frame_stand 1, frame_tool 3, gripper_frame 1, gripper_stand 0, gripper_tool 1, stand_tool 2 | 71 | frame_is_assembled: frame_stand_1 F1 0.76; holding: frame_stand_1 F1 0.57; tool_on_frame: frame_stand_1 F1 0.06 | nominal 90% / drop 75% / miss 75% | nominal 90% / drop 75% / miss 75% |
