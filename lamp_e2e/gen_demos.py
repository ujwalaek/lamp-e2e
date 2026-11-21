"""
Step 1: generate demonstrations (stand-in for LAMP's gen_data.py + OpenRAVE).

LAMP's src/data_gen/Packing.py drives a MagneticGripper in OpenRAVE:
    reach can -> grab -> carry to box (surface_1) -> release -> move to random config
and records one EnvState per motion-plan waypoint. Each EnvState holds
    object_dict[name] = 6D pose [x, y, z, rotvec]      (for objects)
    object_dict[name] = [dof_values, 6D link pose]     (for robot links, e.g. gripper_1)
    grabbed_flag_1, grabbed_object_1                    (the grasp "sensor")

This script reproduces that logic kinematically with numpy (no physics, no collision
checks). Output files go exactly where LAMP expects them:
    Data/Packing/misc/<env>/<env>_data.pkl          {"env_states": [traj, ...]}
    Data/Packing/misc/<env>/<env>_object_list.pkl   set of object names

Environments (mirroring argument_files/gen_data.json for Packing):
    env1: full goal-reaching demos, box at a random pose on the table
    env2: random_env_setup=True, so each demo is truncated after 1-3 of its 4 segments
          (LAMP's way of adding non-goal-reaching demos)
    env9: held-out TEST demos (not used for learning), including injected execution
          failures for the execution-monitoring use case:
             nominal | drop  (can slips during carry) | miss (released outside the box)
"""
import argparse
import os
import pickle

import numpy as np
from scipy.spatial.transform import Rotation as R, Slerp

from _lamp_path import setup
setup()

from Config import Config  # noqa: E402
Config.declare_config("Packing", "MagneticGripper")
from src.data_structures.EnvState import EnvState  # noqa: E402
import useful_functions as uf  # noqa: E402

# ---- geometry, taken from LAMP's Packing.py / Robots.py (MagneticGripper) ----
GRASP_OFFSET_Z = 0.21          # Robots.py: grasping_offset["can"] = 0.21
GRASP_YAW = -np.pi / 4.0       # Packing.sample_grasp_pose: rotz(-pi/4)
DROPAREA_HALF = 0.075          # Packing.droparea_dims
CAN_RADIUS = 0.03
TABLE_X = (-0.45, 0.45)
TABLE_Y = (-0.45, 0.45)
PLACE_Z = 0.001                # can placed 1 mm above the surface frame
N_WAYPOINTS = 12               # waypoints per motion-plan segment

CAN, GRIP, SURF = "can_1", "gripper_1", "surface_1"
OBJECTS = {CAN, GRIP, SURF, "table6"}


def T_from_pose(p):
    return uf.transform_from_sixd_pose(list(p))


def pose_from_T(T):
    return [float(v) for v in uf.sixd_pose_from_transform(T)]


def rotz(a):
    T = np.eye(4)
    T[:3, :3] = R.from_rotvec([0, 0, a]).as_matrix()
    return T


def trans(x, y, z):
    T = np.eye(4)
    T[:3, 3] = [x, y, z]
    return T


# can frame -> gripper frame at grasp (same composition as Packing.sample_grasp_pose)
CAN_T_GRIP = trans(0, 0, GRASP_OFFSET_Z).dot(rotz(GRASP_YAW))


def interp(T0, T1, n):
    """Straight-line 'motion plan': linear position + slerp orientation."""
    rots = R.from_matrix(np.stack([T0[:3, :3], T1[:3, :3]]))
    slerp = Slerp([0, 1], rots)
    out = []
    for s in np.linspace(0, 1, n)[1:]:
        T = np.eye(4)
        T[:3, :3] = slerp([s]).as_matrix()[0]
        T[:3, 3] = (1 - s) * T0[:3, 3] + s * T1[:3, 3]
        out.append(T)
    return out


