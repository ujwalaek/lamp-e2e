# Square: stage-aware durative monitor

| Test case | Runs | Really failed | Flagged | Meaning |
|---|---|---|---|---|
| nominal (recorded, all succeed) | 20 | - | 9 | false alarms |
| drop (physics rollout) | 20 | 20 | 20 | detected |
| miss (physics rollout) | 20 | 20 | 20 | detected |

## False alarms (nominal runs flagged)

| Stage | Condition | Predicate | Why outside | Pose typical of training? | Count |
|---|---|---|---|---|---|
| move-nut-to-peg | at end | nut-at-peg | position and rotation | yes | 3 |
| insert-nut | at start | nut-at-peg | position and rotation | yes | 3 |
| insert-nut | at end | nut-at-peg | position and rotation | yes | 3 |
| release-and-retreat | at start | nut-at-peg | position and rotation | yes | 3 |
| approach-nut | at end | ready-to-grasp | position only | yes | 2 |
| approach-nut | at end | ready-to-grasp |  | yes | 2 |
| approach-nut | at end | ready-to-grasp | grasp flag | yes | 1 |
| insert-nut | over all | holding | position and rotation | yes | 1 |
| move-nut-to-peg | at end | nut-at-peg | position only | yes | 1 |
| insert-nut | at start | nut-at-peg | position only | yes | 1 |
| move-nut-to-peg | over all | holding | position and rotation | yes | 1 |
| move-nut-to-peg | over all | holding | position only | yes | 1 |
| release-and-retreat | over all | nut-at-peg | position and rotation | yes | 1 |
| insert-nut | over all | holding | grasp flag | no | 1 |
| release-and-retreat | at end | holding | inside region it should not be in | no | 1 |

### Every false alarm

