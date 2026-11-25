"""Honest detection counts: a real failure counts as DETECTED only if an alarm fires at or after the moment the
failure was injected (gripper opened / arm pushed). Alarms before that moment are counted as EARLY alarms
(false alarms on the still-normal part of the run).
usage: durative_summary.py Square pegsym_dilate0 pegsym_dilate1 ...   (writes durative_summary.md next to them)"""
import json
import os
import sys

import h5py

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from rollout_video import carry_window  # noqa: E402

domain, tags = sys.argv[1], sys.argv[2:]
task = {"Square": "square", "ToolHang": "tool_hang"}[domain]
base = os.path.join(os.path.dirname(HERE), "out", domain)
f = h5py.File(os.path.expanduser("~/lamp_work/datasets/robomimic/{}/ph/low_dim_v15.hdf5".format(task)), "r")
rows = ["| Variant | False alarms on 20 normal runs | Drops: detected after the drop / early alarm only / missed "
        "| Misses: detected after the push / early alarm only / missed |", "|---|---|---|---|"]
for tag in tags:
    J = json.load(open(os.path.join(base, "durative_" + tag, "durative_eval.json")))
    stride = J["stride"]
    R = J["results"]
    fa = sum(r["flagged"] for r in R["nominal"])
    cells = []
    for case in ("drop", "miss"):
        det = early = miss = 0
        for r in R[case]:
            if r["success"]:
                continue
            s, e = carry_window(f["data"][r["demo"]]["actions"][:])
            event = (s + (e - s) // 2) // stride
            frames = [v["frame"] for v in r["violations"]]
            if any(fr >= event - 1 for fr in frames):
                det += 1
            elif frames:
                early += 1
            else:
                miss += 1
        cells.append("{} / {} / {} (of {})".format(det, early, miss, det + early + miss))
    rows.append("| {} | {} | {} | {} |".format(tag, fa, *cells))
md = "\n".join(rows) + "\n"
open(os.path.join(base, "durative_summary.md"), "w").write(md)
print(md)
