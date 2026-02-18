import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import HomeView from '@/views/HomeView.vue'
import { createPinia, setActivePinia } from 'pinia'

describe('HomeView', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('renders the home page', () => {
    const wrapper = mount(HomeView)
    expect(wrapper.exists()).toBe(true)
  })

  it('displays navigation cards for all modules', () => {
    const wrapper = mount(HomeView)
    const modules = ['bag', 'brain', 'circle', 'vessel']
    modules.forEach(module => {
      expect(wrapper.text().toLowerCase()).toContain(module)
    })
  })

  it('responds to dark mode toggle', async () => {
    const wrapper = mount(HomeView)
    expect(wrapper.vm.darkMode).toBeDefined()
    await wrapper.vm.toggleDarkMode()
    // Verify dark mode state changes
  })

  it('is responsive on mobile viewport', () => {
    global.innerWidth = 375
    const wrapper = mount(HomeView)
    expect(wrapper.find('.mobile-nav').exists()).toBe(true)
  })

  it('is responsive on tablet viewport', () => {
    global.innerWidth = 768
    const wrapper = mount(HomeView)
    expect(wrapper.find('.tablet-nav').exists()).toBe(true)
  })
})
