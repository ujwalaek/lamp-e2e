"""
Fully LEARNED durative monitor: nothing about the task is written by hand.

What the hand-built monitor (durative.py) gets from me, and what this one uses instead:
  hand-written stages (approach / carry / insert / release)   -> stages cut at the robot's own grasp events:
                                                                 free_0, carry_1, free_1, ..., carry_n, free_n
  which object is carried in which order                       -> the most common carry sequence in training demos
  named predicates ('holding', 'nut-on-peg', ...) built from   -> every LAMP region is used as-is, by its LAMP name
  hand-chosen LAMP regions                                        (e.g. gripper_nut_2), nobody interprets it
  hand-chosen conditions per stage                             -> every (region, true/false, at start / over all /
                                                                 at end) combination is a candidate; it is KEPT only
                                                                 if it held in >= Q of the training demos (default
                                                                 98%). Irrelevant relations drop out by themselves.
  tolerances, stage durations                                  -> learned from training demos (as before)
Pose fixes are switches, off unless asked for: LAMP_PEG_SYMMETRY=1 (fold the square peg's 4 sides),
LAMP_TOOL_CANON=1 (fixed tool frame for Tool Hang). The cached runs had these fixes baked in; they are undone first
(peg: the raw peg frame never rotates, see check_peg.py; tool: the canonical rotation is a fixed right-multiplication).
LAMP_MH_TRAIN=1 (Square): train on proficient + half of each other-operator group, test on the other half.

usage: eval_learned.py --task square|tool_hang --tag NAME [--cases "drop miss ..."] [--mh]
"""
import argparse
import collections
import json
import os
import pickle
import sys
import time

os.environ.setdefault("MUJOCO_GL", "egl")
import h5py  # noqa: E402
import numpy as np  # noqa: E402
from scipy.spatial.transform import Rotation as R  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE)); sys.path.insert(0, HERE)
import lamp_env  # noqa: E402
import convert  # noqa: E402
import durative as DUR  # noqa: E402
import eval_durative as ED  # noqa: E402

W, FLICK = DUR.MAX_WINDOW, DUR.MAX_FLICKER
Q = float(os.environ.get("LAMP_COND_Q", "0.98"))
KINDS = ("start", "all", "end")


# ----------------------------------------------------------------------------- data
def raw_poses(task, poses):
    """Undo the pose fixes baked into the cached runs, then re-apply only the ones switched on."""
    p = dict(poses)
    if "peg_1" in p:
        peg = p["peg_1"].copy()
        peg[:, 3:] = 0.0                       # raw peg frame: fixed, zero rotation in every demo
        p["peg_1"] = peg
    if task == "tool_hang" and "tool_1" in p:  # Tool Hang cache was built with LAMP_TOOL_CANON=1
        t = p["tool_1"].copy()
        t[:, 3:] = (R.from_rotvec(t[:, 3:]) * R.from_quat(convert.TOOL_CANON_Q).inv()).as_rotvec()
        p["tool_1"] = t
    if os.environ.get("LAMP_PEG_SYMMETRY") == "1":
        p = convert.canonicalize_peg(p)
    if os.environ.get("LAMP_TOOL_CANON") == "1":
        p = convert.canonicalize_tool(p)
    return p


def make_run(task, d, lab, stride):
    from src.data_structures.EnvState import EnvState
    steps = list(range(0, d["T"], stride))
    poses = raw_poses(task, d["poses"])
    sub = dict(T=len(steps), poses={k: v[steps] for k, v in poses.items()},
               held=[d["held"][t] for t in steps], flags=d["flags"])
    states, _ = convert.to_envstates(sub, 1, EnvState)
    lamp, grounded = lab.label(states)
    lamp.update(region_unions(lamp))
    return dict(states=states, lamp=lamp, held=sub["held"], cmd=np.asarray(d["cmd"])[steps], grounded=grounded)


def region_unions(lamp):
    """Generic candidate predicates: for each object pair, 'in any of these regions' for every set of >= 2 of the
    pair's LAMP regions (e.g. nut_peg_1|nut_peg_2). Which ones are useful is left to the data."""
    import itertools
    by_pair = collections.defaultdict(list)
    for n in lamp:
        by_pair[n.rsplit("_", 1)[0]].append(n)
    out = {}
    for pair, ns in by_pair.items():
        ns = sorted(ns)
        for k in range(2, len(ns) + 1):
            for sub in itertools.combinations(ns, k):
                out["|".join(sub)] = np.any([lamp[n] for n in sub], axis=0)
    return out


