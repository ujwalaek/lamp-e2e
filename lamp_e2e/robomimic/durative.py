"""
Stage-aware durative monitoring on top of LAMP's learned regions.

1. Named predicates are defined as unions of LAMP's learned regions (see PREDICATES below; the
   mapping comes from describe_regions.py: grasp-sensor value + relative-pose range of each region).
2. Each task is a sequence of durative actions (stages). Each stage lists the relations that matter in
   it and PDDL 2.1-style conditions:  at start / over all / at end. Relations not named in a stage are
   ignored during that stage (e.g. gripper->peg while approaching the nut).
3. Stages are segmented from the robot's own commands (gripper close/open) and, inside a carry,
   from the moment the "approach" subgoal first holds (e.g. nut above peg), as an executor would.
4. Tolerances are learned from the training demos (not hand-set):
     over all : the longest run of frames a condition may be false inside the stage
                (95th percentile over training stages) -> 'flicker' tolerance
     at start / at end : the condition must hold somewhere within a window of W frames around the
                stage boundary (W = 95th percentile of the training offsets, capped)
     duration : stage length within [0.5 * min, 1.5 * max] of the training durations
"""
import numpy as np

# ----------------------------------------------------------------------------- predicates
# name -> (description, list of LAMP predicates whose union defines it)
PREDICATES = {
    "Square": {
        "holding":        ("gripper holds the nut",                ["gripper_nut_1", "gripper_nut_2"]),
        "at-grasp-pose":  ("gripper at grasp pose, open",          ["gripper_nut_3"]),
        "nut-above-peg":  ("nut aligned above / sliding down peg", ["nut_peg_1"]),
        "nut-on-peg":     ("nut seated on peg",                    ["nut_peg_2"]),
        "nut-at-peg":     ("nut aligned with peg (above or seated)", ["nut_peg_1", "nut_peg_2"]),
        "ready-to-grasp": ("gripper at grasp pose or already holding", ["gripper_nut_1", "gripper_nut_2", "gripper_nut_3"]),
    },
    "ToolHang": {
        "holding-frame":     ("gripper holds the frame",                ["gripper_frame_1"]),
        "frame-above-stand": ("frame above the stand, before insertion", ["frame_stand_1", "frame_stand_3"]),
        "frame-in-stand":    ("frame inserted in the stand",            ["frame_stand_2"]),
        "at-tool-grasp":     ("gripper at tool grasp pose, open",       ["gripper_tool_1"]),
        "holding-tool":      ("gripper holds the tool",                 ["gripper_tool_2"]),
        "tool-at-hook":      ("tool lined up at hook height",           ["frame_tool_2"]),
        "tool-on-hook":      ("tool hanging on the hook (NOT LEARNED)", []),
    },
}
import os  # noqa: E402

if os.environ.get("LAMP_PEG_SYMMETRY") == "1":
    # re-learned Square model with the peg's 4-fold symmetry folded in: LAMP numbered the two nut-peg
    # regions the other way round (describe_regions.py: nut_peg_1 z +2..+6 cm = seated, nut_peg_2 z -14..-2 cm = above)
    PREDICATES["Square"]["nut-above-peg"] = ("nut aligned above / sliding down peg", ["nut_peg_2"])
    PREDICATES["Square"]["nut-on-peg"] = ("nut seated on peg", ["nut_peg_1"])

PRED_PAIR = {  # which object pair each named predicate is about (for 'relevant relations' per stage)
    "holding": ("gripper_1", "nut_1"), "at-grasp-pose": ("gripper_1", "nut_1"),
    "nut-above-peg": ("nut_1", "peg_1"), "nut-on-peg": ("nut_1", "peg_1"), "nut-at-peg": ("nut_1", "peg_1"),
    "ready-to-grasp": ("gripper_1", "nut_1"),
    "holding-frame": ("gripper_1", "frame_1"), "frame-above-stand": ("frame_1", "stand_1"),
    "frame-in-stand": ("frame_1", "stand_1"), "at-tool-grasp": ("gripper_1", "tool_1"),
    "holding-tool": ("gripper_1", "tool_1"), "tool-at-hook": ("frame_1", "tool_1"),
    "tool-on-hook": ("frame_1", "tool_1"),
}

