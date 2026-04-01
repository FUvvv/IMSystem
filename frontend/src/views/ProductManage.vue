<template>
  <el-card>
    <template #header>
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <span>商品管理</span>
        <el-button type="primary" @click="openDialog('add')">新增商品</el-button>
      </div>
    </template>

    <!-- 商品列表 -->
    <el-table :data="products" border style="width: 100%">
      <el-table-column prop="id" label="商品ID" width="100" />
      <el-table-column prop="name" label="商品名称" />
      <el-table-column prop="category" label="商品分类" />
      <el-table-column prop="price" label="单价 (元)" width="150" />
      <el-table-column label="操作" width="200">
        <template #default="scope">
          <el-button size="small" @click="openDialog('edit', scope.row)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDelete(scope.row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 新增/编辑弹窗 -->
    <el-dialog :title="dialogType === 'add' ? '新增商品' : '编辑商品'" v-model="dialogVisible" width="500px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="商品名称">
          <el-input v-model="form.name" placeholder="请输入商品名称"></el-input>
        </el-form-item>
        <el-form-item label="商品分类">
          <el-select v-model="form.category" placeholder="请选择分类" style="width: 100%;">
            <el-option label="电子产品" value="电子产品" />
            <el-option label="办公用品" value="办公用品" />
            <el-option label="日用百货" value="日用百货" />
          </el-select>
        </el-form-item>
        <el-form-item label="商品单价">
          <el-input-number v-model="form.price" :min="0" :precision="2" :step="1" style="width: 100%;"></el-input-number>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveProduct">确定</el-button>
      </template>
    </el-dialog>
  </el-card>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

// 模拟数据
const products = ref([
  { id: 1, name: '联想ThinkPad笔记本', category: '电子产品', price: 5999.00 },
  { id: 2, name: '得力A4打印纸', category: '办公用品', price: 25.50 }
])

const dialogVisible = ref(false)
const dialogType = ref('add') // add 或 edit
const form = reactive({ id: null, name: '', category: '', price: 0 })

const openDialog = (type, row = null) => {
  dialogType.value = type
  if (type === 'edit' && row) {
    Object.assign(form, row)
  } else {
    Object.assign(form, { id: null, name: '', category: '', price: 0 })
  }
  dialogVisible.value = true
}

const saveProduct = () => {
  if (dialogType.value === 'add') {
    products.value.push({ ...form, id: Date.now() })
    ElMessage.success('新增成功')
  } else {
    const index = products.value.findIndex(p => p.id === form.id)
    if (index !== -1) products.value[index] = { ...form }
    ElMessage.success('修改成功')
  }
  dialogVisible.value = false
}

const handleDelete = (id) => {
  ElMessageBox.confirm('确认删除该商品吗?', '提示', { type: 'warning' }).then(() => {
    products.value = products.value.filter(p => p.id !== id)
    ElMessage.success('删除成功')
  }).catch(() => {})
}
</script>
