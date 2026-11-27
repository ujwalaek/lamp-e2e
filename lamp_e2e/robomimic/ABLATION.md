# Does the relative-pose method work by itself? (no-hardcoding ablation)

**Question.** Can LAMP's relative-pose regions detect execution failures *without* task knowledge written by hand?
If not, what exactly breaks?

**Short answer.** Yes, on both robomimic tasks, with generic settings only. Two things decide it:

- the **criticality threshold θ** (the share of demos that must visit a bin);
- **who the training demos come from**.

Pure LAMP with its default settings detects nothing on Square and about a third of the failures on Tool Hang.
For each gap, one single-setting experiment shows the cause.

## Setup

### The fully learned monitor (`eval_learned.py`)

Nothing task-specific is written in it:

| Previously written by hand (`durative.py`) | Now learned |
|---|---|
| Stages (approach / carry / insert / release) | Cut at the robot's own grasp events: `free0, carry1-<obj>, free1, ...` |
| Which object is carried, in which order | The most common carry sequence in the training demos |
| Named predicates (`holding`, `nut-on-peg`...) as hand-picked LAMP regions | Every LAMP region, plus every union of regions of the same object pair, used under its LAMP name |
| Conditions per stage | Every (predicate, true/false, at start / over all / at end) is a candidate. It is kept only if it held in at least a **cut-off** share of the normal training demos (98 / 95 / 90 / 80%). Irrelevant relations drop out by themselves. |
| Tolerances, durations | Learned from training demos, as before |

Two limits apply to the candidates:
- "Must *not* be in region X" is only used as an "over all" condition. Near a stage boundary it is almost always true, so it carries no information.
- The near misses (candidates that held in 60%–cut-off of the training demos) are logged. That log shows *why* a useful rule was not learned.

### Test set

- **Normal demos:**
  - 20 held-out proficient demos.
  - Square only: a held-out half of robomimic's other-operator demos (better 25, okay 50, worse 50, excluding copies of proficient demos).
- **Failures (physics rollouts):** drop, miss, slip, stall, wrong grasp, wrong peg (Square only).
  - A failure counts as caught only if an alarm fires **at or after** the moment it was injected.
  - Rollouts that still succeeded are left out, except stall.

### Settings kept fixed in every step

These are not task knowledge, but they are choices:
- **Motion-based grasp signal:** an object counts as held while it moves with the gripper.
- **Gripper frame:** turned 180° about x, a robot-level convention.
- **The LAMP search box:** ±15 cm. Object–object pairs use coarser bins, set per task in `domains.py`. LAMP's own code needs this box set by hand for every domain too.

## Square

Results at the 95% cut-off (full table for all cut-offs: `out/Square/ablation_summary.md`).

| Step (each adds one thing) | Regions | False alarms, held-out | Other operators: better / okay / worse | Drop | Miss | Slip | Stall | Wrong grasp | Wrong peg |
|---|---|---|---|---|---|---|---|---|---|
| A0 pure LAMP (35 bins, 61 angle bins, θ 1.0) | 1 | 1/20 | 7/25, 10/50, 21/50 | 0/20 | 0/20 | 0/17 | 20/20* | 0/12 | 0/20 |
| A1 + coarser bins (10 / 13) | 1 | 0/20 | 0/25, 10/50, 20/50 | 0/20 | 0/20 | 0/17 | 20/20* | 1/12 | 0/20 |
| A2 + θ 0.5 | 5 | 3/20 | 10/25, 27/50, 35/50 | 0/20 | 0/20 | 0/17 | 20/20* | 3/12 | 0/20 |
| A3 + peg symmetry (hand-coded) | 5 | 5/20 | 11/25, 30/50, 35/50 | **20/20** | **20/20** | **17/17** | 20/20 | 8/12 | **20/20** |
| A4 = A3 + **mixed-operator training** | 4 | **2/20** | **2/25, 5/50, 4/50** | 20/20 | 20/20 | 17/17 | **1/20** | 8/12 | 20/20 |
| A5 generic: θ 0.2, **no symmetry fix** | 11 | 6/20 | 14/25, 34/50, 36/50 | 20/20 | 20/20 | 17/17 | 20/20 | 10/12 | 20/20 |

\* Stalls are caught by the stage-duration check, not by poses.

### What each step shows

- **A0 to A2: θ = 1.0 is the blocker, not bin size.**
  - LAMP keeps only bins visited by *every* demo, and human grasps vary too much for that. Gripper–nut gets 0 regions at θ 1.0, with fine or coarse bins.
  - At θ 0.5 the grasp regions appear (3 gripper–nut regions).
- **A2 to A3: the peg's 4-fold symmetry blocks the goal rule.**
  - The nut can sit on the peg in 4 orientations, and LAMP treats them as different poses. So no single nut–peg region holds at the end of the carry, and the monitor has no goal rule. It catches **0** drops, misses, slips or wrong pegs.
  - Folding the symmetry by hand is the only change from A2. With it, "nut at peg when the carry ends" holds in 173/180 demos and is learned. It catches **all** of them.
