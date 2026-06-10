/*
 * Nothing Dot — watch face Amazfit Bip 6 (390x450)
 * Numeri dinamici resi come gruppi di cifre-immagine (una IMG per posizione),
 * aggiornate via SRC: e' il metodo che funziona sui watchface Zepp OS.
 */
import '../../shared/device-polyfill';

const W = 390;

const BG_BLACK = 0x000000;
const PILL_DARK = 0x1a1a1c;
const PILL_RED = 0xe2302d;
const PRESS = 0x2c2c2e;
const PRESS_RED = 0xc02824;

const XS_W = 25; // larghezza cifra piccola (pitch 5)
const SM_W = 30; // larghezza cifra media (pitch 6)

function digits(folder) {
  const a = [];
  for (let i = 0; i < 10; i++) a.push(`${folder}/${i}.png`);
  return a;
}
const NUM_BIG_W = digits('num_big_w');
const NUM_BIG_R = digits('num_big_r');

const DOW_IMG = [
  'dow/LUN.png', 'dow/MAR.png', 'dow/MER.png', 'dow/GIO.png',
  'dow/VEN.png', 'dow/SAB.png', 'dow/DOM.png',
];

function pad2(n) {
  return n < 10 ? '0' + n : '' + n;
}

function openNativeApp(kind) {
  try {
    let url = 'activityAppScreen';
    if (kind === 'weather') url = 'WeatherScreen';
    else if (kind === 'sunrise') url = 'SunRiseSunSetScreen';
    else if (kind === 'hr') url = 'HeartRateScreen';
    hmApp.startApp({ appid: 1, url: url, native: true });
  } catch (e) {}
}

