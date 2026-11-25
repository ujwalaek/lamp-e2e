"""One line per flagged run: its violations (stage, condition, cause, pose, in training distribution?)."""
import json
import os
import sys

domain, tag, case = sys.argv[1], sys.argv[2], (sys.argv[3] if len(sys.argv) > 3 else "nominal")
d = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "out", domain,
                 "durative" + (("_" + tag) if tag else ""))
J = json.load(open(os.path.join(d, "durative_eval.json")))
for r in J["results"][case]:
    if not r["violations"]:
        continue
    print("{} ({} violations)".format(r["demo"], len(r["violations"])))
    for v in sorted(r["violations"], key=lambda x: x["frame"]):
        print("   f{:<4} {:20s} {:9s} {:15s} {:28s} pos {} rpy {} typical={} | {}".format(
            v["frame"], v["stage"], v["kind"], v["pred"] + ("" if v["pol"] else "(neg)"), v.get("cause", ""),
            v["rel_pos_cm"], v["rel_rpy_deg"], v.get("in_training_distribution"), "; ".join(v.get("mismatch", []))))
