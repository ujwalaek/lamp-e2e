"""Smoke test: restore a recorded robomimic state in robosuite and render one camera frame."""
import json
import os
import sys

os.environ.setdefault("MUJOCO_GL", "egl")
os.environ.setdefault("PYOPENGL_PLATFORM", "egl")

import h5py  # noqa: E402
import numpy as np  # noqa: E402
import robosuite  # noqa: E402
from PIL import Image  # noqa: E402


def make_env(f):
    meta = json.loads(f["data"].attrs["env_args"])
    kw = dict(meta["env_kwargs"])
    kw.update(has_renderer=False, has_offscreen_renderer=True, use_camera_obs=False, ignore_done=True)
    return robosuite.make(meta["env_name"], **kw)


def restore(env, model_xml, state):
    env.reset()
    env.reset_from_xml_string(env.edit_model_xml(model_xml))
    env.sim.reset()
    env.sim.set_state_from_flattened(state)
    env.sim.forward()


if __name__ == "__main__":
    path, out = sys.argv[1], sys.argv[2]
    with h5py.File(path, "r") as f:
        env = make_env(f)
        d = f["data/demo_0"]
        states = d["states"][:]
        restore(env, d.attrs["model_file"], states[len(states) // 2])
        names = list(env.sim.model.camera_names)
        print("cameras:", names)
        img = env.sim.render(height=256, width=256, camera_name="agentview")[::-1]
        Image.fromarray(img).save(out)
        print("saved", out, img.shape, "mean pixel", round(float(np.mean(img)), 1))
