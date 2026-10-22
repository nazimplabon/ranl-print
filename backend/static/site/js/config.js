// RANL PRINT runtime configuration. The Django-served website uses same-origin APIs.
const isFilePreview = window.location.protocol === 'file:';
const isFrontendDevServer = window.location.port === '5173';
window.RNL_CONFIG = {
  API_BASE: isFilePreview || isFrontendDevServer ? 'http://127.0.0.1:8000' : '',
  PREVIEW_FALLBACK: false,
  CURRENCY: '৳',
  PHONE: '01568 768671',
  EMAIL: 'RANLPrintBD@gmail.com',
  LOCATION: 'Sajborkhila, Sherpur 2100, Bangladesh',
  HOURS: 'Sat–Thu · 9:00 AM–8:00 PM'
};
