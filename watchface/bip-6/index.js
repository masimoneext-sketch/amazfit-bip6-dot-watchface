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

// codice condizione meteo -> icona (mappa Huami standard, da calibrare sul device)
function weatherIconSrc(code) {
  if (code === 0) return 'icon/w_sun.png';            // sereno
  if (code >= 1 && code <= 3) return 'icon/w_cloud.png'; // nuvoloso/nebbia
  if (code === 5 || code === 6) return 'icon/w_storm.png'; // temporale
  if (code >= 13 && code <= 22) return 'icon/w_snow.png';  // neve
  if (code >= 4) return 'icon/w_rain.png';            // pioggia
  return 'icon/w_cloud.png';
}

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
        hour_startX: 29, hour_startY: 40, hour_array: NUM_BIG_W, hour_space: 12, hour_zero: 1,
        minute_startX: 29, minute_startY: 168, minute_array: NUM_BIG_R, minute_space: 12, minute_zero: 1,
      });
    } catch (e) {}
    // linea separatrice
    try { hmUI.createWidget(hmUI.widget.IMG, { x: 46, y: 138, src: 'sep_line.png' }); } catch (e) {}

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
    try { dowWidget = hmUI.createWidget(hmUI.widget.IMG, { x: 24, y: 276, src: `dow/${LANG}/0.png` }); } catch (e) {}
    const dayField = numberField(106, 262, 'num_sm_r', 30, 2);

    // ===== COLONNA DESTRA: 4 pill impilate =====
    const PX = 198, PW = 178, PH = 96, R = 30;
    const rowY = [16, 122, 228, 334];

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
    icon(PX + 8, rowY[0] + 27, 'icon/runner.png');
    const stepField = numberField(PX + 66, rowY[0] + 37, 'num_tiny_g', 15, 5);

    // Meteo (icona dinamica)
    pill(rowY[1], false, 'weather');
    const weatherIcon = icon(PX + 8, rowY[1] + 27, 'icon/w_cloud.png');
    const tempField = numberField(PX + 66, rowY[1] + 37, 'num_tiny_g', 15, 2);
    icon(PX + 66 + 32, rowY[1] + 37, 'num_tiny_g/deg.png');

    // Alba
    pill(rowY[2], false, 'sunrise');
    icon(PX + 8, rowY[2] + 27, 'icon/sunrise.png');
    const sunHField = numberField(PX + 66, rowY[2] + 37, 'num_tiny_g', 15, 2);
    icon(PX + 66 + 30, rowY[2] + 37, 'num_tiny_g/colon.png');
    const sunMField = numberField(PX + 66 + 45, rowY[2] + 37, 'num_tiny_g', 15, 2);

    // Battito
    pill(rowY[3], true, 'hr');
    icon(PX + 8, rowY[3] + 27, 'icon/heart.png');
    try {
      hmUI.createWidget(hmUI.widget.TEXT_IMG, { x: PX + 66, y: rowY[3] + 27, font_array: NUM_HR_W, h_space: 2, type: hmUI.data_type.HEART });
    } catch (e) {}

    stepField.set(0); tempField.set(0); sunHField.set('00'); sunMField.set('00'); dayField.set('10');

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
        if (wk !== null && dowWidget) dowWidget.setProperty(hmUI.prop.SRC, `dow/${LANG}/${(wk + 5) % 7}.png`);
        const d = readNum(timeSensor, ['day']);
        if (d !== null) dayField.set(pad2(d));
      } catch (e) {}
    }
    function updateSteps() {
      try { const s = hmSensor.createSensor(hmSensor.id.STEP); const v = readNum(s, ['getCurrent', 'current']); if (v !== null) stepField.set(v); } catch (e) {}
    }
    function updateWeather() {
      try {
        const weather = hmSensor.createSensor(hmSensor.id.WEATHER);
        const wd = weather.getForecastWeather();
        if (!wd || !wd.forecastData || !wd.forecastData.data || wd.forecastData.count <= 0) return;
        const t0 = wd.forecastData.data[0];
        if (t0 && t0.high !== undefined && t0.high !== null) tempField.set(t0.high);
        // condizione meteo -> icona (campo da calibrare sul device)
        if (weatherIcon && t0) {
          const code = readNum(t0, ['weatherType', 'weatherCode', 'weather', 'code']);
          if (code !== null) weatherIcon.setProperty(hmUI.prop.SRC, weatherIconSrc(code));
        }
        if (wd.tideData && wd.tideData.data && wd.tideData.count > 0) {
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
  },

  onDestroy() {},
});
