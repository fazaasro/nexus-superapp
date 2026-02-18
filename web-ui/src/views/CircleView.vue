<template>
  <v-container class="pa-4">
    <!-- Header -->
    <v-row class="mb-4">
      <v-col cols="12">
        <h1 class="text-h4 font-weight-bold mb-2">Social 👥</h1>
        <p class="text-subtitle-1 text-grey">Manage relationships, health tracking, and mood</p>
      </v-col>
    </v-row>

    <!-- Quick Stats -->
    <v-row class="mb-4">
      <v-col cols="6" sm="3">
        <v-card color="primary" class="pa-4 text-center">
          <div class="text-h4 font-weight-bold">{{ contacts.length }}</div>
          <div class="text-caption opacity-75">Total Contacts</div>
        </v-card>
      </v-col>
      <v-col cols="6" sm="3">
        <v-card color="secondary" class="pa-4 text-center">
          <div class="text-h4 font-weight-bold">{{ innerCircleCount }}</div>
          <div class="text-caption opacity-75">Inner Circle</div>
        </v-card>
      </v-col>
      <v-col cols="6" sm="3">
        <v-card color="accent" class="pa-4 text-center">
          <div class="text-h4 font-weight-bold">{{ healthLogs.length }}</div>
          <div class="text-caption opacity-75">Health Logs</div>
        </v-card>
      </v-col>
      <v-col cols="6" sm="3">
        <v-card color="success" class="pa-4 text-center">
          <div class="text-h4 font-weight-bold">{{ checkins.length }}</div>
          <div class="text-caption opacity-75">Check-ins</div>
        </v-card>
      </v-col>
    </v-row>

    <!-- Actions -->
    <v-row class="mb-4">
      <v-col cols="12">
        <v-btn-toggle v-model="action" mandatory color="primary">
          <v-btn value="contacts">
            <v-icon start>mdi-account-group</v-icon>
            Contacts
          </v-btn>
          <v-btn value="health">
            <v-icon start>mdi-heart-pulse</v-icon>
            Health Logs
          </v-btn>
          <v-btn value="checkins">
            <v-icon start>mdi-emoticon-happy</v-icon>
            Check-ins
          </v-btn>
        </v-btn-toggle>
      </v-col>
    </v-row>

    <!-- Contacts -->
    <v-row v-if="action === 'contacts'">
      <v-col cols="12">
        <v-card color="surface" elevation="2">
          <v-card-title>
            Contacts
            <v-spacer></v-spacer>
            <v-chip size="small">{{ innerCircleCount }} inner circle</v-chip>
          </v-card-title>
          <v-card-text>
            <v-list v-if="contacts.length">
              <v-list-item v-for="contact in contacts" :key="contact.id">
                <template v-slot:prepend>
                  <v-avatar :color="contact.inner_circle ? 'primary' : 'grey'">
                    {{ contact.name?.charAt(0) || '?' }}
                  </v-avatar>
                </template>
                <v-list-item-title>{{ contact.name }}</v-list-item-title>
                <v-list-item-subtitle>
                  {{ contact.relationship }} • Last contacted: {{ contact.last_contacted ? formatDate(contact.last_contacted) : 'Never' }}
                </v-list-item-subtitle>
                <template v-slot:append>
                  <v-btn-group>
                    <v-btn size="small" icon="mdi-phone" @click="recordContact(contact.id)"></v-btn>
                    <v-btn size="small" icon="mdi-pencil"></v-btn>
                    <v-btn size="small" icon="mdi-delete" color="error"></v-btn>
                  </v-btn-group>
                </template>
              </v-list-item>
            </v-list>
            <v-alert v-else type="info" class="mt-4">
              No contacts yet. Add people important to you!
            </v-alert>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Health Logs -->
    <v-row v-if="action === 'health'">
      <v-col cols="12">
        <v-card color="surface" elevation="2">
          <v-card-title>Health Logs</v-card-title>
          <v-card-text>
            <v-row class="mb-4">
              <v-col cols="6">
                <v-select
                  v-model="healthFilter.owner"
                  :items="['Faza', 'Gaby']"
                  label="Person"
                  density="compact"
                ></v-select>
              </v-col>
              <v-col cols="6">
                <v-select
                  v-model="healthFilter.symptom_type"
                  :items="['Sleep', 'Mood', 'Energy', 'Digestion', 'Physical']"
                  label="Type"
                  density="compact"
                  clearable
                ></v-select>
              </v-col>
            </v-row>
            <v-list v-if="filteredHealthLogs.length">
              <v-list-item v-for="log in filteredHealthLogs" :key="log.id">
                <template v-slot:prepend>
                  <v-icon :color="getHealthColor(log.severity)">mdi-heart-pulse</v-icon>
                </template>
                <v-list-item-title>{{ log.symptom_type }} - {{ log.notes }}</v-list-item-title>
                <v-list-item-subtitle>
                  {{ log.owner }} • {{ formatDate(log.date) }}
                </v-list-item-subtitle>
                <template v-slot:append>
                  <v-chip :color="getHealthColor(log.severity)" size="small">
                    {{ log.severity }}
                  </v-chip>
                </template>
              </v-list-item>
            </v-list>
            <v-alert v-else type="info" class="mt-4">
              No health logs. Start tracking to see patterns!
            </v-alert>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Check-ins -->
    <v-row v-if="action === 'checkins'">
      <v-col cols="12">
        <v-card color="surface" elevation="2">
          <v-card-title>
            Relationship Check-ins
            <v-spacer></v-spacer>
            <v-btn size="small" color="primary" @click="showCheckinDialog = true">
              <v-icon start>mdi-plus</v-icon>
              New Check-in
            </v-btn>
          </v-card-title>
          <v-card-text>
            <v-list v-if="checkins.length">
              <v-list-item v-for="checkin in checkins" :key="checkin.id">
                <template v-slot:prepend>
                  <v-icon :color="getVibeColor(checkin.vibe)">mdi-emoticon</v-icon>
                </template>
                <v-list-item-title>
                  Vibe: {{ checkin.vibe }}/10 • {{ checkin.notes }}
                </v-list-item-title>
                <v-list-item-subtitle>
                  {{ formatDate(checkin.date) }}
                </v-list-item-subtitle>
                <template v-slot:append>
                  <v-chip :color="getVibeColor(checkin.vibe)" size="small">
                    {{ checkin.vibe }}/10
                  </v-chip>
                </template>
              </v-list-item>
            </v-list>
            <v-alert v-else type="info" class="mt-4">
              No check-ins yet. Track your relationship vibes!
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

    <!-- Add Contact Dialog -->
    <v-dialog v-model="showAddDialog" max-width="500">
      <v-card color="surface">
        <v-card-title>Add Contact</v-card-title>
        <v-card-text>
          <v-form>
            <v-text-field
              v-model="newContact.name"
              label="Name"
              required
            ></v-text-field>
            <v-text-field
              v-model="newContact.relationship"
              label="Relationship"
            ></v-text-field>
            <v-checkbox
              v-model="newContact.inner_circle"
              label="Inner Circle"
            ></v-checkbox>
            <v-text-field
              v-model="newContact.notes"
              label="Notes"
            ></v-text-field>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey" @click="showAddDialog = false">Cancel</v-btn>
          <v-btn color="primary" @click="addContact">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Check-in Dialog -->
    <v-dialog v-model="showCheckinDialog" max-width="500">
      <v-card color="surface">
        <v-card-title>New Check-in</v-card-title>
        <v-card-text>
          <v-form>
            <v-slider
              v-model="newCheckin.vibe"
              label="Vibe"
              min="1"
              max="10"
              step="1"
              thumb-label
            ></v-slider>
            <v-textarea
              v-model="newCheckin.notes"
              label="Notes"
              rows="3"
            ></v-textarea>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey" @click="showCheckinDialog = false">Cancel</v-btn>
          <v-btn color="primary" @click="addCheckin">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useCircleStore } from '../stores/circle'

