"""Find fixed bodies (pegs) in the per-demo MuJoCo XML and print their world poses; check grasp distances."""
import sys
import xml.etree.ElementTree as ET

import h5py
import numpy as np

path = sys.argv[1]
with h5py.File(path, "r") as f:
    for demo in ["demo_0", "demo_1", "demo_50"]:
        root = ET.fromstring(f["data"][demo].attrs["model_file"])
        hits = []
        for b in root.iter("body"):
            n = b.get("name", "")
            if "peg" in n.lower() or "stand" in n.lower() or "base" == n.lower():
                hits.append((n, b.get("pos"), b.get("quat")))
        print(demo, hits[:6])
    # grasp statistics: distance object->eef at the step the gripper closes
    d = f["data/demo_0"]
    obj, a, g = d["obs/object"][:], d["actions"][:, -1], d["obs/robot0_gripper_qpos"][:]
    nblk = obj.shape[1] // 14
    closes = np.where(np.diff((a > 0).astype(int)) == 1)[0] + 1
    opens = np.where(np.diff((a > 0).astype(int)) == -1)[0] + 1
    print("close steps", closes.tolist(), "open steps", opens.tolist(), "T", len(a))
    for s in list(closes) + list(opens):
        dists = [np.linalg.norm(obj[s, 14 * k:14 * k + 3]) for k in range(nblk)]
        print("  step", s, "obj->eef dists", np.round(dists, 3).tolist(), "finger gap", round(float(g[s, 0] - g[s, 1]), 4))
