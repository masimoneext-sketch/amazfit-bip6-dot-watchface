# -*- coding: utf-8 -*-
"""
Mockup STATICO del quadrante verticale Bip 6 con la nuova PERCENTUALE BATTERIA
in MICRO PIXEL in alto a destra (es. 85%). Riusa il rendering di mockup_v_anim.
Output: tools/out/mockup_battery.png
"""
import os
from PIL import ImageDraw
import dotfont as F
from mockup_v_anim import base_face, draw_sep, draw_eq, WHITE, GREY

# glifo "%" 5x7 dot (non presente nel font: lo disegno a mano qui)
PCT = [
    "XX..X",
    "XX.X.",
    "...X.",
    "..X..",
    ".X...",
    "X..XX",
    "...XX",
]

BATT = "85"          # valore d'esempio
PITCH = 2            # micro pixel
COL = WHITE          # bianco come l'ora


def draw_battery(d, pct_text, where="under_min"):
    num_w = F.text_size(pct_text, PITCH)[0]
    sym_w = F.bitmap_size(PCT, PITCH)[0]
    gap = 3
    total = num_w + gap + sym_w
    if where == "top_right":
        right = 372; x = right - total; y = 12
    else:  # under_min: centrata sotto i minuti (cifre centrate a x=95), nella
           # fascia libera tra la base dei minuti (~254) e la data (~300)
        left_cx = 95; x = left_cx - total / 2; y = 268
    F.draw_text(d, pct_text, x, y, PITCH, COL, radius_ratio=0.46)
    F.draw_bitmap(d, PCT, x + num_w + gap, y, PITCH, COL, radius_ratio=0.46)


def main():
    out_dir = os.path.join(os.path.dirname(__file__), "out")
    os.makedirs(out_dir, exist_ok=True)
    for where, fname in [("under_min", "mockup_battery_undermin.png"),
                         ("top_right", "mockup_battery.png")]:
        img = base_face()
        d = ImageDraw.Draw(img)
        draw_sep(d, 8)
        draw_eq(d, 8)
        draw_battery(d, BATT, where)
        out = os.path.join(out_dir, fname)
        img.save(out)
        print("OK", out)


if __name__ == "__main__":
    main()
