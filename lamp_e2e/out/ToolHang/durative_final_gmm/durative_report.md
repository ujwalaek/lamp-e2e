# ToolHang: stage-aware durative monitor

| Test case | Runs | Really failed | Flagged | Meaning |
|---|---|---|---|---|
| nominal (recorded, all succeed) | 20 | - | 3 | false alarms |
| drop (physics rollout) | 20 | 18 | 11 | detected |
| miss (physics rollout) | 20 | 19 | 17 | detected |

## False alarms (nominal runs flagged)

| Stage | Condition | Predicate | Why outside | Pose typical of training? | Count |
|---|---|---|---|---|---|
| insert-frame | at end | frame-in-stand | position only | yes | 1 |
| approach-tool | over all | frame-in-stand | position only | yes | 1 |
| move-tool-to-hook | over all | frame-in-stand | position only | no | 1 |
| move-tool-to-hook | over all | holding-tool | grasp flag | yes | 1 |
| insert-frame | over all | holding-frame | position and rotation | yes | 1 |

### Every false alarm

- **demo_32**, stage `insert-frame`, at end `frame-in-stand`: not true within 20 frames of the stage end (nearest: 45 frames away). Relative pose (frame_1->stand_1) pos [-3.8, -1.6, -33.3] cm, rpy [4.0, -8.0, -96.0] deg. Outside learned bins: z bin 2 (region 5). Nearest training pose distance 0.07 (99th pct 0.69).
- **demo_32**, stage `approach-tool`, over all `frame-in-stand`: false for 40 of 40 frames in a row (tolerance 77% of stage). Relative pose (frame_1->stand_1) pos [-3.8, -1.6, -33.3] cm, rpy [4.0, -8.0, -96.0] deg. Outside learned bins: z bin 2 (region 5). Nearest training pose distance 0.18 (99th pct 2.70).
- **demo_32**, stage `move-tool-to-hook`, over all `frame-in-stand`: false for 4 of 50 frames in a row (tolerance 0% of stage). Relative pose (frame_1->stand_1) pos [-2.9, -0.1, -33.6] cm, rpy [6.0, 0.0, -85.0] deg. Outside learned bins: z bin 2 (region 5). Nearest training pose distance 2.28 (99th pct 0.07).
- **demo_36**, stage `move-tool-to-hook`, over all `holding-tool`: false for 32 of 115 frames in a row (tolerance 100% of stage). Relative pose (gripper_1->tool_1) pos [-0.4, 0.2, 0.0] cm, rpy [18.0, 54.0, 14.0] deg. Outside learned bins: grasp sensor 0 (region 1). Nearest training pose distance 0.34 (99th pct 6.24).
- **demo_105**, stage `insert-frame`, over all `holding-frame`: false for 5 of 16 frames in a row (tolerance 100% of stage). Relative pose (gripper_1->frame_1) pos [-5.9, 1.7, 4.2] cm, rpy [-53.0, 8.0, 77.0] deg. Outside learned bins: x bin 12 (region 13); y bin 13 (region 14); z bin 15 (region 14); roll bin 5 (region 4); pitch bin 5 (region 4). Nearest training pose distance 0.27 (99th pct 0.42).

## Drop: detections and misses

2 drop rollouts still succeeded physically, so they are not failures and are excluded: demo_103, demo_155.

First condition violated in each detected run:

| Stage | Condition | Predicate | Runs |
|---|---|---|---|
| move-frame-to-stand | at end | frame-above-stand | 6 |
| insert-frame | at end | frame-in-stand | 3 |
| insert-frame | over all | holding-frame | 1 |
| approach-tool | at end | at-tool-grasp | 1 |

Missed (7): demo_0, demo_21, demo_36, demo_44, demo_111, demo_125, demo_131
- **demo_0**: stages [['approach-frame', 0, 35], ['move-frame-to-stand', 35, 136], ['insert-frame', 136, 190], ['approach-tool', 190, 249], ['move-tool-to-hook', 249, 292], ['hang-tool-and-retreat', 292, 341]]
- **demo_21**: stages [['approach-frame', 0, 33], ['move-frame-to-stand', 33, 79], ['insert-frame', 79, 132], ['approach-tool', 132, 176], ['move-tool-to-hook', 176, 228], ['hang-tool-and-retreat', 228, 288]]
- **demo_36**: stages [['approach-frame', 0, 27], ['move-frame-to-stand', 27, 82], ['insert-frame', 82, 114], ['approach-tool', 114, 147], ['move-tool-to-hook', 147, 177], ['hang-tool-and-retreat', 177, 266]]
- **demo_44**: stages [['approach-frame', 0, 26], ['move-frame-to-stand', 26, 75], ['insert-frame', 75, 144], ['approach-tool', 144, 183], ['move-tool-to-hook', 183, 213], ['hang-tool-and-retreat', 213, 262]]
- **demo_111**: stages [['approach-frame', 0, 20], ['move-frame-to-stand', 20, 103], ['insert-frame', 103, 107], ['approach-tool', 107, 130], ['move-tool-to-hook', 130, 158], ['hang-tool-and-retreat', 158, 203]]
- **demo_125**: stages [['approach-frame', 0, 22], ['move-frame-to-stand', 22, 73], ['insert-frame', 73, 107], ['approach-tool', 107, 140], ['move-tool-to-hook', 140, 164], ['hang-tool-and-retreat', 164, 207]]
- **demo_131**: stages [['approach-frame', 0, 20], ['move-frame-to-stand', 20, 84], ['insert-frame', 84, 89], ['approach-tool', 89, 113], ['move-tool-to-hook', 113, 138], ['hang-tool-and-retreat', 138, 168]]

## Miss: detections and misses

1 miss rollouts still succeeded physically, so they are not failures and are excluded: demo_155.

First condition violated in each detected run:

| Stage | Condition | Predicate | Runs |
|---|---|---|---|
| move-tool-to-hook | at end | tool-at-hook | 6 |
| move-frame-to-stand | at end | frame-above-stand | 6 |
| insert-frame | at end | frame-in-stand | 4 |
| insert-frame | over all | holding-frame | 1 |

Missed (2): demo_36, demo_103
- **demo_36**: stages [['approach-frame', 0, 27], ['move-frame-to-stand', 27, 82], ['insert-frame', 82, 114], ['approach-tool', 114, 147], ['move-tool-to-hook', 147, 206], ['hang-tool-and-retreat', 206, 266]]
- **demo_103**: stages [['approach-frame', 0, 19], ['move-frame-to-stand', 19, 82], ['insert-frame', 82, 82], ['approach-tool', 82, 118], ['move-tool-to-hook', 118, 164], ['hang-tool-and-retreat', 164, 206]]

## Condition violations on the 180 training demos (all succeed)

These show how reliable each learned condition is on normal runs.

| Condition | Violations |
|---|---|
| insert-frame / over all / holding-frame / True | 10 |
| approach-tool / over all / frame-in-stand / True | 7 |
| move-tool-to-hook / over all / holding-tool / True | 6 |
| approach-tool / at end / at-tool-grasp / True | 4 |
| move-tool-to-hook / at end / tool-at-hook / True | 4 |
| insert-frame / at end / frame-in-stand / True | 4 |
| move-tool-to-hook / at start / holding-tool / True | 3 |
| move-frame-to-stand / at end / frame-above-stand / True | 2 |
| insert-frame / at start / frame-above-stand / True | 2 |
| move-frame-to-stand / at start / holding-frame / True | 1 |
