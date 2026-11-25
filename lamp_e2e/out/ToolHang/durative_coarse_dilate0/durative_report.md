# ToolHang: stage-aware durative monitor

| Test case | Runs | Really failed | Flagged | Meaning |
|---|---|---|---|---|
| nominal (recorded, all succeed) | 20 | - | 15 | false alarms |
| drop (physics rollout) | 20 | 18 | 17 | detected |
| miss (physics rollout) | 20 | 19 | 19 | detected |

## False alarms (nominal runs flagged)

| Stage | Condition | Predicate | Why outside | Pose typical of training? | Count |
|---|---|---|---|---|---|
| approach-tool | at end | at-tool-grasp | position only | yes | 9 |
| move-tool-to-hook | at start | holding-tool | position only | yes | 5 |
| move-tool-to-hook | at end | tool-at-hook | position and rotation | yes | 5 |
| move-frame-to-stand | at start | holding-frame | position only | yes | 5 |
| insert-frame | at end | frame-in-stand | position only | yes | 3 |
| approach-tool | over all | frame-in-stand | position only | yes | 3 |
| approach-tool | at end | at-tool-grasp | position and rotation | yes | 3 |
| move-tool-to-hook | over all | frame-in-stand | position only | yes | 1 |
| move-frame-to-stand | at start | holding-frame | position only | no | 1 |
| approach-tool | at end | at-tool-grasp | rotation only | yes | 1 |
| move-tool-to-hook | at end | tool-at-hook | position only | yes | 1 |

### Every false alarm

