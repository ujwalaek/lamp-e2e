# Square: stage-aware durative monitor

| Test case | Runs | Really failed | Flagged | Meaning |
|---|---|---|---|---|
| nominal (recorded, all succeed) | 20 | - | 7 | false alarms |
| drop (physics rollout) | 20 | 20 | 20 | detected |
| miss (physics rollout) | 20 | 20 | 20 | detected |

## False alarms (nominal runs flagged)

| Stage | Condition | Predicate | Why outside | Pose typical of training? | Count |
|---|---|---|---|---|---|
| insert-nut | at end | nut-at-peg | position and rotation | yes | 2 |
| release-and-retreat | at start | nut-at-peg | position and rotation | yes | 2 |
| move-nut-to-peg | at end | nut-at-peg | position and rotation | yes | 2 |
| insert-nut | at start | nut-at-peg | position and rotation | yes | 2 |
| move-nut-to-peg | at end | nut-at-peg | position only | yes | 1 |
| insert-nut | at start | nut-at-peg | position only | yes | 1 |
| approach-nut | at end | ready-to-grasp | grasp+pos | yes | 1 |
| move-nut-to-peg | at start | holding | position only | yes | 1 |
| move-nut-to-peg | over all | holding | position only | yes | 1 |
| release-and-retreat | at end | holding | inside region it should not be in | no | 1 |

### Every false alarm

