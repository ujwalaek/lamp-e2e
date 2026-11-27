# Square: stage-aware durative monitor

| Test case | Runs | Really failed | Flagged | Meaning |
|---|---|---|---|---|
| nominal (recorded, all succeed) | 20 | - | 10 | false alarms |
| drop (physics rollout) | 20 | 20 | 20 | detected |
| miss (physics rollout) | 20 | 20 | 20 | detected |

## False alarms (nominal runs flagged)

| Stage | Condition | Predicate | Why outside | Pose typical of training? | Count |
|---|---|---|---|---|---|
| release-and-retreat | over all | nut-at-peg | position and rotation | yes | 4 |
| approach-nut | at end | ready-to-grasp | position and rotation | yes | 3 |
| move-nut-to-peg | at start | holding | ang+grasp+pos | yes | 3 |
| release-and-retreat | over all | nut-at-peg | position only | yes | 2 |
| move-nut-to-peg | at end | nut-at-peg | position and rotation | no | 2 |
| insert-nut | at start | nut-at-peg | position and rotation | no | 2 |
| insert-nut | at end | nut-at-peg | position and rotation | no | 2 |
| release-and-retreat | at start | nut-at-peg | position and rotation | no | 2 |
| release-and-retreat | over all | nut-at-peg | position and rotation | no | 2 |
| insert-nut | over all | holding | position and rotation | yes | 1 |
| move-nut-to-peg | at end | nut-at-peg | position only | no | 1 |
| insert-nut | at start | nut-at-peg | position only | no | 1 |
| insert-nut | at end | nut-at-peg | position only | no | 1 |
| release-and-retreat | at start | nut-at-peg | position only | no | 1 |
| release-and-retreat | over all | nut-at-peg | position only | no | 1 |
| move-nut-to-peg | at end | nut-at-peg | position and rotation | yes | 1 |
| insert-nut | at start | nut-at-peg | position and rotation | yes | 1 |
| insert-nut | at end | nut-at-peg | position and rotation | yes | 1 |
| release-and-retreat | at start | nut-at-peg | position and rotation | yes | 1 |
| insert-nut | over all | holding | grasp flag | yes | 1 |
| release-and-retreat | at end | holding | inside region it should not be in | no | 1 |

### Every false alarm

