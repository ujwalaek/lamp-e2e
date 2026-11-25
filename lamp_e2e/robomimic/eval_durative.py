"""
Evaluate the stage-aware durative monitor (durative.py) and explain every false alarm and miss.

Test set (robomimic held-out 'valid' demos, 20 per task):
  nominal : the recorded human demos (they all succeed)          -> any alarm is a FALSE ALARM
  drop    : physics rollout, gripper opened half-way through the last carry
  miss    : physics rollout, arm pushed sideways half-way through the last carry
            (a drop/miss rollout counts only if robosuite's success check says the task really failed;
             an unflagged real failure is a MISS)
Training demos (180) are used to learn tolerances, durations and the pose distributions for diagnosis.

For every violation the report gives the stage, the condition, the relation, the relative pose, which pose
dimensions fell outside the learned region (position bins / angle bins / grasp sensor), and whether that pose
was nevertheless typical of the training demos in the same stage (k-NN distance in a continuous pose space
with rotation matrices, so there is no angle wrap-around).

usage: eval_durative.py --task square|tool_hang [--stride 1] [--n_test 20]
"""
import argparse
import json
import os
import pickle
import sys
import time

os.environ.setdefault("MUJOCO_GL", "egl")
import h5py  # noqa: E402
import numpy as np  # noqa: E402
from scipy.spatial import cKDTree  # noqa: E402
from scipy.spatial.transform import Rotation as R  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE)); sys.path.insert(0, HERE)
import lamp_env  # noqa: E402
import convert  # noqa: E402
import durative as DUR  # noqa: E402

ANG_DIM = {3: "roll", 4: "pitch", 5: "yaw"}
POS_DIM = {0: "x", 1: "y", 2: "z"}


# ----------------------------------------------------------------------------- labelling
class Labeller:
    def __init__(self, Config):
        import useful_functions as uf
        from src.data_structures.WorldModel import WorldModel
        self.uf, self.Config = uf, Config
        prefix = open(Config.DATA_MISC_DIR + "latest_prefix.txt").read().strip()
        WorldModel.set_params(prefix)
        self.model = WorldModel.load_model(0)
        self.rels = [r for d in self.model.relations.values() for cr, r in d.items() if cr != 0]

    def name(self, r):
        return "{}_{}_{}".format(r.parameter1_type, r.parameter2_type, r.cr)

    def label(self, states):
        """-> dict lamp_pred -> bool array, and per-frame grounded info for diagnosis.
        With LAMP_DILATE=k each learned region is widened by k bins in every pose dimension (grasp sensor exact);
        with k = 0 the result is identical to LAMP's Relation.evaluate_in_ll_state (checked in self_test)."""
        uf = self.uf
        objs = list(states[0].object_dict.keys())
        out = {self.name(r): np.zeros(len(states), dtype=bool) for r in self.rels}
        grounded = {}
        for r in self.rels:
            a = [o for o in objs if o.split("_")[0] == r.parameter1_type][0]
            b = [o for o in objs if o.split("_")[0] == r.parameter2_type][0]
            grounded[self.name(r)] = (r, r.get_grounded_relation(uf.Link(a, r.parameter1_type),
                                                                 uf.Link(b, r.parameter2_type), objs), a, b)
        k = int(os.environ.get("LAMP_DILATE", "0"))
        for t, s in enumerate(states):
            for n, (r, g, a, b) in grounded.items():
                out[n][t] = self.member(r, s, a, b, k)
        return out, grounded

    _sets = {}

    def region_set(self, r, k):
        key = (id(r), k)
        if key not in self._sets:
            import itertools
            base = {tuple(int(v) for v in rb) for rb in r.region}
            if k == 0:
                self._sets[key] = base
            else:
                offs = list(itertools.product(range(-k, k + 1), repeat=6))
                self._sets[key] = {tuple(rb[i] + o[i] for i in range(6)) + (rb[6],) for rb in base for o in offs}
        return self._sets[key]

    def member(self, r, s, a, b, k):
        """Mirror of LAMP's Relation.evaluate_for_map_in_ll_state for cr > 0 (both directions, grasp flag)."""
        uf, C = self.uf, self.Config
        pa, pb = link_pose(C, s, a), link_pose(C, s, b)
        d1 = r.discretizer.get_discretized_pose(uf.get_relative_pose(pb, pa), is_relative=True)
        d2 = r.discretizer.get_discretized_pose(uf.get_relative_pose(pa, pb), is_relative=True)
        grab = 0
        if s.grabbed_flag_1 and C.GRIPPER_NAME in (r.parameter1_type, r.parameter2_type) and \
                s.grabbed_object_1 in (a, b):
            grab = 1
        S = self.region_set(r, k)
        if r.parameter1_type == r.parameter2_type:
            return tuple(d2) + (grab,) in S
        return tuple(d1) + (grab,) in S or tuple(d2) + (grab,) in S

    def self_test(self, states, n=200):
        """Our membership with k=0 must equal LAMP's own evaluation."""
        _, grounded = self.label(states[:1])
        bad = 0
        for s in states[:n]:
            for name, (r, g, a, b) in grounded.items():
                bad += int(self.member(r, s, a, b, 0) != g.evaluate_in_ll_state(s))
        return bad


