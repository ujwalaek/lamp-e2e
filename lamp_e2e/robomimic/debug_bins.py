"""Debug: where do nut->peg relative poses fall in LAMP's bins, and how many demos visit each bin?"""
import collections
import os
import pickle
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import lamp_env  # noqa: E402

domain, prim, sec = sys.argv[1], sys.argv[2], sys.argv[3]
Config = lamp_env.declare(domain)
import useful_functions as uf  # noqa: E402

binned = pickle.load(open(Config.DATA_MISC_DIR + "env1/binned_env1_data.pkl", "rb"))["binned_env_states"]
raw = uf.load_traj("env1")["env_states"]
pos_count, last_bins = collections.Counter(), collections.Counter()
for traj in binned:
    seen = set()
    for s in traj:
        b = s.binned_pose_dict.get(prim, {}).get(sec)
        if b is not None and -1 not in b:
            seen.add(tuple(b[:3]))
    pos_count.update(seen)
    b = traj[-1].binned_pose_dict[prim][sec]
    last_bins[tuple(b)] += 1
n = len(binned)
print("demos:", n)
print("position bins visited by most demos (fraction):")
for k, v in pos_count.most_common(8):
    print("  ", k, round(v / n, 3))
print("final-state full bins (most common):")
for k, v in last_bins.most_common(8):
    print("  ", k, v)
disc = Config.get_discretizer(prim.split("_")[0], sec.split("_")[0])
rb = disc.get_bins(True)
for i in range(3):
    print("axis", i, "relative bin edges first/last:", round(rb[i]["bin_start"][0], 4), round(rb[i]["bin_end"][-1], 4),
          "n", len(rb[i]["bin_start"]))
# continuous values at the final step, to compare
rel = np.array([uf.get_relative_pose(t[-1].object_dict[prim] if not prim.startswith("gripper") else t[-1].object_dict[prim][1],
                                     t[-1].object_dict[sec]) for t in raw])
print("final continuous rel pose mean", np.round(rel.mean(0), 3).tolist(), "std", np.round(rel.std(0), 3).tolist())
print("example final binned:", binned[0][-1].binned_pose_dict[prim][sec], " continuous:", np.round(rel[0], 3).tolist())
for i in range(3):
    print("axis", i, "bin of value", round(rel[0][i], 4), "->", disc.get_bin_from_ll(rel[0][i], i, True))
