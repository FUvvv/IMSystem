import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import axios from 'axios'

// 配置 Axios 全局请求拦截器
axios.interceptors.request.use(config => {
  // 从 localStorage 获取当前登录的用户名
  const username = localStorage.getItem('username')
  if (username) {
    // 将用户名放入请求头中，供后端校验权限和记录日志
    config.headers['X-Username'] = username
  }
  return config
}, error => {
  return Promise.reject(error)
})

// 配置 Axios 全局响应拦截器，统一处理 401/403 权限错误
axios.interceptors.response.use(response => {
  return response
}, error => {
  if (error.response && error.response.status === 403) {
    // 可以配合 ElementPlus 的 ElMessage 提示权限不足
    console.error("权限不足:", error.response.data.detail)
  }
  return Promise.reject(error)
})

const app = createApp(App)
app.use(router)
app.use(ElementPlus)
app.mount('#app')
