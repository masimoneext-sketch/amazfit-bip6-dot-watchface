# -*- coding: utf-8 -*-
"""
Mockup di revisione: tutte e 29 le icone meteo Huami in stile dot-matrix,
griglia 5x6 su sfondo nero (palette Nothing). Etichetta: indice + nome +
gruppo attuale (a quale delle 5 icone correnti e' oggi collassato).
Output: tools/out/weather29.png
"""
import os
from PIL import Image, ImageDraw, ImageFont
import dotfont as F
from weather29 import WEATHER

BLACK = (0, 0, 0)
WHITE = (242, 242, 242)
GREY  = (150, 156, 150)
DIM   = (110, 114, 110)
RED   = (226, 48, 45)

COLS, ROWS = 5, 6
CELL_W, CELL_H = 156, 132
PAD_TOP = 64
W = COLS * CELL_W
H = PAD_TOP + ROWS * CELL_H

PITCH = 6  # passo pallini icona nel mockup


def font(sz):
    for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"):
        if os.path.exists(p):
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()


def main():
    img = Image.new("RGB", (W, H), BLACK)
    d = ImageDraw.Draw(img)
    f_title = font(26)
    f_idx = font(20)
    f_name = font(15)
    f_grp = font(12)

    d.text((20, 18), "Bip 6 — 29 stati meteo Huami (dot-matrix)", font=f_title, fill=WHITE)

    for idx in range(29):
        name, grp, bmp = WEATHER[idx]
        r, c = divmod(idx, COLS)
        x0 = c * CELL_W
        y0 = PAD_TOP + r * CELL_H

        # cornice tenue
        d.rounded_rectangle([x0 + 6, y0 + 4, x0 + CELL_W - 6, y0 + CELL_H - 6],
                            radius=10, outline=(34, 34, 36), width=1)

        # indice in alto a sinistra (rosso = i 2 che restano 'sole', cosi' si notano)
        d.text((x0 + 14, y0 + 10), str(idx), font=f_idx, fill=WHITE)

        # icona dot centrata nella meta' alta della cella
        bw, bh = F.bitmap_size(bmp, PITCH)
        ix = x0 + (CELL_W - bw) / 2
        iy = y0 + 18 + (66 - bh) / 2
        F.draw_bitmap(d, bmp, ix, iy, PITCH, GREY)

        # nome + gruppo attuale in basso
        d.text((x0 + 14, y0 + CELL_H - 40), name, font=f_name, fill=WHITE)
        d.text((x0 + 14, y0 + CELL_H - 22), "ora: " + grp, font=f_grp, fill=DIM)

    out_dir = os.path.join(os.path.dirname(__file__), "out")
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, "weather29.png")
    img.save(out)
    print("OK", out, img.size)


if __name__ == "__main__":
    main()
