import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

// Import translation files
import enCommon from '../locales/en/common.json';
import roCommon from '../locales/ro/common.json';

const resources = {
  en: {
    common: enCommon
  },
  ro: {
    common: roCommon
  }
};

i18n
  .use(initReactI18next)
  .init({
    resources,
    lng: localStorage.getItem('language') || 'en', // default language
    fallbackLng: 'en',
    debug: false,
    
    // Namespace
    defaultNS: 'common',
    
    interpolation: {
      escapeValue: false // React already escapes by default
    },
    
    // Save language to localStorage
    detection: {
      order: ['localStorage', 'navigator'],
      caches: ['localStorage']
    }
  });

export default i18n; 