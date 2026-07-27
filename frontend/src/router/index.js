import { createRouter, createWebHistory } from 'vue-router'

import { authState } from '../stores/auth'
import LoginView from '../views/LoginView.vue'
import NamingView from '../views/NamingView.vue'
import RegisterView from '../views/RegisterView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', redirect: '/naming' },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      meta: { guestOnly: true },
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView,
      meta: { guestOnly: true },
    },
    {
      path: '/naming',
      name: 'naming',
      component: NamingView,
      meta: { requiresAuth: true },
    },
    { path: '/:pathMatch(.*)*', redirect: '/naming' },
  ],
})

router.beforeEach((to) => {
  if (to.meta.requiresAuth && !authState.token) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }
  if (to.meta.guestOnly && authState.token) {
    return { name: 'naming' }
  }
})

export default router
