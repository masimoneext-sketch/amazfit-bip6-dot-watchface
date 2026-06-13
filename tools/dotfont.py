# -*- coding: utf-8 -*-
"""
Motore font dot-matrix stile Nothing per la watch face Bip 6.
Ogni glifo e' una bitmap 5x7 ('X' = punto acceso). Il render disegna
ogni punto come un cerchietto pieno, da cui il look LED/Nothing.
"""
from PIL import Image, ImageDraw

# ---- Glifi 5x7 ('X' acceso, '.' spento) ----------------------------------
GLYPHS = {
    "0": [".XXX.", "X...X", "X..XX", "X.X.X", "XX..X", "X...X", ".XXX."],
    "1": ["..X..", ".XX..", "..X..", "..X..", "..X..", "..X..", ".XXX."],
    "2": [".XXX.", "X...X", "....X", "...X.", "..X..", ".X...", "XXXXX"],
    "3": ["XXXXX", "...X.", "..XX.", "....X", "....X", "X...X", ".XXX."],
    "4": ["...X.", "..XX.", ".X.X.", "X..X.", "XXXXX", "...X.", "...X."],
    "5": ["XXXXX", "X....", "XXXX.", "....X", "....X", "X...X", ".XXX."],
    "6": ["..XX.", ".X...", "X....", "XXXX.", "X...X", "X...X", ".XXX."],
    "7": ["XXXXX", "....X", "...X.", "..X..", ".X...", ".X...", ".X..."],
    "8": [".XXX.", "X...X", "X...X", ".XXX.", "X...X", "X...X", ".XXX."],
    "9": [".XXX.", "X...X", "X...X", ".XXXX", "....X", "...X.", ".XX.."],
    "A": [".XXX.", "X...X", "X...X", "XXXXX", "X...X", "X...X", "X...X"],
    "B": ["XXXX.", "X...X", "X...X", "XXXX.", "X...X", "X...X", "XXXX."],
    "D": ["XXXX.", "X...X", "X...X", "X...X", "X...X", "X...X", "XXXX."],
    "E": ["XXXXX", "X....", "X....", "XXXX.", "X....", "X....", "XXXXX"],
    "G": [".XXX.", "X...X", "X....", "X.XXX", "X...X", "X...X", ".XXX."],
    "I": ["XXXXX", "..X..", "..X..", "..X..", "..X..", "..X..", "XXXXX"],
    "L": ["X....", "X....", "X....", "X....", "X....", "X....", "XXXXX"],
    "M": ["X...X", "XX.XX", "X.X.X", "X.X.X", "X...X", "X...X", "X...X"],
    "N": ["X...X", "XX..X", "X.X.X", "X.X.X", "X..XX", "X...X", "X...X"],
    "O": [".XXX.", "X...X", "X...X", "X...X", "X...X", "X...X", ".XXX."],
    "R": ["XXXX.", "X...X", "X...X", "XXXX.", "X.X..", "X..X.", "X...X"],
    "S": [".XXXX", "X....", "X....", ".XXX.", "....X", "....X", "XXXX."],
    "U": ["X...X", "X...X", "X...X", "X...X", "X...X", "X...X", ".XXX."],
    "V": ["X...X", "X...X", "X...X", "X...X", "X...X", ".X.X.", "..X.."],
    ":": [".....", "..X..", ".....", ".....", "..X..", ".....", "....."],
    "%": ["XX..X", "XX.X.", "...X.", "..X..", ".X...", "X..XX", "...XX"],
    " ": [".....", ".....", ".....", ".....", ".....", ".....", "....."],
}

GLYPH_W = 5
GLYPH_H = 7


def text_size(text, pitch, spacing=1):
    """Dimensione in px (w, h) di una stringa renderizzata."""
    n = len(text)
    w = n * GLYPH_W * pitch + (n - 1) * spacing * pitch
    h = GLYPH_H * pitch
    return int(w), int(h)


def draw_text(draw, text, x, y, pitch, color, spacing=1, radius_ratio=0.54):
    """
    Disegna `text` con angolo in alto-sinistra (x, y).
    pitch = passo tra i centri dei punti (px). radius_ratio = raggio/pitch.
    Ritorna la larghezza occupata.
    """
    r = max(1, pitch * radius_ratio)
    cx0 = x + pitch / 2
    cy0 = y + pitch / 2
    col = 0
    for ch in text.upper():
        g = GLYPHS.get(ch, GLYPHS[" "])
        for ry, row in enumerate(g):
            for rxi, cell in enumerate(row):
                if cell == "X":
                    cx = cx0 + (col + rxi) * pitch
                    cy = cy0 + ry * pitch
                    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)
        col += GLYPH_W + spacing
    w, _ = text_size(text, pitch, spacing)
    return w


def bitmap_size(rows, pitch):
    """Dimensione px (w, h) di una bitmap pixel-art renderizzata a punti."""
    h = len(rows)
    w = max(len(r) for r in rows) if rows else 0
    return int(w * pitch), int(h * pitch)


def draw_bitmap(draw, rows, x, y, pitch, color, radius_ratio=0.38):
    """
    Disegna una bitmap pixel-art arbitraria (lista di stringhe 'X'/'.') a punti,
    stesso stile del font. Usata per le icone delle pill e il fumetto notifiche.
    """
    r = max(1, pitch * radius_ratio)
    cx0 = x + pitch / 2
    cy0 = y + pitch / 2
    for ry, row in enumerate(rows):
        for rx, cell in enumerate(row):
            if cell == "X":
                cx = cx0 + rx * pitch
                cy = cy0 + ry * pitch
                draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)


def render_glyph_png(ch, pitch, color, path, radius_ratio=0.42, pad=2):
    """Genera il PNG di un singolo carattere su sfondo trasparente."""
    w = GLYPH_W * pitch + pad * 2
    h = GLYPH_H * pitch + pad * 2
    img = Image.new("RGBA", (int(w), int(h)), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    draw_text(d, ch, pad, pad, pitch, color, radius_ratio=radius_ratio)
    img.save(path)
    return img