# ----------------------------------------------------------------------------- durative actions
# condition = (kind, predicate, polarity); kind in {"start", "all", "end"}
STAGES = {
    # Revised after the first evaluation (see durative README): humans release the nut while it is still
    # ~8 cm up the peg and it slides down by itself, so "seated" is required at the END of release-and-retreat,
    # and only "aligned with the peg" (above or seated) at the release itself.
    "Square": [
        dict(name="approach-nut", params="?g - gripper ?n - nut",
             cond=[("all", "holding", False), ("end", "ready-to-grasp", True)]),
        dict(name="move-nut-to-peg", params="?g - gripper ?n - nut ?p - peg",
             cond=[("start", "holding", True), ("all", "holding", True), ("end", "nut-at-peg", True)]),
        dict(name="insert-nut", params="?g - gripper ?n - nut ?p - peg",
             cond=[("start", "nut-at-peg", True), ("all", "holding", True), ("end", "nut-at-peg", True)]),
        dict(name="release-and-retreat", params="?g - gripper ?n - nut ?p - peg",
             cond=[("start", "nut-at-peg", True), ("all", "nut-at-peg", True), ("end", "nut-on-peg", True),
                   ("end", "holding", False)]),
    ],
    "ToolHang": [
        dict(name="approach-frame", params="?g - gripper ?f - frame",
             cond=[("all", "holding-frame", False)]),
        dict(name="move-frame-to-stand", params="?g - gripper ?f - frame ?s - stand",
             cond=[("start", "holding-frame", True), ("all", "holding-frame", True), ("end", "frame-above-stand", True)]),
        dict(name="insert-frame", params="?g - gripper ?f - frame ?s - stand",
             cond=[("start", "frame-above-stand", True), ("all", "holding-frame", True), ("end", "frame-in-stand", True)]),
        dict(name="approach-tool", params="?g - gripper ?t - tool ?f - frame ?s - stand",
             cond=[("all", "frame-in-stand", True), ("end", "at-tool-grasp", True)]),
        dict(name="move-tool-to-hook", params="?g - gripper ?t - tool ?f - frame ?s - stand",
             cond=[("start", "holding-tool", True), ("all", "holding-tool", True), ("all", "frame-in-stand", True),
                   ("end", "tool-at-hook", True)]),
        dict(name="hang-tool-and-retreat", params="?g - gripper ?t - tool ?f - frame ?s - stand",
             cond=[("all", "frame-in-stand", True), ("end", "tool-on-hook", True)]),
    ],
}

# object (as inferred by convert.py's grasp flag) carried in each 'carry' block of a task
CARRIES = {"Square": ["nut_1"], "ToolHang": ["frame_1", "tool_1"]}


def named_truth(domain, lamp_true):
    """lamp_true: dict LAMP-predicate-name -> bool array (T,). Returns named predicate -> bool array."""
    T = len(next(iter(lamp_true.values())))
    out = {}
    for name, (_, members) in PREDICATES[domain].items():
        v = np.zeros(T, dtype=bool)
        for m in members:
            if m in lamp_true:
                v |= lamp_true[m]
        out[name] = v
    return out


def carry_blocks(held, cmd):
    """Carry blocks from the commanded gripper state: [(start, end, object)] for each closed command
    interval that holds an object. Consecutive intervals on the same object (regrasps) are merged."""
    closed = np.asarray(cmd) > 0
    blocks, s = [], None
    for t, c in enumerate(list(closed) + [False]):
        if c and s is None:
            s = t
        if not c and s is not None:
            objs = [h for h in held[s:t] if h]
            if objs:
                o = max(set(objs), key=objs.count)
                if blocks and blocks[-1][2] == o:
                    blocks[-1] = (blocks[-1][0], t, o)
                else:
                    blocks.append((s, t, o))
            s = None
    return blocks