def link_pose(Config, s, n):
    p = s.object_dict[n]
    return p[1] if n.split("_")[0] in Config.ROBOT_TYPES else p


# ----------------------------------------------------------------------------- runs
def make_run(task, domain, d, lab, stride):
    """d: convert.build_demo dict (full rate). Subsample, label, segment."""
    from src.data_structures.EnvState import EnvState
    if os.environ.get("LAMP_PEG_SYMMETRY") == "1":
        d = dict(d, poses=convert.canonicalize_peg(d["poses"]))   # also applies to cached runs
    steps = list(range(0, d["T"], stride))
    sub = dict(T=len(steps), poses={k: v[steps] for k, v in d["poses"].items()},
               held=[d["held"][t] for t in steps], flags=d["flags"])
    states, _ = convert.to_envstates(sub, 1, EnvState)
    lamp_true, grounded = lab.label(states)
    truth = DUR.named_truth(domain, lamp_true)
    cmd = np.asarray(d["cmd"])[steps]
    stages = DUR.segment(domain, sub["held"], cmd, truth)
    return dict(states=states, lamp=lamp_true, truth=truth, stages=stages, held=sub["held"], cmd=cmd,
                grounded=grounded)


def demo_from_hdf5(f, name, task):
    g = f["data"][name]
    d = convert.load_demo(g, task, tool_frame=True)
    d["cmd"] = g["actions"][:, -1]
    return d


def demo_from_rollout(f, name, task, case):
    from rollout_video import rollout
    rec, _, success, xml, _ = rollout(f, name, case, 1.0, 12, "agentview", 64, render=False)
    d = convert.build_demo(task, rec["object"], rec["eef_pos"], rec["eef_quat"], rec["gq"], rec["cmd"], xml, True)
    d["cmd"] = rec["cmd"]
    return d, success


# ----------------------------------------------------------------------------- diagnosis
def pose_features(rel6):
    rel6 = np.atleast_2d(rel6)
    return np.hstack([rel6[:, :3] / 0.02, R.from_rotvec(rel6[:, 3:]).as_matrix().reshape(-1, 9) / 0.5])


class Distribution:
    """Training poses per (stage, pair, holding-this-object) for an in-distribution check."""

    def __init__(self, Config, domain, train_runs):
        self.Config, self.data = Config, {}
        for di, r in enumerate(train_runs):
            for st, s, e in r["stages"]:
                for t in range(s, e):
                    sv = r["states"][t]
                    for pred in {p for _, p, _ in [c for x in DUR.STAGES[domain] if x["name"] == st for c in x["cond"]]}:
                        a, b = DUR.PRED_PAIR[pred]
                        key = (st, a, b, sv.grabbed_object_1 == b)
                        rel = self._rel(sv, a, b)
                        self.data.setdefault(key, ([], []))
                        self.data[key][0].append(pose_features(rel)[0]); self.data[key][1].append(di)
        self.trees, self.thr = {}, {}
        for k, (X, ids) in self.data.items():
            X, ids = np.array(X), np.array(ids)
            tree = cKDTree(X)
            kk = min(30, len(X))
            dist, idx = tree.query(X, k=kk)
            nn = []
            for i in range(len(X)):
                other = [dd for dd, j in zip(np.atleast_1d(dist[i]), np.atleast_1d(idx[i])) if ids[j] != ids[i]]
                if other:
                    nn.append(other[0])
            self.trees[k] = tree
            self.thr[k] = float(np.percentile(nn, 99)) if nn else np.inf

    def _rel(self, sv, a, b):
        import useful_functions as uf
        return uf.get_relative_pose(link_pose(self.Config, sv, a), link_pose(self.Config, sv, b))

    def check(self, st, sv, a, b):
        key = (st, a, b, sv.grabbed_object_1 == b)
        if key not in self.trees:
            return None, None
        d, _ = self.trees[key].query(pose_features(self._rel(sv, a, b))[0], k=1)
        return float(d), self.thr[key]