def prune(conds):
    """Drop redundant conditions on the same pair, stage, kind and polarity: for 'must be in', keep the most specific
    region sets (drop a set if a subset of it is also required); for 'must not be in', keep the widest."""
    sets = lambda c: frozenset(c["pred"].split("|"))
    pair = lambda c: c["pred"].split("|")[0].rsplit("_", 1)[0]
    keep = []
    for c in conds:
        same = [x for x in conds if x is not c and x["stage"] == c["stage"] and x["kind"] == c["kind"]
                and x["pol"] == c["pol"] and pair(x) == pair(c)]
        if c["pol"] and any(sets(x) < sets(c) for x in same):
            continue
        if not c["pol"] and any(sets(x) > sets(c) for x in same):
            continue
        keep.append(c)
    return keep


# ----------------------------------------------------------------------------- stages from grasp events
def carry_seq(run):
    return tuple(o for _, _, o in DUR.carry_blocks(run["held"], run["cmd"]))


def learn_skeleton(runs):
    return collections.Counter(carry_seq(r) for r in runs).most_common(1)[0][0]


def stages_of(run, skel):
    T = len(run["cmd"])
    blocks = DUR.carry_blocks(run["held"], run["cmd"])
    st, cur, prev = [], 0, 0
    for i, o in enumerate(skel):
        b = next(((s, e) for s, e, ob in blocks if ob == o and s >= cur), None) or (cur, cur)
        st.append(("free{}".format(i), prev, b[0]))
        st.append(("carry{}-{}".format(i + 1, o.split("_")[0]), b[0], b[1]))
        cur = prev = b[1]
    st.append(("free{}".format(len(skel)), prev, T))
    return st


# ----------------------------------------------------------------------------- conditions
def measure(v, s, e, kind):
    """How far the condition is from holding: frames to the boundary (start/end) or longest-off fraction (all)."""
    if kind == "all":
        if e - s < 3:
            return None
        L = DUR._longest_false_run(v[s:e])
        return 0.0 if L <= 2 else L / (e - s)
    if kind == "start":
        return DUR._offset(v, s, kind)
    return DUR._offset(v, max(s, e - 1), kind)


CAP = {"start": W, "end": W, "all": FLICK}
NEAR_MISS = []     # 'must be in' conditions that held in 60%..Q of training demos: why they were NOT learned


def learn_conditions(runs, preds, Q=Q):
    del NEAR_MISS[:]
    names = [s for s, _, _ in runs[0]["stages"]]
    conds = []
    for si, st in enumerate(names):
        for p in preds:
            for pol in (True, False):
                found = {}
                for kind in KINDS:
                    if not pol and kind != "all":
                        continue        # 'not in X somewhere near the boundary' is nearly always true: no information
                    ms = []
                    for r in runs:
                        _, s, e = r["stages"][si]
                        m = measure(r["lamp"][p] == pol, s, e, kind)
                        if m is not None:
                            ms.append(m)
                    if len(ms) < 0.5 * len(runs):
                        continue
                    ok = [m for m in ms if m <= CAP[kind]]
                    if len(ok) >= Q * len(ms):
                        found[kind] = dict(tol=float(max(ok)), held_in=len(ok), n=len(ms))
                    elif pol and len(ok) >= 0.6 * len(ms):
                        NEAR_MISS.append(dict(stage=st, pred=p, kind=kind, held_in=len(ok), n=len(ms)))
                if "all" in found:          # 'over all' already implies the boundary versions
                    found = {"all": found["all"]}
                for kind, info in found.items():
                    conds.append(dict(stage=st, si=si, pred=p, pol=pol, kind=kind, **info))
    return prune(conds)


def learn_durations(runs):
    names = [s for s, _, _ in runs[0]["stages"]]
    return {st: 1.5 * max(r["stages"][i][2] - r["stages"][i][1] for r in runs) for i, st in enumerate(names)}


