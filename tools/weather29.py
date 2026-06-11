# -*- coding: utf-8 -*-
"""
29 icone meteo dot-matrix (stile Nothing) — una per ogni stato Huami ufficiale
del sensore WEATHER (indice 0..28). Stesse convenzioni di icons.py: bitmap
'X'/'.', rese con dotfont.draw_bitmap. Pensate per il MOCKUP di revisione:
se approvate, confluiscono in gen_assets.py + image_array IMG_LEVEL nel codice.

Ogni voce: indice -> (nome, gruppo_attuale, bitmap)
gruppo_attuale = a quale delle 5 icone correnti lo stato e' oggi mappato.
"""

# ---- mattoni riutilizzabili ----
CLOUD = [
    "...XXXX...",
    "..XXXXXX..",
    ".XXXXXXXX.",
    "XXXXXXXXXX",
    ".XXXXXXXX.",
]
CLOUD_THICK = [
    "...XXXX...",
    "..XXXXXX..",
    ".XXXXXXXX.",
    "XXXXXXXXXX",
    "XXXXXXXXXX",
    ".XXXXXXXX.",
]
SUN = [
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
MOON = [
    "...XXX....",
    "..XXXXX...",
    ".XXX......",
    ".XXX......",
    ".XXX......",
    "..XXXXX...",
    "...XXX....",
]
MOON_STAR = [
    "...XXX...X",
    "..XXXXX...",
    ".XXX......",
    ".XXX...X..",
    ".XXX......",
    "..XXXXX..X",
    "...XXX....",
]

# precipitazioni (riga 0 = subito sotto la nuvola)
R_LIGHT = ["..........", "..X....X.."]
R_SHWR  = ["..........", ".X..X..X..", ".........."]
R_MOD   = [".X..X..X..", "..X..X..X."]
R_HEAVY = [".X..X..X..", "X..X..X..."]
R_STORM = [".X.X.X.X..", "X.X.X.X.X.", ".X.X.X.X.."]
R_VHVY  = ["X.X.X.X.X.", ".XXX.XXX..", "X.X.X.X.X."]

S_LIGHT = ["..........", "...X...X.."]
S_MOD   = [".X..X..X..", "..X..X..X."]
S_HEAVY = [".X.X.X.X..", "X.X.X.X.X.", ".X.X.X.X.."]
S_STORM = ["X.X.X.X.X.", ".X.X.X.X..", "X.X.X.X.X.", ".X.X.X.X.."]

BOLT = [
    "....XX....",
    "...XX.....",
    "..XXXX....",
    "....XX....",
    "...XX.....",
]
HAIL = [".XX...XX..", "..........", "...XX..XX."]
BOLT_HAIL = [
    "....XX....",
    "...XX.....",
    "..XXXX....",
    ".XX...XX..",
]
MIX = [".X..X..X..", "..o..o..o.".replace("o", "X")]  # sleet: drops+flakes

# atmosferici (senza nuvola, linee orizzontali)
FOG = [
    "..........",
    ".XXXXXXXX.",
    "..........",
    "XXXXXXXXXX",
    "..........",
    ".XXXXXXXX.",
    "..........",
]
HAZE = [
    ".X.X.X.X.X",
    "..........",
    "X.X.X.X.X.",
    "..........",
    ".X.X.X.X.X",
]
SAND = [
    "XX..XX..XX",
    "..XX..XX..",
    "XX..XX..XX",
    "..XX..XX..",
]
SAND_HEAVY = [
    "XXX.XXX.XX",
    ".XXX.XXX.X",
    "XXX.XXX.XX",
    ".XXX.XXX.X",
    "XXX.XXX.XX",
]
DUST = [
    "..........",
    ".XX..XX..X",
    "..........",
    "X..XX..XX.",
    "..........",
]
DUST_FLOAT = [
    "..X....X..",
    ".....X....",
    "X....X...X",
    "...X....X.",
]
QMARK = [
    "..XXXX....",
    ".XX..XX...",
    ".....XX...",
    "....XX....",
    "...XX.....",
    "..........",
    "...XX.....",
]


def _cloud(precip, base=CLOUD):
    return base + [".........."] * 0 + precip


WEATHER = {
    0:  ("CLOUDY",        "cloud", CLOUD),
    1:  ("SHOWERS",       "rain",  _cloud(R_SHWR)),
    2:  ("SNOW SHWR",     "snow",  _cloud(S_LIGHT)),
    3:  ("SUNNY",         "sun",   SUN),
    4:  ("OVERCAST",      "cloud", CLOUD_THICK),
    5:  ("LIGHT RAIN",    "rain",  _cloud(R_LIGHT)),
    6:  ("LIGHT SNOW",    "snow",  _cloud(S_LIGHT)),
    7:  ("MOD RAIN",      "rain",  _cloud(R_MOD)),
    8:  ("MOD SNOW",      "snow",  _cloud(S_MOD)),
    9:  ("HEAVY SNOW",    "snow",  _cloud(S_HEAVY)),
    10: ("HEAVY RAIN",    "rain",  _cloud(R_HEAVY)),
    11: ("SANDSTORM",     "cloud", SAND),
    12: ("RAIN+SNOW",     "snow",  _cloud(MIX)),
    13: ("FOG",           "cloud", FOG),
    14: ("HAZY",          "cloud", HAZE),
    15: ("T-STORMS",      "storm", _cloud(BOLT)),
    16: ("SNOWSTORM",     "snow",  _cloud(S_STORM)),
    17: ("FLOAT DUST",    "cloud", DUST_FLOAT),
    18: ("V.HVY RNSTORM", "rain",  _cloud(R_VHVY)),
    19: ("RAIN+HAIL",     "storm", _cloud([".X..X..X.."] + HAIL)),
    20: ("TSTORM+HAIL",   "storm", _cloud(BOLT_HAIL)),
    21: ("HVY RNSTORM",   "rain",  _cloud(R_STORM)),
    22: ("DUST",          "cloud", DUST),
    23: ("HVY SANDSTORM", "cloud", SAND_HEAVY),
    24: ("RAINSTORM",     "rain",  _cloud(R_STORM)),
    25: ("UNKNOWN",       "cloud", QMARK),
    26: ("CLOUDY NIGHT",  "cloud", MOON[:4] + CLOUD),
    27: ("SHOWERS NIGHT", "rain",  MOON[:4] + R_MOD),
    28: ("SUNNY NIGHT",   "sun",   MOON_STAR),
}
