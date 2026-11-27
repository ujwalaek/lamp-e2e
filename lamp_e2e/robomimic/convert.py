"""
robomimic hdf5 -> LAMP demonstrations (EnvState pickles in LAMP's on-disk format).

What is taken from robomimic (low_dim_v15.hdf5, proficient-human demos, 20 Hz):
  gripper_1 pose  <- obs/robot0_eef_pos + obs/robot0_eef_quat (xyzw)
  object poses    <- obs/object: per object [pose-in-eef (7), world pose (7)]; ToolHang adds 2 flags
                     Square:   nut = [7:14];  peg = fixed body 'peg1' from the demo's MuJoCo XML
                     ToolHang: stand = [7:14], frame = [21:28], tool = [35:42],
                               flags [42] frame_is_assembled, [43] tool_on_frame (ground truth)
  grasp flag      <- robomimic has none, so it is inferred: gripper commanded closed (actions[:,-1] > 0)
                     AND the nearest graspable object is within GRASP_DIST of the end effector AND the
                     fingers are not fully shut. The held object stays the same until the gripper opens.
Poses are converted to LAMP's 6-D [x, y, z, rotation vector].

Time steps are subsampled (--stride), always keeping the steps around grasp/release so contact events
are not skipped (LAMP's own demos are sparse motion-plan waypoints, ~35 states each).

Output environments (LAMP needs names envN):
  env1  train demos (robomimic 'train' mask, 180 demos)
  env9  held-out nominal demos (robomimic 'valid' mask, 20 demos)
  env8  held-out demos with an injected failure, two per valid demo:
          drop: half-way through the last carry, the object is released and falls back to its resting height
          miss: from half-way through the last carry, arm and object are shifted 15 cm sideways, so the
                object is put down away from its target
Ground-truth event flags per kept step are saved to envN_gt.npz for evaluation.
"""
import argparse
import os
import pickle
import sys
import xml.etree.ElementTree as ET

import h5py
import numpy as np
from scipy.spatial.transform import Rotation as R

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import lamp_env  # noqa: E402

GRASP_DIST = 0.12   # m; robomimic grasps happen at 2-8 cm from the object reference point
MIN_GAP = 0.005     # m; fingers fully shut => nothing in hand
MISS_SHIFT = np.array([0.0, 0.15, 0.0])

TASKS = {
    "square": dict(domain="Square", file="square/ph/low_dim_v15.hdf5",
                   objects={"nut_1": 0}, graspable=["nut_1"], fixed={"peg_1": "peg1"}, stride=5),
    "tool_hang": dict(domain="ToolHang", file="tool_hang/ph/low_dim_v15.hdf5",
                      objects={"stand_1": 0, "frame_1": 1, "tool_1": 2}, graspable=["frame_1", "tool_1"],
                      fixed={}, stride=10),
}


def to6d(pos, quat_xyzw):
    return np.concatenate([pos, R.from_quat(quat_xyzw).as_rotvec()], axis=-1)


def fixed_body_pose(xml_str, body):
    root = ET.fromstring(xml_str)
    for b in root.iter("body"):
        if b.get("name") == body:
            p = np.array([float(v) for v in b.get("pos").split()])
            q = b.get("quat")
            qw = np.array([float(v) for v in q.split()]) if q else np.array([1.0, 0, 0, 0])   # MuJoCo wxyz
            return np.concatenate([p, R.from_quat(qw[[1, 2, 3, 0]]).as_rotvec()])
    raise KeyError(body)


def load_demo(g, task, tool_frame=False):
    obs = g["obs"]
    return build_demo(task, obs["object"][:], obs["robot0_eef_pos"][:], obs["robot0_eef_quat"][:],
                      obs["robot0_gripper_qpos"][:], g["actions"][:, -1], g.attrs["model_file"], tool_frame)


def canonicalize_peg(poses):
    """The square peg is 4-fold symmetric about its vertical axis, so its frame is only defined up to 90 deg
    turns. Per frame, turn the peg frame by k*90 deg (k in 0..3) to the one closest to the nut's yaw, so
    the four physically identical seatings of the nut map to one relative orientation. Idempotent."""
    if "peg_1" not in poses or "nut_1" not in poses:
        return poses
    peg, nut = poses["peg_1"], poses["nut_1"]
    out = peg.copy()
    for t in range(len(peg)):
        Rp, Rn = R.from_rotvec(peg[t, 3:]), R.from_rotvec(nut[t, 3:])
        best = None
        for k in range(4):
            Rk = Rp * R.from_euler("z", k * np.pi / 2)
            ang = (Rk.inv() * Rn).magnitude()
            if best is None or ang < best[0]:
                best = (ang, Rk)
        out[t, 3:] = best[1].as_rotvec()
    poses = dict(poses)
    poses["peg_1"] = out
    return poses


