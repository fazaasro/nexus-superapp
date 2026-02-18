// Vuetify
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

export default createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'dark',
    themes: {
      light: {
        dark: false,
        colors: {
          primary: '#6366f1', // Indigo
          secondary: '#8b5cf6', // Violet
          accent: '#06b6d4', // Cyan
          success: '#10b981', // Emerald
          warning: '#f59e0b', // Amber
          error: '#ef4444', // Red
          info: '#3b82f6', // Blue
          surface: '#f8fafc',
          background: '#ffffff'
        }
      },
      dark: {
        dark: true,
        colors: {
          primary: '#818cf8', // Light Indigo
          secondary: '#a78bfa', // Light Violet
          accent: '#22d3ee', // Light Cyan
          success: '#34d399', // Light Emerald
          warning: '#fbbf24', // Light Amber
          error: '#f87171', // Light Red
          info: '#60a5fa', // Light Blue
          surface: '#1e293b',
          background: '#0f172a'
        }
      }
    }
  },
  display: {
    mobileBreakpoint: 'sm',
    thresholds: {
      xs: 0,
      sm: 600,
      md: 960,
      lg: 1280,
      xl: 1920,
    },
  },
})
