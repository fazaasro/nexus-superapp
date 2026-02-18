import { describe, it, expect, beforeEach } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'
import { useCircleStore } from '@/stores/circle'

describe('Circle Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('initializes with empty state', () => {
    const store = useCircleStore()
    expect(store.contacts).toEqual([])
    expect(store.healthEpisodes).toEqual([])
    expect(store.moodHistory).toEqual([])
    expect(store.reminders).toEqual([])
  })

  it('adds contact', async () => {
    const store = useCircleStore()
    const contact = {
      id: 1,
      name: 'John Doe',
      email: 'john@example.com',
      phone: '+1234567890',
    }

    await store.addContact(contact)

    expect(store.contacts).toHaveLength(1)
    expect(store.contacts[0]).toEqual(contact)
  })

  it('logs health episode', async () => {
    const store = useCircleStore()
    const episode = {
      id: 1,
      type: 'Checkup',
      date: '2024-02-18',
      notes: 'Regular checkup',
    }

    await store.logHealthEpisode(episode)

    expect(store.healthEpisodes).toHaveLength(1)
    expect(store.healthEpisodes[0]).toEqual(episode)
  })

  it('tracks mood updates', async () => {
    const store = useCircleStore()

    await store.updateMood('happy')
    await store.updateMood('sad')

    expect(store.moodHistory).toHaveLength(2)
    expect(store.currentMood).toBe('sad')
  })

  it('adds reminder', async () => {
    const store = useCircleStore()
    const reminder = {
      id: 1,
      title: 'Call John',
      dueDate: '2024-02-20',
      completed: false,
    }

    await store.addReminder(reminder)

    expect(store.reminders).toHaveLength(1)
    expect(store.reminders[0]).toEqual(reminder)
  })

  it('completes reminder', async () => {
    const store = useCircleStore()

    await store.addReminder({
      id: 1,
      title: 'Call John',
      dueDate: '2024-02-20',
      completed: false,
    })

    await store.completeReminder(1)
    expect(store.reminders[0].completed).toBe(true)
  })

  it('deletes contact', async () => {
    const store = useCircleStore()

    await store.addContact({
      id: 1,
      name: 'John Doe',
      email: 'john@example.com',
      phone: '+1234567890',
    })

    await store.deleteContact(1)
    expect(store.contacts).toHaveLength(0)
  })

  it('persists to localStorage', async () => {
    const store = useCircleStore()
    const contact = { id: 1, name: 'John', email: 'john@example.com', phone: '+1234567890' }

    await store.addContact(contact)
    const saved = localStorage.getItem('nexus-circle-store')
    expect(saved).toBeTruthy()
  })
})
