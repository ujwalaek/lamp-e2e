"""Describe each learned LAMP region in physical terms: grasp-sensor value, relative position range (cm)
and rotation range, and how often it is true in each task stage of the training demos."""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import lamp_env  # noqa: E402

domain = sys.argv[1]
Config = lamp_env.declare(domain)
from src.data_structures.WorldModel import WorldModel  # noqa: E402

prefix = open(Config.DATA_MISC_DIR + "latest_prefix.txt").read().strip()
WorldModel.set_params(prefix)
model = WorldModel.load_model(0)
for key, d in model.relations.items():
    for cr, rel in sorted(d.items()):
        if cr == 0:
            continue
        reg = np.array(rel.region)
        disc = rel.discretizer
        bins = disc.get_bins(True)
        lo = [min(bins[i]["bin_start"][j] for j in reg[:, i]) for i in range(3)]
        hi = [max(bins[i]["bin_end"][j] for j in reg[:, i]) for i in range(3)]
        lo, hi = np.array(lo), np.array(hi)
        if True:   # y bins run downwards in LAMP's Discretizer
            lo[1], hi[1] = min(lo[1], hi[1]), max(lo[1], hi[1])
        ang = [sorted(set(int(v) for v in reg[:, i])) for i in (3, 4, 5)]
        print("{}_{}: {} bins | sensor {} | pos x [{:+.1f},{:+.1f}] y [{:+.1f},{:+.1f}] z [{:+.1f},{:+.1f}] cm | "
              "angle-bin sets r{} p{} y{}".format(key, cr, len(reg), sorted(set(int(v) for v in reg[:, 6])),
                                                  100 * lo[0], 100 * hi[0], 100 * lo[1], 100 * hi[1], 100 * lo[2], 100 * hi[2],
                                                  ang[0], ang[1], ang[2]))
