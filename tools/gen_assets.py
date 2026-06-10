# -*- coding: utf-8 -*-
"""
Genera tutti gli asset PNG della watch face Bip 6 dagli stessi glifi del mockup.
Output in ../assets/. Trasparenti, pronti per i widget Zepp OS (IMG_TIME, TEXT_IMG, IMG).
"""
import os
from PIL import Image, ImageDraw
import dotfont as F
import icons as IC

ASSETS = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "assets", "bip-6"))

WHITE = (242, 242, 242, 255)
RED   = (226, 48, 45, 255)
GREEN = (48, 199, 90, 255)

# pitch per famiglia di glifi
P_BIG = 12   # ore/minuti
P_SM  = 6    # data, giorno mese
P_XS  = 5    # valori dentro le pill (piu' compatti, ci sta anche 05:34)


def ensure(path):
    os.makedirs(path, exist_ok=True)
    return path


def save_glyph(ch, pitch, color, path):
    """Salva un glifo carattere come PNG trasparente, dimensione fissa per cifra."""
    w = F.GLYPH_W * pitch
    h = F.GLYPH_H * pitch
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    F.draw_text(d, ch, 0, 0, pitch, color)
    img.save(path)


def save_bitmap(bitmap, pitch, color, path):
    w, h = F.bitmap_size(bitmap, pitch)
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    F.draw_bitmap(d, bitmap, 0, 0, pitch, color)
    img.save(path)


def save_text(text, pitch, color, path):
    """Salva una stringa intera (es. 'LUN') come PNG."""
    w, h = F.text_size(text, pitch)
    img = Image.new("RGBA", (int(w), int(h)), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    F.draw_text(d, text, 0, 0, pitch, color)
    img.save(path)


def main():
    # --- Cifre grandi: ore (bianche) e minuti (rosse) per IMG_TIME ---
    for fam, col in (("num_big_w", WHITE), ("num_big_r", RED)):
        p = ensure(os.path.join(ASSETS, fam))
        for n in range(10):
            save_glyph(str(n), P_BIG, col, os.path.join(p, f"{n}.png"))

    # --- Cifre piccole: bianche (valori pill, ora alba) e rosse (giorno mese) ---
    for fam, col in (("num_sm_w", WHITE), ("num_sm_r", RED)):
        p = ensure(os.path.join(ASSETS, fam))
        for n in range(10):
            save_glyph(str(n), P_SM, col, os.path.join(p, f"{n}.png"))
        save_glyph(":", P_SM, col, os.path.join(p, "colon.png"))

    # grado "°" piccolo (cerchietto)
    p = ensure(os.path.join(ASSETS, "num_sm_w"))
    deg = Image.new("RGBA", (P_SM*2, P_SM*2), (0, 0, 0, 0))
    dd = ImageDraw.Draw(deg)
    dd.ellipse([1, 1, P_SM*2-2, P_SM*2-2], outline=WHITE, width=2)
    deg.save(os.path.join(p, "deg.png"))

    # --- Cifre extra-small per i valori dentro le pill (bianche) ---
    p = ensure(os.path.join(ASSETS, "num_xs_w"))
    for n in range(10):
        save_glyph(str(n), P_XS, WHITE, os.path.join(p, f"{n}.png"))
    save_glyph(":", P_XS, WHITE, os.path.join(p, "colon.png"))
    degx = Image.new("RGBA", (P_XS*2, P_XS*2), (0, 0, 0, 0))
    ddx = ImageDraw.Draw(degx)
    ddx.ellipse([1, 1, P_XS*2-2, P_XS*2-2], outline=WHITE, width=2)
    degx.save(os.path.join(p, "deg.png"))

    # --- Giorni settimana abbreviati IT (bianchi) ---
    p = ensure(os.path.join(ASSETS, "dow"))
    for name in ("LUN", "MAR", "MER", "GIO", "VEN", "SAB", "DOM"):
        save_text(name, P_SM, WHITE, os.path.join(p, f"{name}.png"))

    # --- Icone pill (bianche) + fumetto notifiche (verde) ---
    p = ensure(os.path.join(ASSETS, "icon"))
    save_bitmap(IC.RUNNER,  3, WHITE, os.path.join(p, "runner.png"))
    save_bitmap(IC.CLOUD,   3, WHITE, os.path.join(p, "cloud.png"))
    save_bitmap(IC.SUNRISE, 3, WHITE, os.path.join(p, "sunrise.png"))
    save_bitmap(IC.HEART,   3, WHITE, os.path.join(p, "heart.png"))
    save_bitmap(IC.BUBBLE,  3, GREEN, os.path.join(p, "bubble.png"))

    # --- preview/icon (dal mockup, ridimensionato a previewSize 266x307) ---
    p = ensure(os.path.join(ASSETS, "images"))
    mk = os.path.join(os.path.dirname(__file__), "..", "mockup.png")
    if os.path.exists(mk):
        prev = Image.open(mk).convert("RGB").resize((266, 307))
        prev.save(os.path.join(p, "preview.png"))

    # conteggio
    total = sum(len(files) for _, _, files in os.walk(ASSETS))
    print(f"Asset generati: {total} file in {ASSETS}")


if __name__ == "__main__":
    main()
