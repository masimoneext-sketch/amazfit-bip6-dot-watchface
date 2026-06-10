/*
 * Nothing Dot — watch face Amazfit Bip 6 (390x450)
 * Allineata al mockup approvato: ora HH:MM con separatore micro-pixel,
 * giorno settimana micro-pixel, valori pill grigi piccoli, cuore grande,
 * icone definite. Numeri dinamici = gruppi di cifre-immagine (SRC).
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
const NUM_TINY_G = digits('num_tiny_g'); // valori pill grigi piccoli
const NUM_HR_W = digits('num_hr_w');     // battito bianco grande
const NUM_SM_R = digits('num_sm_r');     // giorno mese rosso

const DOW_IMG = [
  'dow/LUN.png', 'dow/MAR.png', 'dow/MER.png', 'dow/GIO.png',
  'dow/VEN.png', 'dow/SAB.png', 'dow/DOM.png',
];

function pad2(n) { return n < 10 ? '0' + n : '' + n; }

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
    try {
      hmUI.createWidget(hmUI.widget.FILL_RECT, { x: 0, y: 0, w: W, h: 450, color: BG_BLACK });
    } catch (e) {}

    // ORA: HH bianca + MM rossa
    try {
      hmUI.createWidget(hmUI.widget.IMG_TIME, {
        hour_startX: 34, hour_startY: 56, hour_array: NUM_BIG_W, hour_space: 12, hour_zero: 1,
        minute_startX: 222, minute_startY: 56, minute_array: NUM_BIG_R, minute_space: 12, minute_zero: 1,
      });
    } catch (e) {}
    // separatore ":" micro-pixel
    try {
      hmUI.createWidget(hmUI.widget.IMG, { x: 187, y: 77, src: 'sep_colon.png' });
    } catch (e) {}

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
              if (i < n) {
                wi.setProperty(hmUI.prop.SRC, folder + '/' + s.charAt(i) + '.png');
                wi.setProperty(hmUI.prop.VISIBLE, true);
              } else {
                wi.setProperty(hmUI.prop.VISIBLE, false);
              }
            } catch (e) {}
          }
        },
      };
    }

    // DATA: giorno settimana (micro) + giorno mese (rosso)
    let dowWidget = null;
    try { dowWidget = hmUI.createWidget(hmUI.widget.IMG, { x: 216, y: 166, src: 'dow/MER.png' }); } catch (e) {}
    const dayField = numberField(294, 152, 'num_sm_r', 30, 2);

    // PILL
    const PW = 174, PH = 84, R = 26;
    const xL = 15, xR = 201, y1 = 215, y2 = 313;

    function pill(x, y, red, kind) {
      try {
        hmUI.createWidget(hmUI.widget.BUTTON, {
          x, y, w: PW, h: PH, radius: R,
          normal_color: red ? PILL_RED : PILL_DARK,
          press_color: red ? PRESS_RED : PRESS,
          click_func: () => openNativeApp(kind),
        });
      } catch (e) {
        try { hmUI.createWidget(hmUI.widget.FILL_RECT, { x, y, w: PW, h: PH, radius: R, color: red ? PILL_RED : PILL_DARK }); } catch (e2) {}
      }
    }
    function icon(x, y, src) { try { hmUI.createWidget(hmUI.widget.IMG, { x, y, src }); } catch (e) {} }

    // Passi (alto sx)
    pill(xL, y1, false, 'steps');
    icon(xL + 6, y1 + 21, 'icon/runner.png');
    const stepField = numberField(xL + 64, y1 + 31, 'num_tiny_g', 15, 5);

    // Meteo (alto dx)
    pill(xR, y1, false, 'weather');
    icon(xR + 6, y1 + 21, 'icon/cloud.png');
    const tempField = numberField(xR + 64, y1 + 31, 'num_tiny_g', 15, 2);
    icon(xR + 64 + 32, y1 + 31, 'num_tiny_g/deg.png');

    // Alba HH:MM (basso sx)
    pill(xL, y2, false, 'sunrise');
    icon(xL + 6, y2 + 21, 'icon/sunrise.png');
    const sunHField = numberField(xL + 64, y2 + 31, 'num_tiny_g', 15, 2);
    icon(xL + 64 + 30, y2 + 31, 'num_tiny_g/colon.png');
    const sunMField = numberField(xL + 64 + 45, y2 + 31, 'num_tiny_g', 15, 2);

    // Battito (basso dx, rossa) — widget dati di sistema, bianco grande
    pill(xR, y2, true, 'hr');
    icon(xR + 6, y2 + 21, 'icon/heart.png');
    try {
      hmUI.createWidget(hmUI.widget.TEXT_IMG, {
        x: xR + 64, y: y2 + 21, font_array: NUM_HR_W, h_space: 2, type: hmUI.data_type.HEART,
      });
    } catch (e) {}

    // valori iniziali
    stepField.set(0); tempField.set(0); sunHField.set('00'); sunMField.set('00'); dayField.set('10');

    // ===================== DATI LIVE =====================
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
        if (wk !== null && dowWidget) dowWidget.setProperty(hmUI.prop.SRC, DOW_IMG[(wk + 5) % 7]);
        const d = readNum(timeSensor, ['day']);
        if (d !== null) dayField.set(pad2(d));
      } catch (e) {}
    }
    function updateSteps() {
      try {
        const s = hmSensor.createSensor(hmSensor.id.STEP);
        const v = readNum(s, ['getCurrent', 'current']);
        if (v !== null) stepField.set(v);
      } catch (e) {}
    }
    function updateWeather() {
      try {
        const weather = hmSensor.createSensor(hmSensor.id.WEATHER);
        const wd = weather.getForecastWeather();
        if (!wd) return;
        if (wd.forecastData && wd.forecastData.data && wd.forecastData.count > 0) {
          const t = wd.forecastData.data[0];
          if (t && t.high !== undefined && t.high !== null) tempField.set(t.high);
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
