import { describe, it, expect, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import CircleView from '@/views/CircleView.vue'
import { createPinia, setActivePinia } from 'pinia'
import { useCircleStore } from '@/stores/circle'

describe('CircleView', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('renders the social network interface', () => {
    const wrapper = mount(CircleView)
    expect(wrapper.find('.social-network').exists()).toBe(true)
  })

  it('displays contacts list', () => {
    const wrapper = mount(CircleView)
    expect(wrapper.find('.contacts-list').exists()).toBe(true)
  })

  it('allows adding new contact', async () => {
    const wrapper = mount(CircleView)
    const circleStore = useCircleStore()

    await wrapper.vm.addContact({
      name: 'John Doe',
      email: 'john@example.com',
      phone: '+1234567890',
    })

    expect(circleStore.contacts).toHaveLength(1)
  })

  it('logs health episodes', async () => {
    const wrapper = mount(CircleView)
    await wrapper.vm.logHealthEpisode({
      type: 'Checkup',
      date: '2024-02-18',
      notes: 'Regular checkup',
    })
    expect(wrapper.vm.healthEpisodes).toBeDefined()
  })

  it('tracks mood updates', async () => {
    const wrapper = mount(CircleView)
    await wrapper.vm.updateMood('happy')
    expect(wrapper.vm.currentMood).toBe('happy')
  })

  it('displays reminders', () => {
    const wrapper = mount(CircleView)
    expect(wrapper.find('.reminders-list').exists()).toBe(true)
  })

  it('is responsive on mobile', () => {
    global.innerWidth = 375
    const wrapper = mount(CircleView)
    expect(wrapper.find('.mobile-contact-card').exists()).toBe(true)
  })
})
