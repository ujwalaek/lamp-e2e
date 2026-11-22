# Rollout videos with LAMP's learned regions

Each video replays a **held-out robomimic demo in the MuJoCo physics simulator** (robosuite 1.5.1, `agentview`
camera, 20 fps) and labels every frame with the LAMP model learned from the 180 training demos.

## Cases

| Case | What is done to the recorded human actions | Result in simulation |
|---|---|---|
| nominal | replayed unchanged | task succeeds |
| drop | gripper commanded open half-way through the last carry | object really falls, task fails |
| miss | arm pushed sideways (y action +1.0 for 12 steps) half-way through the last carry | object is put down away from its target, task fails |

The drop and miss failures are **physically simulated**, not edited poses. Each video's title says whether robosuite's own success check passed.

## What the overlay shows (right-hand panel)

For every object pair, e.g. gripper → nut:

- **pos / rot:** the second object's pose in the first object's frame, computed exactly as LAMP does (`useful_functions.get_relative_pose`). Position is in cm; rotation is shown as roll, pitch and yaw in degrees.
- **Status bar:**
  - **green, "IN learned region <predicate>":** one of the regions LAMP learned for this pair contains the current pose. This is LAMP's own test: the binned pose plus the grasp sensor must be inside the region.
  - **red, "OUTSIDE learned regions":** no learned region of this pair contains the pose.
  - **grey:** LAMP learned no region for this pair at all.
- **Plain-language names:** a name like "(~nut on peg)" after a predicate is the ground-truth event it matches best on held-out data (F1 ≥ 0.4). LAMP itself only numbers its predicates.
- **Timeline strip:** the same colour for every frame of the rollout, with a black cursor at the current frame.

## How to read it

Red is not by itself a failure. During free motion (approaching, carrying, retreating) objects are between the
learned regions, and LAMP's negation predicate (`<pair>_0`) is true there. The useful signals are:
- a region that should be **reached** but isn't (miss: nut → peg never turns green at the end),
- a region that is **left too early** (drop: the green "holding" stretch on gripper → nut ends mid-carry).

## Models used

| Task | Representation | θ | Why |
|---|---|---|---|
| Square | coarse (tool frame, ~3 cm, 30° bins) | 0.5 | best "holding" and "nut on peg" match |
| Tool Hang | coarse | 0.9 | best "frame in stand" match (F1 0.99) |

See `../../robomimic/README.md` for those results.

## Files

| File | Demo | Note |
|---|---|---|
| `rollouts_overview.mp4` | | the six main clips below joined into one video, with a title card before each |
| `square_nominal.mp4`, `square_drop.mp4`, `square_miss.mp4` | demo_5 | first held-out demo whose final state LAMP recognises as "nut on peg" (12 of 20 held-out demos do) |
| `square_nominal_demo0_yawflip.mp4` | demo_0 | successful run where LAMP still flags nut → peg as outside: the nut sits at +175° yaw, at the 180° rotation-vector jump |
| `tool_hang_*.mp4` | demo_36 | nominal / drop / miss. Tool Hang needs millimetre precision, so replaying recorded actions open-loop succeeds for only 4 of the 20 held-out demos (`replay_scan.py`). demo_36 is the first of those. |
| `*_last.png` | | last frame of each video |
| `*.json` | | success flag, carry window, fraction of frames outside the learned regions per pair |

To regenerate: `bash lamp_e2e/robomimic/make_videos.sh square|tool_hang ["nominal drop miss"] [demo]`.
