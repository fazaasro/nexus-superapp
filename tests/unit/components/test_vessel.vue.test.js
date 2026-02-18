import { describe, it, expect, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import VesselView from '@/views/VesselView.vue'
import { createPinia, setActivePinia } from 'pinia'
import { useVesselStore } from '@/stores/vessel'

describe('VesselView', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('renders the health dashboard', () => {
    const wrapper = mount(VesselView)
    expect(wrapper.find('.health-dashboard').exists()).toBe(true)
  })

  it('displays Blueprint metrics', () => {
    const wrapper = mount(VesselView)
    expect(wrapper.find('.blueprint-metrics').exists()).toBe(true)
  })

  it('logs workout sessions', async () => {
    const wrapper = mount(VesselView)
    const vesselStore = useVesselStore()

    await wrapper.vm.logWorkout({
      type: 'Running',
      duration: 30,
      calories: 300,
      date: '2024-02-18',
    })

    expect(vesselStore.workouts).toHaveLength(1)
  })

  it('tracks biometrics', async () => {
    const wrapper = mount(VesselView)
    await wrapper.vm.addBiometric({
      type: 'Weight',
      value: 70,
      unit: 'kg',
      date: '2024-02-18',
    })
    expect(wrapper.vm.biometrics).toBeDefined()
  })

  it('displays health trends', () => {
    const wrapper = mount(VesselView)
    expect(wrapper.find('.health-trends').exists()).toBe(true)
  })

  it('shows Blueprint schedule', () => {
    const wrapper = mount(VesselView)
    expect(wrapper.find('.blueprint-schedule').exists()).toBe(true)
  })

  it('is responsive on mobile', () => {
    global.innerWidth = 375
    const wrapper = mount(VesselView)
    expect(wrapper.find('.mobile-health-card').exists()).toBe(true)
  })
})
