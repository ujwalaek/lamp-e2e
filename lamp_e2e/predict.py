"""
Step 5: predict predicates on new (held-out) demos with the learned model, and monitor execution.

For every low-level state x of each test demo (env9: nominal / drop / miss):
  (a) LAMP abstraction alpha(x): PDDLState.get_from_ll. A relation R_k(o1, o2) is true iff the binned
      relative pose (either direction) plus the grasp-sensor value lies in RCR k (bin-set membership,
      exactly as Relation.evaluate_in_ll_state does).
  (b) GMM version (the paper's psi_gamma(p) = [likelihood(p) > eps]): the RCR's BayesianGaussianMixture
      log-likelihood of the continuous 6-D relative pose, thresholded at eps, AND a sensor match.
      eps is calibrated as the 1st percentile of scores on training states where (a) is true.
Then consecutive abstract states are compared with the learned model: a transition whose lifted
<add, delete> effect matches no learned action cluster is flagged UNEXPLAINED. That is the
execution-monitoring signal.

Outputs: lamp_e2e/out/predictions_env9.csv (per-state predicates, both methods) + console report.
"""
import argparse
import csv
import os
import warnings

import numpy as np

from _lamp_path import setup
setup()

from Config import Config  # noqa: E402
Config.declare_config("Packing", "MagneticGripper")
import py3_patches  # noqa: E402
py3_patches.apply()
import useful_functions as uf  # noqa: E402
from src.data_structures.WorldModel import WorldModel  # noqa: E402
from src.data_structures.PDDLState import PDDLState  # noqa: E402
from src.utilities.TransitionClusters import TransitionClusters  # noqa: E402

warnings.filterwarnings("ignore")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")


def link_pose(state, name):
    p = state.object_dict[name]
    return p[1] if name.split("_")[0] in Config.ROBOT_TYPES else p


def grasp_sensor(state, rel, o1, o2):
    """Same grab-flag logic as Relation.evaluate_in_ll_state (0 = free, 1 = holding this, 2 = holding other)."""
    if Config.GRIPPER_NAME not in (rel.parameter1_type, rel.parameter2_type) or not state.grabbed_flag_1:
        return 0
    obj = o2 if rel.parameter1_type == Config.GRIPPER_NAME else o1
    return 1 if state.grabbed_object_1 == obj else 2


def gmm_score(state, rel, o1, o2):
    """Max log-likelihood over both relative-pose directions (LAMP checks both)."""
    p1, p2 = link_pose(state, o1), link_pose(state, o2)
    rels = [uf.get_relative_pose(p2, p1), uf.get_relative_pose(p1, p2)]
    return max(float(rel.mvg.gaussian.score([r])) for r in rels)


def region_sensors(rel):
    return set(int(r[-1]) for r in rel.region)


def lifted_relations(model):
    out = []
    for key, d in model.relations.items():
        for cr, rel in d.items():
            if cr != 0:
                out.append(rel)
    return out


def ground(rel, objects):
    o1 = [o for o in objects if o.split("_")[0] == rel.parameter1_type]
    o2 = [o for o in objects if o.split("_")[0] == rel.parameter2_type]
    return [(a, b) for a in o1 for b in o2 if a != b]


def calibrate_eps(model, envs, pct=1.0):
    eps = {}
    for rel in lifted_relations(model):
        scores = []
        for env in envs:
            for traj in uf.load_traj(env)["env_states"]:
                for s in traj:
                    for o1, o2 in ground(rel, s.object_dict.keys()):
                        g = rel.get_grounded_relation(uf.Link(o1, rel.parameter1_type), uf.Link(o2, rel.parameter2_type),
                                                      list(s.object_dict.keys()))
                        if g.evaluate_in_ll_state(s):
                            scores.append(gmm_score(s, rel, o1, o2))
        name = "{}_{}_{}".format(rel.parameter1_type, rel.parameter2_type, rel.cr)
        eps[name] = float(np.percentile(scores, pct)) if scores else np.inf
    return eps


def abstract(state, model, obj_dict, aux):
    return PDDLState.get_from_ll(model.relations, obj_dict, state, aux)


def lifted_sig(state):
    """Lifted view of a PDDLState: true relations with objects replaced by their types
    (enough for this one-object-per-type demo; LAMP's own lifting uses parameter maps)."""
    return set("({}_{}_{} {} {})".format(r.parameter1_type, r.parameter2_type, r.cr,
                                         r.parameter1_type, r.parameter2_type) for r in state.true_set)


