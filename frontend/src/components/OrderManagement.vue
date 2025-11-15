<template>
  <div>
    <h2>订单管理</h2>
    
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>创建新订单</span>
        </div>
      </template>
      
      <el-form :model="orderForm" :rules="rules" ref="orderFormRef" label-width="100px">
        <el-form-item label="用户ID" prop="user_id">
          <el-input-number v-model="orderForm.user_id" :min="1" placeholder="请输入用户ID"></el-input-number>
        </el-form-item>
        <el-form-item label="产品ID" prop="product_id">
          <el-input-number v-model="orderForm.product_id" :min="1" placeholder="请输入产品ID"></el-input-number>
        </el-form-item>
        <el-form-item label="数量" prop="quantity">
          <el-input-number v-model="orderForm.quantity" :min="1" placeholder="请输入数量"></el-input-number>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitOrderForm">创建订单</el-button>
          <el-button @click="resetForm">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
    
    <el-card class="box-card" style="margin-top: 20px;">
      <template #header>
        <div class="card-header">
          <span>订单列表</span>
          <el-button type="primary" @click="loadOrders">刷新</el-button>
        </div>
      </template>
      
      <el-table :data="orders" v-loading="loading" style="width: 100%">
        <el-table-column prop="id" label="订单ID" width="100"></el-table-column>
        <el-table-column prop="user_id" label="用户ID" width="100"></el-table-column>
        <el-table-column prop="product_id" label="产品ID" width="100"></el-table-column>
        <el-table-column prop="quantity" label="数量" width="80"></el-table-column>
        <el-table-column prop="total_price" label="总价" width="120">
          <template #default="scope">
            ¥{{ scope.row.total_price }}
          </template>
        </el-table-column>
        <el-table-column prop="order_date" label="订单日期"></el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script>
import { orderService } from '../services/api'

export default {
  name: 'OrderManagement',
  data() {
    return {
      orders: [],
      loading: false,
      orderForm: {
        user_id: null,
        product_id: null,
        quantity: 1
      },
      rules: {
        user_id: [
          { required: true, message: '请输入用户ID', trigger: 'blur' }
        ],
        product_id: [
          { required: true, message: '请输入产品ID', trigger: 'blur' }
        ],
        quantity: [
          { required: true, message: '请输入数量', trigger: 'blur' },
          { type: 'number', min: 1, message: '数量必须大于0', trigger: 'blur' }
        ]
      }
    }
  },
  mounted() {
    this.loadOrders()
  },
  methods: {
    async loadOrders() {
      this.loading = true
      try {
        const response = await orderService.getOrders()
        if (response.data.success) {
          this.orders = response.data.data
        } else {
          this.$message.error('加载订单数据失败: ' + response.data.error)
        }
      } catch (error) {
        this.$message.error('请求失败: ' + error.message)
      } finally {
        this.loading = false
      }
    },
    
    async submitOrderForm() {
      this.$refs.orderFormRef.validate(async (valid) => {
        if (valid) {
          try {
            const response = await orderService.createOrder(this.orderForm)
            if (response.data.success) {
              this.$message.success(`订单创建成功！总价: ¥${response.data.total_price}`)
              this.resetForm()
              this.loadOrders()
            } else {
              this.$message.error('创建订单失败: ' + response.data.error)
            }
          } catch (error) {
            this.$message.error('请求失败: ' + error.message)
          }
        }
      })
    },
    
    resetForm() {
      this.orderForm = { user_id: null, product_id: null, quantity: 1 }
      this.$refs.orderFormRef?.resetFields()
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


