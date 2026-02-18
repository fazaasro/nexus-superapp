import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { api } from '@/api/index'

describe('Circle API', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('fetches contacts', async () => {
    const mockContacts = [
      { id: 1, name: 'John Doe', email: 'john@example.com' },
      { id: 2, name: 'Jane Smith', email: 'jane@example.com' },
    ]

    global.fetch = vi.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve(mockContacts),
      })
    )

    const contacts = await api.circle.getContacts()
    expect(contacts).toEqual(mockContacts)
    expect(global.fetch).toHaveBeenCalledWith('/api/circle/contacts')
  })

  it('creates contact', async () => {
    const contact = { name: 'John Doe', email: 'john@example.com', phone: '+1234567890' }
    const created = { id: 1, ...contact }

    global.fetch = vi.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve(created),
      })
    )

    const result = await api.circle.createContact(contact)
    expect(result).toEqual(created)
    expect(global.fetch).toHaveBeenCalledWith('/api/circle/contacts', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(contact),
    })
  })

  it('fetches health episodes', async () => {
    const mockEpisodes = [
      { id: 1, type: 'Checkup', date: '2024-02-18', notes: 'Regular checkup' },
    ]

    global.fetch = vi.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve(mockEpisodes),
      })
    )

    const episodes = await api.circle.getHealthEpisodes()
    expect(episodes).toEqual(mockEpisodes)
    expect(global.fetch).toHaveBeenCalledWith('/api/circle/health')
  })

  it('logs health episode', async () => {
    const episode = { type: 'Checkup', date: '2024-02-18', notes: 'Regular checkup' }
    const logged = { id: 1, ...episode }

    global.fetch = vi.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve(logged),
      })
    )

    const result = await api.circle.logHealthEpisode(episode)
    expect(result).toEqual(logged)
    expect(global.fetch).toHaveBeenCalledWith('/api/circle/health', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(episode),
    })
  })

  it('updates mood', async () => {
    const moodUpdate = { mood: 'happy', timestamp: '2024-02-18T10:00:00' }

    global.fetch = vi.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve({ success: true }),
      })
    )

    await api.circle.updateMood(moodUpdate.mood)
    expect(global.fetch).toHaveBeenCalledWith('/api/circle/mood', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(moodUpdate),
    })
  })

  it('fetches reminders', async () => {
    const mockReminders = [
      { id: 1, title: 'Call John', dueDate: '2024-02-20', completed: false },
    ]

    global.fetch = vi.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve(mockReminders),
      })
    )

    const reminders = await api.circle.getReminders()
    expect(reminders).toEqual(mockReminders)
    expect(global.fetch).toHaveBeenCalledWith('/api/circle/reminders')
  })

  it('deletes contact', async () => {
    global.fetch = vi.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve({ success: true }),
      })
    )

    await api.circle.deleteContact(1)
    expect(global.fetch).toHaveBeenCalledWith('/api/circle/contacts/1', {
      method: 'DELETE',
    })
  })
})
