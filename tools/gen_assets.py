# -*- coding: utf-8 -*-
"""
Genera tutti gli asset PNG della watch face Bip 6, allineati al mockup approvato.
Output in ../assets/bip-6/.
"""
import os
from PIL import Image, ImageDraw
import dotfont as F
import icons as IC
import weather12 as W12

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

    # --- Giorno settimana multilingua (micro-pixel, bianco) ---
    # indice = valore hmSetting.getLanguage(); abbreviazioni LUN..DOM (ASCII).
    # Solo lingue ad alfabeto latino; le altre useranno il fallback EN (idx 2).
    DOW_LANGS = {
        2:  ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"],  # en
        3:  ["LUN", "MAR", "MIE", "JUE", "VIE", "SAB", "DOM"],  # es
        6:  ["LUN", "MAR", "MER", "JEU", "VEN", "SAM", "DIM"],  # fr
        7:  ["MON", "DIE", "MIT", "DON", "FRE", "SAM", "SON"],  # de
        8:  ["SEN", "SEL", "RAB", "KAM", "JUM", "SAB", "MIN"],  # id
        9:  ["PON", "WTO", "SRO", "CZW", "PIA", "SOB", "NIE"],  # pl
        10: ["LUN", "MAR", "MER", "GIO", "VEN", "SAB", "DOM"],  # it
        14: ["T2", "T3", "T4", "T5", "T6", "T7", "CN"],         # vi
        15: ["SEG", "TER", "QUA", "QUI", "SEX", "SAB", "DOM"],  # pt
        16: ["MA", "DI", "WO", "DO", "VR", "ZA", "ZO"],         # nl
        17: ["PZT", "SAL", "CAR", "PER", "CUM", "CMT", "PAZ"],  # tr
        21: ["LUN", "MAR", "MIE", "JOI", "VIN", "SAM", "DUM"],  # ro
        22: ["PO", "UT", "ST", "CT", "PA", "SO", "NE"],         # cs
        25: ["DL", "DT", "DC", "DJ", "DV", "DS", "DG"],         # ca
        26: ["MA", "TI", "KE", "TO", "PE", "LA", "SU"],         # fi
        27: ["MAN", "TIR", "ONS", "TOR", "FRE", "LOR", "SON"],  # nb
        28: ["MAN", "TIR", "ONS", "TOR", "FRE", "LOR", "SON"],  # da
        29: ["MAN", "TIS", "ONS", "TOR", "FRE", "LOR", "SON"],  # sv
        30: ["HET", "KED", "SZE", "CSU", "PEN", "SZO", "VAS"],  # hu
        31: ["ISN", "SEL", "RAB", "KHA", "JUM", "SAB", "AHD"],  # ms
        32: ["PO", "UT", "ST", "ST", "PI", "SO", "NE"],         # sk
    }
    DOW_CW = 72  # canvas fisso, testo allineato a destra (gap costante col giorno mese)
    DOW_CH = F.GLYPH_H * P_DOW
    for idx, days in DOW_LANGS.items():
        pl = ensure(os.path.join(ASSETS, "dow", str(idx)))
        for di, name in enumerate(days):
            img = Image.new("RGBA", (DOW_CW, DOW_CH), (0, 0, 0, 0))
            d = ImageDraw.Draw(img)
            tw = F.text_size(name, P_DOW)[0]
            F.draw_text(d, name, DOW_CW - tw, 0, P_DOW, WHITE, radius_ratio=0.46)
            img.save(os.path.join(pl, f"{di}.png"))

    # --- Icone (grigie su pill scure, bianca per il cuore) ---
    p = ensure(os.path.join(ASSETS, "icon"))
    save_icon(IC.RUNNER,  ICONG, os.path.join(p, "runner.png"))
    save_icon(IC.CLOUD,   ICONG, os.path.join(p, "cloud.png"))
    save_icon(IC.SUNRISE, ICONG, os.path.join(p, "sunrise.png"))
    save_icon(IC.HEART,   WHITE, os.path.join(p, "heart.png"))
    # icone meteo dinamiche: set CURATO 12 (weather12.ICONS) -> icon/w_<key>.png
    for key, bmp in W12.ICONS.items():
        save_icon(bmp, ICONG, os.path.join(p, f"w_{key}.png"))

    # linea orizzontale di pixel (separatore ore/minuti, variante verticale)
    line_pitch = 9
    line_bmp = ["X" * 11]
    lw, lh = F.bitmap_size(line_bmp, line_pitch)
    img = Image.new("RGBA", (lw, lh), (0, 0, 0, 0))
    F.draw_bitmap(ImageDraw.Draw(img), line_bmp, 0, 0, line_pitch, WHITE)
    img.save(os.path.join(ASSETS, "sep_line.png"))

    # --- Separatore ora ":" = due punti da 4 micro-pixel (quadrato 2x2) ---
    mp = 7
    dot = ["XX", "XX"]
    sw = mp * 2
    img = Image.new("RGBA", (sw, sw * 3), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    F.draw_bitmap(d, dot, 0, 0, mp, WHITE)
    F.draw_bitmap(d, dot, 0, sw * 2, mp, WHITE)
    img.save(os.path.join(ASSETS, "sep_colon.png"))

    # --- Separatore verticale ore/minuti: DUE punti da 4 pixel (quadrato 2x2) affiancati ---
    dp = 9
    two = ["XX...XX", "XX...XX"]
    dw, dh = F.bitmap_size(two, dp)
    img = Image.new("RGBA", (dw, dh), (0, 0, 0, 0))
    F.draw_bitmap(ImageDraw.Draw(img), two, 0, 0, dp, WHITE)
    img.save(os.path.join(ASSETS, "sep_dots.png"))

    # --- Pallini equalizer (agganciato al battito): grigio + rosso (cappello barra) ---
    def save_eqdot(color, path, box=15, rr=0.42):
        img = Image.new("RGBA", (box, box), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        r = box * rr
        cx = cy = box / 2
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)
        img.save(path)
    save_eqdot(GREY, os.path.join(ASSETS, "eq_g.png"))
    save_eqdot(RED,  os.path.join(ASSETS, "eq_r.png"))

    # --- preview ---
    p = ensure(os.path.join(ASSETS, "images"))
    mk = os.path.join(os.path.dirname(__file__), "..", "mockup.png")
    if os.path.exists(mk):
        Image.open(mk).convert("RGB").resize((266, 307)).save(os.path.join(p, "preview.png"))

    total = sum(len(files) for _, _, files in os.walk(ASSETS))
    print(f"Asset generati: {total} file in {ASSETS}")


if __name__ == "__main__":
    main()
