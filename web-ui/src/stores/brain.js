import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { brainAPI } from '../api'

export const useBrainStore = defineStore('brain', () => {
  // State
  const entries = ref([])
  const worktrees = ref([])
  const searchResults = ref([])
  const stats = ref(null)
  const loading = ref(false)
  const error = ref(null)

  // Computed
  const entryCount = computed(() => entries.value.length)
  const activeWorktrees = computed(() => worktrees.value.filter(w => w.status === 'active'))
  const recentEntries = computed(() => entries.value.slice(0, 10))

  // Actions
  async function fetchEntries(params = {}) {
    loading.value = true
    error.value = null
    try {
      const result = await brainAPI.getEntries(params)
      entries.value = result.entries || []
      return entries.value
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchEntry(entryId) {
    loading.value = true
    error.value = null
    try {
      const entry = await brainAPI.getEntry(entryId)
      const index = entries.value.findIndex(e => e.id === entryId)
      if (index !== -1) {
        entries.value[index] = entry
      }
      return entry
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function createEntry(data) {
    loading.value = true
    error.value = null
    try {
      const result = await brainAPI.createEntry(data)
      entries.value.unshift(result)
      return result
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function updateEntry(entryId, data) {
    loading.value = true
    error.value = null
    try {
      const result = await brainAPI.updateEntry(entryId, data)
      const index = entries.value.findIndex(e => e.id === entryId)
      if (index !== -1) {
        entries.value[index] = result
      }
      return result
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function deleteEntry(entryId) {
    loading.value = true
    error.value = null
    try {
      await brainAPI.deleteEntry(entryId)
      entries.value = entries.value.filter(e => e.id !== entryId)
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function searchEntries(query, params = {}) {
    loading.value = true
    error.value = null
    try {
      const result = await brainAPI.search(query, params)
      searchResults.value = result.results || []
      return searchResults.value
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function createAnkiCard(entryId) {
    loading.value = true
    error.value = null
    try {
      const result = await brainAPI.createAnkiCard(entryId)
      const entry = entries.value.find(e => e.id === entryId)
      if (entry) {
        entry.anki_card = result
      }
      return result
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function createWebClip(url) {
    loading.value = true
    error.value = null
    try {
      const result = await brainAPI.createWebClip(url)
      entries.value.unshift(result)
      return result
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchWorktrees(params = {}) {
    loading.value = true
    error.value = null
    try {
      const result = await brainAPI.getWorktrees(params)
      worktrees.value = result.worktrees || []
      return worktrees.value
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function createWorktree(data) {
    loading.value = true
    error.value = null
    try {
      const result = await brainAPI.createWorktree(data)
      worktrees.value.unshift(result)
      return result
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
      stats.value = await brainAPI.getStats()
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
    entries,
    worktrees,
    searchResults,
    stats,
    loading,
    error,

    // Computed
    entryCount,
    activeWorktrees,
    recentEntries,

    // Actions
    fetchEntries,
    fetchEntry,
    createEntry,
    updateEntry,
    deleteEntry,
    searchEntries,
    createAnkiCard,
    createWebClip,
    fetchWorktrees,
    createWorktree,
    fetchStats,
    clearError,
  }
})
