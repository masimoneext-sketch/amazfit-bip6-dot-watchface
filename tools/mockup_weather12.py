# -*- coding: utf-8 -*-
"""
Mockup di revisione: set CURATO di 12 icone meteo + legenda del mapping
dei 29 stati Huami. Icone grandi (vicine alla resa reale sul polso).
Output: tools/out/weather12.png
"""
import os
from PIL import Image, ImageDraw, ImageFont
import dotfont as F
from weather12 import ICONS, ICON_LABEL, MAP, HUAMI_NAME

BLACK = (0, 0, 0)
WHITE = (242, 242, 242)
GREY  = (150, 156, 150)
DIM   = (120, 124, 120)

ORDER = ["sun", "moon", "cloud", "overcast", "rain", "snow",
         "sleet", "storm", "hail", "fog", "sand", "unknown"]

COLS = 4
CELL_W, CELL_H = 180, 150
PAD_TOP = 60
GRID_H = PAD_TOP + 3 * CELL_H
LEG_W = 360
W = COLS * CELL_W + LEG_W
H = GRID_H + 20
PITCH = 9  # icone grandi


def font(sz):
    for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",):
        if os.path.exists(p):
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()


def main():
    img = Image.new("RGB", (W, H), BLACK)
    d = ImageDraw.Draw(img)
    f_title = font(26); f_name = font(17); f_leg = font(13); f_lh = font(15)

    d.text((20, 16), "Bip 6 — set curato 12 icone meteo", font=f_title, fill=WHITE)

    for i, key in enumerate(ORDER):
        r, c = divmod(i, COLS)
        x0 = c * CELL_W; y0 = PAD_TOP + r * CELL_H
        d.rounded_rectangle([x0 + 8, y0 + 6, x0 + CELL_W - 8, y0 + CELL_H - 8],
                            radius=12, outline=(36, 36, 38), width=1)
        bmp = ICONS[key]
        bw, bh = F.bitmap_size(bmp, PITCH)
        ix = x0 + (CELL_W - bw) / 2
        iy = y0 + 24 + (84 - bh) / 2
        F.draw_bitmap(d, bmp, ix, iy, PITCH, GREY)
        nm = ICON_LABEL[key]
        tw = d.textlength(nm, font=f_name)
        d.text((x0 + (CELL_W - tw) / 2, y0 + CELL_H - 34), nm, font=f_name, fill=WHITE)

    # legenda mapping 29 -> 12
    lx = COLS * CELL_W + 16
    d.text((lx, PAD_TOP - 4), "29 stati Huami -> icona", font=f_lh, fill=WHITE)
    ly = PAD_TOP + 22
    for idx in range(29):
        line = f"{idx:>2}  {HUAMI_NAME[idx]:<17} -> {ICON_LABEL[MAP[idx]]}"
        d.text((lx, ly), line, font=f_leg, fill=DIM)
        ly += 15

    out_dir = os.path.join(os.path.dirname(__file__), "out")
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, "weather12.png")
    img.save(out)
    print("OK", out, img.size)


if __name__ == "__main__":
    main()
