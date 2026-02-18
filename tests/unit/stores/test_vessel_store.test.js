import { describe, it, expect, beforeEach } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'
import { useVesselStore } from '@/stores/vessel'

describe('Vessel Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('initializes with empty health data', () => {
    const store = useVesselStore()
    expect(store.workouts).toEqual([])
    expect(store.biometrics).toEqual([])
    expect(store.blueprintSchedule).toEqual([])
  })

  it('logs workout session', async () => {
    const store = useVesselStore()
    const workout = {
      id: 1,
      type: 'Running',
      duration: 30,
      calories: 300,
      date: '2024-02-18',
    }

    await store.logWorkout(workout)

    expect(store.workouts).toHaveLength(1)
    expect(store.workouts[0]).toEqual(workout)
  })

  it('adds biometric data', async () => {
    const store = useVesselStore()
    const biometric = {
      id: 1,
      type: 'Weight',
      value: 70,
      unit: 'kg',
      date: '2024-02-18',
    }

    await store.addBiometric(biometric)

    expect(store.biometrics).toHaveLength(1)
    expect(store.biometrics[0]).toEqual(biometric)
  })

  it('calculates health trends', async () => {
    const store = useVesselStore()

    await store.addBiometric({ id: 1, type: 'Weight', value: 75, unit: 'kg', date: '2024-02-10' })
    await store.addBiometric({ id: 2, type: 'Weight', value: 73, unit: 'kg', date: '2024-02-15' })
    await store.addBiometric({ id: 3, type: 'Weight', value: 70, unit: 'kg', date: '2024-02-18' })

    const trend = store.getBiometricTrend('Weight')
    expect(trend).toBeDefined()
    expect(trend.change).toBeLessThan(0) // Losing weight
  })

  it('adds Blueprint schedule', async () => {
    const store = useVesselStore()
    const schedule = {
      id: 1,
      type: 'Workout',
      frequency: 'daily',
      time: '07:00',
    }

    await store.addBlueprintSchedule(schedule)

    expect(store.blueprintSchedule).toHaveLength(1)
    expect(store.blueprintSchedule[0]).toEqual(schedule)
  })

  it('deletes workout', async () => {
    const store = useVesselStore()

    await store.logWorkout({
      id: 1,
      type: 'Running',
      duration: 30,
      calories: 300,
      date: '2024-02-18',
    })

    await store.deleteWorkout(1)
    expect(store.workouts).toHaveLength(0)
  })

  it('calculates weekly workout stats', async () => {
    const store = useVesselStore()

    await store.logWorkout({ id: 1, type: 'Running', duration: 30, calories: 300, date: '2024-02-18' })
    await store.logWorkout({ id: 2, type: 'Cycling', duration: 45, calories: 400, date: '2024-02-17' })

    const stats = store.getWeeklyWorkoutStats()
    expect(stats.totalDuration).toBe(75)
    expect(stats.totalCalories).toBe(700)
    expect(stats.workoutCount).toBe(2)
  })

  it('persists to localStorage', async () => {
    const store = useVesselStore()
    const workout = { id: 1, type: 'Running', duration: 30, calories: 300, date: '2024-02-18' }

    await store.logWorkout(workout)
    const saved = localStorage.getItem('nexus-vessel-store')
    expect(saved).toBeTruthy()
  })
})
