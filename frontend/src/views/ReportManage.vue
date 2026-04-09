<template>
  <div>
    <div style="margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center;">
      <h2>多维度数据报表与查询</h2>
      <el-button type="success" icon="Download" @click="exportDialogVisible = true">自定义导出报表</el-button>
    </div>

    <!-- 顶部数据概览卡片 -->
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

    <!-- 报表展示区 -->
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
                <el-table-column prop="min_alert" label="预警阈值" />
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

    <!-- 自定义导出配置弹窗 -->
    <el-dialog title="自定义报表导出" v-model="exportDialogVisible" width="500px">
      <el-form label-width="100px">
        <el-form-item label="报表模板">
          <el-radio-group v-model="exportConfig.templateType" @change="handleTemplateChange">
            <el-radio label="product">商品明细报表</el-radio>
            <el-radio label="inventory">库存状态报表</el-radio>
          </el-radio-group>
        </el-form-item>
        
        <el-form-item label="导出字段">
          <el-checkbox-group v-model="exportConfig.selectedFields">
            <el-checkbox v-for="field in currentAvailableFields" :key="field.key" :label="field.key">
              {{ field.label }}
            </el-checkbox>
          </el-checkbox-group>
        </el-form-item>

        <el-form-item label="导出格式">
          <el-radio-group v-model="exportConfig.format">
            <el-radio label="xlsx">Excel (.xlsx)</el-radio>
            <el-radio label="pdf">PDF (纯英文)</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="exportDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="executeCustomExport">生成并下载</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, nextTick, watch, computed } from 'vue'
import axios from 'axios'
import * as echarts from 'echarts'
// 注意：如果需要导出样式生效，请确保安装并引入了 xlsx-js-style，而不是普通的 xlsx
import * as XLSX from 'xlsx-js-style' 
import jsPDF from 'jspdf'
import autoTable from 'jspdf-autotable'
import { ElMessage } from 'element-plus'

const activeTab = ref('inventory')
const summary = ref({ product_count: 0, low_stock_count: 0 })
const productStats = ref([])
const inventoryStats = ref([])
const rawProducts = ref([]) 
const inventoryChartRef = ref(null)

const exportDialogVisible = ref(false)
const exportConfig = reactive({
  templateType: 'inventory',
  format: 'xlsx',
  selectedFields: ['name', 'stock', 'min_alert', 'status']
})

const templateFields = {
  product: [
    { key: 'id', label: '商品ID', enLabel: 'Product ID' },
    { key: 'name', label: '商品名称', enLabel: 'Product Name' },
    { key: 'category', label: '商品分类', enLabel: 'Category' },
    { key: 'specifications', label: '规格', enLabel: 'Specifications' },
    { key: 'price', label: '单价(元)', enLabel: 'Price (CNY)' },
    { key: 'production_date', label: '生产日期', enLabel: 'Production Date' },
    { key: 'batch_number', label: '批号', enLabel: 'Batch Number' }
  ],
  inventory: [
    { key: 'name', label: '商品名称', enLabel: 'Product Name' },
    { key: 'stock', label: '当前库存', enLabel: 'Current Stock' },
    { key: 'min_alert', label: '预警阈值', enLabel: 'Alert Threshold' },
    { key: 'status', label: '库存状态', enLabel: 'Stock Status' }
  ]
}

const currentAvailableFields = computed(() => templateFields[exportConfig.templateType])

const handleTemplateChange = (val) => {
  exportConfig.selectedFields = templateFields[val].map(f => f.key)
}

const fetchDashboardData = async () => {
  try {
    const res = await axios.get('http://localhost:8000/api/dashboard')
    summary.value = res.data.summary
    productStats.value = res.data.product_stats
    inventoryStats.value = res.data.inventory_stats
    
    const prodRes = await axios.get('http://localhost:8000/api/products')
    rawProducts.value = prodRes.data
    
    renderCharts()
  } catch (error) {
    if (error.response?.status === 403) {
      ElMessage.error("权限不足，仅管理员可查看报表数据")
    }
  }
}

