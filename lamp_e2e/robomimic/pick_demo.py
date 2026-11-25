"""List held-out demos whose nominal run has no alarm and whose drop and miss rollouts are detected at or
after the injected failure (for choosing a representative video demo by rule)."""
import json
import os
import sys

import h5py

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from rollout_video import carry_window  # noqa: E402

domain, tag = sys.argv[1], sys.argv[2]
task = {"Square": "square", "ToolHang": "tool_hang"}[domain]
J = json.load(open(os.path.join(os.path.dirname(HERE), "out", domain, "durative_" + tag, "durative_eval.json")))
f = h5py.File(os.path.expanduser("~/lamp_work/datasets/robomimic/{}/ph/low_dim_v15.hdf5".format(task)), "r")
by = {c: {r["demo"]: r for r in J["results"][c]} for c in ("nominal", "drop", "miss")}
good = []
for n, r in by["nominal"].items():
    if r["flagged"]:
        continue
    s, e = carry_window(f["data"][n]["actions"][:])
    ev = (s + (e - s) // 2) // J["stride"]
    ok = True
    for c in ("drop", "miss"):
        x = by[c][n]
        if x["success"] or not x["violations"] or min(v["frame"] for v in x["violations"]) < ev - 1:
            ok = False
    if ok:
        good.append(n)
print("demos clean on nominal and caught after the failure in both drop and miss:", good)
