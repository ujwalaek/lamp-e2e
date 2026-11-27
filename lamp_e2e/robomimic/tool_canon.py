"""Tool Hang: measure the average orientation of the hung tool relative to the frame (final state of the training
demos) and check how a canonical tool frame (tool orientation right-multiplied by the inverse of that average)
removes the 180-degree rotation-vector flip. Prints the quaternion to use in convert.TOOL_CANON_Q."""
import os
import sys

import h5py
import numpy as np
from scipy.spatial.transform import Rotation as R

path = os.path.expanduser("~/lamp_work/datasets/robomimic/tool_hang/ph/low_dim_v15.hdf5")
with h5py.File(path, "r") as f:
    train = [x.decode() for x in f["mask/train"][:]]
    rels = []
    for n in train:
        o = f["data"][n]["obs/object"][-1]
        Rf, Rt = R.from_quat(o[24:28]), R.from_quat(o[38:42])     # frame quat [21:28] -> 24:28; tool [35:42] -> 38:42
        rels.append(Rf.inv() * Rt)
    rels = R.concatenate(rels)
    mean = rels.mean()
    rv = rels.as_rotvec()
    canon = (rels * mean.inv()).as_rotvec()
    print("hung tool relative to frame, rotation-vector std (rad) as is:   ", np.round(rv.std(0), 3).tolist(),
          " |angle| mean (deg)", round(float(np.degrees(np.linalg.norm(rv, axis=1)).mean()), 1))
    print("with canonical tool frame (inverse mean applied):           ", np.round(canon.std(0), 3).tolist(),
          " |angle| mean (deg)", round(float(np.degrees(np.linalg.norm(canon, axis=1)).mean()), 1))
    print("TOOL_CANON_Q (xyzw) =", np.round(mean.inv().as_quat(), 6).tolist())
