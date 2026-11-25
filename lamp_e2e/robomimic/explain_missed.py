"""For real failures the monitor did not flag: show, at each stage boundary of the run, which checked
conditions held and the relative pose behind them, so it is clear why the failure looked normal."""
import json
import os
import pickle
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE)); sys.path.insert(0, HERE)
import lamp_env  # noqa: E402
import convert  # noqa: E402
import durative as DUR  # noqa: E402

task, tag, case = sys.argv[1], sys.argv[2], sys.argv[3]
domain = convert.TASKS[task]["domain"]
Config = lamp_env.declare(domain)
import eval_durative as ED  # noqa: E402
import useful_functions as uf  # noqa: E402
base = os.path.join(os.path.dirname(HERE), "out", domain)
J = json.load(open(os.path.join(base, "durative_" + tag, "durative_eval.json")))
missed = [r["demo"] for r in J["results"][case] if not r["success"] and not r["flagged"]]
print("missed {} runs: {}".format(case, missed))
raw = pickle.load(open(os.path.join(base, "durative_runs_cache.pkl"), "rb"))
lab = ED.Labeller(Config)
stride = J["stride"]
for n in missed:
    d, _ = raw[case][n]
    run = ED.make_run(task, domain, d, lab, stride)
    print("\n== {}  stages: {}".format(n, [(s, a, b) for s, a, b in run["stages"]]))
    for st in DUR.STAGES[domain]:
        name, s, e = [x for x in run["stages"] if x[0] == st["name"]][0]
        for kind, pred, pol in st["cond"]:
            if not DUR.PREDICATES[domain][pred][1]:
                print("   {:24s} {:8s} {:16s} NOT CHECKABLE".format(name, kind, pred))
                continue
            t = s if kind == "start" else max(s, e - 1)
            v = run["truth"][pred] == pol
            if kind == "all":
                status = "true in {}/{} frames".format(int(v[s:e].sum()), e - s)
            else:
                status = "{} at frame {}".format("TRUE" if v[min(t, len(v) - 1)] else "false", t)
            a, b = DUR.PRED_PAIR[pred]
            sv = run["states"][min(t, len(run["states"]) - 1)]
            rel = uf.get_relative_pose(ED.link_pose(Config, sv, a), ED.link_pose(Config, sv, b))
            print("   {:24s} {:8s} {:16s} {:28s} {}->{} pos {} cm".format(
                name, kind, ("" if pol else "not ") + pred, status, a, b, np.round(np.array(rel[:3]) * 100, 1).tolist()))
