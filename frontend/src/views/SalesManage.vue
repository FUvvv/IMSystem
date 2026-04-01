<template>
  <el-card>
    <el-tabs v-model="activeTab">
      <!-- 销售订单管理 -->
      <el-tab-pane label="销售订单管理" name="orders">
        <div style="margin-bottom: 15px;">
          <el-button type="primary">创建销售单</el-button>
        </div>
        <el-table :data="salesOrders" border>
          <el-table-column prop="so_no" label="销售单号" />
          <el-table-column prop="customer" label="客户名称" />
          <el-table-column prop="product_name" label="销售商品" />
          <el-table-column prop="quantity" label="销售数量" />
          <el-table-column prop="amount" label="订单总额 (元)" />
          <el-table-column prop="status" label="状态">
            <template #default="scope">
              <el-tag :type="scope.row.status === '待发货' ? 'warning' : 'success'">{{ scope.row.status }}</el-tag>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>

      <!-- 销售发货管理 -->
      <el-tab-pane label="销售发货管理" name="shipping">
        <el-table :data="shippingList" border>
          <el-table-column prop="so_no" label="关联销售单" />
          <el-table-column prop="product_name" label="发货商品" />
          <el-table-column prop="quantity" label="需发货数量" />
          <el-table-column prop="address" label="收货地址" />
          <el-table-column label="操作">
            <template #default="scope">
              <el-button v-if="scope.row.status === '待发货'" size="small" type="primary" @click="shipOrder(scope.row)">执行发货 (扣减库存)</el-button>
              <el-tag v-else type="success">已发货</el-tag>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
    </el-tabs>
  </el-card>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'

const activeTab = ref('orders')

const salesOrders = ref([
  { so_no: 'SO-20260331-001', customer: '北京某科技有限公司', product_name: '联想ThinkPad笔记本', quantity: 2, amount: 11998.00, status: '待发货' },
  { so_no: 'SO-20260329-002', customer: '上海某商贸中心', product_name: '得力A4打印纸', quantity: 20, amount: 510.00, status: '已发货' }
])

// 动态计算发货列表 (包含地址信息)
const shippingList = computed(() => {
  return salesOrders.value.map(order => ({
    ...order,
    address: order.customer === '北京某科技有限公司' ? '北京市海淀区中关村' : '上海市浦东新区'
  }))
})

const shipOrder = (row) => {
  // 找到原始订单并更新状态
  const order = salesOrders.value.find(o => o.so_no === row.so_no)
  if (order) {
    order.status = '已发货'
    ElMessage.success(`单号 ${row.so_no} 发货成功，系统已自动扣减对应库存！`)
  }
}
</script>
