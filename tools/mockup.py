# -*- coding: utf-8 -*-
"""
Compone un mockup 390x450 della watch face Bip 6 (stile Nothing dot-matrix),
cosi' si vede il design senza simulatore. Valori d'esempio dalla foto di Marco.
"""
import os
from PIL import Image, ImageDraw
import dotfont as F
import icons as IC

W, H = 390, 450

# Palette Nothing
BLACK   = (0, 0, 0)
WHITE   = (242, 242, 242)
RED      = (226, 48, 45)
PILL_BG  = (26, 26, 28)
GREEN    = (48, 199, 90)
ICON     = (200, 200, 200)

# Valori d'esempio (saranno dinamici nel codice Zepp OS)
HH, MM   = "11", "14"
DOW, DAY = "MER", "10"
STEPS    = "2616"
TEMP     = "27"
SUNRISE  = "05:34"
HR       = "84"
NOTIF    = "3"


def draw_icon(d, bitmap, cx, cy, pitch, col):
    """Disegna un'icona pixel-art centrata in (cx, cy)."""
    w, h = F.bitmap_size(bitmap, pitch)
    F.draw_bitmap(d, bitmap, cx - w/2, cy - h/2, pitch, col)


def pill(d, x, y, w, h, bg):
    d.rounded_rectangle([x, y, x + w, y + h], radius=int(h*0.32), fill=bg)


def main():
    img = Image.new("RGB", (W, H), BLACK)
    d = ImageDraw.Draw(img)

    # --- ORA: "11" bianco + "14" rosso, una riga ---
    pitch = 12
    hh_w = F.text_size(HH, pitch)[0]
    sp   = F.text_size(" ", pitch)[0] + pitch  # spazio largo tra HH e MM
    mm_w = F.text_size(MM, pitch)[0]
    total = hh_w + sp + mm_w
    x0 = (W - total) // 2
    y_clock = 52
    F.draw_text(d, HH, x0, y_clock, pitch, WHITE)
    F.draw_text(d, MM, x0 + hh_w + sp, y_clock, pitch, RED)

    # (Notifiche: gestite dall'overlay di sistema dell'orologio, non disegnate qui)

    # --- DATA: "MER" bianco + "10" rosso, allineata a destra sotto l'ora ---
    dp = 6
    dow_w = F.text_size(DOW, dp)[0]
    gap   = F.text_size(" ", dp)[0]
    day_w = F.text_size(DAY, dp)[0]
    right = x0 + total
    y_date = y_clock + F.text_size(HH, pitch)[1] + 16
    dx = right - (dow_w + gap + day_w)
    F.draw_text(d, DOW, dx, y_date, dp, WHITE)
    F.draw_text(d, DAY, dx + dow_w + gap, y_date, dp, RED)

    # --- GRIGLIA 2x2 di pill ---
    mx, gx, gy = 15, 12, 14
    pw = (W - 2*mx - gx) // 2
    ph = 84
    y1 = 215
    y2 = y1 + ph + gy
    col_l, col_r = mx, mx + pw + gx

    def fill_pill(px, py, bitmap, value, bg, txt):
        pill(d, px, py, pw, ph, bg)
        icy = py + ph/2
        icx = px + 28
        draw_icon(d, bitmap, icx, icy, 3, WHITE if bg != PILL_BG else ICON)
        # pitch del valore in base alla lunghezza, cosi' non trabocca dalla pill
        vlen = len(value.replace(chr(176), ""))
        vp = 6 if vlen <= 3 else (5 if vlen == 4 else 4)
        vh = F.text_size(value, vp)[1]
        F.draw_text(d, value, px + 52, icy - vh/2, vp, txt)

    fill_pill(col_l, y1, IC.RUNNER,  STEPS,   PILL_BG, WHITE)
    fill_pill(col_r, y1, IC.CLOUD,   TEMP,    PILL_BG, WHITE)
    fill_pill(col_l, y2, IC.SUNRISE, SUNRISE, PILL_BG, WHITE)
    fill_pill(col_r, y2, IC.HEART,   HR,      RED,     WHITE)

    # grado "°" disegnato a mano (cerchietto) accanto alla temperatura
    tp = 6
    tw = F.text_size(TEMP, tp)[0]
    deg_x = col_r + 52 + tw + 5
    deg_y = y1 + ph/2 - F.text_size(TEMP, tp)[1]/2 + 2
    d.ellipse([deg_x, deg_y, deg_x + 7, deg_y + 7], outline=WHITE, width=2)

    out = os.path.join(os.path.dirname(__file__), "..", "mockup.png")
    img.save(out)
    print("Mockup salvato:", os.path.abspath(out))


if __name__ == "__main__":
    main()
