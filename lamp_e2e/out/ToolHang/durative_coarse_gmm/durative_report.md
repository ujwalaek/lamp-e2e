# ToolHang: stage-aware durative monitor

| Test case | Runs | Really failed | Flagged | Meaning |
|---|---|---|---|---|
| nominal (recorded, all succeed) | 20 | - | 4 | false alarms |
| drop (physics rollout) | 20 | 18 | 11 | detected |
| miss (physics rollout) | 20 | 19 | 19 | detected |

## False alarms (nominal runs flagged)

| Stage | Condition | Predicate | Why outside | Pose typical of training? | Count |
|---|---|---|---|---|---|
| move-frame-to-stand | at end | frame-above-stand | position only | yes | 1 |
| insert-frame | at start | frame-above-stand | position only | yes | 1 |
| insert-frame | at end | frame-in-stand | position only | yes | 1 |
| approach-tool | over all | frame-in-stand | position only | yes | 1 |
| move-tool-to-hook | over all | frame-in-stand | position only | no | 1 |
| move-tool-to-hook | over all | holding-tool | grasp flag | yes | 1 |
| move-tool-to-hook | at end | tool-at-hook | position and rotation | yes | 1 |
| approach-tool | at end | at-tool-grasp | position only | yes | 1 |
| insert-frame | over all | holding-frame | position and rotation | yes | 1 |

### Every false alarm

- **demo_32**, stage `move-frame-to-stand`, at end `frame-above-stand`: not true within 18 frames of the stage end (nearest: never). Relative pose (frame_1->stand_1) pos [-3.8, -1.6, -33.3] cm, rpy [4.0, -8.0, -96.0] deg. Outside learned bins: z bin 2 (region 3). Nearest training pose distance 0.07 (99th pct 0.94).
- **demo_32**, stage `insert-frame`, at start `frame-above-stand`: not true within 17 frames of the stage start (nearest: never). Relative pose (frame_1->stand_1) pos [-3.8, -1.6, -33.3] cm, rpy [4.0, -8.0, -96.0] deg. Outside learned bins: z bin 2 (region 3). Nearest training pose distance 0.18 (99th pct 0.35).
- **demo_32**, stage `insert-frame`, at end `frame-in-stand`: not true within 20 frames of the stage end (nearest: 44 frames away). Relative pose (frame_1->stand_1) pos [-3.8, -1.6, -33.3] cm, rpy [4.0, -8.0, -96.0] deg. Outside learned bins: z bin 2 (region 5). Nearest training pose distance 0.18 (99th pct 0.35).
- **demo_32**, stage `approach-tool`, over all `frame-in-stand`: false for 40 of 40 frames in a row (tolerance 93% of stage). Relative pose (frame_1->stand_1) pos [-3.8, -1.6, -33.3] cm, rpy [4.0, -8.0, -96.0] deg. Outside learned bins: z bin 2 (region 5). Nearest training pose distance 0.18 (99th pct 0.35).
- **demo_32**, stage `move-tool-to-hook`, over all `frame-in-stand`: false for 4 of 50 frames in a row (tolerance 0% of stage). Relative pose (frame_1->stand_1) pos [-2.9, -0.1, -33.6] cm, rpy [6.0, 0.0, -85.0] deg. Outside learned bins: z bin 2 (region 5). Nearest training pose distance 2.28 (99th pct 0.07).
- **demo_36**, stage `move-tool-to-hook`, over all `holding-tool`: false for 32 of 115 frames in a row (tolerance 100% of stage). Relative pose (gripper_1->tool_1) pos [-0.4, 0.2, 0.0] cm, rpy [-5.0, 21.0, 178.0] deg. Outside learned bins: grasp sensor 0 (region 1). Nearest training pose distance 0.34 (99th pct 3.51).
- **demo_36**, stage `move-tool-to-hook`, at end `tool-at-hook`: not true within 20 frames of the stage end (nearest: 41 frames away). Relative pose (frame_1->tool_1) pos [-15.9, -1.1, -5.8] cm, rpy [2.0, 39.0, -173.0] deg. Outside learned bins: x bin 7 (region 6); z bin 9 (region 11); roll bin 8 (region 6). Nearest training pose distance 0.59 (99th pct 1.32).
- **demo_103**, stage `approach-tool`, at end `at-tool-grasp`: not true within 20 frames of the stage end (nearest: 47 frames away). Relative pose (gripper_1->tool_1) pos [-2.9, 1.1, -5.1] cm, rpy [5.0, 10.0, -176.0] deg. Outside learned bins: x bin 13 (region 14); z bin 12 (region 14). Nearest training pose distance 0.25 (99th pct 1.90).
- **demo_105**, stage `insert-frame`, over all `holding-frame`: false for 4 of 4 frames in a row (tolerance 100% of stage). Relative pose (gripper_1->frame_1) pos [-5.7, 1.7, 4.4] cm, rpy [-50.0, 9.0, 77.0] deg. Outside learned bins: x bin 12 (region 13); y bin 13 (region 14); z bin 15 (region 14); roll bin 5 (region 4); pitch bin 5 (region 4). Nearest training pose distance 0.28 (99th pct 0.44).

