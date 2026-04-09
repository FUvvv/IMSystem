<template>
  <el-card>
    <template #header>
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
          <el-input v-model="searchKeyword" placeholder="输入商品名称或分类" style="width: 200px; margin-right: 10px;" clearable />
          <el-button type="primary" @click="handleSearch">查询</el-button>
          <el-button @click="resetSearch">显示全部</el-button>
        </div>
        <el-button type="success" @click="openDialog('add')">新增商品</el-button>
      </div>
    </template>

    <el-table :data="products" border style="width: 100%" v-loading="loading">
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="name" label="商品名称" />
      <el-table-column prop="category" label="分类" width="100" />
      <el-table-column prop="specifications" label="规格" width="120" />
      <el-table-column prop="produce_date" label="生产日期" width="120" />
      <el-table-column prop="batch_number" label="批号" width="150" />
      <el-table-column prop="price" label="单价(元)" width="100" />
      <el-table-column label="操作" width="150">
        <template #default="scope">
          <el-button size="small" @click="openDialog('edit', scope.row)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDelete(scope.row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 弹窗表单增加新字段 -->
    <el-dialog :title="dialogType === 'add' ? '新增商品' : '编辑商品'" v-model="dialogVisible" width="600px">
      <el-form :model="form" label-width="100px">
        <el-form-item label="商品名称"><el-input v-model="form.name"></el-input></el-form-item>
        <el-form-item label="商品分类">
          <el-select v-model="form.category" style="width: 100%;">
            <el-option label="电子产品" value="电子产品" />
            <el-option label="办公用品" value="办公用品" />
            <el-option label="日用百货" value="日用百货" />
          </el-select>
        </el-form-item>
        <el-form-item label="商品规格"><el-input v-model="form.specifications" placeholder="如: 500g/包"></el-input></el-form-item>
        <el-form-item label="生产日期">
          <el-date-picker v-model="form.produce_date" type="date" placeholder="选择日期" value-format="YYYY-MM-DD" style="width: 100%;" @change="generateBatchNumber" />
        </el-form-item>
        <el-form-item label="批号"><el-input v-model="form.batch_number" disabled placeholder="选择日期后自动生成"></el-input></el-form-item>
        <el-form-item label="商品单价"><el-input-number v-model="form.price" :min="0" :precision="2" style="width: 100%;"></el-input-number></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveProduct">确定</el-button>
      </template>
    </el-dialog>
  </el-card>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import axios from 'axios'

const apiBase = 'http://localhost:8000/api'
const products = ref([])
const loading = ref(false)
const searchKeyword = ref('')
const dialogVisible = ref(false)
const dialogType = ref('add')
const form = reactive({ id: null, name: '', category: '', specifications: '', produce_date: '', batch_number: '', price: 0 })

// 批号生成算法：分类首字母 + 日期去掉横杠 + 随机数
const generateBatchNumber = () => {
  if (!form.produce_date) return
  const dateStr = form.produce_date.replace(/-/g, '')
  const randomStr = Math.floor(Math.random() * 1000).toString().padStart(3, '0')
  form.batch_number = `BN-${dateStr}-${randomStr}`
}

const fetchProducts = async () => {
  loading.value = true
  const params = searchKeyword.value ? { search: searchKeyword.value } : {}
  const res = await axios.get(`${apiBase}/products`, { params })
  products.value = res.data
  loading.value = false
}

const handleSearch = () => fetchProducts()
const resetSearch = () => {
  searchKeyword.value = ''
  fetchProducts()
}

const openDialog = (type, row = null) => {
  dialogType.value = type
  if (type === 'edit') Object.assign(form, row)
  else Object.assign(form, { id: null, name: '', category: '', specifications: '', produce_date: '', batch_number: '', price: 0 })
  dialogVisible.value = true
}

const saveProduct = async () => {
  try {
    if (dialogType.value === 'add') await axios.post(`${apiBase}/products`, form)
    else await axios.put(`${apiBase}/products/${form.id}`, form)
    ElMessage.success('保存成功')
    dialogVisible.value = false
    fetchProducts()
  } catch (e) { ElMessage.error('操作失败') }
}

const handleDelete = (id) => {
  ElMessageBox.confirm('确认删除?', '警告', { type: 'warning' }).then(async () => {
    await axios.delete(`${apiBase}/products/${id}`)
    ElMessage.success('删除成功')
    fetchProducts()
  }).catch(() => {})
}

onMounted(() => fetchProducts())
</script>
