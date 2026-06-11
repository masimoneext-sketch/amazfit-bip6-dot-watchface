# -*- coding: utf-8 -*-
"""
GIF del mockup VERTICALE attuale (Bip 6): ore/minuti + separatore due punti,
data, 4 pill a destra, e l'EQUALIZER agganciato al battito che si anima.
Coordinate allineate a watchface/bip-6/index.js. BPM d'esempio = 84.
Output: tools/out/mockup_v_anim.gif
"""
import os, math
from PIL import Image, ImageDraw
import dotfont as F
import weather12 as W12

W, H = 390, 450
BLACK = (0, 0, 0)
WHITE = (242, 242, 242)
RED   = (226, 48, 45)
PILL_BG = (26, 26, 28)
ICON  = (200, 200, 200)
GREY  = (150, 156, 150)

BPM = 84
NF = 28


def draw_icon(d, bitmap, cx, cy, pitch, col):
    w, h = F.bitmap_size(bitmap, pitch)
    F.draw_bitmap(d, bitmap, cx - w / 2, cy - h / 2, pitch, col)


def base_face():
    """Parte statica: ore/minuti/separatore/data/pill."""
    img = Image.new("RGB", (W, H), BLACK)
    d = ImageDraw.Draw(img)
    left_cx = 95
    pb = 12  # pitch cifre grandi

    # ore (bianche) y~72, minuti (rossi) y~208
    hh, mm = "11", "14"
    hw = F.text_size(hh, pb)[0]; mw = F.text_size(mm, pb)[0]
    F.draw_text(d, hh, left_cx - hw / 2, 34, pb, WHITE)
    F.draw_text(d, mm, left_cx - mw / 2, 170, pb, RED)

    # separatore: due punti 2x2 (pitch 9) centrati
    dp = 9
    two = ["XX...XX", "XX...XX"]
    tw = F.bitmap_size(two, dp)[0]
    F.draw_bitmap(d, two, left_cx - tw / 2, 138, dp, WHITE)

    # data: DOW (micro) + giorno mese (rosso)
    F.draw_text(d, "GIO", 24, 318, 4, WHITE, radius_ratio=0.46)
    F.draw_text(d, "11", 112, 300, 6, RED)

    # 4 pill a destra
    PX, PW, PH = 202, 170, 82
    rowY = [34, 126, 218, 310]
    pills = [
        (W12.ICONS["sun"] and None, "runner", "2616", PILL_BG, GREY),  # placeholder
    ]
    def pill(row, key_icon, value, bg, txt, icon_bmp):
        py = rowY[row]
        d.rounded_rectangle([PX, py, PX + PW, py + PH], radius=int(PH * 0.32), fill=bg)
        icy = py + PH / 2
        draw_icon(d, icon_bmp, PX + 28, icy, 3, WHITE if bg != PILL_BG else ICON)
        vh = F.text_size(value, 3)[1]
        F.draw_text(d, value, PX + 66, icy - vh / 2, 3, txt)

    # icone pill: passi(runner), meteo(nuvola), alba(mezzo sole), battito(cuore)
    import icons as IC
    pill(0, "steps", "2616",  PILL_BG, GREY, IC.RUNNER)
    pill(1, "weath", "19",    PILL_BG, GREY, W12.ICONS["cloud"])
    pill(2, "sun",   "05:34", PILL_BG, GREY, IC.SUNRISE)
    pill(3, "hr",    str(BPM), RED,    WHITE, IC.HEART)
    # grado meteo
    tw2 = F.text_size("19", 3)[0]
    d.ellipse([PX + 66 + tw2 + 4, icy_w(rowY) , PX + 66 + tw2 + 9, icy_w(rowY) + 5], outline=GREY, width=1)
    return img


def icy_w(rowY):
    return rowY[1] + 82 / 2 - 3


def draw_eq(d, frame):
    EQ_X, EQ_BASE, EQ_BX, EQ_DY, EQ_BARS, EQ_MAXH = 24, 430, 21, 17, 8, 5
    lvl = max(0.0, min(1.0, (BPM - 50) / 100.0))
    energy = 0.2 + 0.8 * lvl
    speed = 0.18 + 0.5 * lvl
    box = 15; r = box * 0.42; off = box / 2
    for i in range(EQ_BARS):
        wave = 0.5 + 0.5 * math.sin(frame * speed + i * 0.8)
        h = 1 + round((EQ_MAXH - 1) * energy * wave)
        h = max(1, min(EQ_MAXH, h))
        for k in range(h):
            cx = EQ_X + i * EQ_BX + off
            cy = EQ_BASE - k * EQ_DY + off
            col = RED if k == h - 1 else GREY
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)


def main():
    base = base_face()
    frames = []
    for f in range(NF):
        img = base.copy()
        draw_eq(ImageDraw.Draw(img), f)
        frames.append(img)
    out_dir = os.path.join(os.path.dirname(__file__), "out")
    os.makedirs(out_dir, exist_ok=True)
    gif = os.path.join(out_dir, "mockup_v_anim.gif")
    frames[0].save(gif, save_all=True, append_images=frames[1:], duration=120, loop=0)
    frames[6].save(os.path.join(out_dir, "mockup_v_anim_frame.png"))
    print("OK", gif)


if __name__ == "__main__":
    main()
