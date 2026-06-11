# -*- coding: utf-8 -*-
"""
Set CURATO di 12 icone meteo dot-matrix (stile Nothing) per Bip 6.
Ogni icona e' visivamente distinta; gli stati Huami simili condividono icona.
Mapping completo 0..28 -> una delle 12 chiavi in MAP.
Se approvato: confluisce in gen_assets.py (12 PNG) + WEATHER_ICONS nel codice.
"""

# ---------- 12 icone ----------
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
    "...XXX.....",
    "..XXXXX...X",
    ".XXX.......",
    ".XXX....X..",
    ".XXX.......",
    "..XXXXX....",
    "...XXX.....",
]
CLOUD = [
    "...XXXX...",
    "..XXXXXX..",
    ".XXXXXXXX.",
    "XXXXXXXXXX",
    ".XXXXXXXX.",
]
OVERCAST = [
    "..XXX...XXX..",
    ".XXXXX.XXXXX.",
    "XXXXXXXXXXXXX",
    "XXXXXXXXXXXXX",
    ".XXXXXXXXXXX.",
]
RAIN = [
    "...XXXX...",
    "..XXXXXX..",
    ".XXXXXXXX.",
    "XXXXXXXXXX",
    ".XXXXXXXX.",
    "..........",
    ".X..X..X..",
    "X..X..X...",
]
SNOW = [
    "...XXXX...",
    "..XXXXXX..",
    ".XXXXXXXX.",
    "XXXXXXXXXX",
    ".XXXXXXXX.",
    "..........",
    "..X...X...",
    "X...X...X.",
    "..X...X...",
]
SLEET = [
    "...XXXX...",
    "..XXXXXX..",
    ".XXXXXXXX.",
    "XXXXXXXXXX",
    ".XXXXXXXX.",
    "..........",
    ".X..X..X..",
    "..o..o..o.".replace("o", "X"),
]
STORM = [
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
HAIL = [
    "...XXXX...",
    "..XXXXXX..",
    ".XXXXXXXX.",
    "XXXXXXXXXX",
    ".XXXXXXXX.",
    "..........",
    ".XX...XX..",
    ".XX...XX..",
    "....XX....",
    "....XX....",
]
FOG = [
    "..........",
    ".XXXXXXXX.",
    "..........",
    "XXXXXXXXXX",
    "..........",
    ".XXXXXXXX.",
    "..........",
    "XXXXXXXXXX",
    "..........",
]
SAND = [
    "XX..XX..XX",
    ".XX..XX..X",
    "..XX..XX..",
    "X..XX..XX.",
    "XX..XX..XX",
]
UNKNOWN = [
    "..XXXX....",
    ".XX..XX...",
    ".....XX...",
    "....XX....",
    "...XX.....",
    "..........",
    "...XX.....",
]

ICONS = {
    "sun": SUN, "moon": MOON, "cloud": CLOUD, "overcast": OVERCAST,
    "rain": RAIN, "snow": SNOW, "sleet": SLEET, "storm": STORM,
    "hail": HAIL, "fog": FOG, "sand": SAND, "unknown": UNKNOWN,
}
ICON_LABEL = {
    "sun": "SOLE", "moon": "LUNA", "cloud": "NUVOLA", "overcast": "COPERTO",
    "rain": "PIOGGIA", "snow": "NEVE", "sleet": "PIOG+NEVE", "storm": "TEMPORALE",
    "hail": "GRANDINE", "fog": "FOSCHIA", "sand": "SABBIA", "unknown": "?",
}

# mapping 0..28 (tabella Huami ufficiale) -> chiave icona
MAP = {
    0: "cloud", 1: "rain", 2: "snow", 3: "sun", 4: "overcast",
    5: "rain", 6: "snow", 7: "rain", 8: "snow", 9: "snow",
    10: "rain", 11: "sand", 12: "sleet", 13: "fog", 14: "fog",
    15: "storm", 16: "snow", 17: "sand", 18: "rain", 19: "hail",
    20: "hail", 21: "rain", 22: "sand", 23: "sand", 24: "rain",
    25: "unknown", 26: "cloud", 27: "rain", 28: "moon",
}
HUAMI_NAME = {
    0: "Cloudy", 1: "Showers", 2: "Snow Showers", 3: "Sunny", 4: "Overcast",
    5: "Light Rain", 6: "Light Snow", 7: "Mod Rain", 8: "Mod Snow", 9: "Heavy Snow",
    10: "Heavy Rain", 11: "Sandstorm", 12: "Rain+Snow", 13: "Fog", 14: "Hazy",
    15: "T-Storms", 16: "Snowstorm", 17: "Floating dust", 18: "V.Heavy Rainstorm",
    19: "Rain+Hail", 20: "T-Storms+Hail", 21: "Heavy Rainstorm", 22: "Dust",
    23: "Heavy sandstorm", 24: "Rainstorm", 25: "Unknown", 26: "Cloudy Night",
    27: "Showers Night", 28: "Sunny Night",
}
