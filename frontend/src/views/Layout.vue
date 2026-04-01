<template>
  <el-container style="height: 100vh;">
    <el-aside width="200px" style="background-color: #2c3e50;">
      <h3 style="color:white; text-align:center;">库存管理系统</h3>
      <el-menu active-text-color="#409EFF" background-color="#2c3e50" text-color="#fff" router>
        <el-menu-item index="/dashboard">报表管理(大盘)</el-menu-item>
        <el-menu-item index="/products">商品管理</el-menu-item>
        <el-menu-item index="/inventory">库存管理</el-menu-item>
        <el-menu-item index="/purchase">采购管理</el-menu-item>
        <el-menu-item index="/sales">销售管理</el-menu-item>
        <el-menu-item index="/users">用户管理</el-menu-item>
        <el-menu-item index="/logs">系统日志</el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header style="background: #fff; border-bottom: 1px solid #eee; display:flex; justify-content: space-between; align-items:center;">
        <span style="font-size: 18px; font-weight: bold;">业务处理中心</span>
        <div>
          <span style="margin-right: 15px;">欢迎您, {{ username }}</span>
          <el-button type="danger" size="small" @click="handleLogout">注销退出</el-button>
        </div>
      </el-header>
      <el-main style="background: #f0f2f5;">
        <router-view></router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()
const username = ref(localStorage.getItem('username') || 'Admin')

const handleLogout = () => {
  ElMessageBox.confirm('确定要注销退出系统吗？', '提示', { type: 'warning' }).then(() => {
    localStorage.removeItem('token')
    localStorage.removeItem('username')
    ElMessage.success('已安全退出')
    router.push('/login')
  }).catch(() => {})
}
</script>
