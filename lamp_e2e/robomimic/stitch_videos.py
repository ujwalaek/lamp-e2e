"""Concatenate the per-rollout videos into one overview video, with a short title card before each clip."""
import os
import sys

import imageio
import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rollout_video import font  # noqa: E402

VID = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "out", "videos")
CLIPS = [
    ("square_nominal", "Square, NOMINAL", "Human demo replayed in physics. The nut ends on the peg: nut -> peg turns green."),
    ("square_drop", "Square, DROP", "Gripper opens mid-carry. The 'holding' region (gripper -> nut) ends early; the nut never reaches the peg region."),
    ("square_miss", "Square, MISS", "Arm pushed sideways mid-carry. The nut is put down 15 cm away: nut -> peg stays red."),
    ("tool_hang_nominal", "Tool Hang, NOMINAL", "Frame inserted in the stand (frame -> stand green), then the wrench is hung on the hook."),
    ("tool_hang_drop", "Tool Hang, DROP", "Gripper opens while carrying the wrench. The wrench falls onto the base."),
    ("tool_hang_miss", "Tool Hang, MISS", "Arm pushed sideways while carrying the wrench. It knocks the frame round: frame -> stand turns red."),
]
FPS, CARD_S = 20, 2.5


def card(w, h, title, text):
    im = Image.new("RGB", (w, h), (250, 250, 250))
    d = ImageDraw.Draw(im)
    d.text((40, h // 2 - 50), title, fill=(30, 30, 30), font=font(34, True))
    d.text((40, h // 2 + 5), text, fill=(90, 90, 90), font=font(18))
    d.text((40, h - 40), "LAMP learned regions on held-out robomimic rollouts  |  green = in a learned region, "
           "red = outside, grey = none learned", fill=(130, 130, 130), font=font(14))
    return np.array(im)


def pad(fr, w, h):
    out = np.full((h, w, 3), 250, dtype=np.uint8)
    y, x = (h - fr.shape[0]) // 2, (w - fr.shape[1]) // 2
    out[y:y + fr.shape[0], x:x + fr.shape[1]] = fr
    return out


if __name__ == "__main__":
    readers = [(imageio.get_reader(os.path.join(VID, c + ".mp4")), t, s) for c, t, s in CLIPS]
    sizes = [r.get_meta_data()["size"] for r, _, _ in readers]
    W = max(s[0] for s in sizes); H = max(s[1] for s in sizes)
    W += W % 2; H += H % 2
    out = os.path.join(VID, "rollouts_overview.mp4")
    with imageio.get_writer(out, fps=FPS, codec="libx264", quality=7, macro_block_size=2) as w:
        for r, title, text in readers:
            c = card(W, H, title, text)
            for _ in range(int(CARD_S * FPS)):
                w.append_data(c)
            for fr in r:
                w.append_data(pad(fr, W, H))
    print("wrote", out)