def transition_key(s1, s2):
    tc = TransitionClusters.generate_transition_clusters.__func__ if hasattr(
        TransitionClusters.generate_transition_clusters, "__func__") else TransitionClusters.generate_transition_clusters
    return list(tc([(s1, s2)]).keys())[0]


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--test_env", default="env9")
    ap.add_argument("--train_envs", nargs="*", default=["env1", "env2"])
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)

    prefix = open(Config.DATA_MISC_DIR + "latest_prefix.txt").read().strip()
    WorldModel.set_params(prefix)
    model = WorldModel.load_model(0)
    known = {str(k): i for i, k in enumerate(model.og_clusters.keys())}
    action_of, pre_of = {}, {}
    for act, (k, cluster) in zip(model.actions, model.og_clusters.items()):
        action_of[str(k)] = "a{}".format(getattr(act, "action_id", "?"))
        # Paper, Alg. 3: pre(a) = intersection of the (lifted) pre-states of all transitions in the cluster.
        pre_of[str(k)] = set.intersection(*[lifted_sig(t[0]) for t in cluster])

    print("calibrating GMM thresholds eps on training states ...")
    eps = calibrate_eps(model, a.train_envs)
    for k, v in eps.items():
        print("  eps[{}] = {:.2f}".format(k, v))

    trajs = uf.load_traj(a.test_env)["env_states"]
    lab_file = os.path.join(Config.DATA_MISC_DIR, a.test_env, a.test_env + "_labels.txt")
    labels = open(lab_file).read().split() if os.path.exists(lab_file) else ["?"] * len(trajs)
    rels = lifted_relations(model)
    rel_names = ["{}_{}_{}".format(r.parameter1_type, r.parameter2_type, r.cr) for r in rels]

    rows, summary = [], []
    agree = total = 0
    print("\n=== predictions on {} ===".format(a.test_env))
    for ti, (traj, lab) in enumerate(zip(trajs, labels)):
        objs = list(traj[0].object_dict.keys())
        obj_dict = uf.get_object_dictionary(objs)
        aux = uf.get_auxilary_preds(obj_dict, model.relations)
        seq, flags = [], []
        prev = None
        for si, s in enumerate(traj):
            st = abstract(s, model, obj_dict, aux)
            true_names = set(str(r) for r in st.true_set)
            row = {"demo": ti, "label": lab, "step": si, "grabbed": int(bool(s.grabbed_flag_1))}
            for rel, name in zip(rels, rel_names):
                for o1, o2 in ground(rel, objs):
                    pred = "({} {} {})".format(name, o1, o2)
                    lamp_true = pred in true_names
                    sc = gmm_score(s, rel, o1, o2)
                    gmm_true = sc >= eps[name] and grasp_sensor(s, rel, o1, o2) in region_sensors(rel)
                    row[name + "[bins]"] = int(lamp_true)
                    row[name + "[gmm]"] = int(gmm_true)
                    row[name + "[loglik]"] = round(sc, 2)
                    agree += int(lamp_true == gmm_true); total += 1
            rows.append(row)
            if prev is None or st != prev:
                if prev is not None:
                    k = str(transition_key(prev, st))
                    if k not in known:
                        flags.append("UNEXPLAINED: effect matches no learned action")
                    elif not pre_of[k].issubset(lifted_sig(prev)):
                        missing = sorted(pre_of[k] - lifted_sig(prev))
                        flags.append("UNEXPLAINED: effect of {} but precondition violated, missing {}".format(
                            action_of[k], " ".join(missing)))
                    else:
                        flags.append(action_of[k])
                seq.append(" ".join(sorted(r for r in true_names)))
                prev = st
        verdict = "ANOMALY" if any(f.startswith("UNEXPLAINED") for f in flags) else "OK"
        summary.append((ti, lab, verdict))
        print("\n--- test demo {} [{}] -> {}".format(ti, lab, verdict))
        for i, s in enumerate(seq):
            print("   s{}: {}".format(i, s))
            if i < len(flags):
                print("        --[{}]-->".format(flags[i]))

    path = os.path.join(OUT, "predictions_{}.csv".format(a.test_env))
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    print("\n=== execution-monitoring summary ===")
    for ti, lab, v in summary:
        print("  demo {} [{:7s}] -> {}".format(ti, lab, v))
    print("\nbin-membership vs GMM agreement: {:.1%} over {} predicate evaluations".format(agree / total, total))
    print("per-state predictions ->", path)
