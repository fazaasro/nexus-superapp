<template>
  <v-container class="pa-4">
    <!-- Header -->
    <v-row class="mb-4">
      <v-col cols="12">
        <h1 class="text-h4 font-weight-bold mb-2">Health ❤️</h1>
        <p class="text-subtitle-1 text-grey">Track fitness, biometrics, and wellness protocols</p>
      </v-col>
    </v-row>

    <!-- Quick Stats -->
    <v-row class="mb-4">
      <v-col cols="6" sm="3">
        <v-card color="primary" class="pa-4 text-center">
          <div class="text-h4 font-weight-bold">{{ workouts.length }}</div>
          <div class="text-caption opacity-75">Workouts (30d)</div>
        </v-card>
      </v-col>
      <v-col cols="6" sm="3">
        <v-card color="secondary" class="pa-4 text-center">
          <div class="text-h4 font-weight-bold">{{ totalWorkoutTime }}m</div>
          <div class="text-caption opacity-75">Total Time</div>
        </v-card>
      </v-col>
      <v-col cols="6" sm="3">
        <v-card color="accent" class="pa-4 text-center">
          <div class="text-h4 font-weight-bold">{{ biometrics.length }}</div>
          <div class="text-caption opacity-75">Biometrics</div>
        </v-card>
      </v-col>
      <v-col cols="6" sm="3">
        <v-card color="success" class="pa-4 text-center">
          <div class="text-h4 font-weight-bold">{{ blueprintCompliance }}%</div>
          <div class="text-caption opacity-75">Blueprint</div>
        </v-card>
      </v-col>
    </v-row>

    <!-- Actions -->
    <v-row class="mb-4">
      <v-col cols="12">
        <v-btn-toggle v-model="action" mandatory color="primary">
          <v-btn value="blueprint">
            <v-icon start>mdi-clipboard-check</v-icon>
            Blueprint
          </v-btn>
          <v-btn value="workouts">
            <v-icon start>mdi-dumbbell</v-icon>
            Workouts
          </v-btn>
          <v-btn value="biometrics">
            <v-icon start>mdi-chart-line</v-icon>
            Biometrics
          </v-btn>
        </v-btn-toggle>
      </v-col>
    </v-row>

    <!-- Blueprint -->
    <v-row v-if="action === 'blueprint'">
      <v-col cols="12">
        <v-card color="surface" elevation="2">
          <v-card-title>
            Blueprint Protocol
            <v-spacer></v-spacer>
            <v-chip size="small">{{ blueprintCompliance }}% today</v-chip>
          </v-card-title>
          <v-card-text>
            <!-- Today's Blueprint -->
            <v-alert v-if="todaysBlueprint" type="success" class="mb-4">
              Today's blueprint logged! Keep up the consistency.
            </v-alert>
            <v-alert v-else type="info" class="mb-4">
              Haven't logged today's blueprint yet.
            </v-alert>

            <!-- Blueprint Form -->
            <v-row>
              <v-col cols="6">
                <v-checkbox v-model="blueprintForm.sleep" label="Sleep (8h)"></v-checkbox>
                <v-checkbox v-model="blueprintForm.meditation" label="Meditation"></v-checkbox>
                <v-checkbox v-model="blueprintForm.exercise" label="Exercise"></v-checkbox>
              </v-col>
              <v-col cols="6">
                <v-checkbox v-model="blueprintForm.nutrition" label="Nutrition"></v-checkbox>
                <v-checkbox v-model="blueprintForm.supplements" label="Supplements"></v-checkbox>
                <v-checkbox v-model="blueprintForm.sobriety" label="Sobriety"></v-checkbox>
              </v-col>
            </v-row>
            <v-textarea
              v-model="blueprintForm.notes"
              label="Notes"
              rows="2"
              class="mt-2"
            ></v-textarea>
            <v-btn color="primary" block @click="logBlueprint" :loading="logging">
              <v-icon start>mdi-check</v-icon>
              Log Blueprint
            </v-btn>

            <!-- Recent Logs -->
            <div class="mt-4">
              <h3 class="text-h6 mb-2">Recent Logs</h3>
              <v-list v-if="blueprintLogs.length" density="compact">
                <v-list-item v-for="log in blueprintLogs.slice(0, 5)" :key="log.id">
                  <v-list-item-title>
                    {{ formatDate(log.date) }} - {{ log.compliance }}% compliance
                  </v-list-item-title>
                </v-list-item>
              </v-list>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Workouts -->
    <v-row v-if="action === 'workouts'">
      <v-col cols="12">
        <v-card color="surface" elevation="2">
          <v-card-title>Workouts</v-card-title>
          <v-card-text>
            <v-list v-if="workouts.length">
              <v-list-item v-for="workout in workouts" :key="workout.id">
                <template v-slot:prepend>
                  <v-icon color="success">mdi-dumbbell</v-icon>
                </template>
                <v-list-item-title>{{ workout.type }}</v-list-item-title>
                <v-list-item-subtitle>
                  {{ formatDate(workout.date) }} • {{ workout.duration }} minutes • {{ workout.intensity }}
                </v-list-item-subtitle>
                <template v-slot:append>
                  <v-chip color="success" size="small">
                    {{ workout.duration }}m
                  </v-chip>
                </template>
              </v-list-item>
            </v-list>
            <v-alert v-else type="info" class="mt-4">
              No workouts logged yet. Start moving!
            </v-alert>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Biometrics -->
    <v-row v-if="action === 'biometrics'">
      <v-col cols="12">
        <v-card color="surface" elevation="2">
          <v-card-title>Biometrics</v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="6">
                <v-text-field
                  v-model.number="biometricForm.weight"
                  label="Weight (kg)"
                  type="number"
                ></v-text-field>
              </v-col>
              <v-col cols="6">
                <v-text-field
                  v-model.number="biometricForm.body_fat"
                  label="Body Fat %"
                  type="number"
                ></v-text-field>
              </v-col>
              <v-col cols="6">
                <v-text-field
                  v-model.number="biometricForm.resting_hr"
                  label="Resting HR"
                  type="number"
                ></v-text-field>
              </v-col>
              <v-col cols="6">
                <v-text-field
                  v-model.number="biometricForm.sleep_hours"
                  label="Sleep Hours"
                  type="number"
                ></v-text-field>
              </v-col>
            </v-row>
            <v-textarea
              v-model="biometricForm.notes"
              label="Notes"
              rows="2"
              class="mt-2"
            ></v-textarea>
            <v-btn color="primary" block @click="logBiometrics" :loading="logging">
              <v-icon start>mdi-plus</v-icon>
              Log Biometrics
            </v-btn>

            <!-- Recent Readings -->
            <div class="mt-4">
              <h3 class="text-h6 mb-2">Recent Readings</h3>
              <v-list v-if="biometrics.length" density="compact">
                <v-list-item v-for="bio in biometrics.slice(0, 5)" :key="bio.id">
                  <v-list-item-title>
                    {{ formatDate(bio.date) }} - {{ bio.weight }}kg • {{ bio.body_fat }}% BF
                  </v-list-item-title>
                </v-list-item>
              </v-list>
            </div>
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
      @click="showWorkoutDialog = true"
    >
      <v-icon>mdi-plus</v-icon>
    </v-btn>

    <!-- Add Workout Dialog -->
    <v-dialog v-model="showWorkoutDialog" max-width="500">
      <v-card color="surface">
        <v-card-title>Log Workout</v-card-title>
        <v-card-text>
          <v-form>
            <v-select
              v-model="newWorkout.type"
              :items="workoutTypes"
              label="Type"
              required
            ></v-select>
            <v-text-field
              v-model.number="newWorkout.duration"
              label="Duration (minutes)"
              type="number"
              required
            ></v-text-field>
            <v-select
              v-model="newWorkout.intensity"
              :items="['Low', 'Medium', 'High']"
              label="Intensity"
            ></v-select>
            <v-textarea
              v-model="newWorkout.notes"
              label="Notes"
              rows="3"
            ></v-textarea>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey" @click="showWorkoutDialog = false">Cancel</v-btn>
          <v-btn color="primary" @click="addWorkout">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useVesselStore } from '../stores/vessel'

