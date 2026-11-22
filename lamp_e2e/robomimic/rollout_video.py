"""
Roll out a robomimic demo in the physics simulator (optionally with a real, physically simulated
failure), label every frame with LAMP's learned regions, and write an annotated video.

  nominal : replay the human demo's recorded actions as they are
  drop    : same actions, but the gripper is commanded open half-way through the last carry,
            so the object really falls
  miss    : same actions, but the arm is pushed sideways for a few steps half-way through the last
            carry, so the object is put down away from its target

For every frame and every object pair the overlay shows:
  - the relative pose (position in cm, rotation in degrees) of the second object in the first one's frame,
    exactly as LAMP computes it (useful_functions.get_relative_pose)
  - GREEN "in learned region <predicate>" when LAMP's learned critical region for that pair contains the
    pose (LAMP's own test: Relation.evaluate_in_ll_state = binned pose + grasp sensor in the region),
    RED "OUTSIDE learned regions" when no learned region of that pair contains it,
    GREY when LAMP learned no region at all for that pair
  - a timeline strip per pair (green/red over the whole rollout, with a cursor)

usage:
  rollout_video.py --task square --case drop --demo demo_150 --out out/videos/square_drop.mp4
"""
import argparse
import json
import os
import sys

os.environ.setdefault("MUJOCO_GL", "egl")
os.environ.setdefault("PYOPENGL_PLATFORM", "egl")

import h5py  # noqa: E402
import numpy as np  # noqa: E402
from PIL import Image, ImageDraw, ImageFont  # noqa: E402
from scipy.spatial.transform import Rotation as R  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

GREEN, RED, GREY = (40, 160, 70), (210, 50, 50), (150, 150, 150)
BG, FG, MUTED = (250, 250, 250), (30, 30, 30), (110, 110, 110)


# ---------------------------------------------------------------- simulation
def make_env(f):
    import robosuite
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


def carry_window(actions):
    """[start, end) of the last substantial 'gripper closed' segment: the last one at least half as long as
    the longest. This skips short final regrasps (e.g. Tool Hang's adjustment after the tool is already hung)."""
    closed = actions[:, -1] > 0
    segs, s = [], None
    for t, c in enumerate(list(closed) + [False]):
        if c and s is None:
            s = t
        if not c and s is not None:
            segs.append((s, t)); s = None
    longest = max(e - b for b, e in segs)
    return [(b, e) for b, e in segs if e - b >= 0.5 * longest][-1]


def rollout(f, demo, case, push, push_steps, camera, size):
    g = f["data"][demo]
    actions = g["actions"][:].copy()
    s, e = carry_window(actions)
    mid = s + (e - s) // 2
    if case == "drop":
        actions[mid:, -1] = -1.0
    elif case == "miss":
        actions[mid:mid + push_steps, 1] += push
    env = make_env(f)
    restore(env, g.attrs["model_file"], g["states"][0])
    rec = {k: [] for k in ("object", "eef_pos", "eef_quat", "gq", "cmd")}
    frames = []
    obs = env._get_observations(force_update=True)
    for t in range(len(actions)):
        rec["object"].append(obs["object-state"]); rec["eef_pos"].append(obs["robot0_eef_pos"])
        rec["eef_quat"].append(obs["robot0_eef_quat"]); rec["gq"].append(obs["robot0_gripper_qpos"])
        rec["cmd"].append(actions[t, -1])
        frames.append(env.sim.render(height=size, width=size, camera_name=camera)[::-1])
        obs, _, _, _ = env.step(actions[t])
    success = bool(env._check_success())
    rec = {k: np.array(v) for k, v in rec.items()}
    return rec, frames, success, g.attrs["model_file"], (s, e, mid)


