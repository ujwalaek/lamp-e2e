# ToolHang: stage-aware durative monitor

| Test case | Runs | Really failed | Flagged | Meaning |
|---|---|---|---|---|
| nominal (recorded, all succeed) | 20 | - | 2 | false alarms |
| drop (physics rollout) | 20 | 18 | 11 | detected |
| miss (physics rollout) | 20 | 19 | 18 | detected |

## False alarms (nominal runs flagged)

| Stage | Condition | Predicate | Why outside | Pose typical of training? | Count |
|---|---|---|---|---|---|
| insert-frame | at end | frame-in-stand | position only | yes | 1 |
| approach-tool | over all | frame-in-stand | position only | yes | 1 |
| move-tool-to-hook | over all | holding-tool | grasp flag | yes | 1 |

### Every false alarm

- **demo_32**, stage `insert-frame`, at end `frame-in-stand`: not true within 20 frames of the stage end (nearest: 45 frames away). Relative pose (frame_1->stand_1) pos [-3.8, -1.6, -33.3] cm, rpy [4.0, -8.0, -96.0] deg. Outside learned bins: z bin 2 (region 5). Nearest training pose distance 0.07 (99th pct 0.66).
- **demo_32**, stage `approach-tool`, over all `frame-in-stand`: false for 40 of 40 frames in a row (tolerance 100% of stage). Relative pose (frame_1->stand_1) pos [-3.8, -1.6, -33.3] cm, rpy [4.0, -8.0, -96.0] deg. Outside learned bins: z bin 2 (region 5). Nearest training pose distance 0.18 (99th pct 0.35).
- **demo_36**, stage `move-tool-to-hook`, over all `holding-tool`: false for 32 of 115 frames in a row (tolerance 100% of stage). Relative pose (gripper_1->tool_1) pos [-0.4, 0.2, 0.0] cm, rpy [-5.0, 21.0, 178.0] deg. Outside learned bins: grasp sensor 0 (region 1). Nearest training pose distance 0.34 (99th pct 3.51).

## Drop: detections and misses

2 drop rollouts still succeeded physically, so they are not failures and are excluded: demo_103, demo_155.

First condition violated in each detected run:

| Stage | Condition | Predicate | Runs |
|---|---|---|---|
| insert-frame | at end | frame-in-stand | 8 |
| approach-tool | at end | at-tool-grasp | 2 |
| approach-tool | over all | frame-in-stand | 1 |

Missed (7): demo_0, demo_21, demo_36, demo_44, demo_105, demo_111, demo_131
- **demo_0**: stages [['approach-frame', 0, 35], ['move-frame-to-stand', 35, 78], ['insert-frame', 78, 190], ['approach-tool', 190, 249], ['move-tool-to-hook', 249, 292], ['hang-tool-and-retreat', 292, 341]]
- **demo_21**: stages [['approach-frame', 0, 33], ['move-frame-to-stand', 33, 74], ['insert-frame', 74, 132], ['approach-tool', 132, 176], ['move-tool-to-hook', 176, 228], ['hang-tool-and-retreat', 228, 288]]
- **demo_36**: stages [['approach-frame', 0, 27], ['move-frame-to-stand', 27, 59], ['insert-frame', 59, 114], ['approach-tool', 114, 147], ['move-tool-to-hook', 147, 177], ['hang-tool-and-retreat', 177, 266]]
- **demo_44**: stages [['approach-frame', 0, 26], ['move-frame-to-stand', 26, 59], ['insert-frame', 59, 144], ['approach-tool', 144, 183], ['move-tool-to-hook', 183, 213], ['hang-tool-and-retreat', 213, 262]]
- **demo_105**: stages [['approach-frame', 0, 21], ['move-frame-to-stand', 21, 53], ['insert-frame', 53, 112], ['approach-tool', 112, 136], ['move-tool-to-hook', 136, 161], ['hang-tool-and-retreat', 161, 190]]
- **demo_111**: stages [['approach-frame', 0, 20], ['move-frame-to-stand', 20, 49], ['insert-frame', 49, 107], ['approach-tool', 107, 130], ['move-tool-to-hook', 130, 158], ['hang-tool-and-retreat', 158, 203]]
- **demo_131**: stages [['approach-frame', 0, 20], ['move-frame-to-stand', 20, 50], ['insert-frame', 50, 89], ['approach-tool', 89, 113], ['move-tool-to-hook', 113, 138], ['hang-tool-and-retreat', 138, 168]]

## Miss: detections and misses

1 miss rollouts still succeeded physically, so they are not failures and are excluded: demo_155.

First condition violated in each detected run:

| Stage | Condition | Predicate | Runs |
|---|---|---|---|
| insert-frame | at end | frame-in-stand | 10 |
| move-tool-to-hook | at end | tool-at-hook | 6 |
| approach-tool | over all | frame-in-stand | 1 |
| approach-tool | at end | at-tool-grasp | 1 |

Missed (1): demo_44
- **demo_44**: stages [['approach-frame', 0, 26], ['move-frame-to-stand', 26, 59], ['insert-frame', 59, 144], ['approach-tool', 144, 183], ['move-tool-to-hook', 183, 244], ['hang-tool-and-retreat', 244, 262]]

## Condition violations on the 180 training demos (all succeed)

These show how reliable each learned condition is on normal runs.

| Condition | Violations |
|---|---|
| approach-tool / over all / frame-in-stand / True | 12 |
| insert-frame / at end / frame-in-stand / True | 8 |
| move-tool-to-hook / over all / holding-tool / True | 6 |
| approach-tool / at end / at-tool-grasp / True | 4 |
| move-tool-to-hook / at end / tool-at-hook / True | 2 |
| move-tool-to-hook / at start / holding-tool / True | 1 |
| move-tool-to-hook / over all / frame-in-stand / True | 1 |
