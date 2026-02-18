import axios from 'axios'

// Create axios instance with default config
const api = axios.create({
  baseURL: '/api/v1',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  }
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('nexus-token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }

    // For testing, add test user header
    if (!config.headers['X-Test-User']) {
      config.headers['X-Test-User'] = 'fazaasro@gmail.com'
    }

    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    const message = error.response?.data?.detail || error.message || 'An error occurred'

    // Show snackbar if available
    if (window.showSnackbar) {
      window.showSnackbar(message, 'error', 4000)
    }

    return Promise.reject(error)
  }
)

// Bag (Finance) API
export const bagAPI = {
  // Transactions
  getTransactions: (params) => api.get('/bag/transactions', { params }),
  createTransaction: (data) => api.post('/bag/transactions', data),
  updateSplit: (txnId, data) => api.post(`/bag/transactions/${txnId}/split`, data),

  // Receipts
  uploadReceipt: (file, notes) => {
    const formData = new FormData()
    formData.append('file', file)
    if (notes) formData.append('notes', notes)
    return api.post('/bag/receipts/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },

  // Runway
  getRunway: (currentBalance) => api.get('/bag/runway', { params: { current_balance: currentBalance } }),

  // Subscriptions
  detectSubscriptions: () => api.get('/bag/subscriptions/detect'),
  createSubscription: (data) => api.post('/bag/subscriptions', data),

  // Budgets
  createBudget: (data) => api.post('/bag/budgets', data),
  getBudgetStatus: (budgetId) => api.get(`/bag/budgets/${budgetId}/status`),
}

// Brain (Knowledge) API
export const brainAPI = {
  // Knowledge Entries
  getEntries: (params) => api.get('/brain/entries', { params }),
  getEntry: (entryId) => api.get(`/brain/entries/${entryId}`),
  createEntry: (data) => api.post('/brain/entries', data),
  updateEntry: (entryId, data) => api.put(`/brain/entries/${entryId}`, data),
  deleteEntry: (entryId) => api.delete(`/brain/entries/${entryId}`),

  // Anki Integration
  createAnkiCard: (entryId) => api.post(`/brain/entries/${entryId}/anki`),

  // Web Clipping
  createWebClip: (url) => api.post('/brain/clip', { url }),

  // Worktrees
  getWorktrees: (params) => api.get('/brain/worktrees', { params }),
  createWorktree: (data) => api.post('/brain/worktrees', data),
  updateWorktreeAccess: (worktreeId) => api.put(`/brain/worktrees/${worktreeId}/access`),

  // Search
  search: (query, params) => api.get('/brain/search', { params: { q: query, ...params } }),

  // Embeddings
  generateEmbedding: (entryId) => api.post(`/brain/entries/${entryId}/embed`),

  // Stats
  getStats: () => api.get('/brain/stats'),
}

// Circle (Social) API
export const circleAPI = {
  // Contacts
  getContacts: (params) => api.get('/circle/contacts', { params }),
  getContact: (contactId) => api.get(`/circle/contacts/${contactId}`),
  createContact: (data) => api.post('/circle/contacts', data),
  updateContact: (contactId, data) => api.put(`/circle/contacts/${contactId}`, data),
  recordContact: (contactId) => api.post(`/circle/contacts/${contactId}/contact`),

  // Health Logs
  getHealthLogs: (params) => api.get('/circle/health-logs', { params }),
  getHealthLog: (logId) => api.get(`/circle/health-logs/${logId}`),
  createHealthLog: (data) => api.post('/circle/health-logs', data),
  analyzeHealth: (owner, symptomType, days) => api.get('/circle/health-logs/analysis', {
    params: { owner, symptom_type: symptomType, days }
  }),

  // Check-ins
  getCheckins: (params) => api.get('/circle/checkins', { params }),
  getCheckinTrends: (days) => api.get('/circle/checkins/trends', { params: { days } }),
  createCheckin: (data) => api.post('/circle/checkins', data),

  // Reminders
  getReminders: () => api.get('/circle/reminders'),

  // Stats
  getStats: () => api.get('/circle/stats'),
}

// Vessel (Health) API
export const vesselAPI = {
  // Blueprint Protocol
  getBlueprintLogs: (params) => api.get('/vessel/blueprint', { params }),
  getBlueprintLog: (logDate, owner) => api.get(`/vessel/blueprint/${logDate}`, { params: { owner } }),
  logBlueprint: (data) => api.post('/vessel/blueprint', data),

  // Workouts
  getWorkouts: (params) => api.get('/vessel/workouts', { params }),
  getWorkoutStats: (owner, days) => api.get('/vessel/workouts/stats', { params: { owner, days } }),
  logWorkout: (data) => api.post('/vessel/workouts', data),

  // Biometrics
  getBiometrics: (params) => api.get('/vessel/biometrics', { params }),
  getBiometricTrends: (owner, days) => api.get('/vessel/biometrics/trends', { params: { owner, days } }),
  logBiometrics: (data) => api.post('/vessel/biometrics', data),

  // Sobriety Tracker
  getSobrietyTracker: (trackerId) => api.get(`/vessel/sobriety/${trackerId}`),
  startSobrietyTracker: (data) => api.post('/vessel/sobriety', data),
  logRelapse: (trackerId, data) => api.put(`/vessel/sobriety/${trackerId}/relapse`, data),

  // Analytics
  getAnalytics: (owner, days) => api.get('/vessel/analytics', { params: { owner, days } }),

  // Stats
  getStats: (owner) => api.get('/vessel/stats', { params: { owner } }),
}

// Health Check
export const healthCheck = () => api.get('/health', { baseURL: '/api' })

export default api