- **demo_5**, stage `move-nut-to-peg`, at end `nut-at-peg`: not true within 5 frames of the stage end (nearest: 11 frames away). Relative pose (nut_1->peg_1) pos [-0.3, 2.7, -4.6] cm, rpy [30.0, -5.0, 10.0] deg. Outside learned bins: y bin 6 (region 7); roll bin 7 (region 6). Nearest training pose distance 0.44 (99th pct 2.02).
- **demo_5**, stage `insert-nut`, at start `nut-at-peg`: not true within 4 frames of the stage start (nearest: 10 frames away). Relative pose (nut_1->peg_1) pos [-0.3, 2.2, -4.3] cm, rpy [29.0, -5.0, 10.0] deg. Outside learned bins: y bin 6 (region 7); roll bin 7 (region 6). Nearest training pose distance 0.34 (99th pct 1.06).
- **demo_5**, stage `insert-nut`, at end `nut-at-peg`: not true within 8 frames of the stage end (nearest: 10 frames away). Relative pose (nut_1->peg_1) pos [-0.3, 2.2, -4.3] cm, rpy [29.0, -5.0, 10.0] deg. Outside learned bins: y bin 6 (region 7); roll bin 7 (region 6). Nearest training pose distance 0.34 (99th pct 1.06).
- **demo_5**, stage `release-and-retreat`, at start `nut-at-peg`: not true within 8 frames of the stage start (nearest: 10 frames away). Relative pose (nut_1->peg_1) pos [-0.3, 2.2, -4.3] cm, rpy [29.0, -5.0, 10.0] deg. Outside learned bins: y bin 6 (region 7); roll bin 7 (region 6). Nearest training pose distance 0.34 (99th pct 1.06).
- **demo_21**, stage `approach-nut`, at end `ready-to-grasp`: not true within 6 frames of the stage end (nearest: 33 frames away). Relative pose (gripper_1->nut_1) pos [4.8, 0.2, -1.9] cm, rpy [3.0, -9.0, -180.0] deg. Outside learned bins: z bin 13 (region 14). Nearest training pose distance 0.35 (99th pct 1.54).
- **demo_27**, stage `approach-nut`, at end `ready-to-grasp`: not true within 6 frames of the stage end (nearest: 19 frames away). Relative pose (gripper_1->nut_1) pos [7.3, 1.4, -1.3] cm, rpy [6.0, -6.0, 179.0] deg. Outside learned bins: grasp sensor 0 (region 1). Nearest training pose distance 0.21 (99th pct 1.54).
- **demo_27**, stage `insert-nut`, over all `holding`: false for 10 of 35 frames in a row (tolerance 0% of stage). Relative pose (gripper_1->nut_1) pos [6.8, -1.6, -2.2] cm, rpy [16.0, -9.0, 172.0] deg. Outside learned bins: y bin 15 (region 14); z bin 13 (region 14); pitch bin 7 (region 6). Nearest training pose distance 0.75 (99th pct 0.76).
- **demo_93**, stage `approach-nut`, at end `ready-to-grasp`: not true within 6 frames of the stage end (nearest: 31 frames away). Relative pose (gripper_1->nut_1) pos [6.4, -0.2, -1.4] cm, rpy [9.0, -6.0, -179.0] deg. . Nearest training pose distance 0.21 (99th pct 1.54).
- **demo_105**, stage `approach-nut`, at end `ready-to-grasp`: not true within 6 frames of the stage end (nearest: 10 frames away). Relative pose (gripper_1->nut_1) pos [7.1, 2.5, -0.9] cm, rpy [4.0, -4.0, -173.0] deg. Outside learned bins: y bin 13 (region 14). Nearest training pose distance 0.22 (99th pct 1.54).
- **demo_105**, stage `move-nut-to-peg`, at end `nut-at-peg`: not true within 5 frames of the stage end (nearest: 6 frames away). Relative pose (nut_1->peg_1) pos [-1.0, 1.4, -8.4] cm, rpy [11.0, 1.0, 9.0] deg. Outside learned bins: y bin 6 (region 7). Nearest training pose distance 0.32 (99th pct 2.02).
- **demo_105**, stage `insert-nut`, at start `nut-at-peg`: not true within 4 frames of the stage start (nearest: 5 frames away). Relative pose (nut_1->peg_1) pos [-0.9, 1.3, -8.1] cm, rpy [11.0, 0.0, 8.0] deg. Outside learned bins: y bin 6 (region 7). Nearest training pose distance 0.57 (99th pct 1.06).
- **demo_125**, stage `move-nut-to-peg`, over all `holding`: false for 5 of 84 frames in a row (tolerance 1% of stage). Relative pose (gripper_1->nut_1) pos [-6.1, 0.7, 1.7] cm, rpy [-26.0, 10.0, 1.0] deg. Outside learned bins: z bin 15 (region 14); roll bin 5 (region 6). Nearest training pose distance 0.29 (99th pct 0.75).
- **demo_125**, stage `move-nut-to-peg`, at end `nut-at-peg`: not true within 5 frames of the stage end (nearest: 10 frames away). Relative pose (nut_1->peg_1) pos [1.2, 2.9, -8.0] cm, rpy [17.0, -3.0, -4.0] deg. Outside learned bins: x bin 8 (region 7); y bin 6 (region 7); roll bin 7 (region 6). Nearest training pose distance 0.62 (99th pct 2.02).
- **demo_125**, stage `insert-nut`, at start `nut-at-peg`: not true within 4 frames of the stage start (nearest: 9 frames away). Relative pose (nut_1->peg_1) pos [1.2, 2.8, -7.8] cm, rpy [17.0, -3.0, -4.0] deg. Outside learned bins: x bin 8 (region 7); y bin 6 (region 7); roll bin 7 (region 6). Nearest training pose distance 0.64 (99th pct 1.06).
- **demo_125**, stage `insert-nut`, at end `nut-at-peg`: not true within 8 frames of the stage end (nearest: 9 frames away). Relative pose (nut_1->peg_1) pos [1.2, 2.8, -7.8] cm, rpy [17.0, -3.0, -4.0] deg. Outside learned bins: x bin 8 (region 7); y bin 6 (region 7); roll bin 7 (region 6). Nearest training pose distance 0.64 (99th pct 1.06).
- **demo_125**, stage `release-and-retreat`, at start `nut-at-peg`: not true within 8 frames of the stage start (nearest: 9 frames away). Relative pose (nut_1->peg_1) pos [1.2, 2.8, -7.8] cm, rpy [17.0, -3.0, -4.0] deg. Outside learned bins: x bin 8 (region 7); y bin 6 (region 7); roll bin 7 (region 6). Nearest training pose distance 0.64 (99th pct 1.06).
- **demo_168**, stage `approach-nut`, at end `ready-to-grasp`: not true within 6 frames of the stage end (nearest: 11 frames away). Relative pose (gripper_1->nut_1) pos [7.3, 1.5, -1.3] cm, rpy [5.0, -6.0, -174.0] deg. . Nearest training pose distance 0.16 (99th pct 1.54).
- **demo_180**, stage `move-nut-to-peg`, over all `holding`: false for 5 of 111 frames in a row (tolerance 1% of stage). Relative pose (gripper_1->nut_1) pos [-5.5, 1.1, 2.7] cm, rpy [-9.0, 9.0, -0.0] deg. Outside learned bins: z bin 15 (region 14). Nearest training pose distance 0.57 (99th pct 0.75).
- **demo_180**, stage `move-nut-to-peg`, at end `nut-at-peg`: not true within 5 frames of the stage end (nearest: 23 frames away). Relative pose (nut_1->peg_1) pos [-0.0, 2.1, -6.7] cm, rpy [17.0, -6.0, 19.0] deg. Outside learned bins: y bin 6 (region 7); roll bin 7 (region 6); yaw bin 7 (region 6). Nearest training pose distance 0.74 (99th pct 2.02).
- **demo_180**, stage `insert-nut`, at start `nut-at-peg`: not true within 4 frames of the stage start (nearest: 22 frames away). Relative pose (nut_1->peg_1) pos [-0.1, 1.8, -5.4] cm, rpy [19.0, -6.0, 18.0] deg. Outside learned bins: y bin 6 (region 7); roll bin 7 (region 6); yaw bin 7 (region 6). Nearest training pose distance 0.50 (99th pct 1.06).
- **demo_180**, stage `insert-nut`, at end `nut-at-peg`: not true within 8 frames of the stage end (nearest: 22 frames away). Relative pose (nut_1->peg_1) pos [-0.1, 1.8, -5.4] cm, rpy [19.0, -6.0, 18.0] deg. Outside learned bins: y bin 6 (region 7); roll bin 7 (region 6); yaw bin 7 (region 6). Nearest training pose distance 0.50 (99th pct 1.06).
- **demo_180**, stage `release-and-retreat`, at start `nut-at-peg`: not true within 8 frames of the stage start (nearest: 22 frames away). Relative pose (nut_1->peg_1) pos [-0.1, 1.8, -5.4] cm, rpy [19.0, -6.0, 18.0] deg. Outside learned bins: y bin 6 (region 7); roll bin 7 (region 6); yaw bin 7 (region 6). Nearest training pose distance 0.50 (99th pct 1.06).
- **demo_180**, stage `release-and-retreat`, over all `nut-at-peg`: false for 22 of 25 frames in a row (tolerance 81% of stage). Relative pose (nut_1->peg_1) pos [-0.1, 1.8, -5.4] cm, rpy [19.0, -6.0, 18.0] deg. Outside learned bins: y bin 6 (region 7); roll bin 7 (region 6); yaw bin 7 (region 6). Nearest training pose distance 0.50 (99th pct 1.06).
- **demo_191**, stage `insert-nut`, over all `holding`: false for 39 of 53 frames in a row (tolerance 0% of stage). Relative pose (gripper_1->nut_1) pos [-5.3, -0.2, 0.4] cm, rpy [-1.0, 7.0, 1.0] deg. Outside learned bins: grasp sensor 0 (region 1). Nearest training pose distance n/a (99th pct n/a).
- **demo_191**, stage `release-and-retreat`, at end `holding` (should be false): not true within 0 frames of the stage end (nearest: 1 frames away). Relative pose (gripper_1->nut_1) pos [-6.6, -4.0, -13.3] cm, rpy [-3.0, 6.0, 18.0] deg. inside region it should not be in. Nearest training pose distance 6.21 (99th pct 0.76).