- **demo_5**, stage `release-and-retreat`, over all `nut-at-peg`: false for 10 of 13 frames in a row (tolerance 100% of stage). Relative pose (nut_1->peg_1) pos [-0.3, 2.2, -4.3] cm, rpy [29.0, -5.0, 10.0] deg. Outside learned bins: y bin 6 (region 7); roll bin 7 (region 6). Nearest training pose distance 0.34 (99th pct 1.69).
- **demo_27**, stage `insert-nut`, over all `holding`: false for 11 of 11 frames in a row (tolerance 100% of stage). Relative pose (gripper_1->nut_1) pos [6.8, -1.6, -2.2] cm, rpy [14.0, -9.0, 172.0] deg. Outside learned bins: y bin 15 (region 14); z bin 13 (region 14); pitch bin 7 (region 6). Nearest training pose distance 0.69 (99th pct 0.76).
- **demo_27**, stage `release-and-retreat`, over all `nut-at-peg`: false for 13 of 18 frames in a row (tolerance 100% of stage). Relative pose (nut_1->peg_1) pos [-1.1, -2.3, -6.1] cm, rpy [-20.0, 7.0, 7.0] deg. Outside learned bins: x bin 6 (region 7); y bin 8 (region 7); roll bin 5 (region 6). Nearest training pose distance 0.81 (99th pct 1.69).
- **demo_36**, stage `release-and-retreat`, over all `nut-at-peg`: false for 3 of 11 frames in a row (tolerance 100% of stage). Relative pose (nut_1->peg_1) pos [-1.1, -0.5, -8.1] cm, rpy [1.0, 4.0, 6.0] deg. Outside learned bins: x bin 6 (region 7). Nearest training pose distance 0.29 (99th pct 1.69).
- **demo_105**, stage `approach-nut`, at end `ready-to-grasp`: not true within 20 frames of the stage end (nearest: 48 frames away). Relative pose (gripper_1->nut_1) pos [-0.9, 20.0, -11.0] cm, rpy [5.0, -3.0, 126.0] deg. Outside learned bins: x bin 14 (region 16); y bin 7 (region 14); z bin 10 (region 13); yaw bin 10 (region 11). Nearest training pose distance 0.86 (99th pct 4.80).
- **demo_105**, stage `move-nut-to-peg`, at start `holding`: not true within 20 frames of the stage start (nearest: 63 frames away). Relative pose (gripper_1->nut_1) pos [-0.9, 20.0, -11.0] cm, rpy [5.0, -3.0, 126.0] deg. Outside learned bins: x bin 14 (region 16); y bin 7 (region 14); z bin 10 (region 14); yaw bin 10 (region 11); grasp sensor 0 (region 1). Nearest training pose distance 0.86 (99th pct 4.80).
- **demo_105**, stage `move-nut-to-peg`, at end `nut-at-peg`: not true within 20 frames of the stage end (nearest: 126 frames away). Relative pose (nut_1->peg_1) pos [-27.6, -22.5, -4.0] cm, rpy [-0.0, -0.0, -36.0] deg. Outside learned bins: x bin -1 (region 7); y bin -1 (region 7); yaw bin 5 (region 6). Nearest training pose distance 2.51 (99th pct 1.69).
- **demo_105**, stage `insert-nut`, at start `nut-at-peg`: not true within 20 frames of the stage start (nearest: 126 frames away). Relative pose (nut_1->peg_1) pos [-27.6, -22.5, -4.0] cm, rpy [-0.0, -0.0, -36.0] deg. Outside learned bins: x bin -1 (region 7); y bin -1 (region 7); yaw bin 5 (region 6). Nearest training pose distance 2.51 (99th pct 1.69).
- **demo_105**, stage `insert-nut`, at end `nut-at-peg`: not true within 20 frames of the stage end (nearest: 126 frames away). Relative pose (nut_1->peg_1) pos [-27.6, -22.5, -4.0] cm, rpy [-0.0, -0.0, -36.0] deg. Outside learned bins: x bin -1 (region 7); y bin -1 (region 7); yaw bin 5 (region 6). Nearest training pose distance 2.51 (99th pct 1.69).
- **demo_105**, stage `release-and-retreat`, at start `nut-at-peg`: not true within 20 frames of the stage start (nearest: 126 frames away). Relative pose (nut_1->peg_1) pos [-27.6, -22.5, -4.0] cm, rpy [-0.0, -0.0, -36.0] deg. Outside learned bins: x bin -1 (region 7); y bin -1 (region 7); yaw bin 5 (region 6). Nearest training pose distance 2.51 (99th pct 1.69).
- **demo_105**, stage `release-and-retreat`, over all `nut-at-peg`: false for 126 of 154 frames in a row (tolerance 100% of stage). Relative pose (nut_1->peg_1) pos [-27.6, -22.5, -4.0] cm, rpy [-0.0, -0.0, -36.0] deg. Outside learned bins: x bin -1 (region 7); y bin -1 (region 7); yaw bin 5 (region 6). Nearest training pose distance 2.51 (99th pct 1.69).
- **demo_111**, stage `release-and-retreat`, over all `nut-at-peg`: false for 5 of 11 frames in a row (tolerance 100% of stage). Relative pose (nut_1->peg_1) pos [0.8, -1.0, -7.4] cm, rpy [-3.0, -9.0, -0.0] deg. Outside learned bins: y bin 8 (region 7). Nearest training pose distance 0.48 (99th pct 1.69).
- **demo_125**, stage `release-and-retreat`, over all `nut-at-peg`: false for 9 of 12 frames in a row (tolerance 100% of stage). Relative pose (nut_1->peg_1) pos [1.2, 2.8, -7.8] cm, rpy [17.0, -3.0, -4.0] deg. Outside learned bins: x bin 8 (region 7); y bin 6 (region 7); roll bin 7 (region 6). Nearest training pose distance 0.64 (99th pct 1.69).
- **demo_131**, stage `approach-nut`, at end `ready-to-grasp`: not true within 20 frames of the stage end (nearest: 50 frames away). Relative pose (gripper_1->nut_1) pos [-0.3, 18.9, -10.5] cm, rpy [-4.0, 2.0, -66.0] deg. Outside learned bins: x bin 14 (region 16); y bin 8 (region 14); z bin 11 (region 14); yaw bin 4 (region 1). Nearest training pose distance 2.47 (99th pct 4.80).
- **demo_131**, stage `move-nut-to-peg`, at start `holding`: not true within 20 frames of the stage start (nearest: 50 frames away). Relative pose (gripper_1->nut_1) pos [-0.3, 18.9, -10.5] cm, rpy [-4.0, 2.0, -66.0] deg. Outside learned bins: x bin 14 (region 12); y bin 8 (region 14); z bin 11 (region 14); yaw bin 4 (region 6); grasp sensor 0 (region 1). Nearest training pose distance 2.47 (99th pct 4.80).
- **demo_131**, stage `move-nut-to-peg`, at end `nut-at-peg`: not true within 20 frames of the stage end (nearest: 117 frames away). Relative pose (nut_1->peg_1) pos [19.3, 29.4, -4.0] cm, rpy [0.0, 0.0, -22.0] deg. Outside learned bins: x bin -1 (region 7); y bin -1 (region 7); yaw bin 5 (region 6). Nearest training pose distance 4.49 (99th pct 1.69).
- **demo_131**, stage `insert-nut`, at start `nut-at-peg`: not true within 20 frames of the stage start (nearest: 117 frames away). Relative pose (nut_1->peg_1) pos [19.3, 29.4, -4.0] cm, rpy [0.0, 0.0, -22.0] deg. Outside learned bins: x bin -1 (region 7); y bin -1 (region 7); yaw bin 5 (region 6). Nearest training pose distance 4.49 (99th pct 1.69).
- **demo_131**, stage `insert-nut`, at end `nut-at-peg`: not true within 20 frames of the stage end (nearest: 117 frames away). Relative pose (nut_1->peg_1) pos [19.3, 29.4, -4.0] cm, rpy [0.0, 0.0, -22.0] deg. Outside learned bins: x bin -1 (region 7); y bin -1 (region 7); yaw bin 5 (region 6). Nearest training pose distance 4.49 (99th pct 1.69).
- **demo_131**, stage `release-and-retreat`, at start `nut-at-peg`: not true within 20 frames of the stage start (nearest: 117 frames away). Relative pose (nut_1->peg_1) pos [19.3, 29.4, -4.0] cm, rpy [0.0, 0.0, -22.0] deg. Outside learned bins: x bin -1 (region 7); y bin -1 (region 7); yaw bin 5 (region 6). Nearest training pose distance 4.49 (99th pct 1.69).
- **demo_131**, stage `release-and-retreat`, over all `nut-at-peg`: false for 117 of 136 frames in a row (tolerance 100% of stage). Relative pose (nut_1->peg_1) pos [19.3, 29.4, -4.0] cm, rpy [0.0, 0.0, -22.0] deg. Outside learned bins: x bin -1 (region 7); y bin -1 (region 7); yaw bin 5 (region 6). Nearest training pose distance 4.49 (99th pct 1.69).
- **demo_168**, stage `approach-nut`, at end `ready-to-grasp`: not true within 20 frames of the stage end (nearest: 37 frames away). Relative pose (gripper_1->nut_1) pos [0.3, 21.5, -10.3] cm, rpy [2.0, -0.0, 106.0] deg. Outside learned bins: x bin 14 (region 16); y bin 7 (region 14); z bin 11 (region 13); yaw bin 9 (region 11). Nearest training pose distance 1.28 (99th pct 4.80).
- **demo_168**, stage `move-nut-to-peg`, at start `holding`: not true within 20 frames of the stage start (nearest: 90 frames away). Relative pose (gripper_1->nut_1) pos [0.3, 21.5, -10.3] cm, rpy [2.0, -0.0, 106.0] deg. Outside learned bins: x bin 14 (region 16); y bin 7 (region 14); z bin 11 (region 14); yaw bin 9 (region 11); grasp sensor 0 (region 1). Nearest training pose distance 1.28 (99th pct 4.80).
- **demo_168**, stage `move-nut-to-peg`, at end `nut-at-peg`: not true within 20 frames of the stage end (nearest: 140 frames away). Relative pose (nut_1->peg_1) pos [-19.4, -30.5, -4.0] cm, rpy [-0.0, -0.0, -15.0] deg. Outside learned bins: x bin -1 (region 7); y bin -1 (region 7). Nearest training pose distance 3.08 (99th pct 1.69).
- **demo_168**, stage `insert-nut`, at start `nut-at-peg`: not true within 20 frames of the stage start (nearest: 140 frames away). Relative pose (nut_1->peg_1) pos [-19.4, -30.5, -4.0] cm, rpy [-0.0, -0.0, -15.0] deg. Outside learned bins: x bin -1 (region 7); y bin -1 (region 7). Nearest training pose distance 3.08 (99th pct 1.69).
- **demo_168**, stage `insert-nut`, at end `nut-at-peg`: not true within 20 frames of the stage end (nearest: 140 frames away). Relative pose (nut_1->peg_1) pos [-19.4, -30.5, -4.0] cm, rpy [-0.0, -0.0, -15.0] deg. Outside learned bins: x bin -1 (region 7); y bin -1 (region 7). Nearest training pose distance 3.08 (99th pct 1.69).
- **demo_168**, stage `release-and-retreat`, at start `nut-at-peg`: not true within 20 frames of the stage start (nearest: 140 frames away). Relative pose (nut_1->peg_1) pos [-19.4, -30.5, -4.0] cm, rpy [-0.0, -0.0, -15.0] deg. Outside learned bins: x bin -1 (region 7); y bin -1 (region 7). Nearest training pose distance 3.08 (99th pct 1.69).
- **demo_168**, stage `release-and-retreat`, over all `nut-at-peg`: false for 140 of 169 frames in a row (tolerance 100% of stage). Relative pose (nut_1->peg_1) pos [-19.4, -30.5, -4.0] cm, rpy [-0.0, -0.0, -15.0] deg. Outside learned bins: x bin -1 (region 7); y bin -1 (region 7). Nearest training pose distance 3.08 (99th pct 1.69).
- **demo_180**, stage `move-nut-to-peg`, at end `nut-at-peg`: not true within 20 frames of the stage end (nearest: 23 frames away). Relative pose (nut_1->peg_1) pos [-0.0, 2.1, -6.7] cm, rpy [17.0, -6.0, 19.0] deg. Outside learned bins: y bin 6 (region 7); roll bin 7 (region 6); yaw bin 7 (region 6). Nearest training pose distance 0.76 (99th pct 2.10).
- **demo_180**, stage `insert-nut`, at start `nut-at-peg`: not true within 20 frames of the stage start (nearest: 22 frames away). Relative pose (nut_1->peg_1) pos [-0.1, 1.8, -5.4] cm, rpy [19.0, -6.0, 18.0] deg. Outside learned bins: y bin 6 (region 7); roll bin 7 (region 6); yaw bin 7 (region 6). Nearest training pose distance 0.50 (99th pct 1.69).
- **demo_180**, stage `insert-nut`, at end `nut-at-peg`: not true within 20 frames of the stage end (nearest: 22 frames away). Relative pose (nut_1->peg_1) pos [-0.1, 1.8, -5.4] cm, rpy [19.0, -6.0, 18.0] deg. Outside learned bins: y bin 6 (region 7); roll bin 7 (region 6); yaw bin 7 (region 6). Nearest training pose distance 0.50 (99th pct 1.69).
- **demo_180**, stage `release-and-retreat`, at start `nut-at-peg`: not true within 20 frames of the stage start (nearest: 22 frames away). Relative pose (nut_1->peg_1) pos [-0.1, 1.8, -5.4] cm, rpy [19.0, -6.0, 18.0] deg. Outside learned bins: y bin 6 (region 7); roll bin 7 (region 6); yaw bin 7 (region 6). Nearest training pose distance 0.50 (99th pct 1.69).
- **demo_180**, stage `release-and-retreat`, over all `nut-at-peg`: false for 22 of 25 frames in a row (tolerance 100% of stage). Relative pose (nut_1->peg_1) pos [-0.1, 1.8, -5.4] cm, rpy [19.0, -6.0, 18.0] deg. Outside learned bins: y bin 6 (region 7); roll bin 7 (region 6); yaw bin 7 (region 6). Nearest training pose distance 0.50 (99th pct 1.69).
- **demo_191**, stage `insert-nut`, over all `holding`: false for 39 of 52 frames in a row (tolerance 100% of stage). Relative pose (gripper_1->nut_1) pos [-5.3, -0.2, 0.4] cm, rpy [-1.0, 7.0, 1.0] deg. Outside learned bins: grasp sensor 0 (region 1). Nearest training pose distance 0.57 (99th pct 1.23).
- **demo_191**, stage `release-and-retreat`, at end `holding` (should be false): not true within 0 frames of the stage end (nearest: 1 frames away). Relative pose (gripper_1->nut_1) pos [-6.6, -4.0, -13.3] cm, rpy [-3.0, 6.0, 18.0] deg. inside region it should not be in. Nearest training pose distance 6.21 (99th pct 0.76).