// Store
const circleStore = useCircleStore()

// State
const action = ref('contacts')
const showAddDialog = ref(false)
const showCheckinDialog = ref(false)
const isMobile = computed(() => window.innerWidth < 960)

// Filters
const healthFilter = ref({
  owner: 'Faza',
  symptom_type: null
})

// Form state
const newContact = ref({
  name: '',
  relationship: '',
  inner_circle: false,
  notes: ''
})

const newCheckin = ref({
  vibe: 7,
  notes: ''
})

// Computed from store
const contacts = computed(() => circleStore.contacts)
const innerCircleContacts = computed(() => circleStore.innerCircleContacts)
const innerCircleCount = computed(() => circleStore.innerCircleContacts.length)
const healthLogs = computed(() => circleStore.healthLogs)
const checkins = computed(() => circleStore.checkins)

const filteredHealthLogs = computed(() => {
  return healthLogs.value.filter(log => {
    const matchesOwner = !healthFilter.value.owner || log.owner === healthFilter.value.owner
    const matchesType = !healthFilter.value.symptom_type || log.symptom_type === healthFilter.value.symptom_type
    return matchesOwner && matchesType
  })
})

// Methods
const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  })
}

const getHealthColor = (severity) => {
  const colors = {
    low: 'success',
    medium: 'warning',
    high: 'error'
  }
  return colors[severity] || 'grey'
}

const getVibeColor = (vibe) => {
  if (vibe >= 8) return 'success'
  if (vibe >= 6) return 'info'
  if (vibe >= 4) return 'warning'
  return 'error'
}

const addContact = async () => {
  try {
    await circleStore.createContact(newContact.value)
    showAddDialog.value = false
    window.showSnackbar('Contact added!', 'success')
    newContact.value = {
      name: '',
      relationship: '',
      inner_circle: false,
      notes: ''
    }
  } catch (error) {
    console.error('Error adding contact:', error)
  }
}

const recordContact = async (contactId) => {
  try {
    await circleStore.recordContact(contactId)
    window.showSnackbar('Contact recorded!', 'success')
  } catch (error) {
    console.error('Error recording contact:', error)
  }
}

const addCheckin = async () => {
  try {
    await circleStore.createCheckin(newCheckin.value)
    showCheckinDialog.value = false
    window.showSnackbar('Check-in added!', 'success')
    newCheckin.value = {
      vibe: 7,
      notes: ''
    }
  } catch (error) {
    console.error('Error adding check-in:', error)
  }
}

// Lifecycle
onMounted(async () => {
  try {
    await Promise.all([
      circleStore.fetchContacts(),
      circleStore.fetchHealthLogs({ days: 30 }),
      circleStore.fetchCheckins({ days: 30 })
    ])
  } catch (error) {
    console.error('Error loading circle data:', error)
  }
})
</script>

<style scoped>
.v-card {
  height: 100%;
}
</style>
