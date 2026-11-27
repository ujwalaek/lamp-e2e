"""Is the raw peg pose constant (same in every frame and demo)? Needed to undo peg-symmetry folding in cached runs."""
import os
import pickle

import numpy as np

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "out", "Square")
old = pickle.load(open(os.path.join(out, "durative_runs_cache.pkl"), "rb"))      # built before peg folding existed
P = np.vstack([d["poses"]["peg_1"] for d in old["train"].values()])
print("old cache peg: rows", len(P), "min", P.min(0).round(4), "max", P.max(0).round(4))
new = pickle.load(open(os.path.join(out, "durative_runs_cache_motion.pkl"), "rb"))
Q = np.vstack([d["poses"]["peg_1"] for d in new["train"].values()])
print("motion cache peg: min", Q.min(0).round(4), "max", Q.max(0).round(4))
