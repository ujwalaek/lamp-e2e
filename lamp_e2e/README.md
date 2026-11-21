# LAMP end-to-end pipeline (small-data, Python 3, no OpenRAVE)

A working **demos → relative poses → relational critical regions (RCRs) → predicates + action model → predicate prediction**
pipeline for [LAMP, arXiv:2402.11871](https://arxiv.org/abs/2402.11871), built on the authors' code
([aair-lab/lamp](https://github.com/aair-lab/lamp), commit `998428c`, cloned to `../lamp`).

**What is reused vs replaced**
- **Reused, unmodified:** every learning step runs LAMP's own classes: `DataAugmenter`, `BinnedEnvState`, `Discretizer`, `RelativeOccupancyMap`,
  `Relation` + `MultiVariateGaussian`, `PDDLState`, `TrajAbstracter`, `TransitionGraph`, `TransitionClusters`,
  `LiftedPDDLAction` and `WorldModel`, with `domain_configs/PackingConfig.py` hyperparameters.
- **Replaced:** only the simulator. LAMP's repo is Python 2.7 + OpenRAVE + ROS. `gen_demos.py` re-implements the logic of
  `src/data_gen/Packing.py` kinematically in numpy and writes `EnvState` pickles in the exact format and paths LAMP expects.
- **Patched at runtime** (`py3_patches.py`, `_lamp_path.py`; the repo itself is untouched): a torch stub (used only by unused
  tensor helpers), py3 `merge_dicts`, and the GMM score thresholds that `PackingConfig` lacks (`MVG_SCORE_THRESHOLD=3`, CafeWorld's value).

## Run

```bash
cd ~/lamp_work
lamp_e2e/run_all.sh                 # ~2 min on CPU; options: --n_full 30 --n_partial 30 --n_test 3 --seed 0
```
Env: `~/lamp_work/venv` (numpy, scipy, scikit-learn, tqdm, networkx). To recreate it:
`python3 -m venv --without-pip venv && python3 -m pip --python venv/bin/python install numpy scipy scikit-learn tqdm networkx`.

## Pipeline: paper ↔ LAMP code ↔ this repo

| # | Paper | LAMP code | Script | Output |
|---|---|---|---|---|
| 1 | Unannotated demos: 6-D poses of objects + robot links (+ grasp flag) | `gen_data.py`, `src/data_gen/Packing.py`, `SimClass.get_one_state` | `gen_demos.py` | `lamp/Data/Packing/misc/envN/envN_data.pkl` |
| 2 | ξ: absolute → relative poses for each object pair | `augment_data.py` → `DataAugmenter`, `useful_functions.get_relative_pose`, `BinnedEnvState` | `extract_poses.py` | `binned_envN_data.pkl`, `envN_relposes.npz` |
| 3 | Pairwise occupancy + criticality μ(ρ)>θ + connected components → RCRs | `gen_rom.py` → `RelativeOccupancyMap` | `learn_rcrs.py` | `60_0_rcr_indices.pkl` |
| 4 | One relation per RCR, GMM predictor ψ, abstraction α, transition clustering, pre = ∩ pre-states | `gen_world_model.py` → `get_lifted_relations_dict`, `Relation`, `PDDLState.get_from_ll`, `TransitionClusters`, `LiftedPDDLAction` | `learn_model.py` | `60_0_Packing_0.pkl`, `lamp/Domains/Packing/domain.pddl`, `out/abstract_demos.txt` |
| 5 | Evaluate predicates on new states | `Relation.evaluate_in_ll_state` | `predict.py` | `out/predictions_env9.csv`, `out/predict_log.txt` |

### Implementation details worth knowing (things the paper leaves out)
- **Pose representation:** 6-D `[x, y, z, rotvec]` (axis-angle), relative pose = `inv(T_a) @ T_b`. Robot links are just objects
  (`gripper_1`, `freight_1`) whose entry is `[joint_values, link_pose]`. Pairs come from a type filter (`DataAugmenter.filter`):
  robot types come first, and gripper–surface and surface–surface pairs are skipped.
- **Discretization drives everything.** Each type pair has a box range and bin counts (`DISCRETIZER_PARAMS`). The relational grid is the world grid ×2√2.
  Angles are rounded to 0.05 rad and binned into 61 bins per axis.
- **The grasp flag is a pose dimension.** The occupancy tensor is `[x, y, z, angle-slot, grasp-sensor]`. The sensor value is 0 = free,
  1 = holding this object, 2 = holding another. This is how "holding" and "aligned but not holding" become separate predicates.
- **Criticality θ = `EVAL_THRESHOLDING_VALUES`**: the fraction of demos that must visit a bin (gripper–can 1.0, can–surface 0.032).
  Each bin counts once per demo. The angle threshold is relaxed until every position bin has orientation support.
  Then `scipy.ndimage.label` runs on the 3-D position occupancy, and each component becomes one RCR.
- **Labelling uses bin-set membership, not GMM likelihood.** `Relation.evaluate_in_ll_state` checks whether the discretized
  relative pose (either direction) plus the sensor value is in the RCR's bin set. The BayesianGMM (`n_components = #bins`, fit to
  uniform samples inside the bins) is used for *sampling* poses during plan refinement. `predict.py` reports both. On this data they
  agree on 99.8% of the 954 test evaluations.
- **Relation `_0` is the negation**: true when the pose is in none of the pair's RCRs. `clear3_*` predicates are LAMP's auxiliary
  "free-region" relations (the paper's R^free).
- **There's no neural network.** "Training a model" here means occupancy counting, connected components, and fitting GMMs.

## Results on the small dataset

60 demos: 30 full in env1, plus 30 truncated in env2 (LAMP's way of adding non-goal-reaching demos). Learned:

```
gripper_can_1  gripper at the grasp pose above the can, magnet ON     ("holding")
gripper_can_2  gripper at the same pose, magnet OFF                   ("aligned / about to grasp / just released")
can_surface_1  can inside the box region                              ("in box")
(+ gripper_can_0, can_surface_0 = negations; names are LAMP's, the glosses are mine)
```
There are 5 lifted actions in `domain.pddl`: approach (`_0→_2`), grab (`_2→_1`), carry-into-box (`can_surface_0→1` while holding),
release (`_1→_2`, needs `can_surface_1`), retreat (`_2→_0`). The action numbers (`a1..a5`) change between runs (Python hash/set
ordering inside LAMP). The learned actions themselves don't.

**Held-out test demos (env9)** are labelled at every state, and each abstract transition is checked against the learned actions
(the effect must match a cluster *and* the cluster's intersected precondition must hold):

| test type | what happens | monitor |
|---|---|---|
| nominal ×3 | full pick-and-place | OK, every transition explained by approach → grab → carry-in → release → retreat |
| drop ×3 | magnet fails mid-carry, can falls | ANOMALY: `holding → free` has no learned action |
| miss ×3 | can released outside the box | ANOMALY: release effect fires but the precondition `can_surface_1` is missing |

## Caveats
- The data is synthetic and kinematic (straight-line "motion plans" with random lifts and jitter, no physics, perfect state estimation, as in the paper's sim).
  The first version used deterministic paths, and LAMP turned the repeated waypoints into spurious RCRs. Waypoint variability matters, because θ is a visit frequency.
- I've only exercised the Packing domain (1 can). Multi-object domains (Keva, Jenga) add same-type pairs and `CONST_TYPES`
  handling, which have more py2-isms that this run never hit.
- Planning and refinement (`run_lamp.py`, FF/K* planners, OpenRAVE IK) are not ported. They aren't needed for predicate learning or prediction.
- The precondition check in `predict.py` lifts states by type, which is enough for one object per type. Multi-object scenes would need LAMP's parameter mapping.
