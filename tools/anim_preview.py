# -*- coding: utf-8 -*-
"""
Anteprima ANIMATA (GIF) di 3 idee di animazione pixel per la fascia
sotto giorno/data della watch face Bip 6. Stile Nothing dot-matrix.
Output: tools/out/anim_preview.gif + tools/out/anim_strip.png (keyframes).
"""
import os, math
from PIL import Image, ImageDraw, ImageFont

BLACK = (0, 0, 0)
WHITE = (235, 235, 235)
GREY  = (150, 156, 150)
DIM   = (70, 72, 70)
RED   = (226, 48, 45)
REDDIM = (110, 30, 28)

W, H = 390, 300
PITCH = 11
R = int(PITCH * 0.40)
NF = 24  # frame


def font(sz):
    p = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    return ImageFont.truetype(p, sz) if os.path.exists(p) else ImageFont.load_default()


def dot(d, cx, cy, col, r=R):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)


def kitt(d, x0, y, frame):
    """Scanner Larson/KITT: testa rossa che spazza avanti-indietro + scia."""
    n = 13
    tri = frame % (2 * (n - 1))
    head = tri if tri < n else 2 * (n - 1) - tri
    for i in range(n):
        cx = x0 + i * PITCH
        dist = abs(i - head)
        if dist == 0: col = RED
        elif dist == 1: col = REDDIM
        elif dist == 2: col = (60, 18, 16)
        else: col = DIM
        dot(d, cx, y, col)


def equalizer(d, x0, y_base, frame):
    """Barre VU che rimbalzano (vibe synthwave/Out Run)."""
    bars = [0, 2, 1, 3, 4, 2, 1, 3]
    maxh = 5
    for i, ph in enumerate(bars):
        h = int((maxh / 2) * (1 + math.sin((frame + ph * 3) * 0.5 + i)))
        h = max(1, min(maxh, h + 1))
        cx = x0 + i * PITCH
        for k in range(h):
            cy = y_base - k * PITCH
            col = RED if k == h - 1 else GREY
            dot(d, cx, cy, col)


# sprite runner 3 pose (gambe), 7x7
RUN = [
    [".XX....",
     ".XX....",
     "XXXX...",
     ".XX....",
     ".XX....",
     "X..X...",
     "X...X.."],
    [".XX....",
     ".XX....",
     "XXXX...",
     ".XX....",
     ".XX....",
     ".XX....",
     ".XX...."],
    [".XX....",
     ".XX....",
     "XXXX...",
     ".XX....",
     ".XX....",
     "X..X...",
     "..X..X."],
]


def runner(d, x0, y0, frame):
    pose = RUN[(frame // 3) % 3]
    bob = (frame // 3) % 2
    for r, row in enumerate(pose):
        for c, ch in enumerate(row):
            if ch == "X":
                dot(d, x0 + c * PITCH, y0 + (r + bob) * PITCH, GREY)


def render_frame(frame, f_lab):
    img = Image.new("RGB", (W, H), BLACK)
    d = ImageDraw.Draw(img)
    d.text((20, 10), "A — KITT scanner (arcade)", font=f_lab, fill=WHITE)
    kitt(d, 30, 56, frame)
    d.text((20, 100), "B — Equalizer (synthwave)", font=f_lab, fill=WHITE)
    equalizer(d, 30, 200, frame)
    d.text((20, 210), "C — Runner sprite (passi)", font=f_lab, fill=WHITE)
    runner(d, 30, 240, frame)
    return img


def main():
    f_lab = font(16)
    frames = [render_frame(i, f_lab) for i in range(NF)]
    out_dir = os.path.join(os.path.dirname(__file__), "out")
    os.makedirs(out_dir, exist_ok=True)
    gif = os.path.join(out_dir, "anim_preview.gif")
    frames[0].save(gif, save_all=True, append_images=frames[1:], duration=90, loop=0)
    # strip statica di 4 keyframe per verifica
    keys = [frames[i] for i in (0, 6, 12, 18)]
    strip = Image.new("RGB", (W, H * 4 + 12 * 3), (20, 20, 20))
    for i, fr in enumerate(keys):
        strip.paste(fr, (0, i * (H + 12)))
    strip.save(os.path.join(out_dir, "anim_strip.png"))
    print("OK", gif, "frames", NF)


if __name__ == "__main__":
    main()
