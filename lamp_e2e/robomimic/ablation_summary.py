"""Table for the no-hardcoding ablation: one row per (step, cut-off).
A failure counts as CAUGHT only if an alarm fires at or after the moment it was injected (same rule as
durative_summary.py); failure rollouts that still succeeded are left out (except stall, which is always a failure).
False alarms: any alarm on a normal demo (held-out proficient demos, other operators' held-out half).
usage: ablation_summary.py Square|ToolHang [cut-off ...]     (writes out/<Domain>/ablation_summary.md)"""
import json
import os
import sys

domain = sys.argv[1]
qs = sys.argv[2:] or ["98", "95", "90", "80"]
base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "out", domain)
FAIL = ["drop", "miss", "slip", "stall", "wrong_grasp", "wrong_peg"]
steps = sorted(n[len("durative_learned_"):].rsplit("_q", 1)[0] for n in os.listdir(base)
               if n.startswith("durative_learned_A") and n.endswith("_q" + qs[0]))


def caught(R, case):
    det = n = 0
    for r in R.get(case, []):
        if r["success"] and case != "stall":
            continue
        n += 1
        ev = r["event"] if r["event"] is not None else 0
        det += any(v["frame"] >= ev - 1 for v in r["violations"])
    return "{}/{}".format(det, n) if n else "-"


rows = []
hdr = None
for st in steps:
    for q in qs:
        p = os.path.join(base, "durative_learned_{}_q{}".format(st, q), "durative_eval.json")
        if not os.path.exists(p):
            continue
        J = json.load(open(p))
        R = J["results"]
        mh = sorted(c for c in R if c.startswith("mh_"))
        fails = [c for c in FAIL if c in R]
        if hdr is None:
            hdr = ["step", "cut-off", "LAMP regions", "rules", "false alarms (held-out)"] + \
                  ["false alarms: " + c[3:] + " operators" for c in mh] + ["caught: " + c for c in fails]
        nom = R["nominal"]
        cells = [st, q + "%", str(sum("|" not in p for p in J["predicates"])), str(len(J["conditions"])),
                 "{}/{}".format(sum(r["flagged"] for r in nom), len(nom))]
        for c in mh:
            rs = [r for r in R[c] if r["success"]]
            cells.append("{}/{}".format(sum(r["flagged"] for r in rs), len(rs)))
        cells += [caught(R, c) for c in fails]
        rows.append(cells)
out = ["| " + " | ".join(hdr) + " |", "|" + "---|" * len(hdr)] + ["| " + " | ".join(r) + " |" for r in rows]
text = "\n".join(out) + "\n"
open(os.path.join(base, "ablation_summary.md"), "w").write(text)
print(text)
