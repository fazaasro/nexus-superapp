<template>
  <v-container class="pa-4">
    <!-- Header -->
    <v-row class="mb-4">
      <v-col cols="12">
        <h1 class="text-h4 font-weight-bold mb-2">Finance 💰</h1>
        <p class="text-subtitle-1 text-grey">Track spending, budget, and runway</p>
      </v-col>
    </v-row>

    <!-- Quick Stats -->
    <v-row class="mb-4">
      <v-col cols="6" sm="3">
        <v-card color="primary" class="pa-4 text-center">
          <div class="text-h4 font-weight-bold">{{ formatCurrency(monthlySpending) }}</div>
          <div class="text-caption opacity-75">This Month</div>
        </v-card>
      </v-col>
      <v-col cols="6" sm="3">
        <v-card color="secondary" class="pa-4 text-center">
          <div class="text-h4 font-weight-bold">{{ runway?.days_remaining || '--' }}</div>
          <div class="text-caption opacity-75">Days Runway</div>
        </v-card>
      </v-col>
      <v-col cols="6" sm="3">
        <v-card color="accent" class="pa-4 text-center">
          <div class="text-h4 font-weight-bold">{{ transactions.length }}</div>
          <div class="text-caption opacity-75">Transactions</div>
        </v-card>
      </v-col>
      <v-col cols="6" sm="3">
        <v-card color="success" class="pa-4 text-center">
          <div class="text-h4 font-weight-bold">{{ subscriptions.length }}</div>
          <div class="text-caption opacity-75">Subscriptions</div>
        </v-card>
      </v-col>
    </v-row>

    <!-- Actions -->
    <v-row class="mb-4">
      <v-col cols="12">
        <v-btn-toggle v-model="action" mandatory color="primary">
          <v-btn value="transactions">
            <v-icon start>mdi-list</v-icon>
            Transactions
          </v-btn>
          <v-btn value="upload">
            <v-icon start>mdi-camera</v-icon>
            Upload Receipt
          </v-btn>
          <v-btn value="budget">
            <v-icon start>mdi-chart-pie</v-icon>
            Budgets
          </v-btn>
        </v-btn-toggle>
      </v-col>
    </v-row>

    <!-- Content based on action -->
    <v-row v-if="action === 'transactions'">
      <v-col cols="12">
        <v-card color="surface" elevation="2">
          <v-card-title>Recent Transactions</v-card-title>
          <v-card-text>
            <v-list v-if="transactions.length">
              <v-list-item v-for="txn in transactions" :key="txn.id">
                <template v-slot:prepend>
                  <v-icon :color="txn.amount > 0 ? 'success' : 'error'">
                    {{ txn.amount > 0 ? 'mdi-arrow-up' : 'mdi-arrow-down' }}
                  </v-icon>
                </template>
                <v-list-item-title>{{ txn.description || txn.category }}</v-list-item-title>
                <v-list-item-subtitle>{{ formatDate(txn.date) }} • {{ txn.category }}</v-list-item-subtitle>
                <template v-slot:append>
                  <div class="text-right">
                    <div :class="txn.amount > 0 ? 'text-success' : 'text-error'">
                      {{ formatCurrency(txn.amount) }}
                    </div>
                    <v-chip v-if="txn.split_type" size="x-small" class="mt-1">
                      {{ txn.split_type }}
                    </v-chip>
                  </div>
                </template>
              </v-list-item>
            </v-list>
            <v-alert v-else type="info" class="mt-4">
              No transactions yet. Upload a receipt or add one manually!
            </v-alert>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row v-if="action === 'upload'">
      <v-col cols="12">
        <v-card color="surface" elevation="2">
          <v-card-title>Upload Receipt</v-card-title>
          <v-card-text>
            <v-file-input
              v-model="receiptFile"
              label="Select receipt image"
              accept="image/*"
              prepend-icon="mdi-camera"
              @change="handleFileUpload"
              :loading="loading"
            ></v-file-input>
            <v-textarea
              v-model="notes"
              label="Notes (optional)"
              rows="2"
              class="mt-4"
            ></v-textarea>
            <v-btn
              color="primary"
              block
              @click="uploadReceipt"
              :loading="loading"
              :disabled="!receiptFile"
            >
              <v-icon start>mdi-upload</v-icon>
              Upload & Process
            </v-btn>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row v-if="action === 'budget'">
      <v-col cols="12">
        <v-card color="surface" elevation="2">
          <v-card-title>Budgets</v-card-title>
          <v-card-text>
            <v-alert type="info">
              Budget tracking coming soon! Set spending limits by category.
            </v-alert>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- FAB for quick actions -->
    <v-btn
      fab
      color="primary"
      fixed
      bottom
      right
      :class="{ 'mb-16': isMobile }"
      @click="showAddDialog = true"
    >
      <v-icon>mdi-plus</v-icon>
    </v-btn>

    <!-- Add Transaction Dialog -->
    <v-dialog v-model="showAddDialog" max-width="500">
      <v-card color="surface">
        <v-card-title>Add Transaction</v-card-title>
        <v-card-text>
          <v-form ref="form">
            <v-text-field
              v-model="newTransaction.description"
              label="Description"
              required
            ></v-text-field>
            <v-text-field
              v-model.number="newTransaction.amount"
              label="Amount"
              type="number"
              required
              :rules="[v => !!v || 'Amount is required']"
            ></v-text-field>
            <v-select
              v-model="newTransaction.category"
              :items="categories"
              label="Category"
              required
            ></v-select>
            <v-date-picker
              v-model="newTransaction.date"
              label="Date"
            ></v-date-picker>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey" @click="showAddDialog = false">Cancel</v-btn>
          <v-btn color="primary" @click="addTransaction">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useBagStore } from '../stores/bag'

