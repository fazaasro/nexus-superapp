import { vi } from 'vitest'
import { config } from '@vue/test-utils'

// Global mocks
global.fetch = vi.fn()

// Mock localStorage
const localStorageMock = {
  getItem: vi.fn(),
  setItem: vi.fn(),
  removeItem: vi.fn(),
  clear: vi.fn(),
}
global.localStorage = localStorageMock

// Vite config for Vue components
config.global.stubs = {
  transition: false,
  'transition-group': false,
}
