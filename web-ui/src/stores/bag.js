import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { bagAPI } from '../api'

export const useBagStore = defineStore('bag', () => {
  // State
  const transactions = ref([])
  const runway = ref(null)
  const subscriptions = ref([])
  const budgets = ref([])
  const loading = ref(false)
  const error = ref(null)

  // Computed
  const totalSpent = computed(() => {
    return transactions.value.reduce((sum, t) => sum + (t.amount || 0), 0)
  })

  const recentTransactions = computed(() => {
    return transactions.value.slice(0, 10)
  })

  const monthlySpending = computed(() => {
    const now = new Date()
    return transactions.value
      .filter(t => {
        const date = new Date(t.date)
        return date.getMonth() === now.getMonth() && date.getFullYear() === now.getFullYear()
      })
      .reduce((sum, t) => sum + (t.amount || 0), 0)
  })

  // Actions
  async function fetchTransactions(params = {}) {
    loading.value = true
    error.value = null
    try {
      transactions.value = await bagAPI.getTransactions(params)
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function createTransaction(data) {
    loading.value = true
    error.value = null
    try {
      const result = await bagAPI.createTransaction(data)
      transactions.value.unshift(result)
      return result
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchRunway(currentBalance) {
    loading.value = true
    error.value = null
    try {
      runway.value = await bagAPI.getRunway(currentBalance)
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function detectSubscriptions() {
    loading.value = true
    error.value = null
    try {
      const result = await bagAPI.detectSubscriptions()
      subscriptions.value = result.patterns || []
      return subscriptions.value
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function uploadReceipt(file, notes) {
    loading.value = true
    error.value = null
    try {
      const result = await bagAPI.uploadReceipt(file, notes)
      // Refresh transactions if receipt was processed
      if (result.processing_result?.transaction) {
        await fetchTransactions()
      }
      return result
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function createBudget(data) {
    loading.value = true
    error.value = null
    try {
      const result = await bagAPI.createBudget(data)
      budgets.value.push(result)
      return result
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
    transactions,
    runway,
    subscriptions,
    budgets,
    loading,
    error,

    // Computed
    totalSpent,
    recentTransactions,
    monthlySpending,

    // Actions
    fetchTransactions,
    createTransaction,
    fetchRunway,
    detectSubscriptions,
    uploadReceipt,
    createBudget,
    clearError,
  }
})
