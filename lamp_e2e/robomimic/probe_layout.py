"""Work out the layout of obs/object empirically: which 7-blocks are world poses (static before grasp)
and which are object-relative-to-eef; also check quaternion convention against eef pose."""
import sys

import h5py
import numpy as np
from scipy.spatial.transform import Rotation as R

path = sys.argv[1]
with h5py.File(path, "r") as f:
    d = f["data/demo_0"]
    obj = d["obs/object"][:]
    eef = d["obs/robot0_eef_pos"][:]
    eq = d["obs/robot0_eef_quat"][:]
    g = d["obs/robot0_gripper_qpos"][:]
    a = d["actions"][:, -1]
    T = obj.shape[0]
    print("T", T, "object dims", obj.shape[1])
    first_close = int(np.argmax(a > 0))
    print("first gripper-close step:", first_close)
    print("std over steps [0, first_close) per dim (small => static world pose):")
    print(np.round(obj[:max(first_close, 2)].std(0), 4).tolist())
    print("step0 eef_pos", np.round(eef[0], 3).tolist(), "eef_quat", np.round(eq[0], 3).tolist())
    for s in range(0, obj.shape[1] - 6, 7):
        blk = obj[0, s:s + 7]
        print("block@%2d pos %s quat %s |q|=%.3f" % (s, np.round(blk[:3], 3).tolist(), np.round(blk[3:], 3).tolist(),
                                                np.linalg.norm(blk[3:])))
    # check: is block A's pos == R(eef)^T (world_pos - eef) for some other block?
    rem = obj.shape[1] % 7
    if rem:
        print("leftover dims:", rem, np.round(obj[0, -rem:], 3).tolist())
    print("gripper qpos step0 / at close+5:", np.round(g[0], 4).tolist(), np.round(g[min(first_close + 5, T - 1)], 4).tolist())
