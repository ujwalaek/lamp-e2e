"""Print the gripper-closed segments of a demo (start, end, length) and the object each one holds."""
import sys

import h5py
import numpy as np

path, demo = sys.argv[1], sys.argv[2]
with h5py.File(path, "r") as f:
    g = f["data"][demo]
    a, o = g["actions"][:], g["obs/object"][:]
    closed = a[:, -1] > 0
    s = None
    for t, c in enumerate(list(closed) + [False]):
        if c and s is None:
            s = t
        if not c and s is not None:
            nblk = o.shape[1] // 14
            d = [np.linalg.norm(o[s, 14 * k:14 * k + 3]) for k in range(nblk)]
            print("closed [{}, {}) len {}  obj->eef dists at start {}".format(s, t, t - s, np.round(d, 3).tolist()))
            s = None
    print("T", len(a))
