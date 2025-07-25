import { createApp } from 'vue'
import './style.css'
import App from './App.vue'

import { createRouter, createWebHashHistory } from 'vue-router'

// Importing pages
import LandingPage from './pages/LandingPage.vue'
import ResultsPage from './pages/ResultsPage.vue'
import NotFoundPage from './pages/NotFoundPage.vue'


const routes = [
    { path: '/', component: LandingPage },
    { path: '/search', component: ResultsPage },
    { path: '/:catchAll(.*)', component: NotFoundPage },
]

const router = createRouter({
    history: createWebHashHistory(),
    routes
})


const app = createApp(App)
app.use(router)
app.mount('#app')