# Tool Hang, LAMP_TOOL_CANON=1: the hung tool sits ~172 deg from the frame's orientation, right at the rotation-vector
# wrap point, so its rotation flips sign between demos and LAMP never learns 'tool on hook'. The tool frame is
# right-multiplied by the inverse of the average hung orientation (measured on the 180 training demos by
# tool_canon.py), so hanging reads as ~23 deg instead of ~172 deg. Same idea as the gripper's tool_frame.
TOOL_CANON_Q = [0.616931, -0.047497, -0.785577, 0.002871]   # xyzw


def canonicalize_tool(poses):
    if "tool_1" not in poses:
        return poses
    t = poses["tool_1"].copy()
    t[:, 3:] = (R.from_rotvec(t[:, 3:]) * R.from_quat(TOOL_CANON_Q)).as_rotvec()
    poses = dict(poses)
    poses["tool_1"] = t
    return poses


FOLLOW_TOL = 0.02     # m: object counts as 'moving with the gripper' if its position in the gripper frame drifts < 2 cm
FOLLOW_LAG = 5        # frames over which the drift is measured (0.25 s at 20 Hz)
SETTLE = 10           # frames after closing during which the grasp may settle before 'following' is required


def held_by_motion(poses, graspable, rel_dist, closed, gap):
    """Grasp signal from the object moving with the gripper (LAMP_GRASP=motion), instead of 'gripper closed near
    the object'. A grasp starts when the gripper closes (fingers not fully shut) with an object within GRASP_DIST;
    it continues only while that object's position in the gripper frame stays within FOLLOW_TOL over FOLLOW_LAG
    frames, or while the gripper itself is not moving (nothing to follow). It ends when the gripper opens or the
    object stops following (e.g. it slipped out, or the gripper re-closed next to an object it is not carrying)."""
    T = len(closed)
    G = poses["gripper_1"]
    Rg = R.from_rotvec(G[:, 3:])
    rel = {n: Rg.inv().apply(poses[n][:, :3] - G[:, :3]) for n in graspable}
    held, since = [None] * T, 0
    for t in range(T):
        if not closed[t] or gap[t] < MIN_GAP:
            continue
        prev = held[t - 1] if t > 0 else None
        if prev is not None:
            since += 1
            k = max(0, t - FOLLOW_LAG)
            drift = np.linalg.norm(rel[prev][t] - rel[prev][k])
            gripper_moved = np.linalg.norm(G[t, :3] - G[k, :3]) > 0.005
            if since <= SETTLE or drift < FOLLOW_TOL or not gripper_moved:
                held[t] = prev
            continue
        name = min(graspable, key=lambda n: rel_dist[n][t])
        if rel_dist[name][t] < GRASP_DIST and (t == 0 or not closed[t - 1] or since == 0):
            held[t], since = name, 0
    return held


def build_demo(task, o, eef_pos, eq, gq, gripper_cmd, model_file, tool_frame=False):
    """Arrays (as recorded by robomimic, or live from robosuite) -> LAMP-ready demo dict."""
    spec = TASKS[task]
    T = o.shape[0]
    if tool_frame:
        # Express the gripper in a frame rotated 180 deg about its x axis, so "pointing down at the object"
        # is close to zero rotation (as in LAMP's own simulated grasps) instead of close to 180 deg, where
        # the rotation-vector representation flips sign and splits one grasp across many angle bins.
        eq = (R.from_quat(eq) * R.from_euler("x", np.pi)).as_quat()
    poses = {"gripper_1": to6d(eef_pos, eq)}
    rel_dist = {}
    for name, k in spec["objects"].items():
        poses[name] = to6d(o[:, 14 * k + 7:14 * k + 10], o[:, 14 * k + 10:14 * k + 14])
        rel_dist[name] = np.linalg.norm(o[:, 14 * k:14 * k + 3], axis=1)
    for name, body in spec["fixed"].items():
        poses[name] = np.repeat(fixed_body_pose(model_file, body)[None], T, axis=0)
    if os.environ.get("LAMP_TOOL_CANON") == "1":
        poses = canonicalize_tool(poses)
    closed = np.asarray(gripper_cmd) > 0
    gap = gq[:, 0] - gq[:, 1]
    if os.environ.get("LAMP_GRASP") == "motion":
        held = held_by_motion(poses, spec["graspable"], rel_dist, closed, gap)
        flags = o[:, 42:44] if task == "tool_hang" else None
        if os.environ.get("LAMP_PEG_SYMMETRY") == "1":
            poses = canonicalize_peg(poses)
        return dict(T=T, poses=poses, held=held, flags=flags)
    held = [None] * T
    for t in range(T):
        if not closed[t] or gap[t] < MIN_GAP:
            continue
        if t > 0 and held[t - 1] is not None:
            held[t] = held[t - 1]
            continue
        name = min(spec["graspable"], key=lambda n: rel_dist[n][t])
        if rel_dist[name][t] < GRASP_DIST:
            held[t] = name
    flags = o[:, 42:44] if task == "tool_hang" else None
    if os.environ.get("LAMP_PEG_SYMMETRY") == "1":
        poses = canonicalize_peg(poses)
    return dict(T=T, poses=poses, held=held, flags=flags)