def via_lift(T0, T1, n, rng):
    """Go up, across, and down. Like a sampling-based motion planner, the intermediate
    waypoints vary from demo to demo (random lift height, waypoint count and jitter);
    only the endpoints are exact."""
    lift = rng.uniform(0.08, 0.20)
    up0 = T0.copy(); up0[2, 3] += lift
    up1 = T1.copy(); up1[2, 3] += lift + rng.uniform(-0.03, 0.03)
    up1[:2, 3] += rng.uniform(-0.03, 0.03, size=2)
    k = max(2, n // 3)
    path = interp(T0, up0, k) + interp(up0, up1, k) + interp(up1, T1, int(rng.integers(k, 2 * k)))
    for T in path[:-1]:
        T[:3, 3] += rng.normal(0, 0.01, size=3)
    return path


class World(object):
    def __init__(self, rng):
        self.rng = rng
        self.T = {}
        self.grabbed = None
        self.grip_rel = None   # gripper_T_can while grabbed

    def state(self):
        d = {}
        for name in (CAN, SURF):
            d[name] = pose_from_T(self.T[name])
        gp = pose_from_T(self.T[GRIP])
        d[GRIP] = [list(gp), list(gp)]        # [dof values, link pose]; magnetic gripper is a free-floating 6-DOF body
        kw = {"grabbed_flag_1": self.grabbed is not None, "grabbed_object_1": self.grabbed}
        return EnvState(obj_dic=d, keyword_arguments=kw, num_robots=1)

    def move_gripper(self, path):
        states = []
        for T in path:
            self.T[GRIP] = T
            if self.grabbed is not None:
                self.T[self.grabbed] = T.dot(self.grip_rel)
            states.append(self.state())
        return states

    def grab(self, obj):
        self.grabbed = obj
        self.grip_rel = np.linalg.inv(self.T[GRIP]).dot(self.T[obj])

    def release(self):
        self.grabbed = None
        self.grip_rel = None


def random_table_xy(rng, margin):
    return (rng.uniform(TABLE_X[0] + margin, TABLE_X[1] - margin),
            rng.uniform(TABLE_Y[0] + margin, TABLE_Y[1] - margin))


def random_gripper_T(rng):
    x, y = random_table_xy(rng, 0.05)
    z = rng.uniform(0.25, 0.45)
    T = trans(x, y, z)
    T[:3, :3] = R.from_euler("xyz", [np.pi, 0, rng.uniform(-np.pi, np.pi)]).as_matrix()  # pointing down
    return T


def reset_world(rng):
    w = World(rng)
    sx, sy = random_table_xy(rng, 0.15)
    w.T[SURF] = trans(sx, sy, 0.0).dot(rotz(rng.uniform(-np.pi, np.pi)))
    while True:  # can on the table, well away from the box
        cx, cy = random_table_xy(rng, 0.05)
        if np.hypot(cx - sx, cy - sy) > 0.30:
            break
    w.T[CAN] = trans(cx, cy, PLACE_Z).dot(rotz(rng.uniform(-np.pi, np.pi)))
    w.T[GRIP] = random_gripper_T(rng)
    return w


def sample_goal_T(w, rng, inside=True):
    lim = DROPAREA_HALF - CAN_RADIUS
    if inside:
        x, y = rng.uniform(-lim, lim, size=2)
    else:  # deliberately outside the box (execution failure)
        ang = rng.uniform(-np.pi, np.pi)
        r = rng.uniform(0.20, 0.25)
        x, y = r * np.cos(ang), r * np.sin(ang)
    # Packing.sample_goal_pose: can placed with identity rotation in the box frame
    return w.T[SURF].dot(trans(x, y, PLACE_Z))


def demo(rng, truncate=False, failure=None):
    """One demonstration = list of EnvStates. failure in {None, 'drop', 'miss'}."""
    w = reset_world(rng)
    segs = [[w.state()]]

    # 1) reach: gripper moves to grasp pose above the can; then grab
    grasp_T = w.T[CAN].dot(CAN_T_GRIP)
    s1 = w.move_gripper(via_lift(w.T[GRIP], grasp_T, N_WAYPOINTS, rng))
    w.grab(CAN)
    s1.append(w.state())
    segs.append(s1)

    # 2) carry to the box; then release
    goal_can_T = sample_goal_T(w, rng, inside=(failure != "miss"))
    place_grip_T = goal_can_T.dot(CAN_T_GRIP)
    path = via_lift(w.T[GRIP], place_grip_T, N_WAYPOINTS, rng)
    if failure == "drop":
        k = len(path) // 2
        s2 = w.move_gripper(path[:k])
        # can slips: the magnet fails, the can falls straight down to the table
        w.release()
        fallen = w.T[CAN].copy(); fallen[2, 3] = PLACE_Z
        w.T[CAN] = fallen
        s2.append(w.state())
        s2 += w.move_gripper(path[k:])
    else:
        s2 = w.move_gripper(path)
        w.release()
        s2.append(w.state())
    segs.append(s2)

    # 3) move the arm to a random configuration
    segs.append(w.move_gripper(interp(w.T[GRIP], random_gripper_T(rng), N_WAYPOINTS)))

    last = rng.integers(1, len(segs)) if truncate else len(segs)   # Packing.start(): randint(1, len(states))
    traj = []
    for s in segs[:last]:
        traj.extend(s)
    return traj


def save_env(env, trajs, labels=None):
    d = os.path.join(Config.DATA_MISC_DIR, env)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, env + "_data" + Config.PICKLE_SUFFIX), "wb") as f:
        pickle.dump({"env_states": trajs}, f, protocol=Config.PICKLE_PROTOCOL)
    with open(os.path.join(d, env + "_object_list" + Config.PICKLE_SUFFIX), "wb") as f:
        pickle.dump(set(OBJECTS), f, protocol=Config.PICKLE_PROTOCOL)
    if labels is not None:
        with open(os.path.join(d, env + "_labels.txt"), "w") as f:
            f.write("\n".join(labels) + "\n")
    print("saved {:6s} {:3d} demos, {:5d} states -> {}".format(env, len(trajs), sum(map(len, trajs)), d))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--n_full", type=int, default=30, help="goal-reaching demos (env1)")
    ap.add_argument("--n_partial", type=int, default=30, help="truncated demos (env2)")
    ap.add_argument("--n_test", type=int, default=3, help="test demos per type (env9)")
    ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args()
    rng = np.random.default_rng(a.seed)

    save_env("env1", [demo(rng) for _ in range(a.n_full)])
    save_env("env2", [demo(rng, truncate=True) for _ in range(a.n_partial)])

    test, labels = [], []
    for kind in ("nominal", "drop", "miss"):
        for _ in range(a.n_test):
            test.append(demo(rng, failure=None if kind == "nominal" else kind))
            labels.append(kind)
    save_env("env9", test, labels)
