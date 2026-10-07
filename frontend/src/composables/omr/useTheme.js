import { updatePrimaryPalette } from '@primeuix/themes'

export function useTheme() {
  const primaryColors = {
    blue: {
      50: '#eff6ff',
      100: '#dbeafe',
      200: '#bfdbfe',
      300: '#93c5fd',
      400: '#60a5fa',
      500: '#3b82f6',
      600: '#2563eb', // Default
      700: '#1d4ed8',
      800: '#1e40af',
      900: '#1e3a8a',
      950: '#172554'
    },
    emerald: {
      50: '#ecfdf5',
      100: '#d1fae5',
      200: '#a7f3d0',
      300: '#6ee7b7',
      400: '#34d399',
      500: '#10b981',
      600: '#059669',
      700: '#047857',
      800: '#065f46',
      900: '#064e3b',
      950: '#022c22'
    },
    violet: {
      50: '#f5f3ff',
      100: '#ede9fe',
      200: '#ddd6fe',
      300: '#c4b5fd',
      400: '#a78bfa',
      500: '#8b5cf6',
      600: '#7c3aed',
      700: '#6d28d9',
      800: '#5b21b6',
      900: '#4c1d95',
      950: '#2e1065'
    }
  }

  function setPrimaryColor(colorName) {
    if (primaryColors[colorName]) {
      updatePrimaryPalette(primaryColors[colorName])
      localStorage.setItem('primary_color', colorName)
    }
  }

  function initTheme() {
    const savedColor = localStorage.getItem('primary_color') || 'blue'
    setPrimaryColor(savedColor)
  }

  function toggleDarkMode() {
    const isDark = document.documentElement.classList.toggle('dark')
    localStorage.setItem('theme', isDark ? 'dark' : 'light')
  }

  function initDarkMode() {
    const saved = localStorage.getItem('theme') || 'light'
    if (saved === 'dark') {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }

  return {
    primaryColors,
    setPrimaryColor,
    initTheme,
    toggleDarkMode,
    initDarkMode
  }
}
