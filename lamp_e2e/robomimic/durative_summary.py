"""Honest detection counts: a real failure counts as DETECTED only if an alarm fires at or after the moment the
failure was injected. Alarms only before that moment are counted as EARLY (false alarms on the still-normal part).
Failure cases: drop, miss, slip, wrong_grasp, wrong_peg (counted only if the task really failed) and stall (always a
failure: the arm freezes; it should be caught by the stage-duration check). Normal cases: nominal (held-out recorded
demos) and mh_* (other operators' demos, robomimic multi-human; any alarm is a false alarm).
usage: durative_summary.py Square tag1 tag2 ...   (writes durative_summary.md next to the variant folders)"""
import json
import os
import sys

import h5py

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from rollout_video import carry_window  # noqa: E402

FAIL_ORDER = ["drop", "miss", "slip", "stall", "wrong_grasp", "wrong_peg"]
domain, tags = sys.argv[1], sys.argv[2:]
task = {"Square": "square", "ToolHang": "tool_hang"}[domain]
base = os.path.join(os.path.dirname(HERE), "out", domain)
f = h5py.File(os.path.expanduser("~/lamp_work/datasets/robomimic/{}/ph/low_dim_v15.hdf5".format(task)), "r")
Js = {t: json.load(open(os.path.join(base, "durative_" + t, "durative_eval.json"))) for t in tags}
fail_cases = [c for c in FAIL_ORDER if any(c in J["results"] for J in Js.values())]
mh_cases = sorted({c for J in Js.values() for c in J["results"] if c.startswith("mh_")})


def event_of(r, case, stride):
    if r.get("event") is not None:
        return r["event"]
    s, e = carry_window(f["data"][r["demo"]]["actions"][:])
    return (s + (e - s) // 2) // stride


hdr = ["Variant", "False alarms (held-out normal)"] + ["{} false alarms".format(c.replace("mh_", "other operators: "))
                                                      for c in mh_cases] + \
      ["{}: caught / early only / missed".format(c) for c in fail_cases]
rows = ["| " + " | ".join(hdr) + " |", "|" + "---|" * len(hdr)]
for tag, J in Js.items():
    R, stride = J["results"], J["stride"]
    cells = ["{}/{}".format(sum(r["flagged"] for r in R["nominal"]), len(R["nominal"]))]
    for c in mh_cases:
        rs = [r for r in R.get(c, []) if r["success"]]
        cells.append("{}/{}".format(sum(r["flagged"] for r in rs), len(rs)) if rs else "-")
    for c in fail_cases:
        if c not in R:
            cells.append("-")
            continue
        det = early = miss = 0
        for r in R[c]:
            if r["success"] and c != "stall":
                continue
            ev = event_of(r, c, stride)
            frames = [v["frame"] for v in r["violations"]]
            if any(fr >= ev - 1 for fr in frames):
                det += 1
            elif frames:
                early += 1
            else:
                miss += 1
        cells.append("{} / {} / {} (of {})".format(det, early, miss, det + early + miss))
    rows.append("| " + " | ".join([tag] + cells) + " |")
md = "\n".join(rows) + "\n"
open(os.path.join(base, "durative_summary.md"), "w").write(md)
print(md)