- **demo_5**, stage `approach-tool`, at end `at-tool-grasp`: not true within 20 frames of the stage end (nearest: never). Relative pose (gripper_1->tool_1) pos [-2.4, 1.1, 0.1] cm, rpy [1.0, 5.0, 170.0] deg. Outside learned bins: x bin 13 (region 14). Nearest training pose distance 0.31 (99th pct 1.90).
- **demo_5**, stage `move-tool-to-hook`, at start `holding-tool`: not true within 20 frames of the stage start (nearest: 32 frames away). Relative pose (gripper_1->tool_1) pos [-2.1, 1.1, 0.0] cm, rpy [1.0, 5.0, 170.0] deg. Outside learned bins: x bin 13 (region 14). Nearest training pose distance 0.34 (99th pct 0.54).
- **demo_5**, stage `move-tool-to-hook`, at end `tool-at-hook`: not true within 20 frames of the stage end (nearest: 39 frames away). Relative pose (frame_1->tool_1) pos [-16.5, 2.2, -4.6] cm, rpy [-5.0, 31.0, 165.0] deg. Outside learned bins: x bin 7 (region 6); y bin 10 (region 11); z bin 10 (region 11); roll bin 5 (region 6). Nearest training pose distance 0.18 (99th pct 1.32).
- **demo_14**, stage `move-tool-to-hook`, at end `tool-at-hook`: not true within 20 frames of the stage end (nearest: 24 frames away). Relative pose (frame_1->tool_1) pos [-17.6, -0.6, -3.5] cm, rpy [3.0, 24.0, -176.0] deg. Outside learned bins: z bin 10 (region 11); roll bin 7 (region 6). Nearest training pose distance 0.33 (99th pct 1.32).
- **demo_32**, stage `move-frame-to-stand`, at start `holding-frame`: not true within 13 frames of the stage start (nearest: never). Relative pose (gripper_1->frame_1) pos [-4.6, 0.7, -0.4] cm, rpy [-96.0, 2.0, 77.0] deg. Outside learned bins: x bin 12 (region 13). Nearest training pose distance 0.09 (99th pct 0.33).
- **demo_32**, stage `insert-frame`, at end `frame-in-stand`: not true within 20 frames of the stage end (nearest: 46 frames away). Relative pose (frame_1->stand_1) pos [-3.8, -1.6, -33.3] cm, rpy [4.0, -8.0, -96.0] deg. Outside learned bins: z bin 2 (region 5). Nearest training pose distance 0.07 (99th pct 0.61).
- **demo_32**, stage `approach-tool`, over all `frame-in-stand`: false for 40 of 40 frames in a row (tolerance 91% of stage). Relative pose (frame_1->stand_1) pos [-3.8, -1.6, -33.3] cm, rpy [4.0, -8.0, -96.0] deg. Outside learned bins: z bin 2 (region 5). Nearest training pose distance 0.18 (99th pct 0.35).
- **demo_32**, stage `approach-tool`, at end `at-tool-grasp`: not true within 20 frames of the stage end (nearest: never). Relative pose (gripper_1->tool_1) pos [-2.8, 0.5, -0.1] cm, rpy [2.0, 3.0, 170.0] deg. Outside learned bins: x bin 13 (region 14). Nearest training pose distance 0.39 (99th pct 1.90).
- **demo_32**, stage `move-tool-to-hook`, at start `holding-tool`: not true within 20 frames of the stage start (nearest: never). Relative pose (gripper_1->tool_1) pos [-3.1, 1.0, 0.3] cm, rpy [2.0, 2.0, 170.0] deg. Outside learned bins: x bin 13 (region 14). Nearest training pose distance 0.40 (99th pct 0.54).
- **demo_36**, stage `move-frame-to-stand`, at start `holding-frame`: not true within 13 frames of the stage start (nearest: never). Relative pose (gripper_1->frame_1) pos [-4.8, 0.9, -0.6] cm, rpy [-97.0, -0.0, 77.0] deg. Outside learned bins: x bin 12 (region 13). Nearest training pose distance 0.18 (99th pct 0.33).
- **demo_36**, stage `approach-tool`, at end `at-tool-grasp`: not true within 20 frames of the stage end (nearest: 60 frames away). Relative pose (gripper_1->tool_1) pos [-1.6, -0.4, -1.5] cm, rpy [8.0, 12.0, -180.0] deg. Outside learned bins: x bin 13 (region 14); roll bin 5 (region 6). Nearest training pose distance 0.31 (99th pct 1.90).
- **demo_36**, stage `move-tool-to-hook`, at end `tool-at-hook`: not true within 20 frames of the stage end (nearest: 69 frames away). Relative pose (frame_1->tool_1) pos [-15.9, -1.1, -5.8] cm, rpy [2.0, 39.0, -173.0] deg. Outside learned bins: x bin 7 (region 6); z bin 9 (region 11); roll bin 8 (region 6). Nearest training pose distance 0.59 (99th pct 1.32).
- **demo_44**, stage `approach-tool`, at end `at-tool-grasp`: not true within 20 frames of the stage end (nearest: never). Relative pose (gripper_1->tool_1) pos [-2.3, 0.4, -2.0] cm, rpy [5.0, 16.0, 179.0] deg. Outside learned bins: x bin 13 (region 14); z bin 13 (region 14); roll bin 5 (region 6). Nearest training pose distance 0.34 (99th pct 1.90).
- **demo_44**, stage `move-tool-to-hook`, at start `holding-tool`: not true within 20 frames of the stage start (nearest: never). Relative pose (gripper_1->tool_1) pos [-2.3, 0.5, -1.5] cm, rpy [5.0, 15.0, 179.0] deg. Outside learned bins: x bin 13 (region 14). Nearest training pose distance 0.38 (99th pct 0.54).
- **demo_44**, stage `move-tool-to-hook`, at end `tool-at-hook`: not true within 20 frames of the stage end (nearest: 23 frames away). Relative pose (frame_1->tool_1) pos [-17.9, 0.4, -2.9] cm, rpy [-5.0, 20.0, 177.0] deg. Outside learned bins: z bin 10 (region 11); roll bin 5 (region 6). Nearest training pose distance 0.06 (99th pct 1.32).
- **demo_56**, stage `move-frame-to-stand`, at start `holding-frame`: not true within 13 frames of the stage start (nearest: 20 frames away). Relative pose (gripper_1->frame_1) pos [-4.7, -0.0, 0.1] cm, rpy [-88.0, -2.0, 83.0] deg. Outside learned bins: x bin 12 (region 13). Nearest training pose distance 0.17 (99th pct 0.33).
- **demo_93**, stage `approach-tool`, at end `at-tool-grasp`: not true within 20 frames of the stage end (nearest: 36 frames away). Relative pose (gripper_1->tool_1) pos [-1.8, -1.0, -3.0] cm, rpy [2.0, 6.0, -168.0] deg. Outside learned bins: x bin 13 (region 14); z bin 13 (region 14). Nearest training pose distance 0.33 (99th pct 1.90).
- **demo_103**, stage `insert-frame`, at end `frame-in-stand`: not true within 20 frames of the stage end (nearest: 40 frames away). Relative pose (frame_1->stand_1) pos [-5.5, 1.4, -31.7] cm, rpy [-4.0, 6.0, -91.0] deg. Outside learned bins: z bin 3 (region 5). Nearest training pose distance 0.07 (99th pct 0.61).
- **demo_103**, stage `approach-tool`, over all `frame-in-stand`: false for 36 of 36 frames in a row (tolerance 91% of stage). Relative pose (frame_1->stand_1) pos [-5.5, 1.5, -31.7] cm, rpy [-4.0, 6.0, -91.0] deg. Outside learned bins: z bin 3 (region 5). Nearest training pose distance 0.21 (99th pct 0.35).
- **demo_103**, stage `approach-tool`, at end `at-tool-grasp`: not true within 20 frames of the stage end (nearest: 47 frames away). Relative pose (gripper_1->tool_1) pos [-2.9, 1.1, -5.1] cm, rpy [5.0, 10.0, -176.0] deg. Outside learned bins: x bin 13 (region 14); z bin 12 (region 14). Nearest training pose distance 0.25 (99th pct 1.90).
- **demo_103**, stage `move-tool-to-hook`, at start `holding-tool`: not true within 20 frames of the stage start (nearest: 26 frames away). Relative pose (gripper_1->tool_1) pos [-2.3, 0.8, -4.0] cm, rpy [4.0, 10.0, -178.0] deg. Outside learned bins: x bin 13 (region 14); z bin 13 (region 14). Nearest training pose distance 0.52 (99th pct 0.54).
- **demo_105**, stage `approach-tool`, at end `at-tool-grasp`: not true within 20 frames of the stage end (nearest: 51 frames away). Relative pose (gripper_1->tool_1) pos [-1.5, -0.3, -0.7] cm, rpy [-1.0, 0.0, 178.0] deg. Outside learned bins: x bin 13 (region 14). Nearest training pose distance 0.26 (99th pct 1.90).
- **demo_111**, stage `approach-tool`, at end `at-tool-grasp`: not true within 20 frames of the stage end (nearest: 58 frames away). Relative pose (gripper_1->tool_1) pos [-2.4, 0.9, -2.9] cm, rpy [-0.0, 14.0, 179.0] deg. Outside learned bins: x bin 13 (region 14); z bin 13 (region 14); roll bin 5 (region 6). Nearest training pose distance 0.38 (99th pct 1.90).
- **demo_111**, stage `move-tool-to-hook`, over all `frame-in-stand`: false for 28 of 57 frames in a row (tolerance 13% of stage). Relative pose (frame_1->stand_1) pos [-4.1, -2.0, -22.6] cm, rpy [-0.0, 0.0, -64.0] deg. Outside learned bins: y bin 12 (region 11). Nearest training pose distance 0.01 (99th pct 0.07).
- **demo_111**, stage `move-tool-to-hook`, at end `tool-at-hook`: not true within 20 frames of the stage end (nearest: 38 frames away). Relative pose (frame_1->tool_1) pos [-17.6, -2.8, -2.0] cm, rpy [-13.0, 16.0, -164.0] deg. Outside learned bins: y bin 12 (region 11); z bin 10 (region 11); roll bin 7 (region 6). Nearest training pose distance 0.34 (99th pct 1.32).
- **demo_131**, stage `move-frame-to-stand`, at start `holding-frame`: not true within 13 frames of the stage start (nearest: never). Relative pose (gripper_1->frame_1) pos [-5.6, 1.5, -2.2] cm, rpy [-94.0, 1.0, 82.0] deg. Outside learned bins: x bin 12 (region 13); z bin 13 (region 14). Nearest training pose distance 0.35 (99th pct 0.33).
- **demo_131**, stage `approach-tool`, at end `at-tool-grasp`: not true within 20 frames of the stage end (nearest: never). Relative pose (gripper_1->tool_1) pos [0.6, -0.9, -2.5] cm, rpy [5.0, 14.0, -170.0] deg. Outside learned bins: z bin 13 (region 14). Nearest training pose distance 0.36 (99th pct 1.90).
- **demo_155**, stage `insert-frame`, at end `frame-in-stand`: not true within 20 frames of the stage end (nearest: 27 frames away). Relative pose (frame_1->stand_1) pos [-5.2, 0.5, -29.8] cm, rpy [-3.0, 2.0, -91.0] deg. Outside learned bins: z bin 3 (region 5). Nearest training pose distance 0.07 (99th pct 0.61).
- **demo_155**, stage `approach-tool`, over all `frame-in-stand`: false for 24 of 24 frames in a row (tolerance 91% of stage). Relative pose (frame_1->stand_1) pos [-5.1, 0.5, -29.2] cm, rpy [-3.0, 2.0, -91.0] deg. Outside learned bins: z bin 3 (region 5). Nearest training pose distance 0.11 (99th pct 0.35).
- **demo_155**, stage `approach-tool`, at end `at-tool-grasp`: not true within 20 frames of the stage end (nearest: never). Relative pose (gripper_1->tool_1) pos [-0.4, -0.8, -1.8] cm, rpy [-2.0, 7.0, -172.0] deg. Outside learned bins: z bin 13 (region 14). Nearest training pose distance 0.35 (99th pct 1.90).
- **demo_168**, stage `move-frame-to-stand`, at start `holding-frame`: not true within 13 frames of the stage start (nearest: never). Relative pose (gripper_1->frame_1) pos [-5.4, 0.6, -0.4] cm, rpy [-97.0, -1.0, 74.0] deg. Outside learned bins: x bin 12 (region 13). Nearest training pose distance 0.14 (99th pct 0.33).
- **demo_168**, stage `approach-tool`, at end `at-tool-grasp`: not true within 20 frames of the stage end (nearest: 43 frames away). Relative pose (gripper_1->tool_1) pos [0.5, -1.4, -1.3] cm, rpy [1.0, 8.0, 180.0] deg. Outside learned bins: yaw bin 12 (region 11). Nearest training pose distance 0.21 (99th pct 1.90).
- **demo_168**, stage `move-tool-to-hook`, at end `tool-at-hook`: not true within 20 frames of the stage end (nearest: never). Relative pose (frame_1->tool_1) pos [-18.0, -2.1, 2.1] cm, rpy [-3.0, -7.0, -165.0] deg. Outside learned bins: y bin 12 (region 11). Nearest training pose distance 0.34 (99th pct 1.32).
- **demo_176**, stage `move-frame-to-stand`, at start `holding-frame`: not true within 13 frames of the stage start (nearest: never). Relative pose (gripper_1->frame_1) pos [-5.0, 1.0, -0.4] cm, rpy [-95.0, -4.0, 82.0] deg. Outside learned bins: x bin 12 (region 13). Nearest training pose distance 0.18 (99th pct 0.33).
- **demo_176**, stage `approach-tool`, at end `at-tool-grasp`: not true within 20 frames of the stage end (nearest: never). Relative pose (gripper_1->tool_1) pos [-3.8, 1.0, -4.1] cm, rpy [-3.0, 2.0, -173.0] deg. Outside learned bins: x bin 13 (region 14); z bin 13 (region 14). Nearest training pose distance 0.31 (99th pct 1.90).
- **demo_176**, stage `move-tool-to-hook`, at start `holding-tool`: not true within 20 frames of the stage start (nearest: never). Relative pose (gripper_1->tool_1) pos [-3.5, 0.9, -2.8] cm, rpy [-3.0, 1.0, -174.0] deg. Outside learned bins: x bin 13 (region 14); z bin 13 (region 14). Nearest training pose distance 0.38 (99th pct 0.54).
- **demo_191**, stage `approach-tool`, at end `at-tool-grasp`: not true within 20 frames of the stage end (nearest: 63 frames away). Relative pose (gripper_1->tool_1) pos [-2.7, 2.6, -6.0] cm, rpy [-7.0, 6.0, 172.0] deg. Outside learned bins: x bin 13 (region 14); y bin 13 (region 14); z bin 12 (region 14). Nearest training pose distance 0.62 (99th pct 1.90).

