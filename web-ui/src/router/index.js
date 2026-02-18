import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import BagView from '../views/BagView.vue'
import BrainView from '../views/BrainView.vue'
import CircleView from '../views/CircleView.vue'
import VesselView from '../views/VesselView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/bag',
      name: 'bag',
      component: BagView
    },
    {
      path: '/brain',
      name: 'brain',
      component: BrainView
    },
    {
      path: '/circle',
      name: 'circle',
      component: CircleView
    },
    {
      path: '/vessel',
      name: 'vessel',
      component: VesselView
    }
  ]
})

export default router
