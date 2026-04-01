<template>
  <div>
    <div style="margin-bottom: 20px; display: flex; justify-content: space-between;">
      <h2>多维度数据报表与查询</h2>
      <el-button type="success" icon="Download" @click="exportReport">导出综合报表 (Excel)</el-button>
    </div>

    <!-- 顶部数据概览卡片 -->
    <el-row :gutter="20" style="margin-bottom: 20px;">
      <el-col :span="6" v-for="item in summaryData" :key="item.title">
        <el-card shadow="hover">
          <div style="font-size: 14px; color: #909399;">{{ item.title }}</div>
          <div style="font-size: 24px; font-weight: bold; margin-top: 10px;">{{ item.value }}</div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 分类查询 Tabs -->
    <el-card>
      <el-tabs v-model="activeTab">
        
        <!-- 商品情况 -->
        <el-tab-pane label="商品情况查询" name="products">
          <el-table :data="productStats" border stripe>
            <el-table-column prop="category" label="商品分类" />
            <el-table-column prop="count" label="商品种类数" />
            <el-table-column prop="avgPrice" label="平均单价 (元)" />
          </el-table>
        </el-tab-pane>

        <!-- 库存情况 -->
        <el-tab-pane label="库存情况查询" name="inventory">
          <el-row :gutter="20">
            <el-col :span="12">
              <el-table :data="inventoryStats" border stripe>
                <el-table-column prop="name" label="商品名称" />
                <el-table-column prop="stock" label="当前库存" />
                <el-table-column prop="status" label="状态">
                  <template #default="scope">
                    <el-tag :type="scope.row.stock < 20 ? 'danger' : 'success'">
                      {{ scope.row.stock < 20 ? '库存预警' : '库存充足' }}
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

        <!-- 采购情况 -->
        <el-tab-pane label="采购情况查询" name="purchase">
          <div ref="purchaseChartRef" style="height: 350px;"></div>
        </el-tab-pane>

        <!-- 销售情况 -->
        <el-tab-pane label="销售情况查询" name="sales">
           <div ref="salesChartRef" style="height: 350px;"></div>
        </el-tab-pane>

      </el-tabs>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, watch } from 'vue'
import * as echarts from 'echarts'
import { ElMessage } from 'element-plus'

const activeTab = ref('inventory')

// 顶部概览数据
const summaryData = ref([
  { title: '平台商品总数', value: '156 件' },
  { title: '库存预警SKU', value: '12 个' },
  { title: '本月采购总额', value: '¥ 45,200' },
  { title: '本月销售总额', value: '¥ 128,500' }
])

// 商品统计表格数据
const productStats = ref([
  { category: '电子产品', count: 45, avgPrice: 3200.00 },
  { category: '办公用品', count: 80, avgPrice: 45.50 },
  { category: '日用百货', count: 31, avgPrice: 22.00 }
])

// 库存统计表格数据
const inventoryStats = ref([
  { name: '联想ThinkPad笔记本', stock: 15 },
  { name: '得力A4打印纸', stock: 500 },
  { name: '罗技无线鼠标', stock: 8 }
])

// 图表引用
const inventoryChartRef = ref(null)
const purchaseChartRef = ref(null)
const salesChartRef = ref(null)

// 渲染图表函数
const renderCharts = () => {
  // 1. 库存饼图
  if (inventoryChartRef.value) {
    const invChart = echarts.init(inventoryChartRef.value)
    invChart.setOption({
      title: { text: '库存资产占比', left: 'center' },
      tooltip: { trigger: 'item' },
      series: [{
        type: 'pie', radius: '60%',
        data: [
          { value: 48000, name: '电子产品' },
          { value: 22500, name: '办公用品' },
          { value: 6820, name: '日用百货' }
        ]
      }]
    })
  }

  // 2. 采购柱状图
  if (purchaseChartRef.value) {
    const purChart = echarts.init(purchaseChartRef.value)
    purChart.setOption({
      title: { text: '近六个月采购金额走势' },
      tooltip: {},
      xAxis: { type: 'category', data: ['10月', '11月', '12月', '1月', '2月', '3月'] },
      yAxis: { type: 'value', name: '金额 (元)' },
      series: [{ type: 'bar', data: [12000, 15000, 8000, 22000, 18000, 45200], itemStyle: { color: '#409EFF' } }]
    })
  }

  // 3. 销售折线图
  if (salesChartRef.value) {
    const saleChart = echarts.init(salesChartRef.value)
    saleChart.setOption({
      title: { text: '近六个月销售额与利润趋势' },
      tooltip: { trigger: 'axis' },
      legend: { data: ['销售额', '毛利润'], top: 25 },
      xAxis: { type: 'category', data: ['10月', '11月', '12月', '1月', '2月', '3月'] },
      yAxis: { type: 'value', name: '金额 (元)' },
      series: [
        { name: '销售额', type: 'line', data: [45000, 52000, 48000, 85000, 76000, 128500], smooth: true },
        { name: '毛利润', type: 'line', data: [12000, 15000, 14000, 28000, 25000, 42000], smooth: true }
      ]
    })
  }
}

// 监听 Tab 切换，重新渲染对应的图表以防止宽度计算错误
watch(activeTab, async () => {
  await nextTick()
  renderCharts()
})

onMounted(() => {
  renderCharts()
})

const exportReport = () => {
  ElMessage.success('报表数据已生成并开始下载 (Excel格式)')
}
</script>
