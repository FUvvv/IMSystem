<template>
  <el-card>
    <template #header>实时库存与预警管理</template>
    <el-table :data="inventory" style="width: 100%">
      <el-table-column prop="product_name" label="商品名称" />
      <el-table-column prop="quantity" label="当前库存">
        <template #default="scope">
          <el-tag :type="scope.row.quantity < scope.row.min_alert ? 'danger' : 'success'">
            {{ scope.row.quantity }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="min_alert" label="最低阈值" />
      <el-table-column label="操作">
        <template #default>
          <el-button size="small" type="primary">入库</el-button>
          <el-button size="small" type="warning">出库</el-button>
        </template>
      </el-table-column>
    </el-table>
  </el-card>
</template>
<script setup>
import { ref } from 'vue'
// 模拟数据
const inventory = ref([
  { product_name: '测试商品A', quantity: 5, min_alert: 10 },
  { product_name: '测试商品B', quantity: 50, min_alert: 10 }
])
</script>
