import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { api } from '@/api/index'

describe('Bag API', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('fetches transactions', async () => {
    const mockTransactions = [
      { id: 1, amount: 100, category: 'Food', date: '2024-02-18' },
      { id: 2, amount: -50, category: 'Transport', date: '2024-02-18' },
    ]

    global.fetch = vi.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve(mockTransactions),
      })
    )

    const transactions = await api.bag.getTransactions()
    expect(transactions).toEqual(mockTransactions)
    expect(global.fetch).toHaveBeenCalledWith('/api/bag/transactions')
  })

  it('creates transaction', async () => {
    const transaction = { amount: 100, category: 'Food', date: '2024-02-18' }
    const created = { id: 1, ...transaction }

    global.fetch = vi.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve(created),
      })
    )

    const result = await api.bag.createTransaction(transaction)
    expect(result).toEqual(created)
    expect(global.fetch).toHaveBeenCalledWith('/api/bag/transactions', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(transaction),
    })
  })

  it('uploads receipt image', async () => {
    const file = new File(['test'], 'receipt.jpg', { type: 'image/jpeg' })
    const mockResult = {
      id: 1,
      text: 'Test receipt text',
      amount: 100,
      category: 'Food',
    }

    const formData = new FormData()
    formData.append('file', file)

    global.fetch = vi.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve(mockResult),
      })
    )

    const result = await api.bag.uploadReceipt(file)
    expect(result).toEqual(mockResult)
    expect(global.fetch).toHaveBeenCalledWith('/api/bag/upload', {
      method: 'POST',
      body: formData,
    })
  })

  it('handles API errors', async () => {
    global.fetch = vi.fn(() =>
      Promise.resolve({
        ok: false,
        status: 500,
        json: () => Promise.resolve({ error: 'Server error' }),
      })
    )

    await expect(api.bag.getTransactions()).rejects.toThrow()
  })

  it('deletes transaction', async () => {
    global.fetch = vi.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve({ success: true }),
      })
    )

    await api.bag.deleteTransaction(1)
    expect(global.fetch).toHaveBeenCalledWith('/api/bag/transactions/1', {
      method: 'DELETE',
    })
  })
})