## Drop: detections and misses

First condition violated in each detected run:

| Stage | Condition | Predicate | Runs |
|---|---|---|---|
| move-nut-to-peg | at end | nut-at-peg | 15 |
| approach-nut | at end | ready-to-grasp | 5 |

Missed (0): none

## Miss: detections and misses

First condition violated in each detected run:

| Stage | Condition | Predicate | Runs |
|---|---|---|---|
| move-nut-to-peg | at end | nut-at-peg | 13 |
| approach-nut | at end | ready-to-grasp | 5 |
| move-nut-to-peg | over all | holding | 2 |

Missed (0): none

## Condition violations on the 180 training demos (all succeed)

These show how reliable each learned condition is on normal runs.

| Condition | Violations |
|---|---|
| release-and-retreat / at end / nut-on-peg / True | 12 |
| insert-nut / at end / nut-at-peg / True | 11 |
| move-nut-to-peg / at end / nut-at-peg / True | 11 |
| insert-nut / at start / nut-at-peg / True | 11 |
| release-and-retreat / at start / nut-at-peg / True | 10 |
| approach-nut / at end / ready-to-grasp / True | 10 |
| release-and-retreat / over all / nut-at-peg / True | 9 |
| move-nut-to-peg / over all / holding / True | 7 |
| insert-nut / over all / holding / True | 4 |
| move-nut-to-peg / at start / holding / True | 2 |
