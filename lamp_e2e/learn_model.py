"""
Step 4: RCRs -> predicates (relations) + abstract demos + lifted action model
(LAMP's gen_world_model.py / WorldModel.generate_model).

  * get_lifted_relations_dict: one Relation per RCR, named <type1>_<type2>_<k> (k >= 1). Each has
      region : the set of 7-D bin indices (6-D pose bins + grasp sensor). Membership in this set is
               the classifier LAMP actually uses when labelling states (Relation.evaluate_in_ll_state).
      mvg    : sklearn BayesianGaussianMixture fit to samples drawn uniformly inside the region's bins.
               It is the paper's generative "RCR predictor", used to sample poses when refining plans.
    plus <type1>_<type2>_0, the negation ("in none of the RCRs").
  * TrajAbstracter: each low-level state -> PDDLState (set of true grounded relations). Consecutive
    duplicates are collapsed, giving one abstract trajectory per demo.
  * TransitionClusters: abstract transitions grouped by identical lifted <add, delete> effects, so
    each cluster is one lifted action. Preconditions come from the intersection of pre-states.
Outputs:
  Data/Packing/misc/<prefix>Packing_model_0.pkl   (LAMP WorldModel pickle)
  Domains/Packing/domain.pddl                     (learned PDDL domain)
  lamp_e2e/out/abstract_demos.txt                 (human-readable predicate sequences)
"""
import os
import sys
import time

from _lamp_path import setup
setup()

from Config import Config  # noqa: E402
Config.declare_config("Packing", "MagneticGripper")
import py3_patches  # noqa: E402
py3_patches.apply()
from src.data_structures.WorldModel import WorldModel  # noqa: E402
from src.data_structures.TransitionGraph import TransitionGraph  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    prefix = open(Config.DATA_MISC_DIR + "latest_prefix.txt").read().strip()
    t0 = time.time()
    WorldModel.set_params(prefix, force_generation=True)
    model = WorldModel.get_model()            # builds relations, graph, clusters and actions
    pddl = model.get_domain_pddl()
    WorldModel.save_model(model, 0)
    model.save_domain_file("domain.pddl", pddl)
    print("model learned in {:.1f}s".format(time.time() - t0))

    print("\n=== invented predicates ===")
    for key, d in model.relations.items():
        for cr, rel in sorted(d.items()):
            g = "-" if rel.mvg is None else "GMM({} comps)".format(rel.mvg.gaussian.n_components)
            print("  {:22s} region bins={:4d}  {}".format("{}_{}".format(key, cr), len(rel.region), g))
    print("\n#abstract transitions:", len(TransitionGraph.transitions_used),
          " #lifted actions:", len(model.actions))

    # human-readable abstract demos
    trajs = TransitionGraph.get_abstract_trajectories()
    with open(os.path.join(OUT, "abstract_demos.txt"), "w") as f:
        for i, t in enumerate(trajs):
            f.write("--- abstract demo {} ({} abstract states)\n".format(i, len(t.traj)))
            for s in t.traj:
                f.write("   " + " ".join(sorted(str(r) for r in s.true_set)) + "\n")
    print("unique abstract demos:", len(trajs), "->", os.path.join(OUT, "abstract_demos.txt"))
    print("PDDL ->", Config.PDDL_DIR + "domain.pddl")
    if "-v" in sys.argv:
        print(pddl)
