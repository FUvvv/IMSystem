<template>
  <el-card>
    <el-tabs v-model="activeTab">
      <!-- 采购需求申请 -->
      <el-tab-pane label="采购需求申请" name="request">
        <el-button type="primary" style="margin-bottom: 15px;">发起采购申请</el-button>
        <el-table :data="requests" border>
          <el-table-column prop="req_no" label="申请单号" />
          <el-table-column prop="product_name" label="需求商品" />
          <el-table-column prop="quantity" label="申请数量" />
          <el-table-column prop="applicant" label="申请人" />
          <el-table-column prop="status" label="状态">
            <template #default="scope">
              <el-tag :type="scope.row.status === '已转订单' ? 'success' : 'warning'">{{ scope.row.status }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作">
            <template #default>
              <el-button size="small" type="success">生成采购单</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>

      <!-- 采购订单管理 & 入库验收 -->
      <el-tab-pane label="采购订单与验收" name="order">
        <el-table :data="orders" border>
          <el-table-column prop="order_no" label="采购单号" />
          <el-table-column prop="product_name" label="商品名称" />
          <el-table-column prop="quantity" label="采购数量" />
          <el-table-column prop="status" label="订单状态">
            <template #default="scope">
              <el-tag v-if="scope.row.status === '待审核'" type="danger">待审核</el-tag>
              <el-tag v-else-if="scope.row.status === '待入库'" type="warning">待入库</el-tag>
              <el-tag v-else type="success">已入库</el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="250">
            <template #default="scope">
              <el-button v-if="scope.row.status === '待审核'" size="small" type="primary" @click="auditOrder(scope.row)">审核通过</el-button>
              <el-button v-if="scope.row.status === '待入库'" size="small" type="success" @click="receiveOrder(scope.row)">验收并入库</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
    </el-tabs>
  </el-card>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

const activeTab = ref('order')

const requests = ref([
  { req_no: 'REQ-001', product_name: '得力A4打印纸', quantity: 100, applicant: 'zhangsan', status: '待处理' },
  { req_no: 'REQ-002', product_name: '联想ThinkPad笔记本', quantity: 5, applicant: 'lisi', status: '已转订单' }
])

const orders = ref([
  { order_no: 'PO-20260331-01', product_name: '联想ThinkPad笔记本', quantity: 5, status: '待审核' },
  { order_no: 'PO-20260331-02', product_name: '得力A4打印纸', quantity: 100, status: '待入库' },
  { order_no: 'PO-20260330-01', product_name: '罗技鼠标', quantity: 50, status: '已入库' }
])

const auditOrder = (row) => {
  row.status = '待入库'
  ElMessage.success(`订单 ${row.order_no} 审核通过，等待入库`)
}

const receiveOrder = (row) => {
  row.status = '已入库'
  ElMessage.success(`订单 ${row.order_no} 验收完成，库存已增加！`)
}
</script>
