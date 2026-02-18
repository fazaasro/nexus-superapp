import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { circleAPI } from '../api'

export const useCircleStore = defineStore('circle', () => {
  // State
  const contacts = ref([])
  const healthLogs = ref([])
  const checkins = ref([])
  const reminders = ref([])
  const stats = ref(null)
  const loading = ref(false)
  const error = ref(null)

  // Computed
  const innerCircleContacts = computed(() => contacts.value.filter(c => c.inner_circle))
  const recentHealthLogs = computed(() => healthLogs.value.slice(0, 20))
  const recentCheckins = computed(() => checkins.value.slice(0, 20))
  const pendingReminders = computed(() => reminders.value.filter(r => !r.completed))

  // Actions
  async function fetchContacts(params = {}) {
    loading.value = true
    error.value = null
    try {
      const result = await circleAPI.getContacts(params)
      contacts.value = result.contacts || []
      return contacts.value
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchContact(contactId) {
    loading.value = true
    error.value = null
    try {
      const contact = await circleAPI.getContact(contactId)
      const index = contacts.value.findIndex(c => c.id === contactId)
      if (index !== -1) {
        contacts.value[index] = contact
      }
      return contact
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function createContact(data) {
    loading.value = true
    error.value = null
    try {
      const result = await circleAPI.createContact(data)
      contacts.value.unshift(result)
      return result
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function updateContact(contactId, data) {
    loading.value = true
    error.value = null
    try {
      const result = await circleAPI.updateContact(contactId, data)
      const index = contacts.value.findIndex(c => c.id === contactId)
      if (index !== -1) {
        contacts.value[index] = result
      }
      return result
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function recordContact(contactId) {
    loading.value = true
    error.value = null
    try {
      const result = await circleAPI.recordContact(contactId)
      const contact = contacts.value.find(c => c.id === contactId)
      if (contact) {
        contact.last_contacted = new Date().toISOString()
      }
      return result
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchHealthLogs(params = {}) {
    loading.value = true
    error.value = null
    try {
      const result = await circleAPI.getHealthLogs(params)
      healthLogs.value = result.logs || []
      return healthLogs.value
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function createHealthLog(data) {
    loading.value = true
    error.value = null
    try {
      const result = await circleAPI.createHealthLog(data)
      healthLogs.value.unshift(result)
      return result
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function analyzeHealth(owner, symptomType, days = 30) {
    loading.value = true
    error.value = null
    try {
      const result = await circleAPI.analyzeHealth(owner, symptomType, days)
      return result
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchCheckins(params = {}) {
    loading.value = true
    error.value = null
    try {
      const result = await circleAPI.getCheckins(params)
      checkins.value = result.checkins || []
      return checkins.value
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function createCheckin(data) {
    loading.value = true
    error.value = null
    try {
      const result = await circleAPI.createCheckin(data)
      checkins.value.unshift(result)
      return result
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchCheckinTrends(days = 30) {
    loading.value = true
    error.value = null
    try {
      const result = await circleAPI.getCheckinTrends(days)
      return result
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchReminders() {
    loading.value = true
    error.value = null
    try {
      reminders.value = await circleAPI.getReminders()
      return reminders.value
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchStats() {
    loading.value = true
    error.value = null
    try {
      stats.value = await circleAPI.getStats()
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
    contacts,
    healthLogs,
    checkins,
    reminders,
    stats,
    loading,
    error,

    // Computed
    innerCircleContacts,
    recentHealthLogs,
    recentCheckins,
    pendingReminders,

    // Actions
    fetchContacts,
    fetchContact,
    createContact,
    updateContact,
    recordContact,
    fetchHealthLogs,
    createHealthLog,
    analyzeHealth,
    fetchCheckins,
    createCheckin,
    fetchCheckinTrends,
    fetchReminders,
    fetchStats,
    clearError,
  }
})
