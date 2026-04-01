<template>
  <div class="login-container">
    <el-card class="login-card">
      <h2 style="text-align: center; margin-bottom: 20px;">库存管理系统登录</h2>
      <el-form :model="form" @keyup.enter="handleLogin">
        <el-form-item>
          <el-input v-model="form.username" placeholder="请输入用户名 (admin)" clearable />
        </el-form-item>
        <el-form-item>
          <el-input v-model="form.password" type="password" placeholder="请输入密码 (123456)" show-password />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" style="width: 100%;" @click="handleLogin">登 录</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()
const form = reactive({ username: '', password: '' })

const handleLogin = () => {
  if (form.username === 'admin' && form.password === '123456') {
    ElMessage.success('登录成功！')
    localStorage.setItem('token', 'mock_token_123') // 模拟保存 token
    localStorage.setItem('username', 'admin')
    router.push('/')
  } else {
    ElMessage.error('用户名或密码错误，请尝试 admin / 123456')
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
  padding: 20px;
}
</style>
