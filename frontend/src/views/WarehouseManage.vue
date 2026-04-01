<template>
  <div>
    <el-button type="primary" style="margin-bottom: 20px;">新增仓库 (待完善表单)</el-button>
    <el-table :data="warehouses" border style="width: 100%">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="code" label="仓库编号" width="120" />
      <el-table-column prop="name" label="仓库名称" />
      <el-table-column prop="address" label="详细地址" />
      <el-table-column prop="manager" label="负责人" width="120" />
    </el-table>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const warehouses = ref([])
onMounted(async () => {
  const res = await axios.get('http://localhost:8000/api/warehouses')
  warehouses.value = res.data
})
</script>
