"""LAMP domain configs for robomimic tasks, in the same format as lamp/domain_configs/<Domain>Config.py.

Object types (LAMP names objects <type>_<id>):
  Square:   gripper_1 (robot link = end effector), nut_1 (square nut), peg_1 (square peg, fixed)
  ToolHang: gripper_1, stand_1 (stand base, the "base" sensor), frame_1 (hook frame), tool_1 (wrench)

Discretizer convention (LAMP's Discretizer): (start, end, bins) describe a *world* box; the relative
grid LAMP actually uses spans +-(end-start)*sqrt(2) with ceil(bins*2*sqrt(2)) bins per position axis.
Angles: 61 bins per axis over [-pi, pi] (LAMP's default everywhere), after rounding to 0.05 rad.

Criticality threshold theta (EVAL_THRESHOLDING_VALUES) = fraction of demos that must visit a bin.
LAMP uses 1.0 for gripper-object pairs in Packing/Keva/Jenga. Defaults below follow that; override with
environment variables for sweeps:
  LAMP_THETA_GRIP   theta for gripper-object pairs     (default 1.0)
  LAMP_THETA_OBJ    theta for object-object pairs      (default 1.0)
  LAMP_GRIP_BINS    world bins per position axis, gripper pairs (default 35, as in Packing)
  LAMP_ANG_BINS     bins per rotation axis, all pairs        (default 61, as in every LAMP config)
"""
import math
import os

import numpy as np

A = math.radians(180)


def _disc(xy, z, bins_xy, bins_z, ang_bins=None):
    ang_bins = ang_bins or int(os.environ.get("LAMP_ANG_BINS", 61))
    return (np.array([-xy, -xy, -z, -A, -A, -A]),
            np.array([xy, xy, z, A, A, A]),
            np.array([bins_xy, bins_xy, bins_z, ang_bins, ang_bins, ang_bins]))


def _env(name, default, cast=float):
    return cast(os.environ.get(name, default))


def _common(objects, graspable, pairs_grip, pairs_obj, disc):
    tg, to = _env("LAMP_THETA_GRIP", 1.0), _env("LAMP_THETA_OBJ", 1.0)
    thr = {frozenset(p): tg for p in pairs_grip}
    thr.update({frozenset(p): to for p in pairs_obj})
    return dict(
        OBJECT_NAME=list(graspable),        # types the gripper can hold (drives the grasp sensor)
        MVG_THRESHOLD=0.8,
        MVG_SCORE_THRESHOLD=3,              # same value as CafeWorldConfig (Packing has none)
        EVAL_THRESHOLDING_VALUES=thr,
        BOUND_OBJECT_NAME="table",
        NON_AUX_OBJECTS_SET=frozenset(objects) - frozenset(["gripper"]),
        DISCRETIZER_PARAMS=disc,
        SURFACES=[], CONST_TYPES=[], CONST_NAMES=[],
        NON_RELATION_OBJECTS=["table"],
        LOCATION_NAME=[],
        IMMOVABLE_OBJECTS=["table"],
        ROBOT_NAME="Panda",
    )


def square():
    gb = _env("LAMP_GRIP_BINS", 35, int)
    grip = _disc(0.15, 0.15, gb, gb)
    pairs_grip = [("gripper", "nut"), ("gripper", "peg")]
    pairs_obj = [("nut", "peg")]
    disc = {frozenset(("gripper", "nut")): grip,
            frozenset(("gripper", "peg")): grip,
            # nut seated on the peg: small xy window, taller z window (nut slides down the peg)
            frozenset(("nut", "peg")): _disc(0.05, 0.10, 5, 5)}
    return _common(["gripper", "nut", "peg"], ["nut"], pairs_grip, pairs_obj, disc)


def tool_hang():
    gb = _env("LAMP_GRIP_BINS", 35, int)
    grip = _disc(0.15, 0.15, gb, gb)
    obj = _disc(0.15, 0.15, 8, 8)            # ~5 cm relational bins for object-object pairs
    pairs_grip = [("gripper", "stand"), ("gripper", "frame"), ("gripper", "tool")]
    pairs_obj = [("stand", "frame"), ("stand", "tool"), ("frame", "tool")]
    disc = {frozenset(p): grip for p in pairs_grip}
    disc.update({frozenset(p): obj for p in pairs_obj})
    return _common(["gripper", "stand", "frame", "tool"], ["frame", "tool"], pairs_grip, pairs_obj, disc)


CONFIGS = {"Square": square, "ToolHang": tool_hang}
