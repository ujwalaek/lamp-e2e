"""
Annotated rollout video for the stage-aware durative monitor.

Per frame the panel shows: the current stage of the durative model, every object pair with its relative pose,
and for each pair either the stage's condition on it (green satisfied / amber needed at stage end, not yet /
red violated) or grey 'not checked in this stage'. The bottom bar is the monitor verdict (OK so far / ALARM
with the violated condition).

usage: durative_video.py --task square --case drop --demo demo_5 --tag pegsym_dilate1 --out out/videos/x.mp4
       (env: LAMP_GRIP_BINS, LAMP_ANG_BINS, LAMP_PEG_SYMMETRY, LAMP_DILATE must match the evaluated variant)
"""
import argparse
import json
import os
import sys

os.environ.setdefault("MUJOCO_GL", "egl")
import h5py  # noqa: E402
import numpy as np  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402
from scipy.spatial.transform import Rotation as R  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE)); sys.path.insert(0, HERE)
import lamp_env  # noqa: E402
import convert  # noqa: E402
import durative as DUR  # noqa: E402
from rollout_video import rollout, font  # noqa: E402

GREEN, RED, AMBER, GREY = (40, 160, 70), (210, 50, 50), (225, 150, 20), (165, 165, 165)
BG, FG, MUTED = (250, 250, 250), (30, 30, 30), (110, 110, 110)
KIND = {"start": "at start", "all": "over all", "end": "at end"}


def load_tolerances(domain, tag):
    J = json.load(open(os.path.join(os.path.dirname(HERE), "out", domain, "durative_" + tag, "durative_eval.json")))
    tol = {}
    for k, v in J["tolerances"].items():
        st, kind, pred, pol = k.split("|")
        tol[(st, kind, pred, pol == "True")] = v
    return tol


def stage_at(stages, t):
    for name, s, e in stages:
        if s <= t < e:
            return name, s, e
    return stages[-1]


def pair_status(domain, run, t, viol_by_key):
    """For each pair: list of (text, colour) for the current stage's conditions on that pair."""
    st, s, e = stage_at(run["stages"], t)
    conds = [c for x in DUR.STAGES[domain] if x["name"] == st for c in x["cond"]]
    out = {}
    for kind, pred, pol in conds:
        pair = DUR.PRED_PAIR[pred]
        learned = bool(DUR.PREDICATES[domain][pred][1])
        val = bool(run["truth"][pred][t]) == pol
        label = "{} {}{}".format(KIND[kind], "" if pol else "not ", pred)
        v = viol_by_key.get((st, KIND[kind], pred))
        if not learned:
            col, txt = GREY, label + ": not checkable (no learned region)"
        elif v is not None and t >= v["frame"]:
            col, txt = RED, label + ": VIOLATED"
        elif kind == "all":
            col, txt = (GREEN if val else AMBER), label + (": holds" if val else ": false now (within tolerance)")
        elif kind == "end":
            col, txt = (GREEN if val else AMBER), label + (": reached" if val else ": needed by stage end")
        else:
            # at start is checked once, at the stage start; not violated -> it passed
            col, txt = GREEN, label + ": ok (checked at stage start)"
        out.setdefault(pair, []).append((txt, col))
    return st, s, e, out


def fixed_height(img_h, domain, pairs):
    """One canvas height that fits the busiest stage (a video needs a constant frame size)."""
    worst = 0
    for st in DUR.STAGES[domain]:
        per = {}
        for _, pred, _ in st["cond"]:
            per[DUR.PRED_PAIR[pred]] = per.get(DUR.PRED_PAIR[pred], 0) + 1
        h = sum(22 + (24 * per[p] + 12 if p in per else 30) for p in pairs)
        worst = max(worst, h)
    return max(img_h, 134 + worst + 70)