const renderCharts = () => {
  if (inventoryChartRef.value && inventoryStats.value.length > 0) {
    const invChart = echarts.init(inventoryChartRef.value)
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

const executeCustomExport = () => {
  if (exportConfig.selectedFields.length === 0) {
    return ElMessage.warning('请至少选择一个导出字段')
  }

  let sourceData = []
  let reportTitle = ''
  let reportTitleEn = ''

  if (exportConfig.templateType === 'product') {
    reportTitle = '商品明细数据报表'
    reportTitleEn = 'Product Detail Data Report'
    sourceData = rawProducts.value.map(p => ({
      id: p.id, name: p.name, category: p.category, 
      specifications: p.specifications, price: p.price, 
      production_date: p.production_date, batch_number: p.batch_number
    }))
  } else {
    reportTitle = '库存状态监控报表'
    reportTitleEn = 'Inventory Status Monitoring Report'
    sourceData = inventoryStats.value.map(i => ({
      name: i.name, stock: i.stock, min_alert: i.min_alert, 
      status: i.stock < i.min_alert ? '库存预警' : '正常'
    }))
  }

  if (sourceData.length === 0) return ElMessage.warning('暂无数据可导出')

  if (exportConfig.format === 'pdf') {
    const doc = new jsPDF()
    
    doc.setFontSize(16)
    doc.text("XX Group Co., Ltd.", 14, 15)
    doc.setFontSize(14)
    doc.text(reportTitleEn, 14, 25)
    
    doc.setFontSize(10)
    doc.text(`Report No: REP-${new Date().getTime()}`, 14, 35)
    doc.text(`Generated At: ${new Date().toLocaleString()}`, 14, 42)
    doc.text(`Export Dept: Data Center`, 100, 42)
    doc.text(`Exported By: Admin`, 150, 42)

    const head = [exportConfig.selectedFields.map(key => {
      return currentAvailableFields.value.find(f => f.key === key).enLabel
    })]

    const body = sourceData.map(item => {
      return exportConfig.selectedFields.map(key => {
        let val = item[key]
        if (key === 'status') {
          val = val === '库存预警' ? 'Low Stock' : 'Normal'
        }
        return val
      })
    })

    autoTable(doc, {
      startY: 50,
      head: head,
      body: body,
      theme: 'grid',
      headStyles: { fillColor: [64, 158, 255] }
    })

    const finalY = doc.lastAutoTable.finalY || 50
    doc.text("Prepared by: ______________   Reviewed by: ______________   Approved by: ______________", 14, finalY + 20)

    doc.save(`${reportTitleEn.replace(/ /g, '_')}_${new Date().getTime()}.pdf`)
    exportDialogVisible.value = false
    ElMessage.success('PDF 报表生成成功！')
    return
  }

  // === Excel 导出 (样式控制) ===
  const colCount = exportConfig.selectedFields.length 
  const maxColIndex = Math.max(colCount - 1, 3);
  
  // 1. 构造 AoA (Array of Arrays) 数据结构
  const excelData = []
  excelData.push(["XX集团有限公司"]) // Row 1
  excelData.push([reportTitle])      // Row 2
  excelData.push([`报表编号: REP-${new Date().getTime()}`]) // Row 3
  
  // Header Row 4
  const headers = exportConfig.selectedFields.map(key => {
    return currentAvailableFields.value.find(f => f.key === key).label
  })
  excelData.push(headers)
  
  // Data Rows 5+
  sourceData.forEach(item => {
    const row = exportConfig.selectedFields.map(key => item[key])
    excelData.push(row)
  })

  // Footer Rows
  excelData.push([`生成时间: ${new Date().toLocaleString()}`])
  excelData.push([`导出部门: 数据中心`])
  excelData.push([`导出人: Admin`])
  excelData.push([`制表人：______________   审核人：______________   批准人：______________`])

  const ws = XLSX.utils.aoa_to_sheet(excelData)

  // 2. 边框通用样式设置
  const borderStyle = {
    top: { style: 'thin', color: { rgb: "000000" } },
    bottom: { style: 'thin', color: { rgb: "000000" } },
    left: { style: 'thin', color: { rgb: "000000" } },
    right: { style: 'thin', color: { rgb: "000000" } }
  }

  // 3. 遍历所有单元格应用样式
  const range = XLSX.utils.decode_range(ws['!ref']);
  for (let R = range.s.r; R <= range.e.r; ++R) {
    for (let C = range.s.c; C <= range.e.c; ++C) {
      const cellAddress = {c: C, r: R};
      const cellRef = XLSX.utils.encode_cell(cellAddress);
      
      // 如果单元格为空，为了显示合并和边框，需要初始化它
      if (!ws[cellRef]) ws[cellRef] = { t: 's', v: '' };

      const cell = ws[cellRef];
      
      // 基础样式：仿宋，14号，左对齐，黑色边框
      let cellStyle = {
        font: { name: '仿宋', sz: 14, bold: false },
        alignment: { horizontal: 'left', vertical: 'center' },
        border: borderStyle
      };

      if (R === 0) {
        // 第一行：公司名，仿宋24加粗，居中
        cellStyle.font = { name: '仿宋', sz: 24, bold: true };
        cellStyle.alignment = { horizontal: 'center', vertical: 'center' };
      } else if (R === 1) {
        // 第二行：表单名，仿宋18加粗，居中
        cellStyle.font = { name: '仿宋', sz: 18, bold: true };
        cellStyle.alignment = { horizontal: 'center', vertical: 'center' };
      } else if (R === 2) {
        // 第三行：报表编号，仿宋14加粗，左对齐
        cellStyle.font = { name: '仿宋', sz: 14, bold: true };
      } else if (R === 3) {
        // 第四行：商品属性，仿宋14加粗，左对齐
        cellStyle.font = { name: '仿宋', sz: 14, bold: true };
      }

      cell.s = cellStyle;
    }
  }

  // 4. 设置行高 (!rows)
  const rowsHeight = [
    { hpt: 32 }, // 第一行 32磅
    { hpt: 22 }, // 第二行 22磅
    { hpt: 20 }, // 第三行 20磅
  ];
  // 从第四行到最后一行，均为 20磅
  for (let i = 3; i <= range.e.r; i++) {
    rowsHeight.push({ hpt: 20 });
  }
  ws['!rows'] = rowsHeight;

  // 5. 设置列宽 (!cols)
  ws['!cols'] = Array(Math.max(colCount, 4)).fill({ wch: 22 });

  // 6. 设置合并单元格 (!merges)
  const dataRowCount = sourceData.length;
  const footerStartRow = 4 + dataRowCount; // Header是第3行(索引)，数据占 dataRowCount 行

  ws['!merges'] = [
    { s: { r: 0, c: 0 }, e: { r: 0, c: maxColIndex } }, // 第一行合并
    { s: { r: 1, c: 0 }, e: { r: 1, c: maxColIndex } }, // 第二行合并
    { s: { r: 2, c: 0 }, e: { r: 2, c: maxColIndex } }, // 第三行合并
    // Footer 四行合并
    { s: { r: footerStartRow, c: 0 }, e: { r: footerStartRow, c: maxColIndex } },
    { s: { r: footerStartRow + 1, c: 0 }, e: { r: footerStartRow + 1, c: maxColIndex } },
    { s: { r: footerStartRow + 2, c: 0 }, e: { r: footerStartRow + 2, c: maxColIndex } },
    { s: { r: footerStartRow + 3, c: 0 }, e: { r: footerStartRow + 3, c: maxColIndex } }
  ];

  const wb = XLSX.utils.book_new()
  XLSX.utils.book_append_sheet(wb, ws, '报表数据')
  XLSX.writeFile(wb, `${reportTitle}_${new Date().getTime()}.xlsx`)
  
  exportDialogVisible.value = false
  ElMessage.success('Excel 报表生成成功！')
}

onMounted(() => fetchDashboardData())
</script>
