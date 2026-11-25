# Square: stage-aware durative monitor

| Test case | Runs | Really failed | Flagged | Meaning |
|---|---|---|---|---|
| nominal (recorded, all succeed) | 20 | - | 1 | false alarms |
| drop (physics rollout) | 20 | 20 | 20 | detected |
| miss (physics rollout) | 20 | 20 | 20 | detected |

## False alarms (nominal runs flagged)

| Stage | Condition | Predicate | Why outside | Pose typical of training? | Count |
|---|---|---|---|---|---|
| insert-nut | over all | holding | grasp flag | no | 1 |
| release-and-retreat | at start | nut-at-peg |  | no | 1 |
| release-and-retreat | at end | nut-on-peg |  | no | 1 |
| release-and-retreat | at end | holding | inside region it should not be in | no | 1 |

### Every false alarm

- **demo_191**, stage `insert-nut`, over all `holding`: false for 31 of 59 frames in a row (tolerance 0% of stage). Relative pose (gripper_1->nut_1) pos [-5.3, -0.2, 0.4] cm, rpy [-1.0, 7.0, 1.0] deg. Outside learned bins: grasp sensor 0 (region 1). Nearest training pose distance n/a (99th pct n/a).
- **demo_191**, stage `release-and-retreat`, at start `nut-at-peg`: not true within 0 frames of the stage start (nearest: 1 frames away). Relative pose (nut_1->peg_1) pos [-0.4, -0.6, 2.1] cm, rpy [0.0, -1.0, 2.0] deg. . Nearest training pose distance 2.82 (99th pct 0.86).
- **demo_191**, stage `release-and-retreat`, at end `nut-on-peg`: not true within 0 frames of the stage end (nearest: 1 frames away). Relative pose (nut_1->peg_1) pos [-0.4, -0.6, 2.1] cm, rpy [0.0, -1.0, 2.0] deg. . Nearest training pose distance 2.82 (99th pct 0.86).
- **demo_191**, stage `release-and-retreat`, at end `holding` (should be false): not true within 0 frames of the stage end (nearest: 1 frames away). Relative pose (gripper_1->nut_1) pos [-6.6, -4.0, -13.3] cm, rpy [-3.0, 6.0, 18.0] deg. inside region it should not be in. Nearest training pose distance 6.21 (99th pct 0.72).

## Drop: detections and misses

First condition violated in each detected run:

| Stage | Condition | Predicate | Runs |
|---|---|---|---|
| move-nut-to-peg | at end | nut-at-peg | 18 |
| release-and-retreat | over all | nut-at-peg | 2 |

Missed (0): none

## Miss: detections and misses

First condition violated in each detected run:

| Stage | Condition | Predicate | Runs |
|---|---|---|---|
| move-nut-to-peg | at end | nut-at-peg | 13 |
| insert-nut | at end | nut-at-peg | 5 |
| insert-nut | over all | holding | 1 |
| move-nut-to-peg | over all | holding | 1 |

Missed (0): none

## Condition violations on the 180 training demos (all succeed)

These show how reliable each learned condition is on normal runs.

| Condition | Violations |
|---|---|
| release-and-retreat / over all / nut-at-peg / True | 1 |
| release-and-retreat / at end / nut-on-peg / True | 1 |
