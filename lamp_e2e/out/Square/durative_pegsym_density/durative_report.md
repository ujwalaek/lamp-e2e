# Square: stage-aware durative monitor

| Test case | Runs | Really failed | Flagged | Meaning |
|---|---|---|---|---|
| nominal (recorded, all succeed) | 20 | - | 4 | false alarms |
| drop (physics rollout) | 20 | 20 | 20 | detected |
| miss (physics rollout) | 20 | 20 | 20 | detected |

## False alarms (nominal runs flagged)

| Stage | Condition | Predicate | Why outside | Pose typical of training? | Count |
|---|---|---|---|---|---|
| release-and-retreat | typical pose | gripper_1->nut_1 | pose atypical for this stage | no | 2 |
| release-and-retreat | typical pose | nut_1->peg_1 | pose atypical for this stage | no | 2 |
| insert-nut | typical pose | gripper_1->nut_1 | pose atypical for this stage | no | 1 |
| insert-nut | typical pose | nut_1->peg_1 | pose atypical for this stage | no | 1 |

### Every false alarm

- **demo_27**, stage `release-and-retreat`, typical pose `gripper_1->nut_1`: atypical for 15 frames in a row (normal demos: at most 6). Relative pose (gripper_1->nut_1) pos [7.0, -1.2, -2.6] cm, rpy [33.0, -7.0, 167.0] deg. pose atypical for this stage. Nearest training pose distance n/a (99th pct n/a).
- **demo_27**, stage `release-and-retreat`, typical pose `nut_1->peg_1`: atypical for 15 frames in a row (normal demos: at most 4). Relative pose (nut_1->peg_1) pos [-0.8, -2.1, -5.8] cm, rpy [-20.0, 6.0, 8.0] deg. pose atypical for this stage. Nearest training pose distance n/a (99th pct n/a).
- **demo_125**, stage `release-and-retreat`, typical pose `nut_1->peg_1`: atypical for 6 frames in a row (normal demos: at most 4). Relative pose (nut_1->peg_1) pos [1.2, 2.8, -7.8] cm, rpy [17.0, -2.0, -4.0] deg. pose atypical for this stage. Nearest training pose distance n/a (99th pct n/a).
- **demo_180**, stage `release-and-retreat`, typical pose `gripper_1->nut_1`: atypical for 9 frames in a row (normal demos: at most 6). Relative pose (gripper_1->nut_1) pos [1.3, -10.3, -20.6] cm, rpy [-9.0, -0.0, 17.0] deg. pose atypical for this stage. Nearest training pose distance n/a (99th pct n/a).
- **demo_191**, stage `insert-nut`, typical pose `gripper_1->nut_1`: atypical for 39 frames in a row (normal demos: at most 20). Relative pose (gripper_1->nut_1) pos [-5.1, -2.4, -1.9] cm, rpy [-1.0, -17.0, 1.0] deg. pose atypical for this stage. Nearest training pose distance n/a (99th pct n/a).
- **demo_191**, stage `insert-nut`, typical pose `nut_1->peg_1`: atypical for 21 frames in a row (normal demos: at most 10). Relative pose (nut_1->peg_1) pos [-3.0, -1.0, -7.4] cm, rpy [-0.0, 24.0, 13.0] deg. pose atypical for this stage. Nearest training pose distance n/a (99th pct n/a).

## Drop: detections and misses

First condition violated in each detected run:

| Stage | Condition | Predicate | Runs |
|---|---|---|---|
| release-and-retreat | typical pose | nut_1->peg_1 | 20 |

Missed (0): none

## Miss: detections and misses

First condition violated in each detected run:

| Stage | Condition | Predicate | Runs |
|---|---|---|---|
| release-and-retreat | typical pose | nut_1->peg_1 | 12 |
| insert-nut | typical pose | nut_1->peg_1 | 6 |
| move-nut-to-peg | typical pose | nut_1->peg_1 | 1 |
| move-nut-to-peg | typical pose | gripper_1->nut_1 | 1 |

Missed (0): none

## Condition violations on the 180 training demos (all succeed)

These show how reliable each learned condition is on normal runs.

| Condition | Violations |
|---|---|
| move-nut-to-peg / typical pose / nut_1->peg_1 / True | 2 |
| insert-nut / typical pose / gripper_1->nut_1 / True | 1 |
