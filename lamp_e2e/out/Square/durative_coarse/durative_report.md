# Square: stage-aware durative monitor

| Test case | Runs | Really failed | Flagged | Meaning |
|---|---|---|---|---|
| nominal (recorded, all succeed) | 20 | - | 13 | false alarms |
| drop (physics rollout) | 20 | 20 | 20 | detected |
| miss (physics rollout) | 20 | 20 | 20 | detected |

## False alarms (nominal runs flagged)

| Stage | Condition | Predicate | Why outside | Pose typical of training? | Count |
|---|---|---|---|---|---|
| release-and-retreat | at end | nut-on-peg | rotation only | yes | 8 |
| move-nut-to-peg | at end | nut-at-peg | position and rotation | yes | 7 |
| insert-nut | at start | nut-at-peg | position and rotation | yes | 5 |
| insert-nut | at end | nut-at-peg | position and rotation | yes | 5 |
| release-and-retreat | at start | nut-at-peg | position and rotation | yes | 5 |
| insert-nut | at start | nut-at-peg | rotation only | yes | 4 |
| insert-nut | at end | nut-at-peg | rotation only | yes | 4 |
| release-and-retreat | at start | nut-at-peg | rotation only | yes | 4 |
| move-nut-to-peg | at end | nut-at-peg | rotation only | yes | 3 |
| insert-nut | at start | nut-at-peg | position and rotation | no | 1 |
| approach-nut | at end | ready-to-grasp | grasp+pos | yes | 1 |
| move-nut-to-peg | at start | holding | position only | yes | 1 |
| move-nut-to-peg | over all | holding | position only | yes | 1 |
| release-and-retreat | at end | holding | inside region it should not be in | no | 1 |

### Every false alarm