// Store
const bagStore = useBagStore()

// State
const action = ref('transactions')
const receiptFile = ref(null)
const notes = ref('')
const loading = ref(false)
const showAddDialog = ref(false)
const isMobile = computed(() => window.innerWidth < 960)

// Form state
const newTransaction = ref({
  description: '',
  amount: 0,
  category: 'Food',
  date: new Date().toISOString().split('T')[0]
})

const categories = [
  'Food',
  'Transport',
  'Shopping',
  'Entertainment',
  'Bills',
  'Health',
  'Other'
]

// Computed from store
const transactions = computed(() => bagStore.transactions)
const monthlySpending = computed(() => bagStore.monthlySpending)
const runway = computed(() => bagStore.runway)
const subscriptions = computed(() => bagStore.subscriptions)

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
    day: 'numeric',
    year: 'numeric'
  })
}

const handleFileUpload = (file) => {
  receiptFile.value = file
}

const uploadReceipt = async () => {
  if (!receiptFile.value) return

  loading.value = true
  try {
    await bagStore.uploadReceipt(receiptFile.value, notes.value)
    window.showSnackbar('Receipt uploaded successfully!', 'success')
    receiptFile.value = null
    notes.value = ''
  } catch (error) {
    console.error('Error uploading receipt:', error)
  } finally {
    loading.value = false
  }
}

const addTransaction = async () => {
  loading.value = true
  try {
    await bagStore.createTransaction({
      ...newTransaction.value,
      amount: Math.abs(newTransaction.value.amount) * -1, // Default to expense
    })
    showAddDialog.value = false
    window.showSnackbar('Transaction added!', 'success')
    newTransaction.value = {
      description: '',
      amount: 0,
      category: 'Food',
      date: new Date().toISOString().split('T')[0]
    }
  } catch (error) {
    console.error('Error adding transaction:', error)
  } finally {
    loading.value = false
  }
}

// Lifecycle
onMounted(async () => {
  try {
    await Promise.all([
      bagStore.fetchTransactions({ limit: 50 }),
      bagStore.fetchRunway(),
      bagStore.detectSubscriptions()
    ])
  } catch (error) {
    console.error('Error loading finance data:', error)
  }
})
</script>

<style scoped>
.v-card {
  height: 100%;
}
</style>
