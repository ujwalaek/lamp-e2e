"""Which held-out demos still succeed when their recorded actions are replayed open-loop in physics?
Also reports how far the replayed object trajectory drifts from the recording."""
import os
import sys

os.environ.setdefault("MUJOCO_GL", "egl")
import h5py  # noqa: E402
import numpy as np  # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rollout_video import make_env, restore  # noqa: E402

path = sys.argv[1]
limit = int(sys.argv[2]) if len(sys.argv) > 2 else 20
with h5py.File(path, "r") as f:
    valid = sorted([x.decode() for x in f["mask/valid"][:]], key=lambda s: int(s.split("_")[1]))[:limit]
    env = make_env(f)
    ok = []
    for dname in valid:
        g = f["data"][dname]
        restore(env, g.attrs["model_file"], g["states"][0])
        acts, rec = g["actions"][:], g["obs/object"][:]
        drift = 0.0
        for t, a in enumerate(acts):
            obs, _, _, _ = env.step(a)
            if t + 1 < len(rec):
                o = obs["object-state"]
                drift = max(drift, float(np.max(np.abs(o[7:10] - rec[t + 1][7:10]))))
        s = bool(env._check_success())
        ok.append(s)
        print("{:9s} success {}  max drift of first object {:.1f} cm".format(dname, s, 100 * drift), flush=True)
    print("replay success: {}/{}".format(sum(ok), len(ok)))
