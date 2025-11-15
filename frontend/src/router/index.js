import { createRouter, createWebHistory } from 'vue-router'
import UserManagement from '../components/UserManagement.vue'
import ProductManagement from '../components/ProductManagement.vue'
import OrderManagement from '../components/OrderManagement.vue'
import SalesAnalytics from '../components/SalesAnalytics.vue'

const routes = [
  { path: '/', redirect: '/users' },
  { path: '/users', component: UserManagement },
  { path: '/products', component: ProductManagement },
  { path: '/orders', component: OrderManagement },
  { path: '/analytics', component: SalesAnalytics }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router