// Store
const vesselStore = useVesselStore()

// State
const action = ref('blueprint')
const logging = ref(false)
const showWorkoutDialog = ref(false)
const isMobile = computed(() => window.innerWidth < 960)

// Form state
const blueprintForm = ref({
  sleep: false,
  meditation: false,
  exercise: false,
  nutrition: false,
  supplements: false,
  sobriety: false,
  notes: ''
})

const biometricForm = ref({
  weight: null,
  body_fat: null,
  resting_hr: null,
  sleep_hours: null,
  notes: ''
})

const newWorkout = ref({
  type: 'Strength',
  duration: 30,
  intensity: 'Medium',
  notes: ''
})

const workoutTypes = [
  'Strength',
  'Cardio',
  'HIIT',
  'Yoga',
  'Running',
  'Cycling',
  'Swimming',
  'Other'
]

// Computed from store
const blueprintLogs = computed(() => vesselStore.blueprintLogs)
const workouts = computed(() => vesselStore.workouts)
const biometrics = computed(() => vesselStore.biometrics)
const todaysBlueprint = computed(() => vesselStore.todaysBlueprint)
const totalWorkoutTime = computed(() => vesselStore.totalWorkoutTime)

const blueprintCompliance = computed(() => {
  if (!todaysBlueprint.value) return 0
  return todaysBlueprint.value.compliance || 0
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

const logBlueprint = async () => {
  logging.value = true
  try {
    const compliance = calculateCompliance(blueprintForm.value)
    await vesselStore.logBlueprint({
      ...blueprintForm.value,
      compliance
    })
    window.showSnackbar('Blueprint logged!', 'success')
    // Reset form
    blueprintForm.value = {
      sleep: false,
      meditation: false,
      exercise: false,
      nutrition: false,
      supplements: false,
      sobriety: false,
      notes: ''
    }
  } catch (error) {
    console.error('Error logging blueprint:', error)
  } finally {
    logging.value = false
  }
}

const logBiometrics = async () => {
  logging.value = true
  try {
    await vesselStore.logBiometrics(biometricForm.value)
    window.showSnackbar('Biometrics logged!', 'success')
    // Reset form
    biometricForm.value = {
      weight: null,
      body_fat: null,
      resting_hr: null,
      sleep_hours: null,
      notes: ''
    }
  } catch (error) {
    console.error('Error logging biometrics:', error)
  } finally {
    logging.value = false
  }
}

const addWorkout = async () => {
  try {
    await vesselStore.logWorkout(newWorkout.value)
    showWorkoutDialog.value = false
    window.showSnackbar('Workout logged!', 'success')
    newWorkout.value = {
      type: 'Strength',
      duration: 30,
      intensity: 'Medium',
      notes: ''
    }
  } catch (error) {
    console.error('Error adding workout:', error)
  }
}

const calculateCompliance = (form) => {
  const items = [
    form.sleep,
    form.meditation,
    form.exercise,
    form.nutrition,
    form.supplements,
    form.sobriety
  ]
  const completed = items.filter(Boolean).length
  return Math.round((completed / items.length) * 100)
}

// Lifecycle
onMounted(async () => {
  try {
    await Promise.all([
      vesselStore.fetchBlueprintLogs({ limit: 10 }),
      vesselStore.fetchWorkouts({ days: 30, limit: 20 }),
      vesselStore.fetchBiometrics({ days: 30, limit: 20 })
    ])
  } catch (error) {
    console.error('Error loading vessel data:', error)
  }
})
</script>

<style scoped>
.v-card {
  height: 100%;
}
</style>