## Drop: detections and misses

2 drop rollouts still succeeded physically, so they are not failures and are excluded: demo_103, demo_155.

First condition violated in each detected run:

| Stage | Condition | Predicate | Runs |
|---|---|---|---|
| insert-frame | at end | frame-in-stand | 6 |
| move-frame-to-stand | at start | holding-frame | 6 |
| approach-tool | at end | at-tool-grasp | 3 |
| move-tool-to-hook | at end | tool-at-hook | 1 |
| move-frame-to-stand | at end | frame-above-stand | 1 |

Missed (1): demo_21
- **demo_21**: stages [['approach-frame', 0, 33], ['move-frame-to-stand', 33, 79], ['insert-frame', 79, 132], ['approach-tool', 132, 176], ['move-tool-to-hook', 176, 228], ['hang-tool-and-retreat', 228, 288]]

## Miss: detections and misses

1 miss rollouts still succeeded physically, so they are not failures and are excluded: demo_155.

First condition violated in each detected run:

| Stage | Condition | Predicate | Runs |
|---|---|---|---|
| insert-frame | at end | frame-in-stand | 7 |
| move-frame-to-stand | at start | holding-frame | 6 |
| approach-tool | at end | at-tool-grasp | 3 |
| move-tool-to-hook | at end | tool-at-hook | 2 |
| move-frame-to-stand | at end | frame-above-stand | 1 |

Missed (0): none

## Condition violations on the 180 training demos (all succeed)

These show how reliable each learned condition is on normal runs.

| Condition | Violations |
|---|---|
| approach-tool / at end / at-tool-grasp / True | 103 |
| move-tool-to-hook / at end / tool-at-hook / True | 43 |
| move-frame-to-stand / at start / holding-frame / True | 40 |
| move-tool-to-hook / at start / holding-tool / True | 31 |
| insert-frame / at end / frame-in-stand / True | 30 |
| move-tool-to-hook / over all / frame-in-stand / True | 9 |
| approach-tool / over all / frame-in-stand / True | 9 |
| hang-tool-and-retreat / over all / frame-in-stand / True | 6 |
