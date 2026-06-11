/*
 * Nothing Dot — VARIANTE VERTICALE (2 colonne) per Amazfit Bip 6 (390x450)
 * Sinistra: ore sopra / minuti sotto + linea separatrice + data.
 * Destra: 4 pill impilate (passi, meteo DINAMICO, alba, battito).
 */
import '../../shared/device-polyfill';

const W = 390;
const BG_BLACK = 0x000000;
const PILL_DARK = 0x1a1a1c;
const PILL_RED = 0xe2302d;
const PRESS = 0x2c2c2e;
const PRESS_RED = 0xc02824;

function digits(folder) {
  const a = [];
  for (let i = 0; i < 10; i++) a.push(`${folder}/${i}.png`);
  return a;
}
const NUM_BIG_W = digits('num_big_w');
const NUM_BIG_R = digits('num_big_r');
const NUM_TINY_G = digits('num_tiny_g');
const NUM_HR_W = digits('num_hr_w');
const NUM_SM_R = digits('num_sm_r');

const DOW_LANGS = [2, 3, 6, 7, 8, 9, 10, 14, 15, 16, 17, 21, 22, 25, 26, 27, 28, 29, 30, 31, 32];
function dowLang() {
  let l = 2;
  try { l = hmSetting.getLanguage(); } catch (e) {}
  return DOW_LANGS.indexOf(l) >= 0 ? l : 2;
}

function pad2(n) { return n < 10 ? '0' + n : '' + n; }

// mappa codici meteo Huami (0..28, tabella UFFICIALE sensore WEATHER Zepp OS) -> set CURATO 12 icone
// indice = condition index 0-based passato da WEATHER_CURRENT a IMG_LEVEL
const SUN = 'icon/w_sun.png', MOON = 'icon/w_moon.png', CLD = 'icon/w_cloud.png', OVC = 'icon/w_overcast.png',
      RN = 'icon/w_rain.png', SN = 'icon/w_snow.png', SLT = 'icon/w_sleet.png', ST = 'icon/w_storm.png',
      HL = 'icon/w_hail.png', FOG = 'icon/w_fog.png', SND = 'icon/w_sand.png', UNK = 'icon/w_unknown.png';
const WEATHER_ICONS = [
  // 0 Cloudy   1 Showers  2 SnowShwr  3 Sunny    4 Overcast 5 LightRain 6 LightSnow 7 ModRain  8 ModSnow  9 HeavySnow
  CLD,         RN,        SN,         SUN,       OVC,       RN,         SN,         RN,        SN,        SN,
  // 10 HvyRain 11 Sandstrm 12 Rain+Snow 13 Fog   14 Hazy    15 TStorm   16 Snowstrm 17 FloatDust 18 VHvyRain 19 Rain+Hail
  RN,          SND,       SLT,        FOG,       FOG,       ST,         SN,         SND,       RN,        HL,
  // 20 TS+Hail 21 HvyRnst 22 Dust    23 HvySand 24 Rainstrm 25 Unknown 26 CldNight 27 ShwrNgt  28 SunNight
  HL,          RN,        SND,       SND,       RN,        UNK,        CLD,        RN,        MOON,
];

// timer dell'equalizer (agganciato al battito) — fermato in onDestroy
let eqTimer = null;

function openNativeApp(kind) {
  try {
    let url = 'activityAppScreen';
    if (kind === 'weather') url = 'WeatherScreen';
    else if (kind === 'sunrise') url = 'TideScreen';
    else if (kind === 'hr') url = 'heart_app_Screen';
    hmApp.startApp({ appid: 1, url: url, native: true });
  } catch (e) {}
}

