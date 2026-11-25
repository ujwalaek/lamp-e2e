"""Turn out/<Domain>/durative/durative_eval.json into a readable markdown report (durative_report.md)."""
import collections
import json
import os
import sys

domain = sys.argv[1]
tag = sys.argv[2] if len(sys.argv) > 2 else ""
d = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "out", domain,
                 "durative" + (("_" + tag) if tag else ""))
J = json.load(open(os.path.join(d, "durative_eval.json")))
R = J["results"]
L = ["# {}: stage-aware durative monitor\n".format(domain)]

nom = R["nominal"]
rows = [("nominal (recorded, all succeed)", len(nom), "-", sum(r["flagged"] for r in nom), "false alarms")]
for case in ("drop", "miss"):
    real = [r for r in R[case] if not r["success"]]
    rows.append(("{} (physics rollout)".format(case), len(R[case]), len(real), sum(r["flagged"] for r in real), "detected"))
L.append("| Test case | Runs | Really failed | Flagged | Meaning |\n|---|---|---|---|---|")
for c, n, f, k, m in rows:
    L.append("| {} | {} | {} | {} | {} |".format(c, n, f, k, m))

# ---- false alarms
L.append("\n## False alarms (nominal runs flagged)\n")
causes = collections.Counter()
for r in nom:
    for v in r["violations"]:
        causes[(v["stage"], v["kind"], v["pred"], v.get("cause", "?"), bool(v.get("in_training_distribution")))] += 1
if causes:
    L.append("| Stage | Condition | Predicate | Why outside | Pose typical of training? | Count |\n|---|---|---|---|---|---|")
    for (st, kind, pred, cause, ind), n in causes.most_common():
        L.append("| {} | {} | {} | {} | {} | {} |".format(st, kind, pred, cause, "yes" if ind else "no", n))
L.append("\n### Every false alarm\n")
for r in nom:
    for v in r["violations"]:
        L.append("- **{}**, stage `{}`, {} `{}`{}: {}. Relative pose ({}) pos {} cm, rpy {} deg. {}. "
                 "Nearest training pose distance {} (99th pct {}).".format(
                     r["demo"], v["stage"], v["kind"], v["pred"], "" if v["pol"] else " (should be false)", v["detail"],
                     v["relation"], v["rel_pos_cm"], v["rel_rpy_deg"],
                     ("Outside learned bins: " + "; ".join(v["mismatch"])) if v.get("mismatch") else v.get("cause", ""),
                     "n/a" if v["knn_dist"] is None else "{:.2f}".format(v["knn_dist"]),
                     "n/a" if v["knn_thr"] is None else "{:.2f}".format(v["knn_thr"])))

# ---- detections and misses
for case in ("drop", "miss"):
    L.append("\n## {}: detections and misses\n".format(case.capitalize()))
    real = [r for r in R[case] if not r["success"]]
    benign = [r for r in R[case] if r["success"]]
    if benign:
        L.append("{} {} rollouts still succeeded physically, so they are not failures and are excluded: {}.\n".format(
            len(benign), case, ", ".join(r["demo"] for r in benign)))
    first = collections.Counter()
    for r in real:
        if r["violations"]:
            v = sorted(r["violations"], key=lambda x: x["frame"])[0]
            first[(v["stage"], v["kind"], v["pred"])] += 1
    if first:
        L.append("First condition violated in each detected run:\n")
        L.append("| Stage | Condition | Predicate | Runs |\n|---|---|---|---|")
        for (st, kind, pred), n in first.most_common():
            L.append("| {} | {} | {} | {} |".format(st, kind, pred, n))
    missed = [r for r in real if not r["flagged"]]
    L.append("\nMissed ({}): {}".format(len(missed), ", ".join(r["demo"] for r in missed) or "none"))
    for r in missed:
        L.append("- **{}**: stages {}".format(r["demo"], r["stages"]))

# ---- training reliability
L.append("\n## Condition violations on the 180 training demos (all succeed)\n")
L.append("These show how reliable each learned condition is on normal runs.\n")
L.append("| Condition | Violations |\n|---|---|")
for k, v in sorted(J["train_violations"].items(), key=lambda x: -x[1]):
    L.append("| {} | {} |".format(k.replace("|", " / "), v))
open(os.path.join(d, "durative_report.md"), "w").write("\n".join(L) + "\n")
print("\n".join(L[:40]))
