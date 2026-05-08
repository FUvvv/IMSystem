<template>
  <el-card>
    <template #header>实时库存与预警管理</template>
    <el-table :data="inventory" style="width: 100%" v-loading="loading" border>
      <el-table-column prop="product_name" label="商品名称" />
      <el-table-column prop="quantity" label="当前库存">
        <template #default="scope">
          <el-tag :type="scope.row.quantity < scope.row.min_alert ? 'danger' : 'success'">
            {{ scope.row.quantity }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="min_alert" label="预警阈值" width="100" />
      <el-table-column label="操作" width="250">
        <template #default="scope">
          <el-button size="small" type="primary" @click="handleStock(scope.row, 'in')">入库</el-button>
          <el-button size="small" type="warning" @click="handleStock(scope.row, 'out')">出库</el-button>
        </template>
      </el-table-column>
    </el-table>
  </el-card>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import axios from 'axios'

const inventory = ref([])
const loading = ref(false)

const fetchInventory = async () => {
  loading.value = true
  const res = await axios.get('http://localhost:8000/api/inventory')
  inventory.value = res.data
  loading.value = false
}

const handleStock = (row, type) => {
  const actionName = type === 'in' ? '入库' : '出库'
  
  // 如果是出库操作，先检查当前库存
  if (type === 'out') {
    if (row.quantity <= 0) {
      ElMessage.warning(`【${row.product_name}】当前库存为0，无法进行出库操作`)
      return
    }
  }
  
  ElMessageBox.prompt(`请输入【${row.product_name}】的${actionName}数量:`, actionName, {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    inputPattern: /^[1-9]\d*$/,
    inputErrorMessage: '请输入正整数'
  }).then(async ({ value }) => {
    const change = parseInt(value)
    
    // 如果是出库操作，判断库存是否充足
    if (type === 'out') {
      if (change > row.quantity) {
        ElMessage.error(`库存不足！当前库存为 ${row.quantity}，出库数量为 ${change}，无法完成出库操作`)
        return // 直接返回，不执行出库
      }
    }
    
    // 计算最终的库存变动值
    const quantityChange = type === 'in' ? change : -change
    
    try {
      await axios.put(`http://localhost:8000/api/inventory/${row.id}`, { quantity_change: quantityChange })
      ElMessage.success(`${actionName}成功！${type === 'out' ? `出库 ${change} 件` : `入库 ${change} 件`}`)
      fetchInventory()
    } catch (e) {
      // 处理后端返回的错误（如数据库层面的库存不足校验）
      if (e.response?.data?.detail) {
        ElMessage.error(e.response.data.detail)
      } else {
        ElMessage.error(`${actionName}失败`)
      }
    }
  }).catch(() => {
    // 用户取消操作
  })
}

onMounted(() => fetchInventory())
</script>
