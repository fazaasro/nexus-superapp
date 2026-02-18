<template>
  <v-container class="pa-4">
    <!-- Header -->
    <v-row class="mb-4">
      <v-col cols="12">
        <h1 class="text-h4 font-weight-bold mb-2">Knowledge 🧠</h1>
        <p class="text-subtitle-1 text-grey">Capture, organize, and recall what you learn</p>
      </v-col>
    </v-row>

    <!-- Quick Stats -->
    <v-row class="mb-4">
      <v-col cols="6" sm="3">
        <v-card color="primary" class="pa-4 text-center">
          <div class="text-h4 font-weight-bold">{{ entryCount }}</div>
          <div class="text-caption opacity-75">Total Entries</div>
        </v-card>
      </v-col>
      <v-col cols="6" sm="3">
        <v-card color="secondary" class="pa-4 text-center">
          <div class="text-h4 font-weight-bold">{{ activeWorktrees.length }}</div>
          <div class="text-caption opacity-75">Active Projects</div>
        </v-card>
      </v-col>
      <v-col cols="6" sm="3">
        <v-card color="accent" class="pa-4 text-center">
          <div class="text-h4 font-weight-bold">{{ ankiCardCount }}</div>
          <div class="text-caption opacity-75">Anki Cards</div>
        </v-card>
      </v-col>
      <v-col cols="6" sm="3">
        <v-card color="success" class="pa-4 text-center">
          <div class="text-h4 font-weight-bold">--</div>
          <div class="text-caption opacity-75">Due Today</div>
        </v-card>
      </v-col>
    </v-row>

    <!-- Search -->
    <v-row class="mb-4">
      <v-col cols="12">
        <v-text-field
          v-model="searchQuery"
          label="Search knowledge..."
          prepend-inner-icon="mdi-magnify"
          variant="outlined"
          clearable
          @keyup.enter="search"
          :loading="searching"
        ></v-text-field>
        <v-row class="mb-2">
          <v-col cols="6" sm="3">
            <v-select
              v-model="filters.domain"
              :items="domains"
              label="Domain"
              clearable
              density="compact"
              variant="outlined"
            ></v-select>
          </v-col>
          <v-col cols="6" sm="3">
            <v-select
              v-model="filters.project"
              :items="projects"
              label="Project"
              clearable
              density="compact"
              variant="outlined"
            ></v-select>
          </v-col>
          <v-col cols="6" sm="3">
            <v-select
              v-model="filters.content_type"
              :items="contentTypes"
              label="Type"
              clearable
              density="compact"
              variant="outlined"
            ></v-select>
          </v-col>
          <v-col cols="6" sm="3">
            <v-btn color="primary" block height="40" @click="search">
              <v-icon start>mdi-magnify</v-icon>
              Search
            </v-btn>
          </v-col>
        </v-row>
      </v-col>
    </v-row>

    <!-- Actions -->
    <v-row class="mb-4">
      <v-col cols="12">
        <v-btn-toggle v-model="action" mandatory color="primary">
          <v-btn value="entries">
            <v-icon start>mdi-note-text</v-icon>
            Entries
          </v-btn>
          <v-btn value="clip">
            <v-icon start>mdi-web</v-icon>
            Web Clip
          </v-btn>
          <v-btn value="worktrees">
            <v-icon start>mdi-source-branch</v-icon>
            Projects
          </v-btn>
        </v-btn-toggle>
      </v-col>
    </v-row>

    <!-- Entries -->
    <v-row v-if="action === 'entries'">
      <v-col cols="12">
        <v-card color="surface" elevation="2">
          <v-card-title>
            Knowledge Entries
            <v-spacer></v-spacer>
            <v-chip size="small">{{ entries.length }} entries</v-chip>
          </v-card-title>
          <v-card-text>
            <v-list v-if="entries.length">
              <v-list-item v-for="entry in entries" :key="entry.id">
                <template v-slot:prepend>
                  <v-icon color="primary">mdi-note-text</v-icon>
                </template>
                <v-list-item-title>{{ entry.title || entry.content?.substring(0, 50) }}</v-list-item-title>
                <v-list-item-subtitle>
                  {{ entry.domain }} • {{ entry.content_type }} • {{ formatDate(entry.created_at) }}
                </v-list-item-subtitle>
                <template v-slot:append>
                  <v-btn-group>
                    <v-btn size="small" icon="mdi-card-plus" @click="createAnkiCard(entry.id)"></v-btn>
                    <v-btn size="small" icon="mdi-pencil"></v-btn>
                    <v-btn size="small" icon="mdi-delete" color="error"></v-btn>
                  </v-btn-group>
                </template>
              </v-list-item>
            </v-list>
            <v-alert v-else type="info" class="mt-4">
              No entries yet. Start capturing knowledge!
            </v-alert>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Web Clip -->
    <v-row v-if="action === 'clip'">
      <v-col cols="12">
        <v-card color="surface" elevation="2">
          <v-card-title>Clip Web Page</v-card-title>
          <v-card-text>
            <v-text-field
              v-model="clipUrl"
              label="URL to clip"
              prepend-inner-icon="mdi-web"
              variant="outlined"
            ></v-text-field>
            <v-btn
              color="primary"
              block
              @click="clipWebPage"
              :loading="clipping"
              :disabled="!clipUrl"
            >
              <v-icon start>mdi-content-save</v-icon>
              Save as Knowledge Entry
            </v-btn>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Worktrees -->
    <v-row v-if="action === 'worktrees'">
      <v-col cols="12">
        <v-card color="surface" elevation="2">
          <v-card-title>Active Projects</v-card-title>
          <v-card-text>
            <v-list v-if="worktrees.length">
              <v-list-item v-for="worktree in worktrees" :key="worktree.id">
                <template v-slot:prepend>
                  <v-icon color="secondary">mdi-source-branch</v-icon>
                </template>
                <v-list-item-title>{{ worktree.name }}</v-list-item-title>
                <v-list-item-subtitle>
                  {{ worktree.path }} • Last accessed: {{ formatDate(worktree.last_accessed) }}
                </v-list-item-subtitle>
                <template v-slot:append>
                  <v-chip :color="worktree.status === 'active' ? 'success' : 'grey'" size="small">
                    {{ worktree.status }}
                  </v-chip>
                </template>
              </v-list-item>
            </v-list>
            <v-alert v-else type="info" class="mt-4">
              No active projects. Create one to start tracking work!
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

    <!-- Add Entry Dialog -->
    <v-dialog v-model="showAddDialog" max-width="600">
      <v-card color="surface">
        <v-card-title>Add Knowledge Entry</v-card-title>
        <v-card-text>
          <v-form>
            <v-text-field
              v-model="newEntry.title"
              label="Title"
            ></v-text-field>
            <v-textarea
              v-model="newEntry.content"
              label="Content"
              rows="6"
              required
            ></v-textarea>
            <v-row>
              <v-col cols="6">
                <v-select
                  v-model="newEntry.domain"
                  :items="domains"
                  label="Domain"
                ></v-select>
              </v-col>
              <v-col cols="6">
                <v-select
                  v-model="newEntry.content_type"
                  :items="contentTypes"
                  label="Type"
                ></v-select>
              </v-col>
            </v-row>
            <v-text-field
              v-model="newEntry.project"
              label="Project (optional)"
            ></v-text-field>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey" @click="showAddDialog = false">Cancel</v-btn>
          <v-btn color="primary" @click="addEntry">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useBrainStore } from '../stores/brain'