## Drop: detections and misses

2 drop rollouts still succeeded physically, so they are not failures and are excluded: demo_103, demo_155.

First condition violated in each detected run:

| Stage | Condition | Predicate | Runs |
|---|---|---|---|
| move-frame-to-stand | at end | frame-above-stand | 8 |
| insert-frame | at end | frame-in-stand | 2 |
| insert-frame | over all | holding-frame | 1 |

Missed (7): demo_0, demo_21, demo_36, demo_44, demo_111, demo_125, demo_131
- **demo_0**: stages [['approach-frame', 0, 35], ['move-frame-to-stand', 35, 139], ['insert-frame', 139, 190], ['approach-tool', 190, 249], ['move-tool-to-hook', 249, 292], ['hang-tool-and-retreat', 292, 341]]
- **demo_21**: stages [['approach-frame', 0, 33], ['move-frame-to-stand', 33, 85], ['insert-frame', 85, 132], ['approach-tool', 132, 176], ['move-tool-to-hook', 176, 228], ['hang-tool-and-retreat', 228, 288]]
- **demo_36**: stages [['approach-frame', 0, 27], ['move-frame-to-stand', 27, 109], ['insert-frame', 109, 114], ['approach-tool', 114, 147], ['move-tool-to-hook', 147, 177], ['hang-tool-and-retreat', 177, 266]]
- **demo_44**: stages [['approach-frame', 0, 26], ['move-frame-to-stand', 26, 139], ['insert-frame', 139, 144], ['approach-tool', 144, 183], ['move-tool-to-hook', 183, 213], ['hang-tool-and-retreat', 213, 262]]
- **demo_111**: stages [['approach-frame', 0, 20], ['move-frame-to-stand', 20, 104], ['insert-frame', 104, 107], ['approach-tool', 107, 130], ['move-tool-to-hook', 130, 158], ['hang-tool-and-retreat', 158, 203]]
- **demo_125**: stages [['approach-frame', 0, 22], ['move-frame-to-stand', 22, 105], ['insert-frame', 105, 107], ['approach-tool', 107, 140], ['move-tool-to-hook', 140, 164], ['hang-tool-and-retreat', 164, 207]]
- **demo_131**: stages [['approach-frame', 0, 20], ['move-frame-to-stand', 20, 85], ['insert-frame', 85, 89], ['approach-tool', 89, 113], ['move-tool-to-hook', 113, 138], ['hang-tool-and-retreat', 138, 168]]

## Miss: detections and misses

1 miss rollouts still succeeded physically, so they are not failures and are excluded: demo_155.

First condition violated in each detected run:

| Stage | Condition | Predicate | Runs |
|---|---|---|---|
| move-frame-to-stand | at end | frame-above-stand | 9 |
| move-tool-to-hook | at end | tool-at-hook | 7 |
| insert-frame | at end | frame-in-stand | 2 |
| insert-frame | over all | holding-frame | 1 |

Missed (0): none

## Condition violations on the 180 training demos (all succeed)

These show how reliable each learned condition is on normal runs.

| Condition | Violations |
|---|---|
| move-tool-to-hook / over all / holding-tool / True | 7 |
| insert-frame / over all / holding-frame / True | 7 |
| approach-tool / over all / frame-in-stand / True | 5 |
| move-tool-to-hook / at end / tool-at-hook / True | 4 |
| move-frame-to-stand / at end / frame-above-stand / True | 4 |
| insert-frame / at start / frame-above-stand / True | 4 |
| approach-tool / at end / at-tool-grasp / True | 4 |
| move-tool-to-hook / at start / holding-tool / True | 2 |
| insert-frame / at end / frame-in-stand / True | 2 |