- **demo_5**, stage `insert-nut`, at end `nut-at-peg`: not true within 9 frames of the stage end (nearest: 11 frames away). Relative pose (nut_1->peg_1) pos [-0.3, 2.7, -4.6] cm, rpy [30.0, -5.0, 10.0] deg. Outside learned bins: y bin 6 (region 7); roll bin 7 (region 6). Nearest training pose distance 0.42 (99th pct 0.81).
- **demo_5**, stage `release-and-retreat`, at start `nut-at-peg`: not true within 9 frames of the stage start (nearest: 10 frames away). Relative pose (nut_1->peg_1) pos [-0.3, 2.2, -4.3] cm, rpy [29.0, -5.0, 10.0] deg. Outside learned bins: y bin 6 (region 7); roll bin 7 (region 6). Nearest training pose distance 0.34 (99th pct 1.06).
- **demo_21**, stage `move-nut-to-peg`, at end `nut-at-peg`: not true within 1 frames of the stage end (nearest: 2 frames away). Relative pose (nut_1->peg_1) pos [0.3, -1.3, -9.4] cm, rpy [-6.0, -0.0, -8.0] deg. Outside learned bins: y bin 8 (region 7). Nearest training pose distance 0.49 (99th pct 2.06).
- **demo_21**, stage `insert-nut`, at start `nut-at-peg`: not true within 0 frames of the stage start (nearest: 1 frames away). Relative pose (nut_1->peg_1) pos [0.1, -1.1, -8.9] cm, rpy [-6.0, -1.0, -7.0] deg. Outside learned bins: y bin 8 (region 7). Nearest training pose distance 0.37 (99th pct 1.06).
- **demo_125**, stage `move-nut-to-peg`, at end `nut-at-peg`: not true within 1 frames of the stage end (nearest: 10 frames away). Relative pose (nut_1->peg_1) pos [1.2, 2.9, -8.0] cm, rpy [17.0, -3.0, -4.0] deg. Outside learned bins: x bin 8 (region 7); y bin 6 (region 7); roll bin 7 (region 6). Nearest training pose distance 0.71 (99th pct 2.06).
- **demo_125**, stage `insert-nut`, at start `nut-at-peg`: not true within 0 frames of the stage start (nearest: 9 frames away). Relative pose (nut_1->peg_1) pos [1.2, 2.8, -7.8] cm, rpy [17.0, -3.0, -4.0] deg. Outside learned bins: x bin 8 (region 7); y bin 6 (region 7); roll bin 7 (region 6). Nearest training pose distance 0.64 (99th pct 1.06).
- **demo_131**, stage `approach-nut`, at end `ready-to-grasp`: not true within 5 frames of the stage end (nearest: 9 frames away). Relative pose (gripper_1->nut_1) pos [-6.3, 2.0, 0.3] cm, rpy [-3.0, 5.0, -4.0] deg. Outside learned bins: y bin 13 (region 14); grasp sensor 0 (region 1). Nearest training pose distance 0.20 (99th pct 1.54).
- **demo_131**, stage `move-nut-to-peg`, at start `holding`: not true within 5 frames of the stage start (nearest: 8 frames away). Relative pose (gripper_1->nut_1) pos [-6.4, 1.9, 0.3] cm, rpy [-3.0, 5.0, -3.0] deg. Outside learned bins: y bin 13 (region 14). Nearest training pose distance 0.28 (99th pct 0.73).
- **demo_168**, stage `move-nut-to-peg`, over all `holding`: false for 52 of 54 frames in a row (tolerance 90% of stage). Relative pose (gripper_1->nut_1) pos [7.5, 1.2, -1.5] cm, rpy [5.0, -7.0, -176.0] deg. Outside learned bins: z bin 13 (region 14). Nearest training pose distance 0.19 (99th pct 0.73).
- **demo_180**, stage `move-nut-to-peg`, at end `nut-at-peg`: not true within 1 frames of the stage end (nearest: 23 frames away). Relative pose (nut_1->peg_1) pos [-0.0, 2.1, -6.7] cm, rpy [17.0, -6.0, 19.0] deg. Outside learned bins: y bin 6 (region 7); roll bin 7 (region 6); yaw bin 7 (region 6). Nearest training pose distance 0.84 (99th pct 2.06).
- **demo_180**, stage `insert-nut`, at start `nut-at-peg`: not true within 0 frames of the stage start (nearest: 22 frames away). Relative pose (nut_1->peg_1) pos [-0.1, 1.8, -5.4] cm, rpy [19.0, -6.0, 18.0] deg. Outside learned bins: y bin 6 (region 7); roll bin 7 (region 6); yaw bin 7 (region 6). Nearest training pose distance 0.50 (99th pct 1.06).
- **demo_180**, stage `insert-nut`, at end `nut-at-peg`: not true within 9 frames of the stage end (nearest: 22 frames away). Relative pose (nut_1->peg_1) pos [-0.1, 1.8, -5.4] cm, rpy [19.0, -6.0, 18.0] deg. Outside learned bins: y bin 6 (region 7); roll bin 7 (region 6); yaw bin 7 (region 6). Nearest training pose distance 0.50 (99th pct 1.06).
- **demo_180**, stage `release-and-retreat`, at start `nut-at-peg`: not true within 9 frames of the stage start (nearest: 22 frames away). Relative pose (nut_1->peg_1) pos [-0.1, 1.8, -5.4] cm, rpy [19.0, -6.0, 18.0] deg. Outside learned bins: y bin 6 (region 7); roll bin 7 (region 6); yaw bin 7 (region 6). Nearest training pose distance 0.50 (99th pct 1.06).
- **demo_191**, stage `release-and-retreat`, at end `holding` (should be false): not true within 0 frames of the stage end (nearest: 1 frames away). Relative pose (gripper_1->nut_1) pos [-6.6, -4.0, -13.3] cm, rpy [-3.0, 6.0, 18.0] deg. inside region it should not be in. Nearest training pose distance 6.21 (99th pct 0.89).

## Drop: detections and misses

First condition violated in each detected run:

| Stage | Condition | Predicate | Runs |
|---|---|---|---|
| move-nut-to-peg | at end | nut-at-peg | 19 |
| approach-nut | at end | ready-to-grasp | 1 |

Missed (0): none

## Miss: detections and misses

First condition violated in each detected run:

| Stage | Condition | Predicate | Runs |
|---|---|---|---|
| move-nut-to-peg | at end | nut-at-peg | 19 |
| approach-nut | at end | ready-to-grasp | 1 |

Missed (0): none

## Condition violations on the 180 training demos (all succeed)

These show how reliable each learned condition is on normal runs.

| Condition | Violations |
|---|---|
| release-and-retreat / at end / nut-on-peg / True | 22 |
| move-nut-to-peg / at start / holding / True | 14 |
| move-nut-to-peg / at end / nut-at-peg / True | 10 |
| insert-nut / at start / nut-at-peg / True | 10 |
| insert-nut / at end / nut-at-peg / True | 9 |
| release-and-retreat / at start / nut-at-peg / True | 9 |
| move-nut-to-peg / over all / holding / True | 9 |
| approach-nut / at end / ready-to-grasp / True | 9 |
