# -*- coding: utf-8 -*-
"""Variante 2 COLONNE: ore+minuti sovrapposti a sinistra, tutte le pill in colonna a destra."""
import os
from PIL import Image, ImageDraw
import dotfont as F
import icons as IC

W, H = 390, 450
BLACK = (0, 0, 0)
WHITE = (242, 242, 242)
RED   = (226, 48, 45)
PILL_BG = (26, 26, 28)
ICON  = (200, 200, 200)
GREY  = (150, 156, 150)

HH, MM   = "11", "14"
DOW, DAY = "MER", "10"
STEPS, TEMP, SUNRISE, HR = "2616", "27", "05:34", "84"


def draw_icon(d, bitmap, cx, cy, pitch, col):
    w, h = F.bitmap_size(bitmap, pitch)
    F.draw_bitmap(d, bitmap, cx - w / 2, cy - h / 2, pitch, col)


def main(weather_bmp=IC.CLOUD, suffix="", temp_val=TEMP):
    img = Image.new("RGB", (W, H), BLACK)
    d = ImageDraw.Draw(img)

    # ===== COLONNA SINISTRA: ore sopra minuti (sovrapposti) =====
    pitch = 11
    hh_w = F.text_size(HH, pitch)[0]
    mm_w = F.text_size(MM, pitch)[0]
    ch = F.text_size(HH, pitch)[1]
    left_cx = 95  # centro colonna sinistra
    y_hh = 74
    y_mm = y_hh + ch + 56  # ore e minuti, blocco piu' in basso
    F.draw_text(d, HH, left_cx - hh_w / 2, y_hh, pitch, WHITE)
    F.draw_text(d, MM, left_cx - mm_w / 2, y_mm, pitch, RED)

    # linea di pixel tra ore e minuti (centrata nel gap)
    line_pitch = 11
    line_bmp = ["X" * 11]
    lw = F.bitmap_size(line_bmp, line_pitch)[0]
    F.draw_bitmap(d, line_bmp, left_cx - lw / 2, y_hh + ch + 26, line_pitch, WHITE)

    # data sotto i minuti
    dp_dow, dp_day = 4, 6
    dow_w = F.text_size(DOW, dp_dow)[0]
    day_w = F.text_size(DAY, dp_day)[0]
    gap = 8
    tot = dow_w + gap + day_w
    dx = left_cx - tot / 2
    y_date = y_mm + ch + 16
    day_h = F.text_size(DAY, dp_day)[1]
    dow_h = F.text_size(DOW, dp_dow)[1]
    F.draw_text(d, DOW, dx, y_date + (day_h - dow_h), dp_dow, WHITE, radius_ratio=0.46)
    F.draw_text(d, DAY, dx + dow_w + gap, y_date, dp_day, RED)

    # ===== COLONNA DESTRA: 4 pill impilate =====
    px = 202
    pw = 170
    ph = 82
    gy = 10
    y0 = 34

    def fill_pill(row, bitmap, value, bg, txt, vp_override=None):
        py = y0 + row * (ph + gy)
        d.rounded_rectangle([px, py, px + pw, py + ph], radius=int(ph * 0.32), fill=bg)
        icy = py + ph / 2
        draw_icon(d, bitmap, px + 28, icy, 3, WHITE if bg != PILL_BG else ICON)
        vlen = len(value.replace(chr(176), ""))
        vp = vp_override if vp_override else (6 if vlen <= 3 else (5 if vlen == 4 else 4))
        vh = F.text_size(value, vp)[1]
        F.draw_text(d, value, px + 66, icy - vh / 2, vp, txt)
        return py

    fill_pill(0, IC.RUNNER,  STEPS,    PILL_BG, GREY,  vp_override=3)
    py_t = fill_pill(1, weather_bmp, temp_val, PILL_BG, GREY, vp_override=3)
    fill_pill(2, IC.SUNRISE, SUNRISE,  PILL_BG, GREY,  vp_override=3)
    fill_pill(3, IC.HEART,   HR,       RED,     WHITE)

    # grado meteo
    tw = F.text_size(temp_val, 3)[0]
    dxg = px + 66 + tw + 4
    dyg = py_t + ph / 2 - F.text_size(TEMP, 3)[1] / 2
    d.ellipse([dxg, dyg, dxg + 5, dyg + 5], outline=GREY, width=1)

    out = os.path.join(os.path.dirname(__file__), "..", f"mockup_v{suffix}.png")
    img.save(out)
    print("salvato:", os.path.basename(out))


if __name__ == "__main__":
    conditions = [
        (IC.WSUN,   "-sole",      "27"),
        (IC.CLOUD,  "-nuvole",    "19"),
        (IC.WRAIN,  "-pioggia",   "14"),
        (IC.WSTORM, "-temporale", "16"),
        (IC.WSNOW,  "-neve",      "1"),
    ]
    for bmp, sfx, t in conditions:
        main(bmp, sfx, t)