def region_mismatch(lab, lamp_names, sv, Config):
    """Which binned dimensions put the pose outside the nearest learned region bin (over the predicate's regions)."""
    best = None
    for n in lamp_names:
        r, g, a, b = lab_grounded(lab, n)
        disc = r.discretizer
        rel = lab.uf.get_relative_pose(link_pose(Config, sv, a), link_pose(Config, sv, b))
        binned = disc.get_discretized_pose(rel, is_relative=True)
        # LAMP only uses the grasp sensor for pairs that involve the gripper (Relation.evaluate_for_map_in_ll_state)
        if "gripper" in (r.parameter1_type, r.parameter2_type) and sv.grabbed_object_1:
            grab = 1 if sv.grabbed_object_1 == b else 2
        else:
            grab = 0
        binned = binned + [grab]
        for rb in r.region:
            diff = [i for i in range(7) if binned[i] != rb[i]]
            score = (len(diff), sum(abs(binned[i] - rb[i]) for i in diff if i < 6))
            if best is None or score < best[0]:
                best = (score, n, binned, list(rb), diff, rel)
    return best


_GROUNDED = {}


def lab_grounded(lab, n):
    return _GROUNDED[n]


def explain(v, run, lab, dist, domain, Config):
    """Turn a violation into a diagnosis dict."""
    pred, pol, t = v["pred"], v["pol"], v["frame"]
    t = min(t, len(run["states"]) - 1)
    sv = run["states"][t]
    a, b = DUR.PRED_PAIR[pred]
    members = DUR.PREDICATES[domain][pred][1]
    _GROUNDED.update(run["grounded"])
    rel = lab.uf.get_relative_pose(link_pose(Config, sv, a), link_pose(Config, sv, b))
    pos_cm = np.round(np.array(rel[:3]) * 100, 1).tolist()
    rpy = np.round(np.degrees(R.from_rotvec(rel[3:]).as_euler("xyz")), 0).tolist()
    stage_of_t = [s for s, s0, s1 in run["stages"] if s0 <= t < s1] or [v["stage"]]
    dd, thr = dist.check(stage_of_t[0], sv, a, b)
    info = dict(v, relation="{}->{}".format(a, b), rel_pos_cm=pos_cm, rel_rpy_deg=rpy,
                knn_dist=dd, knn_thr=thr,
                in_training_distribution=(dd is not None and dd <= thr))
    if pol:   # should have been inside a region, was outside
        bm = region_mismatch(lab, members, sv, Config)
        if bm:
            _, n, binned, rb, diff, _ = bm
            parts = []
            for i in diff:
                if i < 3:
                    parts.append("{} bin {} (region {})".format(POS_DIM[i], binned[i], rb[i]))
                elif i < 6:
                    parts.append("{} bin {} (region {})".format(ANG_DIM[i], binned[i], rb[i]))
                else:
                    parts.append("grasp sensor {} (region {})".format(binned[i], rb[i]))
            dims = set("pos" if i < 3 else ("ang" if i < 6 else "grasp") for i in diff)
            info.update(nearest_region=n, mismatch=parts,
                        cause=("rotation only" if dims == {"ang"} else "position only" if dims == {"pos"}
                               else "grasp flag" if dims == {"grasp"} else "position and rotation" if dims == {"pos", "ang"}
                               else "+".join(sorted(dims))))
    else:     # should have been outside, was inside a region
        info.update(cause="inside region it should not be in")
    return info


# ----------------------------------------------------------------------------- old monitor (for comparison)
def old_monitor_flags(run, lab):
    """The previous all-relations transition monitor (predict.py logic) re-implemented on the same runs."""
    return None  # filled from predict.py results; see report


