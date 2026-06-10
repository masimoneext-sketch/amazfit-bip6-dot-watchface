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
GREY     = (150, 156, 150)  # grigio LCD tipo Casio per i valori delle pill

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

    # separatore ":" — due punti da 4 micro-pixel (quadrato 2x2)
    sep_cx = x0 + hh_w + sp / 2
    mp = 7
    dot = ["XX", "XX"]
    F.draw_bitmap(d, dot, sep_cx - mp, y_clock + 20, mp, WHITE)
    F.draw_bitmap(d, dot, sep_cx - mp, y_clock + 50, mp, WHITE)

    # (Notifiche: gestite dall'overlay di sistema dell'orologio, non disegnate qui)

    # --- DATA: "MER" (micro-pixel) bianco + "10" rosso, allineata a destra ---
    dp = 6           # giorno mese
    dp_dow = 4       # giorno settimana in micro-pixel
    dow_w = F.text_size(DOW, dp_dow)[0]
    gap   = 10
    day_w = F.text_size(DAY, dp)[0]
    right = x0 + total
    y_date = y_clock + F.text_size(HH, pitch)[1] + 16
    dx = right - (dow_w + gap + day_w)
    day_h = F.text_size(DAY, dp)[1]
    dow_h = F.text_size(DOW, dp_dow)[1]
    F.draw_text(d, DOW, dx, y_date + (day_h - dow_h), dp_dow, WHITE, radius_ratio=0.46)
    F.draw_text(d, DAY, dx + dow_w + gap, y_date, dp, RED)

    # --- GRIGLIA 2x2 di pill ---
    mx, gx, gy = 15, 12, 14
    pw = (W - 2*mx - gx) // 2
    ph = 84
    y1 = 215
    y2 = y1 + ph + gy
    col_l, col_r = mx, mx + pw + gx

    def fill_pill(px, py, bitmap, value, bg, txt, vp_override=None):
        pill(d, px, py, pw, ph, bg)
        icy = py + ph/2
        icx = px + 26
        draw_icon(d, bitmap, icx, icy, 3, WHITE if bg != PILL_BG else ICON)
        # pitch del valore in base alla lunghezza, cosi' non trabocca dalla pill
        vlen = len(value.replace(chr(176), ""))
        vp = vp_override if vp_override else (6 if vlen <= 3 else (5 if vlen == 4 else 4))
        vh = F.text_size(value, vp)[1]
        F.draw_text(d, value, px + 64, icy - vh/2, vp, txt)

    fill_pill(col_l, y1, IC.RUNNER,  STEPS,   PILL_BG, GREY,  vp_override=3)
    fill_pill(col_r, y1, IC.CLOUD,   TEMP,    PILL_BG, GREY,  vp_override=3)
    fill_pill(col_l, y2, IC.SUNRISE, SUNRISE, PILL_BG, GREY,  vp_override=3)
    fill_pill(col_r, y2, IC.HEART,   HR,      RED,     WHITE)

    # grado "°" accanto alla temperatura (piccola, grigia)
    tp = 3
    tw = F.text_size(TEMP, tp)[0]
    deg_x = col_r + 64 + tw + 4
    deg_y = y1 + ph/2 - F.text_size(TEMP, tp)[1]/2
    d.ellipse([deg_x, deg_y, deg_x + 5, deg_y + 5], outline=GREY, width=1)

    out = os.path.join(os.path.dirname(__file__), "..", "mockup.png")
    img.save(out)
    print("Mockup salvato:", os.path.abspath(out))


if __name__ == "__main__":
    main()
