import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify'

// Dark mode support
const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)')
const savedTheme = localStorage.getItem('nexus-theme')

let darkMode = savedTheme ? savedTheme === 'dark' : prefersDarkScheme.matches

if (darkMode) {
  document.documentElement.classList.add('dark')
}

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(vuetify)

app.mount('#app')
