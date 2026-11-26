# Stage-aware durative monitoring on LAMP's learned regions

Two things :
- A **durative PDDL model** for each task.
- Detectors that are **used only during their stage**, ignoring task-irrelevant relations. For example, the gripper–peg relation only matters while approaching the peg, and the gripper–nut relation should be verified while the nut is being moved to the peg.

A third question was why each false alarm or miss happened: why did those poses go in or out of distribution?

## What the monitor does

- **Durative model:** `durative.py` defines each task as a sequence of durative actions (stages). Each stage has PDDL 2.1 conditions: *at start*, *over all* and *at end*. The generated models are:
  - `out/Square/durative_pegsym_dilate1/square_durative.pddl`
  - `out/ToolHang/durative_coarse_dilate1/toolhang_durative.pddl`
- **Predicates:** each named predicate (`holding`, `nut-on-peg`, `frame-in-stand`, …) is a union of LAMP's learned regions. The mapping comes from each region's grasp-sensor value and relative-pose range (`describe_regions.py`).
- **Stages are found from the robot's own commands.** Gripper close/open splits approach / carry / release. Inside a carry, the split comes at the moment the approach subgoal is first reached (e.g. nut aligned with the peg).
- **Only the relations named in the current stage are checked.** Everything else is ignored. For example, gripper→peg is never checked, and nut→peg is ignored while approaching the nut.
- **Tolerances are learned from the 180 training demos,** not hand-set:
  - how long an *over all* condition may flicker,
  - how far from a stage boundary an *at start* / *at end* condition may be met,
  - each stage's duration range (written into the PDDL, not yet used for alarms).

| Square stage | Relevant relations | at start | over all | at end |
|---|---|---|---|---|
| approach-nut | gripper–nut | | not holding | ready to grasp |
| move-nut-to-peg | gripper–nut, nut–peg | holding | holding | nut at peg |
| insert-nut | gripper–nut, nut–peg | nut at peg | holding | nut at peg |
| release-and-retreat | gripper–nut, nut–peg | nut at peg | nut at peg | nut seated on peg, not holding |

**Tool Hang stages:**
1. approach-frame
2. move-frame-to-stand (holding frame; ends with frame above stand)
3. insert-frame (holding frame; ends with frame in stand)
4. approach-tool (frame stays in stand; ends at the tool grasp)
5. move-tool-to-hook (holding tool and frame in stand; ends with tool lined up at the hook)
6. hang-tool-and-retreat (frame stays in stand). Its end condition, *tool on hook*, **cannot be checked: LAMP never learned that relation.**

## Test set and counting

- **Runs:** 20 held-out demos per task.
  - **nominal:** the recorded human demo. Any alarm is a false alarm.
  - **drop:** a physics rollout with the gripper opened half-way through the last long carry.
  - **miss:** a physics rollout with the arm pushed sideways half-way through the last long carry.
- **Which runs count as failures:** only rollouts that really fail robosuite's success check. A failure counts as **detected only if an alarm fires at or after the injected failure.** Earlier alarms are reported separately.

## Results

### Square

| Version | False alarms (20 normal) | Drops caught (after the drop) | Misses caught (after the push) |
|---|---|---|---|
| Durative, first stage model | 17 | 20/20 | 20/20 |
| Stage model corrected: humans release the nut ~8 cm up the peg and it slides down, so "seated" is required at the end of release, not at release | 13 | 20/20 | 20/20 |
| + peg symmetry: the square peg's frame is defined up to 90°, so all 4 seatings map to one orientation | 7 | 20/20 | 20/20 |
| + each learned region widened by 1 bin | **1** | **20/20** | **20/20** |

### Tool Hang

| Version | False alarms (20 normal) | Drops: caught after / early alarm only / missed | Misses: caught after / early alarm only / missed |
|---|---|---|---|
| Regions as learned | 15 | 13 / 4 / 1 (of 18) | 18 / 1 / 0 (of 19) |
| Regions widened by 1 bin | 3 | 9 / 2 / 7 (of 18) | 17 / 1 / 1 (of 19) |

