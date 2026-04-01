import { createRouter, createWebHistory } from 'vue-router'
import Layout from '../views/Layout.vue'

const routes = [
  {
    path: '/login',
    component: () => import('../views/Login.vue')
  },
  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    children: [
      { path: 'dashboard', component: () => import('../views/ReportManage.vue') },
      { path: 'products', component: () => import('../views/ProductManage.vue') },
      { path: 'inventory', component: () => import('../views/InventoryManage.vue') },
      { path: 'purchase', component: () => import('../views/PurchaseManage.vue') },
      { path: 'sales', component: () => import('../views/SalesManage.vue') },
      { path: 'users', component: () => import('../views/UserManage.vue') },
      { path: 'logs', component: () => import('../views/LogManage.vue') }
    ]
  }
]

const router = createRouter({ history: createWebHistory(), routes })

// 简单的路由守卫：未登录则跳转登录页
router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('token')
  if (to.path !== '/login' && !isAuthenticated) {
    next('/login')
  } else {
    next()
  }
})

export default router
  