// <!-- added by samer -->
/**
 * plugins/vuetify.js
 *
 * Professional University Design System
 */

// =========================
// STYLES
// =========================

import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'

// =========================
// VUETIFY
// =========================

import { createVuetify } from 'vuetify'
import { VTreeview } from 'vuetify/labs/VTreeview'

// =========================
// LIGHT THEME (WHITE)
// =========================

const lightTheme = {
  dark: false,

  colors: {
    primary: '#1363DF',
    'primary-lighten-1': '#4F8CFF',
    'primary-darken-1': '#0B4FB3',

    secondary: '#334155',

    success: '#16A34A',
    info: '#0EA5E9',
    warning: '#F59E0B',
    error: '#DC2626',

    background: '#F8FAFC',
    surface: '#FFFFFF',

    'text-primary': '#1E293B',
    'text-secondary': '#64748B',
    'text-disabled': '#94A3B8',

    border: '#E2E8F0',
    divider: '#CBD5E1',

    hover: '#F1F5F9',

    sidebar: '#FFFFFF',
    'sidebar-active': '#EEF4FF',
    'sidebar-text': '#334155',

    'table-header': '#F1F5F9',
    'table-hover': '#F8FAFC',

    card: '#FFFFFF'
  }
}

// =========================
// DARK BLUE THEME
// =========================

const blueTheme = {
  dark: true,

  colors: {
    primary: '#4F8CFF',
    'primary-lighten-1': '#7DB0FF',

    secondary: '#CBD5E1',

    success: '#22C55E',
    info: '#38BDF8',
    warning: '#FBBF24',
    error: '#F87171',

    background: '#0F172A',
    surface: '#162033',

    'text-primary': '#F8FAFC',
    'text-secondary': '#CBD5E1',

    border: '#334155',

    hover: '#273449',

    sidebar: '#111827',
    'sidebar-active': '#1D4ED8',
    'sidebar-text': '#E2E8F0',

    'table-header': '#1E293B',
    'table-hover': '#273449',

    card: '#162033'
  }
}

// =========================
// DARK PURPLE THEME
// =========================

const darkTheme = {
  dark: true,

  colors: {
    primary: '#eee',
    'primary-lighten-1': '#A78BFA',

    secondary: '#D1D5DB',

    success: '#22C55E',
    info: '#38BDF8',
    warning: '#FBBF24',
    error: '#F87171',

    background: '#111827',
    surface: '#1F2937',

    'text-primary': '#F9FAFB',
    'text-secondary': '#CBD5E1',

    border: '#374151',

    hover: '#2A3444',

    sidebar: '#0F172A',
    'sidebar-active': '#7C3AED',
    'sidebar-text': '#E5E7EB',

    'table-header': '#1F2937',
    'table-hover': '#2A3444',

    card: '#1F2937'
  }
}

// =========================
// DARK GREEN THEME
// =========================

const natureTheme = {
  dark: true,

  colors: {
    primary: '#34D399',
    'primary-lighten-1': '#6EE7B7',

    secondary: '#D1FAE5',

    success: '#22C55E',
    info: '#38BDF8',
    warning: '#FACC15',
    error: '#F87171',

    background: '#081310',
    surface: '#10201B',

    'text-primary': '#ECFDF5',
    'text-secondary': '#A7F3D0',
    'text-disabled': '#6EE7B7',

    border: '#214238',
    divider: '#2F5D50',
    hover: '#183028',

    sidebar: '060F0D',
    'sidebar-active': '#059669',
    'sidebar-text': '#D1FAE5',

    'table-header': '#10201B',
    'table-hover': '#183028',

    //Input
    'input-background': '#10201B',
    //Card
    card: '#10201B'
  }
}

// =========================
// CREATE VUETIFY
// =========================

const vuetify = createVuetify({
  components: {
    VTreeview,
  },
  theme: {
    defaultTheme: 'lightTheme',

    themes: {
      lightTheme,
      blueTheme,
      darkTheme,
      natureTheme
    }
  },
})

// =========================
// EXPORT
// =========================

export default vuetify
