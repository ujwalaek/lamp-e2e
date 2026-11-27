"""Print which test cases a durative result JSON and the run cache contain.  usage: check_cases.py <Domain> <tag>"""
import json
import os
import pickle
import sys

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "out", sys.argv[1])
J = json.load(open(os.path.join(out, "durative_" + sys.argv[2], "durative_eval.json")))
print("results:", {k: len(v) for k, v in J["results"].items()})
for name in sorted(os.listdir(out)):
    if name.endswith(".pkl") and "runs_cache" in name:
        print(name, list(pickle.load(open(os.path.join(out, name), "rb"))))
