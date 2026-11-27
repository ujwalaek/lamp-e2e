"""Which multi-human (mh) Square demos are identical to proficient-human (ph) demos? (to avoid testing on training data)"""
import hashlib
import sys

import h5py
import numpy as np

ph, mh = sys.argv[1], sys.argv[2]


def key(g):
    o = g["obs/object"][:20]
    return hashlib.md5(np.round(o, 5).tobytes()).hexdigest() + str(g["actions"].shape[0])


with h5py.File(ph, "r") as fp, h5py.File(mh, "r") as fm:
    ph_train = set(x.decode() for x in fp["mask/train"][:])
    pk = {key(fp["data"][n]): n for n in fp["data"]}
    groups = {g: set(x.decode() for x in fm["mask"][g][:]) for g in ("better", "okay", "worse")}
    same, same_train = [], []
    for n in fm["data"]:
        k = key(fm["data"][n])
        if k in pk:
            same.append(n)
            if pk[k] in ph_train:
                same_train.append(n)
    print("mh demos identical to a ph demo: {} (of which in ph TRAIN: {})".format(len(same), len(same_train)))
    for g, s in groups.items():
        print("  {:7s}: {} demos, {} identical to ph, {} new".format(g, len(s), len(s & set(same)), len(s - set(same))))
