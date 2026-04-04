<template>
  <div>
    <div style="margin-bottom: 20px; display: flex; justify-content: space-between;">
      <h2>多维度数据报表与查询</h2>
      <el-button type="success" icon="Download" @click="exportReport">导出库存报表 (Excel)</el-button>
    </div>

    <el-row :gutter="20" style="margin-bottom: 20px;">
      <el-col :span="6">
        <el-card shadow="hover">
          <div style="color: #909399;">平台商品总数</div>
          <div style="font-size: 24px; font-weight: bold;">{{ summary.product_count }} 件</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div style="color: #909399;">库存预警SKU</div>
          <div style="font-size: 24px; font-weight: bold; color: red;">{{ summary.low_stock_count }} 个</div>
        </el-card>
      </el-col>
    </el-row>

    <el-card>
      <el-tabs v-model="activeTab">
        <el-tab-pane label="商品情况查询" name="products">
          <el-table :data="productStats" border stripe>
            <el-table-column prop="category" label="商品分类" />
            <el-table-column prop="count" label="商品种类数" />
            <el-table-column prop="avgPrice" label="平均单价 (元)" />
          </el-table>
        </el-tab-pane>

        <el-tab-pane label="库存情况查询" name="inventory">
          <el-row :gutter="20">
            <el-col :span="12">
              <el-table :data="inventoryStats" border stripe>
                <el-table-column prop="name" label="商品名称" />
                <el-table-column prop="stock" label="当前库存" />
                <el-table-column prop="status" label="状态">
                  <template #default="scope">
                    <el-tag :type="scope.row.stock < scope.row.min_alert ? 'danger' : 'success'">
                      {{ scope.row.stock < scope.row.min_alert ? '库存预警' : '库存充足' }}
                    </el-tag>
                  </template>
                </el-table-column>
              </el-table>
            </el-col>
            <el-col :span="12">
              <div ref="inventoryChartRef" style="height: 300px;"></div>
            </el-col>
          </el-row>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, watch } from 'vue'
import axios from 'axios'
import * as echarts from 'echarts'
import * as XLSX from 'xlsx'
import { ElMessage } from 'element-plus'

const activeTab = ref('inventory')
const summary = ref({ product_count: 0, low_stock_count: 0 })
const productStats = ref([])
const inventoryStats = ref([])
const inventoryChartRef = ref(null)

const fetchDashboardData = async () => {
  const res = await axios.get('http://localhost:8000/api/dashboard')
  summary.value = res.data.summary
  productStats.value = res.data.product_stats
  inventoryStats.value = res.data.inventory_stats
  renderCharts()
}

const renderCharts = () => {
  if (inventoryChartRef.value && inventoryStats.value.length > 0) {
    const invChart = echarts.init(inventoryChartRef.value)
    // 提取分类库存总数作图
    const pieData = productStats.value.map(p => ({ name: p.category, value: p.count }))
    invChart.setOption({
      title: { text: '各分类商品种类占比', left: 'center' },
      tooltip: { trigger: 'item' },
      series: [{ type: 'pie', radius: '60%', data: pieData }]
    })
  }
}

watch(activeTab, async () => {
  await nextTick()
  renderCharts()
})

const exportReport = () => {
  if (inventoryStats.value.length === 0) return ElMessage.warning('暂无数据可导出')
  
  const exportData = inventoryStats.value.map(item => ({
    '商品名称': item.name,
    '当前库存': item.stock,
    '预警阈值': item.min_alert,
    '状态': item.stock < item.min_alert ? '库存预警' : '正常'
  }))

  const ws = XLSX.utils.json_to_sheet(exportData)
  const wb = XLSX.utils.book_new()
  XLSX.utils.book_append_sheet(wb, ws, '库存报表')
  XLSX.writeFile(wb, `库存报表_${new Date().getTime()}.xlsx`)
  ElMessage.success('报表导出成功')
}

onMounted(() => fetchDashboardData())
</script>
