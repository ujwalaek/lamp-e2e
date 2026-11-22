# LAMP on robomimic: Square and Tool Hang

LAMP's pipeline (relative poses → relational critical regions → predicates → action model) applied to
two robomimic tasks with **real human teleoperated demonstrations**, then used as an execution monitor.

**Summary:**
- **With LAMP as published (θ = 1.0, 1 cm / 6° bins), human data mostly breaks predicate invention.**
  - Square: "holding the nut" is never learned, and the one predicate it does learn doesn't line up with "nut on peg".
  - Tool Hang: one predicate, "frame inserted in stand", is learned well.
- **Two parts of LAMP's representation cause most of the trouble.**
  - Its criticality count rewards bins where an object rotates.
  - Its rotation vectors flip sign at the 180° grasp a real gripper uses.
- **Correcting the representation makes predicates usable.**
  - Tool Hang: "frame in stand" reaches F1 0.99 (precision 99.6%, recall 98.6%) against robosuite's own flag, learned with no labels.
  - Square: "holding" reaches F1 0.62.
- **The action model is the weak link for monitoring.** On human data it is either too loose (Square: drops and misses are not caught) or too strict (Tool Hang: 75–100% false alarms on normal runs). On neither task does it separate failures from normal runs.

## Data

| | Square | Tool Hang |
|---|---|---|
| Task | Pick a square nut and place it on a square peg | Insert a hook frame into a stand, then hang a wrench on the hook |
| robomimic file | `square/ph/low_dim_v15.hdf5` (51 MB) | `tool_hang/ph/low_dim_v15.hdf5` (199 MB) |
| Demos | 200 proficient-human (180 train / 20 held out, robomimic's own split) | same |
| Steps per demo (20 Hz) | 107–236 | 332–744 |
| Objects in LAMP | gripper, nut, peg (fixed; pose from the scene XML) | gripper, stand, frame, tool |
| Ground truth for checking | robosuite's `on_peg` rule; grasp flag | robosuite's `frame_is_assembled`, `tool_on_frame` flags; grasp flag |

**Held-out test sets (from the 20 held-out demos):**
- **nominal:** the 20 real demos, unchanged.
- **drop:** the 20 demos with a failure injected half-way through the last carry. The object is released and falls back to its resting height.
- **miss:** the 20 demos with the arm and object shifted 15 cm sideways from half-way through the last carry, so the object is put down away from its target.

## Run

```bash
bash lamp_e2e/robomimic/download.sh square tool_hang                 # ~250 MB into datasets/ (not in git)
bash lamp_e2e/robomimic/run_variant.sh square    base   "1.0 0.9 0.7 0.5 0.3"
bash lamp_e2e/robomimic/run_variant.sh square    coarse "1.0 0.9 0.7 0.5"
bash lamp_e2e/robomimic/run_variant.sh tool_hang base   "1.0 0.7"
bash lamp_e2e/robomimic/run_variant.sh tool_hang coarse "0.9 0.7 0.5"
```

Results go to `lamp_e2e/out/<Square|ToolHang>/sweep_<variant>/theta_<θ>/`, with a `summary.md` per sweep. Each θ folder holds:
- the learned `domain.pddl` and `abstract_demos.txt`
- monitor rates (`monitor_env9.json` for nominal, `monitor_env8.json` for drop and miss)
- the ground-truth comparison (`gt_eval.json`, `evaluate.log`)

Time on a 12-core CPU: about 1.5 min per θ for Square and 6–12 min per θ for Tool Hang.

| File | Role |
|---|---|
| `convert.py` | robomimic hdf5 → LAMP `EnvState` demos (poses, inferred grasp flag, train/test split, injected failures, ground truth) |
| `domains.py` | LAMP domain configs for Square and ToolHang, registered in memory by `lamp_env.py` (nothing is added to the LAMP repo) |
| `run_variant.sh`, `sweep.sh` | convert → poses → θ sweep → learn → predict → evaluate |
| `evaluate.py` | compares each learned predicate with ground truth (accuracy, precision, recall, F1) |
| `debug_bins.py`, `debug_rotation.py`, `why_missed.py` | the diagnostics behind the findings below |

**Variants:**
- **base:** LAMP as-is. End-effector frame, 35 position bins per axis (≈ 0.9 cm), 61 angle bins (≈ 6°).
- **toolframe:** the gripper pose expressed in a frame rotated 180° about x, so a top-down grasp reads as near-zero rotation (as in LAMP's own simulated grasps). Nothing else changes.
- **coarse:** toolframe, plus 10 position bins for gripper pairs (≈ 3 cm) and 13 angle bins (≈ 30°).

In every variant θ is the same for all pairs. LAMP's own configs use 1.0 for gripper–object pairs in Packing, Keva and Jenga, and between 0.001 and 1.0 in CafeWorld.

## Results

F1 is for the learned predicate that best matches each ground-truth event on the held-out nominal states. "Flagged" uses the transition-and-precondition check plus the goal check.

### Square

| Variant | θ | Predicates (RCRs) | "holding" F1 | "nut on peg" F1 | Flagged: nominal / drop / miss |
|---|---|---|---|---|---|
| base | 1.0 | nut–peg 1 | – (none learned) | 0.00 | 0% / 0% / 0% |
| base | 0.5 | gripper–nut 2, nut–peg 2 | 0.07 | 0.27 | 5% / 0% / 0% |
| base | 0.3 | gripper–nut 2, nut–peg 2 | 0.19 | 0.60 | 10% / 0% / 0% |
| toolframe | 0.7 | gripper–nut 1, nut–peg 2 | 0.06 | 0.27 | 0% / 0% / 0% |
| coarse | 0.9 | gripper–nut 2, nut–peg 1 | 0.49 | 0.38 | 5% / 0% / 0% |
| coarse | 0.5 | gripper–nut 3, nut–peg 2 | **0.62** | 0.57 | 0% / 5% / 0% |

### Tool Hang

| Variant | θ | Actions learned | "frame in stand" F1 | "tool on frame" F1 | "holding" F1 | Flagged: nominal / drop / miss |
|---|---|---|---|---|---|---|
| base | 1.0 | 78 | 0.91 (precision 99.5%, recall 83.7%) | 0.08 | 0.40 | 95% / 65% / 65% |
| base | 0.7 | 71 | 0.76 | 0.06 | 0.57 | 90% / 75% / 75% |
| coarse | 0.9 | 59 | **0.99** (precision 99.6%, recall 98.6%) | 0.10 | 0.54 | 75% / 80% / 85% |
| coarse | 0.7 | 108 | 0.99 | 0.10 | 0.54 | 100% / 60% / 55% |
| coarse | 0.5 | 108 | 0.80 | 0.07 | 0.71 | 100% / 85% / 75% |

## Findings

**1. LAMP's criticality measure is not "fraction of demos" on dense data.**
- `RelativeOccupancyMap.create_frequency_map` adds one count to a position bin for every *distinct (position, orientation, sensor)* combination a demo visits there.
- On Square, the bin where the nut sits seated is visited by 96.7% of demos (one count each, because the nut is still) and is rejected at θ = 1.0.
- A bin half-way down the peg, visited by only 77% of demos, passes, because the nut twists through many orientation bins while sliding and gets counted several times per demo.
- LAMP's simulated demos are sparse waypoints with little rotation, so the difference never showed up there.

**2. Rotation vectors break for real grippers.**
- A top-down gripper is about 180° from the object's frame. That is where the axis-angle vector flips sign.
- On Square, 91% of holding states sit within 10° of the flip.
- The vector flips mid-grasp in 69 of 180 demos.
- One physical grasp spreads over 219 distinct angle-bin triples (`debug_rotation.py`).
- Expressing the gripper in a frame where a top-down grasp is near zero rotation removes the flip. On its own that isn't enough with 6° bins; it needs coarser bins as well.

**3. LAMP's predicates are precise but fragmented.**
- When a learned predicate is true it is almost always right: 99–100% precision for "frame in stand" and for the gripper predicates.
- Recall is low for anything that varies between people: grasp offsets (6 cm spread along the nut handle) and the hung tool (about 3 cm spread, swinging).
- Rigid, repeatable contacts (frame seated in stand, nut seated on peg) are learned. Variable ones are not.

**4. The symbolic action model doesn't make a monitor on human data.**
- **Square: too loose.** Predicates flicker during normal handling, so "losing hold of the nut" happens in normal demos and becomes a learned action (26 of 37 actions remove a gripper predicate). "Nut on peg" isn't true at the end of every training demo, so the goal check is empty. Drops and misses look normal (0–5% caught).
- **Tool Hang: too strict.** 180 human demos produce 59–108 actions and up to 290 distinct transitions. Held-out demos almost always contain an unseen one, so 75–100% of normal runs are flagged.
- In both tasks the failure rates are no higher than the false-alarm rate, so the monitor can't tell failures from normal runs.

## What this suggests for execution monitoring

- **Keep:** relative-pose regions as a way to find contact relations without labels. "Frame in stand" at F1 0.99 shows they can work.
- **Change:**
  - Use a rotation representation without a wrap point (quaternion distance or a rotation matrix), and use per-pair bin sizes.
  - Count criticality per demo, as the paper defines it.
  - Score states with the GMM likelihood (a graded "how far from the region" signal) rather than hard bin membership.
  - Smooth predicates over time before reading transitions.
  - Replace the all-or-nothing transition check with transition frequencies learned from the demos, plus explicit goal conditions.

## Caveats

- **The grasp flag is inferred:** gripper commanded closed, object within 12 cm, fingers not fully shut. robomimic doesn't record it.
- **The failures are injected into real demos**, not recorded from a robot that actually failed.
- **Time steps are subsampled:** every 5th (Square) or 10th (Tool Hang) step, plus the steps around every grasp and release.
- **Bin ranges for the new object pairs were chosen by me** (LAMP has no configs for these tasks). θ was swept with one value for all pairs, not tuned per pair.
- **The `holding` score** compares single predicates with one flag covering every held object. In Tool Hang, "holding the frame" and "holding the tool" are separate predicates, so each one can recall at most part of it.