- **demo_0**, stage `move-nut-to-peg`, at end `nut-at-peg`: not true within 6 frames of the stage end (nearest: never). Relative pose (nut_1->peg_1) pos [0.2, -0.8, -8.6] cm, rpy [3.0, 4.0, 177.0] deg. Outside learned bins: yaw bin 11 (region 9). Nearest training pose distance 0.24 (99th pct 1.61).
- **demo_0**, stage `insert-nut`, at start `nut-at-peg`: not true within 5 frames of the stage start (nearest: never). Relative pose (nut_1->peg_1) pos [0.2, -0.6, -7.9] cm, rpy [2.0, 4.0, 177.0] deg. Outside learned bins: yaw bin 11 (region 9). Nearest training pose distance 0.30 (99th pct 1.02).
- **demo_0**, stage `insert-nut`, at end `nut-at-peg`: not true within 8 frames of the stage end (nearest: never). Relative pose (nut_1->peg_1) pos [0.2, -0.6, -7.9] cm, rpy [2.0, 4.0, 177.0] deg. Outside learned bins: yaw bin 11 (region 9). Nearest training pose distance 0.30 (99th pct 1.02).
- **demo_0**, stage `release-and-retreat`, at start `nut-at-peg`: not true within 8 frames of the stage start (nearest: never). Relative pose (nut_1->peg_1) pos [0.2, -0.6, -7.9] cm, rpy [2.0, 4.0, 177.0] deg. Outside learned bins: yaw bin 11 (region 9). Nearest training pose distance 0.30 (99th pct 1.02).
- **demo_0**, stage `release-and-retreat`, at end `nut-on-peg`: not true within 5 frames of the stage end (nearest: never). Relative pose (nut_1->peg_1) pos [0.1, 0.1, 2.1] cm, rpy [-0.0, -0.0, 178.0] deg. Outside learned bins: yaw bin 11 (region 9). Nearest training pose distance 0.07 (99th pct 1.02).
- **demo_5**, stage `move-nut-to-peg`, at end `nut-at-peg`: not true within 6 frames of the stage end (nearest: 11 frames away). Relative pose (nut_1->peg_1) pos [-0.3, 2.7, -4.6] cm, rpy [6.0, 30.0, -77.0] deg. Outside learned bins: y bin 6 (region 7); roll bin 7 (region 6); pitch bin 7 (region 6); yaw bin 4 (region 3). Nearest training pose distance 0.42 (99th pct 1.61).
- **demo_5**, stage `insert-nut`, at start `nut-at-peg`: not true within 5 frames of the stage start (nearest: 10 frames away). Relative pose (nut_1->peg_1) pos [-0.3, 2.2, -4.3] cm, rpy [6.0, 29.0, -77.0] deg. Outside learned bins: y bin 6 (region 7); roll bin 7 (region 6); pitch bin 7 (region 6); yaw bin 4 (region 3). Nearest training pose distance 0.34 (99th pct 1.02).
- **demo_5**, stage `insert-nut`, at end `nut-at-peg`: not true within 8 frames of the stage end (nearest: 10 frames away). Relative pose (nut_1->peg_1) pos [-0.3, 2.2, -4.3] cm, rpy [6.0, 29.0, -77.0] deg. Outside learned bins: y bin 6 (region 7); roll bin 7 (region 6); pitch bin 7 (region 6); yaw bin 4 (region 3). Nearest training pose distance 0.34 (99th pct 1.02).
- **demo_5**, stage `release-and-retreat`, at start `nut-at-peg`: not true within 8 frames of the stage start (nearest: 10 frames away). Relative pose (nut_1->peg_1) pos [-0.3, 2.2, -4.3] cm, rpy [6.0, 29.0, -77.0] deg. Outside learned bins: y bin 6 (region 7); roll bin 7 (region 6); pitch bin 7 (region 6); yaw bin 4 (region 3). Nearest training pose distance 0.34 (99th pct 1.02).
- **demo_21**, stage `move-nut-to-peg`, at end `nut-at-peg`: not true within 6 frames of the stage end (nearest: never). Relative pose (nut_1->peg_1) pos [0.3, -1.3, -9.4] cm, rpy [6.0, 0.0, 172.0] deg. Outside learned bins: y bin 8 (region 7); yaw bin 11 (region 9). Nearest training pose distance 0.21 (99th pct 1.61).
- **demo_21**, stage `insert-nut`, at start `nut-at-peg`: not true within 5 frames of the stage start (nearest: never). Relative pose (nut_1->peg_1) pos [0.1, -1.1, -8.9] cm, rpy [6.0, 1.0, 173.0] deg. Outside learned bins: y bin 8 (region 7); yaw bin 11 (region 9). Nearest training pose distance 0.55 (99th pct 1.02).
- **demo_21**, stage `insert-nut`, at end `nut-at-peg`: not true within 8 frames of the stage end (nearest: never). Relative pose (nut_1->peg_1) pos [0.1, -1.1, -8.9] cm, rpy [6.0, 1.0, 173.0] deg. Outside learned bins: y bin 8 (region 7); yaw bin 11 (region 9). Nearest training pose distance 0.55 (99th pct 1.02).
- **demo_21**, stage `release-and-retreat`, at start `nut-at-peg`: not true within 8 frames of the stage start (nearest: never). Relative pose (nut_1->peg_1) pos [0.1, -1.1, -8.9] cm, rpy [6.0, 1.0, 173.0] deg. Outside learned bins: y bin 8 (region 7); yaw bin 11 (region 9). Nearest training pose distance 0.55 (99th pct 1.02).
- **demo_21**, stage `release-and-retreat`, at end `nut-on-peg`: not true within 5 frames of the stage end (nearest: never). Relative pose (nut_1->peg_1) pos [0.1, 0.1, 2.1] cm, rpy [-0.0, -0.0, 178.0] deg. Outside learned bins: yaw bin 11 (region 9). Nearest training pose distance 0.06 (99th pct 1.02).
- **demo_32**, stage `move-nut-to-peg`, at end `nut-at-peg`: not true within 6 frames of the stage end (nearest: never). Relative pose (nut_1->peg_1) pos [-0.8, -0.6, -8.6] cm, rpy [5.0, 2.0, -179.0] deg. Outside learned bins: yaw bin 1 (region 3). Nearest training pose distance 0.34 (99th pct 1.61).
- **demo_32**, stage `insert-nut`, at start `nut-at-peg`: not true within 5 frames of the stage start (nearest: never). Relative pose (nut_1->peg_1) pos [-0.8, -0.7, -8.6] cm, rpy [5.0, 2.0, -179.0] deg. Outside learned bins: yaw bin 1 (region 3). Nearest training pose distance 0.40 (99th pct 1.02).
- **demo_32**, stage `insert-nut`, at end `nut-at-peg`: not true within 8 frames of the stage end (nearest: never). Relative pose (nut_1->peg_1) pos [-0.8, -0.7, -8.6] cm, rpy [5.0, 2.0, -179.0] deg. Outside learned bins: yaw bin 1 (region 3). Nearest training pose distance 0.40 (99th pct 1.02).
- **demo_32**, stage `release-and-retreat`, at start `nut-at-peg`: not true within 8 frames of the stage start (nearest: never). Relative pose (nut_1->peg_1) pos [-0.8, -0.7, -8.6] cm, rpy [5.0, 2.0, -179.0] deg. Outside learned bins: yaw bin 1 (region 3). Nearest training pose distance 0.40 (99th pct 1.02).
- **demo_32**, stage `release-and-retreat`, at end `nut-on-peg`: not true within 5 frames of the stage end (nearest: never). Relative pose (nut_1->peg_1) pos [0.2, 0.2, 2.1] cm, rpy [0.0, 0.0, 179.0] deg. Outside learned bins: yaw bin 12 (region 9). Nearest training pose distance 0.11 (99th pct 1.02).
- **demo_44**, stage `move-nut-to-peg`, at end `nut-at-peg`: not true within 6 frames of the stage end (nearest: never). Relative pose (nut_1->peg_1) pos [-0.8, 1.1, -6.8] cm, rpy [-4.0, -3.0, -177.0] deg. Outside learned bins: y bin 6 (region 7); yaw bin 1 (region 3). Nearest training pose distance 0.25 (99th pct 1.61).
- **demo_44**, stage `insert-nut`, at start `nut-at-peg`: not true within 5 frames of the stage start (nearest: never). Relative pose (nut_1->peg_1) pos [-0.7, 0.9, -6.0] cm, rpy [-3.0, -3.0, -176.0] deg. Outside learned bins: yaw bin 1 (region 3). Nearest training pose distance 0.18 (99th pct 1.02).
- **demo_44**, stage `insert-nut`, at end `nut-at-peg`: not true within 8 frames of the stage end (nearest: never). Relative pose (nut_1->peg_1) pos [-0.7, 0.9, -6.0] cm, rpy [-3.0, -3.0, -176.0] deg. Outside learned bins: yaw bin 1 (region 3). Nearest training pose distance 0.18 (99th pct 1.02).
- **demo_44**, stage `release-and-retreat`, at start `nut-at-peg`: not true within 8 frames of the stage start (nearest: never). Relative pose (nut_1->peg_1) pos [-0.7, 0.9, -6.0] cm, rpy [-3.0, -3.0, -176.0] deg. Outside learned bins: yaw bin 1 (region 3). Nearest training pose distance 0.18 (99th pct 1.02).
- **demo_44**, stage `release-and-retreat`, at end `nut-on-peg`: not true within 5 frames of the stage end (nearest: never). Relative pose (nut_1->peg_1) pos [-0.4, 0.2, 2.1] cm, rpy [0.0, 0.0, -177.0] deg. Outside learned bins: yaw bin 1 (region 3). Nearest training pose distance 0.09 (99th pct 1.02).
- **demo_105**, stage `move-nut-to-peg`, at end `nut-at-peg`: not true within 6 frames of the stage end (nearest: never). Relative pose (nut_1->peg_1) pos [-1.0, 1.4, -8.4] cm, rpy [-11.0, -1.0, -171.0] deg. Outside learned bins: y bin 6 (region 7); pitch bin 7 (region 6); yaw bin 1 (region 3). Nearest training pose distance 0.52 (99th pct 1.61).
- **demo_105**, stage `insert-nut`, at start `nut-at-peg`: not true within 5 frames of the stage start (nearest: never). Relative pose (nut_1->peg_1) pos [-0.9, 1.3, -8.1] cm, rpy [-11.0, -0.0, -172.0] deg. Outside learned bins: y bin 6 (region 7); pitch bin 7 (region 6); yaw bin 1 (region 3). Nearest training pose distance 0.70 (99th pct 1.02).
- **demo_105**, stage `insert-nut`, at end `nut-at-peg`: not true within 8 frames of the stage end (nearest: never). Relative pose (nut_1->peg_1) pos [-0.9, 1.3, -8.1] cm, rpy [-11.0, -0.0, -172.0] deg. Outside learned bins: y bin 6 (region 7); pitch bin 7 (region 6); yaw bin 1 (region 3). Nearest training pose distance 0.70 (99th pct 1.02).
- **demo_105**, stage `release-and-retreat`, at start `nut-at-peg`: not true within 8 frames of the stage start (nearest: never). Relative pose (nut_1->peg_1) pos [-0.9, 1.3, -8.1] cm, rpy [-11.0, -0.0, -172.0] deg. Outside learned bins: y bin 6 (region 7); pitch bin 7 (region 6); yaw bin 1 (region 3). Nearest training pose distance 0.70 (99th pct 1.02).
- **demo_105**, stage `release-and-retreat`, at end `nut-on-peg`: not true within 5 frames of the stage end (nearest: never). Relative pose (nut_1->peg_1) pos [0.5, 0.0, 2.1] cm, rpy [0.0, -0.0, -176.0] deg. Outside learned bins: yaw bin 1 (region 3). Nearest training pose distance 0.15 (99th pct 1.02).
- **demo_111**, stage `move-nut-to-peg`, at end `nut-at-peg`: not true within 6 frames of the stage end (nearest: never). Relative pose (nut_1->peg_1) pos [0.8, -1.1, -7.5] cm, rpy [3.0, 8.0, -180.0] deg. Outside learned bins: y bin 8 (region 7); yaw bin 12 (region 9). Nearest training pose distance 0.30 (99th pct 1.61).
- **demo_111**, stage `insert-nut`, at start `nut-at-peg`: not true within 5 frames of the stage start (nearest: never). Relative pose (nut_1->peg_1) pos [0.8, -1.0, -7.4] cm, rpy [3.0, 9.0, 180.0] deg. Outside learned bins: y bin 8 (region 7); yaw bin 11 (region 9). Nearest training pose distance 0.48 (99th pct 1.02).
- **demo_111**, stage `insert-nut`, at end `nut-at-peg`: not true within 8 frames of the stage end (nearest: never). Relative pose (nut_1->peg_1) pos [0.8, -1.0, -7.4] cm, rpy [3.0, 9.0, 180.0] deg. Outside learned bins: y bin 8 (region 7); yaw bin 11 (region 9). Nearest training pose distance 0.48 (99th pct 1.02).
- **demo_111**, stage `release-and-retreat`, at start `nut-at-peg`: not true within 8 frames of the stage start (nearest: never). Relative pose (nut_1->peg_1) pos [0.8, -1.0, -7.4] cm, rpy [3.0, 9.0, 180.0] deg. Outside learned bins: y bin 8 (region 7); yaw bin 11 (region 9). Nearest training pose distance 0.48 (99th pct 1.02).
- **demo_111**, stage `release-and-retreat`, at end `nut-on-peg`: not true within 5 frames of the stage end (nearest: never). Relative pose (nut_1->peg_1) pos [-0.0, -0.4, 2.1] cm, rpy [-0.0, -0.0, 179.0] deg. Outside learned bins: yaw bin 12 (region 9). Nearest training pose distance 0.07 (99th pct 1.02).
- **demo_125**, stage `move-nut-to-peg`, at end `nut-at-peg`: not true within 6 frames of the stage end (nearest: 8 frames away). Relative pose (nut_1->peg_1) pos [1.2, 2.9, -8.0] cm, rpy [-3.0, -17.0, 87.0] deg. Outside learned bins: x bin 8 (region 7); y bin 6 (region 7); pitch bin 5 (region 6). Nearest training pose distance 0.99 (99th pct 1.61).
- **demo_125**, stage `insert-nut`, at start `nut-at-peg`: not true within 5 frames of the stage start (nearest: 7 frames away). Relative pose (nut_1->peg_1) pos [1.2, 2.8, -7.8] cm, rpy [-3.0, -17.0, 87.0] deg. Outside learned bins: x bin 8 (region 7); y bin 6 (region 7); pitch bin 5 (region 6). Nearest training pose distance 1.15 (99th pct 1.02).
- **demo_131**, stage `approach-nut`, at end `ready-to-grasp`: not true within 5 frames of the stage end (nearest: 9 frames away). Relative pose (gripper_1->nut_1) pos [-6.3, 2.0, 0.3] cm, rpy [-3.0, 5.0, -4.0] deg. Outside learned bins: y bin 13 (region 14); grasp sensor 0 (region 1). Nearest training pose distance 0.20 (99th pct 1.54).
- **demo_131**, stage `move-nut-to-peg`, at start `holding`: not true within 5 frames of the stage start (nearest: 8 frames away). Relative pose (gripper_1->nut_1) pos [-6.4, 1.9, 0.3] cm, rpy [-3.0, 5.0, -3.0] deg. Outside learned bins: y bin 13 (region 14). Nearest training pose distance 0.28 (99th pct 0.67).
- **demo_168**, stage `move-nut-to-peg`, over all `holding`: false for 56 of 58 frames in a row (tolerance 91% of stage). Relative pose (gripper_1->nut_1) pos [7.5, 1.2, -1.5] cm, rpy [5.0, -7.0, -176.0] deg. Outside learned bins: z bin 13 (region 14). Nearest training pose distance 0.19 (99th pct 0.67).
- **demo_176**, stage `move-nut-to-peg`, at end `nut-at-peg`: not true within 6 frames of the stage end (nearest: never). Relative pose (nut_1->peg_1) pos [-0.6, -0.6, -2.8] cm, rpy [0.0, 2.0, 179.0] deg. Outside learned bins: yaw bin 11 (region 3). Nearest training pose distance 0.47 (99th pct 1.61).
- **demo_176**, stage `insert-nut`, at start `nut-at-peg`: not true within 5 frames of the stage start (nearest: never). Relative pose (nut_1->peg_1) pos [-0.6, -0.7, -2.4] cm, rpy [0.0, 3.0, 179.0] deg. Outside learned bins: yaw bin 11 (region 3). Nearest training pose distance 0.43 (99th pct 1.02).
- **demo_176**, stage `insert-nut`, at end `nut-at-peg`: not true within 8 frames of the stage end (nearest: never). Relative pose (nut_1->peg_1) pos [-0.6, -0.7, -2.4] cm, rpy [0.0, 3.0, 179.0] deg. Outside learned bins: yaw bin 11 (region 3). Nearest training pose distance 0.43 (99th pct 1.02).
- **demo_176**, stage `release-and-retreat`, at start `nut-at-peg`: not true within 8 frames of the stage start (nearest: never). Relative pose (nut_1->peg_1) pos [-0.6, -0.7, -2.4] cm, rpy [0.0, 3.0, 179.0] deg. Outside learned bins: yaw bin 11 (region 3). Nearest training pose distance 0.43 (99th pct 1.02).
- **demo_176**, stage `release-and-retreat`, at end `nut-on-peg`: not true within 5 frames of the stage end (nearest: never). Relative pose (nut_1->peg_1) pos [0.8, -0.6, 2.3] cm, rpy [0.0, -1.0, -180.0] deg. Outside learned bins: yaw bin 0 (region 3). Nearest training pose distance 0.12 (99th pct 1.02).
- **demo_180**, stage `move-nut-to-peg`, at end `nut-at-peg`: not true within 6 frames of the stage end (nearest: never). Relative pose (nut_1->peg_1) pos [-0.0, 2.1, -6.7] cm, rpy [6.0, 17.0, -69.0] deg. Outside learned bins: y bin 6 (region 7); roll bin 7 (region 6); yaw bin 4 (region 3). Nearest training pose distance 0.69 (99th pct 1.61).
- **demo_180**, stage `insert-nut`, at start `nut-at-peg`: not true within 5 frames of the stage start (nearest: never). Relative pose (nut_1->peg_1) pos [-0.1, 1.8, -5.4] cm, rpy [6.0, 19.0, -70.0] deg. Outside learned bins: y bin 6 (region 7); roll bin 7 (region 6); yaw bin 4 (region 3). Nearest training pose distance 0.50 (99th pct 1.02).
- **demo_180**, stage `insert-nut`, at end `nut-at-peg`: not true within 8 frames of the stage end (nearest: never). Relative pose (nut_1->peg_1) pos [-0.1, 1.8, -5.4] cm, rpy [6.0, 19.0, -70.0] deg. Outside learned bins: y bin 6 (region 7); roll bin 7 (region 6); yaw bin 4 (region 3). Nearest training pose distance 0.50 (99th pct 1.02).
- **demo_180**, stage `release-and-retreat`, at start `nut-at-peg`: not true within 8 frames of the stage start (nearest: never). Relative pose (nut_1->peg_1) pos [-0.1, 1.8, -5.4] cm, rpy [6.0, 19.0, -70.0] deg. Outside learned bins: y bin 6 (region 7); roll bin 7 (region 6); yaw bin 4 (region 3). Nearest training pose distance 0.50 (99th pct 1.02).
- **demo_180**, stage `release-and-retreat`, at end `nut-on-peg`: not true within 5 frames of the stage end (nearest: never). Relative pose (nut_1->peg_1) pos [-0.4, 0.4, 2.1] cm, rpy [-1.0, -1.0, -80.0] deg. Outside learned bins: yaw bin 4 (region 3). Nearest training pose distance 0.14 (99th pct 1.02).
- **demo_191**, stage `release-and-retreat`, at end `holding` (should be false): not true within 0 frames of the stage end (nearest: 1 frames away). Relative pose (gripper_1->nut_1) pos [-6.6, -4.0, -13.3] cm, rpy [-3.0, 6.0, 18.0] deg. inside region it should not be in. Nearest training pose distance 6.21 (99th pct 1.05).

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
| release-and-retreat / at end / nut-on-peg / True | 69 |
| insert-nut / at end / nut-at-peg / True | 65 |
| move-nut-to-peg / at end / nut-at-peg / True | 64 |
| insert-nut / at start / nut-at-peg / True | 64 |
| release-and-retreat / at start / nut-at-peg / True | 64 |
| move-nut-to-peg / at start / holding / True | 14 |
| move-nut-to-peg / over all / holding / True | 9 |
| approach-nut / at end / ready-to-grasp / True | 9 |
