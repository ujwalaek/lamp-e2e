"""Compare LAMP's learned predicates with ground truth on held-out robomimic demos.

Ground truth (per kept time step, saved by convert.py):
  Square:   nut_on_peg (robosuite's own on_peg rule), holding (the inferred grasp flag)
  ToolHang: frame_is_assembled, tool_on_frame (flags robosuite records), holding
For every ground-truth event, every learned predicate column (bin-membership labels from predict.py) is
scored, and the best match is reported with accuracy / precision / recall.
"""
import argparse
import csv
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import lamp_env  # noqa: E402


def load_csv(path):
    with open(path) as f:
        return list(csv.DictReader(f))


def scores(pred, gt):
    tp = int(np.sum(pred & gt)); fp = int(np.sum(pred & ~gt)); fn = int(np.sum(~pred & gt))
    acc = float(np.mean(pred == gt))
    prec = tp / (tp + fp) if tp + fp else float("nan")
    rec = tp / (tp + fn) if tp + fn else float("nan")
    return acc, prec, rec


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--domain", required=True)
    ap.add_argument("--envs", nargs="*", default=["env9"])
    a = ap.parse_args()
    Config = lamp_env.declare(a.domain)
    out = lamp_env.out_dir(a.domain)

    gt_all, rows_all = {}, []
    for env in a.envs:
        rows = load_csv(os.path.join(out, "predictions_{}.csv".format(env)))
        gtz = np.load(os.path.join(Config.DATA_MISC_DIR, env, env + "_gt.npz"))
        keys = sorted(set(k.split("__", 1)[1] for k in gtz.files))
        by_demo = {}
        for r in rows:
            by_demo.setdefault(int(r["demo"]), []).append(r)
        for d, rs in by_demo.items():
            rs.sort(key=lambda r: int(r["step"]))
            for k in keys:
                gt_all.setdefault(k, []).extend(gtz["%d__%s" % (d, k)][[int(r["step"]) for r in rs]].tolist())
            gt_all.setdefault("holding", []).extend([int(r["grabbed"]) for r in rs])
            rows_all.extend(rs)

    cols = [c for c in rows_all[0] if c.endswith("[bins]")]
    print("held-out states:", len(rows_all), " learned predicates:", [c[:-6] for c in cols])
    best = {}
    for k, g in gt_all.items():
        g = np.array(g, dtype=bool)
        print("\nground truth '{}': true in {:.0%} of states".format(k, g.mean()))
        res = []
        for c in cols:
            p = np.array([int(r[c]) for r in rows_all], dtype=bool)
            res.append((scores(p, g), c[:-6]))
        # rank by F1 (accuracy alone rewards an always-false predicate when the event is rare)
        f1 = lambda p, r: 0.0 if not (p == p and r == r) or p + r == 0 else 2 * p * r / (p + r)
        res.sort(key=lambda x: (-f1(x[0][1], x[0][2]), -x[0][0]))
        for (acc, prec, rec), name in res[:3]:
            print("   {:22s} accuracy {:5.1%}  precision {:5.1%}  recall {:5.1%}".format(name, acc, prec, rec))
        if res:
            (acc, prec, rec), name = res[0]
            best[k] = {"predicate": name, "accuracy": acc, "precision": prec, "recall": rec,
                       "f1": f1(prec, rec), "gt_rate": float(g.mean())}
        else:
            best[k] = {"predicate": None, "gt_rate": float(g.mean())}
    import json
    with open(os.path.join(out, "gt_eval.json"), "w") as f:
        json.dump(best, f, indent=1)
