"""Quick physics check of each injected failure type on a few held-out demos: does the task really fail,
and what happens to the carried object? (no rendering)"""
import os
import sys

os.environ.setdefault("MUJOCO_GL", "egl")
import h5py  # noqa: E402
import numpy as np  # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rollout_video import rollout  # noqa: E402

path, cases, demos = sys.argv[1], sys.argv[2].split(","), sys.argv[3].split(",")
with h5py.File(path, "r") as f:
    for c in cases:
        res = []
        for d in demos:
            rec, _, success, _, _, ev = rollout(f, d, c, 1.0, 12, "agentview", 64, render=False, return_event=True)
            o = rec["object"]
            final = o[-1, 7:10]
            res.append("{}: success={} final first-object pos {} (event step {} of {})".format(
                d, success, np.round(final, 3).tolist(), ev, len(o)))
        print("== {}".format(c))
        for x in res:
            print("   " + x)