WatchFace({
  build() {
    try { hmUI.createWidget(hmUI.widget.FILL_RECT, { x: 0, y: 0, w: W, h: 450, color: BG_BLACK }); } catch (e) {}

    // ===== COLONNA SINISTRA: ore sopra / minuti sotto =====
    try {
      hmUI.createWidget(hmUI.widget.IMG_TIME, {
        hour_startX: 29, hour_startY: 34, hour_array: NUM_BIG_W, hour_space: 12, hour_zero: 1,
        minute_startX: 29, minute_startY: 170, minute_array: NUM_BIG_R, minute_space: 12, minute_zero: 1,
      });
    } catch (e) {}
    // separatore ore/minuti: due punti 2x2 (centrati sotto le cifre) — lampeggia ~1Hz
    let sepWidget = null;
    try { sepWidget = hmUI.createWidget(hmUI.widget.IMG, { x: 64, y: 138, src: 'sep_dots.png' }); } catch (e) {}

    // helper campo-numero a cifre-immagine
    function numberField(x, y, folder, digitW, maxDigits) {
      const imgs = [];
      for (let i = 0; i < maxDigits; i++) {
        let w = null;
        try { w = hmUI.createWidget(hmUI.widget.IMG, { x: x + i * digitW, y: y, src: folder + '/0.png' }); } catch (e) {}
        imgs.push(w);
      }
      return {
        set: function (value) {
          const s = '' + value;
          const n = s.length > maxDigits ? maxDigits : s.length;
          for (let i = 0; i < maxDigits; i++) {
            const wi = imgs[i];
            if (!wi) continue;
            try {
              if (i < n) { wi.setProperty(hmUI.prop.SRC, folder + '/' + s.charAt(i) + '.png'); wi.setProperty(hmUI.prop.VISIBLE, true); }
              else { wi.setProperty(hmUI.prop.VISIBLE, false); }
            } catch (e) {}
          }
        },
      };
    }

    // DATA: giorno settimana (lingua) + giorno mese
    const LANG = dowLang();
    let dowWidget = null;
    try { dowWidget = hmUI.createWidget(hmUI.widget.IMG, { x: 24, y: 314, src: `dow/${LANG}/0.png` }); } catch (e) {}
    const dayField = numberField(106, 300, 'num_sm_r', 30, 2);

    // ===== COLONNA DESTRA: 4 pill impilate =====
    const PX = 202, PW = 170, PH = 82, R = 28;
    const rowY = [34, 126, 218, 318];  // pill battito (row 3) allineato alla banda equalizer, sollevato dagli angoli arrotondati

    function pill(py, red, kind) {
      try {
        hmUI.createWidget(hmUI.widget.BUTTON, {
          x: PX, y: py, w: PW, h: PH, radius: R,
          normal_color: red ? PILL_RED : PILL_DARK, press_color: red ? PRESS_RED : PRESS,
          click_func: () => openNativeApp(kind),
        });
      } catch (e) {
        try { hmUI.createWidget(hmUI.widget.FILL_RECT, { x: PX, y: py, w: PW, h: PH, radius: R, color: red ? PILL_RED : PILL_DARK }); } catch (e2) {}
      }
    }
    function icon(x, y, src) { try { return hmUI.createWidget(hmUI.widget.IMG, { x, y, src }); } catch (e) { return null; } }

    // Passi
    pill(rowY[0], false, 'steps');
    icon(PX + 8, rowY[0] + 20, 'icon/runner.png');
    const stepField = numberField(PX + 62, rowY[0] + 30, 'num_tiny_g', 15, 5);

    // Meteo: icona dinamica (IMG_LEVEL data-bound) + temperatura attuale (data-bound)
    pill(rowY[1], false, 'weather');
    try {
      hmUI.createWidget(hmUI.widget.IMG_LEVEL, {
        x: PX + 8, y: rowY[1] + 20, image_array: WEATHER_ICONS, image_length: WEATHER_ICONS.length,
        type: hmUI.data_type.WEATHER_CURRENT, show_level: hmUI.show_level.ONLY_NORMAL,
      });
    } catch (e) {}
    try {
      hmUI.createWidget(hmUI.widget.TEXT_IMG, {
        x: PX + 62, y: rowY[1] + 30, font_array: NUM_TINY_G, h_space: 2, type: hmUI.data_type.WEATHER_CURRENT,
      });
    } catch (e) {}
    icon(PX + 62 + 32, rowY[1] + 30, 'num_tiny_g/deg.png');

    // Alba
    pill(rowY[2], false, 'sunrise');
    icon(PX + 8, rowY[2] + 20, 'icon/sunrise.png');
    const sunHField = numberField(PX + 62, rowY[2] + 30, 'num_tiny_g', 15, 2);
    icon(PX + 62 + 30, rowY[2] + 30, 'num_tiny_g/colon.png');
    const sunMField = numberField(PX + 62 + 45, rowY[2] + 30, 'num_tiny_g', 15, 2);

    // Battito
    pill(rowY[3], true, 'hr');
    icon(PX + 8, rowY[3] + 20, 'icon/heart.png');
    try {
      hmUI.createWidget(hmUI.widget.TEXT_IMG, { x: PX + 62, y: rowY[3] + 20, font_array: NUM_HR_W, h_space: 2, type: hmUI.data_type.HEART });
    } catch (e) {}

    stepField.set(0); sunHField.set('00'); sunMField.set('00'); dayField.set('10');

    // ===== DATI LIVE =====
    function readNum(sensor, names) {
      for (let i = 0; i < names.length; i++) {
        try {
          const val = sensor[names[i]];
          if (typeof val === 'function') { const r = sensor[names[i]](); if (r !== undefined && r !== null) return r; }
          else if (val !== undefined && val !== null) return val;
        } catch (e) {}
      }
      return null;
    }

    let timeSensor = null;
    try { timeSensor = hmSensor.createSensor(hmSensor.id.TIME); } catch (e) {}

    function updateDate() {
      try {
        if (!timeSensor) return;
        const wk = readNum(timeSensor, ['week']);
        if (wk !== null && dowWidget) dowWidget.setProperty(hmUI.prop.SRC, `dow/${LANG}/${(wk + 6) % 7}.png`);
        const d = readNum(timeSensor, ['day']);
        if (d !== null) dayField.set(pad2(d));
      } catch (e) {}
    }
    function updateSteps() {
      try { const s = hmSensor.createSensor(hmSensor.id.STEP); const v = readNum(s, ['getCurrent', 'current']); if (v !== null) stepField.set(v); } catch (e) {}
    }
    function updateWeather() {
      // temperatura e icona sono data-bound (auto). Qui solo l'orario alba dal forecast.
      try {
        const weather = hmSensor.createSensor(hmSensor.id.WEATHER);
        const wd = weather.getForecastWeather();
        if (wd && wd.tideData && wd.tideData.data && wd.tideData.count > 0) {
          const tide = wd.tideData.data[0];
          if (tide && tide.sunrise) { sunHField.set(pad2(tide.sunrise.hour)); sunMField.set(pad2(tide.sunrise.minute)); }
        }
      } catch (e) {}
    }

    updateDate(); updateSteps(); updateWeather();
    try {
      if (timeSensor && timeSensor.addEventListener) {
        timeSensor.addEventListener(timeSensor.event.MINUTEEND, () => { updateDate(); updateSteps(); updateWeather(); });
      }
    } catch (e) {}

    // ===== EQUALIZER agganciato al battito (fascia sotto la data) =====
    try {
      const EQ_X = 24, EQ_BASE = 385, EQ_BX = 21, EQ_DY = 17, EQ_BARS = 8, EQ_MAXH = 5;
      const eqDots = [];
      for (let i = 0; i < EQ_BARS; i++) {
        eqDots[i] = [];
        for (let k = 0; k < EQ_MAXH; k++) {
          let w = null;
          try {
            w = hmUI.createWidget(hmUI.widget.IMG, { x: EQ_X + i * EQ_BX, y: EQ_BASE - k * EQ_DY, src: 'eq_g.png' });
            w.setProperty(hmUI.prop.VISIBLE, false);
          } catch (e) {}
          eqDots[i][k] = w;
        }
      }
      let hrSensor = null;
      try { hrSensor = hmSensor.createSensor(hmSensor.id.HEART_RATE); } catch (e) {}
      function readHR() {
        if (!hrSensor) return 0;
        const v = readNum(hrSensor, ['getCurrent', 'last', 'getLast', 'current']);
        return (v && v > 0) ? v : 0;
      }
      let eqFrame = 0, eqBpm = 0;
      function eqTick() {
        // separatore lampeggiante ~1Hz (480ms on / 480ms off a 120ms/frame)
        if (sepWidget) sepWidget.setProperty(hmUI.prop.VISIBLE, (Math.floor(eqFrame / 4) % 2 === 0));
        if (eqFrame % 20 === 0) eqBpm = readHR();           // BPM letto ~ogni 2.4s
        const lvl = eqBpm > 0 ? Math.max(0, Math.min(1, (eqBpm - 50) / 100)) : 0.12;
        const energy = 0.2 + 0.8 * lvl;                      // ampiezza barre dal battito
        const speed = 0.18 + lvl * 0.5;                      // velocita' danza dal battito
        for (let i = 0; i < EQ_BARS; i++) {
          const wave = 0.5 + 0.5 * Math.sin(eqFrame * speed + i * 0.8);
          let h = 1 + Math.round((EQ_MAXH - 1) * energy * wave);
          if (h < 1) h = 1; else if (h > EQ_MAXH) h = EQ_MAXH;
          for (let k = 0; k < EQ_MAXH; k++) {
            const w = eqDots[i][k];
            if (!w) continue;
            if (k < h) {
              w.setProperty(hmUI.prop.SRC, (k === h - 1) ? 'eq_r.png' : 'eq_g.png');
              w.setProperty(hmUI.prop.VISIBLE, true);
            } else {
              w.setProperty(hmUI.prop.VISIBLE, false);
            }
          }
        }
        eqFrame++;
      }
      eqTick();
      if (typeof setInterval !== 'undefined') eqTimer = setInterval(eqTick, 120);
    } catch (e) {}
  },

  onDestroy() {
    try { if (eqTimer && typeof clearInterval !== 'undefined') { clearInterval(eqTimer); eqTimer = null; } } catch (e) {}
  },
});