# ---------------------------------------------------------------- LAMP labelling
def lamp_labels(task, demo_d, Config):
    import useful_functions as uf
    from src.data_structures.WorldModel import WorldModel
    from src.data_structures.EnvState import EnvState
    import convert
    prefix = open(Config.DATA_MISC_DIR + "latest_prefix.txt").read().strip()
    WorldModel.set_params(prefix)
    model = WorldModel.load_model(0)
    states, _ = convert.to_envstates(demo_d, 1, EnvState)            # every frame, no subsampling
    objs = list(states[0].object_dict.keys())
    names = sorted(n for n in objs if n.split("_")[0] not in Config.NON_RELATION_OBJECTS)
    names.sort(key=lambda n: n.split("_")[0] not in Config.ROBOT_TYPES)
    pairs = [(p, q) for i, p in enumerate(names) for q in names[i + 1:]]
    rels = {}
    for key, d in model.relations.items():
        for cr, rel in d.items():
            if cr != 0:
                rels.setdefault(frozenset([rel.parameter1_type, rel.parameter2_type]), []).append(rel)

    def pose(s, n):
        p = s.object_dict[n]
        return p[1] if n.split("_")[0] in Config.ROBOT_TYPES else p

    out = []
    for s in states:
        row = {}
        for p, q in pairs:
            rp = uf.get_relative_pose(pose(s, p), pose(s, q))
            inside = []
            for rel in rels.get(frozenset([p.split("_")[0], q.split("_")[0]]), []):
                a, b = (p, q) if rel.parameter1_type == p.split("_")[0] else (q, p)
                gr = rel.get_grounded_relation(uf.Link(a, rel.parameter1_type), uf.Link(b, rel.parameter2_type), objs)
                if gr.evaluate_in_ll_state(s):
                    inside.append("{}_{}_{}".format(rel.parameter1_type, rel.parameter2_type, rel.cr))
            row[(p, q)] = dict(rel=rp, inside=inside,
                               learned=len(rels.get(frozenset([p.split("_")[0], q.split("_")[0]]), [])))
        row["_held"] = s.grabbed_object_1
        out.append(row)
    return pairs, out


# ---------------------------------------------------------------- drawing
def font(sz, bold=False):
    for p in (["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"] if bold else []) + \
             ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
        if os.path.exists(p):
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()


ROW_LEARNED, ROW_NONE, HEADER = 104, 66, 90