def check(run, conds, dur):
    out = []
    if os.environ.get("LAMP_DURATION_CHECK") == "1":
        for name, s, e in run["stages"]:
            if e - s > dur[name]:
                out.append(dict(stage=name, kind="duration", pred="stage-duration", pol=True, frame=int(s + dur[name]),
                                detail="stage lasted {} frames, normal demos at most {:.0f}".format(e - s, dur[name])))
    for c in conds:
        _, s, e = run["stages"][c["si"]]
        v = run["lamp"][c["pred"]] == c["pol"]
        m = measure(v, s, e, c["kind"])
        if m is None or m <= c["tol"]:
            continue
        if c["kind"] == "all":
            L = DUR._longest_false_run(v[s:e])
            fr = s + DUR._first_false_run_start(v[s:e], L)
            det = "off for {} of {} frames in a row".format(L, e - s)
        else:
            fr = s if c["kind"] == "start" else max(s, e - 1)
            det = "not {} within {} frames of the stage {}".format("true" if c["pol"] else "false", int(c["tol"]), c["kind"])
        out.append(dict(stage=c["stage"], kind="over all" if c["kind"] == "all" else "at " + c["kind"],
                        pred=c["pred"], pol=c["pol"], frame=int(fr), detail=det))
    return out


def cause(v, run, lab, Config):
    """Which pose dimensions put the relation outside its LAMP region (for 'should be true' violations)."""
    if v["kind"] == "duration":
        return "stage too long"
    if not v["pol"]:
        return "entered a region it never enters in this stage"
    ED._GROUNDED.update(run["grounded"])
    sv = run["states"][min(v["frame"], len(run["states"]) - 1)]
    bm = ED.region_mismatch(lab, v["pred"].split("|"), sv, Config)
    if not bm:
        return "?"
    dims = set("pos" if i < 3 else ("ang" if i < 6 else "grasp") for i in bm[4])
    return {frozenset(["ang"]): "rotation only", frozenset(["pos"]): "position only",
            frozenset(["grasp"]): "grasp flag", frozenset(["pos", "ang"]): "position and rotation"}.get(
        frozenset(dims), "+".join(sorted(dims)))


def pddl(domain, model_preds, skel, conds, dur, fps, Q=Q):
    lines = [";; LEARNED durative model of robomimic {} (nothing task-specific written by hand).".format(domain),
             ";; Predicates = LAMP's learned regions; stages = robot grasp events; conditions kept if they held in",
             ";; >= {:.0%} of training demos; durations learned.".format(Q),
             "(define (domain {}-learned)".format(domain.lower()), "  (:requirements :durative-actions :negative-preconditions)",
             "  (:predicates " + " ".join("({})".format(p) for p in model_preds) + ")"]
    for st in dur:
        cs = [c for c in conds if c["stage"] == st]
        lines += ["  (:durative-action {}".format(st),
                  "    :duration (<= ?duration {:.1f})".format(dur[st] / fps), "    :condition (and"]
        for c in cs:
            atom = "({})".format(c["pred"]) if c["pol"] else "(not ({}))".format(c["pred"])
            lines.append("      ({} {})   ; held in {}/{} training demos".format(
                {"start": "at start", "all": "over all", "end": "at end"}[c["kind"]], atom, c["held_in"], c["n"]))
        lines += ["    ))"]
    lines.append(")")
    return "\n".join(lines) + "\n"