def draw(img, t, T, domain, run, pairs, violations, title, sub, panel_w=640):
    viol_by_key = {(v["stage"], v["kind"], v["pred"]): v for v in violations}
    st, s, e, status = pair_status(domain, run, t, viol_by_key)
    H = fixed_height(img.shape[0], domain, pairs)
    canvas = Image.new("RGB", (img.shape[1] + panel_w, H), BG)
    canvas.paste(Image.fromarray(img), (0, (H - img.shape[0]) // 2))
    d = ImageDraw.Draw(canvas)
    x0 = img.shape[1] + 18
    d.text((x0, 10), title, fill=FG, font=font(19, True))
    d.text((x0, 36), sub, fill=MUTED, font=font(13))
    d.text((x0, 56), "t = {:.2f} s   holding: {}".format(t / 20.0, run["held"][t] or "nothing"), fill=FG, font=font(14))
    # stage strip
    d.text((x0, 80), "stage: " + st, fill=FG, font=font(17, True))
    tw = panel_w - 36
    for i, (name, a, b) in enumerate(run["stages"]):
        xa, xb = x0 + int(a * tw / T), x0 + int(b * tw / T)
        d.rectangle((xa, 106, max(xa, xb - 1), 118), fill=(120, 150, 200) if i % 2 == 0 else (170, 190, 225))
    cx = x0 + int(t * tw / T)
    d.rectangle((cx - 1, 102, cx + 1, 122), fill=FG)
    y = 134
    for p, q in pairs:
        sv = run["states"][t]
        from eval_durative import link_pose
        import useful_functions as uf
        rp = uf.get_relative_pose(link_pose(run["Config"], sv, p), link_pose(run["Config"], sv, q))
        pos = np.array(rp[:3]) * 100
        rpy = np.degrees(R.from_rotvec(rp[3:]).as_euler("xyz"))
        relevant = (p, q) in status
        d.text((x0, y), "{} → {}".format(p.rsplit("_", 1)[0], q.rsplit("_", 1)[0]),
               fill=FG if relevant else GREY, font=font(15, True))
        d.text((x0 + 200, y + 1), "pos {:+5.1f} {:+5.1f} {:+5.1f} cm   rpy {:+4.0f} {:+4.0f} {:+4.0f}".format(*pos, *rpy),
               fill=FG if relevant else GREY, font=font(12))
        y += 22
        if not relevant:
            d.text((x0 + 10, y), "not checked in this stage", fill=GREY, font=font(13))
            y += 30
            continue
        for txt, col in status[(p, q)]:
            d.rounded_rectangle((x0, y, x0 + tw, y + 20), radius=5, fill=col)
            d.text((x0 + 8, y + 3), txt, fill=(255, 255, 255), font=font(13))
            y += 24
        y += 12
    # verdict
    fired = [v for v in violations if v["frame"] <= t]
    vy = H - 56
    if fired:
        v = sorted(fired, key=lambda x: x["frame"])[0]
        d.rounded_rectangle((x0, vy, x0 + tw, vy + 40), radius=8, fill=RED)
        d.text((x0 + 10, vy + 4), "ALARM at {:.2f} s".format(v["frame"] / 20.0), fill=(255, 255, 255), font=font(15, True))
        d.text((x0 + 10, vy + 22), "{}: {} {}{}".format(v["stage"], v["kind"], "" if v["pol"] else "not ", v["pred"]),
               fill=(255, 255, 255), font=font(13))
    else:
        d.rounded_rectangle((x0, vy, x0 + tw, vy + 40), radius=8, fill=GREEN)
        d.text((x0 + 10, vy + 11), "OK so far: all checked conditions hold", fill=(255, 255, 255), font=font(15, True))
    return np.array(canvas)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", choices=["square", "tool_hang"], required=True)
    ap.add_argument("--case", choices=["nominal", "drop", "miss"], default="nominal")
    ap.add_argument("--demo", required=True)
    ap.add_argument("--tag", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--size", type=int, default=512)
    a = ap.parse_args()
    domain = convert.TASKS[a.task]["domain"]
    Config = lamp_env.declare(domain)
    import eval_durative as ED
    lab = ED.Labeller(Config)
    tol = load_tolerances(domain, a.tag)
    path = os.path.join(os.path.expanduser("~/lamp_work/datasets/robomimic"), convert.TASKS[a.task]["file"])
    with h5py.File(path, "r") as f:
        if a.case == "nominal":
            # recorded human demo, rendered by restoring each recorded simulator state
            from rollout_video import make_env, restore
            g = f["data"][a.demo]
            env = make_env(f)
            frames = []
            for i, st_ in enumerate(g["states"][:]):
                if i == 0:
                    restore(env, g.attrs["model_file"], st_)
                else:
                    env.sim.set_state_from_flattened(st_)
                    env.sim.forward()
                frames.append(env.sim.render(height=a.size, width=a.size, camera_name="agentview")[::-1])
            d = ED.demo_from_hdf5(f, a.demo, a.task)
            success = True
        else:
            rec, frames, success, xml, _ = rollout(f, a.demo, a.case, 1.0, 12, "agentview", a.size)
            d = convert.build_demo(a.task, rec["object"], rec["eef_pos"], rec["eef_quat"], rec["gq"], rec["cmd"], xml, True)
            d["cmd"] = rec["cmd"]
    run = ED.make_run(a.task, domain, d, lab, 1)
    run["Config"] = Config
    violations = DUR.check(domain, run, tol)
    names = sorted(n for n in run["states"][0].object_dict if n.split("_")[0] not in Config.NON_RELATION_OBJECTS)
    names.sort(key=lambda n: n.split("_")[0] not in Config.ROBOT_TYPES)
    pairs = [(p, q) for i, p in enumerate(names) for q in names[i + 1:]]
    T = min(len(frames), len(run["states"]))
    title = "{} | {} | task success: {}".format(domain, a.case.upper(), "yes" if success else "NO")
    sub = "held-out {} | stage-aware durative monitor on LAMP regions ({})".format(a.demo, a.tag)
    import imageio
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    with imageio.get_writer(a.out, fps=20, codec="libx264", quality=7, macro_block_size=2) as w:
        for t in range(T):
            w.append_data(draw(frames[t], t, T, domain, run, pairs, violations, title, sub))
    alarm_t = min([v["frame"] for v in violations], default=None)
    Image.fromarray(draw(frames[T - 1], T - 1, T, domain, run, pairs, violations, title, sub)).save(a.out[:-4] + "_last.png")
    if alarm_t is not None:
        Image.fromarray(draw(frames[min(alarm_t, T - 1)], min(alarm_t, T - 1), T, domain, run, pairs, violations,
                             title, sub)).save(a.out[:-4] + "_alarm.png")
    print(json.dumps({"demo": a.demo, "case": a.case, "success": bool(success), "alarm_frame": alarm_t,
                      "violations": [(v["stage"], v["kind"], v["pred"], v["frame"]) for v in violations]}))
