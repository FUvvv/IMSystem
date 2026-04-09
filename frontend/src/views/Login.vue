<template>
  <div class="login-container">
    <el-card class="login-card">
      <h2 style="text-align: center; margin-bottom: 20px;">库存管理系统</h2>
      <el-form :model="form" @keyup.enter="handleSubmit">
        <el-form-item>
          <el-input v-model="form.username" placeholder="请输入用户名" clearable />
        </el-form-item>
        <el-form-item>
          <el-input v-model="form.password" type="password" placeholder="请输入密码" show-password />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" style="width: 100%;" @click="handleSubmit" :loading="loading">
            {{ isLogin ? '登 录' : '注 册' }}
          </el-button>
        </el-form-item>
        <div style="text-align: right; font-size: 14px;">
          <el-link type="primary" @click="isLogin = !isLogin">
            {{ isLogin ? '没有账号？去注册' : '已有账号？去登录' }}
          </el-link>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import axios from 'axios'

const router = useRouter()
const form = reactive({ username: '', password: '' })
const loading = ref(false)
const isLogin = ref(true)

const handleSubmit = async () => {
  if (!form.username || !form.password) return ElMessage.warning('请输入用户名和密码')
  loading.value = true
  try {
    if (isLogin.value) {
      const res = await axios.post('http://localhost:8000/api/login', form)
      ElMessage.success('登录成功！')
      localStorage.setItem('token', res.data.token)
      localStorage.setItem('username', res.data.username)
      router.push('/')
    } else {
      await axios.post('http://localhost:8000/api/register', form)
      ElMessage.success('注册成功，请登录！')
      isLogin.value = true // 切换回登录模式
    }
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || '操作失败')
  } finally {
    loading.value = false
  }
}
</script>
<style scoped>
.login-container { height: 100vh; display: flex; justify-content: center; align-items: center; background-color: #2d3a4b; }
.login-card { width: 400px; padding: 30px 20px; }
</style>
