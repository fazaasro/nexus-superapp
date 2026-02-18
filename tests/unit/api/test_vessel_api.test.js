import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { api } from '@/api/index'

describe('Vessel API', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('fetches workouts', async () => {
    const mockWorkouts = [
      { id: 1, type: 'Running', duration: 30, calories: 300, date: '2024-02-18' },
      { id: 2, type: 'Cycling', duration: 45, calories: 400, date: '2024-02-17' },
    ]

    global.fetch = vi.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve(mockWorkouts),
      })
    )

    const workouts = await api.vessel.getWorkouts()
    expect(workouts).toEqual(mockWorkouts)
    expect(global.fetch).toHaveBeenCalledWith('/api/vessel/workouts')
  })

  it('logs workout', async () => {
    const workout = { type: 'Running', duration: 30, calories: 300, date: '2024-02-18' }
    const logged = { id: 1, ...workout }

    global.fetch = vi.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve(logged),
      })
    )

    const result = await api.vessel.logWorkout(workout)
    expect(result).toEqual(logged)
    expect(global.fetch).toHaveBeenCalledWith('/api/vessel/workouts', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(workout),
    })
  })

  it('fetches biometrics', async () => {
    const mockBiometrics = [
      { id: 1, type: 'Weight', value: 70, unit: 'kg', date: '2024-02-18' },
      { id: 2, type: 'Heart Rate', value: 72, unit: 'bpm', date: '2024-02-18' },
    ]

    global.fetch = vi.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve(mockBiometrics),
      })
    )

    const biometrics = await api.vessel.getBiometrics()
    expect(biometrics).toEqual(mockBiometrics)
    expect(global.fetch).toHaveBeenCalledWith('/api/vessel/biometrics')
  })

  it('adds biometric data', async () => {
    const biometric = { type: 'Weight', value: 70, unit: 'kg', date: '2024-02-18' }
    const added = { id: 1, ...biometric }

    global.fetch = vi.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve(added),
      })
    )

    const result = await api.vessel.addBiometric(biometric)
    expect(result).toEqual(added)
    expect(global.fetch).toHaveBeenCalledWith('/api/vessel/biometrics', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(biometric),
    })
  })

  it('fetches Blueprint schedule', async () => {
    const mockSchedule = [
      { id: 1, type: 'Workout', frequency: 'daily', time: '07:00' },
      { id: 2, type: 'Meditation', frequency: 'daily', time: '21:00' },
    ]

    global.fetch = vi.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve(mockSchedule),
      })
    )

    const schedule = await api.vessel.getBlueprintSchedule()
    expect(schedule).toEqual(mockSchedule)
    expect(global.fetch).toHaveBeenCalledWith('/api/vessel/blueprint')
  })

  it('adds Blueprint schedule', async () => {
    const schedule = { type: 'Workout', frequency: 'daily', time: '07:00' }
    const added = { id: 1, ...schedule }

    global.fetch = vi.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve(added),
      })
    )

    const result = await api.vessel.addBlueprintSchedule(schedule)
    expect(result).toEqual(added)
    expect(global.fetch).toHaveBeenCalledWith('/api/vessel/blueprint', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(schedule),
    })
  })

  it('deletes workout', async () => {
    global.fetch = vi.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve({ success: true }),
      })
    )

    await api.vessel.deleteWorkout(1)
    expect(global.fetch).toHaveBeenCalledWith('/api/vessel/workouts/1', {
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

    await expect(api.vessel.getWorkouts()).rejects.toThrow()
  })
})
