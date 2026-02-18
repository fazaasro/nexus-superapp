import { describe, it, expect, beforeEach } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'
import { useBagStore } from '@/stores/bag'

describe('Bag Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('initializes with empty transactions', () => {
    const store = useBagStore()
    expect(store.transactions).toEqual([])
    expect(store.totalBalance).toBe(0)
  })

  it('adds transaction correctly', async () => {
    const store = useBagStore()
    const transaction = {
      id: 1,
      amount: 100,
      category: 'Food',
      date: '2024-02-18',
    }

    await store.addTransaction(transaction)

    expect(store.transactions).toHaveLength(1)
    expect(store.transactions[0]).toEqual(transaction)
  })

  it('calculates total balance correctly', async () => {
    const store = useBagStore()

    await store.addTransaction({ id: 1, amount: 100, category: 'Income', date: '2024-02-18' })
    await store.addTransaction({ id: 2, amount: -50, category: 'Food', date: '2024-02-18' })

    expect(store.totalBalance).toBe(50)
  })

  it('filters transactions by category', async () => {
    const store = useBagStore()

    await store.addTransaction({ id: 1, amount: 100, category: 'Food', date: '2024-02-18' })
    await store.addTransaction({ id: 2, amount: 50, category: 'Transport', date: '2024-02-18' })

    const foodTransactions = store.getTransactionsByCategory('Food')
    expect(foodTransactions).toHaveLength(1)
    expect(foodTransactions[0].category).toBe('Food')
  })

  it('updates transaction', async () => {
    const store = useBagStore()

    await store.addTransaction({ id: 1, amount: 100, category: 'Food', date: '2024-02-18' })
    await store.updateTransaction(1, { amount: 150 })

    expect(store.transactions[0].amount).toBe(150)
  })

  it('deletes transaction', async () => {
    const store = useBagStore()

    await store.addTransaction({ id: 1, amount: 100, category: 'Food', date: '2024-02-18' })
    await store.deleteTransaction(1)

    expect(store.transactions).toHaveLength(0)
  })

  it('persists to localStorage', async () => {
    const store = useBagStore()
    const transaction = { id: 1, amount: 100, category: 'Food', date: '2024-02-18' }

    await store.addTransaction(transaction)
    const saved = localStorage.getItem('nexus-bag-store')
    expect(saved).toBeTruthy()
  })
})
