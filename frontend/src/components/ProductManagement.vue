<template>
  <div>
    <h2>产品管理</h2>
    
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>添加新产品</span>
        </div>
      </template>
      
      <el-form :model="productForm" :rules="rules" ref="productFormRef" label-width="100px">
        <el-form-item label="产品名称" prop="name">
          <el-input v-model="productForm.name" placeholder="请输入产品名称"></el-input>
        </el-form-item>
        <el-form-item label="价格" prop="price">
          <el-input-number v-model="productForm.price" :min="0" :precision="2" placeholder="请输入价格"></el-input-number>
        </el-form-item>
        <el-form-item label="分类" prop="category">
          <el-input v-model="productForm.category" placeholder="请输入分类"></el-input>
        </el-form-item>
        <el-form-item label="库存数量" prop="stock_quantity">
          <el-input-number v-model="productForm.stock_quantity" :min="0" placeholder="请输入库存数量"></el-input-number>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitProductForm">添加产品</el-button>
          <el-button @click="resetForm">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
    
    <el-card class="box-card" style="margin-top: 20px;">
      <template #header>
        <div class="card-header">
          <span>产品列表</span>
          <el-button type="primary" @click="loadProducts">刷新</el-button>
        </div>
      </template>
      
      <el-table :data="products" v-loading="loading" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80"></el-table-column>
        <el-table-column prop="name" label="产品名称"></el-table-column>
        <el-table-column prop="price" label="价格" width="120">
          <template #default="scope">
            ¥{{ scope.row.price }}
          </template>
        </el-table-column>
        <el-table-column prop="category" label="分类"></el-table-column>
        <el-table-column prop="stock_quantity" label="库存" width="100"></el-table-column>
        <el-table-column prop="created_at" label="创建时间"></el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script>
import { productService } from '../services/api'

export default {
  name: 'ProductManagement',
  data() {
    return {
      products: [],
      loading: false,
      productForm: {
        name: '',
        price: 0,
        category: '',
        stock_quantity: 0
      },
      rules: {
        name: [
          { required: true, message: '请输入产品名称', trigger: 'blur' }
        ],
        price: [
          { required: true, message: '请输入价格', trigger: 'blur' },
          { type: 'number', min: 0, message: '价格必须大于等于0', trigger: 'blur' }
        ]
      }
    }
  },
  mounted() {
    this.loadProducts()
  },
  methods: {
    async loadProducts() {
      this.loading = true
      try {
        const response = await productService.getProducts()
        if (response.data.success) {
          this.products = response.data.data
        } else {
          this.$message.error('加载产品数据失败: ' + response.data.error)
        }
      } catch (error) {
        this.$message.error('请求失败: ' + error.message)
      } finally {
        this.loading = false
      }
    },
    
    async submitProductForm() {
      this.$refs.productFormRef.validate(async (valid) => {
        if (valid) {
          try {
            const response = await productService.createProduct(this.productForm)
            if (response.data.success) {
              this.$message.success('产品添加成功')
              this.resetForm()
              this.loadProducts()
            } else {
              this.$message.error('添加产品失败: ' + response.data.error)
            }
          } catch (error) {
            this.$message.error('请求失败: ' + error.message)
          }
        }
      })
    },
    
    resetForm() {
      this.productForm = { name: '', price: 0, category: '', stock_quantity: 0 }
      this.$refs.productFormRef?.resetFields()
    }
  }
}
</script>

<style scoped>
.box-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>


