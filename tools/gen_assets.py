# -*- coding: utf-8 -*-
"""
Genera tutti gli asset PNG della watch face Bip 6, allineati al mockup approvato.
Output in ../assets/bip-6/.
"""
import os
from PIL import Image, ImageDraw
import dotfont as F
import icons as IC

ASSETS = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "assets", "bip-6"))

WHITE = (242, 242, 242, 255)
RED   = (226, 48, 45, 255)
GREY  = (150, 156, 150, 255)   # valori pill (LCD Casio)
ICONG = (200, 200, 200, 255)   # icone su pill scure

# pitch per famiglia
P_BIG  = 12   # ore/minuti
P_DAY  = 6    # giorno del mese (rosso)
P_HR   = 6    # battito (bianco, grande)
P_TINY = 3    # valori pill: passi/meteo/alba (grigi, piccoli)
P_DOW  = 4    # giorno settimana (micro-pixel)
P_ICON = 3    # icone pill
ICON_CANVAS = 42  # canvas quadrato fisso per centrare le icone


def ensure(path):
    os.makedirs(path, exist_ok=True)
    return path


def save_glyph(ch, pitch, color, path, radius_ratio=0.54):
    w = F.GLYPH_W * pitch
    h = F.GLYPH_H * pitch
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    F.draw_text(d, ch, 0, 0, pitch, color, radius_ratio=radius_ratio)
    img.save(path)


def save_text(text, pitch, color, path, radius_ratio=0.54):
    w, h = F.text_size(text, pitch)
    img = Image.new("RGBA", (int(w), int(h)), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    F.draw_text(d, text, 0, 0, pitch, color, radius_ratio=radius_ratio)
    img.save(path)


def save_icon(bitmap, color, path):
    """Icona centrata in un canvas quadrato fisso, cosi' si posiziona uguale per tutte."""
    img = Image.new("RGBA", (ICON_CANVAS, ICON_CANVAS), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    bw, bh = F.bitmap_size(bitmap, P_ICON)
    x = (ICON_CANVAS - bw) / 2
    y = (ICON_CANVAS - bh) / 2
    F.draw_bitmap(d, bitmap, x, y, P_ICON, color)
    img.save(path)


def save_deg(pitch, color, path):
    img = Image.new("RGBA", (pitch * 3, pitch * 3), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    r = pitch * 3 - 2
    d.ellipse([1, 1, r, r], outline=color, width=max(1, pitch // 3))
    img.save(path)


def main():
    # --- Ore/minuti grandi ---
    for fam, col in (("num_big_w", WHITE), ("num_big_r", RED)):
        p = ensure(os.path.join(ASSETS, fam))
        for n in range(10):
            save_glyph(str(n), P_BIG, col, os.path.join(p, f"{n}.png"))

    # --- Giorno mese (rosso, medio) ---
    p = ensure(os.path.join(ASSETS, "num_sm_r"))
    for n in range(10):
        save_glyph(str(n), P_DAY, RED, os.path.join(p, f"{n}.png"))

    # --- Battito (bianco, grande) ---
    p = ensure(os.path.join(ASSETS, "num_hr_w"))
    for n in range(10):
        save_glyph(str(n), P_HR, WHITE, os.path.join(p, f"{n}.png"))

    # --- Valori pill grigi piccoli (passi/meteo/alba) + colon + grado ---
    p = ensure(os.path.join(ASSETS, "num_tiny_g"))
    for n in range(10):
        save_glyph(str(n), P_TINY, GREY, os.path.join(p, f"{n}.png"))
    save_glyph(":", P_TINY, GREY, os.path.join(p, "colon.png"))
    save_deg(P_TINY, GREY, os.path.join(p, "deg.png"))

    # --- Giorno settimana IT, micro-pixel (bianco) ---
    p = ensure(os.path.join(ASSETS, "dow"))
    for name in ("LUN", "MAR", "MER", "GIO", "VEN", "SAB", "DOM"):
        save_text(name, P_DOW, WHITE, os.path.join(p, f"{name}.png"), radius_ratio=0.46)

    # --- Icone (grigie su pill scure, bianca per il cuore) ---
    p = ensure(os.path.join(ASSETS, "icon"))
    save_icon(IC.RUNNER,  ICONG, os.path.join(p, "runner.png"))
    save_icon(IC.CLOUD,   ICONG, os.path.join(p, "cloud.png"))
    save_icon(IC.SUNRISE, ICONG, os.path.join(p, "sunrise.png"))
    save_icon(IC.HEART,   WHITE, os.path.join(p, "heart.png"))

    # --- Separatore ora ":" = due punti da 4 micro-pixel (quadrato 2x2) ---
    mp = 7
    dot = ["XX", "XX"]
    sw = mp * 2
    img = Image.new("RGBA", (sw, sw * 3), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    F.draw_bitmap(d, dot, 0, 0, mp, WHITE)
    F.draw_bitmap(d, dot, 0, sw * 2, mp, WHITE)
    img.save(os.path.join(ASSETS, "sep_colon.png"))

    # --- preview ---
    p = ensure(os.path.join(ASSETS, "images"))
    mk = os.path.join(os.path.dirname(__file__), "..", "mockup.png")
    if os.path.exists(mk):
        Image.open(mk).convert("RGB").resize((266, 307)).save(os.path.join(p, "preview.png"))

    total = sum(len(files) for _, _, files in os.walk(ASSETS))
    print(f"Asset generati: {total} file in {ASSETS}")


if __name__ == "__main__":
    main()
