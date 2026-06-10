# -*- coding: utf-8 -*-
"""
Genera icone pixel-art DEFINITE: disegna una forma vettoriale liscia ad alta
risoluzione e la campiona su una griglia fine di punti. Piu' celle = piu'
definizione, mantenendo lo stile a puntini.
"""
import math
from PIL import Image, ImageDraw


def pixelize(shape_fn, gw, gh, ss=10, threshold=128):
    """Disegna shape_fn su canvas (gw*ss, gh*ss) e campiona ogni cella al centro."""
    W, H = gw * ss, gh * ss
    img = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(img)
    shape_fn(d, W, H)
    rows = []
    for r in range(gh):
        line = ""
        for c in range(gw):
            cx = int((c + 0.5) * ss)
            cy = int((r + 0.5) * ss)
            line += "X" if img.getpixel((cx, cy)) > threshold else "."
        rows.append(line)
    return rows


# ---- forme vettoriali (disegnate bianche su canvas WxH) ----

def _heart(d, W, H):
    pts = []
    for i in range(0, 360, 4):
        t = math.radians(i)
        x = 16 * (math.sin(t) ** 3)
        y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
        px = W * 0.5 + x * (W * 0.030)
        py = H * 0.46 - y * (H * 0.034)
        pts.append((px, py))
    d.polygon(pts, fill=255)


def _sun_half(d, W, H):
    cx, cy = W * 0.5, H * 0.66
    R = min(W, H) * 0.30
    d.pieslice([cx - R, cy - R, cx + R, cy + R], 180, 360, fill=255)
    lw = max(2, int(min(W, H) * 0.085))
    r_in, r_out = R * 1.22, R * 1.92
    for ang in (180, 135, 90, 45, 0):
        a = math.radians(ang)
        x1, y1 = cx + r_in * math.cos(a), cy - r_in * math.sin(a)
        x2, y2 = cx + r_out * math.cos(a), cy - r_out * math.sin(a)
        d.line([(x1, y1), (x2, y2)], fill=255, width=lw)


def _cloud(d, W, H):
    d.ellipse([W * 0.04, H * 0.42, W * 0.46, H * 0.86], fill=255)
    d.ellipse([W * 0.24, H * 0.20, W * 0.66, H * 0.74], fill=255)
    d.ellipse([W * 0.50, H * 0.38, W * 0.94, H * 0.84], fill=255)
    d.rectangle([W * 0.18, H * 0.60, W * 0.82, H * 0.85], fill=255)


def _runner(d, W, H):
    lw = max(2, int(W * 0.10))
    d.ellipse([W * 0.42, H * 0.06, W * 0.66, H * 0.26], fill=255)      # testa
    d.line([(W * 0.54, H * 0.26), (W * 0.58, H * 0.54)], fill=255, width=lw)  # busto
    d.line([(W * 0.58, H * 0.54), (W * 0.34, H * 0.74)], fill=255, width=lw)  # gamba dietro
    d.line([(W * 0.58, H * 0.54), (W * 0.78, H * 0.82)], fill=255, width=lw)  # gamba avanti
    d.line([(W * 0.34, H * 0.74), (W * 0.20, H * 0.70)], fill=255, width=lw)  # piede dietro
    d.line([(W * 0.56, H * 0.34), (W * 0.30, H * 0.40)], fill=255, width=lw)  # braccio dietro
    d.line([(W * 0.56, H * 0.34), (W * 0.80, H * 0.26)], fill=255, width=lw)  # braccio avanti


# bitmap pronte (griglie fini)
HEART   = pixelize(_heart, 20, 18)
SUNRISE = pixelize(_sun_half, 22, 16)
CLOUD   = pixelize(_cloud, 22, 15)
RUNNER  = pixelize(_runner, 16, 20)


if __name__ == "__main__":
    for name in ("HEART", "SUNRISE", "CLOUD", "RUNNER"):
        print("===", name, "===")
        for row in globals()[name]:
            print(row.replace(".", " ").replace("X", "#"))