def mh_split(ph_path):
    """Square multi-human (other operators) demos that are not copies of a proficient-human demo, split per operator
    group: even positions -> training (mixed-operator experiment, LAMP_MH_TRAIN=1), odd positions -> test.
    Returns {group: (train_names, test_names)}."""
    import hashlib
    key = lambda g: hashlib.md5(np.round(g["obs/object"][:20], 5).tobytes()).hexdigest() + str(g["actions"].shape[0])
    out = {}
    with h5py.File(ph_path, "r") as fp, h5py.File(ph_path.replace("/ph/", "/mh/"), "r") as fm:
        ph_keys = {key(fp["data"][n]) for n in fp["data"]}
        for grp in ("better", "okay", "worse"):
            names = sorted([x.decode() for x in fm["mask"][grp][:]], key=lambda s: int(s.split("_")[1]))
            names = [n for n in names if key(fm["data"][n]) not in ph_keys]
            out[grp] = (names[0::2], names[1::2])
    return out


def grasp_segments(held):
    segs, start = [], None
    for t, h in enumerate(held + [None]):
        if h is not None and start is None:
            start = t
        if start is not None and (h is None or h != held[start]):
            segs.append((start, t, held[start]))
            start = t if h is not None else None
    return segs


def inject(d, kind):
    """Return a modified copy of a demo with an injected failure in its last carry."""
    segs = grasp_segments(d["held"])
    if not segs:
        return None
    s, e, obj = segs[-1]
    mid = s + (e - s) // 2
    poses = {k: v.copy() for k, v in d["poses"].items()}
    held = list(d["held"])
    if kind == "drop":
        fallen = poses[obj][mid].copy()
        fallen[2] = poses[obj][s][2]           # back to its resting height
        fallen[3:] = poses[obj][s][3:]
        poses[obj][mid:] = fallen
        for t in range(mid, len(held)):
            if held[t] == obj:
                held[t] = None
    elif kind == "miss":
        poses["gripper_1"][mid:, :3] += MISS_SHIFT
        poses[obj][mid:, :3] += MISS_SHIFT
    return dict(T=d["T"], poses=poses, held=held, flags=d["flags"])


def keep_steps(d, stride):
    T, held = d["T"], d["held"]
    keep = set(range(0, T, stride)) | {T - 1}
    for t in range(1, T):
        if held[t] != held[t - 1]:
            keep |= {t - 1, t}
    return sorted(keep)


def to_envstates(d, stride, EnvState):
    states = []
    steps = keep_steps(d, stride)
    for t in steps:
        od = {}
        for name, p in d["poses"].items():
            v = [float(x) for x in p[t]]
            od[name] = [v, v] if name.startswith("gripper") else v
        kw = {"grabbed_flag_1": d["held"][t] is not None, "grabbed_object_1": d["held"][t]}
        states.append(EnvState(obj_dic=od, keyword_arguments=kw, num_robots=1))
    return states, steps


def ground_truth(task, d, steps):
    if task == "tool_hang":
        return {"frame_is_assembled": d["flags"][steps, 0] > 0.5, "tool_on_frame": d["flags"][steps, 1] > 0.5}
    nut, peg = d["poses"]["nut_1"][steps], d["poses"]["peg_1"][steps]
    # robosuite NutAssembly.on_peg: within 3 cm of the peg in x and y, and below the peg-top height
    on = (np.abs(nut[:, 0] - peg[:, 0]) < 0.03) & (np.abs(nut[:, 1] - peg[:, 1]) < 0.03) & (nut[:, 2] < peg[:, 2] + 0.05)
    return {"nut_on_peg": on}