def segment(domain, held, cmd, truth):
    """Split a run into the task's stages: list of (stage_name, start, end) (end exclusive)."""
    T = len(cmd)
    blocks = carry_blocks(held, cmd)
    want = CARRIES[domain]
    # take the first block for each object in task order (missing -> zero-length)
    chosen, cursor = [], 0
    for o in want:
        b = next(((s, e) for s, e, ob in blocks if ob == o and s >= cursor), None)
        if b is None:
            b = (cursor, cursor)
        chosen.append(b)
        cursor = b[1]
    stages = []
    if domain == "Square":
        (s, e), = chosen
        split = _first_true(truth["nut-at-peg"], s, e)
        stages = [("approach-nut", 0, s), ("move-nut-to-peg", s, split), ("insert-nut", split, e),
                  ("release-and-retreat", e, T)]
    else:
        (fs, fe), (ts, te) = chosen
        split = _first_true(truth["frame-above-stand"], fs, fe)
        stages = [("approach-frame", 0, fs), ("move-frame-to-stand", fs, split), ("insert-frame", split, fe),
                  ("approach-tool", fe, ts), ("move-tool-to-hook", ts, te), ("hang-tool-and-retreat", te, T)]
    return stages


def _first_true(v, s, e):
    idx = np.where(v[s:e])[0]
    return s + int(idx[0]) if len(idx) else e


def _longest_false_run(v):
    best = run = 0
    for x in v:
        run = run + 1 if not x else 0
        best = max(best, run)
    return best


def _offset(v, boundary, kind):
    """Frames between a stage boundary and the nearest frame where the condition holds (inf if never)."""
    idx = np.where(v)[0]
    if not len(idx):
        return np.inf
    return float(np.min(np.abs(idx - boundary)))


# ----------------------------------------------------------------------------- learning tolerances
def learn_tolerances(domain, runs, pct=95):
    """runs: list of dicts with 'truth' (named -> bool array) and 'stages'. Returns per (stage, cond) tolerance
    and per-stage duration bounds, all learned from successful training demos."""
    tol, dur = {}, {}
    for st in STAGES[domain]:
        durs = []
        for kind, pred, pol in st["cond"]:
            vals = []
            for r in runs:
                seg = [x for x in r["stages"] if x[0] == st["name"]][0]
                s, e = seg[1], seg[2]
                v = r["truth"][pred] == pol
                if kind == "all":
                    if e > s:
                        vals.append(_longest_false_run(v[s:e]) / max(1, e - s))   # as a fraction of stage length
                elif kind == "start":
                    vals.append(_offset(v, s, kind))
                else:
                    vals.append(_offset(v, max(s, e - 1), kind))
            finite = [x for x in vals if np.isfinite(x)]
            key = (st["name"], kind, pred, pol)
            tol[key] = dict(value=float(np.percentile(finite, pct)) if finite else np.inf,
                            train_never=int(sum(1 for x in vals if not np.isfinite(x))), n=len(vals))
        for r in runs:
            seg = [x for x in r["stages"] if x[0] == st["name"]][0]
            durs.append(seg[2] - seg[1])
        dur[st["name"]] = (0.5 * min(durs), 1.5 * max(durs))
    return tol, dur


# ----------------------------------------------------------------------------- checking
MAX_WINDOW = 20      # frames (1 s at 20 Hz): at start / at end must hold within this distance of the boundary


def check(domain, run, tol):
    """Return list of violations: dicts with stage, kind, predicate, frame, detail."""
    out = []
    for st in STAGES[domain]:
        seg = [x for x in run["stages"] if x[0] == st["name"]][0]
        s, e = seg[1], seg[2]
        for kind, pred, pol in st["cond"]:
            if not PREDICATES[domain][pred][1]:
                continue                                     # predicate never learned: cannot be checked
            v = run["truth"][pred] == pol
            t = tol[(st["name"], kind, pred, pol)]["value"]
            if kind == "all":
                if e <= s:
                    continue
                L = _longest_false_run(v[s:e])
                if L / (e - s) > t and L > 2:
                    first = s + _first_false_run_start(v[s:e], L)
                    out.append(dict(stage=st["name"], kind="over all", pred=pred, pol=pol, frame=int(first),
                                    detail="false for {} of {} frames in a row (tolerance {:.0%} of stage)".format(
                                        L, e - s, t)))
            else:
                b = s if kind == "start" else max(s, e - 1)
                w = min(MAX_WINDOW, t) if np.isfinite(t) else MAX_WINDOW
                off = _offset(v, b, kind)
                if off > w:
                    out.append(dict(stage=st["name"], kind="at " + kind, pred=pred, pol=pol, frame=int(b),
                                    detail="not true within {} frames of the stage {} (nearest: {})".format(
                                        int(w), kind, "never" if not np.isfinite(off) else "{} frames away".format(int(off)))))
    return out