(2 drops and 1 miss still succeeded physically and are not counted.)

## Why the false alarms and misses happen

For every alarm, `eval_durative.py` records:
- which pose dimensions put the pose outside the nearest learned bin (position, angle or grasp sensor),
- whether the pose was typical of the training demos in that stage. This uses a k-NN distance in a continuous pose space with rotation matrices, so there is no angle wrap; "typical" means within the 99th percentile of training nearest-neighbour distances.

The full lists are in each variant's `durative_report.md`.

**False alarms: almost all are normal poses that LAMP's regions are too narrow to cover.**

| Cause | Where | Fix tried |
|---|---|---|
| Symmetric orientations missing | Square: the peg accepts the nut 4 ways, but LAMP learned only 2 (yaw ±90°). Nuts seated at ~180° fell outside. | Fold the peg's 4-fold symmetry into its frame: 13 → 7 |
| Stage model contradicted by the data | Square: "seated" was required at release, but people let go ~8 cm up the peg | Require "aligned" at release and "seated" at the end: 17 → 13 |
| Regions one bin too tight for human variation | Square: nut released 1–3 cm off-axis or tilted 17–30°; grasp 2 cm off-centre on the handle. Tool Hang: grasp on frame/tool a few cm off the learned bin. All typical of training. | Widen regions by 1 bin: Square 7 → 1, Tool Hang 15 → 3 |
| How people do the task | Tool Hang: frame left ~1 cm less inserted; wrench lowered straight onto the hook without passing the learned "lined up" pose | Not fixed |
| My grasp-flag inference / stage splitting | Square demo_191 and Tool Hang demo_36: the person re-grasps, or ends with the gripper closed again, so a stage boundary is misplaced | Not fixed (would need a better grasp signal) |

**Misses (Tool Hang only):** the wrench is dropped when it's already at hook height. "Tool lined up at hook" is satisfied, so the carry looks complete. The only condition that could catch it, *tool on hook* at the end, was never learned by LAMP (the hanging wrench swings and lands in a different place each time). Widening regions makes the "lined up" region broad enough to include these moments, which is why misses rise from 1 to 7.

**Early alarms in failure runs (Tool Hang):** the physics replay drifts slightly from the recording, so the frame sometimes seats a moment late and an alarm fires before the injected failure.

## Takeaways

- **Stage-aware durative checks work.** On Square they catch every drop and miss at the moment it happens, with 1 false alarm in 20, using only LAMP's learned regions plus task knowledge (stages, the peg's symmetry).
- **What's left is mostly about LAMP's regions, not the stage logic:**
  - symmetric objects need their symmetry folded in;
  - regions need some spatial slack for human variation;
  - relations that vary a lot (a hanging, swinging wrench) aren't learned at all, which leaves the final stage of Tool Hang uncheckable.
- **Widening regions by a fixed bin count is a blunt tool.** On Tool Hang's coarser object bins it trades false alarms for misses. Slack per relation, or scoring with the GMM likelihood instead of hard bins, is the obvious next step.

## Reproduce

```bash
bash lamp_e2e/robomimic/relearn_square_pegsym.sh                # Square model with peg symmetry
bash lamp_e2e/robomimic/run_durative.sh square    "0 1"        # Square, regions as learned / widened
bash lamp_e2e/robomimic/run_durative.sh tool_hang "0 1"        # Tool Hang (coarse theta 0.9 model)
venv/bin/python lamp_e2e/robomimic/durative_summary.py Square pegsym_dilate0 pegsym_dilate1
bash lamp_e2e/robomimic/make_durative_videos.sh square    "nominal drop miss" demo_5
bash lamp_e2e/robomimic/make_durative_videos.sh tool_hang "nominal drop miss" demo_5
```

Video demos were chosen by rule: the first held-out demo whose nominal run has no alarm and whose drop and miss are both caught after the failure (`pick_demo.py`). For Square, demo_5 is also the demo used in the earlier videos.
