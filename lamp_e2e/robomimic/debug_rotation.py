"""Check orientation fragmentation for gripper->object while holding: rotation-vector magnitude near pi
(where the axis-angle representation flips sign) and how many distinct LAMP angle bins one grasp uses."""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import lamp_env  # noqa: E402

domain, pair = sys.argv[1], sys.argv[2]          # e.g. Square gripper_1__nut_1
Config = lamp_env.declare(domain)
z = np.load(Config.DATA_MISC_DIR + "env1/env1_relposes.npz")
a = z[pair]                                      # columns: traj, step, x, y, z, rx, ry, rz, grabbed
held = a[a[:, 8] > 0.5]
rv = held[:, 5:8]
mag = np.linalg.norm(rv, axis=1)
print("holding states:", len(held))
print("rotation angle |rotvec| (deg): mean %.1f, min %.1f, max %.1f" % tuple(np.degrees([mag.mean(), mag.min(), mag.max()])))
print("share of holding states with angle > 170 deg (sign-flip zone): %.0f%%" % (100 * np.mean(mag > np.radians(170))))
sign_flips = 0
for t in np.unique(held[:, 0]):
    r = rv[held[:, 0] == t]
    if len(r) > 1:
        sign_flips += int(np.any(np.sum(r[1:] * r[:-1], axis=1) < 0))
print("demos where the rotvec flips direction between consecutive holding states: %d / %d" % (sign_flips, len(np.unique(held[:, 0]))))
disc = Config.get_discretizer(*[p.split("_")[0] for p in pair.split("__")])
bins = np.array([[disc.get_bin_from_ll(v, i + 3, True) for i, v in enumerate(r)] for r in rv])
print("distinct (rx,ry,rz) angle-bin triples used while holding: %d" % len({tuple(b) for b in bins}))
pos = held[:, 2:5]
print("position while holding: std (cm)", np.round(100 * pos.std(0), 1).tolist())
