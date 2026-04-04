<template>
  <div class="login-container">
    <el-card class="login-card">
      <h2 style="text-align: center; margin-bottom: 20px;">库存管理系统</h2>
      <el-form :model="form" @keyup.enter="handleLogin">
        <el-form-item>
          <el-input v-model="form.username" placeholder="请输入用户名" clearable />
        </el-form-item>
        <el-form-item>
          <el-input v-model="form.password" type="password" placeholder="请输入密码" show-password />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" style="width: 100%;" @click="handleLogin" :loading="loading">登 录</el-button>
        </el-form-item>
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

const handleLogin = async () => {
  if (!form.username || !form.password) {
    return ElMessage.warning('请输入用户名和密码')
  }
  
  loading.value = true
  try {
    // 调用后端真实登录接口
    const res = await axios.post('http://localhost:8000/api/login', {
      username: form.username,
      password: form.password
    })
    
    ElMessage.success('登录成功！')
    // 保存后端返回的 token 和用户名
    localStorage.setItem('token', res.data.token)
    localStorage.setItem('username', res.data.username)
    
    router.push('/')
  } catch (error) {
    // 捕获后端返回的具体错误信息（如密码错误、账号禁用等）
    ElMessage.error(error.response?.data?.detail || '服务器连接失败')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #2d3a4b;
}
.login-card {
  width: 400px;
  padding: 30px 20px;
}
</style>
