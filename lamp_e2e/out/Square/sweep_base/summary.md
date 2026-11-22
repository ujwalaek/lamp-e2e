| theta | RCRs per pair | actions | best predicate vs ground truth | flagged (transition check) | flagged (transition + goal) |
|---|---|---|---|---|---|
| 1.0 | gripper_nut 0, gripper_peg 0, nut_peg 1 | 2 | holding: nut_peg_1 F1 0.01; nut_on_peg: nut_peg_1 F1 0.00 | nominal 0% / drop 0% / miss 0% | nominal 0% / drop 0% / miss 0% |
| 0.9 | gripper_nut 0, gripper_peg 0, nut_peg 2 | 5 | holding: nut_peg_2 F1 0.06; nut_on_peg: nut_peg_1 F1 0.27 | nominal 0% / drop 0% / miss 0% | nominal 0% / drop 0% / miss 0% |
| 0.7 | gripper_nut 0, gripper_peg 0, nut_peg 2 | 6 | holding: nut_peg_2 F1 0.06; nut_on_peg: nut_peg_1 F1 0.27 | nominal 0% / drop 0% / miss 0% | nominal 0% / drop 0% / miss 0% |
| 0.5 | gripper_nut 2, gripper_peg 0, nut_peg 2 | 12 | holding: gripper_nut_1 F1 0.07; nut_on_peg: nut_peg_1 F1 0.27 | nominal 5% / drop 0% / miss 0% | nominal 5% / drop 0% / miss 0% |
| 0.3 | gripper_nut 2, gripper_peg 0, nut_peg 2 | 25 | holding: nut_peg_2 F1 0.19; nut_on_peg: nut_peg_1 F1 0.60 | nominal 10% / drop 0% / miss 0% | nominal 10% / drop 0% / miss 0% |