# ----------------------------------------------------------------------------- main
if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", choices=["square", "tool_hang"], required=True)
    ap.add_argument("--tag", required=True)
    ap.add_argument("--cases", default="drop miss slip stall wrong_grasp wrong_peg")
    ap.add_argument("--mh", action="store_true")
    ap.add_argument("--quick", type=int, default=0, help="smoke test: use only this many demos per set")
    a = ap.parse_args()
    domain = convert.TASKS[a.task]["domain"]
    stride = 1 if a.task == "square" else 2
    Config = lamp_env.declare(domain)
    lab = ED.Labeller(Config)
    t0 = time.time()
    base = os.path.join(os.path.dirname(HERE), "out", domain)
    raw = pickle.load(open(os.path.join(base, "durative_runs_cache_motion{}.pkl".format(
        "_canon" if a.task == "tool_hang" else "")), "rb"))
    fail_cases = [c for c in a.cases.split() if c in raw]
    cases = ["nominal"] + fail_cases
    train_demos = list(raw["train"].values())
    if a.mh:
        mh_raw = pickle.load(open(os.path.join(base, "durative_mh_cache.pkl"), "rb"))
        ph_path = os.path.join(os.path.expanduser("~/lamp_work/datasets/robomimic"), convert.TASKS[a.task]["file"])
        split = convert.mh_split(ph_path)
        for grp, (mtr, mte) in split.items():
            g = mh_raw["mh_" + grp]
            if os.environ.get("LAMP_MH_TRAIN") == "1":
                train_demos += [g[n][0] for n in mtr if n in g]
            raw["mh_" + grp] = {n: g[n] for n in mte if n in g}      # always test on the same held-out half
            cases.append("mh_" + grp)
    if a.quick:
        train_demos = train_demos[:a.quick]
        raw = {c: dict(list(raw[c].items())[:a.quick]) if c in cases else raw[c] for c in raw}
    print("training demos:", len(train_demos), "| test cases:", {c: len(raw[c]) for c in cases}, flush=True)
    train_runs = [make_run(a.task, d, lab, stride) for d in train_demos]
    preds = sorted(train_runs[0]["lamp"])
    skel = learn_skeleton(train_runs)
    n_skel = sum(carry_seq(r) == skel for r in train_runs)
    for r in train_runs:
        r["stages"] = stages_of(r, skel)
    dur = learn_durations(train_runs)
    print("LAMP regions used as predicates:", preds, flush=True)
    print("learned carry sequence:", skel, "({}/{} training demos follow it exactly)".format(n_skel, len(train_runs)),
          flush=True)
    print("labelled training runs ({:.0f}s)".format(time.time() - t0), flush=True)

    test = {}
    for case in cases:
        test[case] = []
        for n, (d, success) in raw[case].items():
            run = make_run(a.task, d, lab, stride)
            run["stages"] = stages_of(run, skel)
            test[case].append((n, d, success, run))
    print("labelled test runs ({:.0f}s)".format(time.time() - t0), flush=True)

    # one model per cut-off Q (the share of normal training demos a condition must hold in); labelling is shared
    qs = [float(x) for x in os.environ.get("LAMP_COND_QS", str(Q)).split()]
    for q in qs:
        tag = a.tag if len(qs) == 1 else "{}_q{:02d}".format(a.tag, int(round(q * 100)))
        out_dir = os.path.join(os.path.dirname(HERE), "out", domain, "durative_" + tag)
        os.makedirs(out_dir, exist_ok=True)
        conds = learn_conditions(train_runs, preds, q)
        near = list(NEAR_MISS)
        print("== cut-off {:.0%}: learned {} conditions over {} stages".format(q, len(conds), len(dur)), flush=True)
        for c in conds:
            print("   {:<14} {:<9} {}{}  ({}/{})".format(c["stage"], c["kind"], "" if c["pol"] else "not ", c["pred"],
                                                       c["held_in"], c["n"]), flush=True)
        print("   near misses (held in most but not enough training demos, so NOT used):", flush=True)
        for c in sorted(near, key=lambda c: -c["held_in"] / c["n"])[:8]:
            print("     {:<14} at {:<6} {}  ({}/{})".format(c["stage"], c["kind"], c["pred"], c["held_in"], c["n"]),
                  flush=True)
        open(os.path.join(out_dir, "{}_learned.pddl".format(domain.lower())), "w").write(
            pddl(domain, preds, skel, conds, dur, 20.0 / stride, q))
        train_flag = sum(bool(check(r, conds, dur)) for r in train_runs)
        results = {}
        for case in cases:
            results[case] = []
            for n, d, success, run in test[case]:
                viol = check(run, conds, dur)
                for v in viol:
                    v["cause"] = cause(v, run, lab, Config)
                results[case].append(dict(demo=n, success=bool(success), flagged=bool(viol), violations=viol,
                                          stages=[(s, int(x), int(y)) for s, x, y in run["stages"]],
                                          event=(int(d["event"]) // stride) if "event" in d else None))
            print("   {}: flagged {}/{}".format(case, sum(r["flagged"] for r in results[case]), len(results[case])),
                  flush=True)
        summary = dict(mode="learned", cutoff=q, stride=stride, skeleton=skel, carry_seq_share=[n_skel, len(train_runs)],
                       predicates=preds, conditions=conds, near_misses=near, durations_frames=dur,
                       train_flagged=[train_flag, len(train_runs)],
                       switches={k: os.environ.get(k) for k in ("LAMP_PEG_SYMMETRY", "LAMP_TOOL_CANON", "LAMP_MH_TRAIN",
                                                                "LAMP_THETA_GRIP", "LAMP_THETA_OBJ",
                                                                "LAMP_THETA_FRAME_TOOL", "LAMP_GRIP_BINS",
                                                                "LAMP_ANG_BINS")},
                       results=results)
        json.dump(summary, open(os.path.join(out_dir, "durative_eval.json"), "w"), indent=1,
                  default=lambda o: o.item() if isinstance(o, (np.generic,)) else str(o))
        print("saved", out_dir, flush=True)
