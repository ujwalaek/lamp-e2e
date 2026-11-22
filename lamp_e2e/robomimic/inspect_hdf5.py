"""Print the structure of a robomimic hdf5 file: demos, lengths, obs keys/shapes, env metadata."""
import json
import sys

import h5py
import numpy as np

path = sys.argv[1]
with h5py.File(path, "r") as f:
    data = f["data"]
    demos = sorted(data.keys(), key=lambda k: int(k.split("_")[1]))
    lens = [data[d]["actions"].shape[0] for d in demos]
    print("file:", path)
    print("#demos:", len(demos), " length min/mean/max:", min(lens), int(np.mean(lens)), max(lens))
    print("mask keys:", list(f["mask"].keys()) if "mask" in f else None)
    env = json.loads(data.attrs["env_args"])
    print("env_name:", env["env_name"])
    print("env_kwargs keys:", sorted(env["env_kwargs"].keys()))
    d0 = data[demos[0]]
    print("demo keys:", list(d0.keys()), " attrs:", list(d0.attrs.keys()))
    for k, v in d0["obs"].items():
        print("  obs/%-28s %s" % (k, v.shape))
    print("actions", d0["actions"].shape, " states", d0["states"].shape)
    print("first object obs:", np.round(d0["obs"]["object"][0], 3).tolist())
    print("actions[:,-1] values:", np.unique(np.round(d0["actions"][:, -1], 2))[:10])
    if "model_file" in d0.attrs:
        xml = d0.attrs["model_file"]
        print("model_file length:", len(xml))
