<template>
  <el-card>
    <template #header>系统操作日志</template>
    
    <!-- 查询与导出 -->
    <el-form :inline="true" :model="searchForm" class="demo-form-inline">
      <el-form-item label="操作人">
        <el-input v-model="searchForm.user" placeholder="输入用户名" clearable />
      </el-form-item>
      <el-form-item label="日志类型">
        <el-select v-model="searchForm.type" placeholder="全部" clearable>
          <el-option label="登录日志" value="登录" />
          <el-option label="操作日志" value="操作" />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handleSearch">查询</el-button>
        <el-button type="success" @click="exportLogs">导出日志 (Excel)</el-button>
      </el-form-item>
    </el-form>

    <!-- 日志列表 -->
    <el-table :data="logs" border stripe style="width: 100%">
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
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'

const searchForm = reactive({ user: '', type: '' })

const logs = ref([
  { id: 1001, user: 'admin', type: '登录', action: '用户登录系统', create_time: '2026-03-31 08:30:00' },
  { id: 1002, user: 'admin', type: '操作', action: '新增商品 [联想ThinkPad笔记本]', create_time: '2026-03-31 09:15:22' },
  { id: 1003, user: 'zhangsan', type: '操作', action: '审核采购单 [PO-20260331-01]', create_time: '2026-03-31 10:05:10' },
  { id: 1004, user: 'admin', type: '操作', action: '修改用户 [lisi] 状态为禁用', create_time: '2026-03-31 11:20:45' }
])

const handleSearch = () => {
  ElMessage.info('执行过滤查询逻辑...')
}

const exportLogs = () => {
  ElMessage.success('日志已成功导出为 Excel 文件！')
}
</script>
