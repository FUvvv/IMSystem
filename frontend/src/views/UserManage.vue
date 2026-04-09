<template>
  <el-card>
    <template #header>
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <span>用户与权限管理</span>
        <el-button type="primary" @click="openDialog('add')">新增用户</el-button>
      </div>
    </template>

    <el-table :data="users" border style="width: 100%" v-loading="loading">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="username" label="用户名" />
      <el-table-column prop="role" label="角色权限">
        <template #default="scope">
          <el-tag :type="scope.row.role === 'admin' ? 'danger' : 'info'">
            {{ scope.row.role === 'admin' ? '超级管理员' : '普通员工' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="status" label="账号状态" width="120">
        <template #default="scope">
          <el-switch v-model="scope.row.status" active-text="正常" inactive-text="禁用" @change="handleStatusChange(scope.row)" />
        </template>
      </el-table-column>
      <el-table-column label="操作" width="250">
        <template #default="scope">
          <el-button size="small" @click="openDialog('edit', scope.row)">编辑角色</el-button>
          <el-button size="small" type="warning" @click="resetPassword(scope.row.id)">重置密码</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog :title="dialogType === 'add' ? '新增用户' : '编辑用户'" v-model="dialogVisible" width="400px">
            <el-form :model="form" label-width="80px">
        <el-form-item label="用户名">
          <el-input v-model="form.username" :disabled="dialogType === 'edit'"></el-input>
        </el-form-item>
        <el-form-item label="密码" v-if="dialogType === 'add'">
          <el-input v-model="form.password" type="password" placeholder="请输入初始密码"></el-input>
        </el-form-item>
        <el-form-item label="角色">
          <el-select v-model="form.role" style="width: 100%;">
            <el-option label="超级管理员" value="admin" />
            <el-option label="普通员工" value="user" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveUser">确定</el-button>
      </template>
    </el-dialog>
  </el-card>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'

const apiBase = 'http://localhost:8000/api'
const users = ref([])
const loading = ref(false)
const dialogVisible = ref(false)
const dialogType = ref('add')
const form = reactive({ id: null, username: '', password: '', role: 'user', status: true })

const fetchUsers = async () => {
  loading.value = true
  const res = await axios.get(`${apiBase}/users`)
  users.value = res.data
  loading.value = false
}

const openDialog = (type, row = null) => {
  dialogType.value = type
  if (type === 'edit') {
    Object.assign(form, row)
    form.password = '' // 密码置空
  } else {
    Object.assign(form, { id: null, username: '', password: '', role: 'user', status: true })
  }
  dialogVisible.value = true
}

const saveUser = async () => {
  try {
    if (dialogType.value === 'add') {
      if (!form.password) return ElMessage.warning('密码不能为空')
      await axios.post(`${apiBase}/users`, form)
      ElMessage.success('新增成功')
    } else {
      await axios.put(`${apiBase}/users/${form.id}`, form)
      ElMessage.success('修改成功')
    }
    dialogVisible.value = false
    fetchUsers()
  } catch (e) {
    ElMessage.error('操作失败')
  }
}

const handleStatusChange = async (row) => {
  try {
    await axios.put(`${apiBase}/users/${row.id}`, {
      username: row.username,
      role: row.role,
      status: row.status
    })
    ElMessage.success(`状态已更新为: ${row.status ? '正常' : '禁用'}`)
  } catch (e) {
    row.status = !row.status // 失败回滚开关状态
    ElMessage.error('状态更新失败')
  }
}

const resetPassword = async (userId) => {
  try {
    await axios.post(`${apiBase}/users/reset_password`, { user_id: userId })
    ElMessage.success('密码已重置为 123456')
  } catch (e) {
    ElMessage.error(e.response?.data?.detail || '重置失败')
  }
}

onMounted(() => fetchUsers())
</script>
