<template>
  <v-app>
    <!-- Mobile Navigation Bottom Bar -->
    <v-bottom-navigation
      v-if="isMobile"
      v-model="currentTab"
      color="primary"
      grow
      elevation="8"
      class="bottom-nav"
    >
      <v-btn value="bag" to="/bag">
        <v-icon>mdi-wallet</v-icon>
        <span>Finance</span>
      </v-btn>
      <v-btn value="brain" to="/brain">
        <v-icon>mdi-brain</v-icon>
        <span>Knowledge</span>
      </v-btn>
      <v-btn value="circle" to="/circle">
        <v-icon>mdi-account-group</v-icon>
        <span>Social</span>
      </v-btn>
      <v-btn value="vessel" to="/vessel">
        <v-icon>mdi-heart-pulse</v-icon>
        <span>Health</span>
      </v-btn>
    </v-bottom-navigation>

    <!-- Desktop Sidebar -->
    <v-navigation-drawer
      v-if="!isMobile"
      v-model="drawer"
      :rail="rail"
      expand-on-hover
      elevation="2"
      color="surface"
    >
      <v-list>
        <v-list-item
          prepend-avatar="https://cdn.vuetifyjs.com/images/john.png"
          :title="userName"
          subtitle="Nexus Super App"
        ></v-list-item>
      </v-list>

      <v-divider></v-divider>

      <v-list density="compact" nav>
        <v-list-item
          prepend-icon="mdi-wallet"
          title="Finance (The Bag)"
          value="bag"
          to="/bag"
          color="primary"
        ></v-list-item>
        <v-list-item
          prepend-icon="mdi-brain"
          title="Knowledge (The Brain)"
          value="brain"
          to="/brain"
          color="primary"
        ></v-list-item>
        <v-list-item
          prepend-icon="mdi-account-group"
          title="Social (The Circle)"
          value="circle"
          to="/circle"
          color="primary"
        ></v-list-item>
        <v-list-item
          prepend-icon="mdi-heart-pulse"
          title="Health (The Vessel)"
          value="vessel"
          to="/vessel"
          color="primary"
        ></v-list-item>
      </v-list>

      <template v-slot:append>
        <v-list>
          <v-list-item
            prepend-icon="mdi-theme-light-dark"
            title="Toggle Theme"
            @click="toggleTheme"
          ></v-list-item>
        </v-list>
      </template>
    </v-navigation-drawer>

    <!-- Top App Bar -->
    <v-app-bar
      :elevation="isMobile ? 0 : 2"
      color="surface"
      :density="isMobile ? 'compact' : 'default'"
    >
      <v-app-bar-nav-icon
        v-if="!isMobile"
        @click.stop="rail = !rail"
      ></v-app-bar-nav-icon>

      <v-app-bar-title>
        <span class="text-h6 font-weight-bold">Nexus</span>
        <span class="text-subtitle-2 text-primary ml-2">{{ pageTitle }}</span>
      </v-app-bar-title>

      <v-spacer></v-spacer>

      <!-- Theme Toggle (Mobile) -->
      <v-btn
        v-if="isMobile"
        icon="mdi-theme-light-dark"
        @click="toggleTheme"
      ></v-btn>

      <!-- Notifications -->
      <v-btn icon="mdi-bell">
        <v-badge content="3" color="error" model-value></v-badge>
      </v-btn>

      <!-- User Menu -->
      <v-menu>
        <template v-slot:activator="{ props }">
          <v-btn icon v-bind="props">
            <v-avatar size="32">
              <img src="https://cdn.vuetifyjs.com/images/john.png" alt="User">
            </v-avatar>
          </v-btn>
        </template>
        <v-list>
          <v-list-item prepend-icon="mdi-account" title="Profile"></v-list-item>
          <v-list-item prepend-icon="mdi-cog" title="Settings"></v-list-item>
          <v-divider></v-divider>
          <v-list-item prepend-icon="mdi-logout" title="Logout"></v-list-item>
        </v-list>
      </v-menu>
    </v-app-bar>

    <!-- Main Content -->
    <v-main :class="{ 'pb-16': isMobile }">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </v-main>

    <!-- Snackbar for notifications -->
    <v-snackbar
      v-model="snackbar.show"
      :color="snackbar.color"
      :timeout="snackbar.timeout"
      location="bottom"
    >
      {{ snackbar.text }}
      <template v-slot:actions>
        <v-btn color="white" variant="text" @click="snackbar.show = false">
          Close
        </v-btn>
      </template>
    </v-snackbar>
  </v-app>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

// UI State
const drawer = ref(true)
const rail = ref(false)
const currentTab = ref('bag')
const isMobile = ref(false)

// Snackbar state
const snackbar = ref({
  show: false,
  text: '',
  color: 'info',
  timeout: 3000
})

// User info
const userName = ref('Faza')

// Computed
const pageTitle = computed(() => {
  const titles = {
    bag: 'Finance',
    brain: 'Knowledge',
    circle: 'Social',
    vessel: 'Health'
  }
  return titles[route.name] || 'Dashboard'
})

// Methods
const toggleTheme = () => {
  const html = document.documentElement
  const isDark = html.classList.contains('dark')

  if (isDark) {
    html.classList.remove('dark')
    localStorage.setItem('nexus-theme', 'light')
  } else {
    html.classList.add('dark')
    localStorage.setItem('nexus-theme', 'dark')
  }
}

const checkMobile = () => {
  isMobile.value = window.innerWidth < 960
}

// Watch route changes
watch(() => route.name, (newName) => {
  currentTab.value = newName || 'bag'
})

// Lifecycle
onMounted(() => {
  checkMobile()
  window.addEventListener('resize', checkMobile)
})

onUnmounted(() => {
  window.removeEventListener('resize', checkMobile)
})

// Global snackbar function (can be used by any component)
window.showSnackbar = (text, color = 'info', timeout = 3000) => {
  snackbar.value = { show: true, text, color, timeout }
}
</script>

<style scoped>
.bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
}

/* Fade transition */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Mobile padding */
.pb-16 {
  padding-bottom: 4rem;
}
</style>

<style>
/* Global styles */
:root {
  --primary-color: #6366f1;
}

/* Smooth scrolling */
html {
  scroll-behavior: smooth;
}

/* Custom scrollbar */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #555;
}

/* Disable text selection on mobile */
@media (max-width: 960px) {
  * {
    -webkit-tap-highlight-color: transparent;
  }
}
</style>
