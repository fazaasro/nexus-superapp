<template>
  <v-container class="pa-4">
    <!-- Welcome Section -->
    <v-row class="mb-4">
      <v-col cols="12">
        <h1 class="text-h4 font-weight-bold mb-2">Welcome back, {{ userName }}! 👋</h1>
        <p class="text-subtitle-1 text-grey">Here's what's happening across your Nexus Super App</p>
      </v-col>
    </v-row>

    <!-- Quick Stats -->
    <v-row class="mb-4">
      <v-col cols="6" sm="3">
        <v-card color="surface" elevation="2" class="pa-4">
          <div class="d-flex align-center">
            <v-icon color="primary" size="40" class="mr-3">mdi-wallet</v-icon>
            <div>
              <div class="text-h6 font-weight-bold">{{ formatCurrency(monthlySpending) }}</div>
              <div class="text-caption text-grey">Monthly Spending</div>
            </div>
          </div>
        </v-card>
      </v-col>
      <v-col cols="6" sm="3">
        <v-card color="surface" elevation="2" class="pa-4">
          <div class="d-flex align-center">
            <v-icon color="secondary" size="40" class="mr-3">mdi-brain</v-icon>
            <div>
              <div class="text-h6 font-weight-bold">{{ entryCount }}</div>
              <div class="text-caption text-grey">Knowledge Entries</div>
            </div>
          </div>
        </v-card>
      </v-col>
      <v-col cols="6" sm="3">
        <v-card color="surface" elevation="2" class="pa-4">
          <div class="d-flex align-center">
            <v-icon color="accent" size="40" class="mr-3">mdi-account-group</v-icon>
            <div>
              <div class="text-h6 font-weight-bold">{{ innerCircleCount }}</div>
              <div class="text-caption text-grey">Inner Circle</div>
            </div>
          </div>
        </v-card>
      </v-col>
      <v-col cols="6" sm="3">
        <v-card color="surface" elevation="2" class="pa-4">
          <div class="d-flex align-center">
            <v-icon color="success" size="40" class="mr-3">mdi-heart-pulse</v-icon>
            <div>
              <div class="text-h6 font-weight-bold">{{ workoutCount }}</div>
              <div class="text-caption text-grey">Workouts (30d)</div>
            </div>
          </div>
        </v-card>
      </v-col>
    </v-row>

    <!-- Module Cards -->
    <v-row>
      <!-- Finance (The Bag) -->
      <v-col cols="12" md="6">
        <v-card color="surface" elevation="2">
          <v-card-title class="d-flex align-center">
            <v-icon color="primary" class="mr-2">mdi-wallet</v-icon>
            <span>Finance</span>
            <v-spacer></v-spacer>
            <v-btn size="small" variant="text" color="primary" to="/bag">View All</v-btn>
          </v-card-title>
          <v-card-text>
            <v-list density="compact">
              <v-list-item v-for="txn in recentTransactions.slice(0, 3)" :key="txn.id">
                <template v-slot:prepend>
                  <v-icon :color="txn.amount > 0 ? 'success' : 'error'">
                    {{ txn.amount > 0 ? 'mdi-arrow-up' : 'mdi-arrow-down' }}
                  </v-icon>
                </template>
                <v-list-item-title>{{ txn.description || txn.category }}</v-list-item-title>
                <v-list-item-subtitle>{{ formatDate(txn.date) }}</v-list-item-subtitle>
                <template v-slot:append>
                  <span :class="txn.amount > 0 ? 'text-success' : 'text-error'">
                    {{ formatCurrency(txn.amount) }}
                  </span>
                </template>
              </v-list-item>
              <v-list-item v-if="recentTransactions.length === 0">
                <v-list-item-title class="text-grey">No recent transactions</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Knowledge (The Brain) -->
      <v-col cols="12" md="6">
        <v-card color="surface" elevation="2">
          <v-card-title class="d-flex align-center">
            <v-icon color="secondary" class="mr-2">mdi-brain</v-icon>
            <span>Knowledge</span>
            <v-spacer></v-spacer>
            <v-btn size="small" variant="text" color="secondary" to="/brain">View All</v-btn>
          </v-card-title>
          <v-card-text>
            <v-list density="compact">
              <v-list-item v-for="entry in recentEntries.slice(0, 3)" :key="entry.id">
                <template v-slot:prepend>
                  <v-icon color="secondary">mdi-note-text</v-icon>
                </template>
                <v-list-item-title>{{ entry.title || entry.content?.substring(0, 50) }}</v-list-item-title>
                <v-list-item-subtitle>{{ entry.domain }} • {{ entry.content_type }}</v-list-item-subtitle>
              </v-list-item>
              <v-list-item v-if="recentEntries.length === 0">
                <v-list-item-title class="text-grey">No recent entries</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Social (The Circle) -->
      <v-col cols="12" md="6">
        <v-card color="surface" elevation="2">
          <v-card-title class="d-flex align-center">
            <v-icon color="accent" class="mr-2">mdi-account-group</v-icon>
            <span>Social</span>
            <v-spacer></v-spacer>
            <v-btn size="small" variant="text" color="accent" to="/circle">View All</v-btn>
          </v-card-title>
          <v-card-text>
            <v-list density="compact">
              <v-list-item v-for="contact in innerCircleContacts.slice(0, 3)" :key="contact.id">
                <template v-slot:prepend>
                  <v-avatar size="32" color="accent">
                    {{ contact.name?.charAt(0) || '?' }}
                  </v-avatar>
                </template>
                <v-list-item-title>{{ contact.name }}</v-list-item-title>
                <v-list-item-subtitle>{{ contact.relationship }}</v-list-item-subtitle>
              </v-list-item>
              <v-list-item v-if="innerCircleContacts.length === 0">
                <v-list-item-title class="text-grey">No inner circle contacts</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Health (The Vessel) -->
      <v-col cols="12" md="6">
        <v-card color="surface" elevation="2">
          <v-card-title class="d-flex align-center">
            <v-icon color="success" class="mr-2">mdi-heart-pulse</v-icon>
            <span>Health</span>
            <v-spacer></v-spacer>
            <v-btn size="small" variant="text" color="success" to="/vessel">View All</v-btn>
          </v-card-title>
          <v-card-text>
            <v-list density="compact">
              <v-list-item v-for="workout in recentWorkouts.slice(0, 3)" :key="workout.id">
                <template v-slot:prepend>
                  <v-icon color="success">mdi-dumbbell</v-icon>
                </template>
                <v-list-item-title>{{ workout.type }} • {{ workout.duration }} min</v-list-item-title>
                <v-list-item-subtitle>{{ formatDate(workout.date) }}</v-list-item-subtitle>
              </v-list-item>
              <v-list-item v-if="recentWorkouts.length === 0">
                <v-list-item-title class="text-grey">No recent workouts</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useBagStore } from '../stores/bag'
