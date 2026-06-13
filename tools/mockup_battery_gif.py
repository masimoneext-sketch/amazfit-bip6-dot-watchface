# -*- coding: utf-8 -*-
"""
GIF animata del quadrante verticale CON la percentuale batteria (per la console
Zepp / store). Riusa base_face + equalizer animato + separatore lampeggiante e
sovrappone la batteria micro-pixel sotto i minuti.
Output: tools/out/bip6-vertical-batteria.gif
"""
import os
from PIL import ImageDraw
from mockup_v_anim import base_face, draw_sep, draw_eq, NF
from mockup_battery import draw_battery, BATT


def main():
    base = base_face()
    frames = []
    for f in range(NF):
        img = base.copy()
        d = ImageDraw.Draw(img)
        draw_sep(d, f)
        draw_eq(d, f)
        draw_battery(d, BATT, "under_min")
        frames.append(img)
    out_dir = os.path.join(os.path.dirname(__file__), "out")
    os.makedirs(out_dir, exist_ok=True)
    gif = os.path.join(out_dir, "bip6-vertical-batteria.gif")
    frames[0].save(gif, save_all=True, append_images=frames[1:], duration=120, loop=0)
    print("OK", gif)


if __name__ == "__main__":
    main()
