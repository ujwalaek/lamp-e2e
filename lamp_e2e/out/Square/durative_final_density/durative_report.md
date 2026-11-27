# Square: stage-aware durative monitor

| Test case | Runs | Really failed | Flagged | Meaning |
|---|---|---|---|---|
| nominal (recorded, all succeed) | 20 | - | 7 | false alarms |
| drop (physics rollout) | 20 | 20 | 20 | detected |
| miss (physics rollout) | 20 | 20 | 19 | detected |

## False alarms (nominal runs flagged)

| Stage | Condition | Predicate | Why outside | Pose typical of training? | Count |
|---|---|---|---|---|---|
| release-and-retreat | typical pose | gripper_1->nut_1 | pose atypical for this stage | no | 4 |
| release-and-retreat | typical pose | nut_1->peg_1 | pose atypical for this stage | no | 4 |
| move-nut-to-peg | typical pose | gripper_1->nut_1 | pose atypical for this stage | no | 1 |
| insert-nut | typical pose | gripper_1->nut_1 | pose atypical for this stage | no | 1 |
| insert-nut | typical pose | nut_1->peg_1 | pose atypical for this stage | no | 1 |

### Every false alarm

- **demo_21**, stage `move-nut-to-peg`, typical pose `gripper_1->nut_1`: atypical for 19 frames in a row (normal demos: at most 16). Relative pose (gripper_1->nut_1) pos [5.0, 0.9, -2.0] cm, rpy [7.0, -9.0, 179.0] deg. pose atypical for this stage. Nearest training pose distance n/a (99th pct n/a).
- **demo_27**, stage `release-and-retreat`, typical pose `gripper_1->nut_1`: atypical for 15 frames in a row (normal demos: at most 8). Relative pose (gripper_1->nut_1) pos [7.3, -1.2, -3.4] cm, rpy [33.0, -8.0, 168.0] deg. pose atypical for this stage. Nearest training pose distance n/a (99th pct n/a).
- **demo_27**, stage `release-and-retreat`, typical pose `nut_1->peg_1`: atypical for 12 frames in a row (normal demos: at most 9). Relative pose (nut_1->peg_1) pos [-0.7, -2.2, -5.7] cm, rpy [-20.0, 6.0, 7.0] deg. pose atypical for this stage. Nearest training pose distance n/a (99th pct n/a).
- **demo_105**, stage `release-and-retreat`, typical pose `gripper_1->nut_1`: atypical for 11 frames in a row (normal demos: at most 8). Relative pose (gripper_1->nut_1) pos [7.3, 1.9, -0.6] cm, rpy [1.0, -3.0, -173.0] deg. pose atypical for this stage. Nearest training pose distance n/a (99th pct n/a).
- **demo_105**, stage `release-and-retreat`, typical pose `nut_1->peg_1`: atypical for 117 frames in a row (normal demos: at most 9). Relative pose (nut_1->peg_1) pos [-27.6, -22.5, 2.0] cm, rpy [0.0, -0.0, -36.0] deg. pose atypical for this stage. Nearest training pose distance n/a (99th pct n/a).
- **demo_131**, stage `release-and-retreat`, typical pose `nut_1->peg_1`: atypical for 102 frames in a row (normal demos: at most 9). Relative pose (nut_1->peg_1) pos [19.3, 29.4, 2.0] cm, rpy [0.0, -0.0, -22.0] deg. pose atypical for this stage. Nearest training pose distance n/a (99th pct n/a).
- **demo_168**, stage `release-and-retreat`, typical pose `gripper_1->nut_1`: atypical for 14 frames in a row (normal demos: at most 8). Relative pose (gripper_1->nut_1) pos [1.7, 2.1, -10.8] cm, rpy [4.0, 5.0, 147.0] deg. pose atypical for this stage. Nearest training pose distance n/a (99th pct n/a).
- **demo_168**, stage `release-and-retreat`, typical pose `nut_1->peg_1`: atypical for 135 frames in a row (normal demos: at most 9). Relative pose (nut_1->peg_1) pos [-19.4, -30.5, 2.0] cm, rpy [0.0, -0.0, -15.0] deg. pose atypical for this stage. Nearest training pose distance n/a (99th pct n/a).
- **demo_180**, stage `release-and-retreat`, typical pose `gripper_1->nut_1`: atypical for 9 frames in a row (normal demos: at most 8). Relative pose (gripper_1->nut_1) pos [3.6, -11.5, -21.3] cm, rpy [-13.0, -1.0, 20.0] deg. pose atypical for this stage. Nearest training pose distance n/a (99th pct n/a).
- **demo_191**, stage `insert-nut`, typical pose `gripper_1->nut_1`: atypical for 39 frames in a row (normal demos: at most 20). Relative pose (gripper_1->nut_1) pos [-5.1, -2.4, -1.9] cm, rpy [-1.0, -17.0, 1.0] deg. pose atypical for this stage. Nearest training pose distance n/a (99th pct n/a).
- **demo_191**, stage `insert-nut`, typical pose `nut_1->peg_1`: atypical for 21 frames in a row (normal demos: at most 10). Relative pose (nut_1->peg_1) pos [-3.0, -1.0, -7.4] cm, rpy [-0.0, 24.0, 13.0] deg. pose atypical for this stage. Nearest training pose distance n/a (99th pct n/a).

## Drop: detections and misses

First condition violated in each detected run:

| Stage | Condition | Predicate | Runs |
|---|---|---|---|
| release-and-retreat | typical pose | nut_1->peg_1 | 16 |
| release-and-retreat | typical pose | gripper_1->nut_1 | 4 |

Missed (0): none

## Miss: detections and misses

First condition violated in each detected run:

| Stage | Condition | Predicate | Runs |
|---|---|---|---|
| release-and-retreat | typical pose | nut_1->peg_1 | 12 |
| insert-nut | typical pose | nut_1->peg_1 | 5 |
| move-nut-to-peg | typical pose | nut_1->peg_1 | 1 |
| move-nut-to-peg | typical pose | gripper_1->nut_1 | 1 |

Missed (1): demo_176
- **demo_176**: stages [['approach-nut', 0, 58], ['move-nut-to-peg', 58, 114], ['insert-nut', 114, 114], ['release-and-retreat', 114, 122]]

## Condition violations on the 180 training demos (all succeed)

These show how reliable each learned condition is on normal runs.

| Condition | Violations |
|---|---|
| insert-nut / typical pose / gripper_1->nut_1 / True | 2 |
