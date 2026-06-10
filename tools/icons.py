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

# ===== Icone meteo dinamiche (stesso stile dot) =====
# Sole INTERO (sereno) — come il mezzo sole dell'alba ma cerchio pieno + 8 raggi da 1 punto
WSUN = [
    ".....X.....",
    ".X.......X.",
    "...........",
    "...XXXXX...",
    "..XXXXXXX..",
    "X.XXXXXXX.X",
    "..XXXXXXX..",
    "...XXXXX...",
    "...........",
    ".X.......X.",
    ".....X.....",
]
# Pioggia: nuvola + gocce
WRAIN = [
    "...XXXX...",
    "..XXXXXX..",
    ".XXXXXXXX.",
    "XXXXXXXXXX",
    ".XXXXXXXX.",
    "..........",
    ".X..X..X..",
    "X..X..X...",
]
# Temporale: nuvola + fulmine
WSTORM = [
    "...XXXX...",
    "..XXXXXX..",
    ".XXXXXXXX.",
    "XXXXXXXXXX",
    ".XXXXXXXX.",
    "....XX....",
    "...XX.....",
    "..XXXX....",
    "....XX....",
    "...XX.....",
]
# Neve: nuvola + fiocchi
WSNOW = [
    "...XXXX...",
    "..XXXXXX..",
    ".XXXXXXXX.",
    "XXXXXXXXXX",
    ".XXXXXXXX.",
    "..........",
    ".X.X.X.X..",
    "..X.X.X...",
    ".X.X.X.X..",
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
