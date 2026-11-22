"""
Step 3: relative poses -> Relational Critical Regions (LAMP's gen_rom.py / RelativeOccupancyMap).

For each object-type pair (e.g. gripper_can, can_surface):
  1. Build a frequency map over binned relative poses, with layout [x, y, z, angle-slot, grasp-sensor].
     A bin counts at most once per trajectory.
  2. Divide by the number of trajectories and binarize with the pair's EVAL_THRESHOLDING_VALUES
     (the paper's criticality threshold theta: gripper-can 1.0, can-surface 0.032).
  3. Run scipy.ndimage.label (connected components) on the position occupancy. Each component,
     together with its frequent orientation bins, is one RCR, i.e. one invented relation.
Output: Data/Packing/misc/<N>_<prefix>_rcr_indices.pkl   (lists of 7-D bin indices per RCR)
"""
import argparse

import numpy as np

import lamp_env

DOMAIN = lamp_env.domain_from_argv()
Config = lamp_env.declare(DOMAIN)
from src.utilities.RelativeOccupancyMapping import RelativeOccupancyMap  # noqa: E402

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-n", "--name", nargs="*", default=["env1", "env2"])
    ap.add_argument("--domain", default="Packing")
    ap.add_argument("--traj_per_env", type=float, default=1.0, help="fraction of demos sampled per env")
    ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args()
    np.random.seed(a.seed)

    rom = RelativeOccupancyMap(a.name, traj_per_env=a.traj_per_env, total_traj_count=0,
                               overwrite=True, load_all=True, prefix=0)
    rom.start()
    print("file prefix:", rom.file_prefix)
    print("thresholds:", {"_".join(sorted(k)): v for k, v in Config.EVAL_THRESHOLDING_VALUES.items()})
    for p, d in rom.rcr_indices_dic.items():
        for s, regions in d.items():
            print("  {}_{}: {} RCR(s)".format(p, s, len(regions)))
            for i, r in enumerate(regions, 1):
                arr = np.array(r)
                print("    RCR {}: {} bins | grasp-sensor values {} | xyz bins {}..{}".format(
                    i, len(r), sorted(set(arr[:, 6].tolist())), arr[:, :3].min(0).tolist(), arr[:, :3].max(0).tolist()))
    with open(Config.DATA_MISC_DIR + "latest_prefix.txt", "w") as f:
        f.write(rom.file_prefix)
    import json
    with open(Config.DATA_MISC_DIR + "rcr_summary.json", "w") as f:
        json.dump({"{}_{}".format(p, s): [len(r) for r in regions]
                   for p, d in rom.rcr_indices_dic.items() for s, regions in d.items()}, f)
