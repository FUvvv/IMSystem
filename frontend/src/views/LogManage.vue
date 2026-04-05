<template>
  <el-card>
    <template #header>系统操作日志</template>
    
    <el-form :inline="true" :model="searchForm">
      <el-form-item label="操作人">
        <el-input v-model="searchForm.user" placeholder="输入用户名" clearable />
      </el-form-item>
      <el-form-item label="日志类型">
        <el-select v-model="searchForm.type" placeholder="全部" clearable style="width: 150px">
          <el-option label="登录" value="登录" />
          <el-option label="操作" value="操作" />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="fetchLogs">查询</el-button>
        <el-button type="success" @click="exportLogs">导出日志 (Excel)</el-button>
      </el-form-item>
    </el-form>

    <el-table :data="logs" border stripe style="width: 100%" v-loading="loading">
      <el-table-column prop="id" label="日志ID" width="100" />
      <el-table-column prop="user" label="操作人" width="150" />
      <el-table-column prop="type" label="类型" width="120">
        <template #default="scope">
          <el-tag :type="scope.row.type === '登录' ? 'success' : 'warning'">{{ scope.row.type }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="action" label="操作内容" />
      <el-table-column prop="create_time" label="操作时间" width="200" />
    </el-table>
  </el-card>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import axios from 'axios'
import * as XLSX from 'xlsx'
import { ElMessage } from 'element-plus'

const searchForm = reactive({ user: '', type: '' })
const logs = ref([])
const loading = ref(false)

const fetchLogs = async () => {
  loading.value = true
  const params = {}
  if (searchForm.user) params.user = searchForm.user
  if (searchForm.type) params.type = searchForm.type
  const res = await axios.get('http://localhost:8000/api/logs', { params })
  logs.value = res.data
  loading.value = false
}

const exportLogs = () => {
  if (logs.value.length === 0) return ElMessage.warning('暂无数据可导出')
  
  // 格式化导出数据
  const exportData = logs.value.map(log => ({
    '日志ID': log.id,
    '操作人': log.user,
    '日志类型': log.type,
    '操作内容': log.action,
    '操作时间': log.create_time
  }))

  const ws = XLSX.utils.json_to_sheet(exportData)
  const wb = XLSX.utils.book_new()
  XLSX.utils.book_append_sheet(wb, ws, '系统日志')
  XLSX.writeFile(wb, `系统日志_${new Date().getTime()}.xlsx`)
  ElMessage.success('日志导出成功')
}

onMounted(() => fetchLogs())
</script>
