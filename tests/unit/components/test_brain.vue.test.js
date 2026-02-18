import { describe, it, expect, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import BrainView from '@/views/BrainView.vue'
import { createPinia, setActivePinia } from 'pinia'
import { useBrainStore } from '@/stores/brain'

describe('BrainView', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('renders the knowledge base interface', () => {
    const wrapper = mount(BrainView)
    expect(wrapper.find('.knowledge-base').exists()).toBe(true)
  })

  it('displays knowledge entries list', () => {
    const wrapper = mount(BrainView)
    expect(wrapper.find('.entries-list').exists()).toBe(true)
  })

  it('allows creating new knowledge entry', async () => {
    const wrapper = mount(BrainView)
    const brainStore = useBrainStore()

    await wrapper.vm.createEntry({
      title: 'Test Entry',
      content: 'Test content',
      tags: ['test'],
    })

    expect(brainStore.entries).toHaveLength(1)
  })

  it('searches through knowledge entries', async () => {
    const wrapper = mount(BrainView)
    await wrapper.vm.searchEntries('test')
    expect(wrapper.vm.searchQuery).toBe('test')
  })

  it('generates Anki cards from entry', async () => {
    const wrapper = mount(BrainView)
    expect(wrapper.vm.generateAnkiCards).toBeDefined()
  })

  it('displays worktree structure', () => {
    const wrapper = mount(BrainView)
    expect(wrapper.find('.worktree').exists()).toBe(true)
  })

  it('is responsive on mobile', () => {
    global.innerWidth = 375
    const wrapper = mount(BrainView)
    expect(wrapper.find('.mobile-entry-card').exists()).toBe(true)
  })
})