import { useBrainStore } from '../stores/brain'
import { useCircleStore } from '../stores/circle'
import { useVesselStore } from '../stores/vessel'

// Stores
const bagStore = useBagStore()
const brainStore = useBrainStore()
const circleStore = useCircleStore()
const vesselStore = useVesselStore()

// State
const userName = ref('Faza')

// Computed from stores
const monthlySpending = computed(() => bagStore.monthlySpending)
const recentTransactions = computed(() => bagStore.recentTransactions)
const entryCount = computed(() => brainStore.entryCount)
const recentEntries = computed(() => brainStore.recentEntries)
const innerCircleContacts = computed(() => circleStore.innerCircleContacts)
const innerCircleCount = computed(() => circleStore.innerCircleContacts.length)
const recentWorkouts = computed(() => vesselStore.recentWorkouts)
const workoutCount = computed(() => vesselStore.recentWorkouts.length)

// Methods
const formatCurrency = (value) => {
  if (!value) return '$0.00'
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD'
  }).format(value)
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric'
  })
}

// Lifecycle
onMounted(async () => {
  try {
    // Fetch data from all stores
    await Promise.all([
      bagStore.fetchTransactions({ limit: 10 }),
      brainStore.fetchEntries({ limit: 10 }),
      circleStore.fetchContacts({ inner_circle_only: true, limit: 10 }),
      vesselStore.fetchWorkouts({ days: 30, limit: 10 })
    ])
  } catch (error) {
    console.error('Error loading dashboard data:', error)
  }
})
</script>

<style scoped>
.v-card {
  height: 100%;
}
</style>