def _first_false_run_start(v, L):
    run = 0
    for i, x in enumerate(v):
        run = run + 1 if not x else 0
        if run == L:
            return i - L + 1
    return 0


# ----------------------------------------------------------------------------- PDDL
def pddl(domain, tol, dur, fps=20.0):
    types = {"Square": "gripper nut peg", "ToolHang": "gripper frame stand tool"}[domain]
    pairs_param = {"gripper_1": "?g", "nut_1": "?n", "peg_1": "?p", "frame_1": "?f", "stand_1": "?s", "tool_1": "?t"}
    typ = {"gripper_1": "gripper", "nut_1": "nut", "peg_1": "peg", "frame_1": "frame", "stand_1": "stand", "tool_1": "tool"}
    lines = [";; Durative model of the robomimic {} task (PDDL 2.1).".format(domain),
             ";; Predicates are LAMP's learned relational regions (union of the listed regions).",
             ";; Durations (seconds) and condition tolerances are learned from 180 training demos.",
             "(define (domain {}-durative)".format(domain.lower()),
             "  (:requirements :typing :durative-actions :negative-preconditions)",
             "  (:types {})".format(types), "  (:predicates"]
    for name, (desc, members) in PREDICATES[domain].items():
        a, b = PRED_PAIR[name]
        lines.append("    ({} {} - {} {} - {})   ; {} := {}".format(
            name, pairs_param[a], typ[a], pairs_param[b], typ[b], desc, " or ".join(members) or "no LAMP region"))
    lines.append("  )")
    for st in STAGES[domain]:
        lo, hi = dur[st["name"]]
        conds = []
        for kind, pred, pol in st["cond"]:
            a, b = PRED_PAIR[pred]
            atom = "({} {} {})".format(pred, pairs_param[a], pairs_param[b])
            atom = atom if pol else "(not {})".format(atom)
            k = {"start": "at start", "all": "over all", "end": "at end"}[kind]
            t = tol[(st["name"], kind, pred, pol)]["value"]
            note = ("flicker tolerance {:.0%} of stage".format(t) if kind == "all"
                    else "within {} frames".format(int(min(MAX_WINDOW, t)) if np.isfinite(t) else MAX_WINDOW))
            if not PREDICATES[domain][pred][1]:
                note = "NOT CHECKABLE: LAMP learned no region for this relation"
            conds.append("      ({} {})   ; {}".format(k, atom, note))
        rel = sorted({"{}-{}".format(typ[PRED_PAIR[p][0]], typ[PRED_PAIR[p][1]]) for _, p, _ in st["cond"]})
        lines += ["", "  ;; relevant relations in this stage: {} (all others ignored)".format(", ".join(rel)),
                  "  (:durative-action {}".format(st["name"]),
                  "    :parameters ({})".format(st["params"]),
                  "    :duration (and (>= ?duration {:.1f}) (<= ?duration {:.1f}))".format(lo / fps, hi / fps),
                  "    :condition (and", *conds, "    )",
                  "    :effect (and {})".format(" ".join(
                      "(at end {})".format("({} {} {})".format(p, pairs_param[PRED_PAIR[p][0]], pairs_param[PRED_PAIR[p][1]])
                                           if pol else "(not ({} {} {}))".format(p, pairs_param[PRED_PAIR[p][0]],
                                                                                  pairs_param[PRED_PAIR[p][1]]))
                      for k, p, pol in st["cond"] if k == "end")), "  )"]
    lines.append(")")
    return "\n".join(lines) + "\n"
