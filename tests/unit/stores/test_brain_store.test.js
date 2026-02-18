import { describe, it, expect, beforeEach } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'
import { useBrainStore } from '@/stores/brain'

describe('Brain Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('initializes with empty knowledge base', () => {
    const store = useBrainStore()
    expect(store.entries).toEqual([])
    expect(store.worktree).toEqual([])
  })

  it('adds knowledge entry', async () => {
    const store = useBrainStore()
    const entry = {
      id: 1,
      title: 'Test Entry',
      content: 'Test content',
      tags: ['test'],
      createdAt: '2024-02-18',
    }

    await store.addEntry(entry)

    expect(store.entries).toHaveLength(1)
    expect(store.entries[0]).toEqual(entry)
  })

  it('searches knowledge entries', async () => {
    const store = useBrainStore()

    await store.addEntry({
      id: 1,
      title: 'Python Programming',
      content: 'Learn Python basics',
      tags: ['python', 'programming'],
      createdAt: '2024-02-18',
    })

    await store.addEntry({
      id: 2,
      title: 'JavaScript Guide',
      content: 'Master JavaScript',
      tags: ['javascript', 'programming'],
      createdAt: '2024-02-18',
    })

    const results = store.searchEntries('Python')
    expect(results).toHaveLength(1)
    expect(results[0].title).toBe('Python Programming')
  })

  it('generates Anki cards from entry', async () => {
    const store = useBrainStore()

    await store.addEntry({
      id: 1,
      title: 'Test Entry',
      content: 'Key fact to remember',
      tags: ['test'],
      createdAt: '2024-02-18',
    })

    const cards = await store.generateAnkiCards(1)
    expect(cards).toBeDefined()
    expect(cards.length).toBeGreaterThan(0)
  })

  it('adds to worktree', async () => {
    const store = useBrainStore()

    await store.addToWorktree({ id: 1, title: 'Test', parentId: null })
    expect(store.worktree).toHaveLength(1)
  })

  it('deletes entry', async () => {
    const store = useBrainStore()

    await store.addEntry({
      id: 1,
      title: 'Test Entry',
      content: 'Test content',
      tags: ['test'],
      createdAt: '2024-02-18',
    })

    await store.deleteEntry(1)
    expect(store.entries).toHaveLength(0)
  })

  it('persists to localStorage', async () => {
    const store = useBrainStore()
    const entry = { id: 1, title: 'Test', content: 'Content', tags: [], createdAt: '2024-02-18' }

    await store.addEntry(entry)
    const saved = localStorage.getItem('nexus-brain-store')
    expect(saved).toBeTruthy()
  })
})
