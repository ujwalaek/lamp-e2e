"""Collect a theta sweep into one markdown table (sweep/summary.md)."""
import glob
import json
import os
import sys

root = sys.argv[1]
rows = []
for d in sorted(glob.glob(os.path.join(root, "theta_*")), key=lambda p: -float(p.split("_")[-1])):
    t = d.split("_")[-1]
    ld = lambda n: json.load(open(os.path.join(d, n))) if os.path.exists(os.path.join(d, n)) else {}
    rcr, gt, m9, m8 = ld("rcr_summary.json"), ld("gt_eval.json"), ld("monitor_env9.json"), ld("monitor_env8.json")
    log = os.path.join(d, "learn_model.log")
    acts = ""
    if os.path.exists(log):
        for line in open(log):
            if "lifted actions" in line:
                acts = line.split("lifted actions:")[-1].strip()
    rcr_s = ", ".join("{} {}".format(k, len(v)) for k, v in sorted(rcr.items()))
    gt_s = "; ".join("{}: {} F1 {:.2f}".format(k, v.get("predicate"), v.get("f1", 0) or 0) for k, v in sorted(gt.items()))
    f = lambda m, k, key: "{:.0%}".format(m[k][key]) if k in m else "-"
    mon = "nominal {} / drop {} / miss {}".format(f(m9, "nominal", "flag_transition_goal"),
                                                   f(m8, "drop", "flag_transition_goal"), f(m8, "miss", "flag_transition_goal"))
    mon1 = "nominal {} / drop {} / miss {}".format(f(m9, "nominal", "flag_transition"),
                                                    f(m8, "drop", "flag_transition"), f(m8, "miss", "flag_transition"))
    rows.append((t, rcr_s, acts, gt_s, mon1, mon))
hdr = "| theta | RCRs per pair | actions | best predicate vs ground truth | flagged (transition check) | flagged (transition + goal) |\n|---|---|---|---|---|---|\n"
md = hdr + "".join("| " + " | ".join(r) + " |\n" for r in rows)
open(os.path.join(root, "summary.md"), "w").write(md)
print(md)