# ----------------------------------------------------------------------------- main
if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", choices=["square", "tool_hang"], required=True)
    ap.add_argument("--stride", type=int, default=None)
    ap.add_argument("--n_test", type=int, default=20)
    ap.add_argument("--n_train", type=int, default=180)
    a = ap.parse_args()
    domain = convert.TASKS[a.task]["domain"]
    stride = a.stride or (1 if a.task == "square" else 2)
    Config = lamp_env.declare(domain)
    lab = Labeller(Config)
    tag = os.environ.get("DURATIVE_TAG", "")
    out_dir = os.path.join(os.path.dirname(HERE), "out", domain, "durative" + (("_" + tag) if tag else ""))
    os.makedirs(out_dir, exist_ok=True)
    # raw demos and physics rollouts are cached once per task and shared by all variants
    cache = os.path.join(os.path.dirname(HERE), "out", domain, "durative_runs_cache.pkl")
    if not os.path.exists(cache) and os.path.exists(os.path.join(out_dir, "runs_cache.pkl")):
        os.replace(os.path.join(out_dir, "runs_cache.pkl"), cache)
    if not os.path.exists(cache) and os.path.exists(os.path.join(os.path.dirname(out_dir), "durative", "runs_cache.pkl")):
        os.replace(os.path.join(os.path.dirname(out_dir), "durative", "runs_cache.pkl"), cache)
    t0 = time.time()
    path = os.path.join(os.path.expanduser("~/lamp_work/datasets/robomimic"), convert.TASKS[a.task]["file"])
    with h5py.File(path, "r") as f:
        names = lambda m: sorted([x.decode() for x in f["mask"][m][:]], key=lambda s: int(s.split("_")[1]))
        train, valid = names("train")[:a.n_train], names("valid")[:a.n_test]
        if os.path.exists(cache):
            raw = pickle.load(open(cache, "rb"))
        else:
            raw = {"train": {n: demo_from_hdf5(f, n, a.task) for n in train},
                   "nominal": {n: (demo_from_hdf5(f, n, a.task), True) for n in valid}}
            for case in ("drop", "miss"):
                raw[case] = {}
                for n in valid:
                    raw[case][n] = demo_from_rollout(f, n, a.task, case)
                    print("rollout", case, n, "success" if raw[case][n][1] else "failed", flush=True)
            pickle.dump(raw, open(cache, "wb"))
    print("data ready in {:.0f}s".format(time.time() - t0), flush=True)

    train_runs = [make_run(a.task, domain, d, lab, stride) for d in raw["train"].values()]
    print("labelled {} training runs ({:.0f}s)".format(len(train_runs), time.time() - t0), flush=True)
    mism = sum(lab.self_test(r["states"], 60) for r in train_runs[:10])
    print("self-test: our region membership (no widening) vs LAMP's evaluate_in_ll_state: {} mismatches".format(mism),
          flush=True)
    tol, dur = DUR.learn_tolerances(domain, train_runs)
    open(os.path.join(out_dir, "{}_durative.pddl".format(domain.lower())), "w").write(DUR.pddl(domain, tol, dur, 20.0 / stride))
    dist = Distribution(Config, domain, train_runs)

    # reliability of each condition on the TRAINING demos (all succeed)
    train_viol = {}
    for r in train_runs:
        for v in DUR.check(domain, r, tol):
            k = (v["stage"], v["kind"], v["pred"], v["pol"])
            train_viol[k] = train_viol.get(k, 0) + 1

    results = {}
    for case in ("nominal", "drop", "miss"):
        results[case] = []
        for n, (d, success) in raw[case].items():
            run = make_run(a.task, domain, d, lab, stride)
            viol = DUR.check(domain, run, tol)
            diag = [explain(v, run, lab, dist, domain, Config) for v in viol]
            results[case].append(dict(demo=n, success=bool(success), flagged=bool(viol), violations=diag,
                                      stages=[(s, int(x), int(y)) for s, x, y in run["stages"]]))
        print("evaluated", case, "({:.0f}s)".format(time.time() - t0), flush=True)

    def js(o):
        if isinstance(o, (np.floating, np.integer)):
            return o.item()
        if isinstance(o, np.bool_):
            return bool(o)
        return str(o)

    summary = {"tolerances": {"|".join(map(str, k)): v for k, v in tol.items()},
               "durations_frames": dur, "stride": stride,
               "train_violations": {"|".join(map(str, k)): v for k, v in train_viol.items()},
               "results": results}
    json.dump(summary, open(os.path.join(out_dir, "durative_eval.json"), "w"), indent=1, default=js)

    # ------------------------------------------------------------------ console report
    nom = results["nominal"]
    print("\n=== {}: stage-aware durative monitor ===".format(domain))
    print("false alarms on nominal held-out demos: {}/{}".format(sum(r["flagged"] for r in nom), len(nom)))
    for case in ("drop", "miss"):
        real = [r for r in results[case] if not r["success"]]
        print("{}: {} rollouts, {} really failed, detected {}/{}".format(
            case, len(results[case]), len(real), sum(r["flagged"] for r in real), len(real)))
    print("\ncondition violations on TRAINING demos (out of {}):".format(len(train_runs)))
    for k, v in sorted(train_viol.items(), key=lambda x: -x[1]):
        print("   {:>3d}  {}".format(v, k))