def draw_frame(img, t, T, pairs, labels, title, subtitle, gloss, panel_w=600):
    need = HEADER + sum(ROW_LEARNED if labels[0][pq]["learned"] else ROW_NONE for pq in pairs) + 6
    H = max(img.shape[0], need)
    canvas = Image.new("RGB", (img.shape[1] + panel_w, H), BG)
    canvas.paste(Image.fromarray(img), (0, (H - img.shape[0]) // 2))
    d = ImageDraw.Draw(canvas)
    x0 = img.shape[1] + 18
    f_t, f_b, f_s, f_m = font(19, True), font(15, True), font(14), font(13)
    d.text((x0, 12), title, fill=FG, font=f_t)
    d.text((x0, 38), subtitle, fill=MUTED, font=f_s)
    held = labels[t]["_held"]
    d.text((x0, 58), "step {}/{}   t = {:.2f} s   holding: {}".format(t + 1, T, t / 20.0, held or "nothing"),
           fill=FG, font=f_s)
    y = HEADER
    for (p, q) in pairs:
        L = labels[t][(p, q)]
        rp = L["rel"]
        pos_cm = np.array(rp[:3]) * 100
        rpy = np.degrees(R.from_rotvec(rp[3:]).as_euler("xyz"))
        d.text((x0, y), "{} → {}".format(p.rsplit("_", 1)[0], q.rsplit("_", 1)[0]), fill=FG, font=f_b)
        d.text((x0, y + 20), "pos  x {:+6.1f}  y {:+6.1f}  z {:+6.1f} cm".format(*pos_cm), fill=FG, font=f_m)
        d.text((x0, y + 37), "rot  r {:+6.0f}  p {:+6.0f}  y {:+6.0f} deg".format(*rpy), fill=FG, font=f_m)
        if L["learned"] == 0:
            # compact row: pose plus a grey note, no status bar or timeline
            d.text((x0 + 330, y + 2), "(no region learned)", fill=GREY, font=f_m)
            y += ROW_NONE
            continue
        if L["inside"]:
            names = ", ".join(n + (" ({})".format(gloss[n]) if n in gloss else "") for n in L["inside"])
            col, txt = GREEN, "IN learned region: " + names
        else:
            col, txt = RED, "OUTSIDE learned regions"
        d.rounded_rectangle((x0, y + 56, x0 + panel_w - 36, y + 78), radius=6, fill=col)
        d.text((x0 + 8, y + 59), txt, fill=(255, 255, 255), font=f_m)
        # timeline strip
        ty, tw = y + 84, panel_w - 36
        for k in range(T):
            Lk = labels[k][(p, q)]
            c = GREY if Lk["learned"] == 0 else (GREEN if Lk["inside"] else RED)
            xa = x0 + int(k * tw / T); xb = x0 + int((k + 1) * tw / T)
            d.rectangle((xa, ty, max(xa, xb - 1), ty + 8), fill=c)
        cx = x0 + int(t * tw / T)
        d.rectangle((cx - 1, ty - 3, cx + 1, ty + 11), fill=FG)
        y += ROW_LEARNED
    return np.array(canvas)


def gloss_for(domain, sweep):
    """Plain-language names for predicates, from the ground-truth match of the matching sweep run."""
    path = os.path.join(os.path.dirname(HERE), "out", domain, sweep, "gt_eval.json")
    if not os.path.exists(path):
        return {}
    names = {"nut_on_peg": "nut on peg", "frame_is_assembled": "frame in stand", "holding": "holding",
             "tool_on_frame": "tool on frame"}
    g = {}
    for k, v in json.load(open(path)).items():
        if v.get("predicate") and v.get("f1", 0) and v["f1"] >= 0.4:
            g.setdefault(v["predicate"], "~" + names.get(k, k))
    return g


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", choices=["square", "tool_hang"], required=True)
    ap.add_argument("--case", choices=["nominal", "drop", "miss"], default="nominal")
    ap.add_argument("--demo", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--camera", default="agentview")
    ap.add_argument("--size", type=int, default=512)
    ap.add_argument("--push", type=float, default=1.0, help="miss: added to the y action")
    ap.add_argument("--push_steps", type=int, default=12)
    ap.add_argument("--tool_frame", action="store_true")
    ap.add_argument("--gloss_sweep", default="", help="e.g. sweep_coarse/theta_0.5 (for predicate names)")
    ap.add_argument("--data_root", default=os.path.expanduser("~/lamp_work/datasets/robomimic"))
    a = ap.parse_args()

    import lamp_env
    import convert
    domain = convert.TASKS[a.task]["domain"]
    Config = lamp_env.declare(domain)
    with h5py.File(os.path.join(a.data_root, convert.TASKS[a.task]["file"]), "r") as f:
        rec, frames, success, xml, (s, e, mid) = rollout(f, a.demo, a.case, a.push, a.push_steps, a.camera, a.size)
    demo_d = convert.build_demo(a.task, rec["object"], rec["eef_pos"], rec["eef_quat"], rec["gq"], rec["cmd"], xml,
                                a.tool_frame)
    pairs, labels = lamp_labels(a.task, demo_d, Config)
    gloss = gloss_for(domain, a.gloss_sweep) if a.gloss_sweep else {}
    T = len(frames)
    title = "{} | {} rollout | task success: {}".format(domain, a.case.upper(), "yes" if success else "NO")
    sub = "robomimic {} (held out)  |  LAMP regions: {}".format(a.demo, a.gloss_sweep or "current model")
    import imageio
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    with imageio.get_writer(a.out, fps=20, codec="libx264", quality=7, macro_block_size=8) as w:
        for t in range(T):
            w.append_data(draw_frame(frames[t], t, T, pairs, labels, title, sub, gloss))
    # a still of an informative frame (end of rollout) for quick preview
    Image.fromarray(draw_frame(frames[-1], T - 1, T, pairs, labels, title, sub, gloss)).save(a.out[:-4] + "_last.png")
    summ = {"demo": a.demo, "case": a.case, "success": success, "frames": T, "carry": [int(s), int(e)], "event_step": int(mid),
            "fraction_outside": {"{}->{}".format(p, q): float(np.mean([not L[(p, q)]["inside"] for L in labels]))
                                 for p, q in pairs if labels[0][(p, q)]["learned"]}}
    json.dump(summ, open(a.out[:-4] + ".json", "w"), indent=1)
    print(json.dumps(summ))
