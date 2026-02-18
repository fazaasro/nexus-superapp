import { defineConfig } from 'vitest/config'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath } from 'node:url'

export default defineConfig({
  plugins: [vue()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['./tests/setup.js'],
    include: ['tests/unit/**/*.test.js', 'tests/integration/**/*.test.js'],
    exclude: ['tests/e2e/**/*'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      include: ['web-ui/src/**/*.{js,vue}'],
      exclude: [
        'node_modules/',
        'tests/',
        '*.config.js',
        '**/*.spec.js',
      ],
      statements: 70,
      branches: 70,
      functions: 70,
      lines: 70,
    },
  },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./web-ui/src', import.meta.url)),
    },
  },
})
