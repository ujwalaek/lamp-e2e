# ToolHang: stage-aware durative monitor

| Test case | Runs | Really failed | Flagged | Meaning |
|---|---|---|---|---|
| nominal (recorded, all succeed) | 20 | - | 3 | false alarms |
| drop (physics rollout) | 20 | 18 | 12 | detected |
| miss (physics rollout) | 20 | 19 | 19 | detected |

## False alarms (nominal runs flagged)

| Stage | Condition | Predicate | Why outside | Pose typical of training? | Count |
|---|---|---|---|---|---|
| insert-frame | at end | frame-in-stand | position only | yes | 1 |
| approach-tool | over all | frame-in-stand | position only | yes | 1 |
| move-tool-to-hook | typical pose | frame_1->tool_1 | pose atypical for this stage | no | 1 |
| move-tool-to-hook | over all | holding-tool | grasp flag | yes | 1 |
| approach-tool | at end | at-tool-grasp | position only | yes | 1 |

### Every false alarm

- **demo_32**, stage `insert-frame`, at end `frame-in-stand`: not true within 20 frames of the stage end (nearest: 45 frames away). Relative pose (frame_1->stand_1) pos [-3.8, -1.6, -33.3] cm, rpy [4.0, -8.0, -96.0] deg. Outside learned bins: z bin 2 (region 5). Nearest training pose distance 0.07 (99th pct 0.66).
- **demo_32**, stage `approach-tool`, over all `frame-in-stand`: false for 40 of 40 frames in a row (tolerance 100% of stage). Relative pose (frame_1->stand_1) pos [-3.8, -1.6, -33.3] cm, rpy [4.0, -8.0, -96.0] deg. Outside learned bins: z bin 2 (region 5). Nearest training pose distance 0.18 (99th pct 2.70).
- **demo_32**, stage `move-tool-to-hook`, typical pose `frame_1->tool_1`: atypical for 20 frames in a row (normal demos: at most 14). Relative pose (frame_1->tool_1) pos [-21.7, -6.0, 2.9] cm, rpy [49.0, 58.0, 34.0] deg. pose atypical for this stage. Nearest training pose distance n/a (99th pct n/a).
- **demo_36**, stage `move-tool-to-hook`, over all `holding-tool`: false for 32 of 115 frames in a row (tolerance 100% of stage). Relative pose (gripper_1->tool_1) pos [-0.4, 0.2, 0.0] cm, rpy [18.0, 54.0, 14.0] deg. Outside learned bins: grasp sensor 0 (region 1). Nearest training pose distance 0.34 (99th pct 6.24).
- **demo_103**, stage `approach-tool`, at end `at-tool-grasp`: not true within 20 frames of the stage end (nearest: 47 frames away). Relative pose (gripper_1->tool_1) pos [-2.9, 1.1, -5.1] cm, rpy [0.0, 66.0, 1.0] deg. Outside learned bins: x bin 13 (region 14); z bin 12 (region 14). Nearest training pose distance 0.25 (99th pct 2.04).

## Drop: detections and misses

2 drop rollouts still succeeded physically, so they are not failures and are excluded: demo_103, demo_155.

First condition violated in each detected run:

| Stage | Condition | Predicate | Runs |
|---|---|---|---|
| insert-frame | at end | frame-in-stand | 7 |
| insert-frame | typical pose | frame_1->stand_1 | 2 |
| hang-tool-and-retreat | typical pose | frame_1->stand_1 | 1 |
| move-frame-to-stand | typical pose | gripper_1->frame_1 | 1 |
| approach-tool | at end | at-tool-grasp | 1 |

Missed (6): demo_0, demo_21, demo_36, demo_105, demo_111, demo_131
- **demo_0**: stages [['approach-frame', 0, 35], ['move-frame-to-stand', 35, 78], ['insert-frame', 78, 190], ['approach-tool', 190, 249], ['move-tool-to-hook', 249, 292], ['hang-tool-and-retreat', 292, 341]]
- **demo_21**: stages [['approach-frame', 0, 33], ['move-frame-to-stand', 33, 74], ['insert-frame', 74, 132], ['approach-tool', 132, 176], ['move-tool-to-hook', 176, 228], ['hang-tool-and-retreat', 228, 288]]
- **demo_36**: stages [['approach-frame', 0, 27], ['move-frame-to-stand', 27, 59], ['insert-frame', 59, 114], ['approach-tool', 114, 147], ['move-tool-to-hook', 147, 177], ['hang-tool-and-retreat', 177, 266]]
- **demo_105**: stages [['approach-frame', 0, 21], ['move-frame-to-stand', 21, 53], ['insert-frame', 53, 112], ['approach-tool', 112, 136], ['move-tool-to-hook', 136, 161], ['hang-tool-and-retreat', 161, 190]]
- **demo_111**: stages [['approach-frame', 0, 20], ['move-frame-to-stand', 20, 49], ['insert-frame', 49, 107], ['approach-tool', 107, 130], ['move-tool-to-hook', 130, 158], ['hang-tool-and-retreat', 158, 203]]
- **demo_131**: stages [['approach-frame', 0, 20], ['move-frame-to-stand', 20, 50], ['insert-frame', 50, 89], ['approach-tool', 89, 113], ['move-tool-to-hook', 113, 138], ['hang-tool-and-retreat', 138, 168]]

## Miss: detections and misses

1 miss rollouts still succeeded physically, so they are not failures and are excluded: demo_155.

First condition violated in each detected run:

| Stage | Condition | Predicate | Runs |
|---|---|---|---|
| insert-frame | typical pose | frame_1->stand_1 | 9 |
| move-tool-to-hook | typical pose | frame_1->tool_1 | 7 |
| insert-frame | at end | frame-in-stand | 2 |
| move-frame-to-stand | typical pose | gripper_1->frame_1 | 1 |

Missed (0): none

## Condition violations on the 180 training demos (all succeed)

These show how reliable each learned condition is on normal runs.

| Condition | Violations |
|---|---|
| approach-tool / over all / frame-in-stand / True | 14 |
| insert-frame / at end / frame-in-stand / True | 10 |
| move-tool-to-hook / over all / holding-tool / True | 5 |
| approach-tool / at end / at-tool-grasp / True | 5 |
| move-tool-to-hook / at start / holding-tool / True | 2 |
| move-frame-to-stand / at end / frame-above-stand / True | 2 |
| insert-frame / at start / frame-above-stand / True | 2 |
| move-tool-to-hook / at end / tool-at-hook / True | 1 |
| approach-tool / typical pose / frame_1->stand_1 / True | 1 |
| move-tool-to-hook / typical pose / gripper_1->tool_1 / True | 1 |
| move-frame-to-stand / typical pose / frame_1->stand_1 / True | 1 |
| move-tool-to-hook / over all / frame-in-stand / True | 1 |
| move-tool-to-hook / typical pose / frame_1->stand_1 / True | 1 |
| insert-frame / typical pose / gripper_1->frame_1 / True | 1 |
| move-frame-to-stand / at start / holding-frame / True | 1 |