## Drop: detections and misses

First condition violated in each detected run:

| Stage | Condition | Predicate | Runs |
|---|---|---|---|
| move-nut-to-peg | at end | nut-at-peg | 15 |
| approach-nut | at end | ready-to-grasp | 4 |
| release-and-retreat | over all | nut-at-peg | 1 |

Missed (0): none

## Miss: detections and misses

First condition violated in each detected run:

| Stage | Condition | Predicate | Runs |
|---|---|---|---|
| move-nut-to-peg | at end | nut-at-peg | 14 |
| approach-nut | at end | ready-to-grasp | 4 |
| move-nut-to-peg | over all | holding | 2 |

Missed (0): none

## Condition violations on the 180 training demos (all succeed)

These show how reliable each learned condition is on normal runs.

| Condition | Violations |
|---|---|
| release-and-retreat / over all / nut-at-peg / True | 76 |
| release-and-retreat / at start / nut-at-peg / True | 8 |
| insert-nut / at end / nut-at-peg / True | 7 |
| move-nut-to-peg / at end / nut-at-peg / True | 5 |
| insert-nut / at start / nut-at-peg / True | 5 |
| release-and-retreat / at end / nut-on-peg / True | 4 |
| insert-nut / over all / holding / True | 4 |
| approach-nut / at end / ready-to-grasp / True | 4 |
| move-nut-to-peg / at start / holding / True | 3 |
| move-nut-to-peg / over all / holding / True | 3 |