WatchFace({
  build() {
    // Sfondo
    try {
      hmUI.createWidget(hmUI.widget.FILL_RECT, { x: 0, y: 0, w: W, h: 450, color: BG_BLACK });
    } catch (e) {}

    // ORA (HH bianca, MM rossa) — auto-aggiornata dal sistema
    try {
      hmUI.createWidget(hmUI.widget.IMG_TIME, {
        hour_startX: 34, hour_startY: 56, hour_array: NUM_BIG_W, hour_space: 12, hour_zero: 1,
        minute_startX: 222, minute_startY: 56, minute_array: NUM_BIG_R, minute_space: 12, minute_zero: 1,
      });
    } catch (e) {}

    // Campo-numero a cifre-immagine. Ritorna { set(value) }.
    function numberField(x, y, folder, digitW, maxDigits, alignRight) {
      const imgs = [];
      for (let i = 0; i < maxDigits; i++) {
        let w = null;
        try {
          w = hmUI.createWidget(hmUI.widget.IMG, { x: x + i * digitW, y: y, src: folder + '/0.png' });
        } catch (e) {}
        imgs.push(w);
      }
      return {
        set: function (value) {
          const s = '' + value;
          const n = s.length > maxDigits ? maxDigits : s.length;
          // offset per allineare a destra se richiesto (per i passi)
          const off = alignRight ? (maxDigits - n) : 0;
          for (let i = 0; i < maxDigits; i++) {
            const w = imgs[i];
            if (!w) continue;
            const srcIdx = i - off;
            try {
              if (srcIdx >= 0 && srcIdx < n) {
                w.setProperty(hmUI.prop.SRC, folder + '/' + s.charAt(srcIdx) + '.png');
                w.setProperty(hmUI.prop.VISIBLE, true);
              } else {
                w.setProperty(hmUI.prop.VISIBLE, false);
              }
            } catch (e) {}
          }
        },
      };
    }

    // DATA: giorno settimana (IMG) + giorno mese (cifre rosse)
    let dowWidget = null;
    try {
      dowWidget = hmUI.createWidget(hmUI.widget.IMG, { x: 184, y: 150, src: 'dow/MER.png' });
    } catch (e) {}
    const dayField = numberField(314, 150, 'num_sm_r', SM_W, 2, false);

    // PILL
    const PW = 174, PH = 84, R = 26;
    const xL = 15, xR = 201, y1 = 210, y2 = 308;

    function pillRect(x, y, red, kind) {
      try {
        hmUI.createWidget(hmUI.widget.BUTTON, {
          x, y, w: PW, h: PH, radius: R,
          normal_color: red ? PILL_RED : PILL_DARK,
          press_color: red ? PRESS_RED : PRESS,
          click_func: () => openNativeApp(kind),
        });
      } catch (e) {
        try {
          hmUI.createWidget(hmUI.widget.FILL_RECT, { x, y, w: PW, h: PH, radius: R, color: red ? PILL_RED : PILL_DARK });
        } catch (e2) {}
      }
    }
    function icon(x, y, src) {
      try { hmUI.createWidget(hmUI.widget.IMG, { x, y, src }); } catch (e) {}
    }

    // Passi
    pillRect(xL, y1, false, 'steps');
    icon(xL + 16, y1 + 27, 'icon/runner.png');
    const stepField = numberField(xL + 50, y1 + 25, 'num_xs_w', XS_W, 5, false);

    // Meteo
    pillRect(xR, y1, false, 'weather');
    icon(xR + 14, y1 + 33, 'icon/cloud.png');
    const tempField = numberField(xR + 48, y1 + 25, 'num_xs_w', XS_W, 2, false);
    icon(xR + 100, y1 + 25, 'num_xs_w/deg.png');

    // Alba HH:MM
    pillRect(xL, y2, false, 'sunrise');
    icon(xL + 12, y2 + 31, 'icon/sunrise.png');
    const sunHField = numberField(xL + 44, y2 + 25, 'num_xs_w', XS_W, 2, false);
    icon(xL + 94, y2 + 25, 'num_xs_w/colon.png');
    const sunMField = numberField(xL + 112, y2 + 25, 'num_xs_w', XS_W, 2, false);

    // Battito
    pillRect(xR, y2, true, 'hr');
    icon(xR + 16, y2 + 31, 'icon/heart.png');
    const hrField = numberField(xR + 48, y2 + 25, 'num_xs_w', XS_W, 3, false);

    // valori iniziali
    stepField.set(0); tempField.set(0); sunHField.set('00'); sunMField.set('00'); hrField.set(0); dayField.set('10');

    // ===================== DATI LIVE =====================
    function readNum(sensor, names) {
      for (let i = 0; i < names.length; i++) {
        try {
          const val = sensor[names[i]];
          if (typeof val === 'function') {
            const r = sensor[names[i]]();
            if (r !== undefined && r !== null) return r;
          } else if (val !== undefined && val !== null) {
            return val;
          }
        } catch (e) {}
      }
      return null;
    }

    let timeSensor = null;
    try { timeSensor = hmSensor.createSensor(hmSensor.id.TIME); } catch (e) {}

    function updateDate() {
      try {
        if (!timeSensor) return;
        const w = readNum(timeSensor, ['week']);   // 1..7
        if (w !== null && dowWidget) {
          const idx = (w + 5) % 7;
          dowWidget.setProperty(hmUI.prop.SRC, DOW_IMG[idx]);
        }
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
    function updateHr() {
      try {
        const h = hmSensor.createSensor(hmSensor.id.HEART_RATE);
        const v = readNum(h, ['getLast', 'last', 'getCurrent', 'current']);
        if (v) hrField.set(v);
      } catch (e) {}
    }
    function updateWeather() {
      try {
        const weather = hmSensor.createSensor(hmSensor.id.WEATHER);
        const wd = weather.getForecastWeather();
        if (!wd) return;
        // temperatura: massima di oggi (giorno 0)
        if (wd.forecastData && wd.forecastData.data && wd.forecastData.count > 0) {
          const today = wd.forecastData.data[0];
          if (today && today.high !== undefined && today.high !== null) {
            tempField.set(today.high);
          }
        }
        // alba: tideData di oggi (giorno 0)
        if (wd.tideData && wd.tideData.data && wd.tideData.count > 0) {
          const tide = wd.tideData.data[0];
          if (tide && tide.sunrise) {
            sunHField.set(pad2(tide.sunrise.hour));
            sunMField.set(pad2(tide.sunrise.minute));
          }
        }
      } catch (e) {}
    }

    updateDate(); updateSteps(); updateHr(); updateWeather();

    try {
      if (timeSensor && timeSensor.addEventListener) {
        timeSensor.addEventListener(timeSensor.event.MINUTEEND, () => {
          updateDate(); updateSteps(); updateHr(); updateWeather();
        });
      }
    } catch (e) {}
  },

  onDestroy() {},
});
