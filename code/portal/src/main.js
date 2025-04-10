import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router' //aca importa la config de las rutas definidas en index.js

const app = createApp(App)

app.use(createPinia())
app.use(router) //aca permite q las rutan esten disponibles

app.mount('#app')
