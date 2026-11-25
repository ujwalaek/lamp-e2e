"""Status of one demo across durative variants: flagged?, first violation, task success."""
import json
import os
import sys

domain, demo, tags = sys.argv[1], sys.argv[2], sys.argv[3:]
base = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "out", domain)
for tag in tags:
    J = json.load(open(os.path.join(base, "durative_" + tag, "durative_eval.json")))
    for case in ("nominal", "drop", "miss"):
        for r in J["results"][case]:
            if r["demo"] == demo:
                v = sorted(r["violations"], key=lambda x: x["frame"])
                first = "{} / {} {}".format(v[0]["stage"], v[0]["kind"], v[0]["pred"]) if v else "-"
                print("{:16s} {:8s} success={!s:5s} flagged={!s:5s} first: {}".format(tag, case, r["success"], r["flagged"], first))
