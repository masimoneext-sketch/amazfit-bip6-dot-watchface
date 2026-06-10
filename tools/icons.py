# -*- coding: utf-8 -*-
"""
Icone pixel-art (bitmap 'X'/'.') per le pill della watch face e il fumetto
notifiche. Stesso stile a punti del font: rese con dotfont.draw_bitmap.
"""

# Passi: due impronte di scarpa (suola + tacco 2x2), molto sfalsate sx-su/dx-giu
RUNNER = [
    ".XX........",
    "XXXX.......",
    "XXXX.......",
    "...........",
    ".XX.....XX.",
    ".XX....XXXX",
    ".......XXXX",
    "...........",
    "........XX.",
    "........XX.",
]

# Meteo: nuvoletta (file cloud.png)
CLOUD = [
    "......XXX...",
    "...XXXXXXXX.",
    "..XXXXXXXXXX",
    ".XXXXXXXXXXX",
    "XXXXXXXXXXXX",
    "XXXXXXXXXXXX",
    ".XXXXXXXXXX.",
]

# Alba: mezzo sole = semicerchio + 5 raggi da 1 punto, staccati
SUNRISE = [
    ".....X.....",
    ".X.......X.",
    "...........",
    "....XXX....",
    "...XXXXX...",
    "X.XXXXXXX.X",
    "..XXXXXXX..",
]

# Cuore (battito) — piu' grande
HEART = [
    ".XX...XX.",
    "XXXXXXXXX",
    "XXXXXXXXX",
    "XXXXXXXXX",
    ".XXXXXXX.",
    "..XXXXX..",
    "...XXX...",
    "....X....",
]

# Fumetto stile WhatsApp (notifiche) — coda in basso a sinistra, 3 puntini
BUBBLE = [
    ".XXXXXXXXX.",
    "XXXXXXXXXXX",
    "XXXXXXXXXXX",
    "XXX.X.X.XXX",
    "XXXXXXXXXXX",
    "XXXXXXXXXXX",
    ".XXXXXXXXX.",
    "..XXX......",
    ".XX........",
    "X..........",
]
