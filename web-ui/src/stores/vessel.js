import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { vesselAPI } from '../api'

export const useVesselStore = defineStore('vessel', () => {
  // State
  const blueprintLogs = ref([])
  const workouts = ref([])
  const biometrics = ref([])
  const sobrietyTrackers = ref([])
  const analytics = ref(null)
  const stats = ref(null)
  const loading = ref(false)
  const error = ref(null)

  // Computed
  const recentWorkouts = computed(() => workouts.value.slice(0, 20))
  const recentBiometrics = computed(() => biometrics.value.slice(0, 20))
  const todaysBlueprint = computed(() => {
    const today = new Date().toISOString().split('T')[0]
    return blueprintLogs.value.find(log => log.date === today)
  })
  const totalWorkoutTime = computed(() => {
    return workouts.value.reduce((sum, w) => sum + (w.duration || 0), 0)
  })

  // Actions
  async function fetchBlueprintLogs(params = {}) {
    loading.value = true
    error.value = null
    try {
      const result = await vesselAPI.getBlueprintLogs(params)
      blueprintLogs.value = result.logs || []
      return blueprintLogs.value
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchBlueprintLog(logDate, owner) {
    loading.value = true
    error.value = null
    try {
      const log = await vesselAPI.getBlueprintLog(logDate, owner)
      const index = blueprintLogs.value.findIndex(l => l.date === logDate)
      if (index !== -1) {
        blueprintLogs.value[index] = log
      } else {
        blueprintLogs.value.unshift(log)
      }
      return log
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function logBlueprint(data) {
    loading.value = true
    error.value = null
    try {
      const result = await vesselAPI.logBlueprint(data)
      const index = blueprintLogs.value.findIndex(l => l.date === result.date)
      if (index !== -1) {
        blueprintLogs.value[index] = result
      } else {
        blueprintLogs.value.unshift(result)
      }
      return result
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchWorkouts(params = {}) {
    loading.value = true
    error.value = null
    try {
      const result = await vesselAPI.getWorkouts(params)
      workouts.value = result.workouts || []
      return workouts.value
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchWorkoutStats(owner, days = 30) {
    loading.value = true
    error.value = null
    try {
      const result = await vesselAPI.getWorkoutStats(owner, days)
      return result
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function logWorkout(data) {
    loading.value = true
    error.value = null
    try {
      const result = await vesselAPI.logWorkout(data)
      workouts.value.unshift(result)
      return result
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchBiometrics(params = {}) {
    loading.value = true
    error.value = null
    try {
      const result = await vesselAPI.getBiometrics(params)
      biometrics.value = result.biometrics || []
      return biometrics.value
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchBiometricTrends(owner, days = 30) {
    loading.value = true
    error.value = null
    try {
      const result = await vesselAPI.getBiometricTrends(owner, days)
      return result
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function logBiometrics(data) {
    loading.value = true
    error.value = null
    try {
      const result = await vesselAPI.logBiometrics(data)
      biometrics.value.unshift(result)
      return result
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchSobrietyTracker(trackerId) {
    loading.value = true
    error.value = null
    try {
      const tracker = await vesselAPI.getSobrietyTracker(trackerId)
      const index = sobrietyTrackers.value.findIndex(t => t.id === trackerId)
      if (index !== -1) {
        sobrietyTrackers.value[index] = tracker
      }
      return tracker
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function startSobrietyTracker(data) {
    loading.value = true
    error.value = null
    try {
      const result = await vesselAPI.startSobrietyTracker(data)
      sobrietyTrackers.value.unshift(result)
      return result
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function logRelapse(trackerId, data) {
    loading.value = true
    error.value = null
    try {
      const result = await vesselAPI.logRelapse(trackerId, data)
      const index = sobrietyTrackers.value.findIndex(t => t.id === trackerId)
      if (index !== -1) {
        sobrietyTrackers.value[index] = result
      }
      return result
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchAnalytics(owner, days = 30) {
    loading.value = true
    error.value = null
    try {
      analytics.value = await vesselAPI.getAnalytics(owner, days)
      return analytics.value
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchStats(owner) {
    loading.value = true
    error.value = null
    try {
      stats.value = await vesselAPI.getStats(owner)
      return stats.value
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  function clearError() {
    error.value = null
  }

  return {
    // State
    blueprintLogs,
    workouts,
    biometrics,
    sobrietyTrackers,
    analytics,
    stats,
    loading,
    error,

    // Computed
    recentWorkouts,
    recentBiometrics,
    todaysBlueprint,
    totalWorkoutTime,

    // Actions
    fetchBlueprintLogs,
    fetchBlueprintLog,
    logBlueprint,
    fetchWorkouts,
    fetchWorkoutStats,
    logWorkout,
    fetchBiometrics,
    fetchBiometricTrends,
    logBiometrics,
    fetchSobrietyTracker,
    startSobrietyTracker,
    logRelapse,
    fetchAnalytics,
    fetchStats,
    clearError,
  }
})
