"""For held-out demos: is the final state inside LAMP's learned regions? (reads predict.py's CSV)"""
import csv
import sys

import h5py

path, col, hdf5 = sys.argv[1], sys.argv[2], sys.argv[3]
rows = list(csv.DictReader(open(path)))
last = {}
for r in rows:
    d, s = int(r["demo"]), int(r["step"])
    if d not in last or s > int(last[d]["step"]):
        last[d] = r
f = h5py.File(hdf5, "r")
valid = sorted([x.decode() for x in f["mask/valid"][:]], key=lambda s: int(s.split("_")[1]))
ok = [valid[d] for d in sorted(last) if last[d].get(col) == "1"]
print("{}: final state inside in {}/{} held-out demos".format(col, len(ok), len(last)))
print("demos where it is inside:", ok)
