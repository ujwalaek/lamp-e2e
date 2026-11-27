"""Which condition fires FIRST in each flagged normal run (held-out and other operators).
usage: alarm_causes.py <Domain> <tag>"""
import collections
import json
import os
import sys

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "out", sys.argv[1])
J = json.load(open(os.path.join(out, "durative_" + sys.argv[2], "durative_eval.json")))
for case, rs in J["results"].items():
    if case != "nominal" and not case.startswith("mh_"):
        continue
    c = collections.Counter()
    for r in rs:
        if not r["success"] or not r["violations"]:
            continue
        v = min(r["violations"], key=lambda v: v["frame"])
        c[(v["stage"], v["kind"], v["pred"], v.get("cause", ""))] += 1
    print("==", case, sum(c.values()), "flagged")
    for k, n in c.most_common(8):
        print("  {:>3d}  {}".format(n, k))
