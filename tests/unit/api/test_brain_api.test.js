import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { api } from '@/api/index'

describe('Brain API', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('fetches knowledge entries', async () => {
    const mockEntries = [
      { id: 1, title: 'Python', content: 'Learn Python', tags: ['python'] },
      { id: 2, title: 'JavaScript', content: 'Learn JS', tags: ['javascript'] },
    ]

    global.fetch = vi.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve(mockEntries),
      })
    )

    const entries = await api.brain.getEntries()
    expect(entries).toEqual(mockEntries)
    expect(global.fetch).toHaveBeenCalledWith('/api/brain/entries')
  })

  it('creates knowledge entry', async () => {
    const entry = { title: 'Test', content: 'Content', tags: ['test'] }
    const created = { id: 1, ...entry, createdAt: '2024-02-18' }

    global.fetch = vi.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve(created),
      })
    )

    const result = await api.brain.createEntry(entry)
    expect(result).toEqual(created)
    expect(global.fetch).toHaveBeenCalledWith('/api/brain/entries', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(entry),
    })
  })

  it('generates Anki cards', async () => {
    const mockCards = [
      { front: 'What is Python?', back: 'A programming language' },
      { front: 'Python uses...', back: 'Indentation' },
    ]

    global.fetch = vi.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve(mockCards),
      })
    )

    const cards = await api.brain.generateAnkiCards(1)
    expect(cards).toEqual(mockCards)
    expect(global.fetch).toHaveBeenCalledWith('/api/brain/entries/1/anki', {
      method: 'POST',
    })
  })

  it('searches entries', async () => {
    const mockResults = [
      { id: 1, title: 'Python Programming', content: 'Learn Python', tags: ['python'] },
    ]

    global.fetch = vi.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve(mockResults),
      })
    )

    const results = await api.brain.searchEntries('Python')
    expect(results).toEqual(mockResults)
    expect(global.fetch).toHaveBeenCalledWith('/api/brain/search?q=Python')
  })

  it('deletes entry', async () => {
    global.fetch = vi.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve({ success: true }),
      })
    )

    await api.brain.deleteEntry(1)
    expect(global.fetch).toHaveBeenCalledWith('/api/brain/entries/1', {
      method: 'DELETE',
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

    await expect(api.brain.getEntries()).rejects.toThrow()
  })
})
