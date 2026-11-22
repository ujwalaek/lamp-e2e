"""
Step 2: demos -> pairwise relative poses (LAMP's augment_data.py / DataAugmenter).

For every state and every ordered object pair (prim, sec) that passes LAMP's filter:
    rel = inv(T_prim) @ T_sec           (useful_functions.get_relative_pose; "sec in prim's frame")
    rel6d = [x, y, z, rotvec]            (6D: translation + axis-angle)
then each dimension is binned with the pair-specific Discretizer (domain_configs/PackingConfig.py
DISCRETIZER_PARAMS). Robot links come first (prim = gripper). Output (LAMP format):
    Data/Packing/misc/<env>/binned_<env>_data.pkl   {"binned_env_states": [[BinnedEnvState, ...], ...]}

Also written, for inspection or for your own models:
    Data/Packing/misc/<env>/<env>_relposes.npz   continuous 6D relative poses + grasp flag
"""
import argparse
import os

import numpy as np

import lamp_env

DOMAIN = lamp_env.domain_from_argv()
Config = lamp_env.declare(DOMAIN)
import src.utilities.DataAugmentation as DA  # noqa: E402
import useful_functions as uf  # noqa: E402

DA.time.sleep = lambda *_: None   # DataAugmenter sleeps 0.1 s per trajectory, plus 5 s at the end


def dump_continuous(env, trajs):
    """Same pair rules as DataAugmenter, but keep the continuous 6D relative pose."""
    def pose(state, name):
        p = state.object_dict[name]
        return p[1] if name.split("_")[0] in Config.ROBOT_TYPES else p

    out = {}
    names = sorted(n for n in trajs[0][0].object_dict if n.split("_")[0] not in Config.NON_RELATION_OBJECTS)
    names.sort(key=lambda n: n.split("_")[0] not in Config.ROBOT_TYPES)     # robot links first, as LAMP does
    pairs = [(p, q) for i, p in enumerate(names) for q in names[i + 1:]]
    for prim, sec in pairs:
        rows = []
        for ti, traj in enumerate(trajs):
            for si, s in enumerate(traj):
                rel = uf.get_relative_pose(pose(s, prim), pose(s, sec))
                rows.append([ti, si] + list(rel) + [float(bool(s.grabbed_flag_1))])
        out["{}__{}".format(prim, sec)] = np.array(rows)
    path = os.path.join(Config.DATA_MISC_DIR, env, env + "_relposes.npz")
    np.savez(path, columns=np.array(["traj", "step", "x", "y", "z", "rx", "ry", "rz", "grabbed"]), **out)
    return path


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-n", "--name", nargs="*", default=["env1", "env2", "env9"])
    ap.add_argument("--domain", default="Packing")
    a = ap.parse_args()
    for env in a.name:
        da = DA.DataAugmenter(env)
        da.augment_data(da.data)
        print("  continuous rel poses ->", dump_continuous(env, da.data))
        s = da.binned_data[0][-1].binned_pose_dict
        print("  example binned rel pose (last state of demo 0):", s)
