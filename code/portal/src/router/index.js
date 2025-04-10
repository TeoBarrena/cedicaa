import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import PublicationDetail from '../components/PublicationDetail.vue'

//definición de rutas
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/contact',
      name: 'contact',
      component: () => import('../views/ContactView.vue'), //parte de la api en la app privad
    },
    {
      path: '/publications/:id',
      name: 'publication',
      component: PublicationDetail,
    },
    {
      path: '/publications',
      name: 'publications',
      component: () => import('../views/PublicationsView.vue'), //parte de la api app privada
    },
  ],
})

export default router