def save_env(Config, env, trajs, objects, gts=None, labels=None):
    p = os.path.join(Config.DATA_MISC_DIR, env)
    os.makedirs(p, exist_ok=True)
    with open(os.path.join(p, env + "_data" + Config.PICKLE_SUFFIX), "wb") as f:
        pickle.dump({"env_states": trajs}, f, protocol=Config.PICKLE_PROTOCOL)
    with open(os.path.join(p, env + "_object_list" + Config.PICKLE_SUFFIX), "wb") as f:
        pickle.dump(set(objects) | {"table"}, f, protocol=Config.PICKLE_PROTOCOL)
    if gts is not None:
        np.savez(os.path.join(p, env + "_gt.npz"), **{"%d__%s" % (i, k): v for i, g in enumerate(gts) for k, v in g.items()})
    if labels is not None:
        with open(os.path.join(p, env + "_labels.txt"), "w") as f:
            f.write("\n".join(labels) + "\n")
    print("saved {}: {} demos, {} states".format(env, len(trajs), sum(map(len, trajs))))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", choices=list(TASKS), required=True)
    ap.add_argument("--data_root", default=os.path.expanduser("~/lamp_work/datasets/robomimic"))
    ap.add_argument("--stride", type=int, default=None)
    ap.add_argument("--max_train", type=int, default=None)
    ap.add_argument("--tool_frame", action="store_true", help="rotate the gripper frame 180 deg about x (see load_demo)")
    a = ap.parse_args()
    spec = TASKS[a.task]
    stride = a.stride or spec["stride"]
    Config = lamp_env.declare(spec["domain"])
    from src.data_structures.EnvState import EnvState

    with h5py.File(os.path.join(a.data_root, spec["file"]), "r") as f:
        names = lambda m: sorted([x.decode() for x in f["mask"][m][:]], key=lambda s: int(s.split("_")[1]))
        train, valid = names("train"), names("valid")
        if a.max_train:
            train = train[:a.max_train]
        demos = {n: load_demo(f["data"][n], a.task, a.tool_frame) for n in train + valid}

    objects = ["gripper_1"] + list(spec["objects"]) + list(spec["fixed"])
    tr = [to_envstates(demos[n], stride, EnvState)[0] for n in train]
    if os.environ.get("LAMP_MH_TRAIN") == "1":
        # mixed-operator training: add half of each other-operator group (the other half stays for testing)
        ph_path = os.path.join(a.data_root, spec["file"])
        with h5py.File(ph_path.replace("/ph/", "/mh/"), "r") as fm:
            for grp, (mtr, _) in mh_split(ph_path).items():
                tr += [to_envstates(load_demo(fm["data"][n], a.task, a.tool_frame), stride, EnvState)[0] for n in mtr]
                print("added {} '{}' other-operator demos to training".format(len(mtr), grp))
    save_env(Config, "env1", tr, objects)

    te, gts = [], []
    for n in valid:
        s, steps = to_envstates(demos[n], stride, EnvState)
        te.append(s); gts.append(ground_truth(a.task, demos[n], steps))
    save_env(Config, "env9", te, objects, gts, ["nominal"] * len(te))

    fe, fgts, labels = [], [], []
    for kind in ("drop", "miss"):
        for n in valid:
            d = inject(demos[n], kind)
            if d is None:
                continue
            s, steps = to_envstates(d, stride, EnvState)
            fe.append(s); fgts.append(ground_truth(a.task, d, steps)); labels.append(kind)
    save_env(Config, "env8", fe, objects, fgts, labels)

    # --- statistics to sanity-check the discretizer ranges ---
    ns = [len(grasp_segments(demos[n]["held"])) for n in train]
    print("grasp segments per train demo: min {} max {} mean {:.2f}".format(min(ns), max(ns), np.mean(ns)))
    held_by = {}
    for n in train:
        for s, e, o in grasp_segments(demos[n]["held"]):
            held_by.setdefault(o, []).append(e - s)
    print("held objects:", {k: len(v) for k, v in held_by.items()})
    import useful_functions as uf
    for (p, q) in [(x, y) for i, x in enumerate(objects) for y in objects[i + 1:]]:
        rel = np.array([uf.get_relative_pose(demos[n]["poses"][p][-1], demos[n]["poses"][q][-1]) for n in train])
        print("final rel pose {:>9s}->{:<9s} mean {} std {}".format(p, q, np.round(rel[:, :3].mean(0), 3).tolist(),
                                                                    np.round(rel[:, :3].std(0), 3).tolist()))
    for n in train[:1]:
        segs = grasp_segments(demos[n]["held"])
        for s, e, o in segs:
            rel = uf.get_relative_pose(demos[n]["poses"]["gripper_1"][s], demos[n]["poses"][o][s])
            print("demo {} grasp {} at step {}: {} in gripper frame = {}".format(n, o, s, o, np.round(rel, 3).tolist()))
    if a.task == "square":
        on = [ground_truth(a.task, demos[n], [demos[n]["T"] - 1])["nut_on_peg"][0] for n in train]
        print("ground truth nut_on_peg at final step: {}/{}".format(int(np.sum(on)), len(on)))