- **A5: the symmetry fix is not needed.**
  - With θ 0.2 and no fix, LAMP learns one nut-on-peg region that spans the seating angles (6 yaw bins). Detection is as good as A3; it costs about one more false alarm in 20.
- **A3 to A4: one operator's style causes most false alarms on other people.**
  - Trained on proficient demos only, 44–70% of other operators' normal demos are flagged. The first alarm is "not at the grasp pose at the end of the approach" or "stage too slow".
  - Training on half of each operator group cuts this to 8–10% on the other half. No pose-based detection is lost.
- **A4: the new trade-off is stalls (20/20 to 1/20).**
  - Slow operators stretch the learned "normal stage length", so a frozen arm still looks normal.
  - Duration alone cannot both accept slow people and catch freezes.

## Tool Hang

Results at the 95% cut-off (full table: `out/ToolHang/ablation_summary.md`).

| Step | Regions | False alarms | Drop | Miss | Slip | Stall | Wrong grasp |
|---|---|---|---|---|---|---|---|
| A0 pure LAMP | 9 | 6/20 | 8/18 | 8/19 | 8/18 | 9/20 | 8/20 |
| A0 pure LAMP, cut-off 98% | 9 | 0/20 | 6/18 | 1/19 | 4/18 | 5/20 | 8/20 |
| A1 + coarser bins, cut-off 98% | 7 | 1/20 | 10/18 | 12/19 | 10/18 | 7/20 | 13/20 |
| A2 + θ 0.9 | 8 | 3/20 | 9/18 | 12/19 | 8/18 | 9/20 | 11/20 |
| A3 + tool frame fix (hand-coded) | 8 | 2/20 | 9/18 | 12/19 | 8/18 | 8/20 | 11/20 |
| A4 + frame–tool θ 0.3 (hand-tuned, one pair) | 9 | **2/20** | **18/18** | **19/19** | **18/18** | **15/20** | **20/20** |
| A5 generic: θ 0.3 for every pair, no tool fix | 19 | 6/20 | 18/18 | 19/19 | 18/18 | 15/20 | 20/20 |

### What each step shows

- **A0 to A1: bins that are too fine.** Coarser bins lift detection from about one third to about two thirds, at 1 false alarm.
- **A3: the 180° tool-angle flip does not matter.** The tool-frame fix changes nothing.
- **A3: the "tool on hook" relation is missing.**
  - Failures during the *frame* carry are mostly caught.
  - Failures during the *tool* carry are almost all missed: drop 0/5, slip 0/8, stall 0/10.
  - That stage has no rule about where the tool must end up. The hung tool's pose spreads over several bins, so at θ 0.9 no frame–tool region describes "on the hook".
- **A4: lowering θ for that one pair makes "tool on hook" a region.**
  - "Tool at the hook when the tool carry ends" is then learned (171/180), and the monitor catches every drop, miss, slip and wrong grasp.
- **A5: the per-pair tuning is not needed.**
  - The same low θ for all pairs gives the same detection, but more false alarms (6/20 vs 2/20), because there are 19 regions and more rules.

## Where the remaining false alarms come from

These are the first rules to fire on normal demos (`why_missed_learned.py`):

- **Grasp pose at the end of the approach.** The pose is outside the learned grasp regions in position and rotation. It is the main cause on Square (generic version) and on other operators.
- **Stage too long.** Slow operators; mainly the "worse" group.
- **Hard bin edges.** Several alarms are "rotation only" or "position only": the pose is one bin outside a region while still typical.

## Conclusions

1. **The relative-pose idea works without task knowledge.** On both tasks, all pose-type failures (drop, miss, slip, wrong grasp, wrong peg) are caught. The generic settings are coarse bins, a low θ, automatic unions of regions, and stages from grasp events.
2. **LAMP's default θ = 1.0 is the main reason it "doesn't work" on human demos.** Real demos never all pass through the same fine bin.
3. **Detection is decided by one goal rule per carry.** That rule is "object at its target when the carry ends". If the relation behind it is not learned (symmetric peg, spread-out tool on hook), every failure in that carry is missed. The near-miss log shows this directly.
4. **False alarms are the real cost.** Lower θ and lower cut-offs add rules, and some of them normal demos also break. Training on demos from several operators is the most effective fix found (on Square, other-operator false alarms fell from 44–70% to 8–10%).
5. **The timing check conflicts with operator variety.** It catches stalls only if all training operators are fast.

## Files

- `eval_learned.py`: the learned monitor.
- `ablation.sh`: all steps.
- `ablation_summary.py`: the tables.
- `why_missed_learned.py`: per-stage miss and false-alarm analysis.
- `out/<Domain>/durative_learned_<step>_q<cut-off>/`:
  - `durative_eval.json`: results, the learned rules and near misses.
  - `<domain>_learned.pddl`: the learned durative PDDL model.
- `convert.py` `mh_split`, `LAMP_MH_TRAIN=1`: the mixed-operator split (even positions train, odd test).
