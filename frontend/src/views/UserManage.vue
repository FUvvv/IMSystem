<template>
  <el-card>
    <template #header>
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <span>用户与权限管理</span>
        <el-button type="primary" @click="dialogVisible = true">新增用户</el-button>
      </div>
    </template>

    <el-table :data="users" border style="width: 100%">
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
      <el-table-column label="操作" width="150">
        <template #default="scope">
          <el-button size="small" @click="editUser(scope.row)">编辑</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 用户弹窗 -->
    <el-dialog title="用户信息" v-model="dialogVisible" width="400px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="用户名">
          <el-input v-model="form.username"></el-input>
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="form.password" type="password" placeholder="不修改请留空"></el-input>
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
        <el-button type="primary" @click="dialogVisible = false; $message.success('保存成功')">确定</el-button>
      </template>
    </el-dialog>
  </el-card>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'

const users = ref([
  { id: 1, username: 'admin', role: 'admin', status: true },
  { id: 2, username: 'zhangsan', role: 'user', status: true },
  { id: 3, username: 'lisi', role: 'user', status: false }
])

const dialogVisible = ref(false)
const form = reactive({ id: null, username: '', password: '', role: 'user' })

const editUser = (row) => {
  Object.assign(form, row)
  form.password = ''
  dialogVisible.value = true
}

const handleStatusChange = (row) => {
  ElMessage.success(`用户 ${row.username} 状态已更新为: ${row.status ? '正常' : '禁用'}`)
}
</script>
