import { describe, it, expect, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import BagView from '@/views/BagView.vue'
import { createPinia, setActivePinia } from 'pinia'
import { useBagStore } from '@/stores/bag'

describe('BagView', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('renders the bag transactions list', () => {
    const wrapper = mount(BagView)
    expect(wrapper.find('.transactions-list').exists()).toBe(true)
  })

  it('displays transaction form', () => {
    const wrapper = mount(BagView)
    expect(wrapper.find('.transaction-form').exists()).toBe(true)
  })

  it('allows adding new transaction', async () => {
    const wrapper = mount(BagView)
    const bagStore = useBagStore()

    await wrapper.vm.addTransaction({
      amount: 100,
      category: 'Food',
      date: '2024-02-18',
    })

    expect(bagStore.transactions).toHaveLength(1)
  })

  it('shows upload button for receipt images', () => {
    const wrapper = mount(BagView)
    expect(wrapper.find('.upload-receipt').exists()).toBe(true)
  })

  it('filters transactions by category', async () => {
    const wrapper = mount(BagView)
    await wrapper.vm.setCategoryFilter('Food')
    expect(wrapper.vm.categoryFilter).toBe('Food')
  })

  it('displays total balance', () => {
    const wrapper = mount(BagView)
    expect(wrapper.find('.total-balance').exists()).toBe(true)
  })

  it('is responsive on mobile', () => {
    global.innerWidth = 375
    const wrapper = mount(BagView)
    expect(wrapper.find('.mobile-transaction-card').exists()).toBe(true)
  })
})