// Store
const brainStore = useBrainStore()

// State
const action = ref('entries')
const searchQuery = ref('')
const searching = ref(false)
const clipping = ref(false)
const clipUrl = ref('')
const showAddDialog = ref(false)
const isMobile = computed(() => window.innerWidth < 960)

// Filters
const filters = ref({
  domain: null,
  project: null,
  content_type: null
})

// Form state
const newEntry = ref({
  title: '',
  content: '',
  domain: 'General',
  content_type: 'Note',
  project: ''
})

const domains = ['General', 'Programming', 'Business', 'Health', 'Learning', 'Other']
const contentTypes = ['Note', 'Code Snippet', 'Article', 'Book Note', 'Tutorial', 'Research']
const projects = ref([])

// Computed from store
const entries = computed(() => brainStore.entries)
const entryCount = computed(() => brainStore.entryCount)
const worktrees = computed(() => brainStore.worktrees)
const activeWorktrees = computed(() => brainStore.activeWorktrees)
const ankiCardCount = computed(() => entries.value.filter(e => e.anki_card).length)

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

const search = async () => {
  searching.value = true
  try {
    await brainStore.searchEntries(searchQuery.value, {
      domain: filters.value.domain,
      project: filters.value.project,
      content_type: filters.value.content_type,
      limit: 50
    })
  } catch (error) {
    console.error('Error searching:', error)
  } finally {
    searching.value = false
  }
}

const clipWebPage = async () => {
  if (!clipUrl.value) return

  clipping.value = true
  try {
    await brainStore.createWebClip(clipUrl.value)
    window.showSnackbar('Web page clipped successfully!', 'success')
    clipUrl.value = ''
    await brainStore.fetchEntries()
  } catch (error) {
    console.error('Error clipping web page:', error)
  } finally {
    clipping.value = false
  }
}

const addEntry = async () => {
  try {
    await brainStore.createEntry(newEntry.value)
    showAddDialog.value = false
    window.showSnackbar('Entry created!', 'success')
    newEntry.value = {
      title: '',
      content: '',
      domain: 'General',
      content_type: 'Note',
      project: ''
    }
    await brainStore.fetchEntries()
  } catch (error) {
    console.error('Error creating entry:', error)
  }
}

const createAnkiCard = async (entryId) => {
  try {
    await brainStore.createAnkiCard(entryId)
    window.showSnackbar('Anki card created!', 'success')
  } catch (error) {
    console.error('Error creating Anki card:', error)
  }
}

// Lifecycle
onMounted(async () => {
  try {
    await Promise.all([
      brainStore.fetchEntries({ limit: 50 }),
      brainStore.fetchWorktrees()
    ])
    // Extract unique projects from entries
    projects.value = [...new Set(entries.value.map(e => e.project).filter(Boolean))]
  } catch (error) {
    console.error('Error loading brain data:', error)
  }
})
</script>

<style scoped>
.v-card {
  height: 100%;
}
</style>
