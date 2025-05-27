import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import axios from 'axios'

import App from './App.vue'
import router from './router'

import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

const app = createApp(App)

const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)

app.use(pinia)

// ✅ axios header 설정은 store보다 늦어도 됨
const token = localStorage.getItem('token')
if (token) {
  axios.defaults.headers.common.Authorization = `Token ${token}`
}

app.use(router)
app.use(createVuetify({ components, directives }))

app.mount('#app')